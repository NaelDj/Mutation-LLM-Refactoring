Refactor the class with the fifth-highest number of survived mutants to increase observability of internally mutated behavior indicated by surviving mutants, enabling tests to distinguish correct from incorrect behavior. Surviving mutants may indicate insufficient observability when mutated behavior occurs internally but cannot be observed or asserted on by tests, leaving the test suite unable to distinguish behavioral differences. After refactoring, add new tests that make the previously unobservable behavior observable: directly test the new observable behavior introduced by the refactoring with focused inputs that distinguish correct behavior from the mutated alternatives indicated by the surviving mutants. Before each refactoring step, briefly state: (a) which surviving mutant(s) (by location/description) you are targeting, (b) what refactoring technique you will apply, and (c) why this increases observability and what new assertion it enables. To run PIT and the tests, please use the scripts provided in the tools folder. To analyse the mutants, you can use only the tools provided in the MCP server. PIT was already run beforehand once, so it is not needed to run it again to be able to retrieve the baseline results. Do not run PIT after each change. Only run PIT once at the end of the iteration to evaluate the effect of the refactoring + new tests. You may run unit tests iteratively as needed to check correctness while developing.

Checkpoint

Compare

Restore

Thinking

I'll help you refactor the class with the fifth-highest number of survived mutants. Let me start by analyzing the PIT results to identify which class that is.

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_classes

Auto-approve

Return per-class PIT mutation scores (test strength) for a workspace. Uses the latest mutations.xml under <workspace>/target/pit-reports.A null mutationScore means the class was not covered by any tests (i.e., no mutants were executed; only NO_COVERAGE mutants exist).

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

I can see that the class with the fifth-highest number of survived mutants is __PiePlot3D__ with 177 surviving mutants. Let me gather detailed information about the surviving mutants in this class.

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_methods

Auto-approve

Return per-method mutation scores (test strength) for a given class, using the latest PIT mutations.xml under <workspace>/target/pit-reports. A null mutationScore means that method had no mutants executed by tests (covered=0; only NO_COVERAGE).

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart",
  "className": "org.jfree.chart.plot.PiePlot3D"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_survivors_for_method

Auto-approve

Return surviving PIT mutants (status=SURVIVED) for a specific method in a class, using the latest mutations.xml under <workspace>/target/pit-reports. Pass methodDesc (JVM descriptor) for exact overload matching; if null, results are grouped by signature. In the response, requestedMethodDesc=null means no overload was specified, and sourceFile is provided only when all survivors map to the same file.

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart",
  "className": "org.jfree.chart.plot.PiePlot3D",
  "method": "draw",
  "methodDesc": "(Ljava/awt/Graphics2D;Ljava/awt/geom/Rectangle2D;Ljava/awt/geom/Point2D;Lorg/jfree/chart/plot/PlotState;Lorg/jfree/chart/plot/PlotRenderingInfo;)V"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

Let me get a complete list of all classes with their mutation scores to identify the fifth-highest:

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_classes

Auto-approve

Return per-class PIT mutation scores (test strength) for a workspace. Uses the latest mutations.xml under <workspace>/target/pit-reports.A null mutationScore means the class was not covered by any tests (i.e., no mutants were executed; only NO_COVERAGE mutants exist).

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

Let me read the PiePlot3D class to understand its current structure:

Cline read 1 file, performed 1 search:

src/main/java/org/jfree/chart/plot/PiePlot3D.java‎

"PiePlot3D" in src/test/java/org/jfree/chart/plot/‎

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_methods

Auto-approve

Return per-method mutation scores (test strength) for a given class, using the latest PIT mutations.xml under <workspace>/target/pit-reports. A null mutationScore means that method had no mutants executed by tests (covered=0; only NO_COVERAGE).

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart",
  "className": "org.jfree.chart.plot.PiePlot3D"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_survivors_for_method

Auto-approve

Return surviving PIT mutants (status=SURVIVED) for a specific method in a class, using the latest mutations.xml under <workspace>/target/pit-reports. Pass methodDesc (JVM descriptor) for exact overload matching; if null, results are grouped by signature. In the response, requestedMethodDesc=null means no overload was specified, and sourceFile is provided only when all survivors map to the same file.

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart",
  "className": "org.jfree.chart.plot.PiePlot3D",
  "method": "draw",
  "methodDesc": "(Ljava/awt/Graphics2D;Ljava/awt/geom/Rectangle2D;Ljava/awt/geom/Point2D;Lorg/jfree/chart/plot/PlotState;Lorg/jfree/chart/plot/PlotRenderingInfo;)V"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

Cline read 1 file:

src/test/java/org/jfree/chart/plot/PiePlot3DTest.java‎

Plan Created

I've analyzed the PIT mutation results and identified that __PiePlot3D__ is the class with the fifth-highest number of survived mutants (177 total survivors). I've gathered detailed information about the surviving mutants and existing test coverage.

## Current Situation

__PiePlot3D__ has 177 surviving mutants distributed across:

- `draw()` method: __128 survivors__ (the main problem area)
- `drawSide()` method: 36 survivors
- `isAngleAtFront()`, `isAngleAtBack()`: 3 survivors each
- `getDarkerSides()`, `equals()`: 2 survivors each
- Various setters and constructor: 1 survivor each

The existing test file (`PiePlot3DTest.java`) only has 3 basic tests:

1. `testEquals()` - property equality testing
2. `testSerialization()` - serialization round-trip
3. `testDrawWithNullDataset()` - null-safety check

## Core Problem

The `draw()` method has 128 surviving mutants because it performs complex internal calculations for pie geometry (areas, radii, centers, angles) that are __not observable__ from outside. The method:

- Calculates geometric properties internally
- Stores them in a `PiePlotState` object
- Performs rendering operations
- But provides no way for tests to verify the computed values are correct

Surviving mutants include:

- __Math mutations__: addition↔subtraction, multiplication↔division in geometric calculations
- __Removed method calls__: to `setPieArea()`, `setPieCenterX()`, `setPieWRadius()`, etc.
- __Negated conditionals__: in branching logic
- __Removed rendering calls__: to `setPaint()`, `fill()`, `draw()`, etc.

## Refactoring Strategy

I propose a __test-driven refactoring__ approach focusing on the highest-impact areas:

### Phase 1: Extract and Test Angle Utilities (6 survivors)

__Target__: `isAngleAtFront()` and `isAngleAtBack()` methods (3 survivors each)

- __Refactoring__: Make these methods `public` instead of `private` (or `protected`)
- __Why__: These are pure mathematical functions that should be directly testable
- __New tests__: Test boundary cases (0°, 90°, 180°, 270°, 360°) and various angles to distinguish correct behavior from mutated alternatives

### Phase 2: Make Paint Modification Observable (2+ survivors)

__Target__: `darkerSides` feature and `getDarkerSides()` method

- __Refactoring__: Extract `Paint applyDarkerSides(Paint original, boolean darker)` method
- __Why__: Currently the `darkerSides` feature is only tested via `equals()`, not functionally. The paint modification happens internally in `drawSide()` and isn't observable.
- __New tests__: Test that the method correctly darkens colors when enabled, returns original when disabled

### Phase 3: Extract Geometric Calculation Methods (50+ survivors)

__Target__: Mathematical calculations in `draw()` method for pie geometry

- __Refactoring__: Extract protected/package-private methods like:

  - `calculateLinkArea(Rectangle2D pieArea, double depthFactor)` → `Rectangle2D`
  - `calculateExplodedPieArea(Rectangle2D linkArea, double linkMargin)` → `Rectangle2D`
  - `calculatePieArea(Rectangle2D explodeArea, double maxExplodePercent)` → `Rectangle2D`
  - `calculatePieDepth(Rectangle2D pieArea, double depthFactor)` → `int`

- __Why__: These calculations are currently embedded in `draw()` with many surviving math mutants. Extracting them makes the computed values directly testable.

- __New tests__: Test each calculation method with specific inputs and verify the output dimensions, positions, and relationships

### Phase 4: Test State-Setting Side Effects (20+ survivors)

__Target__: Calls to `state.setPieArea()`, `state.setPieCenterX()`, etc.

- __Refactoring__: Create a test-friendly subclass or add a getter method to access the `PiePlotState` after drawing
- __Why__: These state-setting operations have "removed call" mutants that survive because tests don't verify the state was actually set
- __New tests__: After calling `draw()`, verify the `PiePlotState` contains expected values for pieArea, center coordinates, radii

## Expected Impact

This refactoring should:

- Kill __60-80 survivors__ by making internal calculations directly testable
- Improve code maintainability by separating calculation from rendering logic
- Make the class easier to understand and modify
- Follow the Single Responsibility Principle better

## Next Steps

Once you toggle to

Act Mode (⌘⇧A), I'll:

1. Start with Phase 1 (angle utilities) as a warm-up - quick win, low risk
2. Proceed through phases systematically
3. Run tests after each refactoring to ensure correctness
4. Add comprehensive new tests for each extracted method
5. Run PIT once at the end to measure the improvement

Would you like me to proceed with this plan?
