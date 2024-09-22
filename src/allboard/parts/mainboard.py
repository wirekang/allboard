# %%
import cadquery

from allboard import entrypoint
from allboard.cq_utils import tbox
from allboard.parts import mainboard_screw

STL = 1
DXF = 1

length = 42
width = 67
height = 1.6

screw_hole_margin = 2

usb_port_length = 9.5
usb_port_width = 8
usb_port_height = 4
usb_port1_x = 9.5
usb_port1_y = width - usb_port_width
usb_port2_x = 27.5
usb_port2_y = usb_port1_y

connectors_x = 28
connectors_y = 23
connectors_length = length - connectors_x
connectors_width = 26
connectors_height = 6


mcu_length = 9
mcu_width = 9
mcu_x = 7
mcu_y = 25.5

button_length = 3
button_width = 3
button_height = 1.5

boot_x = 2.5
boot_y = 53

reset_x = 27
reset_y = 5


def mainboard():
    extensions = [
        (
            usb_port_length,
            usb_port_width,
            usb_port_height,
            usb_port1_x,
            usb_port1_y,
        ),
        (
            usb_port_length,
            usb_port_width,
            usb_port_height,
            usb_port2_x,
            usb_port2_y,
        ),
        (
            connectors_length,
            connectors_width,
            connectors_height,
            connectors_x,
            connectors_y,
        ),
        (
            button_length,
            button_width,
            button_height,
            boot_x,
            boot_y,
        ),
        (
            button_width,
            button_length,
            button_height,
            reset_x,
            reset_y,
        ),
    ]

    hole_rect_offset = screw_hole_margin + mainboard_screw.diameter / 2

    hole_rect_length = length - hole_rect_offset * 2
    hole_rect_width = width - hole_rect_offset * 2

    base = (
        cadquery.Workplane()
        .box(length, width, height, centered=False)
        .faces("+Z")
        .workplane()
        .transformed(offset=(hole_rect_offset, hole_rect_offset, 0))
        .rect(
            hole_rect_length,
            hole_rect_width,
            forConstruction=True,
            centered=False,
        )
        .vertices("<X and >Y or >X and <Y")
        .hole(mainboard_screw.diameter)
    )

    result = base
    for l, w, h, x, y in extensions:
        result = result.union(tbox(l, w, h + height, (x, y), False))

    return result


entrypoint(mainboard())
