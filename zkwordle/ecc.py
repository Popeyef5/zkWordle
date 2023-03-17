from py_ecc.optimized_bn128 import add, multiply, neg, pairing, G1, G2, curve_order, field_modulus, eq, normalize, FQ

class GroupElement:

  def __init__(self, pt):
    self.pt = pt

  def __add__(self, other):
    if not isinstance(other, type(self)):
      return NotImplemented
    return type(self)(add(self.pt, other.pt))

  __radd__ = __add__

  def __iadd__(self, other):
    if not isinstance(other, type(self)):
      return NotImplemented
    self.pt = add(self.pt, other.pt)
    return self 

  def __mul__(self, other):
    if not isinstance(other, int):
      return NotImplemented
    ret = multiply(self.pt, abs(other) % curve_order)
    if other < 0:
      ret = neg(ret)
    return type(self)(ret)

  __rmul__ = __mul__

  def __eq__(self, other):
    if not isinstance(other, type(self)):
      return False
    return eq(self.pt, other.pt)

  def __repr__(self):
      return self.pt.__repr__()

  @classmethod
  def from_ints(cls, x, y):
    pt = (FQ(x), FQ(y), FQ(1))
    return cls(pt)

  @classmethod
  def neutral(cls):
    pt = (FQ(1), FQ(1), FQ(0))
    return cls(pt)

  @property
  def x(self):
    x, _ = normalize(self.pt)
    return x.n

  @property
  def y(self):
    _, y = normalize(self.pt)
    return y.n


class bn128(GroupElement):
  pass

class bn128_2(GroupElement):
  pass


def e(p1, p2):
  return pairing(p2.pt, p1.pt)


G1 = bn128(G1)
G2 = bn128_2(G2)

# https://en.wikipedia.org/wiki/Legendre_symbol
def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    if ls == p - 1:
        return -1
    return ls

# https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
# https://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
def mod_sqrt(a, p):
  if legendre_symbol(a, p) != 1:
    return []
  elif a == 0:
    return [0, 0]
  elif p == 2:
    return [a, a]
  elif p % 4 == 3:
    x = pow(a, (p + 1) // 4, p)
    return [min(x, p-x), max(x, p-x)]

  # Partition p-1 to s * 2^e for an odd s (i.e.
  # reduce all the powers of 2 from p-1)
  #
  s = p - 1
  e = 0
  while s % 2 == 0:
    s //= 2
    e += 1

  # Find some 'n' with a legendre symbol n|p = -1.
  # Shouldn't take long.
  #
  n = 2
  while legendre_symbol(n, p) != -1:
    n += 1

  # Here be dragons!
  # Read the paper "Square roots from 1; 24, 51,
  # 10 to Dan Shanks" by Ezra Brown for more
  # information
  #

  # x is a guess of the square root that gets better
  # with each iteration.
  # b is the "fudge factor" - by how much we're off
  # with the guess. The invariant x^2 = ab (mod p)
  # is maintained throughout the loop.
  # g is used for successive powers of n to update
  # both a and b
  # r is the exponent - decreases with each update
  #
  x = pow(a, (s + 1) // 2, p)
  b = pow(a, s, p)
  g = pow(n, s, p)
  r = e

  while True:
    t = b
    m = 0
    for m in range(r):
      if t == 1:
        break
      t = pow(t, 2, p)

    if m == 0:
      return [min(x, p-x), max(x, p-x)]

    gs = pow(g, 2 ** (r - m - 1), p)
    g = (gs * gs) % p
    x = (x * gs) % p
    b = (b * g) % p
    r = m

  
class Curve:
  
  def __init__(self, a=0, b=3, p=13):
    self.a, self.b, self.p = a, b, p

  def from_x(self, x, sign):
    tmp = (x*x*x + self.a*x + self.b) % self.p
    ret = mod_sqrt(tmp, self.p)
    if ret:
      return ret[1] if sign else ret[0]
    return None


bjj = Curve(
  a=7296080957279758407415468581752425029516121466805344781232734728849116493472,
  b=16213513238399463127589930181672055621146936592900766180517188641980520820846,
  p=21888242871839275222246405745257275088548364400416034343698204186575808495617
)

bjj.Gx = 14414009007687342025526645003307639786191886886413750648631138442071909631647
bjj.Gy = 14577268218881899420966779687690205425227431577728659819975198491127179315626
bjj.G = GroupElement.from_ints(bjj.Gx, bjj.Gy)
