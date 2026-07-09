"""
SAT Math Solver for HP Prime G2 (MicroPython)
Copyright (C) 2026 (cheeseburgerjr)
License: GPLv3
Covers all Digital SAT Math topics.
"""

import math

# ----------------------------------------------------------------------
# UTILITY FUNCTIONS (Math)
# ----------------------------------------------------------------------
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
    coeff = a - c
    const = d - b
    print("\nStep-by-step:")
    UI.show_step("Original", "{}x + {} = {}x + {}".format(a, b, c, d))
    UI.show_step("Subtract cx", "({})x + {} = {}".format(a-c, b, d))
    UI.show_step("Subtract b", "({})x = {}".format(a-c, d - b))
    if coeff == 0:
        if const == 0:
            print("Infinite solutions (identity).")
        else:
            print("No solution (contradiction).")
    else:
        x = const / coeff
        UI.show_step("Divide", "x = {} / {} = {}".format(const, coeff, x))
        print("\nFinal answer: x = {}".format(x))
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
        if x2 - x1 == 0:
            print("Vertical line (undefined slope). x-intercept = {}".format(x1))
            UI.wait()
            return
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        print("\nSlope m = ({} - {}) / ({} - {}) = {}".format(y2, y1, x2, x1, m))
        print("Equation: y = {}x + {}".format(m, b))
        if m != 0:
            print("x-intercept: x = {}".format(-b/m))
        else:
            print("Horizontal line, no x-intercept (unless b=0 then all x)")
        print("y-intercept: (0, {})".format(b))
    elif ch == "2":
        m = UI.get_float("m = ")
        b = UI.get_float("b = ")
        print("Equation: y = {}x + {}".format(m, b))
        if m != 0:
            print("x-intercept: x = {}".format(-b/m))
        else:
            print("Horizontal line (m=0).")
        print("y-intercept: (0, {})".format(b))
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
    det = a1*b2 - a2*b1
    if det == 0:
        if a1*c2 == a2*c1 and b1*c2 == b2*c1:
            print("Infinite solutions (dependent equations).")
        else:
            print("No solution (inconsistent).")
    else:
        x = (c1*b2 - c2*b1) / det
        y = (a1*c2 - a2*c1) / det
        print("\nUsing Cramer's rule:")
        UI.show_step("Determinant", det)
        UI.show_step("x", "({}*{} - {}*{}) / {} = {}".format(c1, b2, c2, b1, det, x))
        UI.show_step("y", "({}*{} - {}*{}) / {} = {}".format(a1, c2, a2, c1, det, y))
        print("\nSolution: x = {}, y = {}".format(x, y))
    UI.wait()

@solver("Heart of Algebra", "4", "Linear Inequalities (one variable)")
def solve_linear_inequality():
    UI.clear()
    print("Solve linear inequality: ax + b < c   (or >, <=, >=)")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    op = input("Operator (<, >, <=, >=): ").strip()
    if a == 0:
        print("Not a linear inequality (a=0).")
        UI.wait()
        return
    rhs = c - b
    if a < 0:
        flip = {"<":">", ">":"<", "<=":">=", ">=":"<="}
        op = flip.get(op, op)
    x_bound = rhs / a
    print("\nStep-by-step:")
    UI.show_step("Original", "{}x + {} {} {}".format(a, b, op, c))
    UI.show_step("Isolate ax", "{}x {} {} = {}".format(a, op, c - b, rhs))
    UI.show_step("Divide by a", "x {} {}".format(op, x_bound))
    if a > 0:
        print("\nSolution: x {} {}".format(op, x_bound))
    else:
        print("\nSolution: x {} {}   (inequality flipped because a<0)".format(op, x_bound))
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
        fx = m*x + b
        print("\nf({}) = {}*{} + {} = {}".format(x, m, x, b, fx))
    elif ch == "2":
        y = UI.get_float("f(x) = ")
        if m == 0:
            if y == b:
                print("All x are solutions.")
            else:
                print("No solution.")
        else:
            x = (y - b) / m
            print("\nSolving {}x + {} = {}".format(m, b, y))
            print("{}x = {}".format(m, y - b))
            print("x = {}".format(x))
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
    print("This demo expands (ax+b)(cx+d) or factors x^2+px+q.")
    print("1. Expand (ax+b)(cx+d)")
    print("2. Factor x^2 + px + q")
    ch = input("Choice: ")
    if ch == "1":
        a = UI.get_float("a = ")
        b = UI.get_float("b = ")
        c = UI.get_float("c = ")
        d = UI.get_float("d = ")
        ac = a*c
        ad_bc = a*d + b*c
        bd = b*d
        print("\nExpanded: ({}x+{})({}x+{}) = {}x^2 + {}x + {}".format(a, b, c, d, ac, ad_bc, bd))
    elif ch == "2":
        p = UI.get_float("p = ")
        q = UI.get_float("q = ")
        disc = p*p - 4*q
        if disc < 0:
            print("Cannot factor over real numbers.")
        else:
            sqrt_disc = math.sqrt(disc)
            r1 = (-p + sqrt_disc)/2
            r2 = (-p - sqrt_disc)/2
            print("\nFactored: (x - {})(x - {})   (if exact roots are integers)".format(r1, r2))
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
    disc = b*b - 4*a*c
    print("\nDiscriminant D = {}".format(disc))
    if disc < 0:
        print("No real solutions.")
    elif disc == 0:
        print("One real solution (double root): x = {}".format(-b/(2*a)))
    else:
        sqrt_disc = math.sqrt(disc)
        x1 = (-b + sqrt_disc)/(2*a)
        x2 = (-b - sqrt_disc)/(2*a)
        print("Two real solutions: x1 = {}, x2 = {}".format(x1, x2))
    UI.wait()

@solver("Advanced Math", "3", "Parabolas (vertex, intercepts)")
def parabola_analysis():
    UI.clear()
    print("Parabola: y = ax^2 + bx + c")
    a = UI.get_nonzero_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    h = -b/(2*a)
    k = a*h*h + b*h + c
    print("\nVertex: ({}, {})".format(h, k))
    print("Axis of symmetry: x = {}".format(h))
    print("Opens {} -> {} value = {}".format('up' if a>0 else 'down',
                                             'minimum' if a>0 else 'maximum', k))
    disc = b*b - 4*a*c
    if disc >= 0:
        sq = math.sqrt(disc)
        x1 = (-b + sq)/(2*a)
        x2 = (-b - sq)/(2*a)
        print("x-intercepts: {}, {}".format(x1, x2))
    else:
        print("No x-intercepts.")
    print("y-intercept: (0, {})".format(c))
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
        A = a
        B = b - m
        C = c - b_line
        disc = B*B - 4*A*C
        if disc < 0:
            print("No intersection.")
        elif disc == 0:
            x = -B/(2*A)
            y = m*x + b_line
            print("Tangent at ({}, {})".format(x, y))
        else:
            sq = math.sqrt(disc)
            x1 = (-B + sq)/(2*A)
            y1 = m*x1 + b_line
            x2 = (-B - sq)/(2*A)
            y2 = m*x2 + b_line
            print("Intersections: ({}, {}) and ({}, {})".format(x1, y1, x2, y2))
    elif ch == "2":
        r = UI.get_positive_float("Radius r = ")
        m = UI.get_float("Line slope m = ")
        b_line = UI.get_float("Line y-intercept b = ")
        A = 1 + m*m
        B = 2*m*b_line
        C = b_line*b_line - r*r
        disc = B*B - 4*A*C
        if disc < 0:
            print("No intersection.")
        elif disc == 0:
            x = -B/(2*A)
            y = m*x + b_line
            print("Tangent at ({}, {})".format(x, y))
        else:
            sq = math.sqrt(disc)
            x1 = (-B + sq)/(2*A)
            y1 = m*x1 + b_line
            x2 = (-B - sq)/(2*A)
            y2 = m*x2 + b_line
            print("Intersections: ({}, {}) and ({}, {})".format(x1, y1, x2, y2))
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
        y = a * (b ** x)
        print("\ny = {} * {}^{} = {}".format(a, b, x, y))
    elif ch == "2":
        P = UI.get_float("Principal P = ")
        r = UI.get_float("Annual rate (as decimal) r = ")
        n = UI.get_float("Compounded per year n = ")
        t = UI.get_float("Time (years) t = ")
        A = P * (1 + r/n) ** (n*t)
        print("\nA = {} * (1 + {}/{})^{}*{} = {}".format(P, r, n, n, t, A))
    elif ch == "3":
        print("1. Half-life (decay)")
        print("2. Doubling time (growth)")
        sub = input("Choice: ")
        if sub == "1":
            init = UI.get_float("Initial amount = ")
            hl = UI.get_positive_float("Half-life = ")
            time = UI.get_float("Time elapsed = ")
            remaining = init * (0.5 ** (time / hl))
            print("Remaining = {} * (1/2)^({}/{}) = {}".format(init, time, hl, remaining))
        elif sub == "2":
            init = UI.get_float("Initial amount = ")
            dt = UI.get_positive_float("Doubling time = ")
            time = UI.get_float("Time elapsed = ")
            final = init * (2 ** (time / dt))
            print("Final = {} * 2^({}/{}) = {}".format(init, time, dt, final))
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
        disc = b*b - 4*a*c
        if disc < 0:
            print("No real roots.")
        else:
            sq = math.sqrt(disc)
            r1 = (-b + sq)/(2*a)
            r2 = (-b - sq)/(2*a)
            print("Roots: {}, {}".format(r1, r2))
    elif ch == "2":
        a = UI.get_float("a = ")
        b = UI.get_float("b = ")
        c = UI.get_float("c = ")
        d = UI.get_float("d = ")
        print("Trying integer root candidates (divisors of constant term)...")
        found = False
        d_int = int(round(d))
        if abs(d - d_int) > 1e-9:
            print("Constant term not integer; skipping integer root test.")
        else:
            max_div = int(math.sqrt(abs(d_int))) + 1 if abs(d_int) > 0 else 1
            for sign in [1, -1]:
                for num in range(1, max_div + 1):
                    if d_int % num == 0:
                        x = sign * num
                        val = a*x**3 + b*x**2 + c*x + d
                        if abs(val) < 1e-9:
                            print("Found root: x = {}".format(x))
                            found = True
                            break
                    if found:
                        break
        if not found:
            print("No easy integer root found.")
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
    if c == 0:
        print("Not a rational function (denominator constant).")
    else:
        vertical = -d / c
        horizontal = a / c
        print("\nVertical asymptote: x = {}".format(vertical))
        print("Horizontal asymptote: y = {}".format(horizontal))
        print("Domain: all real x except {}".format(vertical))
    UI.wait()

@solver("Advanced Math", "8", "Radical Equations")
def solve_radical_equation():
    UI.clear()
    print("Solve sqrt(ax + b) = cx + d")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    d = UI.get_float("d = ")
    A = c*c
    B = 2*c*d - a
    C = d*d - b
    print("Squaring both sides gives quadratic:")
    print("  {}x^2 + {}x + {} = 0".format(A, B, C))
    if A == 0:
        if B == 0:
            if abs(C) < 1e-12:
                print("All x are solutions (if domain allows).")
            else:
                print("No solution.")
        else:
            x = -C / B
            if a*x + b >= 0 and c*x + d >= 0:
                left = math.sqrt(a*x + b)
                right = c*x + d
                if abs(left - right) < 1e-9:
                    print("Valid solution: x = {}".format(x))
                else:
                    print("Candidate x = {} is extraneous. No solution.".format(x))
            else:
                print("x = {} invalid (domain).".format(x))
    else:
        disc = B*B - 4*A*C
        if disc < 0:
            print("No real solutions.")
        else:
            sq = math.sqrt(disc)
            x1 = (-B + sq)/(2*A)
            x2 = (-B - sq)/(2*A)
            sols = []
            for x in [x1, x2]:
                if a*x + b >= 0 and c*x + d >= 0:
                    left = math.sqrt(a*x + b)
                    right = c*x + d
                    if abs(left - right) < 1e-9:
                        sols.append(x)
                    else:
                        print("x = {} is extraneous (left={}, right={})".format(x, left, right))
                else:
                    print("x = {} invalid (domain).".format(x))
            if sols:
                print("Valid solutions: {}".format(sols))
            else:
                print("No valid solutions after checking.")
    UI.wait()

@solver("Advanced Math", "9", "Absolute Value Equations")
def solve_absolute_value():
    UI.clear()
    print("Solve |ax + b| = c")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    if a == 0:
        if c < 0:
            print("No solution (absolute value cannot equal negative).")
        elif c == 0:
            if b == 0:
                print("All real x are solutions (|0| = 0).")
            else:
                print("No solution (|{}| != 0).".format(b))
        else:
            if abs(b) == c:
                print("All real x are solutions (|{}| = {}).".format(b, c))
            else:
                print("No solution (|{}| != {}).".format(b, c))
        UI.wait()
        return

    if c < 0:
        print("No solution (absolute value cannot equal negative).")
    elif c == 0:
        print("Solution: x = {}".format(-b / a))
    else:
        x1 = (c - b) / a
        x2 = (-c - b) / a
        print("\nTwo cases:")
        print("  {}x+{} = {}  -> x = {}".format(a, b, c, x1))
        print("  {}x+{} = -{} -> x = {}".format(a, b, c, x2))
        print("\nSolutions: x = {}, x = {}".format(x1, x2))
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
        if b == 0:
            print("Denominator cannot be zero.")
        elif a == 0:
            print("a cannot be zero (would imply infinite or no solution).")
        else:
            x = (c * b) / a
            print("\n{}/{} = {}/x  => x = {}*{}/{} = {}".format(a, b, c, c, b, a, x))
    elif ch == "2":
        total_qty = UI.get_float("Total quantity = ")
        total_units = UI.get_float("Total units = ")
        if total_units == 0:
            print("Units cannot be zero.")
        else:
            rate = total_qty / total_units
            print("Unit rate = {} / {} = {} per 1 unit".format(total_qty, total_units, rate))
    elif ch == "3":
        print("1. Find speed")
        print("2. Find distance")
        print("3. Find time")
        sub = input("Choice: ")
        if sub == "1":
            d = UI.get_float("Distance = ")
            t = UI.get_positive_float("Time = ")
            print("Speed = {} / {} = {}".format(d, t, d/t))
        elif sub == "2":
            s = UI.get_float("Speed = ")
            t = UI.get_positive_float("Time = ")
            print("Distance = {} * {} = {}".format(s, t, s*t))
        elif sub == "3":
            d = UI.get_float("Distance = ")
            s = UI.get_nonzero_float("Speed = ")
            print("Time = {} / {} = {}".format(d, s, d/s))
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
        result = base * p / 100
        print("{}% of {} = {} * {}/100 = {}".format(p, base, base, p, result))
    elif ch == "2":
        original = UI.get_float("Original value = ")
        if original == 0:
            print("Original value cannot be zero (percent change undefined).")
        else:
            new = UI.get_float("New value = ")
            change = new - original
            pct = (change / original) * 100
            print("Change: {}, Percent change: {}%".format(change, pct))
    elif ch == "3":
        print("1. Discount")
        print("2. Sales tax")
        print("3. Tip")
        sub = input("Choice: ")
        price = UI.get_float("Original price = ")
        rate = UI.get_float("Rate (%) = ")
        if sub == "1":
            final = price * (1 - rate/100)
            print("Discounted price = {} * (1 - {}/100) = {}".format(price, rate, final))
        elif sub == "2":
            final = price * (1 + rate/100)
            print("Total with tax = {} * (1 + {}/100) = {}".format(price, rate, final))
        elif sub == "3":
            tip = price * rate / 100
            print("Tip amount = {}".format(tip))
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
        if total == 0:
            print("Total cannot be zero.")
        else:
            p = fav / total
            print("P = {} / {} = {}".format(fav, total, p))
    elif ch == "2":
        print("1. P(A and B) = P(A)*P(B) if independent")
        print("2. P(A or B) = P(A)+P(B)-P(A and B)")
        sub = input("Choice: ")
        pa = UI.get_float("P(A) = ")
        pb = UI.get_float("P(B) = ")
        if sub == "1":
            print("P(A and B) = {} * {} = {}".format(pa, pb, pa*pb))
        elif sub == "2":
            p_and = UI.get_float("P(A and B) = ")
            p_or = pa + pb - p_and
            print("P(A or B) = {} + {} - {} = {}".format(pa, pb, p_and, p_or))
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
    slope1 = (y2-y1)/(x2-x1) if x2 != x1 else None
    slope2 = (y3-y2)/(x3-x2) if x3 != x2 else None
    if slope1 is not None and slope2 is not None and abs(slope1 - slope2) < 1e-9:
        print("Data appears linear with constant slope.")
    else:
        if y1 != 0 and y2 != 0 and y3 != 0 and abs(y2/y1 - y3/y2) < 1e-9:
            print("Data appears exponential (constant ratio).")
        else:
            print("Data is neither clearly linear nor exponential with these three points.")
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
    iqr = q3 - q1 if q1 is not None and q3 is not None else None
    freq = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
    max_freq = max(freq.values())
    modes = [k for k, v in freq.items() if v == max_freq]
    mode_str = ", ".join(str(m) for m in modes) if max_freq > 1 else "no unique mode"
    range_val = max(nums) - min(nums)
    variance = sum((x-mean)**2 for x in nums) / (n-1) if n > 1 else 0
    std_dev = math.sqrt(variance)
    print("\nCount: {}".format(n))
    print("Mean: {}".format(mean))
    print("Median: {}".format(median))
    print("Mode: {}".format(mode_str))
    print("Range: {}".format(range_val))
    if q1 is not None and q3 is not None:
        print("Q1: {}, Q3: {}, IQR: {}".format(q1, q3, iqr))
    else:
        print("Quartiles: insufficient data.")
    print("Sample Variance: {}".format(variance))
    print("Sample Standard Deviation: {}".format(std_dev))
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
        print("Area = {}".format(l*w))
    elif ch == "2":
        s = UI.get_float("side = ")
        print("Area = {}".format(s*s))
    elif ch == "3":
        b = UI.get_float("base = ")
        h = UI.get_float("height = ")
        print("Area = {}".format(0.5*b*h))
    elif ch == "4":
        b = UI.get_float("base = ")
        h = UI.get_float("height = ")
        print("Area = {}".format(b*h))
    elif ch == "5":
        b1 = UI.get_float("base1 = ")
        b2 = UI.get_float("base2 = ")
        h = UI.get_float("height = ")
        print("Area = {}".format(0.5*(b1+b2)*h))
    elif ch == "6":
        r = UI.get_positive_float("radius = ")
        print("Area = {}".format(math.pi*r*r))
    elif ch == "7":
        r = UI.get_positive_float("radius = ")
        th = UI.get_float("angle deg = ")
        print("Sector area = ({}/360)*pi*{}^2 = {}".format(th, r, (th/360)*math.pi*r*r))
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
        print("V = {}".format(B*h))
    elif ch == "2":
        r = UI.get_positive_float("radius = ")
        h = UI.get_float("height = ")
        print("V = {}".format(math.pi*r*r*h))
    elif ch == "3":
        r = UI.get_positive_float("radius = ")
        h = UI.get_float("height = ")
        print("V = {}".format(1/3*math.pi*r*r*h))
    elif ch == "4":
        r = UI.get_positive_float("radius = ")
        print("V = {}".format(4/3*math.pi*r**3))
    elif ch == "5":
        B = UI.get_float("base area = ")
        h = UI.get_float("height = ")
        print("V = {}".format(1/3*B*h))
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
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    mid_x = (x1+x2)/2
    mid_y = (y1+y2)/2
    if x2-x1 == 0:
        slope = "undefined"
        eq = "x = {}".format(x1)
    else:
        slope = (y2-y1)/(x2-x1)
        b = y1 - slope*x1
        eq = "y = {}x + {}".format(slope, b)
    print("\nDistance = {}".format(dist))
    print("Midpoint = ({}, {})".format(mid_x, mid_y))
    print("Slope = {}".format(slope))
    print("Equation of line: {}".format(eq))
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
        print("Complement: {}, Supplement: {}, Vertical: {}".format(90-a, 180-a, a))
    elif ch == "2":
        a = UI.get_float("Angle (degrees) = ")
        print("Corresponding angle = {}".format(a))
        print("Alternate interior angle = {}".format(a))
        print("Same-side interior angle = {}".format(180-a))
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
        a3 = 180 - a1 - a2
        print("Third angle = {}".format(a3))
    elif ch == "2":
        r1 = UI.get_float("Remote interior 1 = ")
        r2 = UI.get_float("Remote interior 2 = ")
        print("Exterior angle = {}".format(r1 + r2))
    elif ch == "3":
        a1 = UI.get_float("Side in triangle1 = ")
        a2 = UI.get_float("Corresponding side in triangle2 = ")
        scale = a2 / a1 if a1 != 0 else 0
        print("Scale factor = {}".format(scale))
        b1 = UI.get_float("Another side in triangle1 = ")
        b2 = b1 * scale
        print("Corresponding side in triangle2 = {}".format(b2))
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
            c = math.sqrt(a*a + b*b)
            print("Hypotenuse c = sqrt({}^2+{}^2) = {}".format(a, b, c))
        elif sub == "2":
            a = UI.get_positive_float("Known leg = ")
            c = UI.get_positive_float("Hypotenuse = ")
            if c <= a:
                print("Hypotenuse must be > leg.")
            else:
                b = math.sqrt(c*c - a*a)
                print("Missing leg = sqrt({}^2-{}^2) = {}".format(c, a, b))
        else:
            print("Invalid choice.")
    elif ch == "2":
        print("1. 45-45-90")
        print("2. 30-60-90")
        sub = input("Choice: ")
        if sub == "1":
            leg = UI.get_positive_float("Leg length = ")
            hyp = leg * math.sqrt(2)
            print("Hypotenuse = {} * sqrt(2) = {}".format(leg, hyp))
        elif sub == "2":
            x = UI.get_positive_float("Short leg = ")
            hyp = 2*x
            long_leg = x * math.sqrt(3)
            print("Hypotenuse = {}, Long leg = {}".format(hyp, long_leg))
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
            rad = math.radians(angle)
            opp = hyp * math.sin(rad)
            adj = hyp * math.cos(rad)
            print("Opposite = {} * sin({}) = {}".format(hyp, angle, opp))
            print("Adjacent = {} * cos({}) = {}".format(hyp, angle, adj))
        elif side_known == "leg":
            leg = UI.get_positive_float("Leg length = ")
            angle = UI.get_float("Adjacent angle? (0-90) = ")
            if angle <= 0 or angle >= 90:
                print("Angle must be strictly between 0 and 90 degrees (cos !=0).")
            else:
                rad = math.radians(angle)
                hyp = leg / math.cos(rad)
                opp = hyp * math.sin(rad)
                print("Hypotenuse = {} / cos({}) = {}".format(leg, angle, hyp))
                print("Other leg = {} * sin({}) = {}".format(hyp, angle, opp))
        else:
            print("Invalid side specified.")
    elif ch == "2":
        opp = UI.get_positive_float("Opposite = ")
        adj = UI.get_positive_float("Adjacent = ")
        hyp = math.sqrt(opp**2 + adj**2)
        angle = math.degrees(math.atan(opp/adj))
        print("Angle = arctan({}/{}) = {} degrees".format(opp, adj, angle))
        print("Also sin^-1(opp/hyp) = {} degrees".format(math.degrees(math.asin(opp/hyp))))
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
        print("Circumference = 2*pi*{} = {}".format(r, 2*math.pi*r))
        print("Area = pi*{}^2 = {}".format(r, math.pi*r*r))
    elif ch == "2":
        r = UI.get_positive_float("Radius = ")
        th = UI.get_float("Central angle (degrees) = ")
        arc = (th/360) * 2 * math.pi * r
        sector = (th/360) * math.pi * r * r
        print("Arc length = ({}/360)*2*pi*{} = {}".format(th, r, arc))
        print("Sector area = ({}/360)*pi*{}^2 = {}".format(th, r, sector))
    elif ch == "3":
        h = UI.get_float("h = ")
        k = UI.get_float("k = ")
        r = UI.get_positive_float("r = ")
        print("Equation: (x - {})^2 + (y - {})^2 = {}".format(h, k, r*r))
        print("Expanded: x^2 + y^2 - {}x - {}y + {} = 0".format(2*h, 2*k, h*h + k*k - r*r))
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
        try:
            res = log_base(x, b)
            print("log_{}({}) = {}".format(b, x, res))
        except ValueError as e:
            print("Error: {}".format(e))
    elif ch == "2":
        b = UI.get_float("base b = ")
        a = UI.get_float("a = ")
        c = UI.get_float("c = ")
        d = UI.get_float("d = ")
        try:
            if b <= 0 or b == 1:
                print("Base must be positive and not equal to 1.")
            else:
                rhs = b ** d
                if a == 0:
                    print("Invalid: a=0.")
                else:
                    x = (rhs - c) / a
                    if a*x + c <= 0:
                        print("Argument must be >0, no solution.")
                    else:
                        print("Solution: x = {}".format(x))
        except Exception as e:
            print("Error: {}".format(e))
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
    if b == 1:
        print("Base 1 trivial.")
    else:
        if a == 0:
            lhs = b ** c
            if abs(lhs - d) < 1e-12:
                print("All x are solutions (equation is identity).")
            else:
                print("No solution.")
        else:
            try:
                log_val = log_base(d, b)
                x = (log_val - c) / a
                print("Solution: x = {}".format(x))
            except ValueError as e:
                print("Error: {}".format(e))
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
        an = a1 + (n-1)*d
        Sn = n/2 * (a1 + an)
        print("Term a{} = {}".format(n, an))
        print("Sum of first {} terms = {}".format(n, Sn))
    elif ch == "2":
        a1 = UI.get_float("first term a1 = ")
        r = UI.get_float("common ratio r = ")
        n = UI.get_int("n = ")
        an = a1 * (r ** (n-1))
        print("Term a{} = {}".format(n, an))
        if r == 1:
            Sn = a1 * n
        else:
            Sn = a1 * (1 - r**n) / (1 - r)
        print("Sum of first {} terms = {}".format(n, Sn))
        if abs(r) < 1:
            S_inf = a1 / (1 - r)
            print("Infinite sum (|r|<1) = {}".format(S_inf))
        else:
            print("No infinite sum (|r|>=1).")
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
        else:
            real = a1 - a2
            imag = b1 - b2
        print("Result: {} + {}i".format(real, imag))
    elif ch == "2":
        real = a1*a2 - b1*b2
        imag = a1*b2 + a2*b1
        print("Product: {} + {}i".format(real, imag))
    elif ch == "3":
        denom = a2**2 + b2**2
        if denom == 0:
            print("Cannot divide by zero.")
        else:
            real = (a1*a2 + b1*b2) / denom
            imag = (a2*b1 - a1*b2) / denom
            print("Quotient: {} + {}i".format(real, imag))
    elif ch == "4":
        mod = math.sqrt(a1**2 + b1**2)
        print("Modulus = {}".format(mod))
        print("Conjugate = {} - {}i".format(a1, b1))
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
        else:
            fact = 1
            for i in range(2, n+1):
                fact *= i
            print("{}! = {}".format(n, fact))
    elif ch == "2":
        n = UI.get_int("n = ")
        r = UI.get_int("r = ")
        if r < 0 or r > n:
            print("Invalid.")
        else:
            perm = 1
            for i in range(n, n-r, -1):
                perm *= i
            print("{}P{} = {}".format(n, r, perm))
    elif ch == "3":
        n = UI.get_int("n = ")
        r = UI.get_int("r = ")
        if r < 0 or r > n:
            print("Invalid.")
        else:
            comb = 1
            for i in range(1, r+1):
                comb = comb * (n - i + 1) // i
            print("{}C{} = {}".format(n, r, comb))
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
    else:
        comb = 1
        for i in range(1, k+1):
            comb = comb * (n - i + 1) // i
        coeff = comb * (a ** (n-k)) * (b ** k)
        print("Term T_{} = {} * a^{} * b^{} = {}".format(k+1, comb, n-k, k, coeff))
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
        det = a11*a22 - a12*a21
        print("Determinant = {}".format(det))
    elif ch == "2":
        a11 = UI.get_float("a11 = ")
        a12 = UI.get_float("a12 = ")
        a21 = UI.get_float("a21 = ")
        a22 = UI.get_float("a22 = ")
        det = a11*a22 - a12*a21
        if det == 0:
            print("No inverse (det=0).")
        else:
            print("Inverse:")
            print("[ {}, {} ]".format(a22/det, -a12/det))
            print("[ {}, {} ]".format(-a21/det, a11/det))
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
        else:
            x = (b1*a22 - b2*a12) / det
            y = (a11*b2 - a21*b1) / det
            print("Solution: x = {}, y = {}".format(x, y))
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
        print("Magnitude = {}".format(mag))
    else:
        x2 = UI.get_float("x2 = ")
        y2 = UI.get_float("y2 = ")
        if ch == "2":
            dot = x1*x2 + y1*y2
            print("Dot product = {}".format(dot))
        elif ch == "3":
            dot = x1*x2 + y1*y2
            mag1 = math.sqrt(x1**2 + y1**2)
            mag2 = math.sqrt(x2**2 + y2**2)
            if mag1 == 0 or mag2 == 0:
                print("Zero vector, angle undefined.")
            else:
                cos_theta = dot / (mag1 * mag2)
                if cos_theta > 1:
                    cos_theta = 1
                if cos_theta < -1:
                    cos_theta = -1
                theta = math.degrees(math.acos(cos_theta))
                print("Angle = {} degrees".format(theta))
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
            print("Side b (opposite B) = {}".format(b))
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
            c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(C)))
            print("Side c = {}".format(c))
        elif sub == "2":
            a = UI.get_float("side a = ")
            b = UI.get_float("side b = ")
            c = UI.get_float("side c = ")
            try:
                cosA = (b**2 + c**2 - a**2) / (2*b*c)
                if cosA > 1 or cosA < -1:
                    print("Invalid triangle sides.")
                else:
                    A = math.degrees(math.acos(cosA))
                    print("Angle A = {} degrees".format(A))
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
    if a + b > c and a + c > b and b + c > a:
        s = (a + b + c) / 2
        try:
            area = math.sqrt(s * (s-a) * (s-b) * (s-c))
            print("Area = {}".format(area))
        except ValueError:
            print("Invalid input caused negative under sqrt.")
    else:
        print("Sides do not form a valid triangle.")
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
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    print("Distance = {}".format(dist))
    UI.wait()

@solver("Additional Topics", "10", "Quadratic Inequality")
def quadratic_inequality():
    UI.clear()
    print("QUADRATIC INEQUALITY (ax^2+bx+c > 0, etc.)")
    a = UI.get_nonzero_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    op = input("Operator (<, >, <=, >=): ").strip()
    disc = b*b - 4*a*c
    print("Discriminant = {}".format(disc))
    if disc < 0:
        if a > 0:
            truth = True if op in [">", ">="] else False
        else:
            truth = True if op in ["<", "<="] else False
        if truth:
            print("All real x are solutions.")
        else:
            print("No solution.")
    elif disc == 0:
        root = -b/(2*a)
        print("Double root at x = {}".format(root))
        if a > 0:
            if op == ">":
                print("Solution: all x except x = {}".format(root))
            elif op == ">=":
                print("Solution: all real x")
            elif op == "<":
                print("No solution (expression never negative)")
            else:  # op == "<="
                print("Solution: x = {} (only point where expression is zero)".format(root))
        else:  # a < 0
            if op == "<":
                print("Solution: all x except x = {}".format(root))
            elif op == "<=":
                print("Solution: all real x")
            elif op == ">":
                print("No solution (expression never positive)")
            else:  # op == ">="
                print("Solution: x = {} (only point where expression is zero)".format(root))
    else:
        sq = math.sqrt(disc)
        r1 = (-b - sq)/(2*a)
        r2 = (-b + sq)/(2*a)
        if r1 > r2:
            r1, r2 = r2, r1
        print("Roots: {} and {}".format(r1, r2))
        if a > 0:
            if op in [">", ">="]:
                print("Solution: x < {} or x > {}".format(r1, r2))
            else:
                print("Solution: {} < x < {}".format(r1, r2))
        else:
            if op in [">", ">="]:
                print("Solution: {} < x < {}".format(r1, r2))
            else:
                print("Solution: x < {} or x > {}".format(r1, r2))
    UI.wait()

@solver("Additional Topics", "11", "Absolute Value Inequality")
def absolute_value_inequality():
    UI.clear()
    print("ABSOLUTE VALUE INEQUALITY: |ax+b| < c  (or >, <=, >=)")
    a = UI.get_float("a = ")
    b = UI.get_float("b = ")
    c = UI.get_float("c = ")
    op = input("Operator (<, >, <=, >=): ").strip()
    if a == 0:
        abs_b = abs(b)
        if op == "<":
            if abs_b < c:
                print("All real x are solutions.")
            else:
                print("No solution.")
        elif op == "<=":
            if abs_b <= c:
                print("All real x are solutions.")
            else:
                print("No solution.")
        elif op == ">":
            if abs_b > c:
                print("All real x are solutions.")
            else:
                print("No solution.")
        elif op == ">=":
            if abs_b >= c:
                print("All real x are solutions.")
            else:
                print("No solution.")
        UI.wait()
        return

    if c < 0:
        if op in [">", ">="]:
            print("All real x are solutions (abs always >=0 > negative).")
        else:
            print("No solution (abs cannot be < negative).")
    elif c == 0:
        if op in ["<", "<="]:
            x = -b/a
            print("Only solution x = {} (since |...|<=0 implies ...=0)".format(x))
        else:
            x = -b/a
            if op == ">":
                print("All x except x = {}".format(x))
            else:
                print("All real x are solutions.")
    else:
        if op in ["<", "<="]:
            low = (-c - b)/a
            high = (c - b)/a
            if a < 0:
                low, high = high, low
            print("Solution: {} < x < {}".format(low, high))
        else:
            left = (-c - b)/a
            right = (c - b)/a
            if a < 0:
                left, right = right, left
            print("Solution: x < {} or x > {}".format(left, right))
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
        deg = rad * 180 / math.pi
        print("{} rad = {} degrees".format(rad, deg))
    elif ch == "2":
        deg = UI.get_float("degrees = ")
        rad = deg * math.pi / 180
        print("{} deg = {} rad".format(deg, rad))
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
    print("Quotient: {}".format(poly_str if poly_str else "0"))
    print("Remainder: {}".format(remainder))
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
    for co in coeff[1:]:
        val = val * c + co
    print("P({}) = {}".format(c, val))
    UI.wait()

@solver("Additional Topics", "15", "Completing the Square")
def completing_square():
    UI.clear()
    print("COMPLETING THE SQUARE: x^2 + bx + c = (x + p)^2 + q")
    b = UI.get_float("b (coefficient of x) = ")
    c = UI.get_float("c (constant) = ")
    p = b / 2
    q = c - p**2
    print("Result: (x + {})^2 + {}".format(p, q))
    UI.wait()

# ----------------------------------------------------------------------
# SOLVERS – FUNCTION GUIDES (grouped under Additional Topics)
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
# CALCULATOR UTILITIES
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
        print("{}/{} = {}".format(num, den, num/den))
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
        print("Approximation: {}/{}".format(best_num//g, best_den//g))
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
        print("{} = {}%".format(d, d*100))
    elif ch == "2":
        p = UI.get_float("Percent = ")
        print("{}% = {}".format(p, p/100))
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
    else:
        g = gcd(num, den)
        print("GCF = {}, Simplified: {}/{}".format(g, num//g, den//g))
    UI.wait()

@solver("Utilities", "4", "GCF")
def gcf():
    UI.clear()
    a = UI.get_int("First number: ")
    b = UI.get_int("Second number: ")
    print("GCF = {}".format(gcd(a, b)))
    UI.wait()

@solver("Utilities", "5", "LCM")
def lcm():
    UI.clear()
    a = UI.get_int("First number: ")
    b = UI.get_int("Second number: ")
    g = gcd(a, b)
    l = abs(a*b)//g if g != 0 else 0
    print("LCM = {}".format(l))
    UI.wait()

@solver("Utilities", "6", "Prime Factorization")
def prime_factorization():
    UI.clear()
    n = UI.get_int("Enter integer (>1): ")
    if n < 2:
        print("Must be >1.")
        UI.wait()
        return
    factors = []
    temp = n
    d = 2
    while d*d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    print("{} = {}".format(n, ' * '.join(map(str, factors))))
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
            print("0 = 0 x 10^0")
        else:
            exp = int(math.floor(math.log10(abs(num))))
            mantissa = num / (10**exp)
            print("{} = {} x 10^{}".format(num, mantissa, exp))
    elif ch == "2":
        mantissa = UI.get_float("Mantissa = ")
        exponent = UI.get_int("Exponent = ")
        result = mantissa * (10**exponent)
        print("{} x 10^{} = {}".format(mantissa, exponent, result))
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
    disc = b*b - 4*a*c
    if disc < 0:
        print("No real roots.")
    else:
        sq = math.sqrt(disc)
        x1 = (-b + sq)/(2*a)
        x2 = (-b - sq)/(2*a)
        print("x1 = {}, x2 = {}".format(x1, x2))
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
        print("Distance = {}".format(math.sqrt((x2-x1)**2 + (y2-y1)**2)))
    elif ch == "2":
        print("Midpoint = ({}, {})".format((x1+x2)/2, (y1+y2)/2))
    elif ch == "3":
        if x2-x1 == 0:
            print("Slope undefined")
        else:
            print("Slope = {}".format((y2-y1)/(x2-x1)))
    else:
        print("Invalid choice.")
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
        print("c = sqrt({}^2+{}^2) = {}".format(a, b, math.sqrt(a*a+b*b)))
    elif ch == "2":
        leg = UI.get_positive_float("Known leg = ")
        hyp = UI.get_positive_float("Hypotenuse = ")
        if hyp <= leg:
            print("Hypotenuse must be larger.")
        else:
            print("Missing leg = sqrt({}^2-{}^2) = {}".format(hyp, leg, math.sqrt(hyp*hyp - leg*leg)))
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
    print("  SAT Math Solver for HP Prime G2")
    print("="*30)
    print("Covers EVERY Digital SAT Math topic.")
    print("")
    print("Features:")
    print("- Step-by-step solvers")
    print("- Built-in formula reference")
    print("- Text guides for conceptual topics")
    print("- 60+ solvers & utilities")
    print("")
    print("Version: 1.2 (MicroPython) – Complete redesign")
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
        choice = input("Enter choice: ")
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

# ----------------------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------------------
if __name__ == "__main__":
    main_menu()
