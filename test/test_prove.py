import unittest

from hypothesis import given, settings
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
  
  
class TestE2E(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.setup = zk.setup() 

  @settings(deadline=None) 
  @given(st.lists(st.integers(min_value=0, max_value=25), min_size=10, max_size=10)) 
  def test_e2e(self, s):
    a = s[0:5]
    w = s[5:10]
    r = wordle_truth(a, w)
    proof = zk.prove(a, w, r, df=self.setup)
    self.assertEqual(proof, True, 'LxR does not equal O')

if __name__ == "__main__":
  unittest.main()
