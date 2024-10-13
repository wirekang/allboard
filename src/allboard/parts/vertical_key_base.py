# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import (
    vertical_key_base_cutout,
)


roof_fillet = 0.8


def make(
    height=6.5,
    roof_length=8.6,
    roof_width=4.8,
    roof_height=2.1,
    post_width=10,
    post_groove_width=0.75,
    post_groove_height=0.75,
    post_groove_y=2.5,
    post_magnet_y=6,
    lens_distance=9.2,
):
    cutout = vertical_key_base_cutout.make(
        roof_height=roof_height,
        post_width=post_width,
        post_groove_width=post_groove_width,
        post_groove_height=post_groove_height,
        post_groove_y=post_groove_y,
        post_magnet_y=post_magnet_y,
        lens_distance=lens_distance,
    )
    bb = cutout.BoundingBox()
    base_length = bb.xlen
    base_width = bb.ylen + 0.05
    base_height = height
    base = (
        Workplane()
        .box(base_length, base_width, base_height)
        .translate(((bb.xmax + bb.xmin) / 2, base_width / 2, -base_height / 2))
        .union(
            Workplane()
            .box(
                roof_length,
                roof_width,
                roof_height + 0.2,
            )
            .edges("|Z and >Y")
            .fillet(roof_fillet)
            .translate((0, roof_width / 2, roof_height / 2))
        )
        .cut(cutout.translate((0, 0, 0.02)))
    )

    return base


vscode_main(make)
