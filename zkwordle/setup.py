from zkwordle.points import *
from zkwordle.util import dump_json, load_json
from zkwordle.helpers import Variable, fpoly1d
from zkwordle.ecc.bn128 import G1, G2

import time

class CRS:
  
  def __init__(self, s, rho_l, rho_r, a_l, a_r, a_o, beta, gamma):
    self.s = s
    self.rho_l, self.rho_r = rho_l, rho_r
    self.rho_o = rho_l * rho_r
    self.a_l, self.a_r, self.a_o = a_l, a_r, a_o
    self.gamma = gamma
    self.beta = beta

    self.G1, self.G2 = G1, G2

    self.Grho_l, self.Grho_r = rho_l * G1, rho_r * G1
    self.Grho_ls, self.Grho_rs = a_l * self.Grho_l, a_r * self.Grho_r 
    self.Grho_r2 = rho_r * G2
    self.Grho_rs2 = self.a_r * self.Grho_r2
    self.Grho_o = rho_r * self.Grho_l
    self.Grho_os = a_o * self.Grho_o
    self.Grho_o2 = (rho_l * rho_r) * G2

  @classmethod
  def random(cls):
    return cls(2000, 2, 3, 4, 5, 6, 7, 8)

    
def setup(crs=None, load_polys=None, save_polys=None):
  st = time.monotonic()
  if crs is None:
    crs = CRS.random()

  proving_key = {'l': {}, 'ls': {}, 'r': {}, 'rs': {}, 'o': {}, 'os': {}, 'k': {}, 'h': {}}
  verification_key = {'l_pub': {}}

  polys = {}
  if load_polys is not None:
    data = load_json(load_polys)
    for name in data:
      polys[name] = {}
      for type, poly_dict in data[name].items():
        polys[name][type] = fpoly1d(poly_dict["coeffs"], poly_dict["prime"])

  print(f"poly load done in {time.monotonic() - st}s")

  
  def import_var(name, points_l, points_r, points_o, visibility=Variable.PRIVATE):
    t1 = time.monotonic()
    if name in polys:
      var = Variable.from_polys(polys[name], name, visibility)
    else:
      var = Variable(name=name, visibility=visibility)
      var.set_polynomials(points_l, points_r, points_o)
   
      polys[name] = {} 
      polys[name]['l'] = var.polys['l'].poly
      polys[name]['r'] = var.polys['r'].poly
      polys[name]['o'] = var.polys['o'].poly
    
    t2 = time.monotonic()
   
    l = var.evaluate('l', crs.s) 
    r = var.evaluate('r', crs.s) 
    o = var.evaluate('o', crs.s)

    t3 = time.monotonic()

    proving_key['l'][name] = l * crs.Grho_l
    proving_key['ls'][name] = l * crs.Grho_ls
    proving_key['r'][name] = r * crs.Grho_r2
    proving_key['rs'][name] = r * crs.Grho_rs
    proving_key['o'][name] = o * crs.Grho_o
    proving_key['os'][name] = o * crs.Grho_os

    proving_key['k'][name] = (crs.beta * (l * crs.rho_l + r * crs.rho_r + o * crs.rho_o)) * crs.G1

    t4 = time.monotonic()

    print(f"Import finished. Setup: {(t2-t1)/(t4-t1)}. Evaluation: {(t3-t2)/(t4-t1)}. Key prep: {(t4-t3)/(t4-t1)}")

    if visibility==Variable.PUBLIC:
      proving_key['l'][name] = 0 * crs.Grho_l
      proving_key['ls'][name] = 0 * crs.Grho_l
      verification_key['l_pub'][name] = l * crs.Grho_l

  #a_ij
  for i in range(5):
    for j in range(5):
      import_var(f'a{i}{j}', l_aij(i, j), r_aij(i, j), o_aij(i, j), Variable.PUBLIC)

  #w_ij
  for i in range(5):
    for j in range(5):
      import_var(f'w{i}{j}', l_wij(i, j), r_wij(i, j), o_wij(i, j))
    import_var(f'w{i}34', l_wi34(i), r_wi34(i), o_wi34(i))
    import_var(f'w{i}12', l_wi12(i), r_wi12(i), o_wi12(i))

  #r_i
  for i in range(5):
    import_var(f'r{i}', l_ri(i), r_ri(i), o_ri(i), Variable.PUBLIC)

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

  #W
  import_var('Wx', l_Wx(), r_Wx(), o_Wx(), Variable.PUBLIC)
  import_var('Wy', l_Wy(), r_Wy(), o_Wy(), Variable.PUBLIC)

  #b_mnl
  for q in range(63):
    m, n = q // 50, q % 50
    for l in range(4):
      import_var(f'b{m}{n}{l}', l_bmnl(m, n, l), r_bmnl(m, n, l), o_bmnl(m, n, l))

  #bl&_mn
  for q in range(63):
    m, n = q // 50, q % 50
    import_var(f'bl&{m}{n}', l_blJmn(m, n), r_blJmn(m, n), o_blJmn(m, n))
  
  #bc&_mn
  for q in range(63):
    m, n = q // 50, q % 50
    import_var(f'bc&{m}{n}', l_bcJmn(m, n), r_bcJmn(m, n), o_bcJmn(m, n))
  
  #bu&_mn
  for q in range(63):
    m, n = q // 50, q % 50
    import_var(f'bu&{m}{n}', l_buJmn(m, n), r_buJmn(m, n), o_buJmn(m, n))
  
  #b&_mn
  for q in range(63):
    m, n = q // 50, q % 50
    import_var(f'b&{m}{n}', l_bJmn(m, n), r_bJmn(m, n), o_bJmn(m, n))
 
  #R_mnx
  for q in range(63):
    m, n = q // 50, q % 50
    import_var(f'R{m}{n}x', l_Rmnx(m, n), r_Rmnx(m, n), o_Rmnx(m, n))

  #Q loop
  for q in range(63):
    m, n = q // 50, q % 50
    import_var(f'QRx{m}{n}', l_QRxmn(m, n), r_QRxmn(m, n), o_QRxmn(m, n))
    import_var(f'QRy{m}{n}', l_QRymn(m, n), r_QRymn(m, n), o_QRymn(m, n))
    import_var(f'QRd{m}{n}', l_QRdmn(m, n), r_QRdmn(m, n), o_QRdmn(m, n))
    import_var(f'QRs{m}{n}', l_QRsmn(m, n), r_QRsmn(m, n), o_QRsmn(m, n))

  #Q_mn
  for q in range(63):
    m, n = q // 50, q % 50
    import_var(f'Q{m}{n}x', l_Qmnx(m, n), r_Qmnx(m, n), o_Qmnx(m, n))
    import_var(f'Q{m}{n}y', l_Qmny(m, n), r_Qmny(m, n), o_Qmny(m, n))

  #W_ij
  for q in range(25):
    i, j = q // 5, q % 5
    import_var(f'W{i}{j}x', l_Wijx(i, j), r_Wijx(i, j), o_Wijx(i, j))
    import_var(f'W{i}{j}y', l_Wijy(i, j), r_Wijy(i, j), o_Wijy(i, j))
  
  for q in range(24):
    i, j = q // 5, q % 5
    import_var(f'W{i}{j}x2', l_Wijx2(i, j), r_Wijx2(i, j), o_Wijx2(i, j))
    import_var(f'W{i}{j}y2', l_Wijy2(i, j), r_Wijy2(i, j), o_Wijy2(i, j))
    import_var(f'W{i}{j}xy', l_Wijxy(i, j), r_Wijxy(i, j), o_Wijxy(i, j))
  
  #V_ij
  for q in range(1, 25):
    i, j = q // 5, q % 5
    import_var(f'V{i}{j}x', l_Vijx(i, j), r_Vijx(i, j), o_Vijx(i, j))
    import_var(f'V{i}{j}y', l_Vijy(i, j), r_Vijy(i, j), o_Vijy(i, j))
    import_var(f'Vwx{i}{j}', l_Vwxij(i, j), r_Vwxij(i, j), o_Vwxij(i, j))
    import_var(f'Vwy{i}{j}', l_Vwyij(i, j), r_Vwyij(i, j), o_Vwyij(i, j))
    import_var(f'Vwd{i}{j}', l_Vwdij(i, j), r_Vwdij(i, j), o_Vwdij(i, j))
    import_var(f'Vws{i}{j}', l_Vwsij(i, j), r_Vwsij(i, j), o_Vwsij(i, j))
  
  #QW
  import_var(f'QWx', l_QWx(), r_QWx(), o_QWx())
  import_var(f'QWy', l_QWy(), r_QWy(), o_QWy())
  import_var(f'QWd', l_QWd(), r_QWd(), o_QWd())
  import_var(f'QWs', l_QWs(), r_QWs(), o_QWs())

  #v_one
  import_var('v1', l_v1(), r_v1(), o_v1(), Variable.PUBLIC)

  t1 = time.monotonic()

  for i in range(R1CS_LENGTH+1):
    proving_key['h'][i] = (crs.s ** i) * crs.G1

  if save_polys is not None:
    dump_json(polys, save_polys)

  t2 = time.monotonic()
  
  t = fpoly1d([1])
  for i in range(1, R1CS_LENGTH+1):
    t *= fpoly1d([1, -i])

  t_s = t(crs.s)

  t3 = time.monotonic()

  proving_key['lt'] = t_s * crs.Grho_l
  proving_key['rt'] = t_s * crs.Grho_r2
  proving_key['ot'] = t_s * crs.Grho_o
  proving_key['lts'] = t_s * crs.Grho_ls
  proving_key['rts'] = t_s * crs.Grho_rs
  proving_key['ots'] = t_s * crs.Grho_os
  proving_key['ltb'] = t_s * crs.beta * crs.Grho_l
  proving_key['rtb'] = t_s * crs.beta * crs.Grho_r
  proving_key['otb'] = t_s * crs.beta * crs.Grho_o

  verification_key['t'] = (t_s * crs.rho_l * crs.rho_r) * crs.G2
  verification_key['l'] = crs.a_l * crs.G2
  verification_key['r'] = crs.a_r * crs.G1
  verification_key['o'] = crs.a_o * crs.G2
  verification_key['g'] = crs.gamma * crs.G2
  verification_key['bg_1'] = (crs.gamma * crs.beta) * crs.G1
  verification_key['bg_2'] = (crs.gamma * crs.beta) * crs.G2

  et = time.monotonic()
  print(f"Finished setup in {et-st}s.")
  print(f"variable import: {(t1-st)/(et-st)}. Proving h: {(t2-t1)/(et-st)}. T: {(t3-t2)/(et-st)}. Key setup: {(et-t3)/(et-st)}.")

  return proving_key, verification_key, polys

