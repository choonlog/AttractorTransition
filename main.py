"""
AttractorTransition
Created on 2023
Code author : Chun-Kyung Lee(Korea Advanced Institute of Science and Technology)
Contact: chunkyung@kaist.ac.kr
"""
import AttractorTransition as AT



modeltext = '''
ATP = not MPT
BAX = not BCL2  and  CASP8
BCL2 = NFkB
CASP3 = not XIAP  and  apoptosome
CASP8 = DISCminusTNF  and  not cFLIP or DISCminusFAS  and  not cFLIP or CASP3  and  not cFLIP
Cytc = MOMP
DISCminusFAS = FADD  and  FASL
DISCminusTNF = FADD  and  TNFR
FADD = FADD
FASL = FASL
IKK = RIP1ub
MOMP = MPT or BAX
MPT = not BCL2  and  ROS
NFkB = not CASP3  and  IKK
NonACD = not ATP
RIP1 = not CASP8  and  TNFR or not CASP8  and  DISCminusFAS
RIP1k = RIP1
RIP1ub = RIP1  and  cIAP
ROS = not NFkB  and  RIP1k or MPT  and  not NFkB
SMAC = MOMP
TNF = TNF
TNFR = TNF
XIAP = NFkB  and  not SMAC
apoptosis = CASP3
apoptosome = ATP  and  Cytc  and  not XIAP
cFLIP = NFkB
cIAP = not SMAC  and  cIAP or NFkB  and  not SMAC
survival = NFkB
'''




initial_state = '1010001011100101110000100111'
desired_attractor = '1101111011010000000100011000'
# Parameter_1: Modeltext is a Boolean network string data, consisting of logic operators 'and,' 'or,' and 'not'. It should be sorted in ascending order of the left-hand side nodes.
# Parameter_2: Initial_state is a point attractor at the starting point, and the node states should align with the order of modeltext
# Parameter_3: Desired_attractor is a point attractor or cyclic attractor at the ending point, and the node order should match the order of the modeltext. In the case of a cyclic attractor, cyclic nodes should be indicated with an asterisk '*'.
solution = AT.main(modeltext, initial_state, desired_attractor)
print("FVS(solution)")
print(solution)