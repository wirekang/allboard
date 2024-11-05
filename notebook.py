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
        print("\nExport", fname, p)
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

    def apcylinder(
        self,
        height,
        diameter1,
        diameter2,
        x=0.0,
        y=0.0,
        z=0.0,
    ):
        return self.add(
            Wrk()
            .acylinder("+++", height, diameter1, diameter2)
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


A1 = 14.5
A2 = 10
A3 = 7
A4 = 4
A5 = 2.6
A6 = 1
A7 = 2.2
A10 = 9
A8 = A10 / 2 - A5 / 2
A11 = 1.5
A12 = 3.5
A13 = A11 + 0.1
A14 = 0.4
A16 = 5
A15 = (A10 - A16) / 2
A9 = A15 + A16 - A6


B7 = 0.2
B11 = 0.2
B3 = 2.64
B4 = A3 + B7
B5 = 0
B6 = A16 + B11 * 2 + 0.8
B1 = B6 / 2 - B3 / 2
B2 = B6 - (A9 - A15) - B11 - 0.2
B8 = 1.9
B10 = 4
B9 = B10 - A13 - 0.4
B12 = B11
B13 = B10 + B8 + 0.2
B14 = A2 + 0.2

C1 = 9
C2 = 3
C5 = 2.64
C6 = 1.5
C3 = C6 + 0.2
C8 = 7
C14 = 4.5
C13 = 1.2
C11 = 3
C12 = A6
C7 = A7
C4 = C8 / 2 - C5 / 2
C9 = C14 / 2 - C5 / 2

D5 = 10.2
D3 = 0.3
D4 = C13 + D3 * 2 + 0.4
D8 = C14 + D3 * 2 + 0.4
D6 = 1
D7 = 2.6
D1 = (D5 - D8) / 2
D2 = (D5 - C8) / 2 - D3


E3 = 0.2
E13 = 0.2
E9 = D4 + 1
E4 = 2.5
E5 = 1.9
E14 = C12 + 1
E7 = C2 - C3 + C7 + 1
E1 = C1 - C3 - D7
E8 = E3 * 2 + E9 * 2 + E4 + 0.12
E6 = E8 / 2 - E4 / 2
E15 = D8 + 1
E10 = E13 * 2 + E15
E11 = E10 / 2 - E4 / 2


def make_magnet_cutout(height, diameter):
    glue_length = 1.5
    glue_width = 1.2
    glue_height = height
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
            .ty(-bottom_margin * 3)
            .tz(height)
        )
    )


def make_a(*, front=0.0, tall=0.0):
    return (
        Wrk()
        .apbox(
            A10,
            A1 - A2 + tall,
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
            Wrk("XZ")
            .workplane(A2, invert=True)
            .rect(A16, A13 + front, False)
            .translate((A15, 0, A13 + front))
            .add(
                Wrk()
                .workplane(A13 + front)
                .rect(A10, A1 - A2 + tall, False)
                .translate((0, A2))
            )
            .wires()
            .toPending()
            .loft(ruled=True)
        )
    )


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
    margin = 25
    width = 25
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


def make_temp_cluster():
    def c(distance):
        wall = 0.3
        return (
            make_b()
            .add(Wrk().abox("-++", wall, B13, B14))
            .add(Wrk().abox("+++", wall, B13, B14).tx(B6))
            .tx(-(B6) / 2)
            .ty(-B13 - distance)
            .add(
                Wrk()
                .abox("+--", wall, distance, 4)
                .tx(B6 / 2)
                .tz(B14)
            )
            .add(
                Wrk()
                .abox("---", wall * 2, distance, 4)
                .tz(B14)
            )
            .add(
                Wrk()
                .abox("---", wall, distance, 4)
                .tx(-B6 / 2)
                .tz(B14)
            )
        )

    return (
        Wrk()
        .add(make_e().tx(-E8 / 2).ty(-E10 / 2).tz(B14 - E1))
        .add(c(3).ty(-E10 / 2))
        .add(c(2.5).roz(90).tx(E8 / 2))
        .add(c(3.5).roz(180).ty(E10 / 2))
        .add(c(2.5).roz(270).tx(-E8 / 2))
        .add(
            Wrk()
            .abox("++-", 4, 4, 4)
            .tx(B6 / 2)
            .ty(E10 / 2)
            .tz(B14)
        )
        .add(
            Wrk()
            .abox("+--", 4, 4, 4)
            .tx(B6 / 2)
            .ty(-E10 / 2)
            .tz(B14)
        )
        .add(
            Wrk()
            .abox("-+-", 4, 4, 4)
            .tx(-B6 / 2)
            .ty(E10 / 2)
            .tz(B14)
        )
        .add(
            Wrk()
            .abox("---", 4, 4, 4)
            .tx(-B6 / 2)
            .ty(-E10 / 2)
            .tz(B14)
        )
    )


def make_c():
    return (
        Wrk()
        .apbox(C8, C14, C3)
        .cut(
            make_magnet_cutout(C6, C5).tx(C4).ty(C9).tz(0.2)
        )
        .apbox(C13, C14, C1)
        .apbox(C13, C14, C1, C8 - C13)
        .apbox(C11, C12, C7, C8, C14 - C12, C2)
    )


def make_d():
    taper = 0.3

    def left():
        return (
            Wrk()
            .apbox(D4, D8, D7, D2, D1)
            .cut(
                Wrk()
                .rect(D4 - D3 * 2, D8 - D3 * 2, False)
                .workplane(
                    D7, origin=(taper / 2, taper / 2)
                )
                .rect(
                    D4 - D3 * 2 - taper,
                    D8 - D3 * 2 - taper,
                    False,
                )
                .loft()
                .tx(D2 + D3)
                .ty(D1 + D3),
            )
        )

    return (
        Wrk()
        .apcylinder(D6, D5, D5, 0, 0, D7)
        .add(left().tx(-D3 / 2))
        .add(left().tx(C8 - D4 + D3 * 2).tx(D3 / 2))
    )


def make_e():
    def left():
        return Wrk().apbox(E9, E15, E1, E3, E13)

    return (
        Wrk()
        .apbox(E8, E10, E1)
        .cut(left())
        .cut(left().tx(-E9 - E3 + E8 - E3))
        .cut(
            make_magnet_cutout(E5, E4)
            .rox(180)
            .tx(E6)
            .ty(E4 + E11)
            .tz(E5)
        )
        .cut(
            Wrk()
            .abox("--+", E3, E14, E7)
            .tx(E8)
            .ty(E13 + E15)
        )
    )


def make_magnet_tool():
    return (
        Wrk()
        .abox("0++", 5, 25, A11 + 0.2)
        .tz(-0.2)
        .add(Wrk().abox("0++", 15, 17, A11 + 0.2).tz(-0.2))
        .cut(
            make_magnet_cutout(
                A11,
                A5,
            )
            .tx(-A5 / 2)
            .ty(20)
        )
    )


# show(make_a(front=1, tall=1.5).export("a.stl"))
# show(make_a(front=1, tall=4.5).export("a_tall.stl"))
# show(make_a().export("a_short.stl"))
# show(make_b().export("b.stl"))
# show(make_c().export("c.stl"))
# show(make_d().export("d.stl"))
# show(make_e().export("e.stl"))
show(make_temp_cluster().export("temp_cluster.stl"))

# show(make_magnet_tool().export("magnet_tool.stl"))
# show(make_magnet_helper().export("magnet_helper.stl"))