EX Version: 2
Region: /
!#nodeset nodes
Shape. Dimension=0
#Fields=1
1) coordinates, coordinate, rectangular cartesian, real, #Components=3
 x. #Values=2 (value,d/ds1)
 y. #Values=2 (value,d/ds1)
 z. #Values=2 (value,d/ds1)
Node: 1
 -1.479162494069713e+00  0.000000000000000e+00
 -5.688841365188414e+00  0.000000000000000e+00
  8.316505803184116e+02  0.000000000000000e+00
Node: 2
 -6.633272951118450e-01  0.000000000000000e+00
 -1.088684182666644e+01  0.000000000000000e+00
  8.313722720681664e+02  0.000000000000000e+00
Node: 3
 -1.985135291068078e+00  0.000000000000000e+00
 -1.746282118900751e+01  0.000000000000000e+00
  8.308973484455781e+02  0.000000000000000e+00
Node: 4
 -2.011647113917304e+00  0.000000000000000e+00
 -2.338444896505831e+01  0.000000000000000e+00
  8.305453828914985e+02  0.000000000000000e+00
Node: 5
 -1.233912891216252e+00  0.000000000000000e+00
 -2.921598540984682e+01  0.000000000000000e+00
  8.285286603000318e+02  0.000000000000000e+00
Node: 6
  9.659000000000035e-01  0.000000000000000e+00
 -5.817000000000003e+01  0.000000000000000e+00
  8.079999999999998e+02  0.000000000000000e+00
!#mesh mesh1d, dimension=1, nodeset=nodes
Shape. Dimension=1, line
#Scale factor sets=0
#Nodes=2
#Fields=1
1) coordinates, coordinate, rectangular cartesian, real, #Components=3
 x. c.Hermite, no modify, standard node based.
  #Nodes=2
  1. #Values=2
   Value labels: value d/ds1
  2. #Values=2
   Value labels: value d/ds1
 y. c.Hermite, no modify, standard node based.
  #Nodes=2
  1. #Values=2
   Value labels: value d/ds1
  2. #Values=2
   Value labels: value d/ds1
 z. c.Hermite, no modify, standard node based.
  #Nodes=2
  1. #Values=2
   Value labels: value d/ds1
  2. #Values=2
   Value labels: value d/ds1
Element: 1
 Nodes:
 1 2
Element: 2
 Nodes:
 2 3
Element: 3
 Nodes:
 3 4
Element: 4
 Nodes:
 4 5
Element: 5
 Nodes:
 5 6
