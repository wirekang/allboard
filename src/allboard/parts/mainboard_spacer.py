# %%

from allboard import entrypoint
import allboard.parts.mainboard as mainboard

STL = 1

height = 3.8


def mainboard_spacer():

    return (
        mainboard.mainboard()
        .faces("<Z")
        .cut(mainboard.mainboard().translate((0, 0, -mainboard.height)))
        .faces("<Z")
        .wires()
        .toPending()
        .extrude(height, combine=False)
    )


entrypoint(mainboard_spacer())
