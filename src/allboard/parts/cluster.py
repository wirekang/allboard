# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import (
    bolt1,
    cluster_key_down_base_cutout,
    vertical_key_base_cutout,
)
from allboard.utils import run_multithread
from allboard.constants import sacrificial_layer_height

STL = 1


length = 25
width = 48.5
height = 6.5
head_fillet = 12
tail_fillet = 12

roof_length = 8.6
roof_width = 4.8
roof_height = 2.1

post_width = 10
post_groove_width = 0.75
post_groove_height = 0.75
post_groove_y = 2.5
post_magnet_y = 6


connector_cutout_length = 12
connector_cutout_width = 2.7
connector_cutout_height = 2.5
connector_cutout_y = 16

pcb_screw_cutout_y = 21
pcb_nut_cutout_length = 6.5
pcb_nut_cutout_width = 6.5
pcb_nut_cutout_height = 2.7

lens_distance = 9.2

south_margin = 0.5
north_margin = 0.5

adapter_screw_cutout_y = -20
adapter_screw_cutout_z = -2


# todo: refactor
def make():
    vertical_base_roofs = []
    vertical_base_cutouts = []

    def f_vertical_base_cutout(angle, margin=0):
        vertical_base_cutouts.append(
            vertical_key_base_cutout.make(
                roof_height,
                post_width,
                post_groove_width,
                post_groove_height,
                post_groove_y,
                post_magnet_y,
                lens_distance,
            )
            .translate((0, -length / 2 - margin, 0))
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
        vertical_base_roofs.append(
            Workplane()
            .box(roof_length, roof_width, roof_height + 0.2)
            .translate(
                (
                    0,
                    -length / 2 + roof_width / 2,
                    roof_height / 2 + 0.1,
                )
            )
            .rotate((0, 0, 0), (0, 0, 1), angle)
            .val()
        )

    run_multithread(
        [[0, south_margin], [90], [180, north_margin], [270]], f_vertical_base_cutout
    )

    vertical_base_cutout = Workplane().add(vertical_base_cutouts)
    vertical_base_roof = Workplane().add(vertical_base_roofs)

    down_base_cutout = cluster_key_down_base_cutout.make(height, lens_distance)

    connector_cutout = (
        Workplane()
        .box(
            connector_cutout_length,
            connector_cutout_width,
            connector_cutout_height,
        )
        .translate((0, connector_cutout_y, -connector_cutout_height / 2))
    )

    # todo: parameterize
    pcb_screw_cutout = (
        Workplane()
        .cylinder(1.8, bolt1.diameter / 2)
        .translate((0, 0, -bolt1.diameter / 2 / 2))
        .union(
            Workplane()
            .cylinder(4.5, bolt1.diameter / 2)
            .translate((0, 0, -1.8 - 4.5 / 2 - sacrificial_layer_height / 2))
        )
        .union(
            Workplane()
            .box(
                pcb_nut_cutout_length,
                pcb_nut_cutout_width,
                pcb_nut_cutout_height,
            )
            .translate(
                (
                    0,
                    0,
                    -1.8 - pcb_nut_cutout_height / 2 - sacrificial_layer_height / 2,
                )
            )
        )
        .translate((0, pcb_screw_cutout_y, 0))
    )

    adapter_screw_cutout = (
        Workplane()
        .cylinder(-adapter_screw_cutout_z, bolt1.diameter / 2)
        .translate((0, adapter_screw_cutout_y, adapter_screw_cutout_z / 2))
        .union(
            Workplane()
            .cylinder(height + adapter_screw_cutout_z, bolt1.diameter)
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
