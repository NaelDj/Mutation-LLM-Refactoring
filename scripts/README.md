# CK Metric Extraction Scripts

This folder contains scripts used to extract readability-related metrics from CK output files after the thesis runs.

The CK result folders are included in the main replication package under:

```text
data/ck_results/
```

The expected structure is:

```text
data/ck_results/
├── jfreechart/
│   ├── base/
│   │   ├── class.csv
│   │   └── method.csv
│   ├── p2_run1/
│   │   ├── class.csv
│   │   └── method.csv
│   └── ...
├── bukkit/
│   ├── base/
│   │   ├── class.csv
│   │   └── method.csv
│   ├── p2_run1/
│   │   ├── class.csv
│   │   └── method.csv
│   └── ...
```

## Scripts

### `extract_class_metrics.py`

This script compares CK class-level metrics between the `base` folder and each `p2_runX` folder. It extracts the metrics for the class targeted in each run and writes the result to one CSV file.

The extracted class-level metrics are:

```text
wmc, maxNestedBlocksQty, loc, totalMethodsQty, variablesQty, loopQty, cbo
```

Example:

```bash
python extract_class_metrics.py \
  --root ../data/ck_results/bukkit \
  --output ../data/ck_results/output_csv/bukkit_class_metrics.csv
```

Windows PowerShell:

```powershell
python extract_class_metrics.py `
  --root ..\data\ck_results\bukkit `
  --output ..\data\ck_results\output_csv\bukkit_class_metrics.csv
```

### `extract_method_metrics_indiv.py`

This script compares CK method-level metrics between the `base` folder and each `p2_runX` folder. It extracts the targeted methods configured in the script and writes the result to an output folder.

The extracted method-level metrics are:

```text
wmc, maxNestedBlocksQty, loc, parametersQty, variablesQty, loopQty
```

Example:

```bash
python extract_method_metrics_indiv.py \
  --root ../data/ck_results/bukkit \
  --output-dir ../data/ck_results/output_csv/bukkit_methods
```

Windows PowerShell:

```powershell
python extract_method_metrics_indiv.py `
  --root ..\data\ck_results\bukkit `
  --output-dir ..\data\ck_results\output_csv\bukkit_methods
```

By default, this script writes one combined CSV file:

```text
all_method_metrics.csv
```

## Output modes

Both scripts support the same `--mode` argument:

```text
full              before, after, and delta values
delta             only delta values
delta_only        same as delta
ba                only before and after values
before_after_only same as ba
```

For example:

```bash
python extract_class_metrics.py \
  --root ../data/ck_results/bukkit \
  --output ../data/ck_results/output_csv/bukkit_class_metrics_delta.csv \
  --mode delta
```

## Important mappings

Both scripts contain hardcoded mappings that determine which classes or methods are extracted.

- `extract_class_metrics.py` uses `RUN_TO_CLASS`.
- `extract_method_metrics_indiv.py` uses `RUN_TO_TARGET`.

Before running the scripts, make sure these mappings match the project being analysed. For example, the Bukkit mapping should be used for the Bukkit CK results, while the JFreeChart mapping should be used for the JFreeChart CK results.

## Output columns

The class-level script always includes:

```text
repo, target_class, run, match_status
```

The method-level script always includes:

```text
repo, target_class, target_method, matched_method_full, target_overload, run, match_status
```

Depending on the selected mode, the output also includes before values, after values, delta values, or a combination of these.

## Match status

The `match_status` column shows whether the target class or method was matched correctly.

Common values are:

```text
ok
unmapped_run
missing_in_base
missing_in_run
multiple_matches
```

Only rows with `match_status` set to `ok` were used directly for the thesis analysis.