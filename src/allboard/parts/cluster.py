# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import vertical_key_base

STL = 1


length = 24.9
height = 6.5

roof_length = 8.6
roof_width = 4.8
roof_height = 1.9

post_width = 10
post_groove_width = 0.75
post_groove_height = 0.75
post_groove_y = 2
post_magnet_y = 5.4

well_magnet_bottom_margin = -0.15
well_magnet_top_margin = 0.15
well_magnet_height_margin = 0

header_width = 12
connector_cutout_length = 12
connector_cutout_width = 2.7
connector_cutout_height = 2.5
connector_cutout_y = 16
screw_y = 21.5


def _make_vertical_key_bases():
    result = Workplane()
    for angle in [0, 90, 180, 270]:
        result = result.union(
            vertical_key_base.make(
                length=length,
                width=6,
                height=height,
                roof_length=roof_length,
                roof_width=roof_width,
                roof_height=roof_height,
                post_width=post_width,
                post_groove_width=post_groove_width,
                post_groove_height=post_groove_height,
                post_groove_y=post_groove_y,
                post_magnet_y=post_magnet_y,
                well_magnet_bottom_margin=well_magnet_bottom_margin,
                well_magnet_top_margin=well_magnet_top_margin,
                well_magnet_height_margin=well_magnet_height_margin,
            )
            .translate((0, -length / 2, 0))
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
    return result


def make():
    vertical_key_bases = _make_vertical_key_bases()

    header = (
        Workplane()
        .box(length, header_width, height)
        .translate(
            (
                0,
                length / 2 + header_width / 2,
                -height / 2,
            )
        )
    )

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
    screw_cutout = (
        Workplane()
        .cylinder(1.8, 1.5)
        .translate((0, 0, -1.8 / 2))
        .union(Workplane().cylinder(4.5, 1.5).translate((0, 0, -1.8 - 4.5 / 2 - 0.05)))
        .union(
            Workplane()
            .box(
                6.5,
                6.5,
                2.5,
            )
            .translate((0, 0, -1.8 - 2.5 / 2 - 0.05))
        )
        .translate((0, screw_y, 0))
    )

    return vertical_key_bases.union(header).cut(connector_cutout).cut(screw_cutout)


vscode_main(make)
