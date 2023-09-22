from typing import Any


class CubicBezier:
    __slots__ = ['a', 'b', 'c', 'd', 'cx', 'bx', 'ax', 'cy', 'by', 'ay']

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        # pre-calculate the polynomial coefficients
        # irst and last control points are implied to be (0,0) and (1.0, 1.0)
        self.cx = 3.0 * a
        self.bx = 3.0 * (c - a) - self.cx
        self.ax = 1.0 - self.cx - self.bx

        self.cy = 3.0 * b
        self.by = 3.0 * (d - b) - self.cy
        self.ay = 1.0 - self.cy - self.by

    def sample_curve_x(self, t):
        return ((self.ax * t + self.bx) * t + self.cx) * t

    def sample_curve_y(self, t):
        return ((self.ay * t + self.by) * t + self.cy) * t

    def sample_curve_derivative_x(self, t):
        return (3.0 * self.ax * t + 2.0 * self.bx) * t + self.cx

    def calculate(self, x, epsilon=.0001):
        return self.sample_curve_y(self.solve_curve_x(x, epsilon))

    def solve_curve_x(self, t, epsilon=.0001):
        # First try a few iterations of Newton's method -- normally very fast.
        t0 = 0
        t1 = 0
        t2 = 0
        x2 = 0
        # d2 = 0
        # i = 0

        # t2 = t
        # for i in range(8):
        #     x2 = self.sample_curve_x(t2) - t
        #     if abs(x2) < epsilon:
        #         return t2
        #     d2 = self.sample_curve_derivative_x(t2)
        #     if abs(d2) < epsilon:
        #         break
        #
        #     t2 = t2 - x2 / d2

        # No solution found - use bi-section
        t0 = 0.0
        t1 = 1.0
        t2 = t

        if t2 < t0:
            return t0
        if t2 > t1:
            return t1

        while t0 < t1:
            x2 = self.sample_curve_x(t2)
            if abs(x2 - t) < epsilon:
                return t2
            if t > x2:
                t0 = t2
            else:
                t1 = t2

            t2 = (t1 - t0) * .5 + t0

        # Give up
        return t2

    def __call__(self, t) -> Any:
        return self.calculate(t)