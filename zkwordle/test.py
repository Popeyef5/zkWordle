#!/usr/bin/env python3
from zkwordle.ecc import bjj
from zkwordle.pedersen import xl, yl

def d(x, y):
  return 1 if x == y else 0

R1CS_LENGTH = 355
#R1CS_LENGTH = 1110

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

  ret += [
#    (1102-5*i-j, bjj.Gx),
#    (1103-5*i-j, 1),
#    (1104-5*i-j, 1),
#    (1105-5*i-j, 1)
  ]
  
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
  return [
    (26+5*i+j, 1),
#    (1102-5*i-j, bjj.Gy),
#    (1106-5*i-j, bjj.Gx)
  ]


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
    (336+i, d(i, j)),
    (341+i, d(i, j)),
    (346+i, -d(i, j))
  ]


def r_Pij2(i, j):
  ret = [(266+j+5*q, -d(i, j)) for q in range(5)]
  
  for q in range(j+1, 5):
    ret.append((291+sum([n for n in range(q)])+j, -d(i, j)))

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
  return [
    (346+i, 1)
  ]


def l_bmnl(m, n, l):
  return [
#    (356+50*m+n, d(l, 0)),
#    (419+50*m+n, d(l, 0)),
#    (482+50*m+n, d(l, 1)),
#    (608+50*m+n, (yl(m, n, 2)-yl(m, n, 1))*d(l, 0) + (yl(m, n, 3)-yl(m, n, 1))*d(l, 1) + (yl(m, n, 5)-yl(m, n, 1))*d(l, 2)),
#    (671, ((xl(0, 0, 2)-xl(0, 0, 1))*d(l, 0) + (xl(0, 0, 3)-xl(0, 0, 1))*d(l, 1) + (xl(0, 0, 5)-xl(0, 0, 1))*d(l, 2))*d(m, 0)*d(n, 0)),
#    (672+(50*m+n-1)*3, ((xl(m, n, 2)-xl(m, n, 1))*d(l, 0) + (xl(m, n, 3)-xl(m, n, 1))*d(l, 1) + (xl(m, n, 5)-xl(m, n, 1))*d(l, 2))*(1-d(m, 0)*d(n, 0)))
  ]


def r_bmnl(m, n, l):
  return [
#    (356+50*m+n, d(l, 1)),
#    (419+50*m+n, d(l, 2)),
#    (482+50*m+n, d(l, 2)),
#    (545+50*m+n, d(l, 2)),
#    (608+50*m+n, -2*d(l, 3))
  ]


def o_bmnl(m, n, l):
  return [
#    (673+(50*m+n-1)*3, ((xl(m, n, 2)-xl(m, n, 1))*d(l, 0) + (xl(m, n, 3)-xl(m, n, 1))*d(l, 1) + (xl(m, n, 5)-xl(m, n, 1))*d(l, 2))*(1-d(m, 0)*d(n, 0)))
  ] 


def l_blJmn(m, n):
  return [
#    (545+50*m+n, 1),
#    (608+50*m+n, yl(m, n, 4)-yl(m, n, 3)-yl(m, n, 2)+yl(m, n, 1)),
#    (671, (xl(0, 0, 4)-xl(0, 0, 3)-xl(0, 0,2)+xl(0, 0, 1))*d(m ,0)*d(n, 0)),
#    (672+(50*m+n-1)*3, (xl(m, n, 4)-xl(m, n, 3)-xl(m, n, 2)+xl(m, n, 1))*(1-d(m, 0)*d(n, 0)))
  ]


def r_blJmn(m, n):
  return []


def o_blJmn(m, n):
  return [
#    (356+50*m+n, 1),
#    (673+(50*m+n-1)*3, (xl(m, n, 4)-xl(m, n, 3)-xl(m, n, 2)+xl(m, n, 1))*(1-d(m, 0)*d(n, 0)))
  ]
   

def l_bcJmn(m, n):
  return [
#    (608+50*m+n, yl(m, n, 6)-yl(m, n, 5)-yl(m, n, 2)+yl(m, n, 1)),
#    (671, (xl(0, 0, 6)-xl(0, 0, 5)-xl(0, 0,2)+xl(0, 0, 1))*d(m ,0)*d(n, 0)),
#    (672+(50*m+n-1)*3, (xl(m, n, 6)-xl(m, n, 5)-xl(m, n, 2)+xl(m, n, 1))*(1-d(m, 0)*d(n, 0)))
  ]


def r_bcJmn(m, n):
  return []


def o_bcJmn(m, n):
  return [
#    (419+50*m+n, 1),
#    (673+(50*m+n-1)*3, (xl(m, n, 6)-xl(m, n, 5)-xl(m, n, 2)+xl(m, n, 1))*(1-d(m, 0)*d(n, 0)))
  ]
 

def l_buJmn(m, n):
  return [
#    (608+50*m+n, yl(m, n, 7)-yl(m, n, 5)-yl(m, n, 3)+yl(m, n, 1)),
#    (671, (xl(0, 0, 7)-xl(0, 0, 5)-xl(0, 0,3)+xl(0, 0, 1))*d(m ,0)*d(n, 0)),
#    (672+(50*m+n-1)*3, (xl(m, n, 7)-xl(m, n, 5)-xl(m, n, 3)+xl(m, n, 1))*(1-d(m, 0)*d(n, 0)))
  ]


def r_buJmn(m, n):
  return []


def o_buJmn(m, n):
  return [
#    (482+50*m+n, 1),
#    (673+(50*m+n-1)*3, (xl(m, n, 7)-xl(m, n, 5)-xl(m, n, 3)+xl(m, n, 1))*(1-d(m, 0)*d(n, 0)))
  ]
 

def l_bJmn(m, n):
  return [
#    (608+50*m+n, yl(m, n, 8)-yl(m, n, 7)-yl(m, n, 6)+yl(m, n, 5)-yl(m, n, 4)+yl(m, n, 3)+yl(m, n, 2)-yl(m, n, 1)),
#    (671, (xl(0, 0, 8)-xl(0, 0, 7)-xl(0, 0, 6)+xl(0, 0, 5)-xl(m, n, 4)+xl(0, 0, 3)+xl(0, 0, 2)-xl(0, 0, 1))*d(m ,0)*d(n, 0)),
#    (672+(50*m+n-1)*3, (xl(m, n, 8)-xl(m, n, 7)-xl(m, n, 6)+xl(m, n, 5)-xl(m, n, 4)+xl(m, n, 3)+xl(m, n, 2)-xl(m, n, 1))*(1-d(m, 0)*d(n, 0)))
  ]


def r_bJmn(m, n):
  return []


def o_bJmn(m, n):
  return [
#    (545+50*m+n, 1),
#    (673+(50*m+n-1)*3, (xl(m, n, 8)-xl(m, n, 7)-xl(m, n, 6)+xl(m, n, 5)-xl(m, n, 4)+xl(m, n, 3)+xl(m, n, 2)-xl(m, n, 1))*(1-d(m, 0)*d(n, 0)))
  ]


def l_ysmn(m, n):
  return []


def r_ysmn(m, n):
  return []


def o_ysmn(m, n):
  return [
#    (608+50*m+n, 1),
#    (672, -d(m, 0)*d(n, 0)),
#    (672+(50*m+n-1)*3, 1-d(m, 0)*d(n, 0)),
#    (674, d(m, 0)*d(n, 0))
  ]


def l_LQmn(m, n):
  return [
#    (673+(50*m+n-1)*3, 1),
#    (674+(50*m+n-1)*3, 1)
  ]


def r_LQmn(m, n):
  return [
#    (672+(50*m+n-1)*3, 1),
#    (673+(50*m+n-1)*3, 1)
  ]


def o_LQmn(m, n):
  return []

 
def l_LDij(i, j):
  return [
#    (859+(5*i+j)*10, 1),
#    (860+(5*i+j)*10, 1),
#    (861+(5*i+j)*10, 1)
  ]


def r_LDij(i, j):
  return [
#    (860+(5*i+j)*10, 1)
  ]


def o_LDij(i, j):
  return []

 
def l_LAij(i, j):
  return []


def r_LAij(i, j):
  return [
#    (862+(5*i+j)*10, 1),
#    (863+(5*i+j)*10, 1),
#    (866+(5*i+j)*10, 1)
  ]


def o_LAij(i, j):
  return []

 
def l_LAwij(i, j):
  return [
#    (866+(5*i+j)*10, 1),
#    (867+(5*i+j)*10, 1)
  ]


def r_LAwij(i, j):
  return []


def o_LAwij(i, j):
  return [
#    (863+(5*i+j)*10, 1)
  ]

 
def l_Wijx2(i, j):
  return []


def r_Wijx2(i, j):
  return []


def o_Wijx2(i, j):
  return [
#    (858+(5*i+j)*10, 1),
#    (859+(5*i+j)*10, 3)
  ]

 
def l_Vijx(i, j):
  return [
#    (862+(5*i+j)*10, -1)
  ]


def r_Vijx(i, j):
  return [
#    (861+(5*i+j)*10, 1),
#    (867+(5*i+j)*10, -1)
  ]


def o_Vijx(i, j):
  return [
#    (860+(5*i+j)*10, 1),
#    (866+(5*i+j)*10, 1)
  ]

 
def l_Vijy(i, j):
  return []


def r_Vijy(i, j):
  return []


def o_Vijy(i, j):
  return [
#    (861+(5*i+j)*10, 1),
#    (862+(5*i+j)*10, -1),
#    (867+(5*i+j)*10, 1)
  ]

 
def l_Wijx(i, j):
  return [
#    (858+(5*i+j+1)*10, 1-d(i, 4)*d(j, 4)),
#    (1108, d(i, 4)*d(j, 4))
  ]


def r_Wijx(i, j):
  return [
#    (858+(5*i+j+1)*10, 1-d(i, 4)*d(j, 4)),
#    (861+(5*i+j+1)*10, d(i, 4)*d(j, 4)-1),
#    (864+(5*i+j)*10, 1),
#    (867+(5*i+j)*10, 1),
#    (1110, -d(i, 4)*d(j, 4))
  ]


def o_Wijx(i, j):
  return [
#    (860+(5*i+j+1)*10, 2*(1-d(i, 4)*d(j, 4))),
#    (866+(5*i+j)*10, -1),
#    (1109, d(i, 4)*d(j, 4))
  ]

 
def l_Wijy(i, j):
  return []


def r_Wijy(i, j):
  return [
#    (859+(5*i+j+1)*10, 2*(1-d(i, 4)*d(j, 4))),
#    (865+(5*i+j)*10, 1)
  ]


def o_Wijy(i, j):
  return [
#    (861+(5*i+j+1)*10, 1-d(i, 4)*d(j, 4)),
#    (867+(5*i+j)*10, -1),
#    (1108, d(i, 4)*d(j, 4)),
#    (1110, d(i, 4)*d(j, 4))
  ]

 
def l_Wwijx(i, j):
  return []


def r_Wwijx(i, j):
  return []


def o_Wwijx(i, j):
  return [
#    (864+(5*i+j)*10, 1),
#    (866+(5*i+j)*10, 2)
  ]

 
def l_Wwijy(i, j):
  return []


def r_Wwijy(i, j):
  return []


def o_Wwijy(i, j):
  return [
#    (865+(5*i+j)*10, 1),
#    (867+(5*i+j)*10, 2)
  ]

 
def l_LW():
  return [
#    (1109, 1),
#    (1110, 1)
  ]


def r_LW():
  return [
#    (1108, 1),
#    (1109, 1)
  ]


def o_LW():
  return []

 
def l_Wx():
  return []


def r_Wx():
  return [
#    (1110, 1)
  ]


def o_Wx():
  return [
#    (1109, 1)
  ]

 
def l_Wy():
  return []


def r_Wy():
  return []


def o_Wy():
  return [
#    (1110, 1)
  ]


def l_Qmnx(m, n):
  return [
#    (672+(50*m+n)*3, -1),
#    (1108, -d(m, 1)*d(n, 12))
  ]


def r_Qmnx(m, n):
  return [
#    (674+(50*m+n)*3, -1),
#    (674+(50*m+n-1)*3, 1-d(m, 0)*d(n, 0))
  ]


def o_Qmnx(m, n):
  return [
#    (671, d(m, 0)*d(n, 0)),
#    (673+(50*m+n)*3, 1),
#    (673+(50*m+n-1)*3, 1-d(m, 0)*d(n, 0)),
#    (1109, d(m, 1)*d(n, 12))
  ]


def l_Qmny(m, n):
  return []


def r_Qmny(m, n):
  return []


def o_Qmny(m, n):
  return [
#    (672+(50*m+n)*3, d(m, 0)*d(n, 0)-1),
#    (674+(50*m+n)*3, 1),
#    (674+(50*m+n-1)*3, 1-d(m, 0)*d(n, 0)),
#    (1108, -d(m, 1)*d(n, 12))
  ]


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

  for q in range(50):
#    ret.append((608+q, yl(0, q, 1)))
    pass

  for q in range(13):
#    ret.append((608+50+q, yl(1, q, 1)))
    pass
 
#  ret.append((671, xl(0, 0, 1)))
  pass

  for q in range(50):
#    ret.append((672+(q-1)*3, xl(0, q, 1)*(1-d(q, 0))))
    pass

  for q in range(13):
#    ret.append((672+(50+q-1)*3, xl(1, q, 1)))
    pass

  ret.append((858, bjj.Gx))

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
    ret.append((251+q, -1))
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

  for q in range(63):
#    ret.append((608+q, 1))
    pass

  ret += [
#    (671, 1),
    (858, bjj.Gx),
#    (859, 2*bjj.Gy),
    (861, -bjj.Gx)
  ]

  return ret 


def o_v1():
  ret = []

  for q in range(50):
#    ret.append((673+(q-1)*3, xl(0, q, 1)*(1-d(q, 0))))
    pass

  for q in range(13):
#    ret.append((673+(50+q-1)*3, xl(0, q, 1)))
    pass

  for q in range(25):
#    ret.append((859+10*q, bjj.a))
    pass

  ret += [
#    (860, 2*bjj.Gx),
    (861, bjj.Gy)
  ]

  return ret


