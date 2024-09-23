# %%

from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import magnet1, magnet1_cutout

STL = 1


diameter = 15
height = 2
rim_thickness = 1
rim_height = 0.5

post_length = 3.5
post_width = 3.5
post_height = 8
post_margin = 0.6
post_base_height = 2.5
fillet = 0.4

magnet_margin_height = 0.2
magnet_margin_bottom = 0.1
magnet_margin_top = 0.3


def make():
    base = (
        Workplane()
        .cylinder(height, diameter / 2, centered=False)
        .cut(
            Workplane(
                origin=(rim_thickness, rim_thickness, height - rim_height)
            ).cylinder(99, diameter / 2 - rim_thickness, centered=False)
        )
    ).translate((-diameter / 2, -diameter / 2))

    def post(xm=1):
        return (
            Workplane()
            .box(post_length, post_width, post_height)
            .edges("not <Z")
            .fillet(fillet)
            .cut(
                magnet1_cutout.make(
                    magnet_margin_bottom,
                    magnet_margin_top,
                    magnet_margin_height,
                ).translate((0, 0, post_height / 2))
            )
            .translate(
                (
                    (
                        (diameter / 2)
                        - rim_thickness
                        - post_margin
                        - post_width / 2
                    )
                    * xm,
                    0,
                    post_height / 2 + height,
                )
            )
        )

    post_base = (
        Workplane()
        .box(
            diameter - post_margin * 2 - rim_thickness * 2 - fillet * 3,
            post_width,
            post_base_height,
        )
        .translate((0, 0, height + post_base_height / 2))
    )

    return base.union(post(-1)).union(post()).union(post_base)


vscode_main(make())
