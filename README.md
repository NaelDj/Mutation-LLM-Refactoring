# Replication Package

This replication package contains the modified `pom.xml` files, Maven toolchain configuration, prompts, supporting scripts, and post-run analysis data used for the thesis.

The MCP server used in the thesis is available here: https://github.com/NaelDj/PIT-MCP-Server

The replication repository for JFreeChart is available here: https://github.com/NaelDj/JFreeChart-LLM-Refactoring

The replication repository for Bukkit is available here: https://github.com/NaelDj/Bukkit-LLM-Refactoring

## Repository Structure

- `data/`: contains the CSV file used for the post-run targeted-mutant analysis.
- `poms/`: contains the modified Maven `pom.xml` files and the Maven `toolchains.xml` file.
- `prompt/`: contains the prompts used for the LLM-guided refactoring runs.
- `tools/`: contains the scripts used to run tests and PIT mutation testing.

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

The `tools` folder contains OS-specific scripts for running tests and PIT mutation testing.

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
