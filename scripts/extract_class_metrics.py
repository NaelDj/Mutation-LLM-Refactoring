#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable


METRICS = [
    "wmc",
    "maxNestedBlocksQty",
    "loc",
    "totalMethodsQty",
    "variablesQty",
    "loopQty",
    "cbo",
]

MODE_ALIASES = {
    "full": "full",
    "delta": "delta_only",
    "delta_only": "delta_only",
    "ba": "before_after_only",
    "before_after_only": "before_after_only",
}

# Each p2_runX should map to the class that was actually targeted in that run.

# === Uncomment for JFreeChart ===
# RUN_TO_CLASS = {
#     "p2_run1": "org.jfree.chart.plot.XYPlot",
#     "p2_run2": "org.jfree.chart.plot.CategoryPlot",
#     "p2_run3": "org.jfree.chart.plot.PiePlot",
#     "p2_run4": "org.jfree.chart.plot.MeterPlot",
#     "p2_run5": "org.jfree.chart.plot.PiePlot3D",
#     "p2_run6": "org.jfree.chart.axis.CategoryAxis",
# }

# === Active mapping: Bukkit ===
RUN_TO_CLASS = {
    "p2_run1": "org.bukkit.plugin.messaging.StandardMessenger",
    "p2_run2": "org.bukkit.plugin.messaging.PluginMessageListenerRegistration",
    "p2_run3": "org.bukkit.configuration.MemorySection",
    "p2_run4": "org.bukkit.command.SimpleCommandMap",
    "p2_run5": "org.bukkit.command.Command",
    "p2_run6": "org.bukkit.configuration.file.FileConfiguration",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare CK class-level metrics between base and p2_runX folders."
    )
    parser.add_argument(
        "--root",
        dest="root_path",
        required=True,
        help="Path to repo root, e.g. .../jfreechart",
    )
    parser.add_argument(
        "--output",
        dest="output_csv",
        required=True,
        help="Output CSV path",
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
        raise ValueError(
            f"Missing required columns in {csv_path}: {', '.join(missing)}"
        )


def find_exact_class_matches(rows: list[dict[str, str]], target_class: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get("class") == target_class]


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


def main() -> int:
    args = parse_args()
    root_path = Path(args.root_path)
    output_csv = Path(args.output_csv)
    repo_name = root_path.name

    base_csv = root_path / "base" / "class.csv"
    base_rows = load_csv_rows(base_csv)
    require_columns(base_rows, ["class", *METRICS], base_csv)

    run_dirs = list_run_dirs(root_path)
    if not run_dirs:
        raise ValueError(f"No p2_runX folders found under {root_path}")

    output_rows: list[dict[str, object]] = []
    metric_columns = build_metric_columns(args.mode)

    for run_dir in run_dirs:
        run_name = run_dir.name
        target_class = RUN_TO_CLASS.get(run_name)

        row_out: dict[str, object] = {
            "repo": repo_name,
            "target_class": target_class,
            "run": run_name,
            "match_status": "",
        }

        if target_class is None:
            row_out["match_status"] = "unmapped_run"
            for col in metric_columns:
                row_out.setdefault(col, None)
            output_rows.append(row_out)
            continue

        base_matches = find_exact_class_matches(base_rows, target_class)
        if len(base_matches) == 0:
            base_status = "missing_in_base"
            base_row = None
        elif len(base_matches) > 1:
            base_status = "multiple_matches"
            base_row = None
        else:
            base_status = "ok"
            base_row = base_matches[0]

        run_csv = run_dir / "class.csv"
        run_rows = load_csv_rows(run_csv)
        require_columns(run_rows, ["class", *METRICS], run_csv)
        run_matches = find_exact_class_matches(run_rows, target_class)

        if base_status != "ok":
            row_out["match_status"] = base_status
        elif len(run_matches) == 0:
            row_out["match_status"] = "missing_in_run"
        elif len(run_matches) > 1:
            row_out["match_status"] = "multiple_matches"
        else:
            row_out["match_status"] = "ok"
            run_row = run_matches[0]

            for metric in METRICS:
                before = parse_number(base_row.get(metric) if base_row else None)
                after = parse_number(run_row.get(metric))

                if MODE_ALIASES[args.mode] in {"full", "before_after_only"}:
                    row_out[f"{metric}_before"] = before
                    row_out[f"{metric}_after"] = after

                if MODE_ALIASES[args.mode] in {"full", "delta_only"}:
                    row_out[f"{metric}_delta"] = subtract(after, before)

        for col in metric_columns:
            row_out.setdefault(col, None)

        output_rows.append(row_out)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["repo", "target_class", "run", "match_status", *metric_columns]

    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
