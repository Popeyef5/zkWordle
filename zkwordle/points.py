#!/usr/bin/env python3
from zkwordle.ecc import bjj
from zkwordle.pedersen import xl, yl

def d(x, y):
  return 1 if x == y else 0

R1CS_LENGTH = 1320

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

  ret += [
    (1309-11*(5*i+j), bjj.Gx*(1-d(i, 4)*d(j, 4))),
    (1310-11*(5*i+j), (bjj.Gy-1)*(1-d(i, 4)*d(j, 4))),
    (1312-11*(5*i+j), (bjj.Gx + bjj.Gy -1)*(1-d(i, 4)*d(j, 4)))
  ]

  return ret


def o_wij(i, j):
  return [
    (26+5*i+j, 1),
    (1049, bjj.Gx*d(i, 4)*d(j, 4)),
    (1050, (bjj.Gy-1)*d(i, 4)*d(j, 4))
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
    (356+50*m+n, d(l, 0)),
    (419+50*m+n, d(l, 0)),
    (482+50*m+n, d(l, 1)),
    (608+50*m+n, (xl(m, n, 2)-xl(m, n, 1))*d(l, 0) + (xl(m, n, 3)-xl(m, n, 1))*d(l, 1) + (xl(m, n, 5)-xl(m, n, 1))*d(l, 2)),
  ]


def r_bmnl(m, n, l):
  return [
    (356+50*m+n, d(l, 1)),
    (419+50*m+n, d(l, 2)),
    (482+50*m+n, d(l, 2)),
    (545+50*m+n, d(l, 2)),
    (608+50*m+n, -2*d(l, 3)),
    (672+(50*m+n)*6, (yl(m, n, 2)-yl(m, n, 1))*d(l, 0) + (yl(m, n, 3)-yl(m, n, 1))*d(l, 1) + (yl(m, n, 5)-yl(m, n, 1))*d(l, 2)),
    (674+(50*m+n)*6, (yl(m, n, 2)-yl(m, n, 1))*d(l, 0) + (yl(m, n, 3)-yl(m, n, 1))*d(l, 1) + (yl(m, n, 5)-yl(m, n, 1))*d(l, 2)),
  ]


def o_bmnl(m, n, l):
  return [
  ] 


def l_blJmn(m, n):
  return [
    (545+50*m+n, 1),
    (608+50*m+n, xl(m, n, 4)-xl(m, n, 3)-xl(m, n, 2)+xl(m, n, 1)),
  ]


def r_blJmn(m, n):
  return [
    (672+(50*m+n)*6, yl(m, n, 4)-yl(m, n, 3)-yl(m, n, 2)+yl(m, n, 1)),
    (674+(50*m+n)*6, yl(m, n, 4)-yl(m, n, 3)-yl(m, n, 2)+yl(m, n, 1)),
  ]


def o_blJmn(m, n):
  return [
    (356+50*m+n, 1),
  ]
   

def l_bcJmn(m, n):
  return [
    (608+50*m+n, xl(m, n, 6)-xl(m, n, 5)-xl(m, n, 2)+xl(m, n, 1)),
  ]


def r_bcJmn(m, n):
  return [
    (672+(50*m+n)*6, yl(m, n, 6)-yl(m, n, 5)-yl(m, n, 2)+yl(m, n, 1)),
    (674+(50*m+n)*6, yl(m, n, 6)-yl(m, n, 5)-yl(m, n, 2)+yl(m, n, 1)),
  ]


def o_bcJmn(m, n):
  return [
    (419+50*m+n, 1),
  ]
 

def l_buJmn(m, n):
  return [
    (608+50*m+n, xl(m, n, 7)-xl(m, n, 5)-xl(m, n, 3)+xl(m, n, 1)),
  ]


def r_buJmn(m, n):
  return [
    (672+(50*m+n)*6, yl(m, n, 7)-yl(m, n, 5)-yl(m, n, 3)+yl(m, n, 1)),
    (674+(50*m+n)*6, yl(m, n, 7)-yl(m, n, 5)-yl(m, n, 3)+yl(m, n, 1)),
  ]


def o_buJmn(m, n):
  return [
    (482+50*m+n, 1),
  ]
 

def l_bJmn(m, n):
  return [
    (608+50*m+n, xl(m, n, 8)-xl(m, n, 7)-xl(m, n, 6)+xl(m, n, 5)-xl(m, n, 4)+xl(m, n, 3)+xl(m, n, 2)-xl(m, n, 1)),
  ]


def r_bJmn(m, n):
  return [
    (672+(50*m+n)*6, yl(m, n, 8)-yl(m, n, 7)-yl(m, n, 6)+yl(m, n, 5)-yl(m, n, 4)+yl(m, n, 3)+yl(m, n, 2)-yl(m, n, 1)),
    (674+(50*m+n)*6, yl(m, n, 8)-yl(m, n, 7)-yl(m, n, 6)+yl(m, n, 5)-yl(m, n, 4)+yl(m, n, 3)+yl(m, n, 2)-yl(m, n, 1)),
  ]


def o_bJmn(m, n):
  return [
    (545+50*m+n, 1),
  ]


def l_Rmnx(m, n):
  return [
  ]


def r_Rmnx(m, n):
  return [
    (671+6*(50*m+n), 1),
    (674+6*(50*m+n), 1),
  ]


def o_Rmnx(m, n):
  return [
    (608+50*m+n, 1),
  ]


def l_QRxmn(m, n):
  return [
    (673+6*(50*m+n), bjj.JUBJUB_D.s),
  ]


def r_QRxmn(m, n):
  return []


def o_QRxmn(m, n):
  return [
    (671+6*(50*m+n), 1),
    (675+6*(50*m+n), -1),
    (676+6*(50*m+n), -bjj.JUBJUB_A.s),
  ]


def l_QRymn(m, n):
  return []


def r_QRymn(m, n):
  return [
    (673+6*(50*m+n), 1),
  ]


def o_QRymn(m, n):
  return [
    (672+6*(50*m+n), 1),
    (675+6*(50*m+n), -1),
    (676+6*(50*m+n), 1),
  ]


def l_QRdmn(m, n):
  return []


def r_QRdmn(m, n):
  return [
    (675+6*(50*m+n), 1),
    (676+6*(50*m+n), -1),
  ]


def o_QRdmn(m, n):
  return [
    (673+6*(50*m+n), 1),
  ]


def l_QRsmn(m, n):
  return []


def r_QRsmn(m, n):
  return []


def o_QRsmn(m, n):
  return [
    (674+6*(50*m+n), 1),
    (675+6*(50*m+n), 1),
  ]


def l_Qmnx(m, n):
  return [
    (671+6*(50*m+n+1), 1-d(m, 1)*d(n, 12)),
    (674+6*(50*m+n+1), 1-d(m, 1)*d(n, 12)),
    (675+6*(50*m+n), 1),
    (1315, d(m, 1)*d(n, 12)),
    (1318, d(m, 1)*d(n, 12)),
  ]


def r_Qmnx(m, n):
  return []


def o_Qmnx(m, n):
  return []


def l_Qmny(m, n):
  return [
    (672+6*(50*m+n+1), 1-d(m, 1)*d(n, 12)),
    (674+6*(50*m+n+1), 1-d(m, 1)*d(n, 12)),
    (676+6*(50*m+n), 1),
    (1316, d(m, 1)*d(n, 12)),
    (1318, d(m, 1)*d(n, 12)),
  ]


def r_Qmny(m, n):
  return []


def o_Qmny(m, n):
  return []


def l_Wijx2(i, j):
  return []


def r_Wijx2(i, j):
  return [
    (1054+(5*i+j)*11, bjj.JUBJUB_A.s*(1-d(i, 4)*d(j, 4))),
    (1055+(5*i+j)*11, -bjj.JUBJUB_A.s*(1-d(i, 4)*d(j, 4))),
  ]


def o_Wijx2(i, j):
  return [
    (1051+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1055+(5*i+j)*11, -bjj.JUBJUB_A.s*(1-d(i, 4)*d(j, 4))),
  ]

 
def l_Wijy2(i, j):
  return []


def r_Wijy2(i, j):
  return [
    (1054+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1055+(5*i+j)*11, -1+d(i, 4)*d(j, 4)),
  ]


def o_Wijy2(i, j):
  return [
    (1052+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1055+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
  ]

 
def l_Wijxy(i, j):
  return []


def r_Wijxy(i, j):
  return []


def o_Wijxy(i, j):
  return [
    (1053+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1054+(5*i+j)*11, 2*(1-d(i, 4)*d(j, 4))),
  ]

 
def l_Vijx(i, j):
  return [
    (1054+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
    (1056+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
    (1059+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
  ]


def r_Vijx(i, j):
  return []


def o_Vijx(i, j):
  return []

 
def l_Vijy(i, j):
  return [
    (1055+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
    (1057+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
    (1059+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
  ]


def r_Vijy(i, j):
  return []


def o_Vijy(i, j):
  return []

  
def l_Vwxij(i, j):
  return [
    (1058+(5*i+j-1)*11, bjj.JUBJUB_D.s*(1-d(i, 0)*d(j, 0))),
  ]


def r_Vwxij(i, j):
  return []


def o_Vwxij(i, j):
  return [
    (1056+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
    (1060+(5*i+j-1)*11, -1+d(i, 0)*d(j, 0)),
    (1061+(5*i+j-1)*11, -bjj.JUBJUB_A.s*(1-d(i, 0)*d(j, 0))),
  ]

  
def l_Vwyij(i, j):
  return []


def r_Vwyij(i, j):
  return [
    (1058+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
  ]


def o_Vwyij(i, j):
  return [
    (1057+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
    (1060+(5*i+j-1)*11, -1+d(i, 0)*d(j, 0)),
    (1061+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
  ]

 
def l_Vwdij(i, j):
  return []


def r_Vwdij(i, j):
  return [
    (1060+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
    (1061+(5*i+j-1)*11, -1+d(i, 0)*d(j, 0)),
  ]


def o_Vwdij(i, j):
  return [
    (1058+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
  ]

 
def l_Vwsij(i, j):
  return []


def r_Vwsij(i, j):
  return []


def o_Vwsij(i, j):
  return [
    (1059+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
    (1060+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
  ]


def l_Wijx(i, j):
  return [
    (1049, d(i, 0)*d(j, 0)),
    (1051+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1053+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1060+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
  ]


def r_Wijx(i, j):
  return [
    (1051+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1315, d(i, 4)*d(j, 4)),
    (1318, d(i, 4)*d(j, 4)),
  ]


def o_Wijx(i, j):
  return []

 
def l_Wijy(i, j):
  return [
    (1050, d(i, 0)*d(j, 0)),
    (1052+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1061+(5*i+j-1)*11, 1-d(i, 0)*d(j, 0)),
  ]


def r_Wijy(i, j):
  return [
    (1052+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1053+(5*i+j)*11, 1-d(i, 4)*d(j, 4)),
    (1316, d(i, 4)*d(j, 4)),
    (1318, d(i, 4)*d(j, 4)),
  ]


def o_Wijy(i, j):
  return []


def l_QWx():
  return [
    (1317, bjj.JUBJUB_D.s),
  ]


def r_QWx():
  return []


def o_QWx():
  return [
    (1315, 1),
    (1319, -1),
    (1320, -bjj.JUBJUB_A.s),
  ]

 
def l_QWy():
  return []


def r_QWy():
  return [
    (1317, 1),
  ]


def o_QWy():
  return [
    (1316, 1),
    (1319, -1),
    (1320, 1),
  ]


def l_QWd():
  return []


def r_QWd():
  return [
    (1319, 1),
    (1320, -1),
  ]


def o_QWd():
  return [
    (1317, 1),
  ]


def l_QWs():
  return []


def r_QWs():
  return []


def o_QWs():
  return [
    (1318, 1),
    (1319, 1),
  ]


def l_Wx():
  return [
    (1319, 1),
  ]


def r_Wx():
  return []


def o_Wx():
  return []

 
def l_Wy():
  return [
    (1320, 1),
  ]


def r_Wy():
  return []


def o_Wy():
  return []


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

  for q in range(63):
    m, n = q // 50, q % 50
    ret.append((608+q, xl(m, n, 1)))

  ret += [
    (671, 0),
    (672, 1),
    (674, 1),
  ]

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
    ret.append((608+q, 1))

  for q in range(63):
    m, n = q // 50, q % 50
    ret.append((672+6*q, yl(m, n, 1)))
    ret.append((674+6*q, yl(m, n, 1)))
    ret.append((675+6*q, 1))
    ret.append((676+6*q, 1))

  for q in range(24):
    ret.append((1055+11*q, 2))
    ret.append((1057+11*q, 1))
    ret.append((1059+11*q, 1))
    ret.append((1060+11*q, 1))
    ret.append((1061+11*q, 1))

  ret += [
    (1049, 1),
    (1050, 1),
    (1319, 1),
    (1320, 1),
  ]

  return ret 


def o_v1():
  ret = []

  ret += [
    (1050, 1),
  ]

  return ret


