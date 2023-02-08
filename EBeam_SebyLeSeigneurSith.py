import gdsfactory as gf

import ubcpdk.components as pdk
from ubcpdk.tech import LAYER

def MyMZI(DeltaL: int):

    # Create the MZI
    mzi =  pdk.mzi(splitter = pdk.ebeam_y_1550, delta_length = DeltaL)

    topToBottom = mzi.size_info.se

    # Add two fiber grating couplers
    mziWithGratingCouplers = pdk.add_fiber_array(grating_coupler= pdk.gc_te1550, name = "MZI"+str(DeltaL), component = mzi, with_loopback = False, gc_port_labels = ["out", "opt_in_TE_1550_SebyleSeigneurSith_MZI" + str(DeltaL)], layer_label = (10,0), fanout_length  = topToBottom[1]+1, straight_separation = 0)
    
    return mziWithGratingCouplers

# Create the TOP cell for the GDS file
topCell = gf.Component("EBeam_SebyLeSeigneurSith")

# Initialise the DeltaL table
DeltaL_table = [25, 45, 65, 85, 105, 125]
MZI = []

# Defin the floor plan size
floorplan_size = (605, 410)

if __name__ == '__main__':

    gf.clear_cache()
    
    for i in range(len(DeltaL_table)):

        MZI.append(topCell << MyMZI(DeltaL = DeltaL_table[i]))
       

        if i<3:
            
            MZI[i].movex(150*(i))

        else:

            MZI[i].movex(150*(i-3))
            MZI[i].movey(-200)

    # Add the de-embedding structure
    DeEmbeddingStructure = topCell << pdk.add_fiber_array(name = 'DeEmbeddingStructure', with_loopback=False, gc_port_labels = ["out", "opt_in_TE_1550_SebyleSeigneurSith_DeEmbeddingStructure"], layer_label = (10,0), fanout_length = 1, straight_separation = 0)
    DeEmbeddingStructure.movex(origin = 0, destination = 150*3)
    topCell.align(elements=[DeEmbeddingStructure, MZI[2]], alignment='ymin')

    # Add the floor plan
    floor = topCell << gf.components.rectangle(size = floorplan_size, layer = LAYER.FLOORPLAN, name = 'Allowed Zone')
    floor.movex(-100)
    floor.movey(-340)

    topCell.write_gds('./EBeam_SebyLeSeigneurSith.gds')
    
    topCell.show(show_ports= True)
