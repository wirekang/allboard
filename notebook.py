# %%
import os
from typing import Any
import cadquery as cq
from ocp_vscode import (
    show,
    set_port,
    set_defaults,
    Camera,
)


set_port(3939)
set_defaults(
    reset_camera=Camera.KEEP,
    axes=True,
    axes0=True,
)


def parse_axis(axis: str) -> tuple[int, int, int]:
    axis = axis.ljust(3, "0")
    result: Any = ()
    for v in axis:
        if v == "0":
            result = (*result, 0)
        if v == "-":
            result = (*result, -1)
        if v == "+":
            result = (*result, 1)
    return result


class Wrk(cq.Workplane):
    def abox(
        self, axis: str, length, width, height, **kwargs
    ):
        x, y, z = parse_axis(axis)

        return self.box(
            length, width, height, **kwargs
        ).translate(
            (length / 2 * x, width / 2 * y, height / 2 * z)
        )

    def acylinder(self, axis, height, diameter1, diameter2):
        x, y, z = parse_axis(axis)
        ll = max(diameter1, diameter2)
        return (
            Wrk()
            .circle(diameter1 / 2)
            .workplane(offset=height)
            .circle(diameter2 / 2)
            .loft()
            .translate(
                (
                    ll / 2 * x,
                    ll / 2 * y,
                    -height / 2 + height / 2 * z,
                )
            )
        )

    def tx(self, x):
        return self.translate((x, 0, 0))

    def ty(self, y):
        return self.translate((0, y, 0))

    def tz(self, z):
        return self.translate((0, 0, z))

    def rox(self, d):
        return self.rotate((0, 0, 0), (1, 0, 0), d)

    def roy(self, d):
        return self.rotate((0, 0, 0), (0, 1, 0), d)

    def roz(self, d):
        return self.rotate((0, 0, 0), (0, 0, 1), d)

    def rx(self, d):
        return self.rotateAboutCenter((1, 0, 0), d)

    def ry(self, d):
        return self.rotateAboutCenter((0, 1, 0), d)

    def rz(self, d):
        return self.rotateAboutCenter((0, 0, 1), d)

    def export(self, fname):
        p = os.path.join(__file__, "..", "out", fname)
        print("Export", fname, p)
        cq.exporters.export(self, p)
        return self

    def apbox(
        self, length, width, height, x=0.0, y=0.0, z=0.0
    ):
        return self.add(
            Wrk()
            .abox("+++", length, width, height)
            .translate((x, y, z))
        )


class Skt(cq.Sketch):
    def tx(self, x):
        return self.moved(cq.Location((x, 0, 0)))

    def ty(self, y):
        return self.moved(cq.Location((0, y, 0)))

    def tz(self, z):
        return self.moved(cq.Location((0, 0, z)))

    def arect(self, axis: str, w, h, **kwargs):
        x, y, z = parse_axis(axis)

        return self.rect(w, h, **kwargs).moved(
            cq.Location((w / 2 * x, h / 2 * y))
        )


A1 = 15
A2 = 10
A3 = 7
A4 = 5.6
A5 = 2.4
A6 = 1.2
A7 = 3
A10 = 13
A8 = A10 / 2 - A5 / 2
A11 = 1.6
A12 = 4
A13 = A11 + 0.1
A14 = 0.4
A16 = 7
A15 = (A10 - A16) / 2
A9 = A15 + A16 - A6


B7 = 0.2
B11 = 0.4
B3 = 2.6
B4 = A3 + B7
B5 = 0
B6 = A16 + B11 * 2 + 1.2
B1 = B6 / 2 - B3 / 2
B2 = B6 - (A9 - A15)
B8 = 1.6
B10 = 5
B9 = B10 - A13 - 0.8
B12 = B11
B13 = B10 + B8 + 0.1
B14 = A2 + 0.2


def make_magnet_cutout(height, diameter):
    glue_length = 1.2
    glue_width = 1.2
    glue_height = 0.4
    bottom_margin = -0.2
    return (
        Wrk()
        .acylinder(
            "+++",
            height,
            diameter + bottom_margin,
            diameter,
        )
        .add(
            Wrk()
            .abox(
                "0--", glue_length, glue_width, glue_height
            )
            .tx((diameter) / 2)
            .ty(-bottom_margin)
            .tz(height)
        )
    )


def make_a(*, front=2.0):
    result = (
        Wrk()
        .apbox(
            A10,
            A1 - A2,
            A14,
            0,
            A2,
            A13 + front,
        )
        .apbox(A16, A2, A13, A15)
        .apbox(A6, A7, A12, A9, A4, A13)
        .cut(
            make_magnet_cutout(
                A11,
                A5,
            )
            .tx(A8)
            .ty(A3)
            .tz(-A11 + A13)
        )
        .add(
            Wrk("YZ", (0, A2, 0))
            .vLine(A13 + front)
            .hLine(A1 - A2)
            .close()
            .extrude(A16)
            .tx(A15)
        )
        .cut(
            Wrk()
            .apbox(A16, 3, A13 / 2, A15, 0, A13 / 2)
            .ty(2)
        )
    )
    return result


def make_b():
    return (
        Wrk()
        .apbox(B11, B13, B14)
        .apbox(B11, B13, B14, B6 - B11)
        .apbox(B6, B12, B14)
        .apbox(B6, B13 - B10, B14, 0, B10)
        .apbox(B6, B13, B7)
        .add(
            Wrk()
            .rect(B6, B9, False)
            .tz(B7)
            .workplane(B14 - B7)
            .rect(B6, B12, False)
            .loft()
        )
        .cut(
            make_magnet_cutout(B8, B3)
            .rox(90)
            .tx(B1)
            .ty(B10)
            .ty(B8)
            .tz(B4)
        )
        .cut(
            Wrk()
            .abox("+++", B2 - B11, B13 - B10, B14 - B5)
            .ty(B10)
            .tz(B5)
        )
    )


def make_magnet_helper():
    margin = 9
    width = 15
    count = 5
    cutout = Wrk()
    for i in range(count):
        cutout.add(
            make_magnet_cutout(A11 + 0.1, A5)
            .tx(margin * (i + 1))
            .ty(width / 2)
            .tz(0.1)
        )
    return (
        Wrk()
        .abox("+++", margin * (count + 1), width, A11 + 0.2)
        .cut(cutout)
    )


show(make_a().export("a.stl"))
show(make_b().export("b.stl"))
show(make_magnet_helper().export("magnet_helper.stl"))
