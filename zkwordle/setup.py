#!/usr/bin/env python3

from zkwordle.points import *
from zkwordle.util import VariablePolynomial

def setup(write=False):

  import pandas as pd

  polys = []
  
  def import_var(name, points_l, points_r, points_o):
    var = VariablePolynomial(name, 'l')
    var.set_values(points_l)
    var.interpolate()
    polys.append(var)

    var = VariablePolynomial(name, 'r')
    var.set_values(points_r)
    var.interpolate()
    polys.append(var)

    var = VariablePolynomial(name, 'o')
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

  #P_ij
  for i in range(5):
    for j in range(5):
      import_var(f'P{i}{j}01', l_Pij01(i, j), r_Pij01(i, j), o_Pij01(i, j))
      import_var(f'P{i}{j}23', l_Pij23(i, j), r_Pij23(i, j), o_Pij23(i, j))
      import_var(f'P{i}{j}0123', l_Pij0123(i, j), r_Pij0123(i, j), o_Pij0123(i, j))
      import_var(f'P{i}{j}', l_Pij(i, j), r_Pij(i, j), o_Pij(i, j))
      import_var(f'P{i}{j}2', l_Pij2(i, j), r_Pij2(i, j), o_Pij2(i, j))

  #S_ij
  for i in range(5):
    for j in range(i):
      import_var(f'S{i}{j}01', l_Sij01(i, j), r_Sij01(i, j), o_Sij01(i, j))
      import_var(f'S{i}{j}23', l_Sij23(i, j), r_Sij23(i, j), o_Sij23(i, j))
      import_var(f'S{i}{j}0123', l_Sij0123(i, j), r_Sij0123(i, j), o_Sij0123(i, j))
      import_var(f'S{i}{j}', l_Sij(i, j), r_Sij(i, j), o_Sij(i, j))
      import_var(f'S{i}{j}2', l_Sij2(i, j), r_Sij2(i, j), o_Sij2(i, j))

  #D_ij
  for i in range(5):
    for j in range(5):
      import_var(f'Dp{i}{j}', l_Dpij(i, j), r_Dpij(i, j), o_Dpij(i, j))
    
    for j in range(i):
      import_var(f'Dm{i}{j}', l_Dmij(i, j), r_Dmij(i, j), o_Dmij(i, j))

  #T_i
  for i in range(5):
    import_var(f'T{i}12', l_Ti12(i), r_Ti12(i), o_Ti12(i))
    import_var(f'T{i}34', l_Ti34(i), r_Ti34(i), o_Ti34(i))
    import_var(f'T{i}08', l_Ti08(i), r_Ti08(i), o_Ti08(i))
    import_var(f'T{i}76', l_Ti76(i), r_Ti76(i), o_Ti76(i))
    import_var(f'T{i}0876', l_Ti0876(i), r_Ti0876(i), o_Ti0876(i))
    import_var(f'Tp{i}', l_Tpi(i), r_Tpi(i), o_Tpi(i))
    import_var(f'Tm{i}', l_Tmi(i), r_Tmi(i), o_Tmi(i))

  #c_i
  for i in range(5):
    import_var(f'c{i}0', l_ci0(i), r_ci0(i), o_ci0(i))
    import_var(f'c{i}1', l_ci1(i), r_ci1(i), o_ci1(i))
    import_var(f'c{i}2', l_ci2(i), r_ci2(i), o_ci2(i))
    
  #v_one
  import_var('v1', l_v1(), r_v1(), o_v1())

  df = pd.DataFrame() 
  for poly in polys:
    row = pd.concat([pd.DataFrame({'name': poly.name, 'type': poly.type}, index=[0]), pd.DataFrame({f'{len(poly.poly.coeffs)-i}': poly.poly.coeffs[i] for i in range(len(poly.poly.coeffs))}, index=[0])], axis=1)
    df = pd.concat([df, row], ignore_index=True)

  if write:
    df.to_csv('setup.csv')

  return df      

