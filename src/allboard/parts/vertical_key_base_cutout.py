# %%
from cadquery import Assembly, Workplane
from allboard import vscode_main
from allboard.parts import (
    led,
    led_cutout,
    magnet1,
    magnet1_cutout,
    vertical_key_well_cutout,
)
from allboard.constants import (
    vertical_magnet_cutout_bottom_margin,
    vertical_magnet_cutout_top_margin,
    vertical_magnet_cutout_height_margin,
)

lens_hole_margin = 0.3

def make(
    roof_height=2.1,
    post_width=10,
    post_groove_width=0.75,
    post_groove_height=0.75,
    post_groove_y=2.5,
    post_magnet_y=6,
    lens_distance=9.2,
):
    key_well_cutout = vertical_key_well_cutout.make(
        post_width=post_width,
        post_groove_width=post_groove_width,
        post_groove_height=post_groove_height,
        post_groove_y=post_groove_y,
        post_magnet_y=post_magnet_y,
    )
    key_well_cutout = (
        Workplane("YZ")
        .add(key_well_cutout)
        .section(0)
        .faces()
        .first()
        .tag("center")
        .end(3)
    )

    led_ = led_cutout.make(lens_distance)
    led_ = Workplane("YZ").add(led_).section(0).faces().first().tag("center").end(3)

    result = (
        Assembly()
        .add(key_well_cutout, name="well")
        .add(led_, name="led")
        .add(
            magnet1_cutout.make(
                vertical_magnet_cutout_bottom_margin,
                vertical_magnet_cutout_top_margin,
                vertical_magnet_cutout_height_margin,
            ).rotateAboutCenter((1, 0, 0), 90),
            name="magnet",
        )
        .constrain("well", "FixedRotation", (0, 0, 0))
        .constrain("led", "FixedRotation", (0, 0, 0))
        .constrain("led@faces@>Z", "well@faces@>Z", "PointInPlane", -roof_height + 0.1)
        .constrain("magnet@faces@<Y", "well@faces@>Y", "PointInPlane")
        .constrain(
            "magnet@faces@>Z",
            "well@faces@>Z",
            "PointInPlane",
            -post_magnet_y - magnet1.diameter / 2 - vertical_key_well_cutout.margin_z,
        )
        .constrain(
            "led?center",
            "well@faces@>Y",
            "PointInPlane",
            -led.lens_diameter / 2 - lens_hole_margin,
        )
        .constrain("well?center", "led?center", "PointInPlane")
        .constrain("magnet@faces@<Y", "well?center", "PointInPlane")
        .solve()
        .toCompound()
        .fuse()
    )

    return result.translate(
        (
            0,
            -result.BoundingBox().ymin,
            -result.BoundingBox().zmax + roof_height,
        )
    )


vscode_main(make)
