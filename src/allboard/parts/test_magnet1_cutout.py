# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import magnet1, magnet1_cutout
from allboard.utils import encoding2, run_multithread

STL = 1


def make():

    result = Workplane()
    base_size = magnet1.diameter + 10
    base_height = magnet1.height + 0.4

    def _make(x, y, angle, bottom_margin, top_margin, height_margin):
        font_size = 6
        font_margin = 0.4
        base = (
            Workplane()
            .box(
                base_size,
                base_size,
                base_height,
                centered=False,
            )
            .cut(
                magnet1_cutout.make(
                    bottom_margin, top_margin, height_margin
                ).translate((base_size / 2, base_size / 2, base_height))
            )
            .cut(
                Workplane()
                .text(
                    encoding2(bottom_margin),
                    font_size,
                    1,
                    valign="bottom",
                    halign="right",
                )
                .translate(
                    (base_size - font_margin, font_margin, base_height - 0.4)
                )
            )
            .cut(
                Workplane()
                .text(
                    encoding2(top_margin),
                    font_size,
                    1,
                    valign="top",
                    halign="left",
                )
                .translate(
                    (
                        font_margin,
                        base_size + font_margin * 2,
                        base_height - 0.4,
                    )
                )
            )
            .cut(
                Workplane()
                .text(
                    encoding2(height_margin),
                    font_size,
                    1,
                    valign="top",
                    halign="right",
                )
                .translate(
                    (
                        base_size - font_margin,
                        base_size + font_margin * 2,
                        base_height - 0.4,
                    )
                )
            )
        )
        if angle != 0:
            base = base.cut(
                Workplane()
                .text(
                    ".",
                    font_size,
                    1,
                    valign="bottom",
                    halign="left",
                )
                .translate((font_margin, font_margin, base_height - 0.4))
            ).rotateAboutCenter((1, 0, 0), angle)

        base = base.translate(
            (x, y, 0 if angle == 0 else (base_size - base_height) / 2)
        )

        result.add(base)

    args_list = []

    x = 0
    y = 0
    for angle in [0, 90]:
        for bottom_margin in [-0.2, -0.1, 0, 0.1, 0.2]:
            for top_margin in [-0.2, -0.1, 0, 0.1, 0.2]:
                for height_margin in [0]:
                    args_list.append(
                        [
                            x,
                            y,
                            angle,
                            bottom_margin,
                            top_margin,
                            height_margin,
                        ]
                    )
                    x += base_size + 1
            x = 0
            y += base_size + (1 if angle == 0 else 1)

    run_multithread(args_list, _make)

    return result


vscode_main(make)
