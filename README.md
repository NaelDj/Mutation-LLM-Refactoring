# Replication Package

This replication package contains the modified `pom.xml` files, Maven toolchain configuration, prompts, supporting scripts, and post-run analysis data used for the thesis.

The MCP server used in the thesis is available here: https://github.com/NaelDj/PIT-MCP-Server

This repository acts as the central replication package. The project-specific code changes and run branches are stored in the separate JFreeChart and Bukkit replication repositories linked below:

- The replication repository for JFreeChart is available here: https://github.com/NaelDj/JFreeChart-LLM-Refactoring

- The replication repository for Bukkit is available here: https://github.com/NaelDj/Bukkit-LLM-Refactoring

## Repository Structure

- `data/`: contains the post-run analysis data, including CK results, LLM output, and the targeted-mutant CSV file.
- `poms/`: contains the modified Maven `pom.xml` files and the Maven `toolchains.xml` file.
- `prompt/`: contains the prompts used for the LLM-guided refactoring runs.
- `scripts/`: contains scripts used to extract class-level and method-level readability metrics from CK output.
- `tools/`: contains the OS-specific scripts used inside the replication repositories to run tests and PIT mutation testing.

## Setup

1. Clone one of the replication repositories:

   - JFreeChart: https://github.com/NaelDj/JFreeChart-LLM-Refactoring
   - Bukkit: https://github.com/NaelDj/Bukkit-LLM-Refactoring

2. Copy the provided `toolchains.xml` file from the `poms` folder to your local Maven configuration folder:

   **Linux/macOS**

   ```bash
   ~/.m2/toolchains.xml
   ```

   **Windows**

   ```powershell
   %USERPROFILE%\.m2\toolchains.xml
   ```

3. Make sure the JDK path inside `toolchains.xml` matches the location of the required JDK on your machine.

4. Install Cline through the Visual Studio Code Extension Marketplace.

5. Clone and configure the MCP server using the instructions in the MCP server repository.

6. Copy one of the prompts from the `prompt` folder into Cline while using Plan mode.

7. After Plan mode is finished, switch Cline to Act mode and wait until it reports that the task is completed.

## Running Tests and PIT

The `tools` folder contains OS-specific scripts for running tests and PIT mutation testing. These scripts are intended to be used from the root of the JFreeChart or Bukkit replication repository.

**Windows**

```powershell
tools\windows\run_tests.cmd
tools\windows\run_pit.cmd
```

**Linux/macOS**

```bash
./tools/unix/run_tests.sh
./tools/unix/run_pit.sh
```

## Analysis Data and Scripts

The `data` folder contains post-run analysis material:

- `data/ck_results/`: CK output used for the readability analysis.
- `data/llm-output/`: LLM output from the thesis runs.
- `data/mutation_results_by_run.csv`: run-level mutation testing results before and after the LLM-guided refactoring runs.
- `data/targeted_mutants_location_and_categorized.csv`: targeted-mutant data used for the post-run analysis.

The `scripts` folder contains scripts for extracting readability metrics from the CK output:

- `extract_class_metrics.py`: extracts class-level before/after/delta metrics.
- `extract_method_metrics_indiv.py`: extracts method-level before/after/delta metrics for the targeted methods.

See `scripts/README.md` for the exact commands.
