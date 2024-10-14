# %%

from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import magnet1_cutout, vertical_key, vertical_key_post
from allboard.constants import (
    horizontal_magnet_cutout_bottom_margin,
    horizontal_magnet_cutout_top_margin,
    horizontal_magnet_cutout_height_margin,
)

margin_length = 1
margin_width = 2.5
margin_groove_width = -0.2
margin_groove_height = -0.3


def make(
    post_width=10,
    post_groove_width=0.75,
    post_groove_height=0.75,
    post_groove_y=3,
    post_magnet_y=6,
    angle=13,
):
    post = (
        vertical_key_post.make(
            length=vertical_key.post_length + margin_length,
            width=post_width + margin_width,
            height=vertical_key.height,
            magnet_y=post_magnet_y,
            groove_width=post_groove_width + margin_groove_width,
            groove_height=post_groove_height + margin_groove_height,
            groove_y=post_groove_y,
        )
        .union(
            magnet1_cutout.make(
                horizontal_magnet_cutout_bottom_margin * 2,
                horizontal_magnet_cutout_top_margin * 2,
                horizontal_magnet_cutout_height_margin,
            ).translate(
                (
                    0,
                    (post_magnet_y - (post_width + margin_width) / 2),
                    vertical_key.height / 2,
                )
            )
        )
        .rotateAboutCenter((1, 0, 0), -90)
    )
    post_bb = post.combine().val().BoundingBox()
    post_0 = post.translate((0, 0, -post_bb.zmax))
    result = Workplane()
    for angle_ in range(angle + 1):
        result = result.union(post_0.rotate((1, 0, 0), (0, 0, 0), angle_))
    return result


vscode_main(make)
