"""
SAT Math Solver for HP Prime G2 (MicroPython)
Copyright (C) 2026 (cheeseburgerjr)
License: GPLv3
Covers all Digital SAT Math topics.
"""

import math

def log_base(x, base):
    if base <= 0 or base == 1:
        raise ValueError("Log base must be positive and not equal to 1.")
    return math.log(x) / math.log(base)

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def median_of_list(lst):
    if not lst:
        return None
    s = sorted(lst)
    n = len(s)
    if n % 2:
        return s[n//2]
    return (s[n//2 - 1] + s[n//2]) / 2

SEARCH_INDEX = {
    "linear": ("Heart of Algebra", "1", "Linear Equations (one variable): solves ax + b = cx + d with step‑by‑step"),
    "slope": ("Heart of Algebra", "2", "Slope / Intercepts: finds slope and intercepts from points or y = mx + b"),
    "system": ("Heart of Algebra", "3", "Systems of Linear Equations: solves two equations using Cramer's rule"),
    "inequality": ("Heart of Algebra", "4", "Linear Inequalities (one variable): solves ax + b < c (or >, <=, >=)"),
    "function": ("Heart of Algebra", "6", "Linear Functions: evaluate f(x) or find x from f(x) = y"),
    "quadratic": ("Advanced Math", "2", "Quadratic Equations: solves ax² + bx + c = 0 using the quadratic formula"),
    "parabola": ("Advanced Math", "3", "Parabolas: finds vertex, axis, intercepts and direction"),
    "nonlinear": ("Advanced Math", "4", "System of Line & Parabola/Circle: finds intersections of curves"),
    "exponential": ("Advanced Math", "5", "Exponential Functions: growth/decay, compound interest, half‑life"),
    "polynomial": ("Advanced Math", "6", "Polynomial Functions (roots): finds roots of quadratics or integer roots of cubics"),
    "rational": ("Advanced Math", "7", "Rational Functions: finds vertical and horizontal asymptotes"),
    "radical": ("Advanced Math", "8", "Radical Equations: solves √(ax + b) = cx + d with domain checks"),
    "absolute": ("Advanced Math", "9", "Absolute Value Equations: solves |ax + b| = c with both cases"),
    "ratio": ("Problem Solving", "1", "Ratios / Rates / Conversions: solves proportions, unit rates, speed/distance/time"),
    "percent": ("Problem Solving", "2", "Percent Problems: finds percentage, percent change, discount, tax, tip"),
    "probability": ("Problem Solving", "3", "Probability: simple P = fav/total or compound AND/OR events"),
    "statistics": ("Problem Solving", "5", "Descriptive Statistics: mean, median, mode, quartiles, variance, std dev"),
    "scatterplot": ("Problem Solving", "6", "Data Visualization: guide to interpreting scatterplots and graphs"),
    "survey": ("Problem Solving", "7", "Surveys & Experiments: guide to evaluating statistical studies"),
    "area": ("Geometry", "1", "Area: calculates area of rectangles, triangles, circles, sectors, etc."),
    "volume": ("Geometry", "2", "Volume: calculates volume of prisms, cylinders, cones, spheres, pyramids"),
    "coordinate": ("Geometry", "3", "Coordinate Geometry: distance, midpoint, slope, and line equation"),
    "angle": ("Geometry", "4", "Lines & Angles: complement, supplement, parallel lines with transversal"),
    "triangle": ("Geometry", "5", "Triangles: angle sum, exterior angle, similarity scale factor"),
    "right triangle": ("Geometry", "6", "Right Triangles: Pythagorean theorem and 30‑60‑90 / 45‑45‑90 ratios"),
    "pythagorean": ("Geometry", "6", "Right Triangles: Pythagorean theorem and special right triangles"),
    "trigonometry": ("Geometry", "7", "Trigonometry: finds missing sides or angles in right triangles"),
    "circle": ("Geometry", "8", "Circles: circumference, area, arc length, sector area, equation"),
    "log": ("Additional Topics", "1", "Logarithms & Exponential Equations: evaluate or solve logs"),
    "logarithm": ("Additional Topics", "1", "Logarithms & Exponential Equations: evaluate or solve logs"),
    "sequence": ("Additional Topics", "2", "Sequences & Series: arithmetic and geometric nth term and sum"),
    "series": ("Additional Topics", "2", "Sequences & Series: arithmetic and geometric nth term and sum"),
    "complex": ("Additional Topics", "3", "Complex Numbers: add, subtract, multiply, divide, modulus, conjugate"),
    "counting": ("Additional Topics", "4", "Counting & Probability: factorial n!, permutations nPr, combinations nCr"),
    "factorial": ("Additional Topics", "4", "Counting & Probability: factorial n!, permutations nPr, combinations nCr"),
    "permutation": ("Additional Topics", "4", "Counting & Probability: factorial n!, permutations nPr, combinations nCr"),
    "combination": ("Additional Topics", "4", "Counting & Probability: factorial n!, permutations nPr, combinations nCr"),
    "binomial": ("Additional Topics", "5", "Binomial Theorem: finds specific term in (a+b)^n"),
    "matrix": ("Additional Topics", "6", "Matrices & Vectors: determinant, inverse, solve 2x2 systems"),
    "matrices": ("Additional Topics", "6", "Matrices & Vectors: determinant, inverse, solve 2x2 systems"),
    "vector": ("Additional Topics", "6", "Matrices & Vectors: magnitude, dot product, angle between"),
    "vectors": ("Additional Topics", "6", "Matrices & Vectors: magnitude, dot product, angle between"),
    "sine": ("Additional Topics", "7", "Law of Sines / Cosines: finds missing sides or angles in triangles"),
    "cosine": ("Additional Topics", "7", "Law of Sines / Cosines: finds missing sides or angles in triangles"),
    "heron": ("Additional Topics", "8", "Heron's Formula: area of triangle from three sides"),
    "3d": ("Additional Topics", "9", "3D Distance: distance between two points in three‑dimensional space"),
    "quadratic inequality": ("Additional Topics", "10", "Quadratic Inequality: solves ax²+bx+c > 0 (or <, <=, >=)"),
    "absolute inequality": ("Additional Topics", "11", "Absolute Value Inequality: solves |ax+b| < c (or >, <=, >=)"),
    "radian": ("Additional Topics", "12", "Radian/Degree Converter: converts between radians and degrees"),
    "degree": ("Additional Topics", "12", "Radian/Degree Converter: converts between radians and degrees"),
    "long division": ("Additional Topics", "13", "Polynomial Long Division: divides polynomial by (x - c)"),
    "remainder": ("Additional Topics", "14", "Remainder Theorem: evaluates P(c) using synthetic substitution"),
    "completing square": ("Additional Topics", "15", "Completing the Square: rewrites x²+bx+c as (x+p)²+q"),
    "transform": ("Additional Topics", "16", "Function Guides: transformations, inverse functions, piecewise"),
    "work": ("Additional Topics", "17", "Advanced Word Problems: work/rate, mixture, distance/rate/time guides"),
    "mixture": ("Additional Topics", "17", "Advanced Word Problems: work/rate, mixture, distance/rate/time guides"),
    "conic": ("Additional Topics", "19", "Conic Sections Guide: parabolas, circles, ellipses, hyperbolas"),
    "even odd": ("Additional Topics", "20", "Even/Odd, Domain/Range, Composition: function property guides"),
    "domain": ("Additional Topics", "20", "Even/Odd, Domain/Range, Composition: function property guides"),
    "range": ("Additional Topics", "20", "Even/Odd, Domain/Range, Composition: function property guides"),
    "composition": ("Additional Topics", "20", "Even/Odd, Domain/Range, Composition: function property guides"),
    "fraction": ("Utilities", "1", "Fraction <-> Decimal: converts fractions to decimals and vice versa"),
    "decimal": ("Utilities", "2", "Decimal <-> Percent: converts between decimals and percentages"),
    "gcf": ("Utilities", "4", "GCF: greatest common factor of two numbers"),
    "lcm": ("Utilities", "5", "LCM: least common multiple of two numbers"),
    "prime": ("Utilities", "6", "Prime Factorization: finds prime factors of an integer"),
    "scientific": ("Utilities", "7", "Scientific Notation Converter: standard ↔ scientific notation"),
    "formula": ("Formula Reference", "1", "Formula Reference: browse key SAT formulas with examples"),
}

# ----------------------------------------------------------------------
# USER INTERFACE CLASS
# ----------------------------------------------------------------------
class UI:
    @staticmethod
    def clear():
        print("\n" * 30)

    @staticmethod
    def wait(prompt="Press Enter to continue."):
        input(prompt)

    @staticmethod
    def get_float(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid number. Please enter a numeric value.")

    @staticmethod
    def get_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid integer. Please enter a whole number.")

    @staticmethod
    def get_positive_float(prompt):
        while True:
            val = UI.get_float(prompt)
            if val > 0:
                return val
            print("Value must be positive.")

    @staticmethod
    def get_nonzero_float(prompt):
        while True:
            val = UI.get_float(prompt)
            if val != 0:
                return val
            print("Value cannot be zero.")

    @staticmethod
    def show_step(label, value):
        print("  {}: {}".format(label, value))

    @staticmethod
    def show_result(label, value):
        print("{} = {}".format(label, value))

# ----------------------------------------------------------------------
# SOLVER REGISTRY
# ----------------------------------------------------------------------
class SolverRegistry:
    _categories = {}

    @classmethod
    def register(cls, category, key, name, func):
        if category not in cls._categories:
            cls._categories[category] = {}
        cls._categories[category][key] = (name, func)

    @classmethod
    def get_categories(cls):
        return sorted(cls._categories.keys())

    @classmethod
    def get_solvers(cls, category):
        return cls._categories.get(category, {})

    @classmethod
    def run_solver(cls, category, key):
        solvers = cls.get_solvers(category)
        if key in solvers:
            _, func = solvers[key]
            func()
            return True
        return False

# ----------------------------------------------------------------------
# DECORATOR FOR EASY REGISTRATION
# ----------------------------------------------------------------------
def solver(category, key, name):
    def decorator(func):
        SolverRegistry.register(category, key, name, func)
        return func
    return decorator

# ----------------------------------------------------------------------
# INTERACTIVE SEARCH FUNCTION
# ----------------------------------------------------------------------
def search_solver():
    while True:
        UI.clear()
        print("SEARCH SOLVERS")
        print("Enter a keyword (e.g., 'matrix', 'statistics') or 0 to return to main menu.")
        keyword = input("Keyword: ").strip().lower()
        if keyword == "0":
            return

        if not keyword:
            print("Please enter a keyword.")
            UI.wait()
            continue

        matches = []
        for k, (cat, key, desc) in SEARCH_INDEX.items():
            if keyword in k:
                matches.append((cat, key, desc))

        if not matches:
            print("No solver found for '{}'. Try a different term.".format(keyword))
            UI.wait()
            continue

        print("\nMatching solvers:\n")
        for idx, (cat, key, desc) in enumerate(matches, 1):
            print("{}. {}: {}".format(idx, desc.split(":")[0].strip(), desc))

        while True:
            print("\nEnter the ID to select a solver, or 0 to return to main menu.")
            choice = input("Choice: ").strip()
            if choice == "0":
                return
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(matches):
                    cat, key, _ = matches[choice_num - 1]
                    SolverRegistry.run_solver(cat, key)
                    break  # after solver finishes, return to search prompt
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid selection. Please enter a number.")

# ----------------------------------------------------------------------
# SOLVERS – HEART OF ALGEBRA
# ----------------------------------------------------------------------
@solver("Heart of Algebra", "1", "Linear Equations (one variable)")
def solve_linear_one_var():
    UI.clear()
    print("Solve: ax + b = cx + d")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    d = UI.get_float("d = ")
    steps = []
    steps.append("Original equation: {}x + {} = {}x + {}".format(a, b, c, d))
    coeff = a - c
    const = d - b
    steps.append("Subtract {}x from both sides: ({} - {})x + {} = {}".format(c, a, c, b, d))
    steps.append("Simplify: {}x + {} = {}".format(coeff, b, d))
    steps.append("Subtract {} from both sides: {}x = {}".format(b, coeff, d - b))
    steps.append("Simplify: {}x = {}".format(coeff, const))
    if coeff == 0:
        if const == 0:
            steps.append("Infinite solutions (identity).")
            final = "All real numbers"
        else:
            steps.append("No solution (contradiction).")
            final = "No solution"
    else:
        x = const / coeff
        steps.append("Divide by {}: x = {} / {} = {}".format(coeff, const, coeff, x))
        final = "x = {}".format(x)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Heart of Algebra", "2", "Slope / Intercepts")
def solve_slope_intercepts():
    UI.clear()
    print("Find slope / intercepts")
    print("1. From two points")
    print("2. From slope-intercept form (y = mx + b)")
    ch = input("Choice: ")
    if ch == "1":
        x1 = UI.get_float("x1 = ")
        y1 = UI.get_float("y1 = ")
        x2 = UI.get_float("x2 = ")
        y2 = UI.get_float("y2 = ")
        steps = []
        steps.append("Points: ({}, {}) and ({}, {})".format(x1, y1, x2, y2))
        if x2 - x1 == 0:
            steps.append("Vertical line (undefined slope). x-intercept = {}".format(x1))
            print("\n".join("Step {}: {}".format(i+1, s) for i, s in enumerate(steps)))
            print("\n" + "─" * 40)
            print("Final answer: x = {}, vertical line".format(x1))
            UI.wait()
            return
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        steps.append("Slope formula: m = ({} - {}) / ({} - {}) = {}".format(y2, y1, x2, x1, m))
        steps.append("Using point-slope: y - {} = {}(x - {})".format(y1, m, x1))
        steps.append("Simplify: y = {}x + {}".format(m, b))
        if m != 0:
            x_int = -b / m
            steps.append("x-intercept: set y=0 → 0 = {}x + {} → x = {}".format(m, b, x_int))
            final = "Slope: {}, y-intercept: (0, {}), x-intercept: ({}, 0)".format(m, b, x_int)
        else:
            steps.append("Horizontal line, no x-intercept (unless b=0 then all x)")
            final = "Slope: 0, y-intercept: (0, {}), horizontal line".format(b)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        m = UI.get_float("m = ")
        b = UI.get_float("b = ")
        steps = []
        steps.append("Equation: y = {}x + {}".format(m, b))
        if m != 0:
            x_int = -b / m
            steps.append("x-intercept: set y=0 → 0 = {}x + {} → x = {}".format(m, b, x_int))
            final = "Slope: {}, y-intercept: (0, {}), x-intercept: ({}, 0)".format(m, b, x_int)
        else:
            steps.append("Horizontal line (m=0).")
            final = "Slope: 0, y-intercept: (0, {}), horizontal line".format(b)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Heart of Algebra", "3", "Systems of Linear Equations")
def solve_linear_system():
    UI.clear()
    print("System of two linear equations:")
    print("a1 x + b1 y = c1")
    print("a2 x + b2 y = c2")
    a1 = UI.get_float("a1 = ")
    b1 = UI.get_float("b1 = ")
    c1 = UI.get_float("c1 = ")
    a2 = UI.get_float("a2 = ")
    b2 = UI.get_float("b2 = ")
    c2 = UI.get_float("c2 = ")
    steps = []
    steps.append("Equations:")
    steps.append("  {}x + {}y = {}".format(a1, b1, c1))
    steps.append("  {}x + {}y = {}".format(a2, b2, c2))
    det = a1*b2 - a2*b1
    steps.append("Coefficient matrix determinant: D = {}*{} - {}*{} = {}".format(a1, b2, a2, b1, det))
    if abs(det) < 1e-9:
        if abs(a1*c2 - a2*c1) < 1e-9 and abs(b1*c2 - b2*c1) < 1e-9:
            steps.append("Dependent equations → infinite solutions.")
            final = "Infinite solutions"
        else:
            steps.append("Inconsistent equations → no solution.")
            final = "No solution"
    else:
        Dx = c1*b2 - c2*b1
        Dy = a1*c2 - a2*c1
        steps.append("Dx = c1*b2 - c2*b1 = {}*{} - {}*{} = {}".format(c1, b2, c2, b1, Dx))
        steps.append("Dy = a1*c2 - a2*c1 = {}*{} - {}*{} = {}".format(a1, c2, a2, c1, Dy))
        x = Dx / det
        y = Dy / det
        steps.append("x = Dx / D = {} / {} = {}".format(Dx, det, x))
        steps.append("y = Dy / D = {} / {} = {}".format(Dy, det, y))
        final = "x = {}, y = {}".format(x, y)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Heart of Algebra", "4", "Linear Inequalities (one variable)")
def solve_linear_inequality():
    UI.clear()
    print("Solve linear inequality: ax + b < c   (or >, <=, >=)")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    op = input("Operator (<, >, <=, >=): ").strip()
    valid_ops = {"<", ">", "<=", ">="}
    if op not in valid_ops:
        print("Invalid operator. Please try again.")
        UI.wait()
        return
    steps = []
    steps.append("Original: {}x + {} {} {}".format(a, b, op, c))
    if a == 0:
        steps.append("a = 0 → not a linear inequality.")
        final = "Invalid (a=0)"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
        UI.wait()
        return
    rhs = c - b
    steps.append("Subtract {} from both sides: {}x {} {}".format(b, a, op, rhs))
    if a < 0:
        flip = {"<":">", ">":"<", "<=":">=", ">=":"<="}
        new_op = flip.get(op, op)
        steps.append("Divide by {} (negative, so flip inequality): x {} {}".format(a, new_op, rhs/a))
        final = "x {} {}".format(new_op, rhs/a)
    else:
        steps.append("Divide by {}: x {} {}".format(a, op, rhs/a))
        final = "x {} {}".format(op, rhs/a)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Heart of Algebra", "5", "Linear Inequalities (two variables) [guide]")
def guide_linear_inequalities_two_vars():
    UI.clear()
    print("=" * 40)
    print("  LINEAR INEQUALITIES IN TWO VARIABLES")
    print("=" * 40)
    print("""
The SAT often asks you to interpret inequalities like:
      y > 2x + 1
or systems such as:
      y <= -x + 3
      y > 0.5x - 2

Key ideas:
- The boundary line (replace inequality with =)
  is solid if <= or >=, dashed if < or >.
- Shade the region that satisfies the inequality.
  Test a point (0,0) if it's not on the line.
- For a system, the solution is the overlap
  of the shaded regions.

Example SAT question:
  "Which ordered pair is a solution to the system:
       y >= x + 1
       y < -x + 4 ?"

Strategy:
  Plug each answer choice into both inequalities.
  The pair that makes both true is the answer.

Let's test (2,3):
  y >= x+1 -> 3 >= 3 (true)
  y < -x+4 -> 3 < 2 (false) -> reject

Try (0,0):
  0 >= 1 (false) -> reject

Try (1,2):
  2 >= 2 (true)
  2 < -1+4=3 (true) -> correct!

Answer: (1,2)

Remember: Always check the boundary line type
and use a test point when the graph is given.
""")
    UI.wait()

@solver("Heart of Algebra", "6", "Linear Functions")
def solve_linear_function():
    UI.clear()
    print("Linear function: f(x) = mx + b")
    print("1. Evaluate f(x) for a given x")
    print("2. Find x when f(x) is given")
    ch = input("Choice: ")
    m = UI.get_float("m = ")
    b = UI.get_float("b = ")
    if ch == "1":
        x = UI.get_float("x = ")
        steps = []
        steps.append("f(x) = {}x + {}".format(m, b))
        steps.append("Substitute x = {}: f({}) = {}*{} + {}".format(x, x, m, x, b))
        fx = m*x + b
        steps.append("= {} + {} = {}".format(m*x, b, fx))
        final = "f({}) = {}".format(x, fx)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        y = UI.get_float("f(x) = ")
        steps = []
        steps.append("Solve {}x + {} = {}".format(m, b, y))
        if m == 0:
            if y == b:
                steps.append("All x are solutions (0*x = 0).")
                final = "All real numbers"
            else:
                steps.append("No solution (0*x = {})".format(y - b))
                final = "No solution"
        else:
            steps.append("Subtract {}: {}x = {}".format(b, m, y - b))
            x = (y - b) / m
            steps.append("Divide by {}: x = {}".format(m, x))
            final = "x = {}".format(x)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

# ----------------------------------------------------------------------
# SOLVERS – ADVANCED MATH
# ----------------------------------------------------------------------
@solver("Advanced Math", "1", "Equivalent Expressions (simplify/factor)")
def simplify_expression():
    UI.clear()
    print("Equivalent Expressions (basic expand/factor)")
    print("1. Expand (ax+b)(cx+d)")
    print("2. Factor x^2 + px + q")
    ch = input("Choice: ")
    if ch == "1":
        a = UI.get_float("a = ")
        b = UI.get_float("b = ")
        c = UI.get_float("c = ")
        d = UI.get_float("d = ")
        steps = []
        steps.append("Expand ({}x+{})({}x+{})".format(a, b, c, d))
        ac = a*c
        ad_bc = a*d + b*c
        bd = b*d
        steps.append("Multiply: {}x^2 + {}x + {}".format(ac, ad_bc, bd))
        final = "Expanded: {}x^2 + {}x + {}".format(ac, ad_bc, bd)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        p = UI.get_float("p = ")
        q = UI.get_float("q = ")
        steps = []
        steps.append("Factor x^2 + {}x + {}".format(p, q))
        disc = p*p - 4*q
        steps.append("Discriminant = {}^2 - 4*1*{} = {}".format(p, q, disc))
        if disc < 0:
            steps.append("Cannot factor over real numbers.")
            final = "No real factors"
        else:
            sqrt_disc = math.sqrt(disc)
            r1 = (-p + sqrt_disc)/2
            r2 = (-p - sqrt_disc)/2
            steps.append("Roots: x = {} and x = {}".format(r1, r2))
            steps.append("Factored: (x - {})(x - {})".format(r1, r2))
            final = "(x - {})(x - {})".format(r1, r2)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Advanced Math", "2", "Quadratic Equations (factoring/quad. formula)")
def solve_quadratic_menu():
    UI.clear()
    print("Quadratic Equation: ax^2 + bx + c = 0")
    a = UI.get_nonzero_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    steps = []
    steps.append("Equation: {}x^2 + {}x + {} = 0".format(a, b, c))
    disc = b*b - 4*a*c
    steps.append("Discriminant D = {}^2 - 4*{}*{} = {}".format(b, a, c, disc))
    if disc < 0:
        steps.append("D < 0 → no real solutions.")
        final = "No real solutions"
    elif disc == 0:
        x = -b/(2*a)
        steps.append("D = 0 → one real solution (double root).")
        steps.append("x = -{}/ (2*{}) = {}".format(b, a, x))
        final = "x = {}".format(x)
    else:
        sqrt_disc = math.sqrt(disc)
        steps.append("D > 0 → two real solutions.")
        steps.append("x₁ = (-{} + √{}) / (2*{})".format(b, disc, a))
        x1 = (-b + sqrt_disc)/(2*a)
        steps.append("x₁ = ({} + {}) / {} = {}".format(-b, sqrt_disc, 2*a, x1))
        steps.append("x₂ = (-{} - √{}) / (2*{})".format(b, disc, a))
        x2 = (-b - sqrt_disc)/(2*a)
        steps.append("x₂ = ({} - {}) / {} = {}".format(-b, sqrt_disc, 2*a, x2))
        final = "x₁ = {}, x₂ = {}".format(x1, x2)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Advanced Math", "3", "Parabolas (vertex, intercepts)")
def parabola_analysis():
    UI.clear()
    print("Parabola: y = ax^2 + bx + c")
    a = UI.get_nonzero_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    steps = []
    steps.append("Equation: y = {}x^2 + {}x + {}".format(a, b, c))
    h = -b/(2*a)
    k = a*h*h + b*h + c
    steps.append("Vertex x = -b/(2a) = -{}/ (2*{}) = {}".format(b, a, h))
    steps.append("y-coordinate = {}*{}^2 + {}*{} + {} = {}".format(a, h, b, h, c, k))
    steps.append("Vertex: ({}, {})".format(h, k))
    steps.append("Axis of symmetry: x = {}".format(h))
    direction = "up" if a > 0 else "down"
    extrema = "minimum" if a > 0 else "maximum"
    steps.append("Opens {} ({} value = {})".format(direction, extrema, k))
    disc = b*b - 4*a*c
    if disc >= 0:
        sq = math.sqrt(disc)
        x1 = (-b + sq)/(2*a)
        x2 = (-b - sq)/(2*a)
        steps.append("x-intercepts: {} and {}".format(x1, x2))
    else:
        steps.append("No x-intercepts.")
    steps.append("y-intercept: (0, {})".format(c))
    final = "Vertex: ({}, {}), axis: x = {}, opens {}".format(h, k, h, direction)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Advanced Math", "4", "System of Line & Parabola/Circle")
def solve_nonlinear_system():
    UI.clear()
    print("Nonlinear system solver:")
    print("1. Line and Parabola")
    print("2. Line and Circle (center at origin)")
    ch = input("Choice: ")
    if ch == "1":
        m = UI.get_float("Line slope m = ")
        b_line = UI.get_float("Line intercept b = ")
        a = UI.get_nonzero_float("Parabola a = ")
        b = UI.get_float("Parabola b = ")
        c = UI.get_float("Parabola c = ")
        steps = []
        steps.append("Line: y = {}x + {}".format(m, b_line))
        steps.append("Parabola: y = {}x^2 + {}x + {}".format(a, b, c))
        A = a
        B = b - m
        C = c - b_line
        steps.append("Set equal: {}x^2 + {}x + {} = 0".format(A, B, C))
        disc = B*B - 4*A*C
        steps.append("Discriminant = {}^2 - 4*{}*{} = {}".format(B, A, C, disc))
        if disc < 0:
            steps.append("No intersection (discriminant < 0).")
            final = "No intersection"
        elif disc == 0:
            x = -B/(2*A)
            y = m*x + b_line
            steps.append("Tangent point: x = {}, y = {}".format(x, y))
            final = "Tangent at ({}, {})".format(x, y)
        else:
            sq = math.sqrt(disc)
            x1 = (-B + sq)/(2*A)
            y1 = m*x1 + b_line
            x2 = (-B - sq)/(2*A)
            y2 = m*x2 + b_line
            steps.append("x₁ = {}, y₁ = {}".format(x1, y1))
            steps.append("x₂ = {}, y₂ = {}".format(x2, y2))
            final = "Intersections: ({}, {}) and ({}, {})".format(x1, y1, x2, y2)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        r = UI.get_positive_float("Radius r = ")
        m = UI.get_float("Line slope m = ")
        b_line = UI.get_float("Line y-intercept b = ")
        steps = []
        steps.append("Circle: x^2 + y^2 = {}".format(r*r))
        steps.append("Line: y = {}x + {}".format(m, b_line))
        A = 1 + m*m
        B = 2*m*b_line
        C = b_line*b_line - r*r
        steps.append("Substitute: (1 + {})x^2 + 2*{}*{}x + {}^2 - {} = 0".format(m*m, m, b_line, b_line, r*r))
        steps.append(" => {}x^2 + {}x + {} = 0".format(A, B, C))
        disc = B*B - 4*A*C
        steps.append("Discriminant = {}^2 - 4*{}*{} = {}".format(B, A, C, disc))
        if disc < 0:
            steps.append("No intersection (discriminant < 0).")
            final = "No intersection"
        elif disc == 0:
            x = -B/(2*A)
            y = m*x + b_line
            steps.append("Tangent point: x = {}, y = {}".format(x, y))
            final = "Tangent at ({}, {})".format(x, y)
        else:
            sq = math.sqrt(disc)
            x1 = (-B + sq)/(2*A)
            y1 = m*x1 + b_line
            x2 = (-B - sq)/(2*A)
            y2 = m*x2 + b_line
            steps.append("x₁ = {}, y₁ = {}".format(x1, y1))
            steps.append("x₂ = {}, y₂ = {}".format(x2, y2))
            final = "Intersections: ({}, {}) and ({}, {})".format(x1, y1, x2, y2)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Advanced Math", "5", "Exponential Functions (growth/decay)")
def exponential_functions():
    UI.clear()
    print("Exponential Functions")
    print("1. Basic Growth/Decay: y = a * b^x")
    print("2. Compound Interest: A = P(1 + r/n)^(nt)")
    print("3. Half-life / Doubling time")
    ch = input("Choice: ")
    if ch == "1":
        a = UI.get_float("Initial amount a = ")
        b = UI.get_positive_float("Growth/decay factor b = ")
        x = UI.get_float("x = ")
        steps = []
        steps.append("y = {} * {}^{}".format(a, b, x))
        y = a * (b ** x)
        steps.append("= {} * {} = {}".format(a, b**x, y))
        final = "y = {}".format(y)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        P = UI.get_float("Principal P = ")
        r = UI.get_float("Annual rate (as decimal) r = ")
        n = UI.get_positive_float("Compounded per year n = ")
        t = UI.get_float("Time (years) t = ")
        steps = []
        steps.append("A = P(1 + r/n)^(nt)")
        steps.append("A = {} * (1 + {}/{})^({}*{})".format(P, r, n, n, t))
        A = P * (1 + r/n) ** (n*t)
        steps.append("A = {} * {} = {}".format(P, (1 + r/n)**(n*t), A))
        final = "A = {}".format(A)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        print("1. Half-life (decay)")
        print("2. Doubling time (growth)")
        sub = input("Choice: ")
        if sub == "1":
            init = UI.get_float("Initial amount = ")
            hl = UI.get_positive_float("Half-life = ")
            time = UI.get_float("Time elapsed = ")
            steps = []
            steps.append("Remaining = init * (1/2)^(time / half_life)")
            steps.append("= {} * (1/2)^({} / {})".format(init, time, hl))
            remaining = init * (0.5 ** (time / hl))
            steps.append("= {} * {} = {}".format(init, 0.5**(time/hl), remaining))
            final = "Remaining = {}".format(remaining)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "2":
            init = UI.get_float("Initial amount = ")
            dt = UI.get_positive_float("Doubling time = ")
            time = UI.get_float("Time elapsed = ")
            steps = []
            steps.append("Final = init * 2^(time / doubling_time)")
            steps.append("= {} * 2^({} / {})".format(init, time, dt))
            final_val = init * (2 ** (time / dt))
            steps.append("= {} * {} = {}".format(init, 2**(time/dt), final_val))
            final = "Final = {}".format(final_val)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Advanced Math", "6", "Polynomial Functions (roots)")
def polynomial_roots():
    UI.clear()
    print("Polynomial roots (up to quadratic for exact)")
    print("1. Quadratic (ax^2+bx+c)")
    print("2. Cubic (limited to guess integer root)")
    ch = input("Choice: ")
    if ch == "1":
        a = UI.get_nonzero_float("a = ")
        b = UI.get_float("b = ")
        c = UI.get_float("c = ")
        steps = []
        steps.append("Equation: {}x^2 + {}x + {} = 0".format(a, b, c))
        disc = b*b - 4*a*c
        steps.append("Discriminant D = {}^2 - 4*{}*{} = {}".format(b, a, c, disc))
        if disc < 0:
            steps.append("No real roots.")
            final = "No real roots"
        else:
            sq = math.sqrt(disc)
            r1 = (-b + sq)/(2*a)
            r2 = (-b - sq)/(2*a)
            steps.append("x₁ = ({} + {}) / {} = {}".format(-b, sq, 2*a, r1))
            steps.append("x₂ = ({} - {}) / {} = {}".format(-b, sq, 2*a, r2))
            final = "Roots: {}, {}".format(r1, r2)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        a = UI.get_float("a = ")
        b = UI.get_float("b = ")
        c = UI.get_float("c = ")
        d = UI.get_float("d = ")
        steps = []
        steps.append("Cubic: {}x^3 + {}x^2 + {}x + {} = 0".format(a, b, c, d))
        found = False
        for x in range(-20, 21):
            val = a*x**3 + b*x**2 + c*x + d
            if abs(val) < 1e-9:
                steps.append("Found integer root: x = {}".format(x))
                found = True
                break
        if not found:
            a_int = int(round(a)) if abs(a - round(a)) < 1e-9 else None
            d_int = int(round(d)) if abs(d - round(d)) < 1e-9 else None
            if a_int is not None and d_int is not None and a_int != 0 and d_int != 0:
                def divisors(n):
                    n = abs(n)
                    divs = set()
                    for i in range(1, int(math.sqrt(n)) + 1):
                        if n % i == 0:
                            divs.add(i)
                            divs.add(n // i)
                    return list(divs)
                a_divs = divisors(a_int)
                d_divs = divisors(d_int)
                for p in d_divs:
                    for q in a_divs:
                        for sign in (1, -1):
                            x = sign * p / q
                            val = a*x**3 + b*x**2 + c*x + d
                            if abs(val) < 1e-9:
                                steps.append("Found rational root: x = {}".format(x))
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
        if not found:
            steps.append("No rational root found within tested range.")
            final = "No integer/rational root found."
        else:
            final = "Root found: x = {}".format(x)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Advanced Math", "7", "Rational Functions (asymptotes)")
def rational_functions():
    UI.clear()
    print("Rational function: f(x) = (ax + b) / (cx + d)")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    d = UI.get_float("d = ")
    steps = []
    steps.append("f(x) = ({}x + {}) / ({}x + {})".format(a, b, c, d))
    if c == 0:
        steps.append("Denominator constant → not a rational function.")
        final = "Not a rational function"
    else:
        vertical = -d / c
        horizontal = a / c
        steps.append("Vertical asymptote: set denominator = 0 → {}x + {} = 0 → x = {}".format(c, d, vertical))
        steps.append("Horizontal asymptote: compare degrees → y = {}".format(horizontal))
        steps.append("Domain: all real x except {}".format(vertical))
        final = "Vertical: x = {}, Horizontal: y = {}".format(vertical, horizontal)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Advanced Math", "8", "Radical Equations")
def solve_radical_equation():
    UI.clear()
    print("Solve sqrt(ax + b) = cx + d")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    d = UI.get_float("d = ")
    steps = []
    steps.append("Equation: √({}x + {}) = {}x + {}".format(a, b, c, d))
    A = c*c
    B = 2*c*d - a
    C = d*d - b
    steps.append("Square both sides: {}x + {} = ({}x + {})^2".format(a, b, c, d))
    steps.append("Expand: {}x^2 + {}x + {} = 0".format(A, B, C))
    if A == 0:
        if B == 0:
            if abs(C) < 1e-12:
                steps.append("Identity (all x) after squaring, but domain must be checked.")
                final = "All x (check domain)"
            else:
                steps.append("No solution after squaring.")
                final = "No solution"
        else:
            x = -C / B
            steps.append("Linear: x = {} / {} = {}".format(-C, B, x))
            if a*x + b >= 0 and c*x + d >= 0:
                left = math.sqrt(a*x + b)
                right = c*x + d
                if abs(left - right) < 1e-9:
                    steps.append("Check: √({}) = {} → valid".format(a*x+b, right))
                    final = "x = {}".format(x)
                else:
                    steps.append("Check: √({}) = {} ≠ {} → extraneous".format(a*x+b, left, right))
                    final = "No valid solution (extraneous)"
            else:
                steps.append("Domain error: {}x+{} or {}x+{} negative".format(a, b, c, d))
                final = "No valid solution"
    else:
        disc = B*B - 4*A*C
        steps.append("Quadratic discriminant: {}^2 - 4*{}*{} = {}".format(B, A, C, disc))
        if disc < 0:
            steps.append("No real solutions.")
            final = "No real solutions"
        else:
            sq = math.sqrt(disc)
            x1 = (-B + sq)/(2*A)
            x2 = (-B - sq)/(2*A)
            steps.append("Potential roots: x₁ = {}, x₂ = {}".format(x1, x2))
            sols = []
            for x in [x1, x2]:
                if a*x + b >= 0 and c*x + d >= 0:
                    left = math.sqrt(a*x + b)
                    right = c*x + d
                    if abs(left - right) < 1e-9:
                        sols.append(x)
                        steps.append("x = {} passes check (√{} = {})".format(x, a*x+b, right))
                    else:
                        steps.append("x = {} is extraneous (√{} ≠ {})".format(x, a*x+b, right))
                else:
                    steps.append("x = {} invalid due to domain".format(x))
            if sols:
                final = "Solutions: {}".format(sols)
            else:
                final = "No valid solutions after checking"
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Advanced Math", "9", "Absolute Value Equations")
def solve_absolute_value():
    UI.clear()
    print("Solve |ax + b| = c")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    steps = []
    steps.append("|{}x + {}| = {}".format(a, b, c))
    if a == 0:
        if c < 0:
            steps.append("No solution (absolute value cannot equal negative).")
            final = "No solution"
        elif c == 0:
            if b == 0:
                steps.append("|0| = 0 → all x are solutions.")
                final = "All real numbers"
            else:
                steps.append("|{}| ≠ 0 → no solution.".format(b))
                final = "No solution"
        else:
            if abs(b) == c:
                steps.append("|{}| = {} → all x are solutions.".format(b, c))
                final = "All real numbers"
            else:
                steps.append("|{}| ≠ {} → no solution.".format(b, c))
                final = "No solution"
    else:
        if c < 0:
            steps.append("No solution (absolute value cannot equal negative).")
            final = "No solution"
        elif c == 0:
            x = -b / a
            steps.append("Only when {}x + {} = 0 → x = {}".format(a, b, x))
            final = "x = {}".format(x)
        else:
            steps.append("Two cases:")
            x1 = (c - b) / a
            steps.append("Case 1: {}x + {} = {} → x = {}".format(a, b, c, x1))
            x2 = (-c - b) / a
            steps.append("Case 2: {}x + {} = -{} → x = {}".format(a, b, c, x2))
            final = "x = {}, x = {}".format(x1, x2)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

# ----------------------------------------------------------------------
# SOLVERS – PROBLEM SOLVING & DATA ANALYSIS
# ----------------------------------------------------------------------
@solver("Problem Solving", "1", "Ratios / Rates / Conversions")
def ratios_rates():
    UI.clear()
    print("Ratios / Rates / Unit Conversions")
    print("1. Solve proportion a/b = c/x")
    print("2. Unit rate (quantity per 1 unit)")
    print("3. Speed/distance/time")
    ch = input("Choice: ")
    if ch == "1":
        a = UI.get_float("a = ")
        b = UI.get_float("b = ")
        c = UI.get_float("c = ")
        steps = []
        steps.append("Proportion: {}/{} = {}/x".format(a, b, c))
        if b == 0:
            steps.append("Denominator b cannot be zero.")
            final = "Invalid"
        elif a == 0:
            steps.append("a cannot be zero (would imply infinite or no solution).")
            final = "Invalid"
        else:
            x = (c * b) / a
            steps.append("Cross multiply: {} * x = {} * {}".format(a, c, b))
            steps.append("x = {} * {} / {} = {}".format(c, b, a, x))
            final = "x = {}".format(x)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        total_qty = UI.get_float("Total quantity = ")
        total_units = UI.get_float("Total units = ")
        steps = []
        if total_units == 0:
            steps.append("Units cannot be zero.")
            final = "Invalid"
        else:
            rate = total_qty / total_units
            steps.append("Unit rate = {} / {} = {}".format(total_qty, total_units, rate))
            final = "{} per unit".format(rate)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        print("1. Find speed")
        print("2. Find distance")
        print("3. Find time")
        sub = input("Choice: ")
        if sub == "1":
            d = UI.get_float("Distance = ")
            t = UI.get_positive_float("Time = ")
            steps = []
            steps.append("Speed = Distance / Time")
            steps.append("Speed = {} / {} = {}".format(d, t, d/t))
            final = "Speed = {}".format(d/t)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "2":
            s = UI.get_float("Speed = ")
            t = UI.get_positive_float("Time = ")
            steps = []
            steps.append("Distance = Speed * Time")
            steps.append("Distance = {} * {} = {}".format(s, t, s*t))
            final = "Distance = {}".format(s*t)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "3":
            d = UI.get_float("Distance = ")
            s = UI.get_nonzero_float("Speed = ")
            steps = []
            steps.append("Time = Distance / Speed")
            steps.append("Time = {} / {} = {}".format(d, s, d/s))
            final = "Time = {}".format(d/s)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Problem Solving", "2", "Percent Problems")
def percent_problems():
    UI.clear()
    print("Percent Problems")
    print("1. Find % of a number")
    print("2. Percent increase/decrease")
    print("3. Discount / Tax / Tip")
    ch = input("Choice: ")
    if ch == "1":
        p = UI.get_float("Percent (%) = ")
        base = UI.get_float("Number = ")
        steps = []
        steps.append("{}% of {} = {} * {} / 100".format(p, base, base, p))
        result = base * p / 100
        steps.append("= {}".format(result))
        final = "{}% of {} = {}".format(p, base, result)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        original = UI.get_float("Original value = ")
        if original == 0:
            print("Original value cannot be zero (percent change undefined).")
            UI.wait()
            return
        new = UI.get_float("New value = ")
        steps = []
        steps.append("Original = {}, New = {}".format(original, new))
        change = new - original
        steps.append("Change = New - Original = {} - {} = {}".format(new, original, change))
        pct = (change / original) * 100
        steps.append("Percent change = ({} / {}) * 100 = {}%".format(change, original, pct))
        direction = "increase" if change > 0 else "decrease" if change < 0 else "no change"
        final = "{}% {}".format(pct, direction)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        print("1. Discount")
        print("2. Sales tax")
        print("3. Tip")
        sub = input("Choice: ")
        price = UI.get_float("Original price = ")
        rate = UI.get_float("Rate (%) = ")
        if sub == "1":
            steps = []
            steps.append("Discount = {} * {}% = {} * {}/100".format(price, rate, price, rate))
            discount = price * rate / 100
            steps.append("Discount = {}".format(discount))
            final_price = price - discount
            steps.append("Final price = {} - {} = {}".format(price, discount, final_price))
            final = "Discounted price = {}".format(final_price)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "2":
            steps = []
            steps.append("Tax = {} * {}% = {} * {}/100".format(price, rate, price, rate))
            tax = price * rate / 100
            steps.append("Tax = {}".format(tax))
            total = price + tax
            steps.append("Total = {} + {} = {}".format(price, tax, total))
            final = "Total with tax = {}".format(total)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "3":
            steps = []
            steps.append("Tip = {} * {}% = {} * {}/100".format(price, rate, price, rate))
            tip = price * rate / 100
            steps.append("Tip = {}".format(tip))
            final = "Tip amount = {}".format(tip)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Problem Solving", "3", "Probability")
def probability():
    UI.clear()
    print("Probability")
    print("1. Simple probability (favourable / total)")
    print("2. Compound (AND/OR with independent events)")
    ch = input("Choice: ")
    if ch == "1":
        fav = UI.get_int("Favourable outcomes = ")
        total = UI.get_int("Total outcomes = ")
        steps = []
        if total == 0:
            steps.append("Total cannot be zero.")
            final = "Invalid"
        else:
            p = fav / total
            steps.append("P = {} / {} = {}".format(fav, total, p))
            final = "P = {}".format(p)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        print("1. P(A and B) = P(A)*P(B) if independent")
        print("2. P(A or B) = P(A)+P(B)-P(A and B)")
        sub = input("Choice: ")
        pa = UI.get_float("P(A) = ")
        pb = UI.get_float("P(B) = ")
        if sub == "1":
            steps = []
            steps.append("P(A and B) = P(A) * P(B)")
            steps.append("= {} * {} = {}".format(pa, pb, pa*pb))
            final = "P(A and B) = {}".format(pa*pb)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "2":
            p_and = UI.get_float("P(A and B) = ")
            steps = []
            steps.append("P(A or B) = P(A) + P(B) - P(A and B)")
            steps.append("= {} + {} - {} = {}".format(pa, pb, p_and, pa + pb - p_and))
            final = "P(A or B) = {}".format(pa + pb - p_and)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Problem Solving", "4", "Linear vs Exponential Models")
def linear_vs_exponential():
    UI.clear()
    print("Determine if data is linear or exponential.")
    x1 = UI.get_float("x1 = ")
    y1 = UI.get_float("y1 = ")
    x2 = UI.get_float("x2 = ")
    y2 = UI.get_float("y2 = ")
    x3 = UI.get_float("x3 = ")
    y3 = UI.get_float("y3 = ")
    steps = []
    steps.append("Points: ({}, {}), ({}, {}), ({}, {})".format(x1, y1, x2, y2, x3, y3))
    slope1 = (y2-y1)/(x2-x1) if x2 != x1 else None
    slope2 = (y3-y2)/(x3-x2) if x3 != x2 else None
    if slope1 is not None and slope2 is not None:
        steps.append("Slope between first two: {}".format(slope1))
        steps.append("Slope between last two: {}".format(slope2))
        if abs(slope1 - slope2) < 1e-9:
            steps.append("Slopes are equal → linear.")
            final = "Linear (constant slope)"
        else:
            if y1 != 0 and y2 != 0 and y3 != 0:
                if abs((x2-x1) - (x3-x2)) < 1e-9:
                    ratio1 = y2/y1
                    ratio2 = y3/y2
                    steps.append("Ratios: {} and {}".format(ratio1, ratio2))
                    if abs(ratio1 - ratio2) < 1e-9:
                        steps.append("Ratios are equal → exponential.")
                        final = "Exponential (constant ratio)"
                    else:
                        final = "Neither clearly linear nor exponential"
                else:
                    steps.append("x‑values are not equally spaced; constant ratio does not guarantee exponential.")
                    final = "Inconclusive (x not equally spaced)"
            else:
                final = "Neither clearly linear nor exponential"
    else:
        steps.append("Could not compute slopes (vertical alignment).")
        final = "Insufficient data"
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Problem Solving", "5", "Descriptive Statistics")
def descriptive_stats():
    UI.clear()
    print("Enter numbers separated by spaces:")
    data_str = input("> ")
    try:
        nums = [float(x) for x in data_str.split()]
    except:
        print("Invalid numbers.")
        UI.wait()
        return
    if not nums:
        return
    n = len(nums)
    mean = sum(nums) / n
    sorted_nums = sorted(nums)
    median = median_of_list(nums)
    half = n // 2
    lower = sorted_nums[:half]
    upper = sorted_nums[-half:] if n % 2 == 0 else sorted_nums[half+1:]
    q1 = median_of_list(lower) if lower else None
    q3 = median_of_list(upper) if upper else None
    freq = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
    max_freq = max(freq.values())
    modes = [k for k, v in freq.items() if v == max_freq]
    mode_str = ", ".join(str(m) for m in modes) if max_freq > 1 else "no unique mode"
    range_val = max(nums) - min(nums)
    variance = sum((x-mean)**2 for x in nums) / (n-1) if n > 1 else 0
    std_dev = math.sqrt(variance)
    steps = []
    steps.append("Data: {}".format(nums))
    steps.append("n = {}".format(n))
    steps.append("Sum = {}".format(sum(nums)))
    steps.append("Mean = Sum / n = {} / {} = {}".format(sum(nums), n, mean))
    steps.append("Sorted: {}".format(sorted_nums))
    steps.append("Median = {}".format(median))
    if q1 is not None and q3 is not None:
        steps.append("Q1 = {}, Q3 = {}, IQR = {}".format(q1, q3, q3-q1))
    else:
        steps.append("Insufficient data for quartiles.")
    steps.append("Mode: {}".format(mode_str))
    steps.append("Range = {} - {} = {}".format(max(nums), min(nums), range_val))
    steps.append("Variance = {} (sample)".format(variance))
    steps.append("Std Dev = √{} = {}".format(variance, std_dev))
    final = "Mean: {}, Median: {}, Mode: {}, Std Dev: {}".format(mean, median, mode_str, std_dev)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Problem Solving", "6", "Data Visualization [guide]")
def guide_data_visualization():
    UI.clear()
    print("=" * 40)
    print("  DATA VISUALIZATION")
    print("=" * 40)
    print("""
SAT questions present data in:
- Scatterplots: look for trends, clusters,
  outliers, line of best fit.
- Histograms: show frequency of intervals.
- Box plots: show median, quartiles, range,
  and outliers.
- Line graphs: show change over time.

Example:
  "The scatterplot shows the relationship
  between hours studied and test score.
  A line of best fit is drawn. Which of
  the following is the best interpretation
  of the slope?"

The slope tells you the predicted increase
in test score for each additional hour studied.
So if the slope is 7, it means:
  "For each additional hour studied, the test
  score is predicted to increase by 7 points."

How to attack:
- Read the axes labels carefully.
- For scatterplots, identify the type of
  correlation (positive/negative/none).
- For histograms, estimate counts and
  compare bar heights.
- For box plots, know that the box spans
  Q1 to Q3, and the line inside is the median.

Practice: A box plot shows min=40, Q1=55,
median=70, Q3=85, max=100. What is the IQR?
IQR = Q3 - Q1 = 30. 50% of data lies within
the box.
""")
    UI.wait()

@solver("Problem Solving", "7", "Surveys & Experiments [guide]")
def guide_surveys_experiments():
    UI.clear()
    print("=" * 40)
    print("  SURVEYS & EXPERIMENTS")
    print("=" * 40)
    print("""
The SAT tests your ability to evaluate
statistical studies.

Key concepts:
- Random sample: every member of the
  population has an equal chance to be
  selected. Allows generalization.
- Bias: a systematic error that skews
  results (e.g., voluntary response,
  undercoverage).
- Margin of error: expresses the amount
  of random sampling error in a survey's
  results. A smaller margin of error
  requires a larger sample size.
- Experiment vs. observational study:
  experiments impose a treatment and can
  suggest causation; observational studies
  can only show association.

Example SAT question:
  "A researcher wants to estimate the
  average height of high school students
  in a city. She surveys the first 50
  students who arrive at school on Monday
  morning. What is the main flaw in this
  design?"

Flaw: The sample is a convenience sample,
not random. Students arriving early may
differ from the general population (e.g.,
more punctual, possibly different health
habits). Therefore, the results cannot be
reliably generalized to all high school
students in the city.

Another common topic: margin of error.
  A poll reports 52% support with a
  margin of error of +/-3%. This means
  the true percentage is likely between
  49% and 55%.

Always check:
- Is the sample random and representative?
- Is there a control group (in experiments)?
- Can we infer causation, or only association?
""")
    UI.wait()

# ----------------------------------------------------------------------
# SOLVERS – GEOMETRY & TRIGONOMETRY
# ----------------------------------------------------------------------
@solver("Geometry", "1", "Area")
def area_menu():
    UI.clear()
    print("Area Calculator")
    print("1. Rectangle")
    print("2. Square")
    print("3. Triangle")
    print("4. Parallelogram")
    print("5. Trapezoid")
    print("6. Circle")
    print("7. Sector")
    ch = input("Choice: ")
    if ch == "1":
        l = UI.get_float("length = ")
        w = UI.get_float("width = ")
        steps = []
        steps.append("Area = length * width = {} * {} = {}".format(l, w, l*w))
        final = "Area = {}".format(l*w)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        s = UI.get_float("side = ")
        steps = []
        steps.append("Area = side^2 = {}^2 = {}".format(s, s*s))
        final = "Area = {}".format(s*s)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        b = UI.get_float("base = ")
        h = UI.get_float("height = ")
        steps = []
        steps.append("Area = 1/2 * base * height = 0.5 * {} * {} = {}".format(b, h, 0.5*b*h))
        final = "Area = {}".format(0.5*b*h)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "4":
        b = UI.get_float("base = ")
        h = UI.get_float("height = ")
        steps = []
        steps.append("Area = base * height = {} * {} = {}".format(b, h, b*h))
        final = "Area = {}".format(b*h)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "5":
        b1 = UI.get_float("base1 = ")
        b2 = UI.get_float("base2 = ")
        h = UI.get_float("height = ")
        steps = []
        steps.append("Area = 1/2 * (base1 + base2) * height = 0.5 * ({} + {}) * {}".format(b1, b2, h))
        area = 0.5*(b1+b2)*h
        steps.append("= 0.5 * {} * {} = {}".format(b1+b2, h, area))
        final = "Area = {}".format(area)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "6":
        r = UI.get_positive_float("radius = ")
        steps = []
        steps.append("Area = π * r^2 = π * {}^2 = {}π".format(r, r*r))
        area = math.pi * r * r
        steps.append("≈ {}".format(area))
        final = "Area = {}".format(area)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "7":
        r = UI.get_positive_float("radius = ")
        th = UI.get_float("angle deg = ")
        steps = []
        steps.append("Sector area = (θ/360) * π * r^2")
        steps.append("= ({}/360) * π * {}^2".format(th, r))
        area = (th/360) * math.pi * r * r
        steps.append("≈ {}".format(area))
        final = "Sector area = {}".format(area)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Geometry", "2", "Volume")
def volume_menu():
    UI.clear()
    print("Volume Calculator")
    print("1. Prism")
    print("2. Cylinder")
    print("3. Cone")
    print("4. Sphere")
    print("5. Pyramid")
    ch = input("Choice: ")
    if ch == "1":
        B = UI.get_float("base area = ")
        h = UI.get_float("height = ")
        steps = []
        steps.append("Volume = base area * height = {} * {} = {}".format(B, h, B*h))
        final = "Volume = {}".format(B*h)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        r = UI.get_positive_float("radius = ")
        h = UI.get_float("height = ")
        steps = []
        steps.append("Volume = π * r^2 * h = π * {}^2 * {}".format(r, h))
        vol = math.pi * r * r * h
        steps.append("≈ {}".format(vol))
        final = "Volume = {}".format(vol)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        r = UI.get_positive_float("radius = ")
        h = UI.get_float("height = ")
        steps = []
        steps.append("Volume = 1/3 * π * r^2 * h = 1/3 * π * {}^2 * {}".format(r, h))
        vol = (1/3) * math.pi * r * r * h
        steps.append("≈ {}".format(vol))
        final = "Volume = {}".format(vol)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "4":
        r = UI.get_positive_float("radius = ")
        steps = []
        steps.append("Volume = 4/3 * π * r^3 = 4/3 * π * {}^3".format(r))
        vol = (4/3) * math.pi * r**3
        steps.append("≈ {}".format(vol))
        final = "Volume = {}".format(vol)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "5":
        B = UI.get_float("base area = ")
        h = UI.get_float("height = ")
        steps = []
        steps.append("Volume = 1/3 * base area * height = 1/3 * {} * {}".format(B, h))
        vol = (1/3) * B * h
        steps.append("= {}".format(vol))
        final = "Volume = {}".format(vol)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Geometry", "3", "Coordinate Geometry (distance, midpoint, slope)")
def coordinate_geometry():
    UI.clear()
    print("Coordinate Geometry: Distance, Midpoint, Slope, Line Eq")
    x1 = UI.get_float("x1 = ")
    y1 = UI.get_float("y1 = ")
    x2 = UI.get_float("x2 = ")
    y2 = UI.get_float("y2 = ")
    steps = []
    steps.append("Points: ({}, {}) and ({}, {})".format(x1, y1, x2, y2))
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    steps.append("Distance = √(({} - {})^2 + ({} - {})^2)".format(x2, x1, y2, y1))
    steps.append("= √({} + {}) = √{} = {}".format((x2-x1)**2, (y2-y1)**2, (x2-x1)**2 + (y2-y1)**2, dist))
    mid_x = (x1+x2)/2
    mid_y = (y1+y2)/2
    steps.append("Midpoint = (({}+{})/2, ({}+{})/2) = ({}, {})".format(x1, x2, y1, y2, mid_x, mid_y))
    if x2 - x1 == 0:
        slope = "undefined"
        eq = "x = {}".format(x1)
        steps.append("Slope: undefined (vertical line)")
        steps.append("Equation: x = {}".format(x1))
    else:
        slope = (y2 - y1) / (x2 - x1)
        b = y1 - slope * x1
        steps.append("Slope = ({} - {}) / ({} - {}) = {}".format(y2, y1, x2, x1, slope))
        steps.append("Equation: y = {}x + {}".format(slope, b))
        eq = "y = {}x + {}".format(slope, b)
    final = "Distance: {}, Midpoint: ({}, {}), Slope: {}, Eq: {}".format(dist, mid_x, mid_y, slope, eq)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Geometry", "4", "Lines & Angles")
def lines_and_angles():
    UI.clear()
    print("Lines & Angles")
    print("1. Vertical / Complementary / Supplementary angles")
    print("2. Parallel lines with transversal")
    ch = input("Choice: ")
    if ch == "1":
        a = UI.get_float("Given angle (degrees) = ")
        steps = []
        steps.append("Given angle: {}°".format(a))
        comp = 90 - a
        supp = 180 - a
        steps.append("Complement = 90 - {} = {}".format(a, comp))
        steps.append("Supplement = 180 - {} = {}".format(a, supp))
        steps.append("Vertical angle = {} (same)".format(a))
        final = "Complement: {}, Supplement: {}, Vertical: {}".format(comp, supp, a)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        a = UI.get_float("Angle (degrees) = ")
        steps = []
        steps.append("Given angle: {}°".format(a))
        steps.append("Corresponding angle = {}".format(a))
        steps.append("Alternate interior angle = {}".format(a))
        steps.append("Same-side interior angle = 180 - {} = {}".format(a, 180-a))
        final = "Corresponding: {}, Alternate interior: {}, Same-side interior: {}".format(a, a, 180-a)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Geometry", "5", "Triangles")
def triangles():
    UI.clear()
    print("Triangles")
    print("1. Angle sum (180)")
    print("2. Exterior angle theorem")
    print("3. Similarity scale factor")
    ch = input("Choice: ")
    if ch == "1":
        a1 = UI.get_float("Angle 1 = ")
        a2 = UI.get_float("Angle 2 = ")
        steps = []
        steps.append("Angle sum = 180°")
        a3 = 180 - a1 - a2
        steps.append("Angle 3 = 180 - {} - {} = {}".format(a1, a2, a3))
        final = "Third angle = {}".format(a3)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        r1 = UI.get_float("Remote interior 1 = ")
        r2 = UI.get_float("Remote interior 2 = ")
        steps = []
        steps.append("Exterior angle = Remote interior 1 + Remote interior 2")
        ext = r1 + r2
        steps.append("= {} + {} = {}".format(r1, r2, ext))
        final = "Exterior angle = {}".format(ext)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        a1 = UI.get_float("Side in triangle1 = ")
        a2 = UI.get_float("Corresponding side in triangle2 = ")
        steps = []
        if a1 != 0:
            scale = a2 / a1
            steps.append("Scale factor = {} / {} = {}".format(a2, a1, scale))
        else:
            scale = 0
            steps.append("Side1 is zero, scale factor undefined.")
        b1 = UI.get_float("Another side in triangle1 = ")
        b2 = b1 * scale
        steps.append("Corresponding side in triangle2 = {} * {} = {}".format(b1, scale, b2))
        final = "Scale factor: {}, Corresponding side: {}".format(scale, b2)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Geometry", "6", "Right Triangles")
def right_triangles():
    UI.clear()
    print("Right Triangles")
    print("1. Pythagorean Theorem (find missing side)")
    print("2. Special right triangles (30-60-90, 45-45-90)")
    ch = input("Choice: ")
    if ch == "1":
        print("1. Hypotenuse")
        print("2. Leg")
        sub = input("Choice: ")
        if sub == "1":
            a = UI.get_positive_float("Leg a = ")
            b = UI.get_positive_float("Leg b = ")
            steps = []
            steps.append("c² = a² + b² = {}² + {}² = {} + {} = {}".format(a, b, a*a, b*b, a*a+b*b))
            c = math.sqrt(a*a + b*b)
            steps.append("c = √{} = {}".format(a*a+b*b, c))
            final = "Hypotenuse c = {}".format(c)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "2":
            a = UI.get_positive_float("Known leg = ")
            c = UI.get_positive_float("Hypotenuse = ")
            if c <= a:
                print("Hypotenuse must be > leg.")
                UI.wait()
                return
            steps = []
            steps.append("b² = c² - a² = {}² - {}² = {} - {} = {}".format(c, a, c*c, a*a, c*c - a*a))
            b = math.sqrt(c*c - a*a)
            steps.append("b = √{} = {}".format(c*c - a*a, b))
            final = "Missing leg b = {}".format(b)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            print("Invalid choice.")
    elif ch == "2":
        print("1. 45-45-90")
        print("2. 30-60-90")
        sub = input("Choice: ")
        if sub == "1":
            leg = UI.get_positive_float("Leg length = ")
            steps = []
            steps.append("In 45-45-90 triangle, hypotenuse = leg * √2")
            hyp = leg * math.sqrt(2)
            steps.append("Hypotenuse = {} * √2 = {}".format(leg, hyp))
            final = "Hypotenuse = {}".format(hyp)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "2":
            x = UI.get_positive_float("Short leg = ")
            steps = []
            steps.append("30-60-90 triangle: hypotenuse = 2*short leg, long leg = short leg * √3")
            hyp = 2*x
            long_leg = x * math.sqrt(3)
            steps.append("Hypotenuse = 2 * {} = {}".format(x, hyp))
            steps.append("Long leg = {} * √3 = {}".format(x, long_leg))
            final = "Hypotenuse: {}, Long leg: {}".format(hyp, long_leg)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Geometry", "7", "Trigonometry (SOH-CAH-TOA)")
def trigonometry():
    UI.clear()
    print("Trigonometry (Right Triangle)")
    print("1. Find missing side (angle and side known)")
    print("2. Find missing angle (two sides known)")
    ch = input("Choice: ")
    if ch == "1":
        print("Known: 1) hypotenuse, 2) leg")
        side_known = input("Which side is known? (hyp/leg): ").strip().lower()
        if side_known == "hyp":
            hyp = UI.get_positive_float("Hypotenuse = ")
            angle = UI.get_float("Angle (degrees) = ")
            steps = []
            steps.append("Angle = {}°, hypotenuse = {}".format(angle, hyp))
            rad = math.radians(angle)
            opp = hyp * math.sin(rad)
            adj = hyp * math.cos(rad)
            steps.append("sin({}) = opp/hyp → opp = {} * sin({}) = {}".format(angle, hyp, angle, opp))
            steps.append("cos({}) = adj/hyp → adj = {} * cos({}) = {}".format(angle, hyp, angle, adj))
            final = "Opposite: {}, Adjacent: {}".format(opp, adj)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif side_known == "leg":
            leg = UI.get_positive_float("Leg length = ")
            angle = UI.get_float("Adjacent angle? (0-90) = ")
            if angle <= 0 or angle >= 90:
                print("Angle must be strictly between 0 and 90 degrees (cos !=0).")
                UI.wait()
                return
            steps = []
            steps.append("Adjacent angle = {}, adjacent leg = {}".format(angle, leg))
            rad = math.radians(angle)
            hyp = leg / math.cos(rad)
            opp = hyp * math.sin(rad)
            steps.append("cos({}) = adj/hyp → hyp = {} / cos({}) = {}".format(angle, leg, angle, hyp))
            steps.append("sin({}) = opp/hyp → opp = {} * sin({}) = {}".format(angle, hyp, angle, opp))
            final = "Hypotenuse: {}, Opposite: {}".format(hyp, opp)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            print("Invalid side specified.")
    elif ch == "2":
        opp = UI.get_positive_float("Opposite = ")
        adj = UI.get_positive_float("Adjacent = ")
        steps = []
        steps.append("tan(θ) = opp/adj = {} / {}".format(opp, adj))
        angle = math.degrees(math.atan(opp/adj))
        steps.append("θ = arctan({}/{}) = {}°".format(opp, adj, angle))
        hyp = math.sqrt(opp**2 + adj**2)
        steps.append("Also sin⁻¹(opp/hyp) = sin⁻¹({}/{}) = {}°".format(opp, hyp, math.degrees(math.asin(opp/hyp))))
        final = "Angle = {}°".format(angle)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Geometry", "8", "Circles (arc, sector, equation)")
def circles():
    UI.clear()
    print("Circles")
    print("1. Circumference & Area")
    print("2. Arc length & Sector area")
    print("3. Equation of circle (center-radius)")
    ch = input("Choice: ")
    if ch == "1":
        r = UI.get_positive_float("Radius = ")
        steps = []
        steps.append("Circumference = 2πr = 2π*{} = {}π ≈ {}".format(r, 2*r, 2*math.pi*r))
        area = math.pi * r * r
        steps.append("Area = πr² = π*{}² = {}π ≈ {}".format(r, r*r, area))
        final = "Circumference: {}, Area: {}".format(2*math.pi*r, area)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        r = UI.get_positive_float("Radius = ")
        th = UI.get_float("Central angle (degrees) = ")
        steps = []
        steps.append("Arc length = (θ/360) * 2πr = ({}/360) * 2π*{}".format(th, r))
        arc = (th/360) * 2 * math.pi * r
        steps.append("= {}π ≈ {}".format((th/360)*2*r, arc))
        sector = (th/360) * math.pi * r * r
        steps.append("Sector area = (θ/360) * πr² = ({}/360) * π*{}² = {}π ≈ {}".format(th, r, (th/360)*r*r, sector))
        final = "Arc length: {}, Sector area: {}".format(arc, sector)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        h = UI.get_float("h = ")
        k = UI.get_float("k = ")
        r = UI.get_positive_float("r = ")
        steps = []
        steps.append("Center: ({}, {}), radius: {}".format(h, k, r))
        steps.append("Equation: (x - {})² + (y - {})² = {}²".format(h, k, r))
        steps.append("Expanded: x² + y² - {}x - {}y + {} = 0".format(2*h, 2*k, h*h + k*k - r*r))
        final = "Equation: (x - {})² + (y - {})² = {}".format(h, k, r*r)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

# ----------------------------------------------------------------------
# SOLVERS – ADDITIONAL TOPICS
# ----------------------------------------------------------------------
@solver("Additional Topics", "1", "Logarithms & Exponential Equations")
def sub_menu_log_exp():
    UI.clear()
    print("1. Logarithm evaluation/solving")
    print("2. Exponential equations")
    ch = input("Choice: ")
    if ch == "1":
        logarithms()
    elif ch == "2":
        exponential_equations()
    else:
        print("Invalid choice.")
        UI.wait()

def logarithms():
    UI.clear()
    print("LOGARITHMS")
    print("1. Evaluate log_b(x)")
    print("2. Solve log_b(ax+c) = d")
    ch = input("Choice: ")
    if ch == "1":
        b = UI.get_float("base b = ")
        x = UI.get_positive_float("x = ")
        steps = []
        try:
            res = log_base(x, b)
            steps.append("log_{}({}) = log({}) / log({})".format(b, x, x, b))
            steps.append("= {} / {} = {}".format(math.log(x), math.log(b), res))
            final = "log_{}({}) = {}".format(b, x, res)
        except ValueError as e:
            steps.append("Error: {}".format(e))
            final = "Invalid"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        b = UI.get_float("base b = ")
        a = UI.get_float("a = ")
        c = UI.get_float("c = ")
        d = UI.get_float("d = ")
        steps = []
        try:
            if b <= 0 or b == 1:
                steps.append("Base must be positive and not equal to 1.")
                final = "Invalid"
            else:
                rhs = b ** d
                steps.append("log_{}({}x + {}) = {} → {}x + {} = {}".format(b, a, c, d, a, c, rhs))
                if a == 0:
                    steps.append("a = 0 → cannot solve.")
                    final = "Invalid"
                else:
                    x = (rhs - c) / a
                    steps.append("x = ({} - {}) / {} = {}".format(rhs, c, a, x))
                    if a*x + c <= 0:
                        steps.append("Argument <= 0 → no solution.")
                        final = "No solution"
                    else:
                        final = "x = {}".format(x)
        except Exception as e:
            steps.append("Error: {}".format(e))
            final = "Error"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

def exponential_equations():
    UI.clear()
    print("EXPONENTIAL EQUATIONS")
    print("Solve b^(ax+c) = d")
    b = UI.get_positive_float("base b = ")
    a = UI.get_float("a = ")
    c = UI.get_float("c = ")
    d = UI.get_positive_float("d = ")
    steps = []
    if b == 1:
        steps.append("Base = 1 → trivial.")
        final = "Trivial (1 = d)"
    else:
        if a == 0:
            lhs = b ** c
            steps.append("Constant: {} = {}".format(b, c, lhs))
            if abs(lhs - d) < 1e-12:
                steps.append("Identity → all x are solutions.")
                final = "All x"
            else:
                steps.append("No solution.")
                final = "No solution"
        else:
            try:
                log_val = log_base(d, b)
                steps.append("log_{}({}) = {}x + {}".format(b, d, a, c))
                steps.append("{} = {}x + {}".format(log_val, a, c))
                x = (log_val - c) / a
                steps.append("x = ({} - {}) / {} = {}".format(log_val, c, a, x))
                final = "x = {}".format(x)
            except ValueError as e:
                steps.append("Error: {}".format(e))
                final = "Error"
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Additional Topics", "2", "Sequences & Series")
def sequences_series():
    UI.clear()
    print("SEQUENCES & SERIES")
    print("1. Arithmetic: nth term & sum")
    print("2. Geometric: nth term & sum (finite/infinite)")
    ch = input("Choice: ")
    if ch == "1":
        a1 = UI.get_float("first term a1 = ")
        d = UI.get_float("common difference d = ")
        n = UI.get_int("n = ")
        steps = []
        steps.append("Arithmetic: a1 = {}, d = {}".format(a1, d))
        an = a1 + (n-1)*d
        steps.append("a_{} = {} + ({} - 1)*{} = {}".format(n, a1, n, d, an))
        Sn = n/2 * (a1 + an)
        steps.append("S_{} = {}/2 * ({} + {}) = {}".format(n, n, a1, an, Sn))
        final = "a_{} = {}, S_{} = {}".format(n, an, n, Sn)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        a1 = UI.get_float("first term a1 = ")
        r = UI.get_float("common ratio r = ")
        n = UI.get_int("n = ")
        steps = []
        steps.append("Geometric: a1 = {}, r = {}".format(a1, r))
        an = a1 * (r ** (n-1))
        steps.append("a_{} = {} * {}^{} = {}".format(n, a1, r, n-1, an))
        if r == 1:
            Sn = a1 * n
            steps.append("S_{} = a1 * n = {} * {} = {}".format(n, a1, n, Sn))
        else:
            Sn = a1 * (1 - r**n) / (1 - r)
            steps.append("S_{} = {} * (1 - {}^{}) / (1 - {}) = {}".format(n, a1, r, n, r, Sn))
        final = "a_{} = {}, S_{} = {}".format(n, an, n, Sn)
        if abs(r) < 1:
            S_inf = a1 / (1 - r)
            steps.append("Infinite sum S∞ = a1 / (1 - r) = {} / {} = {}".format(a1, 1-r, S_inf))
            final += ", Infinite sum = {}".format(S_inf)
        else:
            steps.append("|r| >= 1 → no infinite sum.")
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Additional Topics", "3", "Complex Numbers")
def complex_numbers():
    UI.clear()
    print("COMPLEX NUMBERS (a+bi)")
    print("1. Add / Subtract")
    print("2. Multiply")
    print("3. Divide")
    print("4. Modulus & Conjugate")
    ch = input("Choice: ")
    a1 = UI.get_float("a1 = ")
    b1 = UI.get_float("b1 = ")
    if ch != "4":
        a2 = UI.get_float("a2 = ")
        b2 = UI.get_float("b2 = ")
    if ch == "1":
        s = input("Add (+) or Subtract (-): ")
        if s == "+":
            real = a1 + a2
            imag = b1 + b2
            steps = []
            steps.append("({} + {}i) + ({} + {}i) = ({} + {}) + ({} + {})i".format(a1, b1, a2, b2, a1, a2, b1, b2))
            steps.append("= {} + {}i".format(real, imag))
            final = "Result: {} + {}i".format(real, imag)
        else:
            real = a1 - a2
            imag = b1 - b2
            steps = []
            steps.append("({} + {}i) - ({} + {}i) = ({} - {}) + ({} - {})i".format(a1, b1, a2, b2, a1, a2, b1, b2))
            steps.append("= {} + {}i".format(real, imag))
            final = "Result: {} + {}i".format(real, imag)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        real = a1*a2 - b1*b2
        imag = a1*b2 + a2*b1
        steps = []
        steps.append("({} + {}i) * ({} + {}i)".format(a1, b1, a2, b2))
        steps.append("= ({}) + ({})i + ({})i + ({} i²)".format(a1*a2, a1*b2, a2*b1, b1*b2))
        steps.append("= ({} - {}) + ({} + {})i".format(a1*a2, b1*b2, a1*b2, a2*b1))
        steps.append("= {} + {}i".format(real, imag))
        final = "Product: {} + {}i".format(real, imag)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        denom = a2**2 + b2**2
        if denom == 0:
            print("Cannot divide by zero.")
            UI.wait()
            return
        real = (a1*a2 + b1*b2) / denom
        imag = (a2*b1 - a1*b2) / denom
        steps = []
        steps.append("({} + {}i) / ({} + {}i)".format(a1, b1, a2, b2))
        steps.append("Multiply numerator and denominator by conjugate ({} - {}i)".format(a2, b2))
        steps.append("Denominator = {}² + {}² = {}".format(a2, b2, denom))
        steps.append("Numerator = ({}) + ({})i".format(a1*a2 + b1*b2, a2*b1 - a1*b2))
        steps.append("= ({} + {}i) / {}".format(a1*a2 + b1*b2, a2*b1 - a1*b2, denom))
        steps.append("= {} + {}i".format(real, imag))
        final = "Quotient: {} + {}i".format(real, imag)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "4":
        mod = math.sqrt(a1**2 + b1**2)
        steps = []
        steps.append("Modulus = √({}² + {}²) = √{} = {}".format(a1, b1, a1**2 + b1**2, mod))
        steps.append("Conjugate = {} - {}i".format(a1, b1))
        final = "Modulus: {}, Conjugate: {} - {}i".format(mod, a1, b1)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Additional Topics", "4", "Counting & Probability (advanced)")
def combinatorics():
    UI.clear()
    print("COUNTING & PROBABILITY")
    print("1. Factorial n!")
    print("2. Permutations nPr")
    print("3. Combinations nCr")
    ch = input("Choice: ")
    if ch == "1":
        n = UI.get_int("n = ")
        if n < 0:
            print("Invalid.")
            UI.wait()
            return
        fact = 1
        for i in range(2, n+1):
            fact *= i
        steps = []
        steps.append("{}! = ".format(n))
        if n == 0:
            steps.append("0! = 1 (by definition)")
        else:
            steps.append("{}! = {} = {}".format(n, " * ".join(str(i) for i in range(2, n+1)), fact))
        final = "{}! = {}".format(n, fact)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        n = UI.get_int("n = ")
        r = UI.get_int("r = ")
        if r < 0 or r > n:
            print("Invalid.")
            UI.wait()
            return
        perm = 1
        for i in range(n, n-r, -1):
            perm *= i
        steps = []
        steps.append("nPr = {}! / ({}!) = {} * ... * {}".format(n, n-r, n, n-r+1))
        steps.append("= {}".format(perm))
        final = "{}P{} = {}".format(n, r, perm)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        n = UI.get_int("n = ")
        r = UI.get_int("r = ")
        if r < 0 or r > n:
            print("Invalid.")
            UI.wait()
            return
        comb = 1
        for i in range(1, r+1):
            comb = comb * (n - i + 1) // i
        steps = []
        steps.append("nCr = n! / (r! (n-r)!)")
        steps.append("= {}C{} = {}".format(n, r, comb))
        final = "{}C{} = {}".format(n, r, comb)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Additional Topics", "5", "Binomial Theorem")
def binomial_theorem():
    UI.clear()
    print("BINOMIAL THEOREM")
    print("Find specific term in (a+b)^n")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    n = UI.get_int("n = ")
    k = UI.get_int("k (0-indexed term number) = ")
    if k < 0 or k > n:
        print("Invalid k.")
        UI.wait()
        return
    comb = 1
    for i in range(1, k+1):
        comb = comb * (n - i + 1) // i
    coeff = comb * (a ** (n-k)) * (b ** k)
    steps = []
    steps.append("Term T_{} = C(n,{}) * a^{{{}}} * b^{{{}}}".format(k+1, k, n-k, k))
    steps.append("C({},{}) = {}".format(n, k, comb))
    steps.append("a^{} = {}, b^{} = {}".format(n-k, a**(n-k), k, b**k))
    steps.append("T_{} = {} * {} * {} = {}".format(k+1, comb, a**(n-k), b**k, coeff))
    final = "Term T_{} = {}".format(k+1, coeff)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Additional Topics", "6", "Matrices & Vectors")
def sub_menu_mat_vec():
    UI.clear()
    print("1. Matrices")
    print("2. Vectors")
    ch = input("Choice: ")
    if ch == "1":
        matrices()
    elif ch == "2":
        vectors()
    else:
        print("Invalid choice.")
        UI.wait()

def matrices():
    UI.clear()
    print("MATRICES (2x2)")
    print("1. Determinant")
    print("2. Inverse")
    print("3. Solve system using matrices")
    ch = input("Choice: ")
    if ch == "1":
        a11 = UI.get_float("a11 = ")
        a12 = UI.get_float("a12 = ")
        a21 = UI.get_float("a21 = ")
        a22 = UI.get_float("a22 = ")
        steps = []
        steps.append("Matrix: [[{}, {}], [{}, {}]]".format(a11, a12, a21, a22))
        det = a11*a22 - a12*a21
        steps.append("det = {}*{} - {}*{} = {}".format(a11, a22, a12, a21, det))
        final = "Determinant = {}".format(det)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        a11 = UI.get_float("a11 = ")
        a12 = UI.get_float("a12 = ")
        a21 = UI.get_float("a21 = ")
        a22 = UI.get_float("a22 = ")
        det = a11*a22 - a12*a21
        if det == 0:
            print("No inverse (det=0).")
            UI.wait()
            return
        steps = []
        steps.append("Matrix A = [[{}, {}], [{}, {}]]".format(a11, a12, a21, a22))
        steps.append("det = {}".format(det))
        steps.append("Inverse = 1/{} * [[{}, -{}], [-{}, {}]]".format(det, a22, a12, a21, a11))
        inv11 = a22/det
        inv12 = -a12/det
        inv21 = -a21/det
        inv22 = a11/det
        steps.append("= [[{}, {}], [{}, {}]]".format(inv11, inv12, inv21, inv22))
        final = "Inverse: [[{}, {}], [{}, {}]]".format(inv11, inv12, inv21, inv22)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        a11 = UI.get_float("a11 = ")
        a12 = UI.get_float("a12 = ")
        b1 = UI.get_float("b1 = ")
        a21 = UI.get_float("a21 = ")
        a22 = UI.get_float("a22 = ")
        b2 = UI.get_float("b2 = ")
        det = a11*a22 - a12*a21
        if det == 0:
            print("No unique solution.")
            UI.wait()
            return
        x = (b1*a22 - b2*a12) / det
        y = (a11*b2 - a21*b1) / det
        steps = []
        steps.append("Matrix form: [[{}, {}], [{}, {}]] [x,y]^T = [{}, {}]^T".format(a11, a12, a21, a22, b1, b2))
        steps.append("det = {}".format(det))
        steps.append("x = ({}*{} - {}*{}) / {} = {}".format(b1, a22, b2, a12, det, x))
        steps.append("y = ({}*{} - {}*{}) / {} = {}".format(a11, b2, a21, b1, det, y))
        final = "Solution: x = {}, y = {}".format(x, y)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

def vectors():
    UI.clear()
    print("VECTORS")
    print("1. Magnitude")
    print("2. Dot product")
    print("3. Angle between")
    ch = input("Choice: ")
    x1 = UI.get_float("x1 = ")
    y1 = UI.get_float("y1 = ")
    if ch == "1":
        mag = math.sqrt(x1**2 + y1**2)
        steps = []
        steps.append("|v| = √({}² + {}²) = √{} = {}".format(x1, y1, x1**2 + y1**2, mag))
        final = "Magnitude = {}".format(mag)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        x2 = UI.get_float("x2 = ")
        y2 = UI.get_float("y2 = ")
        if ch == "2":
            dot = x1*x2 + y1*y2
            steps = []
            steps.append("v1 · v2 = {}*{} + {}*{} = {} + {} = {}".format(x1, x2, y1, y2, x1*x2, y1*y2, dot))
            final = "Dot product = {}".format(dot)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif ch == "3":
            dot = x1*x2 + y1*y2
            mag1 = math.sqrt(x1**2 + y1**2)
            mag2 = math.sqrt(x2**2 + y2**2)
            if mag1 == 0 or mag2 == 0:
                print("Zero vector, angle undefined.")
                UI.wait()
                return
            cos_theta = dot / (mag1 * mag2)
            if cos_theta > 1: cos_theta = 1
            if cos_theta < -1: cos_theta = -1
            theta = math.degrees(math.acos(cos_theta))
            steps = []
            steps.append("cos θ = (v1·v2) / (|v1||v2|)")
            steps.append("= {} / ({} * {}) = {}".format(dot, mag1, mag2, cos_theta))
            steps.append("θ = arccos({}) = {}°".format(cos_theta, theta))
            final = "Angle = {}°".format(theta)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            print("Invalid choice.")
    UI.wait()

@solver("Additional Topics", "7", "Law of Sines / Cosines")
def law_of_sines_cosines():
    UI.clear()
    print("LAW OF SINES / COSINES")
    print("1. Law of Sines (AAS/ASA)")
    print("2. Law of Cosines (SAS/SSS)")
    ch = input("Choice: ")
    if ch == "1":
        A = UI.get_float("angle A (deg) = ")
        B = UI.get_float("angle B (deg) = ")
        a = UI.get_float("side a opposite A = ")
        try:
            b = a * math.sin(math.radians(B)) / math.sin(math.radians(A))
            steps = []
            steps.append("Law of Sines: a/sin(A) = b/sin(B)")
            steps.append("{} / sin({}) = b / sin({})".format(a, A, B))
            steps.append("b = {} * sin({}) / sin({})".format(a, B, A))
            steps.append("b = {} * {} / {} = {}".format(a, math.sin(math.radians(B)), math.sin(math.radians(A)), b))
            final = "Side b = {}".format(b)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        except ZeroDivisionError:
            print("sin(A) cannot be zero (angle 0 or 180).")
    elif ch == "2":
        print("Which case?")
        print("1. SAS (two sides and included angle)")
        print("2. SSS (three sides to find angle)")
        sub = input("Choice: ")
        if sub == "1":
            a = UI.get_float("side a = ")
            b = UI.get_float("side b = ")
            C = UI.get_float("included angle C (deg) = ")
            steps = []
            steps.append("Law of Cosines: c² = a² + b² - 2ab cos(C)")
            steps.append("c² = {}² + {}² - 2*{}*{}*cos({})".format(a, b, a, b, C))
            c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(C)))
            steps.append("= {} + {} - {} = {}".format(a**2, b**2, 2*a*b*math.cos(math.radians(C)), c**2))
            steps.append("c = √{} = {}".format(c**2, c))
            final = "Side c = {}".format(c)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        elif sub == "2":
            a = UI.get_positive_float("side a = ")
            b = UI.get_positive_float("side b = ")
            c = UI.get_positive_float("side c = ")
            try:
                cosA = (b**2 + c**2 - a**2) / (2*b*c)
                if cosA > 1 or cosA < -1:
                    print("Invalid triangle sides.")
                    UI.wait()
                    return
                A = math.degrees(math.acos(cosA))
                steps = []
                steps.append("cos(A) = (b² + c² - a²) / (2bc)")
                steps.append("= ({}² + {}² - {}²) / (2*{}*{}) = {}".format(b, c, a, b, c, cosA))
                steps.append("A = arccos({}) = {}°".format(cosA, A))
                final = "Angle A = {}°".format(A)
                for i, s in enumerate(steps, 1):
                    print("Step {}: {}".format(i, s))
                print("\n" + "─" * 40)
                print("Final answer: {}".format(final))
            except ZeroDivisionError:
                print("Side lengths cannot be zero.")
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Additional Topics", "8", "Heron's Formula")
def herons_formula():
    UI.clear()
    print("HERON'S FORMULA (Triangle area given 3 sides)")
    a = UI.get_float("side a = ")
    b = UI.get_float("side b = ")
    c = UI.get_float("side c = ")
    steps = []
    if a + b > c and a + c > b and b + c > a:
        s = (a + b + c) / 2
        steps.append("Semi-perimeter s = ({}+{}+{})/2 = {}".format(a, b, c, s))
        steps.append("s-a = {}, s-b = {}, s-c = {}".format(s-a, s-b, s-c))
        try:
            area = math.sqrt(s * (s-a) * (s-b) * (s-c))
            steps.append("Area = √( {} * {} * {} * {} )".format(s, s-a, s-b, s-c))
            steps.append("= √{} = {}".format(s*(s-a)*(s-b)*(s-c), area))
            final = "Area = {}".format(area)
        except ValueError:
            steps.append("Invalid input caused negative under sqrt.")
            final = "Error"
    else:
        steps.append("Sides do not form a valid triangle.")
        final = "Invalid"
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Additional Topics", "9", "3D Distance")
def three_d_distance():
    UI.clear()
    print("3D DISTANCE")
    x1 = UI.get_float("x1 = ")
    y1 = UI.get_float("y1 = ")
    z1 = UI.get_float("z1 = ")
    x2 = UI.get_float("x2 = ")
    y2 = UI.get_float("y2 = ")
    z2 = UI.get_float("z2 = ")
    steps = []
    steps.append("Points: ({}, {}, {}) and ({}, {}, {})".format(x1, y1, z1, x2, y2, z2))
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    steps.append("d = √(({} - {})² + ({} - {})² + ({} - {})²)".format(x2, x1, y2, y1, z2, z1))
    steps.append("= √({} + {} + {})".format((x2-x1)**2, (y2-y1)**2, (z2-z1)**2))
    steps.append("= √{} = {}".format((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2, dist))
    final = "Distance = {}".format(dist)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Additional Topics", "10", "Quadratic Inequality")
def quadratic_inequality():
    UI.clear()
    print("QUADRATIC INEQUALITY (ax^2+bx+c > 0, etc.)")
    a = UI.get_nonzero_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    op = input("Operator (<, >, <=, >=): ").strip()
    steps = []
    steps.append("Solve {}x² + {}x + {} {} 0".format(a, b, c, op))
    disc = b*b - 4*a*c
    steps.append("Discriminant D = {}² - 4*{}*{} = {}".format(b, a, c, disc))
    if disc < 0:
        steps.append("No real roots (discriminant < 0).")
        if a > 0:
            truth = True if op in [">", ">="] else False
            steps.append("a > 0 → parabola opens up, expression always positive.")
        else:
            truth = True if op in ["<", "<="] else False
            steps.append("a < 0 → parabola opens down, expression always negative.")
        final = "All real x" if truth else "No solution"
    elif disc == 0:
        root = -b/(2*a)
        steps.append("Double root at x = {}".format(root))
        if a > 0:
            if op == ">":
                steps.append("a > 0 → expression > 0 except at root.")
                final = "x ≠ {}".format(root)
            elif op == ">=":
                steps.append("a > 0 → expression >= 0 everywhere.")
                final = "All real x"
            elif op == "<":
                steps.append("a > 0 → expression never negative.")
                final = "No solution"
            else:  # <=
                steps.append("a > 0 → expression <= 0 only at root.")
                final = "x = {}".format(root)
        else:  # a < 0
            if op == "<":
                steps.append("a < 0 → expression < 0 except at root.")
                final = "x ≠ {}".format(root)
            elif op == "<=":
                steps.append("a < 0 → expression <= 0 everywhere.")
                final = "All real x"
            elif op == ">":
                steps.append("a < 0 → expression never positive.")
                final = "No solution"
            else:  # >=
                steps.append("a < 0 → expression >= 0 only at root.")
                final = "x = {}".format(root)
    else:
        sq = math.sqrt(disc)
        r1 = (-b - sq)/(2*a)
        r2 = (-b + sq)/(2*a)
        if r1 > r2:
            r1, r2 = r2, r1
        steps.append("Roots: {} and {}".format(r1, r2))
        if a > 0:
            if op == ">":
                steps.append("a > 0 → solution outside interval.")
                final = "x < {} or x > {}".format(r1, r2)
            elif op == ">=":
                steps.append("a > 0 → solution outside interval (including endpoints).")
                final = "x ≤ {} or x ≥ {}".format(r1, r2)
            elif op == "<":
                steps.append("a > 0 → solution inside interval.")
                final = "{} < x < {}".format(r1, r2)
            else:  # <=
                steps.append("a > 0 → solution inside interval (including endpoints).")
                final = "{} ≤ x ≤ {}".format(r1, r2)
        else:
            if op == ">":
                steps.append("a < 0 → solution inside interval.")
                final = "{} < x < {}".format(r1, r2)
            elif op == ">=":
                steps.append("a < 0 → solution inside interval (including endpoints).")
                final = "{} ≤ x ≤ {}".format(r1, r2)
            elif op == "<":
                steps.append("a < 0 → solution outside interval.")
                final = "x < {} or x > {}".format(r1, r2)
            else:  # <=
                steps.append("a < 0 → solution outside interval (including endpoints).")
                final = "x ≤ {} or x ≥ {}".format(r1, r2)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Additional Topics", "11", "Absolute Value Inequality")
def absolute_value_inequality():
    UI.clear()
    print("ABSOLUTE VALUE INEQUALITY: |ax+b| < c  (or >, <=, >=)")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    op = input("Operator (<, >, <=, >=): ").strip()
    steps = []
    steps.append("|{}x + {}| {} {}".format(a, b, op, c))
    if a == 0:
        abs_b = abs(b)
        steps.append("Constant |{}| = {}".format(b, abs_b))
        if op == "<":
            result = abs_b < c
            final = "All real x" if result else "No solution"
        elif op == "<=":
            result = abs_b <= c
            final = "All real x" if result else "No solution"
        elif op == ">":
            result = abs_b > c
            final = "All real x" if result else "No solution"
        elif op == ">=":
            result = abs_b >= c
            final = "All real x" if result else "No solution"
        steps.append("Condition {} → {}".format(op, final))
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
        UI.wait()
        return
    if c < 0:
        if op in [">", ">="]:
            final = "All real x (absolute always >= 0 > negative)"
        else:
            final = "No solution (absolute cannot be < negative)"
        steps.append("c < 0 → special case.")
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif c == 0:
        if op in ["<", "<="]:
            x = -b/a
            steps.append("|{}x+{}| <= 0 → only when = 0 → x = {}".format(a, b, x))
            final = "x = {}".format(x)
        else:
            x = -b/a
            if op == ">":
                steps.append("|{}x+{}| > 0 → all x except {}".format(a, b, x))
                final = "x ≠ {}".format(x)
            else:
                steps.append("|{}x+{}| >= 0 → all real x".format(a, b))
                final = "All real x"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        if op in ["<", "<="]:
            low = (-c - b)/a
            high = (c - b)/a
            if a < 0:
                low, high = high, low
            steps.append("Case {}: -{} < {}x+{} < {}".format(op, c, a, b, c))
            if op == "<":
                final = "{} < x < {}".format(low, high)
            else:
                final = "{} ≤ x ≤ {}".format(low, high)
        else:
            left = (-c - b)/a
            right = (c - b)/a
            if a < 0:
                left, right = right, left
            steps.append("Case {}: {}x+{} < -{} or {}x+{} > {}".format(op, a, b, c, a, b, c))
            if op == ">":
                final = "x < {} or x > {}".format(left, right)
            else:
                final = "x ≤ {} or x ≥ {}".format(left, right)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    UI.wait()

@solver("Additional Topics", "12", "Radian/Degree Converter")
def radian_degree():
    UI.clear()
    print("RADIAN <-> DEGREE CONVERTER")
    print("1. Radians to Degrees")
    print("2. Degrees to Radians")
    ch = input("Choice: ")
    if ch == "1":
        rad = UI.get_float("radians = ")
        steps = []
        steps.append("Degrees = radians * 180 / π")
        deg = rad * 180 / math.pi
        steps.append("= {} * 180 / π = {}".format(rad, deg))
        final = "{} rad = {}°".format(rad, deg)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        deg = UI.get_float("degrees = ")
        steps = []
        steps.append("Radians = degrees * π / 180")
        rad = deg * math.pi / 180
        steps.append("= {} * π / 180 = {}".format(deg, rad))
        final = "{}° = {} rad".format(deg, rad)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Additional Topics", "13", "Polynomial Long Division")
def polynomial_long_division():
    UI.clear()
    print("POLYNOMIAL LONG DIVISION (linear divisor only)")
    print("Divide polynomial P(x) by (x - c) using synthetic division.")
    c = UI.get_float("c (divisor x-c): ")
    print("Enter coefficients of P(x) from highest degree to constant, separated by spaces:")
    coeff_str = input("> ")
    try:
        coeff = [float(x) for x in coeff_str.split()]
    except:
        print("Invalid coefficients.")
        UI.wait()
        return
    if len(coeff) < 2:
        print("Need at least 2 coefficients.")
        UI.wait()
        return
    result = [coeff[0]]
    for i in range(1, len(coeff)-1):
        val = result[-1] * c + coeff[i]
        result.append(val)
    remainder = result[-1] * c + coeff[-1]
    steps = []
    steps.append("Synthetic division with c = {}".format(c))
    steps.append("Bring down {}:".format(coeff[0]))
    for i in range(1, len(coeff)-1):
        steps.append("Multiply {} by {} → {}, add to {} → {}".format(result[-1], c, result[-1]*c, coeff[i], result[-1]*c + coeff[i]))
    steps.append("Remainder: {}".format(remainder))
    deg = len(result) - 1
    poly_str = ""
    for i, coef in enumerate(result):
        power = deg - i
        if abs(coef) < 1e-12:
            continue
        if power == 0:
            poly_str += "{:+.4f}".format(coef)
        elif power == 1:
            poly_str += "{:+.4f}x".format(coef)
        else:
            poly_str += "{:+.4f}x^{}".format(coef, power)
    if poly_str.startswith("+"):
        poly_str = poly_str[1:]
    if not poly_str:
        poly_str = "0"
    steps.append("Quotient: {}".format(poly_str))
    final = "Quotient: {}, Remainder: {}".format(poly_str, remainder)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Additional Topics", "14", "Remainder Theorem")
def remainder_theorem():
    UI.clear()
    print("REMAINDER THEOREM")
    print("Evaluates P(c) using synthetic substitution.")
    c = UI.get_float("c = ")
    coeff_str = input("Enter polynomial coefficients (high to low) separated by spaces: ")
    try:
        coeff = [float(x) for x in coeff_str.split()]
    except:
        print("Invalid.")
        UI.wait()
        return
    val = coeff[0]
    steps = []
    steps.append("Synthetic substitution with c = {}".format(c))
    steps.append("Start with {}".format(coeff[0]))
    for i in range(1, len(coeff)):
        old = val
        val = val * c + coeff[i]
        steps.append("Multiply {} by {} → {}, add {} → {}".format(old, c, old*c, coeff[i], val))
    final = "P({}) = {}".format(c, val)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Additional Topics", "15", "Completing the Square")
def completing_square():
    UI.clear()
    print("COMPLETING THE SQUARE: x^2 + bx + c = (x + p)^2 + q")
    b = UI.get_float("b (coefficient of x) = ")
    c = UI.get_float("c (constant) = ")
    steps = []
    steps.append("x² + {}x + {}".format(b, c))
    p = b / 2
    q = c - p**2
    steps.append("p = b/2 = {}".format(p))
    steps.append("q = c - p² = {} - ({})² = {}".format(c, p, q))
    steps.append("Completed square: (x + {})² + {}".format(p, q))
    final = "(x + {})² + {}".format(p, q)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

# ----------------------------------------------------------------------
# FUNCTION GUIDES (grouped under Additional Topics)
# ----------------------------------------------------------------------
@solver("Additional Topics", "16", "Function Guides (transforms, inverse, etc.)")
def function_guides_menu():
    UI.clear()
    print("1. Function Transformations")
    print("2. Inverse Functions")
    print("3. Piecewise Functions")
    ch = input("Choice: ")
    if ch == "1":
        guide_function_transformations()
    elif ch == "2":
        guide_inverse_functions()
    elif ch == "3":
        guide_piecewise_functions()
    else:
        print("Invalid choice.")
        UI.wait()

def guide_function_transformations():
    UI.clear()
    print("FUNCTION TRANSFORMATIONS")
    print("========================")
    print("""
Given parent function f(x), transformations:
- f(x)+k : vertical shift up k (down if -)
- f(x+k) : horizontal shift left k (right if -)
- -f(x)  : reflection over x-axis
- f(-x)  : reflection over y-axis
- a*f(x) : vertical stretch if |a|>1, compress if 0<|a|<1
- f(b*x): horizontal stretch if 0<|b|<1, compress if |b|>1

Example: g(x) = 2*(x-3)^2 + 1
Parent: f(x)=x^2.
Transformations: right 3, vertical stretch x2, up 1.
Vertex moves from (0,0) to (3,1), parabola narrower.
""")
    UI.wait()

def guide_inverse_functions():
    UI.clear()
    print("INVERSE FUNCTIONS")
    print("================")
    print("""
Inverse f^-1(x) "undoes" f(x).
- To find: replace f(x) with y, swap x and y, solve for y.
- Graph is reflection over line y=x.
- Domain of f is range of f^-1 and vice versa.

Example: f(x) = (2x+1)/3
Swap: x = (2y+1)/3 -> 3x = 2y+1 -> y = (3x-1)/2
Thus f^-1(x) = (3x-1)/2
""")
    UI.wait()

def guide_piecewise_functions():
    UI.clear()
    print("PIECEWISE FUNCTIONS")
    print("===================")
    print("""
A function defined by different formulas over different
intervals. Evaluate by checking which condition x satisfies.

Example: f(x) = { x^2   for x < 2
                { 3x-1  for x >= 2
Find f(1): 1<2 -> f(1)=1^2=1
Find f(3): 3>=2 -> f(3)=3*3-1=8
""")
    UI.wait()

@solver("Additional Topics", "17", "Advanced Word Problems (work, mixture, distance)")
def word_problem_guides_menu():
    UI.clear()
    print("1. Work / Rate Problems")
    print("2. Mixture Problems")
    print("3. Advanced Distance/Rate/Time")
    ch = input("Choice: ")
    if ch == "1":
        guide_work_rate_problems()
    elif ch == "2":
        guide_mixture_problems()
    elif ch == "3":
        guide_distance_rate_time_advanced()
    else:
        print("Invalid choice.")
        UI.wait()

def guide_work_rate_problems():
    UI.clear()
    print("WORK / RATE PROBLEMS")
    print("====================")
    print("""
Combine rates: 1/time1 + 1/time2 = 1/total_time

Example: Alice can paint a house in 6 hours, Bob in 4 hours.
How long together?
1/6 + 1/4 = 1/t
(2/12 + 3/12) = 5/12 = 1/t -> t = 12/5 = 2.4 hours.
""")
    UI.wait()

def guide_mixture_problems():
    UI.clear()
    print("MIXTURE PROBLEMS")
    print("================")
    print("""
Set up a system: amount and concentration.

Example: Mix 30% acid with 10% acid to get 50L of 22% acid.
Let x = volume of 30%, y = volume of 10%.
x + y = 50
0.30x + 0.10y = 0.22(50)=11
Solve -> x=30, y=20.
""")
    UI.wait()

def guide_distance_rate_time_advanced():
    UI.clear()
    print("DISTANCE/RATE/TIME (ADVANCED)")
    print("============================")
    print("""
Two objects moving toward each other: combined speed.
Two objects moving apart: sum of speeds.
Circular tracks: relative speed for catching up.

Example: Two trains 200 miles apart start toward each other,
one at 60 mph, other at 40 mph. When do they meet?
Combined speed = 100 mph, time = 200/100 = 2 hours.
""")
    UI.wait()

@solver("Additional Topics", "18", "Geometry Guides (circle theorems, unit circle)")
def geometry_guides_menu():
    UI.clear()
    print("1. Circle Theorems")
    print("2. Unit Circle & Exact Values")
    ch = input("Choice: ")
    if ch == "1":
        guide_circle_theorems()
    elif ch == "2":
        guide_unit_circle()
    else:
        print("Invalid choice.")
        UI.wait()

def guide_circle_theorems():
    UI.clear()
    print("CIRCLE THEOREMS")
    print("===============")
    print("""
- Inscribed angle = half the measure of its intercepted arc.
- Central angle = arc measure.
- Angle in a semicircle is a right angle.
- Tangent is perpendicular to radius at point of tangency.
- Intersecting chords: product of segments are equal.
""")
    UI.wait()

def guide_unit_circle():
    UI.clear()
    print("UNIT CIRCLE & EXACT VALUES")
    print("==========================")
    print("""
Common angles (degrees -> radians):
0:0, 30:pi/6, 45:pi/4, 60:pi/3, 90:pi/2
sin/cos values:
30 deg: sin=1/2, cos=sqrt3/2
45 deg: sin=sqrt2/2, cos=sqrt2/2
60 deg: sin=sqrt3/2, cos=1/2
""")
    UI.wait()

@solver("Additional Topics", "19", "Conic Sections Guide")
def guide_conic_sections():
    UI.clear()
    print("CONIC SECTIONS (Parabola, Circle, Ellipse, Hyperbola)")
    print("====================================================")
    print("""
SAT primarily tests circle and parabola. Know:
Circle: (x-h)^2+(y-k)^2=r^2
Parabola: y=ax^2+bx+c, vertex at x=-b/(2a)
Ellipse: x^2/a^2 + y^2/b^2 = 1 (horizontal if a>b)
Hyperbola: x^2/a^2 - y^2/b^2 = 1 (opens left/right)
Questions may ask to identify the shape from an equation.
""")
    UI.wait()

@solver("Additional Topics", "20", "Even/Odd, Domain/Range, Composition")
def misc_function_guides_menu():
    UI.clear()
    print("1. Even & Odd Functions")
    print("2. Domain & Range")
    print("3. Function Composition")
    ch = input("Choice: ")
    if ch == "1":
        guide_even_odd_functions()
    elif ch == "2":
        guide_domain_range()
    elif ch == "3":
        guide_function_composition()
    else:
        print("Invalid choice.")
        UI.wait()

def guide_even_odd_functions():
    UI.clear()
    print("EVEN & ODD FUNCTIONS")
    print("====================")
    print("""
Even: f(-x)=f(x) (symmetric about y-axis, e.g., x^2)
Odd: f(-x)=-f(x) (symmetric about origin, e.g., x^3)
Test by substituting -x.
""")
    UI.wait()

def guide_domain_range():
    UI.clear()
    print("DOMAIN & RANGE")
    print("==============")
    print("""
Domain: all possible x-values.
Look for: denominator not zero, inside sqrt >=0, inside log >0.
Range: possible y-values.
For quadratic: vertex's y is max/min if a<0/a>0.
""")
    UI.wait()

def guide_function_composition():
    UI.clear()
    print("FUNCTION COMPOSITION")
    print("====================")
    print("""
(f o g)(x) = f(g(x)). Evaluate inner function first.
Example: f(x)=2x, g(x)=x+3 -> f(g(4)) = f(7)=14.
""")
    UI.wait()

# ----------------------------------------------------------------------
# FORMULA REFERENCE
# ----------------------------------------------------------------------
FORMULA_REFERENCE = {
    "Slope": {
        "formula": "m = (y2 - y1) / (x2 - x1)",
        "vars": "m: slope, (x1,y1) and (x2,y2): two points",
        "use": "Find slope of a line through two points.",
        "example": "(1,2) and (3,6) -> m = (6-2)/(3-1) = 4/2 = 2"
    },
    "Slope-Intercept Form": {
        "formula": "y = mx + b",
        "vars": "m: slope, b: y-intercept",
        "use": "Equation of a line.",
        "example": "m=2, b=3 -> y = 2x + 3"
    },
    "Point-Slope Form": {
        "formula": "y - y1 = m(x - x1)",
        "vars": "m: slope, (x1,y1): point on line",
        "use": "Line equation given slope and a point.",
        "example": "m=3, point (2,1) -> y - 1 = 3(x - 2)"
    },
    "Distance Formula": {
        "formula": "d = sqrt((x2-x1)^2 + (y2-y1)^2)",
        "vars": "(x1,y1), (x2,y2): two points",
        "use": "Distance between two points.",
        "example": "(0,0) and (3,4) -> d = sqrt(9+16) = 5"
    },
    "Midpoint": {
        "formula": "M = ((x1+x2)/2, (y1+y2)/2)",
        "vars": "Midpoint coordinates.",
        "use": "Find midpoint of a segment.",
        "example": "(2,3) and (4,7) -> M = (3,5)"
    },
    "Quadratic Formula": {
        "formula": "x = (-b +/- sqrt(b^2 - 4ac)) / (2a)",
        "vars": "a, b, c coefficients of ax^2+bx+c=0",
        "use": "Solve any quadratic equation.",
        "example": "x^2-5x+6=0 -> a=1,b=-5,c=6 -> disc=1 -> x=3 or 2"
    },
    "Discriminant": {
        "formula": "D = b^2 - 4ac",
        "vars": "D < 0: no real solutions; D = 0: one real; D > 0: two real",
        "use": "Determines number of real solutions of a quadratic.",
        "example": "x^2+1=0 -> D=-4 -> no real solutions"
    },
    "Pythagorean Theorem": {
        "formula": "a^2 + b^2 = c^2",
        "vars": "a, b: legs; c: hypotenuse",
        "use": "Right triangle side calculations.",
        "example": "a=3, b=4 -> c^2=25 -> c=5"
    },
    "Area of Circle": {
        "formula": "A = pi * r^2",
        "vars": "r: radius",
        "use": "Area of a circle.",
        "example": "r=5 -> A=25pi ~ 78.54"
    },
    "Circumference": {
        "formula": "C = 2 * pi * r",
        "vars": "r: radius",
        "use": "Circumference of a circle.",
        "example": "r=7 -> C=14pi ~ 43.98"
    },
    "Volume of Sphere": {
        "formula": "V = (4/3) * pi * r^3",
        "vars": "r: radius",
        "use": "Volume of a sphere.",
        "example": "r=3 -> V=36pi ~ 113.1"
    },
    "SOH-CAH-TOA": {
        "formula": "sin = opp/hyp, cos = adj/hyp, tan = opp/adj",
        "vars": "opposite, adjacent, hypotenuse sides relative to angle",
        "use": "Right triangle trigonometry.",
        "example": "sin(30 deg)=0.5"
    },
    "Arc Length": {
        "formula": "L = (theta/360) * 2 * pi * r   (theta in degrees)",
        "vars": "theta: central angle, r: radius",
        "use": "Length of an arc.",
        "example": "theta=90 deg, r=4 -> L = (90/360)*8pi = 2pi ~ 6.28"
    },
    "Sector Area": {
        "formula": "A = (theta/360) * pi * r^2",
        "vars": "theta: central angle, r: radius",
        "use": "Area of a sector.",
        "example": "theta=60 deg, r=6 -> A = (60/360)*36pi = 6pi ~ 18.85"
    },
    "Compound Interest": {
        "formula": "A = P(1 + r/n)^(nt)",
        "vars": "P: principal, r: annual rate, n: times per year, t: years",
        "use": "Value of an investment with compound interest.",
        "example": "P=1000, r=0.05, n=12, t=10 -> A ~ 1647.01"
    },
    "Exponential Growth/Decay": {
        "formula": "y = a * b^x   (b>1 growth, 0<b<1 decay)",
        "vars": "a: initial amount, b: growth/decay factor",
        "use": "Model exponential change.",
        "example": "y = 100 * 2^x -> doubles each step"
    },
}

@solver("Formula Reference", "1", "Browse Formulas")
def formula_reference():
    while True:
        UI.clear()
        print("SAT Formula Reference")
        formulas = list(FORMULA_REFERENCE.keys())
        for i, name in enumerate(formulas, 1):
            print("{}. {}".format(i, name))
        print("{}. Return".format(len(formulas)+1))
        try:
            ch = int(input("Choice: "))
            if 1 <= ch <= len(formulas):
                name = formulas[ch-1]
                f = FORMULA_REFERENCE[name]
                UI.clear()
                print("--- {} ---".format(name))
                print("Formula: {}".format(f['formula']))
                print("Variables: {}".format(f['vars']))
                print("When to use: {}".format(f['use']))
                print("Example: {}".format(f['example']))
                UI.wait()
            elif ch == len(formulas)+1:
                break
            else:
                print("Invalid choice.")
                UI.wait()
        except:
            print("Invalid input.")
            UI.wait()

# ----------------------------------------------------------------------
# UTILITIES
# ----------------------------------------------------------------------
@solver("Utilities", "1", "Fraction <-> Decimal")
def frac_decimal():
    UI.clear()
    print("1. Fraction -> Decimal")
    print("2. Decimal -> Fraction (approx)")
    ch = input("Choice: ")
    if ch == "1":
        num = UI.get_float("Numerator = ")
        den = UI.get_nonzero_float("Denominator = ")
        steps = []
        steps.append("Decimal = {} / {} = {}".format(num, den, num/den))
        final = "{}".format(num/den)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        dec = UI.get_float("Decimal = ")
        best_num, best_den = 1, 1
        best_err = abs(dec - 1)
        for den in range(1, 10001):
            num = round(dec * den)
            err = abs(dec - num/den)
            if err < best_err:
                best_err = err
                best_num, best_den = num, den
                if err == 0:
                    break
        g = gcd(best_num, best_den)
        steps = []
        steps.append("Searching for fraction approximation of {}".format(dec))
        steps.append("Best match: {}/{} ≈ {}".format(best_num, best_den, best_num/best_den))
        steps.append("Simplified: {}/{}".format(best_num//g, best_den//g))
        final = "{}/{}".format(best_num//g, best_den//g)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Utilities", "2", "Decimal <-> Percent")
def dec_percent():
    UI.clear()
    print("1. Decimal -> Percent")
    print("2. Percent -> Decimal")
    ch = input("Choice: ")
    if ch == "1":
        d = UI.get_float("Decimal = ")
        steps = []
        steps.append("{} * 100 = {}%".format(d, d*100))
        final = "{}%".format(d*100)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        p = UI.get_float("Percent = ")
        steps = []
        steps.append("{} / 100 = {}".format(p, p/100))
        final = "{}".format(p/100)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Utilities", "3", "Fraction Simplifier")
def simplify_fraction():
    UI.clear()
    num = UI.get_int("Numerator = ")
    den = UI.get_int("Denominator (non-zero) = ")
    if den == 0:
        print("Denominator cannot be zero.")
        UI.wait()
        return
    g = gcd(num, den)
    steps = []
    steps.append("GCF({}, {}) = {}".format(num, den, g))
    steps.append("{}/{} = {}/{}".format(num, den, num//g, den//g))
    final = "{}/{}".format(num//g, den//g)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Utilities", "4", "GCF")
def gcf():
    UI.clear()
    a = UI.get_int("First number: ")
    b = UI.get_int("Second number: ")
    g = gcd(a, b)
    steps = []
    steps.append("Euclidean algorithm: gcd({}, {})".format(a, b))
    steps.append("Result: {}".format(g))
    final = "GCF = {}".format(g)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Utilities", "5", "LCM")
def lcm():
    UI.clear()
    a = UI.get_int("First number: ")
    b = UI.get_int("Second number: ")
    g = gcd(a, b)
    l = abs(a*b)//g if g != 0 else 0
    steps = []
    steps.append("LCM = (|{}*{}|) / gcd({}, {})".format(a, b, a, b))
    steps.append("= {} / {} = {}".format(abs(a*b), g, l))
    final = "LCM = {}".format(l)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Utilities", "6", "Prime Factorization")
def prime_factorization():
    UI.clear()
    n = UI.get_int("Enter integer (>1): ")
    if n < 2:
        print("Must be >1.")
        UI.wait()
        return
    steps = []
    temp = n
    d = 2
    factors = []
    while d*d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    steps.append("Prime factorization of {}".format(n))
    steps.append(" = " + " × ".join(str(f) for f in factors))
    final = "{} = {}".format(n, " × ".join(str(f) for f in factors))
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Utilities", "7", "Scientific Notation Converter")
def scientific_notation():
    UI.clear()
    print("1. Standard to Scientific")
    print("2. Scientific to Standard")
    ch = input("Choice: ")
    if ch == "1":
        num = UI.get_float("Number = ")
        if num == 0:
            steps = []
            steps.append("0 = 0 × 10^0")
            final = "0 × 10^0"
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            exp = int(math.floor(math.log10(abs(num))))
            mantissa = num / (10**exp)
            steps = []
            steps.append("{} = {} × 10^{}".format(num, mantissa, exp))
            final = "{} × 10^{}".format(mantissa, exp)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
    elif ch == "2":
        mantissa = UI.get_float("Mantissa = ")
        exponent = UI.get_int("Exponent = ")
        result = mantissa * (10**exponent)
        steps = []
        steps.append("{} × 10^{} = {}".format(mantissa, exponent, result))
        final = "{}".format(result)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

@solver("Utilities", "8", "Quadratic Formula Calculator")
def quad_formula_calc():
    UI.clear()
    print("Quadratic Formula: ax^2 + bx + c = 0")
    a = UI.get_nonzero_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    steps = []
    steps.append("Equation: {}x² + {}x + {} = 0".format(a, b, c))
    disc = b*b - 4*a*c
    steps.append("Discriminant D = {}² - 4*{}*{} = {}".format(b, a, c, disc))
    if disc < 0:
        steps.append("No real roots.")
        final = "No real roots"
    else:
        sq = math.sqrt(disc)
        x1 = (-b + sq)/(2*a)
        x2 = (-b - sq)/(2*a)
        steps.append("x₁ = ({} + √{}) / {} = {}".format(-b, disc, 2*a, x1))
        steps.append("x₂ = ({} - √{}) / {} = {}".format(-b, disc, 2*a, x2))
        final = "x₁ = {}, x₂ = {}".format(x1, x2)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Utilities", "9", "Distance / Midpoint / Slope Calculators")
def coord_utils():
    UI.clear()
    print("Coordinate Utilities")
    print("1. Distance")
    print("2. Midpoint")
    print("3. Slope")
    ch = input("Choice: ")
    x1 = UI.get_float("x1 = ")
    y1 = UI.get_float("y1 = ")
    x2 = UI.get_float("x2 = ")
    y2 = UI.get_float("y2 = ")
    if ch == "1":
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        steps = []
        steps.append("Distance = √(({} - {})² + ({} - {})²)".format(x2, x1, y2, y1))
        steps.append("= √({} + {}) = √{} = {}".format((x2-x1)**2, (y2-y1)**2, (x2-x1)**2 + (y2-y1)**2, dist))
        final = "Distance = {}".format(dist)
    elif ch == "2":
        mid_x = (x1+x2)/2
        mid_y = (y1+y2)/2
        steps = []
        steps.append("Midpoint = (({} + {})/2, ({} + {})/2) = ({}, {})".format(x1, x2, y1, y2, mid_x, mid_y))
        final = "Midpoint = ({}, {})".format(mid_x, mid_y)
    elif ch == "3":
        if x2-x1 == 0:
            steps = []
            steps.append("Slope undefined (vertical line)")
            final = "Undefined"
        else:
            slope = (y2-y1)/(x2-x1)
            steps = []
            steps.append("Slope = ({} - {}) / ({} - {}) = {}".format(y2, y1, x2, x1, slope))
            final = "Slope = {}".format(slope)
    else:
        print("Invalid choice.")
        UI.wait()
        return
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()

@solver("Utilities", "10", "Pythagorean Calculator")
def pythagorean_calc():
    UI.clear()
    print("Pythagorean Theorem: a^2 + b^2 = c^2")
    print("1. Find hypotenuse (c)")
    print("2. Find leg (a or b)")
    ch = input("Choice: ")
    if ch == "1":
        a = UI.get_positive_float("a = ")
        b = UI.get_positive_float("b = ")
        steps = []
        steps.append("c² = {}² + {}² = {} + {} = {}".format(a, b, a*a, b*b, a*a+b*b))
        c = math.sqrt(a*a + b*b)
        steps.append("c = √{} = {}".format(a*a+b*b, c))
        final = "Hypotenuse c = {}".format(c)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        leg = UI.get_positive_float("Known leg = ")
        hyp = UI.get_positive_float("Hypotenuse = ")
        if hyp <= leg:
            print("Hypotenuse must be larger.")
            UI.wait()
            return
        steps = []
        steps.append("b² = c² - a² = {}² - {}² = {} - {} = {}".format(hyp, leg, hyp*hyp, leg*leg, hyp*hyp - leg*leg))
        b = math.sqrt(hyp*hyp - leg*leg)
        steps.append("b = √{} = {}".format(hyp*hyp - leg*leg, b))
        final = "Missing leg = {}".format(b)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()

# ----------------------------------------------------------------------
# ABOUT
# ----------------------------------------------------------------------
@solver("About", "1", "About this Program")
def about():
    UI.clear()
    print("="*30)
    print("  SAT Math Solver")
    print("="*30)
    print("Covers EVERY Digital SAT Math topic.")
    print("")
    print("Features:")
    print("- Step-by-step solvers")
    print("- Built-in formula reference")
    print("- Text guides for conceptual topics")
    print("- 60+ solvers & utilities")
    print("- Searchable solver index with interactive selection")
    print("")
    print("Version: 1.3")
    print("License: GPL 3.0")
    print("Author: cheeseburgerjr")
    print("")
    print("Made for students, by a student.")
    UI.wait()

# ----------------------------------------------------------------------
# MAIN MENU ENGINE
# ----------------------------------------------------------------------
def main_menu():
    while True:
        UI.clear()
        print("="*30)
        print("      SAT Math Solver")
        print("="*30)
        categories = SolverRegistry.get_categories()
        for idx, cat in enumerate(categories, 1):
            print("{}. {}".format(idx, cat))
        print("{}. Exit".format(len(categories)+1))
        print("S. Search solvers by keyword")
        choice = input("Enter choice: ").strip()
        if choice.lower() == "s":
            search_solver()
            continue
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(categories):
                cat = categories[choice_num - 1]
                while True:
                    UI.clear()
                    print("--- {} ---".format(cat))
                    solvers = SolverRegistry.get_solvers(cat)
                    items = sorted(solvers.items(), key=lambda kv: int(kv[0]))
                    for key, (name, _) in items:
                        print("{}. {}".format(key, name))
                    print("0. Return to main menu")
                    sub_choice = input("Choice: ")
                    if sub_choice == "0":
                        break
                    elif sub_choice in solvers:
                        SolverRegistry.run_solver(cat, sub_choice)
                    else:
                        print("Invalid choice.")
                        UI.wait()
            elif choice_num == len(categories) + 1:
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
                UI.wait()
        except ValueError:
            print("Invalid input.")
            UI.wait()

if __name__ == "__main__":
    main_menu()
