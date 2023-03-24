import numpy as np
from zkwordle.ecc import bn128
from zkwordle.util import mod_inv, polydivmod
from zkwordle.points import R1CS_LENGTH

prime = bn128.curve_order

class fpoly1d:
  
  def __init__(self, c,  prime=prime):
    self.prime = prime
    
    if isinstance(c, fpoly1d):
      self.coeffs = c.coeffs
      return
 
    c = np.atleast_1d(c).astype(object)
    c = np.trim_zeros(c, 'f')
    self.coeffs = np.mod(c, self.prime)

  def toJSON(self):
    return self.__dict__

  def __call__(self, val):
    y = 0
    for c in self.coeffs:
      y = (y * val + c) % self.prime
    return y

  def __mul__(self, other):
    if isinstance(other, fpoly1d):
      return fpoly1d(np.convolve(self.coeffs, other.coeffs))
    else:
      return fpoly1d(self.coeffs * other)

  def __rmul__(self, other):
    if np.isscalar(other):
      return fpoly1d(other * self.coeffs)
    else:
      other = fpoly1d(other)
      return fpoly1d(np.convolve(self.coeffs, other.coeffs))

  def __imul__(self, other):
    if np.isscalar(other):
      self.coeffs = np.mod(self.coeffs * other, self.prime)
    else:
      other = fpoly1d(other)
      self.coeffs = np.mod(np.convolve(self.coeffs, other.coeffs), self.prime)
    return self

  def __add__(self, other):
    other = fpoly1d(other)
    return fpoly1d(np.polyadd(self.coeffs, other.coeffs))

  def __radd__(self, other):
    other = fpoly1d(other)
    return fpoly1d(np.polyadd(self.coeffs, other.coeffs))

  def __iadd__(self, other):
    other = fpoly1d(other)
    self.coeffs = np.mod(np.polyadd(self.coeffs, other.coeffs), self.prime)
    return self

  def __sub__(self, other):
    other = fpoly1d(other)
    return fpoly1d(np.polysub(self.coeffs, other.coeffs))

  def __rsub__(self, other):
    other = fpoly1d(other)
    return fpoly1d(np.polysub(self.coeffs, other.coeffs))

  def __isub__(self, other):
    other = fpoly1d(other)
    self.coeffs = np.mod(np.polysub(self.coeffs, other.coeffs), self.prime)
    return self

  def __div__(self, other):
    if np.isscalar(other):
      other_inv = mod_inv(other, self.prime)
      return fpoly1d(self.coeffs * other_inv)
    q, r = polydivmod(self.coeffs, other.coeffs, self.prime)
    return fpoly1d(q), fpoly1d(r)

  __truediv__ = __div__

  def __rdiv__(self, other):
    if np.isscalar(other):
      other_inv = mod_inv(other. self.prime)
      return fpoly1d(self.coeffs * other_inv)
    q, r = polydivmod(self.coeffs, other.coeffs, self.prime)
    return fpoly1d(q), fpoly1d(r)
 
  def __eq__(self, other):
    if not isinstance(other, fpoly1d):
      return NotImplemented
    if self.coeffs.shape != other.coeffs.shape:
      return False
    return (self.coeffs == other.coeffs).all()

  def __ne__(self, other):
    if not isinstance(other, fpoly1d):
      return NotImplemented
    return not self.__eq__(other)


class VariablePolynomial:

  def __init__(self):
    self.x = np.arange(1, R1CS_LENGTH + 1, dtype=object)
    self.y = np.zeros(R1CS_LENGTH, dtype=object)
    self.poly = None

  def __call__(self, s):
    if self.poly is None:
      return None
    return self.poly(s)

  def set_value(self, px, py):
    value = py % prime
    if value == 0:
      return
    self.y[px-1] = value

  def set_values(self, pts):
    for px, py in pts:
      self.set_value(px, py)

  def interpolate(self):
    # Emulating SciPy's Lagrange implementation
    self.poly = fpoly1d(0)
    for i in np.flatnonzero(self.y):
      pt = fpoly1d(self.y[i])
      for j in range(len(self.x)):
        if i == j:
          continue
        fac = self.x[i] - self.x[j]
        pt *= fpoly1d([1, -self.x[j]])/fac
      self.poly += pt

  def print(self, all=False):
    print('-'*40)
    if self.poly is None:
      print("Polynomial not yet interpolated.")
      return
    for i in range(R1CS_LENGTH):
      if self.y[i] - self.poly(self.x[i]):
        print(f"Unexpected discrepancy at x={self.x[i]}. Expected value: {self.y[i]}. Interpolated value: {self.poly(self.x[i])}.")
      elif self.y[i] or all:
        print(f"{self.x[i]}: {self.poly(self.x[i])}")


class Variable:
  
  PUBLIC = 0
  PRIVATE = 1

  def __init__(self, name='', visibility=None):
    self.name = name
    self.visibility = visibility if visibility is not None else self.PRIVATE
    self.polys = {}

  def set_single_polynomial(self, type, points):
    poly = VariablePolynomial()
    poly.set_values(points)
    poly.interpolate()
    self.polys[type] = poly

  def set_polynomials(self, points_l, points_r, points_o):
    self.set_single_polynomial('l', points_l)
    self.set_single_polynomial('r', points_r)
    self.set_single_polynomial('o', points_o)

  def evaluate(self, key, s):
    if key not in self.polys:
      return None
    return self.polys[key](s)

  def to_dict(self):
    return {
      'name': self.name,
      'visibility': self.visibility,
      'polys': {
        'l': self.polys.get('l').poly.coeffs,
        'r': self.polys.get('r').poly.coeffs,
        'o': self.polys.get('o').poly.coeffs,
      }
    }

  @classmethod
  def from_polys(cls, polys, name='', visibility=None):
    ret = cls(name, visibility)
    for type, poly in polys.items():
      tmp = VariablePolynomial()
      tmp.poly = poly
      ret.polys[type] = tmp
    return ret


