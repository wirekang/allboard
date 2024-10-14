# %%
from cadquery import Assembly, Workplane
from allboard import vscode_main
from allboard.parts import thumb_cluster_right, vertical_key, vertical_key_post


STL = 1


width0 = 5
width1 = 7
width2 = 10
angle1 = 40
angle2 = 120


def make():
    length = vertical_key.post_length
    height = vertical_key.height
    post = vertical_key_post.make(
        length=length,
        width=thumb_cluster_right.post_width + width0,
        height=height,
        groove_width=thumb_cluster_right.post_groove_width,
        groove_height=thumb_cluster_right.post_groove_height,
        groove_y=thumb_cluster_right.post_groove_y,
        magnet_y=thumb_cluster_right.post_magnet_y,
    )

    p1 = Workplane().box(
        length,
        width1,
        height,
    )

    p2 = Workplane().box(
        length,
        width2,
        height,
    )

    asm = (
        Assembly()
        .add(post, name="post")
        .add(p1, name="p1")
        .add(p2, name="p2")
        .constrain("post", "Fixed")
        .constrain(
            "p1",
            "FixedRotation",
            (angle1, 0, 0),
        )
        .constrain(
            "p2",
            "FixedRotation",
            (angle2, 0, 0),
        )
        .constrain("post@faces@>Y", "p1@faces@<Y", "Plane")
        .constrain("p2@faces@<Y", "p1@faces@>Y", "Plane")
        .solve()
    )

    return Workplane().add(asm.toCompound().fuse(tol=0.3)).edges(">Y or >Z").fillet(0.5)


vscode_main(make)
