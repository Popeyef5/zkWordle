#!/usr/bin/env python3


def d(x, y):
  return 1 if x == y else 0


def l_aij(i, j):
  ret = [(1+5*i+j, 1)]
   
  for q in range(5):
    ret.append((91+5*i+q, d(j, 0)))
    ret.append((116+5*i+q, d(j, 2)))

    if q > i:
      ret.append((216+sum([n for n in range(q)])+i, d(j, 0)))
      ret.append((226+sum([n for n in range(q)])+i, d(j, 2)))

  s = sum([n for n in range(i)])
  for q in range(i):
    ret.append((216+s+q, d(j, 0))) 
    ret.append((226+s+q, d(j, 2))) 

  return ret 

 
def r_aij(i, j):
  ret = [(1+5*i+j, 1)]

  for q in range(5):
    ret.append((91+5*i+q, d(j, 1)))
    ret.append((116+5*i+q, d(j, 3)))
    ret.append((166+5*i+q, d(j, 4)))

    if q > i:
      ret.append((216+sum([n for n in range(q)])+i, d(j, 1)))
      ret.append((226+sum([n for n in range(q)])+i, d(j, 3)))
      ret.append((246+sum([n for n in range(q)])+i, d(j, 4)))

  s = sum([n for n in range(i)])
  for q in range(i):
    ret.append((216+s+q, d(j, 1))) 
    ret.append((226+s+q, d(j, 3))) 
    ret.append((246+s+q, d(j, 4))) 

  return ret 
 

def o_aij(i, j):
  return [(1+5*i+j, 1)]


def l_wij(i, j):
  ret = [
    (26+5*i+j, 1),
    (61+3*i, d(j, 3)),
    (62+3*i, d(j, 1))
  ]

  for q in range(5):
    ret.append((91+i+5*q, d(j, 0)))
    ret.append((116+i+5*q, d(j, 2)))
  
  return ret


def r_wij(i, j):
  ret = [
    (26+5*i+j, 1), 
    (61+3*i, d(j, 4)), 
    (62+3*i, d(j, 2)), 
    (63+3*i, d(j, 2)), 
  ]

  for q in range(5):
    ret.append((91+i+5*q, d(j, 1)))
    ret.append((116+i+5*q, d(j, 3)))
    ret.append((166+i+5*q, d(j, 4)))

  return ret


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
  return [(336+i, 1)]


def o_rhoi0(i):
  return [(76+i, 1)]


def l_rhoi1(i):
  return []


def r_rhoi1(i):
  return [(341+i, 1)]


def o_rhoi1(i):
  return [(81+i, 1)]


def l_rhoi2(i):
  return []


def r_rhoi2(i):
  return [(346+i, 1)]


def o_rhoi2(i):
  return [(86+i, 1)]


def l_Pij01(i, j):
  return [(141+5*i+j, 1)]


def r_Pij01(i, j):
  return []


def o_Pij01(i, j):
  return [(91+5*i+j, 1)]


def l_Pij23(i, j):
  return []


def r_Pij23(i, j):
  return [(141+5*i+j, 1)]


def o_Pij23(i, j):
  return [(116+5*i+j, 1)]


def l_Pij0123(i, j):
  return [(166+5*i+j, 1)]


def r_Pij0123(i, j):
  return []


def o_Pij0123(i, j):
  return [(141+5*i+j, 1)]


def l_Pij(i, j):
  return [(191+5*i+j, 1)]


def r_Pij(i, j):
  return [(191+5*i+j, 1)]


def o_Pij(i, j):
  return [(166+5*i+j, 1)]


def l_Pij2(i, j):
  return [
    (266+5*i+j, 1),
    (341+i, d(i, j)),
    (346+i, -d(i, j))
  ]


def r_Pij2(i, j):
  ret = [(266+j+5*q, -d(i, j)) for q in range(5)]
  
  for q in range(j+1, 5):
    ret.append((266+sum([n for n in range(q)])+j, -d(i, j)))

  return ret


def o_Pij2(i, j):
  return [(191+5*i+j, 1)]


def l_Sij01(i, j):
  ret = []

  for q in range(j+1, 5):
    ret.append((236+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def r_Sij01(i, j):
  return []


def o_Sij01(i, j):
  ret = [] 

  for q in range(j+1, 5):
    ret.append((216+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def l_Sij23(i, j):
  return []


def r_Sij23(i, j):
  ret = []

  for q in range(j+1, 5):
    ret.append((236+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def o_Sij23(i, j):
  ret = [] 

  for q in range(j+1, 5):
    ret.append((226+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def l_Sij0123(i, j):
  ret = []

  for q in range(j+1, 5):
    ret.append((246+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def r_Sij0123(i, j):
  return []


def o_Sij0123(i, j):
  ret = [] 

  for q in range(j+1, 5):
    ret.append((236+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def l_Sij(i, j):
  ret = []

  for q in range(j+1, 5):
    ret.append((256+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def r_Sij(i, j):
  ret = []

  for q in range(j+1, 5):
    ret.append((256+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def o_Sij(i, j):
  ret = [] 

  for q in range(j+1, 5):
    ret.append((246+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def l_Sij2(i, j):
  ret = []

  for q in range(j+1, 5):
    ret.append((291+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def r_Sij2(i, j):
  return []


def o_Sij2(i, j):
  ret = [] 

  for q in range(j+1, 5):
    ret.append((256+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def l_Dpij(i, j):
  return [
    (301+i, 1),
    (306+i, 1),
    (311+i, 1),
    (316+i, 1)
  ]


def r_Dpij(i, j):
  return [
    (301+i, 1),
    (306+i, 1),
    (311+i, 1),
    (316+i, 1),
    (331+i, 1)
  ]


def o_Dpij(i, j):
  return [(266+5*i+j, 1)]


def l_Dmij(i, j):
  return [
    (301+i, -1),
    (306+i, -1),
    (311+i, -1),
    (316+i, -1)
  ]


def r_Dmij(i, j):
  return [
    (301+i, -1),
    (306+i, -1),
    (311+i, -1),
    (316+i, -1),
    (331+i, -1)
  ]


def o_Dmij(i, j):
  ret = [] 

  for q in range(j+1, 5):
    ret.append((291+sum([n for n in range(q)])+j, d(i, q)))

  return ret


def l_Ti12(i):
  return [(326+i, 1)]


def r_Ti12(i):
  return []


def o_Ti12(i):
  return [(301+i, 1)]


def l_Ti34(i):
  return []


def r_Ti34(i):
  return [(326+i, 1)]


def o_Ti34(i):
  return [(306+i, 1)]


def l_Ti08(i):
  return [(321+i, 1)]


def r_Ti08(i):
  return []


def o_Ti08(i):
  return [(311+i, 1)]


def l_Ti76(i):
  return []


def r_Ti76(i):
  return [(321+i, 1)]


def o_Ti76(i):
  return [(316+i, 1)]


def l_Ti0876(i):
  return [(331+i, 1)]


def r_Ti0876(i):
  return []


def o_Ti0876(i):
  return [(321+i, 1)]


def l_Tpi(i):
  return [(341+i, 1)]


def r_Tpi(i):
  return []


def o_Tpi(i):
  return [(326+i, 1)]


def l_Tmi(i):
  return [(336+i, 1)]


def r_Tmi(i):
  return []


def o_Tmi(i):
  return [(331+i, 1)]


def l_ci0(i):
  return [(351+i, 1)]


def r_ci0(i):
  return []


def o_ci0(i):
  return [(336+i, 1)]


def l_ci1(i):
  return [(351+i, 1)]


def r_ci1(i):
  return []


def o_ci1(i):
  return [(341+i, 1)]


def l_ci2(i):
  return [(351+i, 1)]


def r_ci2(i):
  return []


def o_ci2(i):
  return [(346+i, 1)]


def l_v1():
  ret = []

  for q in range(5):
    ret.append((76+q,  -1))
    ret.append((301+q, -1))
    ret.append((306+q, -3))
    ret.append((316+q, 2))
    ret.append((346+q, 1))

  for q in range(50):
    ret.append((91+q, -1))

  for q in range(20):
    ret.append((216+q, -1))

  return ret


def r_v1():
  ret = []

  for q in range(5):
    ret.append((52+2*q, -3))
    ret.append((62+3*q, -1))
    ret.append((76+q, -2))
    ret.append((81+q, -2))
    ret.append((86+q, -1))
    ret.append((246+q, -1))
    ret.append((301+q, -2))
    ret.append((306+q, -4))
    ret.append((311+q, 1))
    ret.append((316+q, 3))
    ret.append((331+q, 4))
    ret.append((351+q, 1))

  for q in range(25):
    ret.append((91+q, -1))
    ret.append((116+q, -1))
    ret.append((166+q, -1))

  for q in range(20):
    ret.append((216+q, -1))

  for q in range(35):
    ret.append((266+q, 1))

  return ret 


def o_v1():
  return []

