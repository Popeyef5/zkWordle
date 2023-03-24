from py_ecc.optimized_bn128 import add, multiply, neg, pairing, G1, G2, curve_order, field_modulus, eq, normalize, FQ
from .util import mod_sqrt

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


  
class Curve:
  
  def __init__(self, a=0, b=3, p=13):
    self.a, self.b, self.p = a, b, p

  def from_x(self, x, sign):
    tmp = (x*x*x + self.a*x + self.b) % self.p
    ret = mod_sqrt(tmp, self.p)
    if ret:
      return ret[1] if sign else ret[0]
    return None


# bjj = Curve(
#   a=7296080957279758407415468581752425029516121466805344781232734728849116493472,
#   b=16213513238399463127589930181672055621146936592900766180517188641980520820846,
#   p=21888242871839275222246405745257275088548364400416034343698204186575808495617
# )

# bjj.Gx = 14414009007687342025526645003307639786191886886413750648631138442071909631647
# bjj.Gy = 14577268218881899420966779687690205425227431577728659819975198491127179315626
# bjj.G = GroupElement.from_ints(bjj.Gx, bjj.Gy)
