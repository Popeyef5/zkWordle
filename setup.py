#!/usr/bin/env python3

from points import *

import numpy as np

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617

def mod_inv(x, p):
  x = x % p
  t = 0
  nt = 1
  r = p
  nr = x
  while nr != 0:
    q = r // nr
    t, nt = nt, t - q * nt
    r, nr = nr, r - q * nr
  if r != 1:
    raise ValeError("number has no inverse")
  return t % p


class fpoly1d:
  
  def __init__(self, c,  prime=p):
    self.prime = prime
    
    if isinstance(c, fpoly1d):
      self.coeffs = c.coeffs
      return
 
    c = np.atleast_1d(c).astype(object)
    self.coeffs = np.mod(c, self.prime)

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
    return NotImplemented

  __truediv__ = __div__

  def __rdiv__(self, other):
    if np.isscalar(other):
      other_inv = mod_inv(other. self.prime)
      return fpoly1d(self.coeffs * other_inv)
    return NotImplemented


class VP:

  def __init__(self, name='', type='l'):
    self.name = name
    self.type = type
    self.x = np.arange(1, 261, dtype=object)
    self.y = np.zeros(260, dtype=object)
    self.poly = None

  def set_value(self, px, py):
    self.y[px-1] = py % p

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
    self.print()

  def print(self, all=False):
    print('-'*40)
    print(self.name, self.type)
    #print('Differences:', np.any(self.y-self.poly(self.x)))
    print('-'*40)
    if self.poly is None:
      print("Polynomial not yet interpolated.")
      return
    for i in range(260):
      if self.y[i] - self.poly(self.x[i]):
        print(f"Unexpected discrepancy at x={self.x[i]}. Expected value: {self.y[i]}. Interpolated value: {self.poly(self.x[i])}.")
      elif self.y[i] or all:
        print(f"{self.x[i]}: {self.poly(self.x[i])}")


if __name__ == "__main__":
  polys = []
  
  def import_var(name, points_l, points_r, points_o):
    var = VP(name, 'l')
    var.set_values(points_l)
    var.interpolate()
    polys.append(var)

    var = VP(name, 'r')
    var.set_values(points_r)
    var.interpolate()
    polys.append(var)

    var = VP(name, 'o')
    var.set_values(points_o)
    var.interpolate()
    polys.append(var)

  #a_ij
  for i in range(5):
    for j in range(5):
      import_var(f'a{i}{j}', l_aij(i, j), r_aij(i, j), o_aij(i, j))

  #w_ij
  for i in range(5):
    for j in range(5):
      import_var(f'w{i}{j}', l_wij(i, j), r_wij(i, j), o_wij(i, j))
    import_var(f'w{i}34', l_wi34(i), r_wi34(i), o_wi34(i))
    import_var(f'w{i}12', l_wi12(i), r_wi12(i), o_wi12(i))

  #r_i
  for i in range(5):
    import_var(f'r{i}', l_ri(i), r_ri(i), o_ri(i))

  #r_i2
  for i in range(5):
    import_var(f'r{i}2', l_ri2(i), r_ri2(i), o_ri2(i))

  #rho_i
  for i in range(5):
    import_var(f'rho{i}0', l_rhoi0(i), r_rhoi0(i), o_rhoi0(i)) 
    import_var(f'rho{i}1', l_rhoi1(i), r_rhoi1(i), o_rhoi1(i)) 
    import_var(f'rho{i}2', l_rhoi2(i), r_rhoi2(i), o_rhoi2(i)) 

  #PI_ij
  for i in range(5):
    for j in range(5):
      import_var(f'P{i}{j}12', l_Pij12(i, j), r_Pij12(i, j), o_Pij12(i, j))
      import_var(f'P{i}{j}34', l_Pij34(i, j), r_Pij34(i, j), o_Pij34(i, j))
      import_var(f'P{i}{j}1234', l_Pij1234(i, j), r_Pij1234(i, j), o_Pij1234(i, j))
      import_var(f'P{i}{j}', l_Pij(i, j), r_Pij(i, j), o_Pij(i, j))
      import_var(f'P{i}{j}2', l_Pij2(i, j), r_Pij2(i, j), o_Pij2(i, j))

  #D_i
  for i in range(5):
    import_var(f'D{i}12', l_Di12(i), r_Di12(i), o_Di12(i))
    import_var(f'D{i}34', l_Di34(i), r_Di34(i), o_Di34(i))
    import_var(f'D{i}1234', l_Di1234(i), r_Di1234(i), o_Di1234(i))
    import_var(f'D{i}', l_Di(i), r_Di(i), o_Di(i))
    import_var(f'D{i}2', l_Di2(i), r_Di2(i), o_Di2(i))

  #c_i
  for i in range(5):
    import_var(f'c{i}0', l_ci0(i), r_ci0(i), o_ci0(i))
    import_var(f'c{i}1', l_ci1(i), r_ci1(i), o_ci1(i))
    import_var(f'c{i}2', l_ci2(i), r_ci2(i), o_ci2(i))
    
  #v_one
  import_var('v1', l_v1(), r_v1(), o_v1())

  import csv
  
  with open('setup.csv', mode='w') as file:
    csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for poly in polys:
      csv_writer.writerow([poly.name, poly.type, *poly.poly.coeffs])
      
    










