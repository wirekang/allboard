# %%
from cadquery import Edge, Workplane
from allboard import vscode_main
from allboard.cq_utils import union_padding
from allboard.parts import magnet1, magnet1_cutout, vertical_key, vertical_key_post

angle = 13
margin_x = 1
margin_y = 0
margin_z = 0.1


def make(
    post_width=10,
    post_groove_width=0.75,
    post_groove_height=0.75,
    post_groove_y=2,
    post_magnet_y=5.4,
    well_magnet_bottom_margin=-0.15,
    well_magnet_top_margin=-0.15,
    well_magnet_height_margin=0,
):
    result = (
        vertical_key_post.make(
            length=vertical_key.post_length,
            width=post_width,
            height=vertical_key.height,
            magnet_y=post_magnet_y,
            groove_width=post_groove_width,
            groove_height=post_groove_height,
            groove_y=post_groove_y,
        )
        .union(
            magnet1_cutout.make().translate(
                (0, (post_magnet_y - post_width / 2), vertical_key.height / 2)
            )
        )
        .rotateAboutCenter((1, 0, 0), 90)
    ).combine()
    result = union_padding(result, x=margin_x, y=margin_y, z=margin_z)
    post_bb = result.combine().objects[0].BoundingBox()
    post_0 = result.translate((0, 0, -post_bb.zmin))
    result = post_0
    for hat_width in range(angle + 1):
        result = result.union(
            post_0.rotate((1, 0, 0), (0, 0, 0), hat_width).translate((0, 0, 0.2))
        )

    result = result.union(
        magnet1_cutout.make(
            well_magnet_bottom_margin,
            well_magnet_top_margin,
            well_magnet_height_margin,
        )
        .rotateAboutCenter((1, 0, 0), -90)
        .translate(
            (
                0,
                -magnet1.height / 2,
                post_magnet_y + magnet1.diameter / 2,
            )
        )
    )

    e1: Edge = result.edges("|X").edges("<Y").edges(">Z").val()
    e2: Edge = result.edges("|X").edges(">Y").edges(">Z").val()

    hat_length = e1.startPoint().x - e1.endPoint().x
    hat_width = e2.startPoint().y - e1.startPoint().y
    hat_height = e1.startPoint().z - e2.startPoint().z + 0.05

    return result.union(
        Workplane()
        .box(hat_length, hat_width, hat_height)
        .translate(
            (
                0,
                hat_width / 2 + e1.startPoint().y,
                e1.startPoint().z - hat_height / 2 + 0.05,
            )
        )
    )


vscode_main(make)
