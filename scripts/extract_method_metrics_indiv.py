#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Iterable


METRICS = [
    "wmc",
    "maxNestedBlocksQty",
    "loc",
    "parametersQty",
    "variablesQty",
    "loopQty",
]

MODE_ALIASES = {
    "full": "full",
    "delta": "delta_only",
    "delta_only": "delta_only",
    "ba": "before_after_only",
    "before_after_only": "before_after_only",
}

# Hardcoded output layout:
# - "separate_csv" -> one CSV per class/method/overload
# - "one_csv"      -> one combined CSV with everything
OUTPUT_LAYOUT = "one_csv"
COMBINED_OUTPUT_FILENAME = "all_method_metrics.csv"

# Per run:
# - class required
# - methods:
#     - None or [] => export all methods in that class
#     - ["draw", "render"] => export only those methods
#
# Method matching rule:
# - "draw/5" matches only "draw/5"
# - "draw" matches "draw/0", "draw/1", "draw/5", etc.
# - "draw" does not match "drawAxes"
# RUN_TO_TARGET = {
#     "p2_run1": {
#         "class": "org.jfree.chart.plot.XYPlot",
#         "methods": ["draw"],
#     },
#     "p2_run2": {
#         "class": "org.jfree.chart.plot.CategoryPlot",
#         "methods": ["draw"],
#     },
#     "p2_run3": {
#         "class": "org.jfree.chart.plot.PiePlot",
#         "methods": ["drawPie"],
#     },
#     "p2_run4": {
#         "class": "org.jfree.chart.plot.MeterPlot",
#         "methods": ["drawTick"],
#     },
#     "p2_run5": {
#         "class": "org.jfree.chart.plot.PiePlot3D",
#         "methods": ["drawSide", "isAngleAtFront", "isAngleAtBack"],
#     },
#     "p2_run6": {
#         "class": "org.jfree.chart.axis.CategoryAxis",
#         "methods": ["drawCategoryLabels"],
#     },
# }

RUN_TO_TARGET = {
    "p2_run1": {
        "class": "org.bukkit.plugin.messaging.StandardMessenger",
        "methods": ["removeFromOutgoing", "getIncomingChannelRegistrations"],
    },
    "p2_run2": {
        "class": "org.bukkit.plugin.messaging.PluginMessageListenerRegistration",
        "methods": ["equals", "hashCode"],
    },
    "p2_run3": {
        "class": "org.bukkit.configuration.MemorySection",
        "methods": ["getInt", "getDouble", "getLong"],
    },
    "p2_run4": {
        "class": "org.bukkit.command.SimpleCommandMap",
        "methods": ["SimpleCommandMap", "register"],
    },
    "p2_run5": {
        "class": "org.bukkit.command.Command",
        "methods": ["isRegistered", "allowChangesFrom", "register", "setLabel", "setAliases"],
    },
    "p2_run6": {
        "class": "org.bukkit.configuration.file.FileConfiguration",
        "methods": ["save", "load"],
    },
}

# Preferred non-metric columns for overload identification, if present in CK output.
OVERLOAD_ID_CANDIDATES = [
    "signature",
    "parameters",
    "parameterTypes",
    "paramTypes",
    "returnType",
    "type",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare CK method-level metrics between base and p2_runX folders "
            "using hardcoded run/class/method mappings."
        )
    )
    parser.add_argument(
        "--root",
        dest="root_path",
        required=True,
        help="Path to repo root, e.g. .../jfreechart",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        required=True,
        help="Directory where CSV files will be written",
    )
    parser.add_argument(
        "--mode",
        default="full",
        choices=sorted(MODE_ALIASES.keys()),
        help="Export mode: full, delta/delta_only, ba/before_after_only",
    )
    return parser.parse_args()


def load_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    with csv_path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {csv_path}")
        return list(reader)


def require_columns(rows: list[dict[str, str]], required: Iterable[str], csv_path: Path) -> None:
    if not rows:
        with csv_path.open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            actual = set(reader.fieldnames or [])
    else:
        actual = set(rows[0].keys())

    missing = [col for col in required if col not in actual]
    if missing:
        raise ValueError(f"Missing required columns in {csv_path}: {', '.join(missing)}")


def normalize_method_name(method_value: str | None) -> str:
    if method_value is None:
        return ""
    return str(method_value).strip()


def parse_number(value: str | None) -> float | int | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if number.is_integer():
        return int(number)
    return number


def subtract(after: float | int | None, before: float | int | None) -> float | int | None:
    if after is None or before is None:
        return None
    result = after - before
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def build_metric_columns(mode: str) -> list[str]:
    cols: list[str] = []
    normalized = MODE_ALIASES[mode]
    for metric in METRICS:
        if normalized in {"full", "before_after_only"}:
            cols.append(f"{metric}_before")
            cols.append(f"{metric}_after")
        if normalized in {"full", "delta_only"}:
            cols.append(f"{metric}_delta")
    return cols


def list_run_dirs(root_path: Path) -> list[Path]:
    runs = [p for p in root_path.iterdir() if p.is_dir() and p.name.startswith("p2_run")]

    def sort_key(path: Path):
        suffix = path.name.replace("p2_run", "")
        return int(suffix) if suffix.isdigit() else sys.maxsize

    return sorted(runs, key=sort_key)


def clean_target_config() -> dict[str, dict[str, object]]:
    cleaned: dict[str, dict[str, object]] = {}
    for run_name, config in RUN_TO_TARGET.items():
        target_class = str(config.get("class", "")).strip()
        raw_methods = config.get("methods")

        if not target_class:
            continue

        if raw_methods is None:
            methods = None
        else:
            methods = [normalize_method_name(m) for m in raw_methods if normalize_method_name(m)]
            if not methods:
                methods = None

        cleaned[run_name] = {
            "class": target_class,
            "methods": methods,
        }
    return cleaned


def group_runs_by_class(cleaned_config: dict[str, dict[str, object]]) -> dict[str, list[tuple[str, list[str] | None]]]:
    grouped: dict[str, list[tuple[str, list[str] | None]]] = {}
    for run_name, config in cleaned_config.items():
        target_class = str(config["class"])
        target_methods = config["methods"]
        grouped.setdefault(target_class, []).append((run_name, target_methods))
    return grouped


def find_rows_for_class(rows: list[dict[str, str]], target_class: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get("class") == target_class]


def find_rows_for_class_and_method(
    rows: list[dict[str, str]],
    target_class: str,
    target_method: str,
) -> list[dict[str, str]]:
    return [
        row for row in rows
        if row.get("class") == target_class
        and method_matches(target_method, row.get("method"))
    ]


def method_names_from_rows(rows: list[dict[str, str]]) -> list[str]:
    names = {
        normalize_method_name(row.get("method"))
        for row in rows
        if normalize_method_name(row.get("method"))
    }
    return sorted(names)


def safe_filename(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)


def stable_row_sort_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(f"{k}={row.get(k, '')}" for k in sorted(row.keys()))


def available_overload_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []
    all_keys: set[str] = set()
    for row in rows:
        all_keys.update(row.keys())
    return [col for col in OVERLOAD_ID_CANDIDATES if col in all_keys]


def build_overload_descriptor(row: dict[str, str], overload_cols: list[str]) -> str:
    parts: list[str] = []
    for col in overload_cols:
        value = str(row.get(col, "")).strip()
        if value:
            parts.append(f"{col}={value}")
    return " | ".join(parts)


def assign_overload_labels(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    """
    Groups rows of the same class+normalized-method into overload buckets.

    Strategy:
    1. If useful overload-identifying columns exist, group by those.
    2. Otherwise fall back to ordinal buckets after stable sorting.
    """
    if not rows:
        return {}

    overload_cols = available_overload_columns(rows)

    if overload_cols:
        grouped: dict[str, list[dict[str, str]]] = {}
        for row in rows:
            descriptor = build_overload_descriptor(row, overload_cols)
            label = descriptor if descriptor else "overload1"
            grouped.setdefault(label, []).append(row)
        return grouped

    sorted_rows = sorted(rows, key=stable_row_sort_key)
    grouped: dict[str, list[dict[str, str]]] = {}
    for idx, row in enumerate(sorted_rows, start=1):
        grouped[f"overload{idx}"] = [row]
    return grouped


def collect_overload_labels_for_method(
    base_rows: list[dict[str, str]],
    run_rows_by_name: dict[str, list[dict[str, str]]],
    target_class: str,
    method_name: str,
    relevant_runs: list[str],
) -> list[str]:
    labels: set[str] = set()

    base_method_rows = find_rows_for_class_and_method(base_rows, target_class, method_name)
    for label in assign_overload_labels(base_method_rows).keys():
        labels.add(label)

    for run_name in relevant_runs:
        run_rows = run_rows_by_name[run_name]
        run_method_rows = find_rows_for_class_and_method(run_rows, target_class, method_name)
        for label in assign_overload_labels(run_method_rows).keys():
            labels.add(label)

    return sorted(labels)


def get_row_for_overload(
    rows: list[dict[str, str]],
    target_class: str,
    method_name: str,
    overload_label: str,
) -> tuple[str, dict[str, str] | None]:
    method_rows = find_rows_for_class_and_method(rows, target_class, method_name)
    grouped = assign_overload_labels(method_rows)

    matches = grouped.get(overload_label, [])
    if len(matches) == 0:
        return "missing", None
    if len(matches) > 1:
        return "multiple_matches", None
    return "ok", matches[0]


def method_matches(target_method: str, csv_method: str | None) -> bool:
    target = str(target_method).strip()
    actual = str(csv_method or "").strip()

    # Exact match always works
    if actual == target:
        return True

    # If target already specifies /..., require exact match only
    if "/" in target:
        return False

    # Otherwise allow only target/<something>
    return actual.startswith(target + "/")


def get_full_method_name(
    base_row: dict[str, str] | None,
    run_row: dict[str, str] | None,
    fallback: str,
) -> str:
    """
    Prefer the exact CK method name from the matched row.
    Usually base and run should agree; if not, prefer run, then base.
    """
    if run_row:
        value = normalize_method_name(run_row.get("method"))
        if value:
            return value
    if base_row:
        value = normalize_method_name(base_row.get("method"))
        if value:
            return value
    return fallback


def write_csv(output_csv: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if OUTPUT_LAYOUT not in {"separate_csv", "one_csv"}:
        raise ValueError(
            f"Invalid OUTPUT_LAYOUT={OUTPUT_LAYOUT!r}. "
            f"Use 'separate_csv' or 'one_csv'."
        )

    args = parse_args()
    root_path = Path(args.root_path)
    output_dir = Path(args.output_dir)
    repo_name = root_path.name

    base_csv = root_path / "base" / "method.csv"
    base_rows = load_csv_rows(base_csv)
    require_columns(base_rows, ["class", "method", *METRICS], base_csv)

    run_dirs = list_run_dirs(root_path)
    if not run_dirs:
        raise ValueError(f"No p2_runX folders found under {root_path}")

    run_rows_by_name: dict[str, list[dict[str, str]]] = {}
    for run_dir in run_dirs:
        run_csv = run_dir / "method.csv"
        run_rows = load_csv_rows(run_csv)
        require_columns(run_rows, ["class", "method", *METRICS], run_csv)
        run_rows_by_name[run_dir.name] = run_rows

    cleaned_config = clean_target_config()
    grouped_by_class = group_runs_by_class(cleaned_config)
    metric_columns = build_metric_columns(args.mode)
    output_dir.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "repo",
        "target_class",
        "target_method",
        "matched_method_full",
        "target_overload",
        "run",
        "match_status",
        *metric_columns,
    ]

    all_output_rows: list[dict[str, object]] = []

    for target_class, run_targets in grouped_by_class.items():
        ordered_run_targets = sorted(
            run_targets,
            key=lambda item: int(item[0].replace("p2_run", "")) if item[0].replace("p2_run", "").isdigit() else sys.maxsize
        )
        relevant_run_names = [run_name for run_name, _ in ordered_run_targets if run_name in run_rows_by_name]

        method_names: set[str] = set()
        for run_name, configured_methods in ordered_run_targets:
            if run_name not in run_rows_by_name:
                continue

            if configured_methods is None:
                base_class_rows = find_rows_for_class(base_rows, target_class)
                run_class_rows = find_rows_for_class(run_rows_by_name[run_name], target_class)
                method_names.update(method_names_from_rows(base_class_rows))
                method_names.update(method_names_from_rows(run_class_rows))
            else:
                method_names.update(configured_methods)

        for method_name in sorted(method_names):
            overload_labels = collect_overload_labels_for_method(
                base_rows=base_rows,
                run_rows_by_name=run_rows_by_name,
                target_class=target_class,
                method_name=method_name,
                relevant_runs=relevant_run_names,
            )

            if not overload_labels:
                continue

            for overload_label in overload_labels:
                output_rows: list[dict[str, object]] = []

                for run_name, configured_methods in ordered_run_targets:
                    if run_name not in run_rows_by_name:
                        continue

                    if configured_methods is not None and method_name not in configured_methods:
                        continue

                    row_out: dict[str, object] = {
                        "repo": repo_name,
                        "target_class": target_class,
                        "target_method": method_name,
                        "matched_method_full": "",
                        "target_overload": overload_label,
                        "run": run_name,
                        "match_status": "",
                    }

                    base_status, base_row = get_row_for_overload(
                        base_rows,
                        target_class,
                        method_name,
                        overload_label,
                    )
                    run_status, run_row = get_row_for_overload(
                        run_rows_by_name[run_name],
                        target_class,
                        method_name,
                        overload_label,
                    )

                    row_out["matched_method_full"] = get_full_method_name(
                        base_row=base_row,
                        run_row=run_row,
                        fallback=method_name,
                    )

                    if base_status == "missing":
                        row_out["match_status"] = "missing_in_base"
                    elif base_status == "multiple_matches":
                        row_out["match_status"] = "multiple_matches"
                    elif run_status == "missing":
                        row_out["match_status"] = "missing_in_run"
                    elif run_status == "multiple_matches":
                        row_out["match_status"] = "multiple_matches"
                    else:
                        row_out["match_status"] = "ok"

                        for metric in METRICS:
                            before = parse_number(base_row.get(metric) if base_row else None)
                            after = parse_number(run_row.get(metric) if run_row else None)

                            if MODE_ALIASES[args.mode] in {"full", "before_after_only"}:
                                row_out[f"{metric}_before"] = before
                                row_out[f"{metric}_after"] = after

                            if MODE_ALIASES[args.mode] in {"full", "delta_only"}:
                                row_out[f"{metric}_delta"] = subtract(after, before)

                    for col in metric_columns:
                        row_out.setdefault(col, None)

                    output_rows.append(row_out)
                    all_output_rows.append(dict(row_out))

                if OUTPUT_LAYOUT == "separate_csv":
                    if not output_rows:
                        continue

                    output_csv = output_dir / (
                        f"{safe_filename(repo_name)}__"
                        f"{safe_filename(target_class)}__"
                        f"{safe_filename(method_name)}__"
                        f"{safe_filename(overload_label)}.csv"
                    )
                    write_csv(output_csv, fieldnames, output_rows)

    if OUTPUT_LAYOUT == "one_csv":
        output_csv = output_dir / COMBINED_OUTPUT_FILENAME
        write_csv(output_csv, fieldnames, all_output_rows)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())