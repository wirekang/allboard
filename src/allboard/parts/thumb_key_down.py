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


length = 14.5
width = 26.5
height = 2.5

back_width = 3

post_length = 7.3
post_width = 2.9
post_height = 9


stop_width = 3
stop_height = 5
stop_angle = 7

post_stop_distance = 3

led_y = 22
led_width = 3
led_height = 0.7

magnet_z = 7.5


def make():
    base = (
        Workplane()
        .box(length, width, height)
        .translate(
            (0, width / 2, -height / 2),
        )
    )

    back = (
        Workplane()
        .box(length, back_width + post_width, height)
        .translate(
            (0, -(back_width + post_width) / 2, -height / 2),
        )
    )

    post = (
        Workplane()
        .box(post_length, post_width, post_height)
        .translate((0, -post_width / 2, post_height / 2))
    )

    stop = (
        Workplane()
        .box(length, stop_width, stop_height)
        .translate(
            (
                0,
                stop_width / 2 + post_stop_distance,
                stop_height / 2,
            )
        )
    )

    stop_cutout = (
        Workplane()
        .box(length, stop_width, stop_height * 2)
        .rotateAboutCenter((1, 0, 0), -stop_angle)
        .translate(
            (
                0,
                -stop_width / 2 + post_stop_distance + 0.3,
                stop_height / 2,
            )
        )
    )

    stop = stop.cut(stop_cutout)

    led_ = (
        Workplane()
        .box(length, led_width, led_height)
        .translate(
            (
                0,
                led_y,
                led_height / 2,
            )
        )
    )

    magnet = (
        magnet1_cutout.make(
            horizontal_magnet_cutout_bottom_margin,
            horizontal_magnet_cutout_top_margin,
            horizontal_magnet_cutout_height_margin,
        )
        .rotate((0, 0, 0), (1, 0, 0), -90)
        .translate((0, 0, magnet_z))
    )

    return base.union(post).union(back).union(stop).union(led_).cut(magnet)


vscode_main(make)
