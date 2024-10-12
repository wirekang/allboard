# %%
from cadquery import Assembly, Workplane
from allboard import vscode_main
from allboard.parts import (
    led,
    led_cutout,
    magnet1,
    vertical_key_well_cutout,
)


lens2lens = 9.2


def make(
    roof_height=1.8,
    post_width=10,
    post_groove_width=0.75,
    post_groove_height=0.75,
    post_groove_y=3,
    post_magnet_y=5.4,
    well_magnet_bottom_margin=-0.15,
    well_magnet_top_margin=-0.15,
    well_magnet_height_margin=0,
):
    key_well_cutout = vertical_key_well_cutout.make(
        post_width=post_width,
        post_groove_width=post_groove_width,
        post_groove_height=post_groove_height,
        post_groove_y=post_groove_y,
        post_magnet_y=post_magnet_y,
        well_magnet_bottom_margin=well_magnet_bottom_margin,
        well_magnet_top_margin=well_magnet_top_margin,
        well_magnet_height_margin=well_magnet_height_margin,
    ).rotateAboutCenter((1, 0, 0), 180)

    lens_hole = (
        Workplane()
        .cylinder(lens2lens, led.lens_diameter / 2)
        .rotateAboutCenter((0, 1, 0), 90)
    )

    result = (
        Assembly()
        .add(key_well_cutout, name="base")
        .add(led_cutout.make().rotateAboutCenter((0, 0, 1), 90), name="left")
        .add(led_cutout.make().rotateAboutCenter((0, 0, 1), -90), name="right")
        .add(lens_hole, name="hole")
        .add(
            Workplane().box(0.0001, 0.0001, 0.0001).faces("|Z").tag("center").end(1),
            name="center",
        )
        .constrain("base", "FixedRotation", (0, 0, 0))
        .constrain("left", "FixedRotation", (0, 0, 0))
        .constrain("right", "FixedRotation", (0, 0, 0))
        .constrain("hole", "FixedRotation", (0, 0, 0))
        .constrain("center", "Fixed")
        .constrain("left@faces@>X", "center?center", "PointInPlane", lens2lens / 2)
        .constrain("right@faces@<X", "center?center", "PointInPlane", lens2lens / 2)
        .constrain(
            "left@faces@>X", "base@faces@>Y", "PointInPlane", -led.lens_diameter - 0.3
        )
        .constrain(
            "right@faces@<X", "base@faces@>Y", "PointInPlane", -led.lens_diameter - 0.3
        )
        .constrain(
            "left@faces@>Z", "base@faces@>Z", "PointInPlane", -roof_height + 0.05
        )
        .constrain(
            "right@faces@>Z", "base@faces@>Z", "PointInPlane", -roof_height + 0.05
        )
        .constrain("hole@faces@<X", "left@faces@>X", "PointInPlane")
        .constrain("hole@faces@>X", "right@faces@<X", "PointInPlane")
        .constrain(
            "hole@faces@>Z",
            "left@faces@>Z",
            "PointInPlane",
            -led.lens_z,
        )
        .constrain(
            "hole@faces@>Z",
            "right@faces@>Z",
            "PointInPlane",
            -led.lens_z,
        )
        .constrain(
            "hole@faces@>Y",
            "base@faces@>Y",
            "PointInPlane",
            -magnet1.height - well_magnet_height_margin - 0.3,
        )
        .solve()
    )
    result.children = [c for c in result.children if c.name != "center"]
    del result.objects["center"]
    result = result.toCompound().fuse()

    return result.translate(
        (
            0,
            -result.BoundingBox().ymin,
            -result.BoundingBox().zmax + roof_height,
        )
    )


vscode_main(make)
