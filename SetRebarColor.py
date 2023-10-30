import ifcopenshell
import time
import sys, getopt

def SetRebarColor(in_path):

    #INPUT:
    #in_path = r"C:\Users\eibre\OneDrive - Norconsult Group\Documents\VOS-RIBarmering.ifc"
    out_path = in_path#[:-4]+"_color.ifc"
    pset_name = 'IFC Armering'
    property_name = '11 PosNr'
    colours = [
        [255, 255, 0], [0, 255, 255], [255, 0, 255], [0, 0, 255], [255, 153, 0], [255, 0, 0], [0, 204, 255], [153, 204, 0], [255, 102, 0], [255, 0, 255], [128, 0, 0], [128, 128, 0], [0, 128, 0], [0, 128, 128], [0, 0, 128], [128, 0, 128], [255, 128, 128], [255, 255, 153], [51, 153, 102], [153, 204, 255], [255, 153, 0], [51, 102, 255], [51, 153, 102], [255, 204, 153], [255, 255, 0], [0, 0, 255], [153, 153, 255], [51, 204, 204], [128, 0, 128], [0, 128, 128], [128, 128, 0], [255, 128, 128], [51, 102, 255], [255, 153, 204], [255, 204, 153], [128, 0, 128], [0, 128, 0], [255, 204, 0], [51, 102, 255], [51, 102, 255], [0, 255, 0], [153, 153, 255], [255, 255, 0], [255, 0, 255], [51, 204, 204], [51, 102, 255], [204, 204, 255], [51, 102, 255], [204, 255, 204], [255, 0, 0], [0, 0, 255], [51, 153, 102], [255, 255, 0], [255, 153, 0], [153, 204, 255], [255, 102, 0], [204, 153, 255], [204, 204, 255], [255, 153, 204], [51, 51, 153], [255, 255, 0], [0, 0, 255], [153, 153, 255], [51, 204, 204], [128, 0, 128], [0, 128, 128], [128, 128, 0], [255, 128, 128], [51, 102, 255], [255, 153, 204], [255, 0, 0], [0, 0, 255], [51, 153, 102], [255, 255, 0], [255, 153, 0], [153, 204, 255], [255, 102, 0], [204, 153, 255], [204, 204, 255], [255, 153, 204]
    ]

    # Script starts:
    t_start = time.perf_counter()

    print(f"Opening file at {in_path}")
    f = ifcopenshell.open(in_path)

    rebars = f.by_type('IfcReinforcingBar')
    print(f'The model contains {len(rebars)} rebars')
    IfcSweptDiskSolid = f.by_type('IfcSweptDiskSolid')
    print(f'The model contains {len(IfcSweptDiskSolid)} IfcSweptDiskSolid')
    styleItems = f.by_type('IfcStyledItem')
    print(f'The model contains {len(styleItems)} styled items')
    styles = f.by_type('IfcSurfaceStyle')
    print(f'The model contains {len(styles)} styles:')

    for style in styles:
        print(f' * {style.Name}')
    def get_propery_value(rebar, pset_name, p_name):
        for pset in rebar.IsDefinedBy:
            if pset.RelatingPropertyDefinition.Name == pset_name:
                for property in pset.RelatingPropertyDefinition.HasProperties:
                    if property.Name == p_name:
                        return property.NominalValue[0]

    import collections
    from collections import defaultdict
    rebar_dict = defaultdict(list)
    print(f"Grouping rebar by values of property {property_name} in pset {pset_name}")
    for k,v in zip([int(get_propery_value(rebar, pset_name, property_name)) for rebar in rebars], rebars):
        rebar_dict[k].append(v)
        
    ordered_rebars = collections.OrderedDict(sorted(rebar_dict.items()))
    num_groups = len(ordered_rebars)
    print(f"Found {num_groups} different groups")

    import math
    colours = colours*math.ceil(num_groups/len(colours))
    colours = colours[:num_groups]
    rgb_colours = list()

    for rgb in colours:
        rgb_colours.append(f.createIfcColourRgb(None, rgb[0]/255, rgb[1]/255, rgb[2]/255))
        
    if(len(styleItems) > 10):
        print("Removing existing IfcStyledItems")
        for styleItem in styleItems:
            f.remove(styleItem)

    i=0
    print("Creating styled items for rebar color..")
    for k, group in ordered_rebars.items():
        colour = rgb_colours[i]
        print(f"Group where {property_name} = {k} contains {len(group)} elements")
        surfaceStyleShading = f.createIfcSurfaceStyleShading()
        surfaceStyleShading.SurfaceColour = colour
        surfaceStyle = f.createIfcSurfaceStyle(colour.Name, "BOTH",(surfaceStyleShading,))
        presStyleAssign = f.createIfcPresentationStyleAssignment((surfaceStyle,))
        i=i+1
        for rebar in group:
            item = rebar.Representation.Representations[0].Items[0]
            f.createIfcStyledItem(item, (presStyleAssign,), None)
            
    print(f"Saving file to {out_path}..")
    f.write(out_path)
    t_end = time.perf_counter()
    print(f"File saved, script completed in in {t_end-t_start:0.4f} seconds")

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
   SetRebarColor(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])