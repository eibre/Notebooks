import sys, getopt


def ReportRebarData(in_path):
   
    import ifcopenshell
    #in_path = r"X:\nor\oppdrag\Molde2\522\04\52204946\BIM\Innsynsmodell\VOS-RIBarmering.ifc"
    #out_path = in_path
    print(in_path)

    f = ifcopenshell.open(in_path)

    def get_complete_tag(rebar):

        n = ifcopenshell.util.element.get_pset(element=rebar, name="IFC Armering", prop="12 Antall i gruppe")
        ø = ifcopenshell.util.element.get_pset(element=rebar, name="IFC Armering", prop="13 Diameter")
        s = ifcopenshell.util.element.get_pset(element=rebar, name="IFC Armering", prop="14 Senteravstand")
        p1 = ifcopenshell.util.element.get_pset(element=rebar, name="IFC Armering", prop="10 Konstruksjonsdel")
        p2 = ifcopenshell.util.element.get_pset(element=rebar, name="IFC Armering", prop="11 PosNr")
        placement = ifcopenshell.util.element.get_pset(element=rebar, name="IFC Armering", prop="15 Plassering")
        comments = ifcopenshell.util.element.get_pset(element=rebar, name="IFC Armering", prop="16 Kommentar")
        return f'{n}ø{ø}c{s}-{p1}{p2} {placement} {comments}'

    rebars = f.by_type('IfcReinforcingBar')
    print('The model contains:')
    print(f'{len(rebars)} rebars such as {rebars[0].Name}')
    print(get_complete_tag(rebars[0]))
    IfcReinforcingBarTypes = f.by_type('IfcReinforcingBarType')
    print(f'{len(IfcReinforcingBarTypes)} IfcReinforcingBarTypes')
    for IfcReinforcingBarType in IfcReinforcingBarTypes:
        print(f' * {IfcReinforcingBarType.Name}')
    IfcSweptDiskSolid = f.by_type('IfcSweptDiskSolid')
    print(f'{len(IfcSweptDiskSolid)} IfcSweptDiskSolid')
    styleItems = f.by_type('IfcStyledItem')
    print(f'{len(styleItems)} styled items')

    styles = f.by_type('IfcSurfaceStyle')
    print(f'{len(styles)} styles:')

    import ifcopenshell.util
    import ifcopenshell.util.element
    print(ifcopenshell.util.element.get_psets(rebars[0]))

def main(argv):
   inputfile = ''
   outputfile = ''
   opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   for opt, arg in opts:
      if opt == '-h':
         print ('RebarInfo.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   ReportRebarData(inputfile)



if __name__ == "__main__":
   main(sys.argv[1:])


