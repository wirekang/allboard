# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.cq_utils import tbox
from allboard.parts import magnet1_cutout
from allboard.constants import (
    horizontal_magnet_cutout_bottom_margin,
    horizontal_magnet_cutout_top_margin,
    horizontal_magnet_cutout_height_margin,
)


def make(
    length=7.3,
    width=10,
    height=1.7,
    magnet_y=6,
    groove_width=0.75,
    groove_height=0.7,
    groove_y=2.5,
):
    return (
        Workplane()
        .box(length, width, height)
        .edges("<Y")
        .fillet(height / 2 - 0.00001)
        .cut(
            magnet1_cutout.make(
                bottom_margin=horizontal_magnet_cutout_bottom_margin,
                top_margin=horizontal_magnet_cutout_top_margin,
                height_margin=horizontal_magnet_cutout_height_margin,
            ).translate((0, -width / 2 + magnet_y, height / 2))
        )
        .cut(
            tbox(
                length,
                groove_width,
                groove_height,
                (
                    0,
                    -width / 2 + groove_y,
                    -height / 2 + groove_height / 2,
                ),
            )
        )
    )


vscode_main(make)
