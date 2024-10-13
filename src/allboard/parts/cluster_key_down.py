# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import magnet1_cutout
from allboard.constants import (
    horizontal_magnet_cutout_bottom_margin,
    horizontal_magnet_cutout_top_margin,
    horizontal_magnet_cutout_height_margin,
)

STL = 1


diameter = 15
height = 2
rim_thickness = 1
rim_height = 0.5

post_length = 3.5
post_width = 3.5
post_height = 10
post_distance = 8.3
post_base_height = 2.7
post_fillet = 0.4


def make():
    base = (
        Workplane()
        .cylinder(height, diameter / 2, centered=False)
        .cut(
            Workplane(
                origin=(rim_thickness, rim_thickness, height - rim_height)
            ).cylinder(99, diameter / 2 - rim_thickness, centered=False)
        )
    ).translate((-diameter / 2, -diameter / 2))

    def post(xm=1):
        return (
            Workplane()
            .box(post_length, post_width, post_height)
            .edges(">Z")
            .fillet(post_fillet)
            .cut(
                magnet1_cutout.make(
                    horizontal_magnet_cutout_bottom_margin,
                    horizontal_magnet_cutout_top_margin,
                    horizontal_magnet_cutout_height_margin,
                ).translate((0, 0, post_height / 2))
            )
            .translate(
                (
                    post_distance / 2 * xm,
                    0,
                    post_height / 2 + height - rim_height,
                )
            )
        )

    post_base = (
        Workplane()
        .box(
            diameter - rim_thickness * 2 - post_fillet * 3,
            post_width,
            post_base_height,
        )
        .translate((0, 0, height + post_base_height / 2 - rim_height))
    )

    return base.union(post(-1)).union(post()).union(post_base)


vscode_main(make)
