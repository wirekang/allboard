# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import cluster_key_down, led_cutout, magnet1_cutout
from allboard.constants import (
    horizontal_magnet_cutout_bottom_margin,
    horizontal_magnet_cutout_top_margin,
    horizontal_magnet_cutout_height_margin,
)

post_margin = 1


def make(
    length=16,
    width=16,
    height=6.5,
    lens_distance=10,
):
    post_left = (
        Workplane()
        .box(
            cluster_key_down.post_length + post_margin,
            cluster_key_down.post_width + post_margin,
            cluster_key_down.post_height,
        )
        .translate(
            (-cluster_key_down.post_distance / 2, 0, -cluster_key_down.post_height / 2)
        )
    )

    post_right = (
        Workplane()
        .box(
            cluster_key_down.post_length + post_margin,
            cluster_key_down.post_width + post_margin,
            cluster_key_down.post_height,
        )
        .translate(
            (cluster_key_down.post_distance / 2, 0, -cluster_key_down.post_height / 2)
        )
    )

    post_base = (
        Workplane()
        .box(
            cluster_key_down.post_distance,
            cluster_key_down.post_width + post_margin,
            cluster_key_down.post_base_height + post_margin,
        )
        .translate(
            (0, 0, -height + cluster_key_down.post_base_height / 2 + post_margin / 2)
        )
    )

    magnet = magnet1_cutout.make(
        horizontal_magnet_cutout_bottom_margin,
        horizontal_magnet_cutout_top_margin,
        horizontal_magnet_cutout_height_margin,
    )

    led = led_cutout.make(lens_distance).rotateAboutCenter((0, 0, 1), 90)

    base = Workplane().box(length, width, height).translate((0, 0, -height / 2))

    result = base.cut(post_left).cut(post_right).cut(post_base).cut(led).cut(magnet)
    return result


vscode_main(make)
