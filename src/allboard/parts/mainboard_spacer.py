# %%

from allboard import entrypoint
import allboard.parts.mainboard as mainboard

STL = 1

height = 3.8


def make():

    return (
        mainboard.make()
        .faces("<Z")
        .cut(mainboard.make().translate((0, 0, -mainboard.height)))
        .faces("<Z")
        .wires()
        .toPending()
        .extrude(height, combine=False)
    )


entrypoint(make())
