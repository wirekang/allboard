# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.cq_utils import tbox
from allboard.parts import vertical_key_post

height = 1.7
extra_height = 1
fillet = 0.6
post_length = 7.3


def make(
    length=13,
    width=5,
    angle=0,
    post_width=10,
    post_groove_width=0.75,
    post_groove_height=0.75,
    post_groove_y=2,
    post_magnet_y=5.4,
):
    base = (
        Workplane()
        .box(length, width, height + extra_height)
        .translate((0, 0, extra_height / 2))
    )

    base_cutout = (
        Workplane()
        .cylinder(width * 2, width * 2)
        .rotateAboutCenter((1, 0, 0), 90)
        .translate((0, width - width / 2, width * 2 + height / 2))
    )

    base = base.cut(base_cutout).edges("(not <Z) and (not <Y)").fillet(fillet)
    if angle > 0:
        base = (
            base.rotate(
                (0, -width / 2, height / 2), (1, -width / 2, height / 2), angle
            )
            .faces("<Z")
            .edges(">Y")
            .ancestors("Face")
            .faces(">Y")
            .wires()
            .toPending()
            .extrude(-50)
            .cut(tbox(100, 100, 100, (0, 0, -50 - height / 2)))
        )

    post = vertical_key_post.make(
        post_length,
        post_width,
        height,
        post_magnet_y,
        post_groove_width,
        post_groove_height,
        post_groove_y,
    )

    bridge = Workplane().box(post_length, post_width / 5, height)
    return (
        base.translate((0, width / 2, 0))
        .union(post.translate((0, -post_width / 2, 0)))
        .union(bridge)
    )


vscode_main(make)
