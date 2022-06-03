#!/usr/bin/env python3


def d(x, y):
  return 1 if x == y else 0


def l_aij(i, j):
  return [
    (1+5*i+j, 1),
    (91+5*i, d(j, 0)),
    (92+5*i, d(j, 0)),
    (93+5*i, d(j, 0)),
    (94+5*i, d(j, 0)),
    (95+5*i, d(j, 0)),
    (116+5*i, d(j, 2)),
    (117+5*i, d(j, 2)),
    (118+5*i, d(j, 2)),
    (119+5*i, d(j, 2)),
    (120+5*i, d(j, 2)),
    (216+i, 2**j),
    (221+i, 2**j),
    (251+i, 2**j)
  ]
 
def r_aij(i, j):
  return [
    (1+5*i+j, 1),
    (91+5*i, d(j, 1)),
    (92+5*i, d(j, 1)),
    (93+5*i, d(j, 1)),
    (94+5*i, d(j, 1)),
    (95+5*i, d(j, 1)),
    (116+5*i, d(j, 3)),
    (117+5*i, d(j, 3)),
    (118+5*i, d(j, 3)),
    (119+5*i, d(j, 3)),
    (120+5*i, d(j, 3)),
    (166+5*i, d(j, 4)),
    (167+5*i, d(j, 4)),
    (168+5*i, d(j, 4)),
    (169+5*i, d(j, 4)),
    (170+5*i, d(j, 4)),
    (216+i, 2**j),
    (221+i, 2**j),
    (231+i, 2**j)
  ]
 
def o_aij(i, j):
  return [(1+5*i+j, 1)]

def l_wij(i, j):
  return [
    (26+5*i+j, 1), 
    (61+3*i, d(j, 3)), 
    (62+3*i, d(j, 1)), 
    (91+i, d(j, 0)), 
    (96+i, d(j, 0)), 
    (101+i, d(j, 0)), 
    (106+i, d(j, 0)), 
    (111+i, d(j, 0)), 
    (116+i, d(j, 2)), 
    (121+i, d(j, 2)), 
    (126+i, d(j, 2)), 
    (131+i, d(j, 2)), 
    (136+i, d(j, 2)), 
    (216, -1*d(i, 0)*2**j),
    (217, -1*d(i, 0)*2**j),
    (218, -1*d(i, 0)*2**j),
    (219, -1*d(i, 0)*2**j),
    (220, -1*d(i, 0)*2**j),
    (221, -1*d(i, 2)*2**j),
    (222, -1*d(i, 2)*2**j),
    (223, -1*d(i, 2)*2**j),
    (224, -1*d(i, 2)*2**j),
    (225, -1*d(i, 2)*2**j),
    (251+i, -1*2**j)
  ]

def r_wij(i, j):
  return [
    (26+5*i+j, 1), 
    (61+3*i, d(j, 4)), 
    (62+3*i, d(j, 2)), 
    (63+3*i, d(j, 2)), 
    (91+i, d(j, 1)), 
    (96+i, d(j, 1)), 
    (101+i, d(j, 1)), 
    (106+i, d(j, 1)), 
    (111+i, d(j, 1)), 
    (116+i, d(j, 3)), 
    (121+i, d(j, 3)), 
    (126+i, d(j, 3)), 
    (131+i, d(j, 3)), 
    (136+i, d(j, 3)), 
    (166+i, d(j, 4)), 
    (171+i, d(j, 4)), 
    (176+i, d(j, 4)), 
    (181+i, d(j, 4)), 
    (186+i, d(j, 4)), 
    (216, -1*d(i, 1)*2**j),
    (217, -1*d(i, 1)*2**j),
    (218, -1*d(i, 1)*2**j),
    (219, -1*d(i, 1)*2**j),
    (220, -1*d(i, 1)*2**j),
    (221, -1*d(i, 3)*2**j),
    (222, -1*d(i, 3)*2**j),
    (223, -1*d(i, 3)*2**j),
    (224, -1*d(i, 3)*2**j),
    (225, -1*d(i, 3)*2**j),
    (231, -1*d(i, 4)*2**j),
    (232, -1*d(i, 4)*2**j),
    (233, -1*d(i, 4)*2**j),
    (234, -1*d(i, 4)*2**j),
    (235, -1*d(i, 4)*2**j),
  ]

def o_wij(i, j):
  return [(26+5*i+j, 1)]

def l_wi34(i):
  return [(63+3*i, 1)]

def r_wi34(i):
  return []

def o_wi34(i):
  return [(61+3*i, 1)]

def l_wi12(i):
  return []

def r_wi12(i):
  return [(63+3*i, 1)]

def o_wi12(i):
  return [(62+3*i, 1)]

def l_ri(i):
  return [
    (51+2*i, 1),
    (76+i, 1),
    (81+i, 1),
    (86+i, 1)
  ]

def r_ri(i):
  return [
    (51+2*i, 1),
    (52+2*i, 1),
    (76+i, 1),
    (81+i, 1),
    (86+i, 1)
  ]

def o_ri(i):
  return [(52+2*i, -2)]

def l_ri2(i):
  return [(52+2*i, 1)]

def r_ri2(i):
  return []

def o_ri2(i):
  return [(51+2*i, 1)]

def l_rhoi0(i):
  return []

def r_rhoi0(i):
  return [(241+i, 1)]

def o_rhoi0(i):
  return [(76+i, 1)]

def l_rhoi1(i):
  return []

def r_rhoi1(i):
  return [(246+i, 1)]

def o_rhoi1(i):
  return [(81+i, 1)]

def l_rhoi2(i):
  return []

def r_rhoi2(i):
  return [(251+i, 1)]

def o_rhoi2(i):
  return [(86+i, 1)]

def l_Pij12(i, j):
  return [(141+5*i+j, 1)]

def r_Pij12(i, j):
  return []

def o_Pij12(i, j):
  return [(91+5*i+j, 1)]

def l_Pij34(i, j):
  return []

def r_Pij34(i, j):
  return [(141+5*i+j, 1)]

def o_Pij34(i, j):
  return [(116+5*i+j, 1)]

def l_Pij1234(i, j):
  return [(166+5*i+j, 1)]

def r_Pij1234(i, j):
  return []

def o_Pij1234(i, j):
  return [(141+5*i+j, 1)]

def l_Pij(i, j):
  return [(191+5*i+j, 1)]

def r_Pij(i, j):
  return [(191+5*i+j, 1)]

def o_Pij(i, j):
  return [(166+5*i+j, 1)]

def l_Pij2(i, j):
  return [
    (241+i, 1),
    (246+i, d(i, j))
  ]

def r_Pij2(i, j):
  return []

def o_Pij2(i, j):
  return [(191+5*i+j, 1)]

def l_Di12(i):
  return [(226+i, 1)]

def r_Di12(i):
  return []

def o_Di12(i):
  return [(216+i, 1)]

def l_Di34(i):
  return []

def r_Di34(i):
  return [(226+i, 1)]

def o_Di34(i):
  return [(221+i, 1)]

def l_Di1234(i):
  return [(231+i, 1)]

def r_Di1234(i):
  return []

def o_Di1234(i):
  return [(226+i, 1)]

def l_Di(i):
  return [(236+i, 1)]

def r_Di(i):
  return [(236+i, 1)]

def o_Di(i):
  return [(231+i, 1)]

def l_Di2(i):
  return [(246+i, 1)]

def r_Di2(i):
  return []

def o_Di2(i):
  return [(236+i, 1)]

def l_ci0(i):
  return [(256+i, 1)]

def r_ci0(i):
  return []

def o_ci0(i):
  return [(241+i, 1)]

def l_ci1(i):
  return [(256+i, 1)]

def r_ci1(i):
  return []

def o_ci1(i):
  return [(246+i, 1)]

def l_ci2(i):
  return [(256+i, 1)]

def r_ci2(i):
  return []

def o_ci2(i):
  return [(251+i, 1)]

def l_v1():
  ret = []
  for i in range(5):
    ret.append((76+i,  -1))

  for i in range(50):
    ret.append((91+i, -1))

  return ret

def r_v1():
  ret = []
  for i in range(5):
    ret.append((52+2*i, -3))
    ret.append((62+3*i, -1))
    ret.append((76+i, -2))
    ret.append((81+i, -2))
    ret.append((86+i, -1))
    ret.append((256+i, 1))

  for i in range(25):
    ret.append((91+i, -1))
    ret.append((116+i, -1))
    ret.append((166+i, -1))

  return ret 

def o_v1():
  return []

