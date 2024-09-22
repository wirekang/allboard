# %%
import cadquery

from allboard import entrypoint
from allboard.cq_utils import tapered_cylinder
from allboard.parts import magnet1


def magnet1_cutout(
    bottom_margin=-0.15,
    top_margin=0.15,
    height_margin=0,
):
    return tapered_cylinder(
        magnet1.diameter + bottom_margin,
        magnet1.diameter + top_margin,
        magnet1.height + height_margin,
    )


entrypoint(magnet1_cutout())
