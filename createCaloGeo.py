# module for creating the FLUKA geometry of the FOOT calorimeter
# A. Mereghetti, 2023/11/03
# python version: >= 3.8.10

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "externals/pyFLUKAgeo"))
from grid import Grid
from geometry import acquireGeometries, Geometry
sys.path.append(os.path.join(os.path.dirname(__file__), "pyLib"))
from InputParsers import FOOTpGeoParser, CaloGeoParser
    
def testActualGeo(lDebug=True):
    BaseNames, BaseLabs, GlobCoords, GlobAngles = FOOTpGeoParser("/media/sf_vb_share/docs_FLUKAcalo/FOOT.geo",myEles="Calo")
    crysIDs, crysCoords, crysAngles = CaloGeoParser("/media/sf_vb_share/docs_FLUKAcalo/TACAdetector.geo",grab="crys")
    modIDs, modCoords, modAngles = CaloGeoParser("/media/sf_vb_share/docs_FLUKAcalo/TACAdetector.geo",grab="mod")

def testRegularSingleProto(lDebug=False):
    # user input
    # - grid of centers on a spherical shell
    R=100
    dR=50
    NR=1
    Tmax=14.0  # theta [degs] --> range: -Tmax:Tmax
    NT=15      # number of steps (i.e. grid cells)
    Pmax=23.0  # phi [degs] --> range: -Pmax:Pmax
    NP=24      # number of steps (i.e. grid cells)
    # - prototypes to use:
    fileNames=[ "caloCrys.inp" ] ; geoNames=fileNames
    protoName="caloCrys.inp"

    # actual processing
    # - hive geometry
    HiveGeo=Geometry.DefineHive_SphericalShell(R,R+dR,NR,-Tmax,Tmax,NT,-Pmax,Pmax,NP,lDebug=lDebug)
    if (lDebug):
        HiveGeo.echo("hive.inp")

    # - gridded crystals
    #   acquire geometries
    myProtoGeos=acquireGeometries(fileNames,geoNames=geoNames);
    cellGrid=Grid.SphericalShell(R,R+dR,NR,-Tmax,Tmax,NT,-Pmax,Pmax,NP,lDebug=lDebug)
    myProtoList=[ protoName for ii in range(len(cellGrid)) ]
    GridGeo=Geometry.BuildGriddedGeo(cellGrid,myProtoList,myProtoGeos,osRegNames=["OUTER"],lDebug=lDebug)
    if (lDebug):
        GridGeo.echo("grid.inp")

    # - merge geometries
    mergedGeo=Geometry.MergeGeos(HiveGeo,GridGeo,lDebug=lDebug)
    mergedGeo.echo("merged.inp")

if (__name__=="__main__"):
    # testRegularSingleProto(lDebug=False)
    testActualGeo(lDebug=True)
