# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import led

margin_length = 0.3
margin_width = 0.3
margin_height = 0.1
lens_margin_length = 0
lens_margin_width = -0.1

base_length = led.base_length + margin_length
base_width = led.base_width + margin_width
base_height = led.base_height + margin_height


def make():
    lens_cut_length = led.lens_diameter + lens_margin_length
    lens_cut_width = led.lens_diameter / 2 + lens_margin_width
    lens_cut_height = base_height

    return (
        Workplane()
        .box(
            base_length,
            base_width,
            base_height,
        )
        .union(
            Workplane()
            .box(
                lens_cut_length,
                lens_cut_width,
                lens_cut_height,
            )
            .translate(
                (
                    0,
                    -led.base_width / 2
                    - (led.lens_diameter / 2 + lens_margin_width) / 2,
                    lens_cut_height - led.lens_z - led.lens_diameter / 2,
                )
            )
        )
        .translate((0, 0, base_height / 2))
    ).cut(Workplane().box(10, 10, 10).translate((0, 0, base_height + 5)))


vscode_main(make)
