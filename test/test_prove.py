import unittest
import os

from hypothesis import given, settings, assume
from hypothesis import strategies as st

import zkwordle as zk


LOAD_POLYS = os.environ.get("LOAD_POLYS", None)


def wordle_truth(a, w):
  r = [0]*len(a)
  a = a.copy()
  w = w.copy()
  for i in range(len(a), 0, -1):
    if a[-i] == w[-i]:
      r[-i] = 2
      w.pop(-i)
  for i, l in enumerate(a):
    if l in w and r[i] != 2:
      r[i] = 1
      w.pop(w.index(l))

  return r


@st.composite
def valid_args(draw):
  s = draw(st.lists(st.integers(min_value=0, max_value=25), min_size=10, max_size=10))
  a = s[0:5]
  w = s[5:10]
  
  n = draw(st.integers(min_value=0, max_value=2**253-1))
  N = zk.hash(n)
  wc = sum([n << 5*i for i, n in enumerate(w)])
  W = wc * zk.ecc.bjj.Point.GENERATOR
  H = W + N
  return [*s, H.x, H.y, n]


@st.composite
def invalid_args(draw):
  s = draw(st.lists(st.integers(min_value=0, max_value=25), min_size=10, max_size=10))
  a = s[0:5]
  w = s[5:10]
  r = draw(st.lists(st.integers(min_value=0, max_value=2), min_size=5, max_size=5))
  assume(r != wordle_truth(a, w))
  n = draw(st.integers(min_value=0, max_value=2**255-1))
  H = zk.hash(n)
  return [*s, *r, H.x, H.y, n]
  
  
class TestE2E(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.proving, cls.verifying, cls.polys = zk.setup(load_polys=LOAD_POLYS) 

  @settings(max_examples=5, deadline=None) 
  @given(valid_args())
  def test_e2e(self, s):
    a = s[0:5]
    w = s[5:10]
    r = wordle_truth(a, w)
    W = s[10:12]
    n = s[12]
    proof = zk.prove(a, W, r, w, n, self.proving, self.polys)
    res = zk.verify(a, W, r, self.verifying, proof)
    self.assertEqual(res, True, 'LxR does not equal O')

  @settings(max_examples=5, deadline=None)
  @given(invalid_args())
  def test_invalid_proof(self, s):
    a = s[0:5]
    w = s[5:10]
    r = s[10:15]
    W = s[15:17]
    n = s[17]
    proof = zk.prove(a, W, r, w, n, self.proving, self.polys)
    res = zk.verify(a, W, r, self.verifying, proof)
    self.assertEqual(res, False, 'Verification algorithm passed for false proof.')


if __name__ == "__main__":
  unittest.main()
