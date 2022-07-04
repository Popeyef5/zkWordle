from zkwordle.points import *
from zkwordle.util import Variable, fpoly1d, dump_json
from zkwordle.ecc import G1, G2


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
    self.Grho_ls, self.Grho_rs = a_l * self.rho_l, a_r * self.rho_r 
    self.Grho_r2 = rho_r * G2
    self.Grho_o = rho_r * self.rho_l
    self.Grho_os = a_o * self.rho_o
    self.Grho_o2 = (rho_l * rho_r) * G2

  @classmethod
  def random(cls):
    return cls(1, 2, 3, 4, 5, 6, 7, 8)

    
def setup(crs=None):

  if crs is None:
    crs = CRS.random()

  proving_key = {'l': {}, 'ls': {}, 'r': {}, 'rs': {}, 'o': {}, 'os': {}, 'k': {}, 'h': {}}
  verification_key = {'l': {}}

  polys = {}
  
  def import_var(name, points_l, points_r, points_o, visibility=Variable.PRIVATE):
    var = Variable(name=name, visibility=visibility)
    var.set_polynomials(points_l, points_r, points_o)
   
    polys[name] = {} 
    polys[name]['l'] = var.polys['l'].poly
    polys[name]['r'] = var.polys['r'].poly
    polys[name]['o'] = var.polys['o'].poly
   
    l = var.evaluate('l', crs.s) 
    r = var.evaluate('r', crs.s) 
    o = var.evaluate('o', crs.s) 

    proving_key['l'][name] = l * crs.Grho_l
    proving_key['ls'][name] = l * crs.Grho_l
    proving_key['r'][name] = r * crs.Grho_r2
    proving_key['rs'][name] = r * crs.Grho_rs
    proving_key['o'][name] = o * crs.Grho_o
    proving_key['os'][name] = o * crs.Grho_os

    proving_key['k'][name] = (crs.beta * (l * crs.rho_l + r * crs.rho_r + o * crs.rho_o)) * crs.G1

    if visibility==Variable.PUBLIC:
      proving_key['l'][name] = 0 * crs.Grho_l
      proving_key['ls'][name] = 0 * crs.Grho_l
      verification_key['l'][name] = l * crs.Grho_l

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
    
  #v_one
  import_var('v1', l_v1(), r_v1(), o_v1())

  for i in range(356):
    proving_key['h'][i] = (crs.s ** i) * crs.G1

  t = fpoly1d([1])
  for i in range(1, 356):
    t *= fpoly1d([1, -i])

  verification_key['t'] = (t(crs.s) * crs.rho_l * crs.rho_r) * crs.G2
  verification_key['l'] = crs.a_l * crs.G2
  verification_key['r'] = crs.a_r * crs.G1
  verification_key['o'] = crs.a_o * crs.G2
  verification_key['g'] = crs.gamma * crs.G2
  verification_key['bg_1'] = (crs.gamma * crs.beta) * crs.G1
  verification_key['bg_2'] = (crs.gamma * crs.beta) * crs.G2

  return proving_key, verification_key, polys

