# Replication Package

This replication package contains the modified `pom.xml` files, Maven toolchain configuration, and supporting scripts used for the thesis runs.

The MCP server used in the thesis is available here: https://github.com/NaelDj/PIT-MCPServer
The replication repository for JFreeChart is available here: https://github.com/NaelDj/mlr-jfreechart

## Setup

1. Download or clone the specific project release mentioned in the thesis report.

2. Replace the project’s original `pom.xml` with the corresponding `pom.xml` from this replication package.

3. Copy the provided `toolchains.xml` file to your local Maven configuration folder:

**Linux/macOS**
```bash
~/.m2/toolchains.xml
```

**Windows**
```powershell
%USERPROFILE%\.m2\toolchains.xml
```

4. Make sure the JDK path inside `toolchains.xml` matches the location of the required JDK on your machine.

5. Copy the provided `tools` folder into the root of the project repository. The folder should be placed next to the project’s `pom.xml`, so the scripts can be run from the expected location.

6. Install Cline through the Visual Studio Code Extension Marketplace.

7. Connect the MCP server with Cline using the instructions in the MCP server repository.

8. Copy a prompt from prompt folder into Cline while using Plan mode.

9. After Plan mode is finished, switch Cline to Act mode and wait until it reports that the task is completed.
