# %%

from allboard import entrypoint
from allboard.cq_utils import tbox
import allboard.parts.central_pcb as central_pcb

STL = 1

height = 3.8


def central_pcb_spacer():

    return (
        central_pcb.central_pcb()
        .faces("<Z")
        .cut(central_pcb.central_pcb().translate((0, 0, -central_pcb.height)))
        .faces("<Z")
        .wires()
        .toPending()
        .extrude(height, combine=False)
    )


entrypoint(central_pcb_spacer())
