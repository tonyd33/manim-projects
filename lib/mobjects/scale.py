from manim import *
from lib.misc.compose_animations import ComposeAnimations


class Scale(Group):
    def __init__(
        self, *args, left_mobject: Mobject, right_mobject: Mobject, **kwargs
    ):
        super().__init__(*args, **kwargs)

        column_height = 3
        pivot_height_ratio = 0.8
        rope_height_ratio = 0.5
        scale_length_ratio = 0.5
        rope_cutoff_ratio = 0.25

        base = Arc(angle=PI)
        base_close = Line(
            start=base.get_corner(DOWN + LEFT),
            end=base.get_corner(DOWN + RIGHT),
        )
        column = Line(
            start=base.get_top(), end=base.get_top() + UP * column_height
        )

        pivot_point = base.get_top() + UP * column_height * pivot_height_ratio
        left_point = pivot_point + LEFT * base.width
        right_point = pivot_point + RIGHT * base.width

        left_base_point = left_point + DOWN * column_height * rope_height_ratio
        right_base_point = (
            right_point + DOWN * column_height * rope_height_ratio
        )

        left_base = Line(
            start=left_base_point
            + LEFT * column_height * scale_length_ratio / 2,
            end=left_base_point
            + RIGHT * column_height * scale_length_ratio / 2,
        )
        right_base = Line(
            start=right_base_point
            + LEFT * column_height * scale_length_ratio / 2,
            end=right_base_point
            + RIGHT * column_height * scale_length_ratio / 2,
        )

        pivot = Dot(pivot_point)
        cap = Dot(column.get_end())

        lever_arm = Line(start=left_point, end=right_point)

        left_rope1 = Line(
            start=left_point,
            end=left_point
            + DOWN * rope_height_ratio * rope_cutoff_ratio * column_height,
        )
        left_rope2 = left_rope1.copy()
        right_rope1 = Line(
            start=right_point,
            end=right_point
            + DOWN * rope_height_ratio * rope_cutoff_ratio * column_height,
        )
        right_rope2 = right_rope1.copy()

        left_rope1.rotate(-PI / 6, about_point=left_point)
        left_rope2.rotate(PI / 6, about_point=left_point)
        right_rope1.rotate(-PI / 6, about_point=right_point)
        right_rope2.rotate(PI / 6, about_point=right_point)

        left_ropes = Group(left_rope1, left_rope2)
        right_ropes = Group(right_rope1, right_rope2)

        left_ropes.add_updater(
            lambda z: z.move_to(lever_arm.get_start()).align_to(
                lever_arm.get_start(), UP
            )
        )
        right_ropes.add_updater(
            lambda z: z.move_to(lever_arm.get_end()).align_to(
                lever_arm.get_end(), UP
            )
        )

        left_base.add_updater(
            lambda z: z.move_to(lever_arm.get_start()).shift(
                DOWN * column_height * rope_height_ratio
            )
        )
        right_base.add_updater(
            lambda z: z.move_to(lever_arm.get_end()).shift(
                DOWN * column_height * rope_height_ratio
            )
        )

        left_mobject.next_to(left_base, UP)
        right_mobject.next_to(right_base, UP)

        left_mobject.add_updater(lambda z: z.next_to(left_base, UP))
        right_mobject.add_updater(lambda z: z.next_to(right_base, UP))

        self.lever_arm = lever_arm
        self.pivot = pivot

        self.add(
            base,
            base_close,
            column,
            pivot,
            cap,
            lever_arm,
            left_ropes,
            right_ropes,
            left_base,
            right_base,
            left_mobject,
            right_mobject,
        )
        self.center()


class WeighScale(ComposeAnimations):
    def __init__(self, scale: Scale, *args, angle: float = PI/12, run_time=4, **kwargs):
        super().__init__(scale.lever_arm, *args, run_time=run_time, **kwargs)
        self.scale = scale
        self.angle = angle
        self.add_directives(
            (0.5, WeighScale.rotate1), (0.5, WeighScale.rotate2)
        )

    def rotate1(self, alpha: float):
        self.mobject.become(self.starting_mobject)
        self.mobject.rotate(
            there_and_back(alpha) * self.angle,
            about_point=self.scale.pivot.get_center(),
        )

    def rotate2(self, alpha: float):
        self.mobject.become(self.starting_mobject)
        self.mobject.rotate(
            -there_and_back(alpha) * self.angle,
            about_point=self.scale.pivot.get_center(),
        )


class ScaleTest(Scene):
    def construct(self):
        scale = Scale(
            left_mobject=MathTex(r"0.9\ldots=1"),
            right_mobject=MathTex(r"0.9\ldots\neq1"),
        )
        self.add(scale)
        self.wait()
        self.play(WeighScale(scale, angle=PI / 12))
        self.play(WeighScale(scale, angle=PI / 12))
        self.play(WeighScale(scale, angle=PI / 12))
