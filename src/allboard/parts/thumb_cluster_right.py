# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import bolt1_cutout, vertical_key_base_cutout

STL = 1
DXF = 1


roof_length = 8.6
roof_width = 4.8
roof_height = 5.8
roof_fillet = 0.8

post_width = 16
post_groove_width = 0.75
post_groove_height = 0.75
post_groove_y = 3.1
post_magnet_y = 9.4

inner_x = -16.5
inner_y = 6.25
inner_angle = 20

mod_x = inner_x - 5.7
mod_y = inner_y
mod_angle = inner_angle

upper_x = 20
upper_y = 10

lower_x = upper_x
lower_y = -16

key_angle = 10
key_lower_angle = 7

length = 46
width = 54
height = 6.2

led_distance = 12
led_distance_down = 20.5

led_margin_y_inner = 0.6
led_margin_y_outer = 0.3

pcb_screw_cutout1_x = 9.5
pcb_screw_cutout1_y = 18.5
pcb_screw_cutout1_angle = -10

pcb_screw_cutout2_x = -13
pcb_screw_cutout2_y = -7
pcb_screw_cutout2_angle = -66

fillet = 1.5


def make():
    base = (
        (
            Workplane()
            .moveTo(13.5, -51.5)
            .lineTo(43.5, -51.5)
            .lineTo(43.5, -7.5)
            .lineTo(25, -4.5)
            .lineTo(6.5, -5)
            .lineTo(2, -20)
            .close()
        )
        .extrude(height)
        .translate((-length / 2, width / 2, -height))
        .edges("|Z")
        .fillet(fillet)
    )

    roof = Workplane()
    inner_cutout = (
        vertical_key_base_cutout.make(
            roof_height=roof_height,
            post_width=post_width,
            post_groove_width=post_groove_width,
            post_groove_height=post_groove_height,
            post_groove_y=post_groove_y,
            post_magnet_y=post_magnet_y,
            led_distance=led_distance,
            angle=key_angle,
            led_margin_y=led_margin_y_inner,
        )
        .rotate((0, 0, 0), (0, 0, 1), -90)
        .translate((inner_x, inner_y, 0))
        .rotate((0, 0, 0), (0, 0, 1), -inner_angle)
    )
    roof.add(
        Workplane()
        .box(roof_length, roof_width + inner_x - mod_x, roof_height)
        .translate((0, 0, roof_height / 2))
        .rotate((0, 0, 0), (0, 0, 1), -90)
        .translate((inner_x - 0.5, inner_y, 0))
        .rotate((0, 0, 0), (0, 0, 1), -inner_angle)
        .edges("|Z")
        .fillet(roof_fillet)
    )

    mod_cutout = (
        vertical_key_base_cutout.make(
            roof_height=roof_height,
            post_width=post_width,
            post_groove_width=post_groove_width,
            post_groove_height=post_groove_height,
            post_groove_y=post_groove_y,
            post_magnet_y=post_magnet_y,
            led_distance=led_distance,
            angle=key_angle,
            led_margin_y=led_margin_y_inner,
        )
        .rotate((0, 0, 0), (0, 0, 1), -90)
        .translate((mod_x, mod_y, 0))
        .rotate((0, 0, 0), (0, 0, 1), -mod_angle)
    )

    upper_cutout = (
        vertical_key_base_cutout.make(
            roof_height=roof_height,
            post_width=post_width,
            post_groove_width=post_groove_width,
            post_groove_height=post_groove_height,
            post_groove_y=post_groove_y,
            post_magnet_y=post_magnet_y,
            led_distance=led_distance,
            angle=key_angle,
            led_margin_y=led_margin_y_outer,
        )
        .rotate((0, 0, 0), (0, 0, 1), 90)
        .translate((upper_x, upper_y, 0))
    )
    roof.add(
        Workplane()
        .box(roof_length, roof_width, roof_height)
        .translate((0, 0, roof_height / 2))
        .rotate((0, 0, 0), (0, 0, 1), 90)
        .translate((upper_x - roof_width / 2, upper_y, 0))
        .edges("|Z")
        .fillet(roof_fillet)
    )

    lower_cutout = (
        vertical_key_base_cutout.make(
            roof_height=roof_height,
            post_width=post_width,
            post_groove_width=post_groove_width,
            post_groove_height=post_groove_height,
            post_groove_y=post_groove_y,
            post_magnet_y=post_magnet_y,
            led_distance=led_distance,
            angle=key_lower_angle,
            led_margin_y=led_margin_y_outer,
        )
        .rotate((0, 0, 0), (0, 0, 1), 90)
        .translate((lower_x, lower_y, 0))
    )
    roof.add(
        Workplane()
        .box(roof_length, roof_width, roof_height)
        .translate((0, 0, roof_height / 2))
        .rotate((0, 0, 0), (0, 0, 1), 90)
        .translate((lower_x - roof_width / 2, lower_y, 0))
        .edges("|Z")
        .fillet(roof_fillet)
    )

    pcb_screw_cutout1 = (
        bolt1_cutout.make()
        .translate((pcb_screw_cutout1_x, pcb_screw_cutout1_y, 0))
        .rotateAboutCenter((0, 0, 1), pcb_screw_cutout1_angle)
    )

    pcb_screw_cutout2 = (
        bolt1_cutout.make()
        .translate((pcb_screw_cutout2_x, pcb_screw_cutout2_y, 0))
        .rotateAboutCenter((0, 0, 1), pcb_screw_cutout2_angle)
    )

    return (
        base.union(roof)
        .cut(inner_cutout)
        .cut(mod_cutout)
        .cut(upper_cutout)
        .cut(lower_cutout)
        .cut(pcb_screw_cutout1)
        .cut(pcb_screw_cutout2)
    )


vscode_main(make)
