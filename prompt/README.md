# Prompt

This folder contains the prompt used for the LLM-guided refactoring runs.

The main prompt targets the class with the highest number of surviving mutants. For later runs, the same prompt was reused by changing the target rank, for example from "highest" to "second-highest", "third-highest", or "fourth-highest".

An example adapted prompt is included to show how this change was made.

The prompts were used in Cline. The prompt was first copied into Cline while using Plan mode. After the planning step was finished, Cline was switched to Act mode to apply the refactoring and generate tests.
