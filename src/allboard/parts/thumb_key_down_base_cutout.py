# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import led_cutout, magnet1_cutout, thumb_key_down
from allboard.constants import (
    horizontal_magnet_cutout_bottom_margin,
    horizontal_magnet_cutout_top_margin,
    horizontal_magnet_cutout_height_margin,
)


margin_length = 1.5
margin_width = 3
post_margin_length = 1.5
post_margin_width = 3


def make(
    height=6.2,
    led_distance=20,
):
    length = thumb_key_down.length + margin_length
    width = thumb_key_down.width - thumb_key_down.post_stop_distance + margin_width
    base = (
        Workplane()
        .box(
            length,
            width,
            height,
        )
        .translate((0, width / 2 + thumb_key_down.post_stop_distance, -height / 2))
    )

    post = (
        Workplane()
        .box(
            thumb_key_down.post_length + post_margin_length,
            thumb_key_down.post_width + post_margin_width,
            (thumb_key_down.post_height + thumb_key_down.height),
        )
        .translate(
            (
                0,
                -thumb_key_down.post_width / 2 - post_margin_width / 2,
                (thumb_key_down.post_height + thumb_key_down.height) / 2 - height,
            )
        )
    )

    magnet = (
        magnet1_cutout.make(
            horizontal_magnet_cutout_bottom_margin,
            horizontal_magnet_cutout_top_margin,
            horizontal_magnet_cutout_height_margin,
        )
        .rotate((0, 0, 0), (1, 0, 0), 90)
        .translate(
            (
                0,
                0,
                thumb_key_down.magnet_z - height,
            )
        )
    )

    led_ = led_cutout.make(led_distance).translate((0, thumb_key_down.led_y, 0))

    return base.union(post).union(magnet).union(led_)


vscode_main(make)
