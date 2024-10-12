# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import (
    vertical_key_base_cutout,
)


roof_fillet = 0.8


def make(
    length=15,
    width=6,
    height=6.5,
    roof_length=8.6,
    roof_width=4.8,
    roof_height=1.9,
    post_width=10,
    post_groove_width=0.75,
    post_groove_height=0.75,
    post_groove_y=2,
    post_magnet_y=5.4,
    well_magnet_bottom_margin=-0.15,
    well_magnet_top_margin=0.15,
    well_magnet_height_margin=0,
):
    cutout = vertical_key_base_cutout.make(
        roof_height=roof_height,
        post_width=post_width,
        post_groove_width=post_groove_width,
        post_groove_height=post_groove_height,
        post_groove_y=post_groove_y,
        post_magnet_y=post_magnet_y,
        well_magnet_bottom_margin=well_magnet_bottom_margin,
        well_magnet_top_margin=well_magnet_top_margin,
        well_magnet_height_margin=well_magnet_height_margin,
    ).clean()
    base = (
        Workplane()
        .box(
            length,
            width,
            height,
        )
        .translate((0, width / 2, -height / 2))
        .union(
            Workplane()
            .box(
                roof_length,
                roof_width,
                roof_height,
            )
            .edges("|Z and >Y")
            .fillet(roof_fillet)
            .translate((0, roof_width / 2, roof_height / 2))
        )
        .cut(cutout)
    )

    return base


vscode_main(make)
