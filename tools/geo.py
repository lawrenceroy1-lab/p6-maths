"""Small helpers used by the unit build scripts (not part of the website).

check(value, expected, where) stops the build if a calculation does not match the answer key.
"""
import math
from fractions import Fraction

PROBLEMS = []


def check(value, expected, where):
    ok = abs(float(value) - float(expected)) < 1e-9
    if not ok:
        PROBLEMS.append(f"{where}: calculated {value}, answer key says {expected}")
    return value


def fmt(x):
    """Nice number text: 7.5 -> '7.5', 8.0 -> '8'."""
    if isinstance(x, Fraction):
        x = float(x)
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.2f}".rstrip("0").rstrip(".")


def apex(B, C, angB, angC, up=True):
    """Third corner A of triangle ABC from base B-C and base angles (degrees). SVG y points down."""
    bx, by = B
    cx, cy = C
    base = math.atan2(cy - by, cx - bx)
    s = -1 if up else 1
    d1 = base + s * math.radians(angB)
    d2 = base + math.pi - s * math.radians(angC)
    # solve B + t*u1 = C + k*u2
    u1 = (math.cos(d1), math.sin(d1))
    u2 = (math.cos(d2), math.sin(d2))
    det = u1[0] * (-u2[1]) - u1[1] * (-u2[0])
    t = ((cx - bx) * (-u2[1]) - (cy - by) * (-u2[0])) / det
    return [round(bx + t * u1[0], 1), round(by + t * u1[1], 1)]


def polar(c, r, deg):
    """Point on a circle, deg measured clockwise from 3 o'clock (SVG)."""
    return [round(c[0] + r * math.cos(math.radians(deg)), 1), round(c[1] + r * math.sin(math.radians(deg)), 1)]


def lerp(a, b, t):
    return [round(a[0] + (b[0] - a[0]) * t, 1), round(a[1] + (b[1] - a[1]) * t, 1)]


def foot(P, A, B):
    """Foot of the perpendicular from P to line AB."""
    ax, ay = A
    bx, by = B
    dx, dy = bx - ax, by - ay
    t = ((P[0] - ax) * dx + (P[1] - ay) * dy) / (dx * dx + dy * dy)
    return [round(ax + t * dx, 1), round(ay + t * dy, 1)]


def angle_at(V, A, B):
    """Angle AVB in degrees."""
    a1 = math.atan2(A[1] - V[1], A[0] - V[0])
    a2 = math.atan2(B[1] - V[1], B[0] - V[0])
    d = abs(math.degrees(a1 - a2)) % 360
    return 360 - d if d > 180 else d
