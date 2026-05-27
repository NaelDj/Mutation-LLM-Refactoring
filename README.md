# Replication Package

This replication package contains the modified `pom.xml` files, Maven toolchain configuration, supporting scripts, and prompts used for the thesis runs.

The MCP server used in the thesis is available here: https://github.com/NaelDj/PIT-MCPServer

The replication repository for JFreeChart is available here: https://github.com/NaelDj/mlr-jfreechart

The replication repository for Bukkit is available here: https://github.com/NaelDj/mlr-bukkit

## Setup

1. Clone one of the replication repositories:

   - JFreeChart: https://github.com/NaelDj/mlr-jfreechart
   - Bukkit: https://github.com/NaelDj/mlr-bukkit

2. Copy the provided `toolchains.xml` file to your local Maven configuration folder:

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

5. Connect the MCP server with Cline using the instructions in the MCP server repository.

6. Copy one of the prompts from the `prompt` folder into Cline while using Plan mode.

7. After Plan mode is finished, switch Cline to Act mode and wait until it reports that the task is completed.
