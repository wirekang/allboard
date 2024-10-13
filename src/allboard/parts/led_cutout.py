# %%
from cadquery import Assembly, Workplane
from allboard import vscode_main
from allboard.parts import led

margin_length = 0.3
margin_width = 0.3
margin_height = 0.1
lens_margin_length = 0
lens_margin_width = 0

def make(lens_distance=10):
    base_length = led.base_length + margin_length
    base_width = led.base_width + margin_width
    base_height = led.base_height + margin_height

    lens_cut_length = led.lens_diameter / 2 + lens_margin_length
    lens_cut_width = led.lens_diameter + lens_margin_width
    lens_cut_height = led.lens_z + led.lens_diameter / 2

    base = Workplane().box(base_length, base_width, base_height)
    lens_cut = Workplane().box(lens_cut_length, lens_cut_width, lens_cut_height)
    lens_hole = (
        Workplane()
        .cylinder(lens_distance / 2, led.lens_diameter / 2)
        .rotateAboutCenter((0, 1, 0), 90)
    )

    asm = (
        (
            Assembly()
            .add(base, name="base")
            .add(lens_cut, name="lens_cut")
            .add(lens_hole, name="hole")
            .constrain("base", "FixedRotation", (0, 0, 0))
            .constrain("lens_cut", "FixedRotation", (0, 0, 0))
            .constrain("hole", "FixedRotation", (0, 0, 0))
            .constrain("base@faces@>Z", "lens_cut@faces@>Z", "PointInPlane")
            .constrain("base@faces@>X", "lens_cut@faces@<X", "PointInPlane")
            .constrain("hole@faces@<X", "lens_cut@faces@>X", "PointInPlane")
            .constrain(
                "hole@faces@<Z",
                "lens_cut@faces@<Z",
                "PointInPlane",
                -led.lens_diameter / 2,
            )
            .solve()
        )
        .toCompound()
        .fuse()
    )

    return (
        Workplane(asm)
        .translate((-asm.BoundingBox().xmax, 0, -asm.BoundingBox().zmax))
        .mirror("YZ", union=True)
        .combine()
    )


vscode_main(make)
