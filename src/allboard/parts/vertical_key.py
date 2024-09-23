# %%
from threading import Lock, Thread
from cadquery import Workplane
from allboard import vscode_main
from allboard.cq_utils import tbox
from allboard.parts import vertical_key_post

height = 1.7
extra_height = 1
fillet = 0.6
post_length = 7.3


def make(
    length,
    width,
    angle,
    post_width,
    post_groove_width,
    post_groove_height,
    post_groove_y,
    post_magnet_y,
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


vscode_main(
    make(
        length=13,
        width=5,
        angle=0,
        post_width=10,
        post_groove_width=0.75,
        post_groove_height=0.75,
        post_groove_y=2,
        post_magnet_y=5.4,
    )
)


# _mutex = Lock()
# _results = []
# _names = []
# _threads = []


# def _job(*args):
#     result = make(
#         length,
#         width,
#         angle,
#         post_width,
#         post_groove_width=0.5,
#         post_groove_height=0.5,
#         post_groove_y=2,
#         post_magnet_y=5,
#     )
#     _mutex.acquire(True)
#     i = len(_results)
#     _results.append(
#         result.translate(
#             (
#                 (i % 10) * 40,
#                 int(i / 10) * 70,
#                 0,
#             )
#         )
#     )
#     _names.append(str(args))
#     _mutex.release()


# for length in [13, 30]:
#     for width in [5, 11, 30]:
#         for angle in [0, 10]:
#             for post_width in [10, 20]:
#                 for post_groove_width in [0.5]:
#                     for post_groove_height in [0.5]:
#                         for post_groove_y in [2]:
#                             for post_magnet_y in [5, 10]:
#                                 t = Thread(
#                                     target=_job,
#                                     args=[
#                                         length,
#                                         width,
#                                         angle,
#                                         post_width,
#                                         post_groove_width,
#                                         post_groove_height,
#                                         post_groove_y,
#                                         post_magnet_y,
#                                     ],
#                                 )
#                                 t.start()
#                                 _threads.append(t)

# for t in _threads:
#     t.join()

# vscode_main(*_results, names=_names)
