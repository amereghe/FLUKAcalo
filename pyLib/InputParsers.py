# module for parsing various input files
# A. Mereghetti, 2023/12/17
# python version: >= 3.8.10

import numpy as np

def FOOTpGeoParser(FileName,myEles=None,lDebug=False):
    '''
    parser of the FOOT.geo file.
    myEles is a list of elements for which the info should be
       extracted (either basename or label); if None or "ALL",
       no filter based on name matching is performed after parsing
    '''
    BaseNames=[]; BaseLabs=[]; Coords=[]; Angles=[]
    print("parsing file %s..."%(FileName))
    ff=open(FileName,"r")
    for tmpLine in ff.readlines():
        if (tmpLine.startswith("//")):
            # a comment line
            continue
        elif (len(tmpLine.strip())==0):
            # empty line
            continue
        if ("BaseName" in tmpLine):
            myPos=tmpLine.find("BaseName")
            BaseLabs.append(tmpLine[0:myPos])
            myBaseName=tmpLine.split()[1]
            BaseNames.append(myBaseName.replace('"',''))
        elif("PosX" in tmpLine):
            data=tmpLine.split()
            Coords.append(np.array(data[1:6:2]))
        elif("AngX" in tmpLine):
            data=tmpLine.split()
            Angles.append(np.array(data[1:6:2]))
    ff.close()
    if (len(Coords)!=len(BaseNames)):
        print("...problem in parsing: found %d coordinate sets and %d basenames!"%(len(Coords),len(BaseNames)))
        exit(1)
    if (len(Angles)!=len(BaseNames)):
        print("...problem in parsing: found %d angle sets and %d basenames!"%(len(Angles),len(BaseNames)))
        exit(1)
    print("...done: found %d sub-detectors;"%(len(BaseNames)))

    if ( myEles is not None ):
       print("...apply filtering...")
       if ( myEles is str ):
           if ( myEles.upper()!="ALL" ):
               # apply filter
               if (myEles in BaseNames):
                   print("...found %s in BaseNames;"%(myEles))
                   myId=BaseNames.index()
                   BaseNames=[BaseNames[myId]]
                   BaseLabs=[BaseLabs[myId]]
                   Coords=[Coords[myId]]
                   Angles=[Angles[myId]]
               elif (myEles in BaseNames):
                   print("...found %s in BaseLabs;"%(myEles))
                   myId=BaseLabs.index()
                   BaseNames=[BaseNames[myId]]
                   BaseLabs=[BaseLabs[myId]]
                   Coords=[Coords[myId]]
                   Angles=[Angles[myId]]
       elif ( "ALL" not in [tmpStr.upper() for tmpStr in myEles] ):
           # apply filter
           for BaseName,BaseLab in zip(reversed(BaseNames),reversed(BaseLabs)):
               if (BaseName not in myEles and BaseLab not in myEles):
                   myId=BaseNames.index(BaseName)
                   BaseNames.pop(myId)
                   BaseLabs.pop(myId)
                   Coords.pop(myId)
                   Angles.pop(myId)
            # echo what's left in:
           for BaseName,BaseLab in zip(BaseNames,BaseLabs):
               print("...keeping %s/%s;"%(BaseName,BaseLab))
    print("...returning infos for %d sub-detectors;"%(len(BaseNames)))
    return BaseNames, BaseLabs, Coords, Angles
    
def CaloGeoParser(FileName,grab="crys",lDebug=False):
    '''
    parser of the TACAdetector.geo file.
    For the time being, it extracts positions/angles of crystals or
      modules - NOT BOTH AT THE SAME TIME
    '''
    IDs=[]; Coords=[]; Angles=[]
    if (grab.upper().startswith("CRY")):
        myWhat="crystal"
        myGrab="CrystalId"
    elif (grab.upper().startswith("MOD")):
        myWhat="module"
        myGrab="ModuleId"
    else:
        print("...grabbing %s: what is it?"%(grab))
        exit(1)
        
    print("grabbing %s infos in file %s..."%(myWhat,FileName))
    ff=open(FileName,"r")
    lRead=False
    for tmpLine in ff.readlines():
        if (tmpLine.startswith(myGrab)):
            lRead=True
            IDs.append(int(tmpLine.split()[1]))
        elif (lRead and tmpLine.startswith("PositionX:")):
            data=tmpLine.split()
            Coords.append(np.array(data[1:6:2]))
        elif (lRead and tmpLine.startswith("TiltX:")):
            data=tmpLine.split()
            Angles.append(np.array(data[1:6:2]))
            lRead=False
    ff.close()
    if (len(Coords)!=len(IDs)):
        print("...problem in parsing: found %d coordinate sets and %d IDs!"%(len(Coords),len(IDs)))
        exit(1)
    if (len(Angles)!=len(IDs)):
        print("...problem in parsing: found %d angle sets and %d IDs!"%(len(Angles),len(IDs)))
        exit(1)
    
    print("...done: acquired %d %s data sets;"%(len(IDs),myWhat))
    return IDs, Coords, Angles
            
            
