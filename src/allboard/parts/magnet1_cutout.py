# %%

from allboard import vscode_main
from allboard.cq_utils import tapered_cylinder
from allboard.parts import magnet1


def make(
    bottom_margin=-0.15,
    top_margin=0.15,
    height_margin=0.0,
):
    height = magnet1.height + height_margin
    return tapered_cylinder(
        magnet1.diameter + bottom_margin,
        magnet1.diameter + top_margin,
        height,
    ).translate((0, 0, -height))


vscode_main(make)
