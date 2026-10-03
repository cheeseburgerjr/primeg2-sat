"""
SAT Math Solver for HP Prime G2 (MicroPython)
Copyright (C) 2026 (cheeseburgerjr)
License: GPLv3
Covers all Digital SAT Math topics.
"""

import math


def is_finite_number(x):
    try:
        return math.isfinite(x)
    except AttributeError:
        try:
            return not (math.isnan(x) or math.isinf(x))
        except Exception:
            return True


def _insert_pi_multiplication(s):
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isdigit():
            out.append(c)
            i += 1
            j = i
            while j < n and s[j] == ' ':
                j += 1
            if j + 1 < n and s[j:j+2] == 'pi':
                out.append('*')
                i = j
            continue
        if i + 1 < n and s[i:i+2] == 'pi':
            out.append('pi')
            i += 2
            j = i
            while j < n and s[j] == ' ':
                j += 1
            if j < n and s[j].isdigit():
                out.append('*')
                i = j
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def parse_number(s):
    s = s.strip()
    if not s:
        raise ValueError("empty input")

    s = s.replace('π', 'pi')

    if 'pi' in s.lower():
        s = s.lower()
        s = _insert_pi_multiplication(s)
        s = s.replace('pi', str(math.pi))
        if not all(c in '0123456789.*/+- ()' for c in s):
            raise ValueError("invalid pi expression")
        try:
            val = eval(s)
        except Exception:
            raise ValueError("invalid pi expression")
        if not is_finite_number(val):
            raise ValueError("non-finite value")
        return val

    if ' ' in s:
        parts = s.split()
        if len(parts) == 2:
            try:
                whole = float(parts[0])
            except Exception:
                whole = None
            if whole is not None:
                try:
                    frac = parse_number(parts[1])
                except Exception:
                    frac = None
                if frac is not None:
                    if frac < 0:
                        raise ValueError("negative fractional part in mixed number is not allowed")
                    if whole < 0:
                        return whole - frac
                    return whole + frac

    if '/' in s:
        parts = s.split('/')
        if len(parts) == 2:
            try:
                num = float(parts[0])
                den = float(parts[1])
            except Exception:
                raise ValueError("invalid fraction")
            if den == 0:
                raise ValueError("division by zero")
            return num / den

    val = float(s)
    if not is_finite_number(val):
        raise ValueError("non-finite value")
    return val


def log_base(x, base):
    if base <= 0 or base == 1:
        raise ValueError("Log base must be positive and not equal to 1.")
    if x <= 0:
        raise ValueError("Log argument must be positive.")
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


def is_approx_zero(x, eps=1e-9):
    return abs(x) < eps


SEARCH_INDEX = {
    "linear equation": ("Heart of Algebra", "1", "Linear Equations (one variable): solves ax + b = cx + d with step‑by‑step", "linear equation, one variable, solve for x"),
    "slope": ("Heart of Algebra", "2", "Slope / Intercepts: finds slope and intercepts from points or y = mx + b", "slope, intercept, gradient, y-intercept, x-intercept, line"),
    "system": ("Heart of Algebra", "3", "Systems of Linear Equations: solves two equations using Cramer's rule", "system, simultaneous, cramer, 2x2"),
    "inequality": ("Heart of Algebra", "4", "Linear Inequalities (one variable): solves ax + b < c (or >, <=, >=)", "inequality, linear, one variable, solve"),
    "system inequality": ("Heart of Algebra", "5", "System of Linear Inequalities Checker: check if a point satisfies multiple inequalities", "system of inequalities, point, check, shaded region"),
    "function": ("Heart of Algebra", "6", "Linear Functions: evaluate f(x) or find x from f(x) = y", "linear function, evaluate, find x"),
    "parallel": ("Heart of Algebra", "7", "Parallel & Perpendicular Lines: find slope of parallel/perpendicular line and equation", "parallel, perpendicular, slope, line, through point"),
    "translation": ("Heart of Algebra", "8", "Line Translation & X-Intercept: finds new x-intercept after translating a line", "translation, shift, x-intercept, line, translate"),
    "word problem": ("Heart of Algebra", "9", "Linear Word Problems: translate word problems to linear equations and solve", "word problem, linear, translate, solve"),
    "simplify": ("Advanced Math", "1", "Equivalent Expressions: expand (ax+b)(cx+d) or factor x^2+px+q", "expand, factor, equivalent, simplify"),
    "quadratic": ("Advanced Math", "2", "Quadratic Equations: solves ax² + bx + c = 0 using the quadratic formula", "quadratic, formula, roots, solve, parabola"),
    "parabola": ("Advanced Math", "3", "Parabolas: finds vertex, axis, intercepts and direction", "parabola, vertex, axis, intercepts, direction, opens"),
    "nonlinear": ("Advanced Math", "4", "System of Line & Parabola/Circle: finds intersections of curves", "nonlinear, system, line, parabola, circle, intersection"),
    "exponential": ("Advanced Math", "5", "Exponential Functions: growth/decay, compound interest, half‑life", "exponential, growth, decay, compound interest, half-life, doubling"),
    "polynomial": ("Advanced Math", "6", "Polynomial Functions (roots): finds roots of quadratics or integer roots of cubics", "polynomial, roots, cubic, quadratic"),
    "rational": ("Advanced Math", "7", "Rational Functions: finds vertical and horizontal asymptotes", "rational, asymptote, vertical, horizontal, domain"),
    "radical": ("Advanced Math", "8", "Radical Equations: solves √(ax + b) = cx + d with domain checks", "radical, square root, equation, domain, extraneous"),
    "absolute value": ("Advanced Math", "9", "Absolute Value Equations: solves |ax + b| = c with both cases", "absolute value, equation, cases"),
    "quadratic inequality": ("Advanced Math", "10", "Quadratic Inequality: solves ax²+bx+c > 0 (or <, <=, >=)", "quadratic inequality, inequality, parabola"),
    "absolute inequality": ("Advanced Math", "11", "Absolute Value Inequality: solves |ax+b| < c (or >, <=, >=)", "absolute value inequality, inequality, absolute"),
    "long division": ("Advanced Math", "12", "Polynomial Long Division: divides polynomial by (x - c)", "long division, polynomial, divide, synthetic"),
    "remainder": ("Advanced Math", "13", "Remainder Theorem: evaluates P(c) using synthetic substitution", "remainder theorem, polynomial, evaluate, synthetic"),
    "completing square": ("Advanced Math", "14", "Completing the Square: rewrites x²+bx+c as (x+p)²+q", "completing square, vertex, quadratic"),
    "transformations": ("Advanced Math", "15", "Function Transformations: from parent function and shifts/stretches", "transformations, shift, stretch, reflect, function"),
    "inverse": ("Advanced Math", "16", "Inverse Function (linear): computes f⁻¹(x) for f(x)=mx+b", "inverse, linear function, find inverse"),
    "piecewise": ("Advanced Math", "17", "Piecewise Function Evaluator: evaluates piecewise functions at a point", "piecewise, evaluate, condition, expression"),
    "even odd": ("Advanced Math", "18", "Even/Odd Functions: determines if a function is even, odd, or neither", "even, odd, symmetry, function"),
    "domain range": ("Advanced Math", "19", "Domain & Range Finder: finds domain and range of functions", "domain, range, function, interval"),
    "composition": ("Advanced Math", "20", "Function Composition: evaluates (f∘g)(x) given f(x) and g(x)", "composition, composite, f(g(x))"),
    "rational equation": ("Advanced Math", "21", "Rational Equations: solves (ax+b)/(cx+d)=k", "rational equation, solve, denominator"),
    "parameter": ("Advanced Math", "22", "Parameter Condition Solver: finds constants for infinite/no solutions", "parameter, infinite solutions, no solution, condition, constants"),
    "exponential equation": ("Advanced Math", "23", "Exponential Equations: solves b^(ax+c)=d", "exponential, equation, solve"),
    "logarithm": ("Advanced Math", "24", "Logarithmic Equations: solves log_b(ax+c)=d", "log, logarithm, log base"),
    "ratio": ("Problem Solving", "1", "Ratios & Proportions: solves a/b = c/x", "ratio, proportion, solve"),
    "unit rate": ("Problem Solving", "2", "Unit Rates: quantity per 1 unit", "unit rate, per unit"),
    "speed": ("Problem Solving", "3", "Speed/Distance/Time: solve for any variable", "speed, distance, time, rate"),
    "percent": ("Problem Solving", "4", "Percent Problems: finds percentage, percent change, discount, tax, tip", "percent, percentage, change, discount, tax, tip"),
    "probability": ("Problem Solving", "5", "Simple Probability: favourable/total", "probability, chance, simple"),
    "compound probability": ("Problem Solving", "6", "Compound Probability: P(A and B), P(A or B)", "compound probability, AND, OR, independent"),
    "conditional probability": ("Problem Solving", "7", "Conditional Probability (2×2 table): computes P(A|B) from table", "conditional probability, P(A|B), table, two-way"),
    "statistics": ("Problem Solving", "8", "Descriptive Statistics: mean, median, mode, quartiles, variance, std dev", "statistics, mean, median, mode, variance, standard deviation, quartile, IQR"),
    "frequency table": ("Problem Solving", "9", "Frequency Table Statistics: computes mean, median from value/frequency pairs", "frequency, grouped, mean, median, table"),
    "box plot": ("Problem Solving", "10", "Box Plot Statistics: from five-number summary, compute IQR and outliers", "box plot, five-number summary, IQR, outlier, fence"),
    "best fit": ("Problem Solving", "11", "Line of Best Fit (Linear Regression): least squares from points", "line of best fit, regression, least squares, slope, intercept"),
    "linear vs exponential": ("Problem Solving", "12", "Linear vs Exponential Models: determine growth type from data", "linear, exponential, model, growth"),
    "scatterplot": ("Problem Solving", "13", "Scatterplot Interpretation: enter points, identify correlation, estimate line", "scatterplot, correlation, trend, line of best fit"),
    "survey": ("Problem Solving", "14", "Surveys & Experiments: evaluate study design, bias, margin of error", "survey, experiment, bias, margin of error, sample"),
    "margin of error": ("Problem Solving", "15", "Margin of Error: calculates margin of error from sample stats", "margin of error, confidence, sample"),
    "weighted average": ("Problem Solving", "16", "Weighted Average: computes weighted mean from values and weights", "weighted average, mean, weights"),
    "data table": ("Problem Solving", "17", "Data Table Analysis: extract info from tables", "data table, table, extract, analyze"),
    "area": ("Geometry", "1", "Area (2D Shapes): rectangle, triangle, circle, sector, trapezoid, parallelogram", "area, rectangle, triangle, circle, sector, parallelogram, trapezoid"),
    "volume": ("Geometry", "2", "Volume (3D Shapes): prism, cylinder, cone, sphere, pyramid", "volume, prism, cylinder, cone, sphere, pyramid"),
    "surface area": ("Geometry", "3", "Surface Area: cube, prism, cylinder, cone, sphere, pyramid", "surface area, cube, prism, cylinder, cone, sphere, pyramid"),
    "coordinate": ("Geometry", "4", "Coordinate Geometry: distance, midpoint, slope, line equation", "coordinate, distance, midpoint, slope, line equation"),
    "angle": ("Geometry", "5", "Lines & Angles: complementary, supplementary, parallel lines", "angle, complement, supplement, parallel, transversal"),
    "triangle": ("Geometry", "6", "Triangles: angle sum, exterior angle, similarity", "triangle, angle sum, exterior, similarity, scale factor"),
    "right triangle": ("Geometry", "7", "Right Triangles: Pythagorean theorem, 30-60-90, 45-45-90", "right triangle, pythagorean, 30-60-90, 45-45-90"),
    "trigonometry": ("Geometry", "8", "Trigonometry (SOH-CAH-TOA): find sides or angles", "trigonometry, sin, cos, tan, SOHCAHTOA"),
    "circle": ("Geometry", "9", "Circles: circumference, area, arc length, sector area, equation", "circle, circumference, area, arc, sector, equation"),
    "circle theorem": ("Geometry", "10", "Circle Theorems: inscribed angle, central angle, arc measures", "circle theorem, inscribed angle, central angle, intercepted arc, chord, tangent"),
    "unit circle": ("Geometry", "11", "Unit Circle: exact sin/cos/tan for common angles", "unit circle, sin, cos, tan, exact values, trig"),
    "law of sines": ("Geometry", "12", "Law of Sines: find missing sides/angles", "law of sines, sine, angle, side"),
    "law of cosines": ("Geometry", "13", "Law of Cosines: find missing sides/angles", "law of cosines, cosine, angle, side"),
    "heron": ("Geometry", "14", "Heron's Formula: area from 3 sides", "heron, area, triangle, sides"),
    "3d distance": ("Geometry", "15", "3D Distance: distance between points in 3D", "3d distance, three dimensional"),
    "similar figures": ("Geometry", "16", "Similar Figures: scale factors, corresponding sides", "similar, scale factor, corresponding"),
    "congruence": ("Geometry", "17", "Congruence: determine if figures are congruent", "congruent, congruence, same shape"),
    "transformations geometry": ("Geometry", "18", "Transformations (Geometry): reflections, rotations, translations", "transformation, reflection, rotation, translation, point"),
    "complex": ("Additional Topics", "1", "Complex Numbers: add, subtract, multiply, divide, modulus, conjugate", "complex, imaginary, i, modulus, conjugate"),
    "sequence": ("Additional Topics", "2", "Sequences & Series: arithmetic and geometric nth term and sum", "sequence, arithmetic, geometric, series, sum"),
    "combinatorics": ("Additional Topics", "3", "Combinatorics: factorial, permutations nPr, combinations nCr", "counting, factorial, permutation, combination"),
    "binomial": ("Additional Topics", "4", "Binomial Theorem: find specific term in (a+b)^n", "binomial, term, expansion"),
    "matrix": ("Additional Topics", "5", "Matrices (2×2): determinant, inverse, solve system", "matrix, determinant, inverse, system, 2x2"),
    "vector": ("Additional Topics", "6", "Vectors: magnitude, dot product, angle between", "vector, magnitude, dot product, angle"),
    "radian": ("Additional Topics", "7", "Radian/Degree Converter: convert between units", "radian, degree, convert, angle"),
    "conic": ("Additional Topics", "8", "Conic Sections: identify from equation and find features", "conic, ellipse, hyperbola, circle, parabola"),
    "prime": ("Utilities", "1", "Prime Factorization: find prime factors", "prime, factorization, factor"),
    "gcf": ("Utilities", "2", "GCF: greatest common factor", "gcf, greatest common factor, gcd"),
    "lcm": ("Utilities", "3", "LCM: least common multiple", "lcm, least common multiple"),
    "fraction": ("Utilities", "4", "Fraction/Decimal/Percent conversions", "fraction, decimal, percent, convert"),
    "scientific": ("Utilities", "5", "Scientific Notation: standard ↔ scientific", "scientific notation, convert, standard"),
    "formula": ("Formula Reference", "1", "Formula Reference: browse key SAT formulas with examples", "formula, reference, cheat sheet"),
    "about": ("About", "1", "About this Program: version, license, author", "about, version, license, author"),
}


class UI:
    @staticmethod
    def clear():
        print("\n" * 30)

    @staticmethod
    def wait(prompt="Press Enter to continue."):
        try:
            input(prompt)
        except (KeyboardInterrupt, EOFError):
            raise SystemExit

    @staticmethod
    def get_float(prompt):
        while True:
            try:
                val = parse_number(input(prompt))
                if not is_finite_number(val):
                    raise ValueError("non-finite")
                return val
            except (EOFError, KeyboardInterrupt):
                raise SystemExit
            except ValueError:
                print("Invalid number. Enter finite decimals, fractions (22/7), mixed (3 1/2), or pi.")

    @staticmethod
    def get_int(prompt):
        while True:
            try:
                val = parse_number(input(prompt))
                if val == int(val):
                    return int(val)
                print("Please enter a whole number.")
            except (EOFError, KeyboardInterrupt):
                raise SystemExit
            except ValueError:
                print("Invalid number. Enter finite decimals, fractions (22/7), mixed (3 1/2), or pi.")

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
    def get_positive_int(prompt):
        while True:
            val = UI.get_int(prompt)
            if val > 0:
                return val
            print("Value must be a positive whole number.")

    @staticmethod
    def get_nonnegative_int(prompt):
        while True:
            val = UI.get_int(prompt)
            if val >= 0:
                return val
            print("Value must be a non-negative whole number.")

    @staticmethod
    def get_probability(prompt):
        while True:
            val = UI.get_float(prompt)
            if 0.0 <= val <= 1.0:
                return val
            print("Probability must be between 0 and 1 inclusive.")

    @staticmethod
    def get_operator(prompt="Operator (<, >, <=, >=): "):
        while True:
            try:
                op = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                raise SystemExit
            if op in {"<", ">", "<=", ">="}:
                return op
            print("Invalid operator. Enter one of <, >, <=, >=.")

    @staticmethod
    def show_step(label, value):
        print("  {}: {}".format(label, value))

    @staticmethod
    def show_result(label, value):
        print("{} = {}".format(label, value))


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


def solver(category, key, name):
    def decorator(func):
        SolverRegistry.register(category, key, name, func)
        return func
    return decorator


def search_solver():
    while True:
        UI.clear()
        print("SEARCH SOLVERS")
        print("Enter a keyword (e.g., 'matrix', 'statistics') or 0 to return to main menu.")
        try:
            keyword = input("Keyword: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        if keyword == "0":
            return

        if not keyword:
            print("Please enter a keyword.")
            UI.wait()
            continue

        matches = []
        seen = set()
        for k, (cat, key, desc, extra) in SEARCH_INDEX.items():
            if keyword in k or keyword in extra.lower():
                ident = (cat, key)
                if ident in seen:
                    continue
                seen.add(ident)
                matches.append((cat, key, desc))

        if not matches:
            print("No solver found for '{}'. Try a different term.".format(keyword))
            UI.wait()
            continue

        print("\nMatching solvers:\n")
        for idx, (cat, key, desc) in enumerate(matches, 1):
            print("{}. {}".format(idx, desc))

        while True:
            print("\nEnter the ID to select a solver, or 0 to return to main menu.")
            try:
                choice = input("Choice: ").strip()
            except (EOFError, KeyboardInterrupt):
                raise SystemExit
            if choice == "0":
                return
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(matches):
                    cat, key, _ = matches[choice_num - 1]
                    SolverRegistry.run_solver(cat, key)
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid selection. Please enter a number.")


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


@solver("Heart of Algebra", "2", "Slope & Intercepts")
def solve_slope_intercepts():
    UI.clear()
    print("Find slope / intercepts")
    print("1. From two points")
    print("2. From slope-intercept form (y = mx + b)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        x1 = UI.get_float("x1 = ")
        y1 = UI.get_float("y1 = ")
        x2 = UI.get_float("x2 = ")
        y2 = UI.get_float("y2 = ")
        steps = []
        steps.append("Points: ({}, {}) and ({}, {})".format(x1, y1, x2, y2))
        if x2 == x1 and y2 == y1:
            steps.append("The two points are identical; they do not determine a unique line.")
            print("\n".join("Step {}: {}".format(i+1, s) for i, s in enumerate(steps)))
            print("\n" + "─" * 40)
            print("Final answer: Undefined (identical points)")
            UI.wait()
            return
        if x2 == x1:
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
    if is_approx_zero(det):
        if is_approx_zero(a1*c2 - a2*c1) and is_approx_zero(b1*c2 - b2*c1):
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
    op = UI.get_operator()
    steps = []
    steps.append("Original: {}x + {} {} {}".format(a, b, op, c))
    if a == 0:
        steps.append("a = 0 → constant inequality: {} {} {}".format(b, op, c))
        truth = {
            "<": b < c,
            ">": b > c,
            "<=": b <= c,
            ">=": b >= c,
        }[op]
        if truth:
            steps.append("Condition is true for all x.")
            final = "All real numbers"
        else:
            steps.append("Condition is false for all x.")
            final = "No solution"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
        UI.wait()
        return
    rhs = c - b
    steps.append("Subtract {} from both sides: {}x {} {}".format(b, a, op, rhs))
    if a < 0:
        flip = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}
        new_op = flip[op]
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


@solver("Heart of Algebra", "5", "Linear Inequalities (Two Variables) - Checker")
def system_inequalities_checker():
    UI.clear()
    print("SYSTEM OF LINEAR INEQUALITIES CHECKER")
    print("Enter up to 3 inequalities in the form y ? mx + b")
    print("We'll check if a given point (x,y) satisfies ALL inequalities.\n")
    inequalities = []
    for i in range(1, 4):
        print("Inequality {}:".format(i))
        m = UI.get_float("  m (slope) = ")
        b = UI.get_float("  b (intercept) = ")
        op = UI.get_operator("  Operator (<, >, <=, >=): ")
        inequalities.append((m, b, op))
        try:
            cont = input("Add another inequality? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        if cont != 'y':
            break

    x = UI.get_float("Enter x of point: ")
    y = UI.get_float("Enter y of point: ")
    steps = []
    steps.append("Point: ({}, {})".format(x, y))
    all_satisfied = True
    for idx, (m, b, op) in enumerate(inequalities, 1):
        rhs = m*x + b
        steps.append("Inequality {}: y {} {}x + {}  →  {} {} {}".format(idx, op, m, b, y, op, rhs))
        if op == "<":
            satisfied = y < rhs
        elif op == ">":
            satisfied = y > rhs
        elif op == "<=":
            satisfied = y <= rhs
        else:
            satisfied = y >= rhs
        steps.append("  → {}".format("True" if satisfied else "False"))
        if not satisfied:
            all_satisfied = False

    final = "The point ({}, {}) {} the system.".format(x, y, "satisfies" if all_satisfied else "does NOT satisfy")
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Heart of Algebra", "6", "Linear Functions")
def solve_linear_function():
    UI.clear()
    print("Linear function: f(x) = mx + b")
    print("1. Evaluate f(x) for a given x")
    print("2. Find x when f(x) is given")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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


@solver("Heart of Algebra", "7", "Parallel & Perpendicular Lines")
def parallel_perpendicular_lines():
    UI.clear()
    print("Parallel & Perpendicular Lines")
    print("Given a line y = mx + b, or two points, find slope of parallel/perpendicular line and equation through a point.")
    print("1. From slope-intercept form (y = mx + b)")
    print("2. From two points")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    m = None
    if ch == "1":
        m = UI.get_float("m = ")
        b = UI.get_float("b = ")
        steps = []
        steps.append("Given line: y = {}x + {}".format(m, b))
    elif ch == "2":
        x1 = UI.get_float("x1 = ")
        y1 = UI.get_float("y1 = ")
        x2 = UI.get_float("x2 = ")
        y2 = UI.get_float("y2 = ")
        steps = []
        if x2 == x1 and y2 == y1:
            print("Identical points do not determine a line.")
            UI.wait()
            return
        if x2 == x1:
            steps.append("Vertical line through ({}, {}) and ({}, {})".format(x1, y1, x2, y2))
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            steps.append("Given line through points: slope = {}, intercept = {}".format(m, b))
    else:
        print("Invalid choice.")
        UI.wait()
        return

    print("\nFind slope of line that is:")
    print("1. Parallel")
    print("2. Perpendicular")
    try:
        rel = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit

    slope_new = None
    if m is None:
        if rel == "1":
            slope_new = "undefined"
            steps.append("Parallel to vertical line → vertical (undefined slope).")
        elif rel == "2":
            slope_new = 0.0
            steps.append("Perpendicular to vertical line → horizontal (slope 0).")
        else:
            print("Invalid relation.")
            UI.wait()
            return
    else:
        if rel == "1":
            slope_new = m
            steps.append("Parallel slope = original slope = {}".format(m))
        elif rel == "2":
            if m == 0:
                slope_new = "undefined"
                steps.append("Perpendicular to horizontal is vertical.")
            else:
                slope_new = -1 / m
                steps.append("Perpendicular slope = -1/m = {}".format(slope_new))
        else:
            print("Invalid relation.")
            UI.wait()
            return

    if isinstance(slope_new, str) and "undefined" in slope_new:
        xp = UI.get_float("Enter x of point: ")
        UI.get_float("Enter y of point: ")
        steps.append("Line through point is vertical: x = {}".format(xp))
        final = "Equation: x = {}".format(xp)
    else:
        xp = UI.get_float("Enter x of point: ")
        yp = UI.get_float("Enter y of point: ")
        b_new = yp - slope_new * xp
        steps.append("Using point-slope: y - {} = {}(x - {})".format(yp, slope_new, xp))
        steps.append("Simplify: y = {}x + {}".format(slope_new, b_new))
        final = "y = {}x + {}".format(slope_new, b_new)

    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Heart of Algebra", "8", "Line Translation & X-Intercept")
def line_translation_xintercept():
    UI.clear()
    print("LINE TRANSLATION AND X-INTERCEPT")
    print("Find the new x-intercept after translating a line.")
    print("1. From two points")
    print("2. From slope (m) and y-intercept (b)")
    try:
        choice = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if choice == "1":
        x1 = UI.get_float("x1 = ")
        y1 = UI.get_float("y1 = ")
        x2 = UI.get_float("x2 = ")
        y2 = UI.get_float("y2 = ")
        if x2 == x1 and y2 == y1:
            print("Identical points do not determine a line.")
            UI.wait()
            return
        if x2 == x1:
            print("Vertical line; translation not supported in this solver.")
            UI.wait()
            return
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        steps = []
        steps.append("Points: ({}, {}) and ({}, {})".format(x1, y1, x2, y2))
        steps.append("Slope m = {} / {} = {}".format(y2 - y1, x2 - x1, m))
        steps.append("y-intercept b = {} - {}*{} = {}".format(y1, m, x1, b))
    elif choice == "2":
        m = UI.get_float("m = ")
        b = UI.get_float("b = ")
        steps = []
        steps.append("Line: y = {}x + {}".format(m, b))
    else:
        print("Invalid choice.")
        UI.wait()
        return

    print("\nTranslation options:")
    print("1. Vertical (up/down)")
    print("2. Horizontal (left/right)")
    try:
        trans_choice = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if trans_choice == "1":
        try:
            direction = input("Direction (up/down): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        amount = UI.get_float("Amount: ")
        if direction == "up":
            new_b = b + amount
            steps.append("Translate up by {}: new y-intercept = {} + {} = {}".format(amount, b, amount, new_b))
        elif direction == "down":
            new_b = b - amount
            steps.append("Translate down by {}: new y-intercept = {} - {} = {}".format(amount, b, amount, new_b))
        else:
            print("Invalid direction.")
            UI.wait()
            return
        new_m = m
        steps.append("New line: y = {}x + {}".format(new_m, new_b))
        if new_m == 0:
            if new_b == 0:
                steps.append("Line is y = 0 (x-axis); every x is an x-intercept.")
                final = "All real numbers are x-intercepts."
            else:
                steps.append("Horizontal line, no x-intercept.")
                final = "Horizontal line, no x-intercept."
        else:
            x_int = -new_b / new_m
            steps.append("x-intercept: set y=0 → 0 = {}x + {} → x = {}".format(new_m, new_b, x_int))
            final = "x-intercept = {}".format(x_int)
    elif trans_choice == "2":
        try:
            direction = input("Direction (left/right): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        amount = UI.get_float("Amount: ")
        if direction == "right":
            steps.append("Translate right by {}: replace x with (x - {})".format(amount, amount))
            new_m = m
            new_b = b - m*amount
            steps.append("New line: y = {}x + ({})".format(new_m, new_b))
        elif direction == "left":
            steps.append("Translate left by {}: replace x with (x + {})".format(amount, amount))
            new_m = m
            new_b = b + m*amount
            steps.append("New line: y = {}x + ({})".format(new_m, new_b))
        else:
            print("Invalid direction.")
            UI.wait()
            return
        if new_m == 0:
            if new_b == 0:
                steps.append("Line is y = 0 (x-axis); every x is an x-intercept.")
                final = "All real numbers are x-intercepts."
            else:
                steps.append("Horizontal line, no x-intercept.")
                final = "Horizontal line, no x-intercept."
        else:
            x_int = -new_b / new_m
            steps.append("x-intercept: set y=0 → 0 = {}x + {} → x = {}".format(new_m, new_b, x_int))
            final = "x-intercept = {}".format(x_int)
    else:
        print("Invalid translation choice.")
        UI.wait()
        return

    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Heart of Algebra", "9", "Linear Word Problems")
def linear_word_problems():
    UI.clear()
    print("LINEAR WORD PROBLEMS")
    print("Translate word problems to linear equations and solve.")
    print("1. Simple linear equation (ax + b = cx + d)")
    print("2. Equation from two points (find slope and intercept)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        solve_linear_one_var()
    elif ch == "2":
        x1 = UI.get_float("x1 = ")
        y1 = UI.get_float("y1 = ")
        x2 = UI.get_float("x2 = ")
        y2 = UI.get_float("y2 = ")
        if x2 == x1:
            if y2 == y1:
                print("Identical points do not determine a line.")
                UI.wait()
                return
            print("Vertical line: x = {}".format(x1))
            final = "x = {}".format(x1)
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            steps = []
            steps.append("Slope = {}, intercept = {}".format(m, b))
            steps.append("Equation: y = {}x + {}".format(m, b))
            final = "y = {}x + {}".format(m, b)
            for i, s in enumerate(steps, 1):
                print("Step {}: {}".format(i, s))
            print("\n" + "─" * 40)
            print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()


@solver("Advanced Math", "1", "Equivalent Expressions (simplify/factor)")
def simplify_expression():
    UI.clear()
    print("Equivalent Expressions (basic expand/factor)")
    print("1. Expand (ax+b)(cx+d)")
    print("2. Factor x^2 + px + q")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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


@solver("Advanced Math", "2", "Quadratic Equations")
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
    elif is_approx_zero(disc):
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


@solver("Advanced Math", "3", "Parabolas")
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


@solver("Advanced Math", "4", "System: Line & Parabola/Circle")
def solve_nonlinear_system():
    UI.clear()
    print("Nonlinear system solver:")
    print("1. Line and Parabola")
    print("2. Line and Circle")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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
        elif is_approx_zero(disc):
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
        h = UI.get_float("h (center x) = ")
        k = UI.get_float("k (center y) = ")
        r = UI.get_positive_float("Radius r = ")
        m = UI.get_float("Line slope m = ")
        b_line = UI.get_float("Line y-intercept b = ")
        steps = []
        steps.append("Circle: (x - {})^2 + (y - {})^2 = {}".format(h, k, r*r))
        steps.append("Line: y = {}x + {}".format(m, b_line))
        A = 1 + m*m
        B = 2*m*(b_line - k) - 2*h
        C = h*h + (b_line - k)*(b_line - k) - r*r
        steps.append("Substitute: (1 + {})x^2 + {}x + {} = 0".format(m*m, B, C))
        steps.append(" => {}x^2 + {}x + {} = 0".format(A, B, C))
        disc = B*B - 4*A*C
        steps.append("Discriminant = {}^2 - 4*{}*{} = {}".format(B, A, C, disc))
        if disc < 0:
            steps.append("No intersection (discriminant < 0).")
            final = "No intersection"
        elif is_approx_zero(disc):
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


@solver("Advanced Math", "5", "Exponential Functions")
def exponential_functions():
    UI.clear()
    print("Exponential Functions")
    print("1. Basic Growth/Decay: y = a * b^x")
    print("2. Compound Interest: A = P(1 + r/n)^(nt)")
    print("3. Half-life / Doubling time")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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
        n = UI.get_positive_int("Compounded per year n = ")
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
        try:
            sub = input("Choice: ")
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
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
    print("Polynomial roots")
    print("1. Quadratic (ax^2+bx+c)")
    print("2. Cubic (limited to guess integer root)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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
        a = UI.get_nonzero_float("a = ")
        b = UI.get_float("b = ")
        c = UI.get_float("c = ")
        d = UI.get_float("d = ")
        steps = []
        steps.append("Cubic: {}x^3 + {}x^2 + {}x + {} = 0".format(a, b, c, d))
        found = False
        x = None
        for x_test in range(-50, 51):
            val = a*x_test**3 + b*x_test**2 + c*x_test + d
            if is_approx_zero(val):
                steps.append("Found integer root: x = {}".format(x_test))
                found = True
                x = x_test
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
                    return sorted(divs)
                a_divs = divisors(a_int)
                d_divs = divisors(d_int)
                for p in d_divs:
                    for q in a_divs:
                        for sign in (1, -1):
                            x_test = sign * p / q
                            val = a*x_test**3 + b*x_test**2 + c*x_test + d
                            if is_approx_zero(val):
                                steps.append("Found rational root: x = {}".format(x_test))
                                found = True
                                x = x_test
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
    if c == 0 and d == 0:
        steps.append("Denominator identically zero → function undefined everywhere.")
        final = "Undefined"
    elif c == 0:
        steps.append("Denominator is a nonzero constant → linear function.")
        slope = a / d
        intercept = b / d
        steps.append("f(x) = ({}/{})x + ({}/{}) = {}x + {}".format(a, d, b, d, slope, intercept))
        steps.append("No vertical asymptote. No horizontal asymptote (unbounded linear).")
        final = "Linear function: f(x) = {}x + {} (no asymptotes)".format(slope, intercept)
    else:
        vertical = -d / c
        has_hole = is_approx_zero(a * d - b * c)
        if has_hole:
            if is_approx_zero(a) and is_approx_zero(b):
                steps.append("Numerator identically zero → f(x) = 0 for x ≠ {}.".format(vertical))
                steps.append("Removable hole at x = {} with value 0.".format(vertical))
                final = "Hole at x = {} (value 0); domain: x ≠ {}; range: {{0}}".format(vertical, vertical)
            else:
                hole_val = a / c
                steps.append("Numerator is a multiple of denominator → removable hole.")
                steps.append("Hole at x = {} with limit value a/c = {}.".format(vertical, hole_val))
                final = "Hole at x = {} (value {}); domain: x ≠ {}; range: y ≠ {}".format(vertical, hole_val, vertical, hole_val)
        else:
            steps.append("Vertical asymptote: set denominator = 0 → {}x + {} = 0 → x = {}".format(c, d, vertical))
            if a == 0:
                horizontal = 0
                steps.append("Numerator degree (0) < denominator degree (1) → horizontal asymptote: y = 0")
            else:
                horizontal = a / c
                steps.append("Both linear (degree 1) → horizontal asymptote: y = a/c = {}".format(horizontal))
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
            if is_approx_zero(C):
                steps.append("After squaring, identity — verify original for all x.")
                if d < 0:
                    steps.append("Right side d = {} < 0, but square root is non-negative → no solution.".format(d))
                    final = "No solution"
                elif a == 0:
                    if b >= 0 and is_approx_zero(math.sqrt(b) - d):
                        steps.append("√{} = {} → true for all x.".format(b, d))
                        final = "All real numbers"
                    else:
                        steps.append("√{} ≠ {} → no solution.".format(b, d))
                        final = "No solution"
                else:
                    x = (d*d - b) / a
                    if a*x + b >= 0:
                        steps.append("Unique solution: x = {}".format(x))
                        final = "x = {}".format(x)
                    else:
                        steps.append("Solution fails domain check.")
                        final = "No solution"
            else:
                steps.append("No solution after squaring.")
                final = "No solution"
        else:
            x = -C / B
            steps.append("Linear: x = {} / {} = {}".format(-C, B, x))
            if a*x + b >= 0 and c*x + d >= 0:
                left = math.sqrt(a*x + b)
                right = c*x + d
                if is_approx_zero(left - right):
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
        elif is_approx_zero(disc):
            x = -B / (2*A)
            steps.append("Discriminant = 0 → one double root: x = {}".format(x))
            if a*x + b >= 0 and c*x + d >= 0:
                left = math.sqrt(a*x + b)
                right = c*x + d
                if is_approx_zero(left - right):
                    steps.append("Check: √({}) = {} → valid".format(a*x+b, right))
                    final = "x = {}".format(x)
                else:
                    steps.append("Check: √({}) = {} ≠ {} → extraneous".format(a*x+b, left, right))
                    final = "No valid solution (extraneous)"
            else:
                steps.append("Domain error: {}x+{} or {}x+{} negative".format(a, b, c, d))
                final = "No valid solution"
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
                    if is_approx_zero(left - right):
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
            if is_approx_zero(abs(b) - c):
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


@solver("Advanced Math", "10", "Quadratic Inequality")
def quadratic_inequality():
    UI.clear()
    print("QUADRATIC INEQUALITY (ax^2+bx+c > 0, etc.)")
    a = UI.get_nonzero_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    op = UI.get_operator()
    steps = []
    steps.append("Solve {}x² + {}x + {} {} 0".format(a, b, c, op))
    disc = b*b - 4*a*c
    steps.append("Discriminant D = {}² - 4*{}*{} = {}".format(b, a, c, disc))
    if disc < 0:
        steps.append("No real roots (discriminant < 0).")
        if a > 0:
            truth = op in (">", ">=")
            steps.append("a > 0 → parabola opens up, expression always positive.")
        else:
            truth = op in ("<", "<=")
            steps.append("a < 0 → parabola opens down, expression always negative.")
        final = "All real x" if truth else "No solution"
    elif is_approx_zero(disc):
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
            else:
                steps.append("a > 0 → expression <= 0 only at root.")
                final = "x = {}".format(root)
        else:
            if op == "<":
                steps.append("a < 0 → expression < 0 except at root.")
                final = "x ≠ {}".format(root)
            elif op == "<=":
                steps.append("a < 0 → expression <= 0 everywhere.")
                final = "All real x"
            elif op == ">":
                steps.append("a < 0 → expression never positive.")
                final = "No solution"
            else:
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
            else:
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
            else:
                steps.append("a < 0 → solution outside interval (including endpoints).")
                final = "x ≤ {} or x ≥ {}".format(r1, r2)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "11", "Absolute Value Inequality")
def absolute_value_inequality():
    UI.clear()
    print("ABSOLUTE VALUE INEQUALITY: |ax+b| < c  (or >, <=, >=)")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    op = UI.get_operator()
    steps = []
    steps.append("|{}x + {}| {} {}".format(a, b, op, c))
    if a == 0:
        abs_b = abs(b)
        steps.append("Constant |{}| = {}".format(b, abs_b))
        if op == "<":
            result = abs_b < c
        elif op == "<=":
            result = abs_b <= c
        elif op == ">":
            result = abs_b > c
        else:
            result = abs_b >= c
        final = "All real numbers" if result else "No solution"
        steps.append("Condition {} → {}".format(op, final))
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
        UI.wait()
        return
    if c < 0:
        if op in (">", ">="):
            final = "All real numbers (absolute value always >= 0 > negative)"
        else:
            final = "No solution (absolute value cannot be < negative)"
        steps.append("c < 0 → special case.")
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif c == 0:
        x = -b/a
        if op == "<":
            steps.append("|{}x+{}| < 0 has no solution.".format(a, b))
            final = "No solution"
        elif op == "<=":
            steps.append("|{}x+{}| <= 0 only when = 0 → x = {}".format(a, b, x))
            final = "x = {}".format(x)
        elif op == ">":
            steps.append("|{}x+{}| > 0 for all x except {}".format(a, b, x))
            final = "x ≠ {}".format(x)
        else:
            steps.append("|{}x+{}| >= 0 for all real x".format(a, b))
            final = "All real x"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        if op in ("<", "<="):
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


@solver("Advanced Math", "12", "Polynomial Long Division")
def polynomial_long_division():
    UI.clear()
    print("POLYNOMIAL LONG DIVISION (linear divisor only)")
    print("Divide polynomial P(x) by (x - c) using synthetic division.")
    c = UI.get_float("c (divisor x-c): ")
    print("Enter coefficients of P(x) from highest degree to constant, separated by spaces:")
    try:
        coeff_str = input("> ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    try:
        coeff = [parse_number(x) for x in coeff_str.split()]
    except Exception:
        print("Invalid coefficients.")
        UI.wait()
        return
    if len(coeff) < 2:
        print("Need at least 2 coefficients.")
        UI.wait()
        return
    result = [coeff[0]]
    for i in range(1, len(coeff)):
        prev = result[-1]
        new_val = prev * c + coeff[i]
        result.append(new_val)
    quotient_coeffs = result[:-1]
    remainder = result[-1]

    steps = []
    steps.append("Synthetic division with c = {}".format(c))
    steps.append("Bring down {}:".format(coeff[0]))
    for i in range(1, len(coeff)):
        prev = result[i-1]
        prod = prev * c
        add = coeff[i]
        new_val = prod + add
        steps.append("Multiply {} by {} → {}, add to {} → {}".format(prev, c, prod, add, new_val))
    steps.append("Remainder: {}".format(remainder))
    deg = len(quotient_coeffs) - 1
    poly_str = ""
    for i, coef in enumerate(quotient_coeffs):
        power = deg - i
        if is_approx_zero(coef):
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


@solver("Advanced Math", "13", "Remainder Theorem")
def remainder_theorem():
    UI.clear()
    print("REMAINDER THEOREM")
    print("Evaluates P(c) using synthetic substitution.")
    c = UI.get_float("c = ")
    try:
        coeff_str = input("Enter polynomial coefficients (high to low) separated by spaces: ").strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if not coeff_str:
        print("No coefficients entered.")
        UI.wait()
        return
    try:
        coeff = [parse_number(x) for x in coeff_str.split()]
    except Exception:
        print("Invalid.")
        UI.wait()
        return
    if not coeff:
        print("No coefficients.")
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


@solver("Advanced Math", "14", "Completing the Square")
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


@solver("Advanced Math", "15", "Function Transformations")
def function_transformations():
    UI.clear()
    print("FUNCTION TRANSFORMATIONS")
    print("Enter parent function:")
    print("1. x^2")
    print("2. x^3")
    print("3. |x|")
    print("4. sqrt(x)")
    print("5. 1/x")
    try:
        parent_choice = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    parent_map = {"1": "x^2", "2": "x^3", "3": "|x|", "4": "sqrt(x)", "5": "1/x"}
    parent = parent_map.get(parent_choice, "x^2")
    steps = []
    steps.append("Parent function: f(x) = {}".format(parent))

    transforms = []
    print("Enter transformations (one per line), empty line to finish.")
    print("Options: left/right/up/down <value>, stretch <factor>, compress <factor>, reflect x, reflect y")
    while True:
        try:
            t = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        if not t:
            break
        transforms.append(t)

    expression = parent
    for t in transforms:
        lower = t.lower()
        if "left" in lower:
            try:
                val = parse_number(t.split()[-1])
                expression = expression.replace("x", "(x + {})".format(val))
                steps.append("Shift left by {} → f(x+{})".format(val, val))
            except Exception:
                steps.append("Invalid left shift")
        elif "right" in lower:
            try:
                val = parse_number(t.split()[-1])
                expression = expression.replace("x", "(x - {})".format(val))
                steps.append("Shift right by {} → f(x-{})".format(val, val))
            except Exception:
                steps.append("Invalid right shift")
        elif "up" in lower:
            try:
                val = parse_number(t.split()[-1])
                expression = "({} + {})".format(expression, val)
                steps.append("Shift up by {} → f(x)+{}".format(val, val))
            except Exception:
                steps.append("Invalid up shift")
        elif "down" in lower:
            try:
                val = parse_number(t.split()[-1])
                expression = "({} - {})".format(expression, val)
                steps.append("Shift down by {} → f(x)-{}".format(val, val))
            except Exception:
                steps.append("Invalid down shift")
        elif "stretch" in lower:
            try:
                val = parse_number(t.split()[-1])
                expression = "{}*({})".format(val, expression)
                steps.append("Vertical stretch by {} → {}*f(x)".format(val, val))
            except Exception:
                steps.append("Invalid stretch factor")
        elif "compress" in lower:
            try:
                val = parse_number(t.split()[-1])
                expression = "{}*({})".format(val, expression)
                steps.append("Vertical compression by {} → {}*f(x)".format(val, val))
            except Exception:
                steps.append("Invalid compression factor")
        elif "reflect x" in lower:
            expression = "-({})".format(expression)
            steps.append("Reflect over x-axis → -f(x)")
        elif "reflect y" in lower:
            expression = expression.replace("x", "(-x)")
            steps.append("Reflect over y-axis → f(-x)")
        else:
            steps.append("Unknown transformation: {}".format(t))

    final = "Transformed function: g(x) = {}".format(expression)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "16", "Inverse Function (linear)")
def inverse_function_linear():
    UI.clear()
    print("INVERSE FUNCTION (linear) f(x) = mx + b")
    m = UI.get_float("m = ")
    b = UI.get_float("b = ")
    steps = []
    steps.append("f(x) = {}x + {}".format(m, b))
    if m == 0:
        steps.append("m = 0 → function is constant, no inverse (not one-to-one).")
        final = "No inverse (constant function)"
    else:
        inv_m = 1/m
        inv_b = -b/m
        steps.append("To find inverse, swap x and y: x = {}y + {}".format(m, b))
        steps.append("Solve for y: y = (x - {}) / {}".format(b, m))
        steps.append("f^(-1)(x) = {}x + {}".format(inv_m, inv_b))
        final = "f^(-1)(x) = {}x + {}".format(inv_m, inv_b)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "17", "Piecewise Function Evaluator")
def piecewise_evaluator():
    UI.clear()
    print("PIECEWISE FUNCTION EVALUATOR")
    pieces = []
    print("Enter pieces one by one. Each piece: condition (e.g., x < 2) and expression (e.g., x^2).")
    print("Use 'x' as the variable. Empty line to finish.")
    while True:
        try:
            cond = input("Condition (or blank to finish): ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        if not cond:
            break
        try:
            expr = input("Expression: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        if not expr:
            print("Expression cannot be empty.")
            continue
        pieces.append((cond, expr))
    if not pieces:
        print("No pieces entered.")
        UI.wait()
        return
    x_val = UI.get_float("Enter x to evaluate: ")
    steps = []
    steps.append("x = {}".format(x_val))
    result = None
    scope = {"x": x_val, "math": math, "sqrt": math.sqrt, "abs": abs, "sin": math.sin,
             "cos": math.cos, "tan": math.tan, "log": math.log, "log10": math.log10,
             "exp": math.exp, "pi": math.pi, "e": math.e}
    for cond, expr in pieces:
        try:
            cond_eval = eval(cond, {"__builtins__": {}}, scope)
        except Exception as e:
            steps.append("Error evaluating condition '{}': {}".format(cond, e))
            continue
        if cond_eval:
            try:
                result = eval(expr, {"__builtins__": {}}, scope)
            except Exception as e:
                steps.append("Error evaluating expression '{}': {}".format(expr, e))
                final = "Error"
                for i, s in enumerate(steps, 1):
                    print("Step {}: {}".format(i, s))
                print("\n" + "─" * 40)
                print("Final answer: {}".format(final))
                UI.wait()
                return
            steps.append("Condition '{}' is true for x={}".format(cond, x_val))
            steps.append("Evaluate '{}' → {}".format(expr, result))
            break
        else:
            steps.append("Condition '{}' is false for x={}".format(cond, x_val))
    if result is None:
        steps.append("No piece matched the given x.")
        final = "Undefined (no piece matches)"
    else:
        final = "f({}) = {}".format(x_val, result)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "18", "Even/Odd Functions")
def even_odd_functions():
    UI.clear()
    print("EVEN/ODD FUNCTIONS")
    print("Enter function as expression in x, e.g., x^2, x^3, x^2+x, etc.")
    try:
        expr = input("f(x) = ").strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if not expr:
        print("No expression entered.")
        UI.wait()
        return
    scope_template = {"__builtins__": {}, "math": math, "sqrt": math.sqrt, "abs": abs,
                      "sin": math.sin, "cos": math.cos, "tan": math.tan,
                      "log": math.log, "exp": math.exp, "pi": math.pi, "e": math.e}
    def eval_func(x):
        try:
            s = dict(scope_template)
            s["x"] = x
            return eval(expr, s)
        except Exception:
            return None
    steps = []
    steps.append("f(x) = {}".format(expr))
    test_vals = [0.5, 1, 2, 3]
    even = True
    odd = True
    for val in test_vals:
        f_pos = eval_func(val)
        f_neg = eval_func(-val)
        if f_pos is None or f_neg is None:
            steps.append("Cannot evaluate at x={} or -{}".format(val, val))
            even = odd = False
            break
        steps.append("f({}) = {}, f(-{}) = {}".format(val, f_pos, val, f_neg))
        if not is_approx_zero(f_pos - f_neg):
            even = False
        if not is_approx_zero(f_pos + f_neg):
            odd = False
    if even and odd:
        final = "Both even and odd (zero function only)"
    elif even:
        final = "Even function (symmetric about y-axis)"
    elif odd:
        final = "Odd function (symmetric about origin)"
    else:
        final = "Neither even nor odd"
    steps.append("Conclusion: {}".format(final))
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "19", "Domain & Range Finder")
def domain_range_finder():
    UI.clear()
    print("DOMAIN & RANGE FINDER")
    print("1. Polynomial")
    print("2. Rational (linear/linear)")
    print("3. Radical (sqrt of expression)")
    print("4. Logarithmic (log of expression)")
    print("5. Exponential (a*b^x)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    steps = []
    if ch == "1":
        steps.append("Polynomials are defined for all real x.")
        steps.append("Domain: all real numbers (-∞, ∞)")
        final = "Domain: (-∞, ∞); Range: varies by degree and leading coefficient"
    elif ch == "2":
        a = UI.get_float("Numerator a (ax+b): a = ")
        b = UI.get_float("b = ")
        c = UI.get_float("Denominator c (cx+d): c = ")
        d = UI.get_float("d = ")
        steps.append("f(x) = ({}x + {}) / ({}x + {})".format(a, b, c, d))
        if c == 0:
            if d == 0:
                steps.append("Denominator identically zero → undefined everywhere.")
                final = "Domain: empty; Range: undefined"
            else:
                steps.append("Denominator constant → domain all reals.")
                final = "Domain: (-∞, ∞)"
        else:
            va = -d / c
            steps.append("Denominator zero at x = {}".format(va))
            steps.append("Domain: all real x except {}".format(va))
            if a == 0:
                final = "Domain: x ≠ {}; Range: y = 0 (excluding any hole)".format(va)
            else:
                ha = a / c
                final = "Domain: x ≠ {}; Horizontal asymptote y = {} (range excludes y = {})".format(va, ha, ha)
    elif ch == "3":
        try:
            expr = input("Inside sqrt: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        steps.append("Domain: expression inside sqrt must be >= 0")
        steps.append("Solve {} >= 0".format(expr))
        try:
            x = UI.get_float("Solve at x = ")
            scope = {"__builtins__": {}, "x": x, "math": math, "sqrt": math.sqrt,
                     "abs": abs, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                     "log": math.log, "exp": math.exp, "pi": math.pi, "e": math.e}
            val = eval(expr, scope)
            steps.append("At x = {}, inside = {}".format(x, val))
            steps.append("Check sign across domain.")
        except Exception as e:
            steps.append("Could not evaluate: {}".format(e))
        final = "Domain: x such that {} >= 0".format(expr)
    elif ch == "4":
        try:
            arg = input("Argument: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        steps.append("Domain: argument must be > 0")
        steps.append("Solve {} > 0".format(arg))
        final = "Domain: x such that {} > 0".format(arg)
    elif ch == "5":
        steps.append("Exponential functions defined for all real x.")
        steps.append("Domain: (-∞, ∞)")
        steps.append("Range: (0, ∞) if a>0, else (-∞, 0) if a<0")
        final = "Domain: (-∞, ∞); Range: (0, ∞) for a>0, (-∞, 0) for a<0"
    else:
        print("Invalid choice.")
        UI.wait()
        return
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "20", "Function Composition")
def function_composition():
    UI.clear()
    print("FUNCTION COMPOSITION (f∘g)(x)")
    print("Enter f(x) and g(x) as expressions in x.")
    try:
        f_expr = input("f(x) = ").strip()
        g_expr = input("g(x) = ").strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if not f_expr or not g_expr:
        print("Both functions required.")
        UI.wait()
        return
    x_val = UI.get_float("Enter x to evaluate: ")
    steps = []
    steps.append("f(x) = {}, g(x) = {}".format(f_expr, g_expr))
    scope = {"__builtins__": {}, "x": x_val, "math": math, "sqrt": math.sqrt,
             "abs": abs, "sin": math.sin, "cos": math.cos, "tan": math.tan,
             "log": math.log, "exp": math.exp, "pi": math.pi, "e": math.e}
    try:
        g_val = eval(g_expr, scope)
    except Exception as e:
        steps.append("Error evaluating g({}): {}".format(x_val, e))
        final = "Error"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
        UI.wait()
        return
    steps.append("g({}) = {}".format(x_val, g_val))
    scope2 = dict(scope)
    scope2["x"] = g_val
    try:
        fg_val = eval(f_expr, scope2)
    except Exception as e:
        steps.append("Error evaluating f({}): {}".format(g_val, e))
        final = "Error"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
        UI.wait()
        return
    steps.append("f({}) = {}".format(g_val, fg_val))
    final = "(f∘g)({}) = {}".format(x_val, fg_val)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "21", "Rational Equations")
def rational_equation():
    UI.clear()
    print("Solve (ax + b) / (cx + d) = k")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    d = UI.get_float("d = ")
    k = UI.get_float("k = ")
    steps = []
    steps.append("({}x + {}) / ({}x + {}) = {}".format(a, b, c, d, k))
    if c == 0 and d == 0:
        steps.append("Denominator identically zero → undefined.")
        final = "Undefined"
    else:
        steps.append("Multiply both sides by ({}x + {}):".format(c, d))
        steps.append("{}x + {} = {} * ({}x + {})".format(a, b, k, c, d))
        steps.append("{}x + {} = {}x + {}".format(a, b, k*c, k*d))
        lhs_coeff = a - k*c
        rhs_const = k*d - b
        steps.append("Bring x terms: {}x = {}".format(lhs_coeff, rhs_const))
        if is_approx_zero(lhs_coeff):
            if is_approx_zero(rhs_const):
                steps.append("Identity → infinite solutions (except domain).")
                final = "All x (except denominator zero)"
            else:
                steps.append("No solution.")
                final = "No solution"
        else:
            x = rhs_const / lhs_coeff
            steps.append("x = {} / {} = {}".format(rhs_const, lhs_coeff, x))
            if is_approx_zero(c*x + d):
                steps.append("But x = {} makes denominator zero, so extraneous.".format(x))
                final = "No valid solution (extraneous)"
            else:
                final = "x = {}".format(x)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "22", "Parameter Condition Solver")
def parameter_condition_solver():
    UI.clear()
    print("PARAMETER CONDITION SOLVER")
    print("Finds values of parameters (e.g., r, s) that make a linear equation have infinitely many solutions.")
    print("Given an equation of the form A*x + B = C*x + D, we equate coefficients.")
    print("You'll enter the resulting system of two linear equations in two unknown parameters.")
    print("The solver will solve for the parameters using Cramer's rule.\n")
    print("Example: For the problem (12x+28)/4 - s/13 = r(x-8), we get:")
    print("  From x coefficients:  1*r + 0*s = 3")
    print("  From constants:       8*r + (1/13)*s = 7")
    print("Enter those two equations below.\n")
    print("Enter coefficients for equation 1: a1*p + b1*q = c1")
    a1 = UI.get_float("a1 = ")
    b1 = UI.get_float("b1 = ")
    c1 = UI.get_float("c1 = ")
    print("Enter coefficients for equation 2: a2*p + b2*q = c2")
    a2 = UI.get_float("a2 = ")
    b2 = UI.get_float("b2 = ")
    c2 = UI.get_float("c2 = ")
    steps = []
    steps.append("System:")
    steps.append("  {}p + {}q = {}".format(a1, b1, c1))
    steps.append("  {}p + {}q = {}".format(a2, b2, c2))
    det = a1*b2 - a2*b1
    steps.append("Det = {}*{} - {}*{} = {}".format(a1, b2, a2, b1, det))
    if is_approx_zero(det):
        steps.append("Det = 0 → no unique solution for parameters (or infinite parameter solutions).")
        steps.append("Check if the system is consistent.")
        if is_approx_zero(a1*c2 - a2*c1) and is_approx_zero(b1*c2 - b2*c1):
            steps.append("System is dependent → infinitely many parameter pairs satisfy the condition.")
            final = "Infinite parameter solutions"
        else:
            steps.append("System is inconsistent → no parameter values can satisfy the condition.")
            final = "No solution for parameters"
    else:
        det_p = c1*b2 - c2*b1
        det_q = a1*c2 - a2*c1
        steps.append("det_p = {}*{} - {}*{} = {}".format(c1, b2, c2, b1, det_p))
        steps.append("det_q = {}*{} - {}*{} = {}".format(a1, c2, a2, c1, det_q))
        p = det_p / det
        q = det_q / det
        steps.append("p = det_p / det = {} / {} = {}".format(det_p, det, p))
        steps.append("q = det_q / det = {} / {} = {}".format(det_q, det, q))
        final = "p = {}, q = {}".format(p, q)
        steps.append("These values make the original equation an identity (infinite solutions).")
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Advanced Math", "23", "Exponential Equations")
def exponential_equations():
    UI.clear()
    print("EXPONENTIAL EQUATIONS")
    print("Solve b^(ax+c) = d")
    b = UI.get_positive_float("base b = ")
    a = UI.get_float("a = ")
    c = UI.get_float("c = ")
    d = UI.get_positive_float("d = ")
    steps = []
    if is_approx_zero(b - 1):
        steps.append("Base = 1 → 1^(anything) = 1.")
        if is_approx_zero(d - 1):
            steps.append("d = 1 → identity. All x are solutions.")
            final = "All real numbers"
        else:
            steps.append("d ≠ 1 → no solution.")
            final = "No solution"
    else:
        if a == 0:
            lhs = b ** c
            steps.append("Constant: {}^{} = {}".format(b, c, lhs))
            if is_approx_zero(lhs - d):
                steps.append("Identity → all x are solutions.")
                final = "All real numbers"
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


@solver("Advanced Math", "24", "Logarithmic Equations")
def logarithmic_equations():
    UI.clear()
    print("LOGARITHMIC EQUATIONS")
    print("Solve log_b(ax+c) = d")
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
    UI.wait()


@solver("Problem Solving", "1", "Ratios & Proportions")
def ratios_proportions():
    UI.clear()
    print("Solve proportion a/b = c/x")
    a = UI.get_float("a = ")
    b = UI.get_nonzero_float("b = ")
    c = UI.get_float("c = ")
    steps = []
    steps.append("Proportion: {}/{} = {}/x".format(a, b, c))
    if a == 0:
        if c == 0:
            steps.append("0/{} = 0/x → true for all x ≠ 0.".format(b))
            final = "All x except 0"
        else:
            steps.append("0/{} = {}/x has no solution (since c ≠ 0).".format(b, c))
            final = "No solution"
    else:
        x = (c * b) / a
        steps.append("Cross multiply: {} * x = {} * {}".format(a, c, b))
        steps.append("x = {} * {} / {} = {}".format(c, b, a, x))
        final = "x = {}".format(x)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "2", "Unit Rates")
def unit_rates():
    UI.clear()
    print("Unit rate: quantity per 1 unit")
    total_qty = UI.get_float("Total quantity = ")
    total_units = UI.get_nonzero_float("Total units = ")
    steps = []
    rate = total_qty / total_units
    steps.append("Unit rate = {} / {} = {}".format(total_qty, total_units, rate))
    final = "{} per unit".format(rate)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "3", "Speed/Distance/Time")
def speed_distance_time():
    UI.clear()
    print("Speed/Distance/Time")
    print("1. Find speed")
    print("2. Find distance")
    print("3. Find time")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
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
    elif ch == "2":
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
    elif ch == "3":
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
    UI.wait()


@solver("Problem Solving", "4", "Percent Problems")
def percent_problems():
    UI.clear()
    print("Percent Problems")
    print("1. Find % of a number")
    print("2. Percent increase/decrease")
    print("3. Discount / Tax / Tip")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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
        original = UI.get_nonzero_float("Original value = ")
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
        try:
            sub = input("Choice: ")
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        price = UI.get_positive_float("Original price = ")
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


@solver("Problem Solving", "5", "Simple Probability")
def simple_probability():
    UI.clear()
    print("Simple Probability")
    while True:
        fav = UI.get_int("Favourable outcomes = ")
        total = UI.get_int("Total outcomes = ")
        if total <= 0:
            print("Total outcomes must be positive.")
            continue
        if fav < 0 or fav > total:
            print("Favourable outcomes must be between 0 and {} inclusive.".format(total))
            continue
        break
    steps = []
    p = fav / total
    steps.append("P = {} / {} = {}".format(fav, total, p))
    final = "P = {}".format(p)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "6", "Compound Probability")
def compound_probability():
    UI.clear()
    print("Compound Probability")
    print("1. P(A and B) = P(A)*P(B) if independent")
    print("2. P(A or B) = P(A)+P(B)-P(A and B)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    pa = UI.get_probability("P(A) = ")
    pb = UI.get_probability("P(B) = ")
    if ch == "1":
        steps = []
        steps.append("P(A and B) = P(A) * P(B)")
        steps.append("= {} * {} = {}".format(pa, pb, pa*pb))
        final = "P(A and B) = {}".format(pa*pb)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        p_and = UI.get_probability("P(A and B) = ")
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
    UI.wait()


@solver("Problem Solving", "7", "Conditional Probability (2×2 table)")
def conditional_probability():
    UI.clear()
    print("Conditional Probability from a 2x2 table.")
    print("Enter counts for A and B:")
    a_yes_b_yes = UI.get_float("A yes, B yes = ")
    a_yes_b_no = UI.get_float("A yes, B no = ")
    a_no_b_yes = UI.get_float("A no, B yes = ")
    a_no_b_no = UI.get_float("A no, B no = ")
    steps = []
    total = a_yes_b_yes + a_yes_b_no + a_no_b_yes + a_no_b_no
    steps.append("Table:")
    steps.append("          B yes   B no")
    steps.append("A yes     {}      {}".format(a_yes_b_yes, a_yes_b_no))
    steps.append("A no      {}      {}".format(a_no_b_yes, a_no_b_no))
    steps.append("Total = {}".format(total))
    denom_ab = a_yes_b_yes + a_no_b_yes
    denom_ba = a_yes_b_yes + a_yes_b_no
    p_a_given_b = a_yes_b_yes / denom_ab if denom_ab > 0 else None
    p_b_given_a = a_yes_b_yes / denom_ba if denom_ba > 0 else None
    p_a = (a_yes_b_yes + a_yes_b_no) / total if total != 0 else None
    p_b = (a_yes_b_yes + a_no_b_yes) / total if total != 0 else None
    steps.append("P(A|B) = P(A and B) / P(B) = {} / {} = {}".format(
        a_yes_b_yes, denom_ab, p_a_given_b if p_a_given_b is not None else "undefined"))
    steps.append("P(B|A) = P(A and B) / P(A) = {} / {} = {}".format(
        a_yes_b_yes, denom_ba, p_b_given_a if p_b_given_a is not None else "undefined"))
    steps.append("P(A) = {}".format(p_a))
    steps.append("P(B) = {}".format(p_b))
    final = "P(A|B) = {}, P(B|A) = {}".format(p_a_given_b, p_b_given_a)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "8", "Descriptive Statistics")
def descriptive_stats():
    UI.clear()
    print("Enter numbers separated by spaces:")
    try:
        data_str = input("> ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    try:
        nums = [parse_number(x) for x in data_str.split()]
    except Exception:
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
    if max_freq == 1:
        mode_str = "no mode (all values occur once)"
    elif len(modes) == len(freq):
        mode_str = "all values tied (no unique mode)"
    else:
        mode_str = ", ".join(str(m) for m in modes)
    range_val = max(nums) - min(nums)
    sample_variance = sum((x-mean)**2 for x in nums) / (n-1) if n > 1 else 0
    pop_variance = sum((x-mean)**2 for x in nums) / n if n > 0 else 0
    sample_std = math.sqrt(sample_variance)
    pop_std = math.sqrt(pop_variance)
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
    steps.append("Sample variance = {}".format(sample_variance))
    steps.append("Population variance = {}".format(pop_variance))
    steps.append("Sample std dev = {}".format(sample_std))
    steps.append("Population std dev = {}".format(pop_std))
    final = "Mean: {}, Median: {}, Mode: {}\nSample std dev: {}, Population std dev: {}".format(
        mean, median, mode_str, sample_std, pop_std)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "9", "Frequency Table Statistics")
def frequency_table_stats():
    UI.clear()
    print("Enter value and frequency pairs (space separated), e.g., '1 5 2 3' (value=1 freq=5, value=2 freq=3)")
    print("Enter all pairs: ")
    try:
        data = input("> ").split()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if len(data) % 2 != 0:
        print("Must have even number of entries.")
        UI.wait()
        return
    try:
        pairs = [(parse_number(data[i]), parse_number(data[i+1])) for i in range(0, len(data), 2)]
    except Exception:
        print("Invalid input.")
        UI.wait()
        return
    values = []
    for v, f in pairs:
        if f < 0 or f != int(f):
            print("Frequencies must be non-negative integers.")
            UI.wait()
            return
        for _ in range(int(f)):
            values.append(v)
    if not values:
        print("No data.")
        UI.wait()
        return
    n = len(values)
    mean = sum(values) / n
    sorted_vals = sorted(values)
    median = median_of_list(sorted_vals)
    freq_count = {}
    for v in values:
        freq_count[v] = freq_count.get(v, 0) + 1
    max_f = max(freq_count.values())
    modes = [k for k, v in freq_count.items() if v == max_f]
    if max_f == 1:
        mode_str = "no mode"
    elif len(modes) == len(freq_count):
        mode_str = "all tied"
    else:
        mode_str = ", ".join(str(m) for m in modes)
    steps = []
    steps.append("Values with frequencies: {}".format(pairs))
    steps.append("Expanded list ({} values): {}".format(n, values))
    steps.append("Mean = {}".format(mean))
    steps.append("Median = {}".format(median))
    steps.append("Mode = {}".format(mode_str))
    final = "Mean: {}, Median: {}, Mode: {}".format(mean, median, mode_str)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "10", "Box Plot Statistics")
def box_plot_stats():
    UI.clear()
    print("BOX PLOT STATISTICS (Five-number summary)")
    mn = UI.get_float("Minimum = ")
    q1 = UI.get_float("Q1 = ")
    med = UI.get_float("Median = ")
    q3 = UI.get_float("Q3 = ")
    mx = UI.get_float("Maximum = ")
    steps = []
    steps.append("Five-number summary: Min={}, Q1={}, Median={}, Q3={}, Max={}".format(mn, q1, med, q3, mx))
    iqr = q3 - q1
    range_val = mx - mn
    steps.append("IQR = Q3 - Q1 = {} - {} = {}".format(q3, q1, iqr))
    steps.append("Range = Max - Min = {} - {} = {}".format(mx, mn, range_val))
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    steps.append("Lower fence = Q1 - 1.5*IQR = {} - 1.5*{} = {}".format(q1, iqr, lower_fence))
    steps.append("Upper fence = Q3 + 1.5*IQR = {} + 1.5*{} = {}".format(q3, iqr, upper_fence))
    steps.append("Any data point below {} or above {} is an outlier.".format(lower_fence, upper_fence))
    final = "IQR = {}, Range = {}, Outlier boundaries: ({}, {})".format(iqr, range_val, lower_fence, upper_fence)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "11", "Line of Best Fit (Linear Regression)")
def best_fit_line():
    UI.clear()
    print("Enter points (x y) separated by spaces, e.g., '1 2 3 4 5 6' gives (1,2),(3,4),(5,6)")
    try:
        data = input("> ").split()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if len(data) % 2 != 0:
        print("Must have even number of entries.")
        UI.wait()
        return
    try:
        pts = [(parse_number(data[i]), parse_number(data[i+1])) for i in range(0, len(data), 2)]
    except Exception:
        print("Invalid input.")
        UI.wait()
        return
    if len(pts) < 2:
        print("Need at least 2 points.")
        UI.wait()
        return
    n = len(pts)
    sum_x = sum(p[0] for p in pts)
    sum_y = sum(p[1] for p in pts)
    sum_xy = sum(p[0]*p[1] for p in pts)
    sum_x2 = sum(p[0]*p[0] for p in pts)
    denom = n * sum_x2 - sum_x * sum_x
    if is_approx_zero(denom):
        print("Vertical line, cannot fit linear regression.")
        UI.wait()
        return
    slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y * sum_x2 - sum_x * sum_xy) / denom
    steps = []
    steps.append("Points: {}".format(pts))
    steps.append("n = {}".format(n))
    steps.append("Σx = {}, Σy = {}, Σxy = {}, Σx² = {}".format(sum_x, sum_y, sum_xy, sum_x2))
    steps.append("slope = (n*Σxy - Σx*Σy) / (n*Σx² - (Σx)²)")
    steps.append("= ({}*{} - {}*{}) / ({}*{} - {}²) = {}".format(n, sum_xy, sum_x, sum_y, n, sum_x2, sum_x, slope))
    steps.append("intercept = (Σy*Σx² - Σx*Σxy) / (n*Σx² - (Σx)²)")
    steps.append("= ({}*{} - {}*{}) / {} = {}".format(sum_y, sum_x2, sum_x, sum_xy, denom, intercept))
    final = "y = {}x + {}".format(slope, intercept)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "12", "Linear vs Exponential Models")
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
        if is_approx_zero(slope1 - slope2):
            steps.append("Slopes are equal → linear.")
            final = "Linear (constant slope)"
        else:
            if y1 != 0 and y2 != 0 and y3 != 0:
                if is_approx_zero((x2-x1) - (x3-x2)):
                    ratio1 = y2/y1
                    ratio2 = y3/y2
                    steps.append("Ratios: {} and {}".format(ratio1, ratio2))
                    if ratio1 <= 0 or ratio2 <= 0:
                        steps.append("Non-positive ratio → not a standard real exponential model.")
                        final = "Neither linear nor standard exponential (negative/zero ratio)"
                    elif is_approx_zero(ratio1 - ratio2):
                        steps.append("Ratios are positive and equal → exponential.")
                        final = "Exponential (constant positive ratio)"
                    else:
                        final = "Neither clearly linear nor exponential"
                else:
                    steps.append("x-values are not equally spaced; constant ratio does not guarantee exponential.")
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


@solver("Problem Solving", "13", "Scatterplot Interpretation")
def scatterplot_interpretation():
    UI.clear()
    print("SCATTERPLOT INTERPRETATION")
    print("Enter points (x y) separated by spaces, e.g., '1 2 3 4 5 6'")
    try:
        data = input("> ").split()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if len(data) % 2 != 0:
        print("Must have even number of entries.")
        UI.wait()
        return
    try:
        pts = [(parse_number(data[i]), parse_number(data[i+1])) for i in range(0, len(data), 2)]
    except Exception:
        print("Invalid input.")
        UI.wait()
        return
    if len(pts) < 2:
        print("Need at least 2 points.")
        UI.wait()
        return
    n = len(pts)
    sum_x = sum(p[0] for p in pts)
    sum_y = sum(p[1] for p in pts)
    sum_xy = sum(p[0]*p[1] for p in pts)
    sum_x2 = sum(p[0]*p[0] for p in pts)
    denom = n * sum_x2 - sum_x * sum_x
    if is_approx_zero(denom):
        print("Vertical trend; cannot compute correlation.")
        UI.wait()
        return
    slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y * sum_x2 - sum_x * sum_xy) / denom
    sum_y2 = sum(p[1]*p[1] for p in pts)
    r_num = n * sum_xy - sum_x * sum_y
    r_den = math.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
    r = r_num / r_den if r_den != 0 else 0
    steps = []
    steps.append("Points: {}".format(pts))
    steps.append("Line of best fit: y = {}x + {}".format(slope, intercept))
    steps.append("Correlation coefficient r = {}".format(r))
    if abs(r) > 0.7:
        corr = "strong"
    elif abs(r) > 0.3:
        corr = "moderate"
    else:
        corr = "weak"
    if r > 0:
        direction = "positive"
    elif r < 0:
        direction = "negative"
    else:
        direction = "no"
    steps.append("Interpretation: {} {} correlation".format(direction, corr))
    final = "Line: y = {}x + {}, r = {}".format(slope, intercept, r)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "14", "Surveys & Experiments")
def surveys_experiments():
    UI.clear()
    print("SURVEYS & EXPERIMENTS EVALUATOR")
    print("Answer questions to evaluate study design:")
    try:
        print("1. Was the sample random? (y/n)")
        rand = input("> ").strip().lower()
        print("2. Was there a control group? (y/n)")
        control = input("> ").strip().lower()
        print("3. Could there be bias? (y/n)")
        bias = input("> ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    steps = []
    steps.append("Sample random: {}".format(rand))
    steps.append("Control group: {}".format(control))
    steps.append("Possible bias: {}".format(bias))
    if rand == "y" and bias == "n":
        steps.append("Well-designed study, results likely generalizable.")
        final = "Good design"
    elif rand == "n" or bias == "y":
        steps.append("Potential issues: sample may not be representative, or bias may be present.")
        final = "Flawed design"
    else:
        steps.append("Mixed results; evaluate carefully.")
        final = "Inconclusive"
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "15", "Margin of Error")
def margin_of_error():
    UI.clear()
    print("MARGIN OF ERROR")
    print("Enter sample statistics:")
    sample_size = UI.get_positive_int("Sample size (n) = ")
    std_dev = UI.get_positive_float("Standard deviation (sigma) = ")
    while True:
        confidence = UI.get_float("Confidence level (as decimal, e.g., 0.95) = ")
        if 0 < confidence < 1:
            break
        print("Confidence must be between 0 and 1.")
    z_scores = {0.80: 1.28, 0.85: 1.44, 0.90: 1.645, 0.95: 1.96, 0.98: 2.33, 0.99: 2.576}
    z = z_scores.get(round(confidence, 2), 1.96)
    moe = z * std_dev / math.sqrt(sample_size)
    steps = []
    steps.append("n = {}, sigma = {}, confidence = {}".format(sample_size, std_dev, confidence))
    steps.append("Z-score = {}".format(z))
    steps.append("Margin of error = Z * sigma / sqrt(n) = {} * {} / sqrt({}) = {}".format(z, std_dev, sample_size, moe))
    final = "Margin of error = {}".format(moe)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "16", "Weighted Average")
def weighted_average():
    UI.clear()
    print("WEIGHTED AVERAGE")
    print("Enter values and weights as pairs: value weight, value weight, ...")
    try:
        data = input("> ").split()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if len(data) % 2 != 0:
        print("Must have even number of entries.")
        UI.wait()
        return
    try:
        pairs = [(parse_number(data[i]), parse_number(data[i+1])) for i in range(0, len(data), 2)]
    except Exception:
        print("Invalid input.")
        UI.wait()
        return
    total_weight = sum(w for _, w in pairs)
    if total_weight == 0:
        print("Sum of weights cannot be zero.")
        UI.wait()
        return
    weighted_sum = sum(v * w for v, w in pairs)
    avg = weighted_sum / total_weight
    steps = []
    steps.append("Pairs: {}".format(pairs))
    steps.append("Weighted sum = {}".format(weighted_sum))
    steps.append("Total weight = {}".format(total_weight))
    steps.append("Weighted average = {} / {} = {}".format(weighted_sum, total_weight, avg))
    final = "Weighted average = {}".format(avg)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Problem Solving", "17", "Data Table Analysis")
def data_table_analysis():
    UI.clear()
    print("DATA TABLE ANALYSIS")
    print("Enter table data as rows: for each row, enter values separated by spaces.")
    print("We'll compute column sums, means, and identify patterns.")
    rows = []
    print("Enter rows (empty line to finish):")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        if not line:
            break
        rows.append(line.split())
    if not rows:
        print("No data entered.")
        UI.wait()
        return
    data = []
    for r in rows:
        try:
            data.append([parse_number(x) for x in r])
        except Exception:
            data.append([x for x in r])
    steps = []
    steps.append("Table rows: {}".format(data))
    n_cols = len(data[0])
    equal_lengths = all(len(row) == n_cols for row in data)
    all_float = all(isinstance(x, float) for row in data for x in row)
    if equal_lengths and all_float:
        col_sums = [sum(row[i] for row in data) for i in range(n_cols)]
        col_means = [s / len(data) for s in col_sums]
        steps.append("Column sums: {}".format(col_sums))
        steps.append("Column means: {}".format(col_means))
        final = "Sums: {}, Means: {}".format(col_sums, col_means)
    else:
        final = "Non-numeric or uneven data; can't compute column sums."
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Geometry", "1", "Area (2D Shapes)")
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
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        l = UI.get_positive_float("length = ")
        w = UI.get_positive_float("width = ")
        steps = []
        steps.append("Area = length * width = {} * {} = {}".format(l, w, l*w))
        final = "Area = {}".format(l*w)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        s = UI.get_positive_float("side = ")
        steps = []
        steps.append("Area = side^2 = {}^2 = {}".format(s, s*s))
        final = "Area = {}".format(s*s)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        b = UI.get_positive_float("base = ")
        h = UI.get_positive_float("height = ")
        steps = []
        steps.append("Area = 1/2 * base * height = 0.5 * {} * {} = {}".format(b, h, 0.5*b*h))
        final = "Area = {}".format(0.5*b*h)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "4":
        b = UI.get_positive_float("base = ")
        h = UI.get_positive_float("height = ")
        steps = []
        steps.append("Area = base * height = {} * {} = {}".format(b, h, b*h))
        final = "Area = {}".format(b*h)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "5":
        b1 = UI.get_positive_float("base1 = ")
        b2 = UI.get_positive_float("base2 = ")
        h = UI.get_positive_float("height = ")
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
        if th < 0 or th > 360:
            print("Angle must be between 0 and 360 degrees.")
            UI.wait()
            return
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


@solver("Geometry", "2", "Volume (3D Shapes)")
def volume_menu():
    UI.clear()
    print("Volume Calculator")
    print("1. Prism")
    print("2. Cylinder")
    print("3. Cone")
    print("4. Sphere")
    print("5. Pyramid")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        B = UI.get_positive_float("base area = ")
        h = UI.get_positive_float("height = ")
        steps = []
        steps.append("Volume = base area * height = {} * {} = {}".format(B, h, B*h))
        final = "Volume = {}".format(B*h)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        r = UI.get_positive_float("radius = ")
        h = UI.get_positive_float("height = ")
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
        h = UI.get_positive_float("height = ")
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
        B = UI.get_positive_float("base area = ")
        h = UI.get_positive_float("height = ")
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


@solver("Geometry", "3", "Surface Area")
def surface_area_menu():
    UI.clear()
    print("Surface Area Calculator")
    print("1. Cube")
    print("2. Rectangular Prism")
    print("3. Cylinder")
    print("4. Cone")
    print("5. Sphere")
    print("6. Pyramid (square base)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        s = UI.get_positive_float("Side length = ")
        steps = []
        steps.append("Surface area = 6 * side² = 6 * {}² = {}".format(s, 6*s*s))
        final = "SA = {}".format(6*s*s)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        l = UI.get_positive_float("Length = ")
        w = UI.get_positive_float("Width = ")
        h = UI.get_positive_float("Height = ")
        steps = []
        steps.append("Surface area = 2(lw + wh + lh)")
        steps.append("= 2({}*{} + {}*{} + {}*{})".format(l, w, w, h, l, h))
        sa = 2*(l*w + w*h + l*h)
        steps.append("= 2({} + {} + {}) = {}".format(l*w, w*h, l*h, sa))
        final = "SA = {}".format(sa)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        r = UI.get_positive_float("Radius = ")
        h = UI.get_positive_float("Height = ")
        steps = []
        steps.append("Surface area = 2πr² + 2πrh")
        steps.append("= 2π*{}² + 2π*{}*{}".format(r, r, h))
        sa = 2*math.pi*r*r + 2*math.pi*r*h
        steps.append("≈ {}".format(sa))
        final = "SA = {}".format(sa)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "4":
        r = UI.get_positive_float("Radius = ")
        l = UI.get_positive_float("Slant height = ")
        steps = []
        steps.append("Surface area = πr² + πrl")
        steps.append("= π*{}² + π*{}*{}".format(r, r, l))
        sa = math.pi*r*r + math.pi*r*l
        steps.append("≈ {}".format(sa))
        final = "SA = {}".format(sa)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "5":
        r = UI.get_positive_float("Radius = ")
        steps = []
        steps.append("Surface area = 4πr² = 4π*{}²".format(r))
        sa = 4*math.pi*r*r
        steps.append("≈ {}".format(sa))
        final = "SA = {}".format(sa)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "6":
        base = UI.get_positive_float("Base side length = ")
        slant = UI.get_positive_float("Slant height = ")
        steps = []
        steps.append("Surface area = base_area + 4*(1/2*base*slant)")
        steps.append("= {}² + 2*{}*{}".format(base, base, slant))
        sa = base*base + 2*base*slant
        steps.append("= {}".format(sa))
        final = "SA = {}".format(sa)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()


@solver("Geometry", "4", "Coordinate Geometry")
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
    if x2 == x1 and y2 == y1:
        slope = "undefined"
        eq = "N/A"
        steps.append("Identical points → do not determine a unique line.")
    elif x2 - x1 == 0:
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


@solver("Geometry", "5", "Lines & Angles")
def lines_and_angles():
    UI.clear()
    print("Lines & Angles")
    print("1. Complementary/Supplementary")
    print("2. Parallel lines with transversal")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        a = UI.get_float("Given angle (degrees) = ")
        steps = []
        steps.append("Given angle: {}°".format(a))
        comp = 90 - a
        supp = 180 - a
        steps.append("Complement = 90 - {} = {}".format(a, comp))
        steps.append("Supplement = 180 - {} = {}".format(a, supp))
        final = "Complement: {}, Supplement: {}".format(comp, supp)
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


@solver("Geometry", "6", "Triangles")
def triangles():
    UI.clear()
    print("Triangles")
    print("1. Angle sum (180)")
    print("2. Exterior angle theorem")
    print("3. Similarity scale factor")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        a1 = UI.get_positive_float("Angle 1 = ")
        a2 = UI.get_positive_float("Angle 2 = ")
        if a1 + a2 >= 180:
            print("Sum of two angles must be less than 180°.")
            UI.wait()
            return
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
        r1 = UI.get_positive_float("Remote interior 1 = ")
        r2 = UI.get_positive_float("Remote interior 2 = ")
        if r1 + r2 >= 180:
            print("Sum of remote interior angles must be less than 180°.")
            UI.wait()
            return
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
        a1 = UI.get_positive_float("Side in triangle1 = ")
        a2 = UI.get_positive_float("Corresponding side in triangle2 = ")
        steps = []
        scale = a2 / a1
        steps.append("Scale factor = {} / {} = {}".format(a2, a1, scale))
        b1 = UI.get_positive_float("Another side in triangle1 = ")
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


@solver("Geometry", "7", "Right Triangles")
def right_triangles():
    UI.clear()
    print("Right Triangles")
    print("1. Pythagorean Theorem (find missing side)")
    print("2. Special right triangles (30-60-90, 45-45-90)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        print("1. Hypotenuse")
        print("2. Leg")
        try:
            sub = input("Choice: ")
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
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
        try:
            sub = input("Choice: ")
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
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


@solver("Geometry", "8", "Trigonometry (SOH-CAH-TOA)")
def trigonometry():
    UI.clear()
    print("Trigonometry (Right Triangle)")
    print("1. Find missing side (angle and side known)")
    print("2. Find missing angle (two sides known)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        print("Known: 1) hypotenuse, 2) leg")
        try:
            side_known = input("Which side is known? (hyp/leg): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        if side_known == "hyp":
            hyp = UI.get_positive_float("Hypotenuse = ")
            angle = UI.get_float("Angle (degrees) = ")
            if angle <= 0 or angle >= 90:
                print("Angle must be strictly between 0 and 90 degrees.")
                UI.wait()
                return
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
                print("Angle must be strictly between 0 and 90 degrees.")
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


@solver("Geometry", "9", "Circles")
def circles():
    UI.clear()
    print("Circles")
    print("1. Circumference & Area")
    print("2. Arc length & Sector area")
    print("3. Equation of circle (center-radius)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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
        if th < 0 or th > 360:
            print("Angle must be between 0 and 360 degrees.")
            UI.wait()
            return
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


@solver("Geometry", "10", "Circle Theorems")
def circle_theorems():
    UI.clear()
    print("Circle Theorems")
    print("1. Inscribed angle from intercepted arc")
    print("2. Central angle from inscribed angle")
    print("3. Arc measure from inscribed angle")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        arc = UI.get_positive_float("Intercepted arc measure (degrees) = ")
        steps = []
        steps.append("Inscribed angle = 1/2 * intercepted arc")
        angle = arc / 2
        steps.append("= 1/2 * {} = {}".format(arc, angle))
        final = "Inscribed angle = {}°".format(angle)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        inscribed = UI.get_float("Inscribed angle (degrees) = ")
        steps = []
        steps.append("Central angle = 2 * inscribed angle")
        central = 2 * inscribed
        steps.append("= 2 * {} = {}".format(inscribed, central))
        final = "Central angle = {}°".format(central)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        inscribed = UI.get_float("Inscribed angle (degrees) = ")
        steps = []
        steps.append("Intercepted arc = 2 * inscribed angle")
        arc = 2 * inscribed
        steps.append("= 2 * {} = {}".format(inscribed, arc))
        final = "Intercepted arc = {}°".format(arc)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()


@solver("Geometry", "11", "Unit Circle")
def unit_circle_values():
    UI.clear()
    print("UNIT CIRCLE EXACT VALUES")
    angle = UI.get_float("Enter angle in degrees: ")
    steps = []
    angle = angle % 360
    exact_sin_cos = {0: ("0","1"), 30: ("1/2", "√3/2"), 45: ("√2/2", "√2/2"),
                     60: ("√3/2", "1/2"), 90: ("1","0"), 180: ("0","-1"), 270: ("-1","0"), 360: ("0","1")}
    rad = math.radians(angle)
    sin_val = math.sin(rad)
    cos_val = math.cos(rad)
    tan_val = math.tan(rad) if abs(math.cos(rad)) > 1e-12 else None
    steps.append("Angle = {}°".format(angle))
    found_exact = False
    tan_exact = None
    for a, (s_exact, c_exact) in exact_sin_cos.items():
        if abs(angle - a) < 1e-9 or abs(angle - a - 360) < 1e-9:
            steps.append("Exact values: sin = {}, cos = {}".format(s_exact, c_exact))
            if tan_val is not None:
                if a in (0, 180, 360): tan_exact = "0"
                elif a == 45: tan_exact = "1"
                elif a == 30: tan_exact = "√3/3"
                elif a == 60: tan_exact = "√3"
                elif a in (90, 270): tan_exact = "undefined"
                if tan_exact:
                    steps.append("Exact tan = {}".format(tan_exact))
                else:
                    steps.append("tan ≈ {}".format(tan_val))
            else:
                steps.append("tan is undefined")
            final = "sin = {}, cos = {}, tan = {}".format(s_exact, c_exact, tan_exact if tan_exact else "undefined")
            found_exact = True
            break
    if not found_exact:
        steps.append("No exact surd for this angle (use approx values)")
        steps.append("sin ≈ {}, cos ≈ {}, tan ≈ {}".format(sin_val, cos_val, tan_val))
        final = "sin ≈ {}, cos ≈ {}, tan ≈ {}".format(sin_val, cos_val, tan_val)
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Geometry", "12", "Law of Sines")
def law_of_sines():
    UI.clear()
    print("LAW OF SINES")
    print("Given angle A, angle B, side a opposite A, find side b")
    A = UI.get_float("Angle A (deg) = ")
    B = UI.get_float("Angle B (deg) = ")
    a = UI.get_positive_float("Side a = ")
    if A <= 0 or A >= 180:
        print("Angle A must be strictly between 0 and 180 degrees.")
        UI.wait()
        return
    if B <= 0 or B >= 180:
        print("Angle B must be strictly between 0 and 180 degrees.")
        UI.wait()
        return
    if A + B >= 180:
        print("A + B must be less than 180°.")
        UI.wait()
        return
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
        print("sin(A) cannot be zero.")
    UI.wait()


@solver("Geometry", "13", "Law of Cosines")
def law_of_cosines():
    UI.clear()
    print("LAW OF COSINES")
    print("1. SAS (two sides and included angle)")
    print("2. SSS (three sides to find angle)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        a = UI.get_positive_float("side a = ")
        b = UI.get_positive_float("side b = ")
        C = UI.get_float("included angle C (deg) = ")
        if C <= 0 or C >= 180:
            print("Angle C must be strictly between 0 and 180 degrees.")
            UI.wait()
            return
        radicand = a**2 + b**2 - 2*a*b*math.cos(math.radians(C))
        if radicand < 0:
            print("Invalid input (radicand negative).")
            UI.wait()
            return
        steps = []
        steps.append("Law of Cosines: c² = a² + b² - 2ab cos(C)")
        steps.append("c² = {}² + {}² - 2*{}*{}*cos({})".format(a, b, a, b, C))
        c = math.sqrt(radicand)
        steps.append("= {} + {} - {} = {}".format(a**2, b**2, 2*a*b*math.cos(math.radians(C)), c**2))
        steps.append("c = √{} = {}".format(c**2, c))
        final = "Side c = {}".format(c)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        a = UI.get_positive_float("side a = ")
        b = UI.get_positive_float("side b = ")
        c = UI.get_positive_float("side c = ")
        if not (a + b > c and a + c > b and b + c > a):
            print("Sides do not form a valid (non-degenerate) triangle.")
            UI.wait()
            return
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
    UI.wait()


@solver("Geometry", "14", "Heron's Formula")
def herons_formula():
    UI.clear()
    print("HERON'S FORMULA (Triangle area given 3 sides)")
    a = UI.get_positive_float("side a = ")
    b = UI.get_positive_float("side b = ")
    c = UI.get_positive_float("side c = ")
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


@solver("Geometry", "15", "3D Distance")
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


@solver("Geometry", "16", "Similar Figures")
def similar_figures():
    UI.clear()
    print("SIMILAR FIGURES")
    print("Given two similar figures, find scale factor or missing side.")
    print("1. Find scale factor from two corresponding sides")
    print("2. Find missing side using scale factor")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        s1 = UI.get_positive_float("Side in figure 1 = ")
        s2 = UI.get_positive_float("Corresponding side in figure 2 = ")
        scale = s2 / s1
        steps = []
        steps.append("Scale factor = {} / {} = {}".format(s2, s1, scale))
        final = "Scale factor (figure1 to figure2) = {}".format(scale)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "2":
        s1 = UI.get_positive_float("Side in figure 1 = ")
        scale = UI.get_nonzero_float("Scale factor (1 to 2) = ")
        s2 = s1 * scale
        steps = []
        steps.append("Side in figure 2 = {} * {} = {}".format(s1, scale, s2))
        final = "Corresponding side in figure 2 = {}".format(s2)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()


@solver("Geometry", "17", "Congruence")
def congruence():
    UI.clear()
    print("CONGRUENCE")
    print("Check if two triangles are congruent based on side lengths (SSS).")
    a1 = UI.get_positive_float("Side a1 = ")
    b1 = UI.get_positive_float("Side b1 = ")
    c1 = UI.get_positive_float("Side c1 = ")
    a2 = UI.get_positive_float("Side a2 = ")
    b2 = UI.get_positive_float("Side b2 = ")
    c2 = UI.get_positive_float("Side c2 = ")
    steps = []
    steps.append("Triangle1 sides: ({}, {}, {})".format(a1, b1, c1))
    steps.append("Triangle2 sides: ({}, {}, {})".format(a2, b2, c2))
    s1 = sorted([a1, b1, c1])
    s2 = sorted([a2, b2, c2])
    if s1 == s2:
        steps.append("All corresponding sides are equal → SSS congruence.")
        final = "Congruent (SSS)"
    else:
        steps.append("Sides not equal; could be congruent by other criteria, but this is SSS only.")
        final = "Not congruent by SSS"
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Geometry", "18", "Transformations (Geometry)")
def transformations_geometry():
    UI.clear()
    print("GEOMETRIC TRANSFORMATIONS")
    print("Apply transformations to a point.")
    x = UI.get_float("Enter x coordinate: ")
    y = UI.get_float("Enter y coordinate: ")
    steps = []
    steps.append("Original point: ({}, {})".format(x, y))
    print("Choose transformation:")
    print("1. Reflection over x-axis")
    print("2. Reflection over y-axis")
    print("3. Reflection over y=x")
    print("4. Rotation 90° counterclockwise")
    print("5. Rotation 180°")
    print("6. Rotation 270° counterclockwise")
    print("7. Translation (dx, dy)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        new = (x, -y)
        steps.append("Reflect over x-axis → ({}, {})".format(new[0], new[1]))
        final = "Reflected point: ({}, {})".format(new[0], new[1])
    elif ch == "2":
        new = (-x, y)
        steps.append("Reflect over y-axis → ({}, {})".format(new[0], new[1]))
        final = "Reflected point: ({}, {})".format(new[0], new[1])
    elif ch == "3":
        new = (y, x)
        steps.append("Reflect over y=x → ({}, {})".format(new[0], new[1]))
        final = "Reflected point: ({}, {})".format(new[0], new[1])
    elif ch == "4":
        new = (-y, x)
        steps.append("Rotate 90° CCW → ({}, {})".format(new[0], new[1]))
        final = "Rotated point: ({}, {})".format(new[0], new[1])
    elif ch == "5":
        new = (-x, -y)
        steps.append("Rotate 180° → ({}, {})".format(new[0], new[1]))
        final = "Rotated point: ({}, {})".format(new[0], new[1])
    elif ch == "6":
        new = (y, -x)
        steps.append("Rotate 270° CCW → ({}, {})".format(new[0], new[1]))
        final = "Rotated point: ({}, {})".format(new[0], new[1])
    elif ch == "7":
        dx = UI.get_float("dx = ")
        dy = UI.get_float("dy = ")
        new = (x + dx, y + dy)
        steps.append("Translate by ({}, {}) → ({}, {})".format(dx, dy, new[0], new[1]))
        final = "Translated point: ({}, {})".format(new[0], new[1])
    else:
        print("Invalid choice.")
        UI.wait()
        return
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Additional Topics", "1", "Complex Numbers")
def complex_numbers():
    UI.clear()
    print("COMPLEX NUMBERS (a+bi)")
    print("1. Add / Subtract")
    print("2. Multiply")
    print("3. Divide")
    print("4. Modulus & Conjugate")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    a1 = UI.get_float("a1 = ")
    b1 = UI.get_float("b1 = ")
    a2 = b2 = 0
    if ch != "4":
        a2 = UI.get_float("a2 = ")
        b2 = UI.get_float("b2 = ")
    if ch == "1":
        try:
            s = input("Add (+) or Subtract (-): ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        if s not in ("+", "-"):
            print("Operator must be + or -.")
            UI.wait()
            return
        steps = []
        if s == "+":
            real = a1 + a2
            imag = b1 + b2
            steps.append("({} + {}i) + ({} + {}i) = ({} + {}) + ({} + {})i".format(a1, b1, a2, b2, a1, a2, b1, b2))
            steps.append("= {} + {}i".format(real, imag))
            final = "Result: {} + {}i".format(real, imag)
        else:
            real = a1 - a2
            imag = b1 - b2
            steps.append("({} + {}i) - ({} + {}i) = ({} - {}) + ({} - {})i".format(a1, b1, a2, b2, a1, a2, b1, b2))
            steps.append("= {} + {}i".format(real, imag))
            final = "Result: {} + {}i".format(real, imag)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
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
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
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
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "4":
        mod = math.sqrt(a1**2 + b1**2)
        steps = []
        steps.append("Modulus = √({}² + {}²) = √{} = {}".format(a1, b1, a1**2 + b1**2, mod))
        steps.append("Conjugate = {} - {}i".format(a1, b1))
        final = "Modulus: {}, Conjugate: {} - {}i".format(mod, a1, b1)
        for i, s_step in enumerate(steps, 1):
            print("Step {}: {}".format(i, s_step))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()


@solver("Additional Topics", "2", "Sequences & Series")
def sequences_series():
    UI.clear()
    print("SEQUENCES & SERIES")
    print("1. Arithmetic: nth term & sum")
    print("2. Geometric: nth term & sum (finite/infinite)")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        a1 = UI.get_float("first term a1 = ")
        d = UI.get_float("common difference d = ")
        n = UI.get_positive_int("n = ")
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
        n = UI.get_positive_int("n = ")
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
            steps.append("|r| >= 1 → no finite infinite sum.")
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    else:
        print("Invalid choice.")
    UI.wait()


@solver("Additional Topics", "3", "Combinatorics")
def combinatorics():
    UI.clear()
    print("COUNTING & PROBABILITY")
    print("1. Factorial n!")
    print("2. Permutations nPr")
    print("3. Combinations nCr")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        n = UI.get_nonnegative_int("n = ")
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
        n = UI.get_nonnegative_int("n = ")
        r = UI.get_nonnegative_int("r = ")
        if r > n:
            print("r must be <= n.")
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
        n = UI.get_nonnegative_int("n = ")
        r = UI.get_nonnegative_int("r = ")
        if r > n:
            print("r must be <= n.")
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


@solver("Additional Topics", "4", "Binomial Theorem")
def binomial_theorem():
    UI.clear()
    print("BINOMIAL THEOREM")
    print("Find specific term in (a+b)^n")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    n = UI.get_nonnegative_int("n = ")
    k = UI.get_int("k (0-indexed term number) = ")
    if k < 0 or k > n:
        print("Invalid k (must satisfy 0 <= k <= n).")
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


@solver("Additional Topics", "5", "Matrices (2×2)")
def matrices():
    UI.clear()
    print("MATRICES (2x2)")
    print("1. Determinant")
    print("2. Inverse")
    print("3. Solve system using matrices")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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


@solver("Additional Topics", "6", "Vectors")
def vectors():
    UI.clear()
    print("VECTORS")
    print("1. Magnitude")
    print("2. Dot product")
    print("3. Angle between")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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


@solver("Additional Topics", "7", "Radian/Degree Converter")
def radian_degree():
    UI.clear()
    print("RADIAN <-> DEGREE CONVERTER")
    print("1. Radians to Degrees")
    print("2. Degrees to Radians")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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


@solver("Additional Topics", "8", "Conic Sections")
def conic_sections():
    UI.clear()
    print("CONIC SECTIONS")
    print("Identify conic from equation in general form.")
    print("General form: Ax² + By² + Cx + Dy + E = 0")
    A = UI.get_float("A = ")
    B = UI.get_float("B = ")
    C = UI.get_float("C = ")
    D = UI.get_float("D = ")
    E = UI.get_float("E = ")
    steps = []
    steps.append("Equation: {}x² + {}y² + {}x + {}y + {} = 0".format(A, B, C, D, E))
    if A == 0 and B == 0:
        steps.append("Not a conic (linear or degenerate).")
        final = "Not a conic"
    elif A == B:
        steps.append("Circle (A=B).")
        final = "Circle"
    elif A != 0 and B != 0:
        if (A > 0 and B > 0) or (A < 0 and B < 0):
            steps.append("Ellipse (A and B have same sign).")
            final = "Ellipse"
        else:
            steps.append("Hyperbola (A and B have opposite signs).")
            final = "Hyperbola"
    elif A == 0 or B == 0:
        steps.append("Parabola (one quadratic term).")
        final = "Parabola"
    else:
        steps.append("Unclear; need more information.")
        final = "Unknown"
    for i, s in enumerate(steps, 1):
        print("Step {}: {}".format(i, s))
    print("\n" + "─" * 40)
    print("Final answer: {}".format(final))
    UI.wait()


@solver("Utilities", "1", "Prime Factorization")
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
        d += 1 if d == 2 else 2
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


@solver("Utilities", "2", "GCF")
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


@solver("Utilities", "3", "LCM")
def lcm():
    UI.clear()
    a = UI.get_int("First number: ")
    b = UI.get_int("Second number: ")
    if a == 0 and b == 0:
        steps = []
        steps.append("lcm(0, 0) is undefined (all positive integers are common multiples).")
        final = "Undefined"
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
        UI.wait()
        return
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


@solver("Utilities", "4", "Fraction/Decimal/Percent Conversions")
def frac_dec_percent():
    UI.clear()
    print("1. Fraction -> Decimal")
    print("2. Decimal -> Fraction (approx)")
    print("3. Decimal -> Percent")
    print("4. Percent -> Decimal")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
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
        if not is_finite_number(dec):
            print("Non-finite input.")
            UI.wait()
            return
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
        best_num //= g
        best_den //= g
        if best_den < 0:
            best_num = -best_num
            best_den = -best_den
        steps = []
        steps.append("Searching for fraction approximation of {}".format(dec))
        steps.append("Best match: {}/{} ≈ {}".format(best_num, best_den, best_num/best_den))
        final = "{}/{}".format(best_num, best_den)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "3":
        d = UI.get_float("Decimal = ")
        steps = []
        steps.append("{} * 100 = {}%".format(d, d*100))
        final = "{}%".format(d*100)
        for i, s in enumerate(steps, 1):
            print("Step {}: {}".format(i, s))
        print("\n" + "─" * 40)
        print("Final answer: {}".format(final))
    elif ch == "4":
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


@solver("Utilities", "5", "Scientific Notation")
def scientific_notation():
    UI.clear()
    print("1. Standard to Scientific")
    print("2. Scientific to Standard")
    try:
        ch = input("Choice: ")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit
    if ch == "1":
        num = UI.get_float("Number = ")
        if not is_finite_number(num):
            print("Non-finite input.")
            UI.wait()
            return
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
        try:
            result = mantissa * (10**exponent)
        except OverflowError:
            print("Result overflows.")
            UI.wait()
            return
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


FORMULA_REFERENCE = {
    "Slope": {"formula": "m = (y2 - y1) / (x2 - x1)", "vars": "m: slope, (x1,y1) and (x2,y2): two points", "use": "Find slope of a line through two points.", "example": "(1,2) and (3,6) -> m = (6-2)/(3-1) = 4/2 = 2"},
    "Slope-Intercept Form": {"formula": "y = mx + b", "vars": "m: slope, b: y-intercept", "use": "Equation of a line.", "example": "m=2, b=3 -> y = 2x + 3"},
    "Point-Slope Form": {"formula": "y - y1 = m(x - x1)", "vars": "m: slope, (x1,y1): point on line", "use": "Line equation given slope and a point.", "example": "m=3, point (2,1) -> y - 1 = 3(x - 2)"},
    "Distance Formula": {"formula": "d = sqrt((x2-x1)^2 + (y2-y1)^2)", "vars": "(x1,y1), (x2,y2): two points", "use": "Distance between two points.", "example": "(0,0) and (3,4) -> d = sqrt(9+16) = 5"},
    "Midpoint": {"formula": "M = ((x1+x2)/2, (y1+y2)/2)", "vars": "Midpoint coordinates.", "use": "Find midpoint of a segment.", "example": "(2,3) and (4,7) -> M = (3,5)"},
    "Quadratic Formula": {"formula": "x = (-b +/- sqrt(b^2 - 4ac)) / (2a)", "vars": "a, b, c coefficients of ax^2+bx+c=0", "use": "Solve any quadratic equation.", "example": "x^2-5x+6=0 -> a=1,b=-5,c=6 -> disc=1 -> x=3 or 2"},
    "Discriminant": {"formula": "D = b^2 - 4ac", "vars": "D < 0: no real solutions; D = 0: one real; D > 0: two real", "use": "Determines number of real solutions of a quadratic.", "example": "x^2+1=0 -> D=-4 -> no real solutions"},
    "Pythagorean Theorem": {"formula": "a^2 + b^2 = c^2", "vars": "a, b: legs; c: hypotenuse", "use": "Right triangle side calculations.", "example": "a=3, b=4 -> c^2=25 -> c=5"},
    "Area of Circle": {"formula": "A = pi * r^2", "vars": "r: radius", "use": "Area of a circle.", "example": "r=5 -> A=25pi ~ 78.54"},
    "Circumference": {"formula": "C = 2 * pi * r", "vars": "r: radius", "use": "Circumference of a circle.", "example": "r=7 -> C=14pi ~ 43.98"},
    "Volume of Sphere": {"formula": "V = (4/3) * pi * r^3", "vars": "r: radius", "use": "Volume of a sphere.", "example": "r=3 -> V=36pi ~ 113.1"},
    "SOH-CAH-TOA": {"formula": "sin = opp/hyp, cos = adj/hyp, tan = opp/adj", "vars": "opposite, adjacent, hypotenuse sides relative to angle", "use": "Right triangle trigonometry.", "example": "sin(30 deg)=0.5"},
    "Arc Length": {"formula": "L = (theta/360) * 2 * pi * r   (theta in degrees)", "vars": "theta: central angle, r: radius", "use": "Length of an arc.", "example": "theta=90 deg, r=4 -> L = (90/360)*8pi = 2pi ~ 6.28"},
    "Sector Area": {"formula": "A = (theta/360) * pi * r^2", "vars": "theta: central angle, r: radius", "use": "Area of a sector.", "example": "theta=60 deg, r=6 -> A = (60/360)*36pi = 6pi ~ 18.85"},
    "Compound Interest": {"formula": "A = P(1 + r/n)^(nt)", "vars": "P: principal, r: annual rate, n: times per year, t: years", "use": "Value of an investment with compound interest.", "example": "P=1000, r=0.05, n=12, t=10 -> A ~ 1647.01"},
    "Exponential Growth/Decay": {"formula": "y = a * b^x   (b>1 growth, 0<b<1 decay)", "vars": "a: initial amount, b: growth/decay factor", "use": "Model exponential change.", "example": "y = 100 * 2^x -> doubles each step"},
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
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
        except Exception:
            print("Invalid input.")
            UI.wait()
            continue
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
    print("- 85+ solvers & utilities")
    print("- Searchable solver index with interactive selection")
    print("")
    print("Version: 1.5")
    print("License: GPL 3.0")
    print("Author: cheeseburgerjr")
    print("")
    print("Made for students, by a student.")
    UI.wait()


def main_menu():
    while True:
        UI.clear()
        print("="*30)
        print("      SAT Math Solver      ")
        print("="*30)
        categories = SolverRegistry.get_categories()
        for idx, cat in enumerate(categories, 1):
            print("{}. {}".format(idx, cat))
        print("{}. Exit".format(len(categories)+1))
        print("S. Search solvers by keyword")
        try:
            choice = input("Enter choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit
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
                    try:
                        sub_choice = input("Choice: ")
                    except (EOFError, KeyboardInterrupt):
                        raise SystemExit
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
