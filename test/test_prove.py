import unittest

from hypothesis import given, settings, assume
from hypothesis import strategies as st

import zkwordle as zk


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
def invalid_args(draw):
  s = draw(st.lists(st.integers(min_value=0, max_value=25), min_size=10, max_size=10))
  a = s[0:5]
  w = s[5:10]
  r = draw(st.lists(st.integers(min_value=0, max_value=2), min_size=5, max_size=5))
  assume(r != wordle_truth(a, w))
  return [*s, *r]
  
  
class TestE2E(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.polys, cls.proving, cls.verifying = zk.setup() 

  @settings(deadline=None) 
  @given(st.lists(st.integers(min_value=0, max_value=25), min_size=10, max_size=10)) 
  def test_e2e(self, s):
    a = s[0:5]
    w = s[5:10]
    r = wordle_truth(a, w)
    proof = zk.prove(a, w, r, polys_df=self.polys, proving_df=self.proving)
    res = zk.verify(polys_df=self.polys, proof_df=proof, verifying_df=self.verifying)
    self.assertEqual(res, True, 'LxR does not equal O')

  @settings(deadline=None)
  @given(invalid_args())
  def test_revert_proof(self, s):
    a = s[0:5]
    w = s[5:10]
    r = s[10:15]
    with self.assertRaises(zk.InvalidProof, msg=f"No exception was raised for a={a}, w={w} and r={r}"):
      zk.prove(a, w, r, polys_df=self.polys, proving_df=self.proving)

  @settings(deadline=None)
  @given(invalid_args())
  def test_invalid_proof(self, s):
    a = s[0:5]
    w = s[5:10]
    r = s[10:15]
    proof = zk.prove(a, w, r, polys_df=self.polys, proving_df=self.proving, raise_exception=False)
    res = zk.verify(polys_df=self.polys, proof_df=proof, verifying_df=self.verifying)
    self.assertEqual(res, False, 'Verification algorithm passed for false proof.')


if __name__ == "__main__":
  unittest.main()
