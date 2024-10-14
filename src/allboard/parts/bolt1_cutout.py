# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import bolt1
from allboard.constants import sacrificial_layer_height

nut_length = 6
nut_width = 6
nut_height = 3

thickness = 2.5


def make(
    margin_nut_length=0,
    margin_nut_width=0,
):
    c1 = (
        Workplane()
        .cylinder(
            thickness,
            bolt1.diameter / 2,
        )
        .translate((0, 0, -thickness / 2))
    )

    nut = (
        Workplane()
        .box(nut_length + margin_nut_length, nut_width + margin_nut_width, nut_height)
        .translate((0, 0, -nut_height / 2 - thickness - sacrificial_layer_height))
    )

    return c1.union(nut)


vscode_main(make)
