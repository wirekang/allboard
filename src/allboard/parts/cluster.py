# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import (
    bolt1,
    bolt1_cutout,
    cluster_key_down_base_cutout,
    vertical_key_base_cutout,
)
from allboard.constants import sacrificial_layer_height

STL = 1
DXF = 1


length = 25
width = 48
height = 6.5
head_fillet = 5
tail_fillet = 12.2

roof_length = 8.6
roof_width = 4.8
roof_height = 2
roof_fillet = 0.8

post_width = 10
post_groove_width = 0.75
post_groove_height = 0.75
post_groove_y = 3.1
post_magnet_y = 5.5


connector_cutout_length = 12
connector_cutout_width = 2.4
connector_cutout_height = 2.5
connector_cutout_y = 15.5

pcb_screw_cutout_y = 20.7

led_distance = 12
led_distance_north = 14
led_distance_down = 9.9


south_margin = 0
north_margin = 0

adapter_screw_cutout_y = -16.5
adapter_screw_cutout_z = -2

key_angle = 15

led_margin_y = 0.6
led_margin_y_south = 0.8
led_margin_y_north = 1

tail_cut = 4


def make():
    vertical_base_cutout = Workplane()
    vertical_base_roof = Workplane()

    def f_vertical_base_cutout(angle, d, lm):
        vertical_base_cutout.add(
            vertical_key_base_cutout.make(
                roof_height,
                post_width,
                post_groove_width,
                post_groove_height,
                post_groove_y,
                post_magnet_y,
                led_distance=d,
                angle=key_angle,
                led_margin_y=lm,
            )
            .translate((0, -length / 2, 0))
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
        vertical_base_roof.add(
            Workplane()
            .box(roof_length, roof_width, roof_height + 0.2)
            .edges("|Z")
            .fillet(roof_fillet)
            .translate(
                (
                    0,
                    -length / 2 + roof_width / 2,
                    roof_height / 2 + 0.1,
                )
            )
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )

    f_vertical_base_cutout(0, led_distance, led_margin_y_south)
    f_vertical_base_cutout(90, led_distance, led_margin_y)
    f_vertical_base_cutout(180, led_distance_north, led_margin_y_north)
    f_vertical_base_cutout(270, led_distance, led_margin_y)

    down_base_cutout = cluster_key_down_base_cutout.make(height, led_distance_down)

    connector_cutout = (
        Workplane()
        .box(
            connector_cutout_length,
            connector_cutout_width,
            connector_cutout_height,
        )
        .translate((0, connector_cutout_y, -connector_cutout_height / 2))
    )

    pcb_screw_cutout = bolt1_cutout.make(margin_nut_width=1).translate(
        (0, pcb_screw_cutout_y, 0)
    )

    adapter_screw_cutout = (
        Workplane()
        .cylinder(-adapter_screw_cutout_z, bolt1.diameter / 2)
        .translate((0, adapter_screw_cutout_y, adapter_screw_cutout_z / 2))
        .union(
            Workplane()
            .box(
                bolt1.diameter * 1.5,
                bolt1.diameter * 1.5,
                height + adapter_screw_cutout_z,
            )
            .translate(
                (
                    0,
                    adapter_screw_cutout_y,
                    adapter_screw_cutout_z
                    - (height + adapter_screw_cutout_z) / 2
                    - sacrificial_layer_height,
                )
            )
        )
    )

    base = (
        Workplane()
        .box(length, width, height)
        .translate((0, 0, -height / 2))
        .cut(
            Workplane()
            .box(length, width, height)
            .translate((0, -width + tail_cut, -height / 2)),
        )
        .edges("|Z and >Y")
        .fillet(head_fillet)
        .edges("|Z and <Y")
        .fillet(tail_fillet)
    )

    return (
        base.union(vertical_base_roof)
        .cut(vertical_base_cutout)
        .cut(down_base_cutout)
        .cut(connector_cutout)
        .cut(pcb_screw_cutout)
        .cut(adapter_screw_cutout)
    )


vscode_main(make)
