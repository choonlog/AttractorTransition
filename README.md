# AttractorTransition
AttractorTransition is a Python package designed for implementing
attractor-transition control for complex biological networks modelled as
Boolean networks (BNs). It utilizes similarity between initial and final
attractors and Boolean algebraic properties of underlying state transition
equations. The package simplifies the BN expression through the coordinate
transformation and systematically identifies control inputs. It can handle
fixed-point attractors as well as cyclic ones as demonstrated in numerical
experiments. A related paper is expected to be published soon.

## Installation
You can simply download AttractorTransition from this git repository, while
setup.py is not provided. AttractorTransition is executed on any operating
system (Windows, Mac OS, Linux, etc), but Python 3.5 or higher versions must
be installed to run the program.

## Output
It ultimately produces attractor-transition control inputs as the output set.

## Example
The following function is in main.py:
```
import AttractorTransition as AT

initial_state = '1010001011100101110000100111'
desired_attractor = '1101111011010000000100011000'
# Parameter_1: Modeltext is a Boolean network string data, consisting of
logic operators 'and,' 'or,' and 'not'. It should be sorted in ascending
order of the left-hand side nodes.
# Parameter_2: Initial_state is a point attractor at the starting point, and
the node states should align with the order of modeltext.
# Parameter_3: Desired_attractor is a point attractor or cyclic attractor at
the ending point, and the node order should match the order of the modeltext.
In the case of a cyclic attractor, cyclic nodes should be indicated with an
asterisk '*'.
solution = AT.main(modeltext, initial_state, desired_attractor)
print("FVS(solution)")
print(solution)
```

Parameter_1 is in the following format.
```
ATP = not MPT
BAX = not BCL2  and  CASP8
BCL2 = NFkB
CASP3 = not XIAP  and  apoptosome
CASP8 = DISCminusTNF  and  not cFLIP or DISCminusFAS  and  not cFLIP or CASP3
and  not cFLIP
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
```

## Supplementary materials
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/90976609-95a6-400a-b537-a18e79c3ba40.png" width="800"/>
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/53783db2-4d21-4b2e-b11d-8eda9977aa56.png" width="800"/>
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/3e81fb1c-f458-4a93-8453-7de761eb7f17.png" width="800"/>
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/755448fa-b77f-4662-bb81-f7c976f9dbe1.png" width="800"/>
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/672904a5-df0a-481d-82ad-f5888f21dc0d.png" width="800"/>
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/00a1e364-25c0-47af-8460-4a2f72fb72e2.png" width="800"/>
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/e77a332a-cfca-44ba-91eb-5c5ba81f676c.png" width="800"/>
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/59243dc7-fd40-4c09-be1c-1871e1ee49e9.png" width="800"/>
<img src="https://github.com/choonlog/AttractorTransition/assets/22069522/52851a86-848a-46dd-b856-839a903f350d" width="800"/>



