Refactor the class with the fourth-highest number of survived mutants to increase observability of internally mutated behavior indicated by surviving mutants, enabling tests to distinguish correct from incorrect behavior. Surviving mutants may indicate insufficient observability when mutated behavior occurs internally but cannot be observed or asserted on by tests, leaving the test suite unable to distinguish behavioral differences. After refactoring, add new tests that make the previously unobservable behavior observable: directly test the new observable behavior introduced by the refactoring with focused inputs that distinguish correct behavior from the mutated alternatives indicated by the surviving mutants. Before each refactoring step, briefly state: (a) which surviving mutant(s) (by location/description) you are targeting, (b) what refactoring technique you will apply, and (c) why this increases observability and what new assertion it enables. To run PIT and the tests, please use the scripts provided in the tools folder. To analyse the mutants, you can use only the tools provided in the MCP server. PIT was already run beforehand once, so it is not needed to run it again to be able to retrieve the baseline results. Do not run PIT after each change. Only run PIT once at the end of the iteration to evaluate the effect of the refactoring + new tests. You may run unit tests iteratively as needed to check correctness while developing.

138.8k200.0k

11/11

All tasks have been completed!

Checkpoint

Compare

Restore

Thinking

I'll help you refactor the class with the fourth-highest number of survived mutants to increase observability. Let me start by analyzing the PIT mutation results to identify which class we need to work on.

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

Perfect! I can see the PIT mutation results. The class with the fourth-highest number of survived mutants is __org.jfree.chart.plot.MeterPlot__ with __196 surviving mutants__.

Let me gather more detailed information about which methods in MeterPlot have the most surviving mutants.

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_methods

Auto-approve

Return per-method mutation scores (test strength) for a given class, using the latest PIT mutations.xml under <workspace>/target/pit-reports. A null mutationScore means that method had no mutants executed by tests (covered=0; only NO_COVERAGE).

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart",
  "className": "org.jfree.chart.plot.MeterPlot"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

Now let me examine the specific surviving mutants in the methods with the most survivors. Let me start with the `draw` method which has 71 surviving mutants:

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_survivors_for_method

Auto-approve

Return surviving PIT mutants (status=SURVIVED) for a specific method in a class, using the latest mutations.xml under <workspace>/target/pit-reports. Pass methodDesc (JVM descriptor) for exact overload matching; if null, results are grouped by signature. In the response, requestedMethodDesc=null means no overload was specified, and sourceFile is provided only when all survivors map to the same file.

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart",
  "className": "org.jfree.chart.plot.MeterPlot",
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

Let me also check the `drawTick` method which has 46 surviving mutants:

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_survivors_for_method

Auto-approve

Return surviving PIT mutants (status=SURVIVED) for a specific method in a class, using the latest mutations.xml under <workspace>/target/pit-reports. Pass methodDesc (JVM descriptor) for exact overload matching; if null, results are grouped by signature. In the response, requestedMethodDesc=null means no overload was specified, and sourceFile is provided only when all survivors map to the same file.

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart",
  "className": "org.jfree.chart.plot.MeterPlot",
  "method": "drawTick",
  "methodDesc": "(Ljava/awt/Graphics2D;Ljava/awt/geom/Rectangle2D;DZ)V"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

Cline read 2 files:

src/main/java/org/jfree/chart/plot/MeterPlot.java‎

src/test/java/org/jfree/chart/plot/MeterPlotTest.java‎

Plan Created

Based on the PIT mutation analysis, I can see that __MeterPlot__ has significant surviving mutants. Let me analyze the key findings:

## Analysis Summary

__MeterPlot__ has extensive surviving mutants in two main methods:

- `draw()`: 73 surviving mutants
- `drawTick()`: 46 surviving mutants

The surviving mutants reveal a critical __observability problem__: the code performs complex graphical calculations and drawing operations, but tests cannot observe the actual rendering results. The current test suite (MeterPlotTest.java) only tests:

- Property getters/setters
- Equals/cloning/serialization
- NO tests verify actual drawing correctness

## Root Cause Patterns

1. __VoidMethodCallMutator survivors__ (Graphics operations): Removing calls to `setPaint()`, `setStroke()`, `draw()`, `fill()` don't fail tests → drawing output not verified

2. __MathMutator survivors__ (Coordinate calculations): Arithmetic operations for positioning survive → exact positions not verified

3. __Conditional mutants survivors__: Boundary conditions and conditionals survive → edge cases not tested

## Refactoring Plan

I'll apply __Extract Method__ refactoring to separate calculation logic from drawing operations, making calculations observable and testable.

### Target Areas (in priority order):

__1. Tick Position Calculations__ (drawTick method, lines 1070-1081)

- Extract method: `calculateTickEndpoints(Rectangle2D meterArea, double value)`
- Returns: A data structure with the calculated coordinates
- Enables testing: Verify correct coordinate calculations for different angles/values

__2. Tick Label Positioning Logic__ (drawTick method, lines 1099-1112)

- Extract method: `calculateTickLabelPosition(Rectangle2D tickLabelBounds, double valueAngle, double x, double y)`
- Returns: Point2D with adjusted label position
- Enables testing: Verify label positioning for different angles (especially boundary cases at 90°, 270°, etc.)

__3. Needle Position Calculation__ (draw method, lines 847-853)

- Extract method: `calculateNeedlePosition(Rectangle2D meterArea, double value)`
- Returns: Data structure with needle endpoint coordinates
- Enables testing: Verify needle points to correct angle for given values

__4. Value-to-Angle Conversion__ (already public but needs better testing)

- Method exists: `valueToAngle(double value)`
- Add comprehensive tests: boundary values, range limits, various angles

Each extracted method will:

- Have clear inputs/outputs
- Be package-private or public (accessible to tests)
- Contain pure calculation logic without side effects
- Enable direct assertions on computed values

### Testing Strategy

For each extracted calculation method, write tests that:

- Use boundary values that trigger surviving mutants
- Assert exact coordinate values
- Cover different angle ranges (0-90, 90-180, etc.)
- Test edge cases (min/max range values, special angles)

This will kill mutants by making the previously unobservable internal calculations directly testable.

Would you like me to proceed with this refactoring plan? I'll need to toggle to

Act Mode (⌘⇧A) to implement the changes.

Checkpoint

Compare

Restore

Thinking

I'll now implement the refactoring plan to increase observability of MeterPlot's internal calculations. Let me start by extracting the calculation methods from the drawing code.

## Step 1: Extract Tick Position Calculation

__Targeting:__ Surviving mutants in lines 1070-1081 (MathMutator on coordinate calculations)

__Refactoring technique:__ Extract Method - separate coordinate calculation from drawing

__Why this increases observability:__ The tick endpoint coordinates are currently computed inline during drawing. By extracting them into a separate method that returns a data structure, tests can directly verify the calculations without needing to inspect rendered graphics.

Let me first create a data structure to hold tick endpoints:

Cline wants to create a new file:

/src/main/java/org/jfree/chart/plot/TickEndpoints.java‎

Checkpoint

Compare

Restore

Thinking

Now I'll extract the tick position calculation method in MeterPlot and refactor the drawTick method to use it:

Cline wants to edit this file:

/src/main/java/org/jfree/chart/plot/MeterPlot.java‎

1

```java
------- SEARCH
    /**
     * Draws a tick on the dial.
     *
     * @param g2  the graphics device.
     * @param meterArea  the meter area.
     * @param value  the tick value.
     * @param label  a flag that controls whether a value label is drawn.
     */
    protected void drawTick(Graphics2D g2, Rectangle2D meterArea,
                            double value, boolean label) {

        double valueAngle = valueToAngle(value);

        double meterMiddleX = meterArea.getCenterX();
        double meterMiddleY = meterArea.getCenterY();

        g2.setPaint(this.tickPaint);
        g2.setStroke(new BasicStroke(2.0f));

        double valueP2X;
        double valueP2Y;

        double radius = (meterArea.getWidth() / 2) + DEFAULT_BORDER_SIZE;
        double radius1 = radius - 15;

        double valueP1X = meterMiddleX
                + (radius * Math.cos(Math.PI * (valueAngle / 180)));
        double valueP1Y = meterMiddleY
                - (radius * Math.sin(Math.PI * (valueAngle / 180)));

        valueP2X = meterMiddleX
                + (radius1 * Math.cos(Math.PI * (valueAngle / 180)));
        valueP2Y = meterMiddleY
                - (radius1 * Math.sin(Math.PI * (valueAngle / 180)));

        Line2D.Double line = new Line2D.Double(valueP1X, valueP1Y, valueP2X,
                valueP2Y);
        g2.draw(line);
=======
    /**
     * Calculates the start and end points for a tick mark at the specified value.
     * This method performs the coordinate calculations without any drawing operations,
     * making the calculation logic testable and observable.
     *
     * @param meterArea  the meter area.
     * @param value  the tick value.
     *
     * @return The tick endpoints (never {@code null}).
     */
    protected TickEndpoints calculateTickEndpoints(Rectangle2D meterArea, double value) {
        double valueAngle = valueToAngle(value);
        
        double meterMiddleX = meterArea.getCenterX();
        double meterMiddleY = meterArea.getCenterY();
        
        double radius = (meterArea.getWidth() / 2) + DEFAULT_BORDER_SIZE;
        double radius1 = radius - 15;
        
        double valueP1X = meterMiddleX
                + (radius * Math.cos(Math.PI * (valueAngle / 180)));
        double valueP1Y = meterMiddleY
                - (radius * Math.sin(Math.PI * (valueAngle / 180)));
        
        double valueP2X = meterMiddleX
                + (radius1 * Math.cos(Math.PI * (valueAngle / 180)));
        double valueP2Y = meterMiddleY
                - (radius1 * Math.sin(Math.PI * (valueAngle / 180)));
        
        return new TickEndpoints(valueP1X, valueP1Y, valueP2X, valueP2Y);
    }

    /**
     * Draws a tick on the dial.
     *
     * @param g2  the graphics device.
     * @param meterArea  the meter area.
     * @param value  the tick value.
     * @param label  a flag that controls whether a value label is drawn.
     */
    protected void drawTick(Graphics2D g2, Rectangle2D meterArea,
                            double value, boolean label) {

        double valueAngle = valueToAngle(value);

        g2.setPaint(this.tickPaint);
        g2.setStroke(new BasicStroke(2.0f));

        TickEndpoints endpoints = calculateTickEndpoints(meterArea, value);
        
        Line2D.Double line = new Line2D.Double(endpoints.getX1(), endpoints.getY1(), 
                endpoints.getX2(), endpoints.getY2());
        g2.draw(line);
+++++++ REPLACE
```

Checkpoint

Compare

Restore

Thinking

I need to fix a compilation error - the variables `valueP2X` and `valueP2Y` are no longer available after the refactoring. Let me correct this:

Cline wants to edit this file:

/src/main/java/org/jfree/chart/plot/MeterPlot.java‎

1

```java
------- SEARCH
        if (this.tickLabelsVisible && label) {

            String tickLabel =  this.tickLabelFormat.format(value);
            g2.setFont(this.tickLabelFont);
            g2.setPaint(this.tickLabelPaint);

            FontMetrics fm = g2.getFontMetrics();
            Rectangle2D tickLabelBounds
                = TextUtils.getTextBounds(tickLabel, g2, fm);

            double x = valueP2X;
            double y = valueP2Y;
=======
        if (this.tickLabelsVisible && label) {

            String tickLabel =  this.tickLabelFormat.format(value);
            g2.setFont(this.tickLabelFont);
            g2.setPaint(this.tickLabelPaint);

            FontMetrics fm = g2.getFontMetrics();
            Rectangle2D tickLabelBounds
                = TextUtils.getTextBounds(tickLabel, g2, fm);

            double x = endpoints.getX2();
            double y = endpoints.getY2();
+++++++ REPLACE
```

Checkpoint

Compare

Restore

Thinking

Now let me verify that the refactoring didn't break anything by running the tests:

Cline wants to execute this command:

Completed

```shell
cd tools/windows && run_tests.cmd
```

```shell
At line:1 char:18
+ cd tools/windows && run_tests.cmd
+                  ~~
The token '&&' is not a valid statement separator in this version.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : InvalidEndOfLine
```

Checkpoint

Compare

Restore

Thinking

Cline wants to execute this command:

Completed

```shell
tools\windows\run_tests.cmd
```

```shell
TESTS: OK
```

Checkpoint

Compare

Restore

Thinking

Excellent! The tests pass. Now let me add focused tests for the newly extracted `calculateTickEndpoints` method. These tests will directly verify the coordinate calculations that were previously unobservable, targeting the surviving MathMutator mutants:

Cline wants to edit this file:

/src/test/java/org/jfree/chart/plot/MeterPlotTest.java‎

1

```java
------- SEARCH
    /**
     * Serialize an instance, restore it, and check for equality.
     */
    @Test
    public void testSerialization2() {
        MeterPlot p1 = new MeterPlot(new DefaultValueDataset(1.23));
        MeterPlot p2 = TestUtils.serialised(p1);
        assertEquals(p1, p2);

    }

}
=======
    /**
     * Serialize an instance, restore it, and check for equality.
     */
    @Test
    public void testSerialization2() {
        MeterPlot p1 = new MeterPlot(new DefaultValueDataset(1.23));
        MeterPlot p2 = TestUtils.serialised(p1);
        assertEquals(p1, p2);

    }

    /**
     * Tests the calculateTickEndpoints method with various values to ensure
     * coordinate calculations are correct. This test targets surviving mutants
     * in the tick endpoint calculation logic.
     */
    @Test
    public void testCalculateTickEndpoints() {
        MeterPlot plot = new MeterPlot();
        plot.setRange(new Range(0.0, 100.0));
        plot.setMeterAngle(270); // Default angle
        
        // Create a test meter area
        java.awt.geom.Rectangle2D meterArea = new java.awt.geom.Rectangle2D.Double(
                100, 100, 200, 200);
        
        // Test with value at minimum (0)
        TickEndpoints endpoints1 = plot.calculateTickEndpoints(meterArea, 0.0);
        assertNotNull(endpoints1);
        
        // Test with value at midpoint (50)
        TickEndpoints endpoints2 = plot.calculateTickEndpoints(meterArea, 50.0);
        assertNotNull(endpoints2);
        
        // Test with value at maximum (100)
        TickEndpoints endpoints3 = plot.calculateTickEndpoints(meterArea, 100.0);
        assertNotNull(endpoints3);
        
        // The outer and inner endpoints should be different
        assertNotEquals(endpoints1.getX1(), endpoints1.getX2());
        assertNotEquals(endpoints1.getY1(), endpoints1.getY2());
        
        // Different values should produce different endpoints
        assertFalse(endpoints1.getX1() == endpoints2.getX1() 
                && endpoints1.getY1() == endpoints2.getY1());
        assertFalse(endpoints2.getX1() == endpoints3.getX1() 
                && endpoints2.getY1() == endpoints3.getY1());
    }
    
    /**
     * Tests calculateTickEndpoints for specific angle calculations to verify
     * the mathematical operations. This targets MathMutator survivors.
     */
    @Test
    public void testCalculateTickEndpointsAngles() {
        MeterPlot plot = new MeterPlot();
        plot.setRange(new Range(0.0, 100.0));
        plot.setMeterAngle(270);
        
        java.awt.geom.Rectangle2D meterArea = new java.awt.geom.Rectangle2D.Double(
                0, 0, 100, 100);
        
        double centerX = meterArea.getCenterX(); // 50
        double centerY = meterArea.getCenterY(); // 50
        double radius = (meterArea.getWidth() / 2) + MeterPlot.DEFAULT_BORDER_SIZE; // 53
        double radius1 = radius - 15; // 38
        
        // Test at value 0 (should be at rightmost position due to valueToAngle)
        double angle0 = plot.valueToAngle(0.0);
        TickEndpoints endpoints0 = plot.calculateTickEndpoints(meterArea, 0.0);
        
        double expectedX1_0 = centerX + (radius * Math.cos(Math.PI * (angle0 / 180)));
        double expectedY1_0 = centerY - (radius * Math.sin(Math.PI * (angle0 / 180)));
        double expectedX2_0 = centerX + (radius1 * Math.cos(Math.PI * (angle0 / 180)));
        double expectedY2_0 = centerY - (radius1 * Math.sin(Math.PI * (angle0 / 180)));
        
        assertEquals(expectedX1_0, endpoints0.getX1(), 0.001);
        assertEquals(expectedY1_0, endpoints0.getY1(), 0.001);
        assertEquals(expectedX2_0, endpoints0.getX2(), 0.001);
        assertEquals(expectedY2_0, endpoints0.getY2(), 0.001);
        
        // Test at value 100 (should be at leftmost position)
        double angle100 = plot.valueToAngle(100.0);
        TickEndpoints endpoints100 = plot.calculateTickEndpoints(meterArea, 100.0);
        
        double expectedX1_100 = centerX + (radius * Math.cos(Math.PI * (angle100 / 180)));
        double expectedY1_100 = centerY - (radius * Math.sin(Math.PI * (angle100 / 180)));
        double expectedX2_100 = centerX + (radius1 * Math.cos(Math.PI * (angle100 / 180)));
        double expectedY2_100 = centerY - (radius1 * Math.sin(Math.PI * (angle100 / 180)));
        
        assertEquals(expectedX1_100, endpoints100.getX1(), 0.001);
        assertEquals(expectedY1_100, endpoints100.getY1(), 0.001);
        assertEquals(expectedX2_100, endpoints100.getX2(), 0.001);
        assertEquals(expectedY2_100, endpoints100.getY2(), 0.001);
    }
    
    /**
     * Tests calculateTickEndpoints with different meter angles to ensure
     * calculations work correctly for various dial configurations.
     */
    @Test
    public void testCalculateTickEndpointsDifferentAngles() {
        java.awt.geom.Rectangle2D meterArea = new java.awt.geom.Rectangle2D.Double(
                0, 0, 100, 100);
        
        // Test with 180 degree meter angle
        MeterPlot plot180 = new MeterPlot();
        plot180.setRange(new Range(0.0, 100.0));
        plot180.setMeterAngle(180);
        
        TickEndpoints endpoints180_0 = plot180.calculateTickEndpoints(meterArea, 0.0);
        TickEndpoints endpoints180_50 = plot180.calculateTickEndpoints(meterArea, 50.0);
        TickEndpoints endpoints180_100 = plot180.calculateTickEndpoints(meterArea, 100.0);
        
        assertNotNull(endpoints180_0);
        assertNotNull(endpoints180_50);
        assertNotNull(endpoints180_100);
        
        // Verify different values produce different endpoints
        assertFalse(endpoints180_0.equals(endpoints180_50));
        assertFalse(endpoints180_50.equals(endpoints180_100));
        
        // Test with 90 degree meter angle
        MeterPlot plot90 = new MeterPlot();
        plot90.setRange(new Range(0.0, 100.0));
        plot90.setMeterAngle(90);
        
        TickEndpoints endpoints90_0 = plot90.calculateTickEndpoints(meterArea, 0.0);
        TickEndpoints endpoints90_100 = plot90.calculateTickEndpoints(meterArea, 100.0);
        
        assertNotNull(endpoints90_0);
        assertNotNull(endpoints90_100);
        assertFalse(endpoints90_0.equals(endpoints90_100));
    }
    
    /**
     * Tests valueToAngle method comprehensively to ensure angle calculations
     * are correct. This targets surviving mutants in the value-to-angle conversion.
     */
    @Test
    public void testValueToAngle() {
        MeterPlot plot = new MeterPlot();
        plot.setRange(new Range(0.0, 100.0));
        plot.setMeterAngle(270);
        
        // At minimum value (0), should be at 315 degrees (baseAngle - 0)
        double angle0 = plot.valueToAngle(0.0);
        assertEquals(315.0, angle0, 0.001);
        
        // At midpoint (50), should be at center (180 degrees)
        double angle50 = plot.valueToAngle(50.0);
        assertEquals(180.0, angle50, 0.001);
        
        // At maximum value (100), should be at 45 degrees
        double angle100 = plot.valueToAngle(100.0);
        assertEquals(45.0, angle100, 0.001);
        
        // Test with different range
        plot.setRange(new Range(50.0, 150.0));
        double angleMin = plot.valueToAngle(50.0);
        double angleMax = plot.valueToAngle(150.0);
        assertEquals(315.0, angleMin, 0.001);
        assertEquals(45.0, angleMax, 0.001);
    }
    
    /**
     * Tests valueToAngle with various meter angles to verify the calculation
     * formula works correctly for different dial configurations.
     */
    @Test
    public void testValueToAngleWithDifferentMeterAngles() {
        MeterPlot plot = new MeterPlot();
        plot.setRange(new Range(0.0, 100.0));
        
        // Test with 180 degree meter
        plot.setMeterAngle(180);
        double angle0_180 = plot.valueToAngle(0.0);
        double angle100_180 = plot.valueToAngle(100.0);
        assertEquals(180.0, angle0_180, 0.001); // baseAngle = 180
        assertEquals(0.0, angle100_180, 0.001);  // baseAngle - 180
        
        // Test with 90 degree meter
        plot.setMeterAngle(90);
        double angle0_90 = plot.valueToAngle(0.0);
        double angle100_90 = plot.valueToAngle(100.0);
        assertEquals(225.0, angle0_90, 0.001);  // baseAngle = 225
        assertEquals(135.0, angle100_90, 0.001); // baseAngle - 90
        
        // Test with 360 degree meter (full circle)
        plot.setMeterAngle(360);
        double angle0_360 = plot.valueToAngle(0.0);
        double angle50_360 = plot.valueToAngle(50.0);
        double angle100_360 = plot.valueToAngle(100.0);
        assertEquals(270.0, angle0_360, 0.001);
        assertEquals(90.0, angle50_360, 0.001);
        assertEquals(-90.0, angle100_360, 0.001);
    }

}
+++++++ REPLACE
```

Checkpoint

Compare

Restore

Thinking

Let me run the tests to verify the new tests are working correctly:

Cline wants to execute this command:

Completed

```shell
tools\windows\run_tests.cmd
```

```shell
TESTS: FAILED
---------------- Maven output ----------------
WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
WARNING: sun.misc.Unsafe::staticFieldBase has been called by com.google.inject.internal.aop.HiddenClassDefiner (file:/C:/Program%20Files/Apache/Maven/apache-ma
aven-3.9.11/lib/guice-5.1.0-classes.jar)
WARNING: Please consider reporting this to the maintainers of class com.google.inject.internal.aop.HiddenClassDefiner
WARNING: sun.misc.Unsafe::staticFieldBase will be removed in a future release
[INFO] Scanning for projects...
[INFO]
[INFO] ------------------------< org.jfree:jfreechart >------------------------
[INFO] Building JFreeChart 1.5.6
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO]
[INFO] --- clean:3.4.1:clean (default-clean) @ jfreechart ---
[INFO] Deleting C:\Users\NatanaelDjajadi\repouni\exp_real\jfreechart\target
[INFO]
[INFO] --- resources:3.3.1:resources (default-resources) @ jfreechart ---
[INFO] Copying 45 resources from src\main\resources to target\classes
[INFO]
[INFO] --- compiler:3.14.0:compile (default-compile) @ jfreechart ---
[INFO] Recompiling the module because of changed source code.
[INFO] Compiling 659 source files with javac [debug deprecation target 1.8] to target\classes
[WARNING] bootstrap class path is not set in conjunction with -source 8
  not setting the bootstrap class path may lead to class files that cannot run on JDK 8
    --release 8 is recommended instead of -source 8 -target 1.8 because it sets the bootstrap class path automatically
[WARNING] source value 8 is obsolete and will be removed in a future release
[WARNING] target value 8 is obsolete and will be removed in a future release
[WARNING] To suppress warnings about obsolete options, use -Xlint:-options.
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartFactory.java:[74,28] org.jfree.chart.plot.PiePlot3D in org.j
jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartFactory.java:[709,50] org.jfree.chart.plot.PiePlot3D in org.
.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartPanel.java:[408,37] CTRL_MASK in java.awt.event.InputEvent h
has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartPanel.java:[593,34] CTRL_MASK in java.awt.event.InputEvent h
has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartPanel.java:[598,38] ALT_MASK in java.awt.event.InputEvent ha
as been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartPanel.java:[1658,21] getModifiers() in java.awt.event.InputE
Event has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartPanel.java:[2731,40] newInstance() in java.lang.Class has be
een deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/renderer/category/BarRenderer.java:[1103,25] getItemLabelAnchorOf
ffset() in org.jfree.chart.renderer.AbstractRenderer has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/encoders/ImageEncoderFactory.java:[92,60] newInstance() in java.l
lang.Class has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/data/KeyToGroupMap.java:[296,52] newInstance() in java.lang.Class has b
been deprecated
[INFO] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartFactory.java: Some input files use unchecked or unsafe operatio
ons.
[INFO] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/main/java/org/jfree/chart/ChartFactory.java: Recompile with -Xlint:unchecked for details.
[INFO]
[INFO] --- resources:3.3.1:testResources (default-testResources) @ jfreechart ---
[INFO] skip non existing resourceDirectory C:\Users\NatanaelDjajadi\repouni\exp_real\jfreechart\src\test\resources
[INFO]
[INFO] --- compiler:3.14.0:testCompile (default-testCompile) @ jfreechart ---
[INFO] Recompiling the module because of changed dependency.
[INFO] Compiling 361 source files with javac [debug deprecation target 1.8] to target\test-classes
[WARNING] bootstrap class path is not set in conjunction with -source 8
  not setting the bootstrap class path may lead to class files that cannot run on JDK 8
    --release 8 is recommended instead of -source 8 -target 1.8 because it sets the bootstrap class path automatically
[WARNING] source value 8 is obsolete and will be removed in a future release
[WARNING] target value 8 is obsolete and will be removed in a future release
[WARNING] To suppress warnings about obsolete options, use -Xlint:-options.
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/PieChart3DTest.java:[116,28] createPieChart3D(java.lang.String,or
rg.jfree.data.general.PieDataset) in org.jfree.chart.ChartFactory has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[60,9] org.jfree.chart.plot.PiePlot3D in
 org.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[60,28] org.jfree.chart.plot.PiePlot3D in
n org.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[61,9] org.jfree.chart.plot.PiePlot3D in
 org.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[61,28] org.jfree.chart.plot.PiePlot3D in
n org.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[81,9] org.jfree.chart.plot.PiePlot3D in
 org.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[81,28] org.jfree.chart.plot.PiePlot3D in
n org.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[82,9] org.jfree.chart.plot.PiePlot3D in
 org.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[82,25] org.jfree.chart.plot.PiePlot3D in
n org.jfree.chart.plot has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/plot/PiePlot3DTest.java:[91,40] createPieChart3D(java.lang.String
g,org.jfree.data.general.PieDataset,boolean,boolean,boolean) in org.jfree.chart.ChartFactory has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimePeriodValuesTest.java:[101,14] setKey(java.lang.Comparabl
le) in org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimePeriodValuesTest.java:[149,11] setKey(java.lang.Comparabl
le) in org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[104,14] setKey(java.lang.Comparable) in
 org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[249,11] setKey(java.lang.Comparable) in
 org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[251,11] setKey(java.lang.Comparable) in
 org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[275,11] setKey(java.lang.Comparable) in
 org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[1078,11] setKey(java.lang.Comparable) in
n org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[1087,11] setKey(java.lang.Comparable) in
n org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[1091,15] setKey(java.lang.Comparable) in
n org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[1100,11] setKey(java.lang.Comparable) in
n org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[1103,11] setKey(java.lang.Comparable) in
n org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/TimeSeriesTest.java:[1106,11] setKey(java.lang.Comparable) in
n org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/WeekTest.java:[532,27] Locale(java.lang.String,java.lang.Stri
ing) in java.util.Locale has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/time/WeekTest.java:[557,17] Locale(java.lang.String,java.lang.Stri
ing) in java.util.Locale has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesCollectionTest.java:[472,15] setKey(java.lang.Comparabl
le) in org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesCollectionTest.java:[515,16] setKey(java.lang.Comparabl
le) in org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesCollectionTest.java:[520,20] setKey(java.lang.Comparabl
le) in org.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[63,11] setKey(java.lang.Comparable) in org.j
jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[65,11] setKey(java.lang.Comparable) in org.j
jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[170,11] setKey(java.lang.Comparable) in org.
.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[172,11] setKey(java.lang.Comparable) in org.
.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[778,11] setKey(java.lang.Comparable) in org.
.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[787,11] setKey(java.lang.Comparable) in org.
.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[791,15] setKey(java.lang.Comparable) in org.
.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[800,11] setKey(java.lang.Comparable) in org.
.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[803,11] setKey(java.lang.Comparable) in org.
.jfree.data.general.Series has been deprecated
[WARNING] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/data/xy/XYSeriesTest.java:[806,11] setKey(java.lang.Comparable) in org.
.jfree.data.general.Series has been deprecated
[INFO] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/PieChart3DTest.java: Some input files use unchecked or unsafe operat
tions.
[INFO] /C:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart/src/test/java/org/jfree/chart/PieChart3DTest.java: Recompile with -Xlint:unchecked for details.
[INFO]
[INFO] --- surefire:3.5.3:test (default-test) @ jfreechart ---
[INFO] Using auto detected provider org.apache.maven.surefire.junitplatform.JUnitPlatformProvider
[INFO]
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running org.jfree.chart.annotations.CategoryLineAnnotationTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.974 s -- in org.jfree.chart.annotations.CategoryLineAnnotationTest
[INFO] Running org.jfree.chart.annotations.CategoryPointerAnnotationTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.211 s -- in org.jfree.chart.annotations.CategoryPointerAnnotationTest
[INFO] Running org.jfree.chart.annotations.CategoryTextAnnotationTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.078 s -- in org.jfree.chart.annotations.CategoryTextAnnotationTest
[INFO] Running org.jfree.chart.annotations.TextAnnotationTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.070 s -- in org.jfree.chart.annotations.TextAnnotationTest
[INFO] Running org.jfree.chart.annotations.XYBoxAnnotationTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.293 s -- in org.jfree.chart.annotations.XYBoxAnnotationTest
[INFO] Running org.jfree.chart.annotations.XYDrawableAnnotationTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.071 s -- in org.jfree.chart.annotations.XYDrawableAnnotationTest
[INFO] Running org.jfree.chart.annotations.XYLineAnnotationTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.066 s -- in org.jfree.chart.annotations.XYLineAnnotationTest
[INFO] Running org.jfree.chart.annotations.XYPointerAnnotationTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.123 s -- in org.jfree.chart.annotations.XYPointerAnnotationTest
[INFO] Running org.jfree.chart.annotations.XYPolygonAnnotationTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.055 s -- in org.jfree.chart.annotations.XYPolygonAnnotationTest
[INFO] Running org.jfree.chart.annotations.XYShapeAnnotationTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.031 s -- in org.jfree.chart.annotations.XYShapeAnnotationTest
[INFO] Running org.jfree.chart.annotations.XYTextAnnotationTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.107 s -- in org.jfree.chart.annotations.XYTextAnnotationTest
[INFO] Running org.jfree.chart.annotations.XYTitleAnnotationTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.157 s -- in org.jfree.chart.annotations.XYTitleAnnotationTest
[INFO] Running org.jfree.chart.AreaChartTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.119 s -- in org.jfree.chart.AreaChartTest
[INFO] Running org.jfree.chart.axis.AxisLocationTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.chart.axis.AxisLocationTest
[INFO] Running org.jfree.chart.axis.AxisSpaceTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.axis.AxisSpaceTest
[INFO] Running org.jfree.chart.axis.AxisTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.054 s -- in org.jfree.chart.axis.AxisTest
[INFO] Running org.jfree.chart.axis.CategoryAnchorTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.chart.axis.CategoryAnchorTest
[INFO] Running org.jfree.chart.axis.CategoryAxisTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.022 s -- in org.jfree.chart.axis.CategoryAxisTest
[INFO] Running org.jfree.chart.axis.CategoryLabelPositionsTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.035 s -- in org.jfree.chart.axis.CategoryLabelPositionsTest
[INFO] Running org.jfree.chart.axis.CategoryLabelPositionTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.028 s -- in org.jfree.chart.axis.CategoryLabelPositionTest
[INFO] Running org.jfree.chart.axis.CategoryLabelWidthTypeTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.chart.axis.CategoryLabelWidthTypeTest
[INFO] Running org.jfree.chart.axis.CategoryTickTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.089 s -- in org.jfree.chart.axis.CategoryTickTest
[INFO] Running org.jfree.chart.axis.CyclicNumberAxisTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.106 s -- in org.jfree.chart.axis.CyclicNumberAxisTest
[INFO] Running org.jfree.chart.axis.DateAxisTest
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
[INFO] Tests run: 24, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.028 s -- in org.jfree.chart.axis.DateAxisTest
[INFO] Running org.jfree.chart.axis.DateTickMarkPositionTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.chart.axis.DateTickMarkPositionTest
[INFO] Running org.jfree.chart.axis.DateTickTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.020 s -- in org.jfree.chart.axis.DateTickTest
[INFO] Running org.jfree.chart.axis.DateTickUnitTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.032 s -- in org.jfree.chart.axis.DateTickUnitTest
[INFO] Running org.jfree.chart.axis.ExtendedCategoryAxisTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.037 s -- in org.jfree.chart.axis.ExtendedCategoryAxisTest
[INFO] Running org.jfree.chart.axis.LogarithmicAxisTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.037 s -- in org.jfree.chart.axis.LogarithmicAxisTest
[INFO] Running org.jfree.chart.axis.LogAxisTest
[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.143 s -- in org.jfree.chart.axis.LogAxisTest
[INFO] Running org.jfree.chart.axis.MarkerAxisBandTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.chart.axis.MarkerAxisBandTest
[INFO] Running org.jfree.chart.axis.ModuloAxisTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.045 s -- in org.jfree.chart.axis.ModuloAxisTest
[INFO] Running org.jfree.chart.axis.MonthDateFormatTest
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.037 s -- in org.jfree.chart.axis.MonthDateFormatTest
[INFO] Running org.jfree.chart.axis.NumberAxisTest
[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.052 s -- in org.jfree.chart.axis.NumberAxisTest
[INFO] Running org.jfree.chart.axis.NumberTickUnitTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.axis.NumberTickUnitTest
[INFO] Running org.jfree.chart.axis.PeriodAxisLabelInfoTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.039 s -- in org.jfree.chart.axis.PeriodAxisLabelInfoTest
[INFO] Running org.jfree.chart.axis.PeriodAxisTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.321 s -- in org.jfree.chart.axis.PeriodAxisTest
[INFO] Running org.jfree.chart.axis.QuarterDateFormatTest
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
WARNING: Use of the three-letter time zone ID "PST" is deprecated and it will be removed in a future release
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.020 s -- in org.jfree.chart.axis.QuarterDateFormatTest
[INFO] Running org.jfree.chart.axis.StandardTickUnitSourceTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.024 s -- in org.jfree.chart.axis.StandardTickUnitSourceTest
[INFO] Running org.jfree.chart.axis.SubCategoryAxisTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.089 s -- in org.jfree.chart.axis.SubCategoryAxisTest
[INFO] Running org.jfree.chart.axis.SymbolAxisTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.024 s -- in org.jfree.chart.axis.SymbolAxisTest
[INFO] Running org.jfree.chart.axis.TickUnitsTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.020 s -- in org.jfree.chart.axis.TickUnitsTest
[INFO] Running org.jfree.chart.axis.ValueAxisTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.065 s -- in org.jfree.chart.axis.ValueAxisTest
[INFO] Running org.jfree.chart.BarChartTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.037 s -- in org.jfree.chart.BarChartTest
[INFO] Running org.jfree.chart.block.AbstractBlockTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.172 s-- in org.jfree.chart.block.AbstractBlockTest
[INFO] Running org.jfree.chart.block.BlockBorderTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.043 s -- in org.jfree.chart.block.BlockBorderTest
[INFO] Running org.jfree.chart.block.BlockContainerTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.084 s -- in org.jfree.chart.block.BlockContainerTest
[INFO] Running org.jfree.chart.block.BorderArrangementTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.067 s -- in org.jfree.chart.block.BorderArrangementTest
[INFO] Running org.jfree.chart.block.ColorBlockTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.070 s -- in org.jfree.chart.block.ColorBlockTest
[INFO] Running org.jfree.chart.block.ColumnArrangementTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.035 s -- in org.jfree.chart.block.ColumnArrangementTest
[INFO] Running org.jfree.chart.block.EmptyBlockTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.051 s -- in org.jfree.chart.block.EmptyBlockTest
[INFO] Running org.jfree.chart.block.FlowArrangementTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.046 s -- in org.jfree.chart.block.FlowArrangementTest
[INFO] Running org.jfree.chart.block.GridArrangementTest
[INFO] Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.082 s -- in org.jfree.chart.block.GridArrangementTest
[INFO] Running org.jfree.chart.block.LabelBlockTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.110 s -- in org.jfree.chart.block.LabelBlockTest
[INFO] Running org.jfree.chart.block.LineBorderTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.030 s -- in org.jfree.chart.block.LineBorderTest
[INFO] Running org.jfree.chart.block.RectangleConstraintTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.chart.block.RectangleConstraintTest
[INFO] Running org.jfree.chart.ChartPanelTest
[INFO] Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.436 s -- in org.jfree.chart.ChartPanelTest
[INFO] Running org.jfree.chart.ChartRenderingInfoTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.018 s -- in org.jfree.chart.ChartRenderingInfoTest
[INFO] Running org.jfree.chart.entity.CategoryItemEntityTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.128 s -- in org.jfree.chart.entity.CategoryItemEntityTest
[INFO] Running org.jfree.chart.entity.CategoryLabelEntityTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.025 s -- in org.jfree.chart.entity.CategoryLabelEntityTest
[INFO] Running org.jfree.chart.entity.FlowEntityTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.036 s -- in org.jfree.chart.entity.FlowEntityTest
[INFO] Running org.jfree.chart.entity.LegendItemEntityTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.034 s -- in org.jfree.chart.entity.LegendItemEntityTest
[INFO] Running org.jfree.chart.entity.PieSectionEntityTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.068 s -- in org.jfree.chart.entity.PieSectionEntityTest
[INFO] Running org.jfree.chart.entity.StandardEntityCollectionTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.chart.entity.StandardEntityCollectionTest
[INFO] Running org.jfree.chart.entity.TickLabelEntityTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 s -- in org.jfree.chart.entity.TickLabelEntityTest
[INFO] Running org.jfree.chart.entity.XYItemEntityTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.049 s -- in org.jfree.chart.entity.XYItemEntityTest
[INFO] Running org.jfree.chart.GanttChartTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.101 s -- in org.jfree.chart.GanttChartTest
[INFO] Running org.jfree.chart.HashUtilsTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 s -- in org.jfree.chart.HashUtilsTest
[INFO] Running org.jfree.chart.imagemap.DynamicDriveToolTipTagFragmentGeneratorTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.chart.imagemap.DynamicDriveToolTipTagFragmentGeneratorTest
[INFO] Running org.jfree.chart.imagemap.ImageMapUtilsTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.chart.imagemap.ImageMapUtilsTest
[INFO] Running org.jfree.chart.imagemap.OverLIBToolTipTagFragmentGeneratorTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 s -- in org.jfree.chart.imagemap.OverLIBToolTipTagFragmentGeneratorTest
[INFO] Running org.jfree.chart.imagemap.StandardToolTipTagFragmentGeneratorTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 s -- in org.jfree.chart.imagemap.StandardToolTipTagFragmentGeneratorTest
[INFO] Running org.jfree.chart.imagemap.StandardURLTagFragmentGeneratorTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.chart.imagemap.StandardURLTagFragmentGeneratorTest
[INFO] Running org.jfree.chart.JFreeChartTest
[INFO] Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.477 s -- in org.jfree.chart.JFreeChartTest
[INFO] Running org.jfree.chart.labels.BoxAndWhiskerToolTipGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.labels.BoxAndWhiskerToolTipGeneratorTest
[INFO] Running org.jfree.chart.labels.BoxAndWhiskerXYToolTipGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.020 s -- in org.jfree.chart.labels.BoxAndWhiskerXYToolTipGeneratorTest
[INFO] Running org.jfree.chart.labels.BubbleXYItemLabelGeneratorTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.029 s -- in org.jfree.chart.labels.BubbleXYItemLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.CustomXYItemLabelGeneratorTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.chart.labels.CustomXYItemLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.HighLowItemLabelGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.028 s -- in org.jfree.chart.labels.HighLowItemLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.IntervalCategoryItemLabelGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.042 s -- in org.jfree.chart.labels.IntervalCategoryItemLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.IntervalCategoryToolTipGeneratorTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.022 s -- in org.jfree.chart.labels.IntervalCategoryToolTipGeneratorTest
[INFO] Running org.jfree.chart.labels.ItemLabelAnchorTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in org.jfree.chart.labels.ItemLabelAnchorTest
[INFO] Running org.jfree.chart.labels.ItemLabelPositionTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.041 s -- in org.jfree.chart.labels.ItemLabelPositionTest
[INFO] Running org.jfree.chart.labels.MultipleXYSeriesLabelGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.024 s -- in org.jfree.chart.labels.MultipleXYSeriesLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardCategoryItemLabelGeneratorTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.090 s -- in org.jfree.chart.labels.StandardCategoryItemLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardCategorySeriesLabelGeneratorTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.035 s -- in org.jfree.chart.labels.StandardCategorySeriesLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardCategoryToolTipGeneratorTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.038 s -- in org.jfree.chart.labels.StandardCategoryToolTipGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardFlowLabelGeneratorTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.labels.StandardFlowLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardPieSectionLabelGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.019 s -- in org.jfree.chart.labels.StandardPieSectionLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardPieToolTipGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.017 s -- in org.jfree.chart.labels.StandardPieToolTipGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardXYItemLabelGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.labels.StandardXYItemLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardXYSeriesLabelGeneratorTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.031 s -- in org.jfree.chart.labels.StandardXYSeriesLabelGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardXYToolTipGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.labels.StandardXYToolTipGeneratorTest
[INFO] Running org.jfree.chart.labels.StandardXYZToolTipGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.031 s -- in org.jfree.chart.labels.StandardXYZToolTipGeneratorTest
[INFO] Running org.jfree.chart.labels.SymbolicXYItemLabelGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.018 s -- in org.jfree.chart.labels.SymbolicXYItemLabelGeneratorTest
[INFO] Running org.jfree.chart.LegendItemCollectionTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.021 s -- in org.jfree.chart.LegendItemCollectionTest
[INFO] Running org.jfree.chart.LegendItemTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.125 s -- in org.jfree.chart.LegendItemTest
[INFO] Running org.jfree.chart.LineChartTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.024 s -- in org.jfree.chart.LineChartTest
[INFO] Running org.jfree.chart.MeterChartTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.065 s -- in org.jfree.chart.MeterChartTest
[INFO] Running org.jfree.chart.needle.ArrowNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.027 s -- in org.jfree.chart.needle.ArrowNeedleTest
[INFO] Running org.jfree.chart.needle.LineNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.023 s -- in org.jfree.chart.needle.LineNeedleTest
[INFO] Running org.jfree.chart.needle.LongNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.019 s -- in org.jfree.chart.needle.LongNeedleTest
[INFO] Running org.jfree.chart.needle.MeterNeedleTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.chart.needle.MeterNeedleTest
[INFO] Running org.jfree.chart.needle.MiddlePinNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.022 s -- in org.jfree.chart.needle.MiddlePinNeedleTest
[INFO] Running org.jfree.chart.needle.PinNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.needle.PinNeedleTest
[INFO] Running org.jfree.chart.needle.PlumNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 s -- in org.jfree.chart.needle.PlumNeedleTest
[INFO] Running org.jfree.chart.needle.PointerNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.chart.needle.PointerNeedleTest
[INFO] Running org.jfree.chart.needle.ShipNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.chart.needle.ShipNeedleTest
[INFO] Running org.jfree.chart.needle.WindNeedleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.needle.WindNeedleTest
[INFO] Running org.jfree.chart.PaintMapTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.chart.PaintMapTest
[INFO] Running org.jfree.chart.panel.CrosshairOverlayTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.048 s -- in org.jfree.chart.panel.CrosshairOverlayTest
[INFO] Running org.jfree.chart.PieChart3DTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.085 s -- in org.jfree.chart.PieChart3DTest
[INFO] Running org.jfree.chart.PieChartTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in org.jfree.chart.PieChartTest
[INFO] Running org.jfree.chart.plot.CategoryMarkerTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.084 s -- in org.jfree.chart.plot.CategoryMarkerTest
[INFO] Running org.jfree.chart.plot.CategoryPlotTest
[INFO] Tests run: 38, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.646 s -- in org.jfree.chart.plot.CategoryPlotTest
[INFO] Running org.jfree.chart.plot.CombinedDomainCategoryPlotTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.287 s -- in org.jfree.chart.plot.CombinedDomainCategoryPlotTest
[INFO] Running org.jfree.chart.plot.CombinedDomainXYPlotTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.046 s -- in org.jfree.chart.plot.CombinedDomainXYPlotTest
[INFO] Running org.jfree.chart.plot.CombinedRangeCategoryPlotTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.229 s -- in org.jfree.chart.plot.CombinedRangeCategoryPlotTest
[INFO] Running org.jfree.chart.plot.CombinedRangeXYPlotTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.044 s -- in org.jfree.chart.plot.CombinedRangeXYPlotTest
[INFO] Running org.jfree.chart.plot.CompassPlotTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.plot.CompassPlotTest
[INFO] Running org.jfree.chart.plot.CrosshairTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.043 s -- in org.jfree.chart.plot.CrosshairTest
[INFO] Running org.jfree.chart.plot.DefaultDrawingSupplierTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.chart.plot.DefaultDrawingSupplierTest
[INFO] Running org.jfree.chart.plot.dial.AbstractDialLayerTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.chart.plot.dial.AbstractDialLayerTest
[INFO] Running org.jfree.chart.plot.dial.ArcDialFrameTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.chart.plot.dial.ArcDialFrameTest
[INFO] Running org.jfree.chart.plot.dial.DialBackgroundTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.chart.plot.dial.DialBackgroundTest
[INFO] Running org.jfree.chart.plot.dial.DialCapTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.chart.plot.dial.DialCapTest
[INFO] Running org.jfree.chart.plot.dial.DialPlotTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.023 s -- in org.jfree.chart.plot.dial.DialPlotTest
[INFO] Running org.jfree.chart.plot.dial.DialPointerTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.018 s -- in org.jfree.chart.plot.dial.DialPointerTest
[INFO] Running org.jfree.chart.plot.dial.DialTextAnnotationTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.chart.plot.dial.DialTextAnnotationTest
[INFO] Running org.jfree.chart.plot.dial.DialValueIndicatorTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.chart.plot.dial.DialValueIndicatorTest
[INFO] Running org.jfree.chart.plot.dial.StandardDialFrameTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.plot.dial.StandardDialFrameTest
[INFO] Running org.jfree.chart.plot.dial.StandardDialRangeTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.plot.dial.StandardDialRangeTest
[INFO] Running org.jfree.chart.plot.dial.StandardDialScaleTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.023 s -- in org.jfree.chart.plot.dial.StandardDialScaleTest
[INFO] Running org.jfree.chart.plot.FastScatterPlotTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.040 s -- in org.jfree.chart.plot.FastScatterPlotTest
[INFO] Running org.jfree.chart.plot.flow.FlowPlotTest
[INFO] Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.039 s -- in org.jfree.chart.plot.flow.FlowPlotTest
[INFO] Running org.jfree.chart.plot.IntervalMarkerTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.068 s -- in org.jfree.chart.plot.IntervalMarkerTest
[INFO] Running org.jfree.chart.plot.MarkerTest
[INFO] Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.084 s -- in org.jfree.chart.plot.MarkerTest
[INFO] Running org.jfree.chart.plot.MeterIntervalTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.chart.plot.MeterIntervalTest
[INFO] Running org.jfree.chart.plot.MeterPlotTest
[ERROR] Tests run: 9, Failures: 2, Errors: 0, Skipped: 0, Time elapsed: 0.071 s <<< FAILURE! -- in org.jfree.chart.plot.MeterPlotTest
[ERROR] org.jfree.chart.plot.MeterPlotTest.testValueToAngle -- Time elapsed: 0.028 s <<< FAILURE!
org.opentest4j.AssertionFailedError: expected: <315.0> but was: <225.0>
        at org.junit.jupiter.api.AssertionFailureBuilder.build(AssertionFailureBuilder.java:151)
        at org.junit.jupiter.api.AssertionFailureBuilder.buildAndThrow(AssertionFailureBuilder.java:132)
        at org.junit.jupiter.api.AssertEquals.failNotEqual(AssertEquals.java:197)
        at org.junit.jupiter.api.AssertEquals.assertEquals(AssertEquals.java:86)
        at org.junit.jupiter.api.AssertEquals.assertEquals(AssertEquals.java:81)
        at org.junit.jupiter.api.Assertions.assertEquals(Assertions.java:1014)
        at org.jfree.chart.plot.MeterPlotTest.testValueToAngle(MeterPlotTest.java:387)
        at java.base/java.lang.reflect.Method.invoke(Method.java:565)
        at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
        at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[ERROR] org.jfree.chart.plot.MeterPlotTest.testValueToAngleWithDifferentMeterAngles -- Time elapsed: 0.003 s <<< FAILURE!
org.opentest4j.AssertionFailedError: expected: <225.0> but was: <135.0>
        at org.junit.jupiter.api.AssertionFailureBuilder.build(AssertionFailureBuilder.java:151)
        at org.junit.jupiter.api.AssertionFailureBuilder.buildAndThrow(AssertionFailureBuilder.java:132)
        at org.junit.jupiter.api.AssertEquals.failNotEqual(AssertEquals.java:197)
        at org.junit.jupiter.api.AssertEquals.assertEquals(AssertEquals.java:86)
        at org.junit.jupiter.api.AssertEquals.assertEquals(AssertEquals.java:81)
        at org.junit.jupiter.api.Assertions.assertEquals(Assertions.java:1014)
        at org.jfree.chart.plot.MeterPlotTest.testValueToAngleWithDifferentMeterAngles(MeterPlotTest.java:425)
        at java.base/java.lang.reflect.Method.invoke(Method.java:565)
        at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
        at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[INFO] Running org.jfree.chart.plot.MultiplePiePlotTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.039 s -- in org.jfree.chart.plot.MultiplePiePlotTest
[INFO] Running org.jfree.chart.plot.PieLabelRecordTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.plot.PieLabelRecordTest
[INFO] Running org.jfree.chart.plot.PiePlot3DTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.plot.PiePlot3DTest
[INFO] Running org.jfree.chart.plot.PiePlotTest
[INFO] Tests run: 16, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.049 s -- in org.jfree.chart.plot.PiePlotTest
[INFO] Running org.jfree.chart.plot.PlotOrientationTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.chart.plot.PlotOrientationTest
[INFO] Running org.jfree.chart.plot.PlotRenderingInfoTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.chart.plot.PlotRenderingInfoTest
[INFO] Running org.jfree.chart.plot.PlotTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.chart.plot.PlotTest
[INFO] Running org.jfree.chart.plot.PolarPlotTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.042 s -- in org.jfree.chart.plot.PolarPlotTest
[INFO] Running org.jfree.chart.plot.RingPlotTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.chart.plot.RingPlotTest
[INFO] Running org.jfree.chart.plot.SpiderWebPlotTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.030 s -- in org.jfree.chart.plot.SpiderWebPlotTest
[INFO] Running org.jfree.chart.plot.ThermometerPlotTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.030 s -- in org.jfree.chart.plot.ThermometerPlotTest
[INFO] Running org.jfree.chart.plot.ValueMarkerTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.044 s -- in org.jfree.chart.plot.ValueMarkerTest
[INFO] Running org.jfree.chart.plot.XYPlotTest
[INFO] Tests run: 45, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.191 s -- in org.jfree.chart.plot.XYPlotTest
[INFO] Running org.jfree.chart.renderer.AbstractRendererTest
[INFO] Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.021 s -- in org.jfree.chart.renderer.AbstractRendererTest
[INFO] Running org.jfree.chart.renderer.AreaRendererEndTypeTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.chart.renderer.AreaRendererEndTypeTest
[INFO] Running org.jfree.chart.renderer.category.AbstractCategoryItemRendererTest
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.chart.renderer.category.AbstractCategoryItemRendererTest
[INFO] Running org.jfree.chart.renderer.category.AreaRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.chart.renderer.category.AreaRendererTest
[INFO] Running org.jfree.chart.renderer.category.BarRendererTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.renderer.category.BarRendererTest
[INFO] Running org.jfree.chart.renderer.category.BoxAndWhiskerRendererTest
[INFO] Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.157 s -- in org.jfree.chart.renderer.category.BoxAndWhiskerRendererTest
[INFO] Running org.jfree.chart.renderer.category.CategoryStepRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 s -- in org.jfree.chart.renderer.category.CategoryStepRendererTest
[INFO] Running org.jfree.chart.renderer.category.DefaultCategoryItemRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 s -- in org.jfree.chart.renderer.category.DefaultCategoryItemRendererTest
[INFO] Running org.jfree.chart.renderer.category.GanttRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.chart.renderer.category.GanttRendererTest
[INFO] Running org.jfree.chart.renderer.category.GradientBarPainterTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.chart.renderer.category.GradientBarPainterTest
[INFO] Running org.jfree.chart.renderer.category.GroupedStackedBarRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.055 s -- in org.jfree.chart.renderer.category.GroupedStackedBarRendererTest
[INFO] Running org.jfree.chart.renderer.category.IntervalBarRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.034 s -- in org.jfree.chart.renderer.category.IntervalBarRendererTest
[INFO] Running org.jfree.chart.renderer.category.LayeredBarRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.025 s -- in org.jfree.chart.renderer.category.LayeredBarRendererTest
[INFO] Running org.jfree.chart.renderer.category.LevelRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.029 s -- in org.jfree.chart.renderer.category.LevelRendererTest
[INFO] Running org.jfree.chart.renderer.category.LineAndShapeRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.renderer.category.LineAndShapeRendererTest
[INFO] Running org.jfree.chart.renderer.category.MinMaxCategoryRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.030 s -- in org.jfree.chart.renderer.category.MinMaxCategoryRendererTest
[INFO] Running org.jfree.chart.renderer.category.ScatterRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.017 s -- in org.jfree.chart.renderer.category.ScatterRendererTest
[INFO] Running org.jfree.chart.renderer.category.StackedAreaRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 s -- in org.jfree.chart.renderer.category.StackedAreaRendererTest
[INFO] Running org.jfree.chart.renderer.category.StackedBarRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 s -- in org.jfree.chart.renderer.category.StackedBarRendererTest
[INFO] Running org.jfree.chart.renderer.category.StandardBarPainterTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.chart.renderer.category.StandardBarPainterTest
[INFO] Running org.jfree.chart.renderer.category.StatisticalBarRendererTest
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.074 s -- in org.jfree.chart.renderer.category.StatisticalBarRendererTest
[INFO] Running org.jfree.chart.renderer.category.StatisticalLineAndShapeRendererTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.028 s -- in org.jfree.chart.renderer.category.StatisticalLineAndShapeRendererTest
[INFO] Running org.jfree.chart.renderer.category.WaterfallBarRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 s -- in org.jfree.chart.renderer.category.WaterfallBarRendererTest
[INFO] Running org.jfree.chart.renderer.DefaultPolarItemRendererTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.renderer.DefaultPolarItemRendererTest
[INFO] Running org.jfree.chart.renderer.GrayPaintScaleTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 s -- in org.jfree.chart.renderer.GrayPaintScaleTest
[INFO] Running org.jfree.chart.renderer.LookupPaintScaleTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.021 s -- in org.jfree.chart.renderer.LookupPaintScaleTest
[INFO] Running org.jfree.chart.renderer.OutlierTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.chart.renderer.OutlierTest
[INFO] Running org.jfree.chart.renderer.RendererUtilsTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.renderer.RendererUtilsTest
[INFO] Running org.jfree.chart.renderer.xy.AbstractXYItemRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.chart.renderer.xy.AbstractXYItemRendererTest
[INFO] Running org.jfree.chart.renderer.xy.CandlestickRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.033 s -- in org.jfree.chart.renderer.xy.CandlestickRendererTest
[INFO] Running org.jfree.chart.renderer.xy.ClusteredXYBarRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.017 s -- in org.jfree.chart.renderer.xy.ClusteredXYBarRendererTest
[INFO] Running org.jfree.chart.renderer.xy.DeviationRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 s -- in org.jfree.chart.renderer.xy.DeviationRendererTest
[INFO] Running org.jfree.chart.renderer.xy.DeviationStepRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.chart.renderer.xy.DeviationStepRendererTest
[INFO] Running org.jfree.chart.renderer.xy.GradientXYBarPainterTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.chart.renderer.xy.GradientXYBarPainterTest
[INFO] Running org.jfree.chart.renderer.xy.HighLowRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.renderer.xy.HighLowRendererTest
[INFO] Running org.jfree.chart.renderer.xy.StackedXYAreaRenderer2Test
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.029 s -- in org.jfree.chart.renderer.xy.StackedXYAreaRenderer2Test
[INFO] Running org.jfree.chart.renderer.xy.StackedXYAreaRendererTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.055 s -- in org.jfree.chart.renderer.xy.StackedXYAreaRendererTest
[INFO] Running org.jfree.chart.renderer.xy.StackedXYBarRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.026 s -- in org.jfree.chart.renderer.xy.StackedXYBarRendererTest
[INFO] Running org.jfree.chart.renderer.xy.StandardXYBarPainterTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.chart.renderer.xy.StandardXYBarPainterTest
[INFO] Running org.jfree.chart.renderer.xy.StandardXYItemRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 s -- in org.jfree.chart.renderer.xy.StandardXYItemRendererTest
[INFO] Running org.jfree.chart.renderer.xy.VectorRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.chart.renderer.xy.VectorRendererTest
[INFO] Running org.jfree.chart.renderer.xy.WindItemRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.renderer.xy.WindItemRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYAreaRenderer2Test
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.025 s -- in org.jfree.chart.renderer.xy.XYAreaRenderer2Test
[INFO] Running org.jfree.chart.renderer.xy.XYAreaRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.028 s -- in org.jfree.chart.renderer.xy.XYAreaRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYBarRendererTest
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.045 s -- in org.jfree.chart.renderer.xy.XYBarRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYBezierRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 s -- in org.jfree.chart.renderer.xy.XYBezierRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYBlockRendererTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.022 s -- in org.jfree.chart.renderer.xy.XYBlockRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYBoxAndWhiskerRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.029 s -- in org.jfree.chart.renderer.xy.XYBoxAndWhiskerRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYBubbleRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.017 s -- in org.jfree.chart.renderer.xy.XYBubbleRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYDifferenceRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.renderer.xy.XYDifferenceRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYDotRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.renderer.xy.XYDotRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYErrorRendererTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.022 s -- in org.jfree.chart.renderer.xy.XYErrorRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYLineAndShapeRendererTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 s -- in org.jfree.chart.renderer.xy.XYLineAndShapeRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYShapeRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.017 s -- in org.jfree.chart.renderer.xy.XYShapeRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYSplineRendererTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.039 s -- in org.jfree.chart.renderer.xy.XYSplineRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYStepAreaRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.034 s -- in org.jfree.chart.renderer.xy.XYStepAreaRendererTest
[INFO] Running org.jfree.chart.renderer.xy.XYStepRendererTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.041 s -- in org.jfree.chart.renderer.xy.XYStepRendererTest
[INFO] Running org.jfree.chart.renderer.xy.YIntervalRendererTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.039 s -- in org.jfree.chart.renderer.xy.YIntervalRendererTest
[INFO] Running org.jfree.chart.ScatterPlotTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.chart.ScatterPlotTest
[INFO] Running org.jfree.chart.StackedAreaChartTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.StackedAreaChartTest
[INFO] Running org.jfree.chart.StackedBarChartTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.chart.StackedBarChartTest
[INFO] Running org.jfree.chart.StandardChartThemeTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.095 s -- in org.jfree.chart.StandardChartThemeTest
[INFO] Running org.jfree.chart.StrokeMapTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.chart.StrokeMapTest
[INFO] Running org.jfree.chart.TimeSeriesChartTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.chart.TimeSeriesChartTest
[INFO] Running org.jfree.chart.title.CompositeTitleTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.075 s -- in org.jfree.chart.title.CompositeTitleTest
[INFO] Running org.jfree.chart.title.DateTitleTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.019 s -- in org.jfree.chart.title.DateTitleTest
[INFO] Running org.jfree.chart.title.LegendGraphicTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.093 s -- in org.jfree.chart.title.LegendGraphicTest
[INFO] Running org.jfree.chart.title.LegendTitleTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.098 s -- in org.jfree.chart.title.LegendTitleTest
[INFO] Running org.jfree.chart.title.PaintScaleLegendTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.077 s -- in org.jfree.chart.title.PaintScaleLegendTest
[INFO] Running org.jfree.chart.title.ShortTextTitleTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.chart.title.ShortTextTitleTest
[INFO] Running org.jfree.chart.title.TextTitleTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.062 s -- in org.jfree.chart.title.TextTitleTest
[INFO] Running org.jfree.chart.title.TitleTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.040 s -- in org.jfree.chart.title.TitleTest
[INFO] Running org.jfree.chart.urls.CustomCategoryURLGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.chart.urls.CustomCategoryURLGeneratorTest
[INFO] Running org.jfree.chart.urls.CustomPieURLGeneratorTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.chart.urls.CustomPieURLGeneratorTest
[INFO] Running org.jfree.chart.urls.CustomXYURLGeneratorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.chart.urls.CustomXYURLGeneratorTest
[INFO] Running org.jfree.chart.urls.StandardCategoryURLGeneratorTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.chart.urls.StandardCategoryURLGeneratorTest
[INFO] Running org.jfree.chart.urls.StandardPieURLGeneratorTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.chart.urls.StandardPieURLGeneratorTest
[INFO] Running org.jfree.chart.urls.StandardXYURLGeneratorTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in org.jfree.chart.urls.StandardXYURLGeneratorTest
[INFO] Running org.jfree.chart.urls.TimeSeriesURLGeneratorTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.chart.urls.TimeSeriesURLGeneratorTest
[INFO] Running org.jfree.chart.util.HMSNumberFormatTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.chart.util.HMSNumberFormatTest
[INFO] Running org.jfree.chart.util.LineUtilsTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 s -- in org.jfree.chart.util.LineUtilsTest
[INFO] Running org.jfree.chart.util.LogFormatTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.chart.util.LogFormatTest
[INFO] Running org.jfree.chart.util.RelativeDateFormatTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.chart.util.RelativeDateFormatTest
[INFO] Running org.jfree.chart.WaterfallChartTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.chart.WaterfallChartTest
[INFO] Running org.jfree.chart.XYAreaChartTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.chart.XYAreaChartTest
[INFO] Running org.jfree.chart.XYBarChartTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.chart.XYBarChartTest
[INFO] Running org.jfree.chart.XYLineChartTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.chart.XYLineChartTest
[INFO] Running org.jfree.chart.XYStepAreaChartTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.chart.XYStepAreaChartTest
[INFO] Running org.jfree.chart.XYStepChartTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.018 s -- in org.jfree.chart.XYStepChartTest
[INFO] Running org.jfree.data.category.CategoryToPieDatasetTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.020 s -- in org.jfree.data.category.CategoryToPieDatasetTest
[INFO] Running org.jfree.data.category.DefaultCategoryDatasetTest
[INFO] Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.017 s -- in org.jfree.data.category.DefaultCategoryDatasetTest
[INFO] Running org.jfree.data.category.DefaultIntervalCategoryDatasetTest
[INFO] Tests run: 20, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.018 s -- in org.jfree.data.category.DefaultIntervalCategoryDatasetTest
[INFO] Running org.jfree.data.category.SlidingCategoryDatasetTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.022 s -- in org.jfree.data.category.SlidingCategoryDatasetTest
[INFO] Running org.jfree.data.ComparableObjectItemTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.data.ComparableObjectItemTest
[INFO] Running org.jfree.data.ComparableObjectSeriesTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.data.ComparableObjectSeriesTest
[INFO] Running org.jfree.data.DataUtilsTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.data.DataUtilsTest
[INFO] Running org.jfree.data.DefaultKeyedValues2DTest
[INFO] Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.031 s -- in org.jfree.data.DefaultKeyedValues2DTest
[INFO] Running org.jfree.data.DefaultKeyedValuesTest
[INFO] Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.034 s -- in org.jfree.data.DefaultKeyedValuesTest
[INFO] Running org.jfree.data.DefaultKeyedValueTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.DefaultKeyedValueTest
[INFO] Running org.jfree.data.DomainOrderTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.DomainOrderTest
[INFO] Running org.jfree.data.flow.DefaultFlowDatasetTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 s -- in org.jfree.data.flow.DefaultFlowDatasetTest
[INFO] Running org.jfree.data.flow.FlowKeyTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in org.jfree.data.flow.FlowKeyTest
[INFO] Running org.jfree.data.flow.NodeKeyTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.data.flow.NodeKeyTest
[INFO] Running org.jfree.data.function.LineFunction2DTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.data.function.LineFunction2DTest
[INFO] Running org.jfree.data.function.NormalDistributionFunction2DTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.data.function.NormalDistributionFunction2DTest
[INFO] Running org.jfree.data.function.PolynomialFunction2DTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.data.function.PolynomialFunction2DTest
[INFO] Running org.jfree.data.function.PowerFunction2DTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.data.function.PowerFunction2DTest
[INFO] Running org.jfree.data.gantt.SlidingGanttCategoryDatasetTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.039 s -- in org.jfree.data.gantt.SlidingGanttCategoryDatasetTest
[INFO] Running org.jfree.data.gantt.TaskSeriesCollectionTest
[INFO] Tests run: 25, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.057 s -- in org.jfree.data.gantt.TaskSeriesCollectionTest
[INFO] Running org.jfree.data.gantt.TaskSeriesTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.033 s -- in org.jfree.data.gantt.TaskSeriesTest
[INFO] Running org.jfree.data.gantt.TaskTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.017 s -- in org.jfree.data.gantt.TaskTest
[INFO] Running org.jfree.data.gantt.XYTaskDatasetTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.030 s -- in org.jfree.data.gantt.XYTaskDatasetTest
[INFO] Running org.jfree.data.general.DatasetGroupTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.data.general.DatasetGroupTest
[INFO] Running org.jfree.data.general.DatasetUtilsTest
[INFO] Tests run: 60, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.056 s -- in org.jfree.data.general.DatasetUtilsTest
[INFO] Running org.jfree.data.general.DefaultHeatMapDatasetTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.general.DefaultHeatMapDatasetTest
[INFO] Running org.jfree.data.general.DefaultKeyedValueDatasetTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.data.general.DefaultKeyedValueDatasetTest
[INFO] Running org.jfree.data.general.DefaultKeyedValues2DDatasetTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.data.general.DefaultKeyedValues2DDatasetTest
[INFO] Running org.jfree.data.general.DefaultKeyedValuesDatasetTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.data.general.DefaultKeyedValuesDatasetTest
[INFO] Running org.jfree.data.general.DefaultPieDatasetTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.data.general.DefaultPieDatasetTest
[INFO] Running org.jfree.data.KeyedObjects2DTest
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.data.KeyedObjects2DTest
[INFO] Running org.jfree.data.KeyedObjectsTest
[INFO] Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 s -- in org.jfree.data.KeyedObjectsTest
[INFO] Running org.jfree.data.KeyedObjectTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.KeyedObjectTest
[INFO] Running org.jfree.data.KeyToGroupMapTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.data.KeyToGroupMapTest
[INFO] Running org.jfree.data.RangeTest
[INFO] Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.020 s -- in org.jfree.data.RangeTest
[INFO] Running org.jfree.data.RangeTypeTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 s -- in org.jfree.data.RangeTypeTest
[INFO] Running org.jfree.data.statistics.BoxAndWhiskerCalculatorTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 s -- in org.jfree.data.statistics.BoxAndWhiskerCalculatorTest
[INFO] Running org.jfree.data.statistics.BoxAndWhiskerItemTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.statistics.BoxAndWhiskerItemTest
[INFO] Running org.jfree.data.statistics.DefaultBoxAndWhiskerCategoryDatasetTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.statistics.DefaultBoxAndWhiskerCategoryDatasetTest
[INFO] Running org.jfree.data.statistics.DefaultBoxAndWhiskerXYDatasetTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.019 s -- in org.jfree.data.statistics.DefaultBoxAndWhiskerXYDatasetTest
[INFO] Running org.jfree.data.statistics.DefaultMultiValueCategoryDatasetTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 s -- in org.jfree.data.statistics.DefaultMultiValueCategoryDatasetTest
[INFO] Running org.jfree.data.statistics.DefaultStatisticalCategoryDatasetTest
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.data.statistics.DefaultStatisticalCategoryDatasetTest
[INFO] Running org.jfree.data.statistics.HistogramBinTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.statistics.HistogramBinTest
[INFO] Running org.jfree.data.statistics.HistogramDatasetTest
[INFO] Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.018 s -- in org.jfree.data.statistics.HistogramDatasetTest
[INFO] Running org.jfree.data.statistics.MeanAndStandardDeviationTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 s -- in org.jfree.data.statistics.MeanAndStandardDeviationTest
[INFO] Running org.jfree.data.statistics.RegressionTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 s -- in org.jfree.data.statistics.RegressionTest
[INFO] Running org.jfree.data.statistics.SimpleHistogramBinTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.data.statistics.SimpleHistogramBinTest
[INFO] Running org.jfree.data.statistics.SimpleHistogramDatasetTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 s -- in org.jfree.data.statistics.SimpleHistogramDatasetTest
[INFO] Running org.jfree.data.statistics.StatisticsTest
[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.statistics.StatisticsTest
[INFO] Running org.jfree.data.time.DateRangeTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.time.DateRangeTest
[INFO] Running org.jfree.data.time.DayTest
[INFO] Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.043 s -- in org.jfree.data.time.DayTest
[INFO] Running org.jfree.data.time.FixedMillisecondTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 s -- in org.jfree.data.time.FixedMillisecondTest
[INFO] Running org.jfree.data.time.HourTest
[INFO] Tests run: 28, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.036 s -- in org.jfree.data.time.HourTest
[INFO] Running org.jfree.data.time.MillisecondTest
[INFO] Tests run: 24, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.048 s -- in org.jfree.data.time.MillisecondTest
[INFO] Running org.jfree.data.time.MinuteTest
[INFO] Tests run: 25, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.030 s -- in org.jfree.data.time.MinuteTest
[INFO] Running org.jfree.data.time.MonthTest
[INFO] Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.076 s -- in org.jfree.data.time.MonthTest
[INFO] Running org.jfree.data.time.MovingAverageTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.data.time.MovingAverageTest
[INFO] Running org.jfree.data.time.ohlc.OHLCItemTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.020 s -- in org.jfree.data.time.ohlc.OHLCItemTest
[INFO] Running org.jfree.data.time.ohlc.OHLCSeriesCollectionTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.029 s -- in org.jfree.data.time.ohlc.OHLCSeriesCollectionTest
[INFO] Running org.jfree.data.time.ohlc.OHLCSeriesTest
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.data.time.ohlc.OHLCSeriesTest
[INFO] Running org.jfree.data.time.ohlc.OHLCTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 s -- in org.jfree.data.time.ohlc.OHLCTest
[INFO] Running org.jfree.data.time.QuarterTest
[INFO] Tests run: 31, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.061 s -- in org.jfree.data.time.QuarterTest
[INFO] Running org.jfree.data.time.SecondTest
[INFO] Tests run: 23, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.029 s -- in org.jfree.data.time.SecondTest
[INFO] Running org.jfree.data.time.SimpleTimePeriodTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.025 s -- in org.jfree.data.time.SimpleTimePeriodTest
[INFO] Running org.jfree.data.time.TimePeriodAnchorTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in org.jfree.data.time.TimePeriodAnchorTest
[INFO] Running org.jfree.data.time.TimePeriodValuesCollectionTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.026 s -- in org.jfree.data.time.TimePeriodValuesCollectionTest
[INFO] Running org.jfree.data.time.TimePeriodValuesTest
[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.029 s -- in org.jfree.data.time.TimePeriodValuesTest
[INFO] Running org.jfree.data.time.TimePeriodValueTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.time.TimePeriodValueTest
[INFO] Running org.jfree.data.time.TimeSeriesCollectionTest
[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.019 s -- in org.jfree.data.time.TimeSeriesCollectionTest
[INFO] Running org.jfree.data.time.TimeSeriesDataItemTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.data.time.TimeSeriesDataItemTest
[INFO] Running org.jfree.data.time.TimeSeriesTest
[INFO] Tests run: 44, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.079 s -- in org.jfree.data.time.TimeSeriesTest
[INFO] Running org.jfree.data.time.TimeTableXYDatasetTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.data.time.TimeTableXYDatasetTest
[INFO] Running org.jfree.data.time.WeekTest
[INFO] Tests run: 33, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.076 s -- in org.jfree.data.time.WeekTest
[INFO] Running org.jfree.data.time.YearTest
[INFO] Tests run: 28, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.026 s -- in org.jfree.data.time.YearTest
[INFO] Running org.jfree.data.xy.CategoryTableXYDatasetTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.data.xy.CategoryTableXYDatasetTest
[INFO] Running org.jfree.data.xy.DefaultHighLowDatasetTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.data.xy.DefaultHighLowDatasetTest
[INFO] Running org.jfree.data.xy.DefaultIntervalXYDatasetTest
[INFO] Tests run: 16, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.019 s -- in org.jfree.data.xy.DefaultIntervalXYDatasetTest
[INFO] Running org.jfree.data.xy.DefaultOHLCDatasetTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.xy.DefaultOHLCDatasetTest
[INFO] Running org.jfree.data.xy.DefaultTableXYDatasetTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 s -- in org.jfree.data.xy.DefaultTableXYDatasetTest
[INFO] Running org.jfree.data.xy.DefaultWindDatasetTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.data.xy.DefaultWindDatasetTest
[INFO] Running org.jfree.data.xy.DefaultXYDatasetTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.data.xy.DefaultXYDatasetTest
[INFO] Running org.jfree.data.xy.DefaultXYZDatasetTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.010 s -- in org.jfree.data.xy.DefaultXYZDatasetTest
[INFO] Running org.jfree.data.xy.IntervalXYDelegateTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.xy.IntervalXYDelegateTest
[INFO] Running org.jfree.data.xy.MatrixSeriesCollectionTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 s -- in org.jfree.data.xy.MatrixSeriesCollectionTest
[INFO] Running org.jfree.data.xy.MatrixSeriesTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.data.xy.MatrixSeriesTest
[INFO] Running org.jfree.data.xy.OHLCDataItemTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 s -- in org.jfree.data.xy.OHLCDataItemTest
[INFO] Running org.jfree.data.xy.TableXYDatasetTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.data.xy.TableXYDatasetTest
[INFO] Running org.jfree.data.xy.VectorDataItemTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 s -- in org.jfree.data.xy.VectorDataItemTest
[INFO] Running org.jfree.data.xy.VectorSeriesCollectionTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.data.xy.VectorSeriesCollectionTest
[INFO] Running org.jfree.data.xy.VectorSeriesTest
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.016 s -- in org.jfree.data.xy.VectorSeriesTest
[INFO] Running org.jfree.data.xy.VectorTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in org.jfree.data.xy.VectorTest
[INFO] Running org.jfree.data.xy.XIntervalDataItemTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.xy.XIntervalDataItemTest
[INFO] Running org.jfree.data.xy.XIntervalSeriesCollectionTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.xy.XIntervalSeriesCollectionTest
[INFO] Running org.jfree.data.xy.XIntervalSeriesTest
[INFO] Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.xy.XIntervalSeriesTest
[INFO] Running org.jfree.data.xy.XYBarDatasetTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.data.xy.XYBarDatasetTest
[INFO] Running org.jfree.data.xy.XYCoordinateTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.xy.XYCoordinateTest
[INFO] Running org.jfree.data.xy.XYDataItemTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in org.jfree.data.xy.XYDataItemTest
[INFO] Running org.jfree.data.xy.XYIntervalDataItemTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.xy.XYIntervalDataItemTest
[INFO] Running org.jfree.data.xy.XYIntervalSeriesCollectionTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 s -- in org.jfree.data.xy.XYIntervalSeriesCollectionTest
[INFO] Running org.jfree.data.xy.XYIntervalSeriesTest
[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 s -- in org.jfree.data.xy.XYIntervalSeriesTest
[INFO] Running org.jfree.data.xy.XYIntervalTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 s -- in org.jfree.data.xy.XYIntervalTest
[INFO] Running org.jfree.data.xy.XYSeriesCollectionTest
[INFO] Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 s -- in org.jfree.data.xy.XYSeriesCollectionTest
[INFO] Running org.jfree.data.xy.XYSeriesTest
[INFO] Tests run: 37, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.033 s -- in org.jfree.data.xy.XYSeriesTest
[INFO] Running org.jfree.data.xy.YIntervalDataItemTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 s -- in org.jfree.data.xy.YIntervalDataItemTest
[INFO] Running org.jfree.data.xy.YIntervalSeriesCollectionTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 s -- in org.jfree.data.xy.YIntervalSeriesCollectionTest
[INFO] Running org.jfree.data.xy.YIntervalSeriesTest
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 s -- in org.jfree.data.xy.YIntervalSeriesTest
[INFO] Running org.jfree.data.xy.YIntervalTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in org.jfree.data.xy.YIntervalTest
[INFO] Running org.jfree.data.xy.YWithXIntervalTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 s -- in org.jfree.data.xy.YWithXIntervalTest
[INFO]
[INFO] Results:
[INFO]
[ERROR] Failures:
[ERROR]   MeterPlotTest.testValueToAngle:387 expected: <315.0> but was: <225.0>
[ERROR]   MeterPlotTest.testValueToAngleWithDifferentMeterAngles:425 expected: <225.0> but was: <135.0>
[INFO]
[ERROR] Tests run: 2356, Failures: 2, Errors: 0, Skipped: 0
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  54.644 s
[INFO] Finished at: 2026-03-17T14:47:12+01:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:3.5.3:test (default-test) on project jfreechart: There are test failures.
[ERROR]
[ERROR] See C:\Users\NatanaelDjajadi\repouni\exp_real\jfreechart\target\surefire-reports for the individual test results.
[ERROR] See dump files (if any exist) [date].dump, [date]-jvmRun[N].dump and [date].dumpstream.
[ERROR] -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
---------------- End output ------------------
```

Checkpoint

Compare

Restore

Thinking

I need to fix the test expectations - I made an error in calculating the expected angles. Let me correct the tests:

Cline wants to edit this file:

/src/test/java/org/jfree/chart/plot/MeterPlotTest.java‎

2

```java
------- SEARCH
    /**
     * Tests valueToAngle method comprehensively to ensure angle calculations
     * are correct. This targets surviving mutants in the value-to-angle conversion.
     */
    @Test
    public void testValueToAngle() {
        MeterPlot plot = new MeterPlot();
        plot.setRange(new Range(0.0, 100.0));
        plot.setMeterAngle(270);
        
        // At minimum value (0), should be at 315 degrees (baseAngle - 0)
        double angle0 = plot.valueToAngle(0.0);
        assertEquals(315.0, angle0, 0.001);
        
        // At midpoint (50), should be at center (180 degrees)
        double angle50 = plot.valueToAngle(50.0);
        assertEquals(180.0, angle50, 0.001);
        
        // At maximum value (100), should be at 45 degrees
        double angle100 = plot.valueToAngle(100.0);
        assertEquals(45.0, angle100, 0.001);
        
        // Test with different range
        plot.setRange(new Range(50.0, 150.0));
        double angleMin = plot.valueToAngle(50.0);
        double angleMax = plot.valueToAngle(150.0);
        assertEquals(315.0, angleMin, 0.001);
        assertEquals(45.0, angleMax, 0.001);
    }
=======
    /**
     * Tests valueToAngle method comprehensively to ensure angle calculations
     * are correct. This targets surviving mutants in the value-to-angle conversion.
     */
    @Test
    public void testValueToAngle() {
        MeterPlot plot = new MeterPlot();
        plot.setRange(new Range(0.0, 100.0));
        plot.setMeterAngle(270);
        
        // With meterAngle=270, baseAngle = 180 + ((270-180)/2) = 225
        // At minimum value (0), angle = 225 - 0 = 225
        double angle0 = plot.valueToAngle(0.0);
        assertEquals(225.0, angle0, 0.001);
        
        // At midpoint (50), angle = 225 - ((50/100)*270) = 225 - 135 = 90
        double angle50 = plot.valueToAngle(50.0);
        assertEquals(90.0, angle50, 0.001);
        
        // At maximum value (100), angle = 225 - 270 = -45
        double angle100 = plot.valueToAngle(100.0);
        assertEquals(-45.0, angle100, 0.001);
        
        // Test with different range - the angles should still be the same
        plot.setRange(new Range(50.0, 150.0));
        double angleMin = plot.valueToAngle(50.0);
        double angleMax = plot.valueToAngle(150.0);
        assertEquals(225.0, angleMin, 0.001);
        assertEquals(-45.0, angleMax, 0.001);
    }
+++++++ REPLACE

------- SEARCH
    /**
     * Tests valueToAngle with various meter angles to verify the calculation
     * formula works correctly for different dial configurations.
     */
    @Test
    public void testValueToAngleWithDifferentMeterAngles() {
        MeterPlot plot = new MeterPlot();
        plot.setRange(new Range(0.0, 100.0));
        
        // Test with 180 degree meter
        plot.setMeterAngle(180);
        double angle0_180 = plot.valueToAngle(0.0);
        double angle100_180 = plot.valueToAngle(100.0);
        assertEquals(180.0, angle0_180, 0.001); // baseAngle = 180
        assertEquals(0.0, angle100_180, 0.001);  // baseAngle - 180
        
        // Test with 90 degree meter
        plot.setMeterAngle(90);
        double angle0_90 = plot.valueToAngle(0.0);
        double angle100_90 = plot.valueToAngle(100.0);
        assertEquals(225.0, angle0_90, 0.001);  // baseAngle = 225
        assertEquals(135.0, angle100_90, 0.001); // baseAngle - 90
        
        // Test with 360 degree meter (full circle)
        plot.setMeterAngle(360);
        double angle0_360 = plot.valueToAngle(0.0);
        double angle50_360 = plot.valueToAngle(50.0);
        double angle100_360 = plot.valueToAngle(100.0);
        assertEquals(270.0, angle0_360, 0.001);
        assertEquals(90.0, angle50_360, 0.001);
        assertEquals(-90.0, angle100_360, 0.001);
    }
=======
    /**
     * Tests valueToAngle with various meter angles to verify the calculation
     * formula works correctly for different dial configurations.
     */
    @Test
    public void testValueToAngleWithDifferentMeterAngles() {
        MeterPlot plot = new MeterPlot();
        plot.setRange(new Range(0.0, 100.0));
        
        // Test with 180 degree meter: baseAngle = 180 + ((180-180)/2) = 180
        plot.setMeterAngle(180);
        double angle0_180 = plot.valueToAngle(0.0);
        double angle100_180 = plot.valueToAngle(100.0);
        assertEquals(180.0, angle0_180, 0.001); // 180 - 0
        assertEquals(0.0, angle100_180, 0.001);  // 180 - 180
        
        // Test with 90 degree meter: baseAngle = 180 + ((90-180)/2) = 135
        plot.setMeterAngle(90);
        double angle0_90 = plot.valueToAngle(0.0);
        double angle100_90 = plot.valueToAngle(100.0);
        assertEquals(135.0, angle0_90, 0.001);  // 135 - 0
        assertEquals(45.0, angle100_90, 0.001); // 135 - 90
        
        // Test with 360 degree meter: baseAngle = 180 + ((360-180)/2) = 270
        plot.setMeterAngle(360);
        double angle0_360 = plot.valueToAngle(0.0);
        double angle50_360 = plot.valueToAngle(50.0);
        double angle100_360 = plot.valueToAngle(100.0);
        assertEquals(270.0, angle0_360, 0.001); // 270 - 0
        assertEquals(90.0, angle50_360, 0.001);  // 270 - 180
        assertEquals(-90.0, angle100_360, 0.001); // 270 - 360
    }
+++++++ REPLACE
```

Checkpoint

Compare

Restore

Thinking

Now let me verify the tests pass:

Cline wants to execute this command:

Completed

```shell
tools\windows\run_tests.cmd
```

```shell
TESTS: OK
```

Checkpoint

Compare

Restore

Thinking

Perfect! All tests pass. Now let me run PIT once at the end to evaluate the effect of the refactoring and new tests:

Cline wants to execute this command:

Completed

```shell
tools\windows\run_pit.cmd
```

```shell
PIT: OK
```

Checkpoint

Compare

Restore

Thinking

Excellent! PIT has run successfully. Now let me check the results to see how the refactoring and new tests have improved the mutation score for MeterPlot:

Cline wants to use a tool on the `PIT-MCPServer` MCP server:

pit_methods

Auto-approve

Return per-method mutation scores (test strength) for a given class, using the latest PIT mutations.xml under <workspace>/target/pit-reports. A null mutationScore means that method had no mutants executed by tests (covered=0; only NO_COVERAGE).

Arguments

```json
{
  "workspace": "c:/Users/NatanaelDjajadi/repouni/exp_real/jfreechart",
  "className": "org.jfree.chart.plot.MeterPlot"
}
```

Response

Plain TextRich DisplayMarkdown

Checkpoint

Compare

Restore

Thinking

Excellent results! Let me create a summary document of the improvements:

Task Completed

Successfully refactored MeterPlot (the class with the fourth-highest number of survived mutants) to increase observability of internally mutated behavior.

## Summary of Refactoring Work

### Refactoring Technique Applied:

__Extract Method__ - Extracted pure calculation logic from graphics rendering methods to make internal behavior observable and testable.

### Changes Made:

1. __Created TickEndpoints value object__ (`src/main/java/org/jfree/chart/plot/TickEndpoints.java`)

   - Immutable class to hold tick endpoint coordinates
   - Makes coordinate calculations observable

2. __Extracted calculateTickEndpoints method__ in MeterPlot

   - Separates coordinate calculation from graphics drawing
   - Takes meterArea and value as input
   - Returns TickEndpoints with calculated coordinates
   - Previously this logic was embedded in drawTick() method where it was unobservable

3. __Added comprehensive tests__ in MeterPlotTest:

   - `testCalculateTickEndpoints()` - Tests basic endpoint calculations
   - `testCalculateTickEndpointsAngles()` - Tests mathematical accuracy of calculations
   - `testCalculateTickEndpointsDifferentAngles()` - Tests with various meter angles
   - `testValueToAngle()` - Tests value-to-angle conversion with boundary cases
   - `testValueToAngleWithDifferentMeterAngles()` - Tests angle calculations with different configurations

### Results - Mutation Score Improvements:

__New calculateTickEndpoints method:__

- Mutation Score: __100%__ (1.0)
- Killed: 20 mutants
- Survived: 0 mutants
- Perfect observability of coordinate calculations

__valueToAngle method:__

- Mutation Score: __100%__ (1.0)
- Killed: 8 mutants
- Survived: 0 mutants
- All angle calculation mutants now observable

### Why This Increases Observability:

__Before:__ Coordinate calculations were embedded in `drawTick()` method which performs graphics operations. Since graphics output cannot be easily tested, the 27 mathematical mutants in coordinate calculations survived (0% mutation score).

__After:__ By extracting `calculateTickEndpoints()` as a pure function that returns a testable value object, we can:

1. Directly test coordinate calculations without graphics context
2. Assert on exact coordinate values
3. Distinguish correct calculations from mutated alternatives
4. Achieve 100% mutation coverage for the mathematical operations

The refactoring demonstrates how __Extract Method__ increases observability by separating testable logic (calculations) from untestable operations (graphics rendering), enabling tests to verify correctness of previously unobservable internal behavior.
