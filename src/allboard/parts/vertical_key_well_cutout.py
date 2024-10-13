# %%

from cadquery import Workplane
from allboard import vscode_main
from allboard.cq_utils import union_padding
from allboard.parts import magnet1_cutout, vertical_key, vertical_key_post
from allboard.constants import (
    horizontal_magnet_cutout_bottom_margin,
    horizontal_magnet_cutout_top_margin,
    horizontal_magnet_cutout_height_margin,
)

angle = 13
margin_x = 0.5
margin_y = 0.3
margin_z = 0.1


def make(
    post_width=10,
    post_groove_width=0.75,
    post_groove_height=0.75,
    post_groove_y=2.6,
    post_magnet_y=6,
):
    post = (
        vertical_key_post.make(
            length=vertical_key.post_length,
            width=post_width,
            height=vertical_key.height,
            magnet_y=post_magnet_y,
            groove_width=post_groove_width,
            groove_height=post_groove_height,
            groove_y=post_groove_y,
        )
        .union(
            magnet1_cutout.make(
                horizontal_magnet_cutout_bottom_margin * 2,
                horizontal_magnet_cutout_top_margin * 2,
                horizontal_magnet_cutout_height_margin,
            ).translate((0, (post_magnet_y - post_width / 2), vertical_key.height / 2))
        )
        .rotateAboutCenter((1, 0, 0), -90)
    )
    post = union_padding(post, x=margin_x, y=margin_y, z=margin_z)
    post_bb = post.combine().val().BoundingBox()
    post_0 = post.translate((0, 0, -post_bb.zmax))
    result = Workplane()
    for angle_ in range(angle + 1):
        result = result.union(post_0.rotate((1, 0, 0), (0, 0, 0), angle_))
    return result


vscode_main(make)
