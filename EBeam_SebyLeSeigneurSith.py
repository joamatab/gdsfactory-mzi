import gdsfactory as gf

import ubcpdk.components as pdk
from ubcpdk.tech import LAYER

def MyMZI(DeltaL: int):

    # Create the MZI
    mzi = pdk.mzi(splitter = pdk.ebeam_y_1550, delta_length = DeltaL)

    # Add two fiber grating couplers
    mziWithGratingCouplers = pdk.add_fiber_array(name = "MZI"+str(DeltaL), component = mzi, grating_coupler = pdk.ebeam_gc_te1550, with_loopback = False, gc_port_labels = ["out", "opt_in_TE_1550_SebyleSeigneurSith_MZI" + str(DeltaL)], layer_label = (10,0))

    return mziWithGratingCouplers

# Create the TOP cell for the GDS file
topCell = gf.Component("EBeam_SebyLeSeigneurSith")

# Initialise the DeltaL table
DeltaL_table = [25, 45, 65, 85, 105, 125]
MZI = []

# Defin the floor plan size
floorplan_size = (605, 410)

if __name__ == '__main__':
    
    for i in range(len(DeltaL_table)):

        MZI.append(topCell << MyMZI(DeltaL = DeltaL_table[i]))

        if i<3:
            
            MZI[i].movex(200*(i))

        else:

            MZI[i].movex(200*(i-3))
            MZI[i].movey(-200)

    floor = topCell << gf.components.rectangle(size = floorplan_size, layer = LAYER.FLOORPLAN, name = 'Allowed Zone')
    floor.movex(-90)
    floor.movey(-360)

    topCell.write_gds('./EBeam_SebyLeSeigneurSith.gds')
    
    topCell.show()
  