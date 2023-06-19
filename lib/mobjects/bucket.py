from manim import *
import math
from lib.misc.compose_animations import ComposeAnimations

DEFAULT_LABEL_FONT = TexFontTemplates.american_typewriter


class Bucket(VGroup):
    def __init__(
        self,
        label=None,
        label_font=DEFAULT_LABEL_FONT,
        label_scaling=1,
        **kwargs,
    ):
        super().__init__(**kwargs)
        base = Line()
        left = Line(start=base.get_start(), end=base.end + RIGHT / 2)
        right = Line(start=base.get_end(), end=base.start + LEFT / 2)
        left.set_angle(PI / 2 + PI / 24)
        right.set_angle(PI / 2 - PI / 24)

        items_anchor = base

        self.add(base, left, right)

        self.bucket_height = self.height
        self.items_anchor = items_anchor
        self.base = base
        self.left = left
        self.right = right

        self.label_font = label_font
        self.label_scaling = label_scaling

        self.label = None
        self.surrounding_lines = None

        if label is not None:
            self.relabel(label)

        self.center()
        self.sort_submobjects()

    def relabel(self, label):
        if self.label is not None:
            self.remove(self.label)
        if self.surrounding_lines is not None:
            self.remove(self.surrounding_lines)

        max_width = self.base.get_length() * 0.9
        stroke_width = 2
        buff = 0.05
        label_tex = MathTex(r"\left[", label, r"\right]", tex_template=self.label_font)
        label_tex.scale_to_fit_height(
            self.bucket_height * 0.1 * self.label_scaling
        )
        label_tex.next_to(
            self.base, UP, buff=(self.left.height - label_tex.height) / 2
        )
        if label_tex.width > max_width:
            label_tex.set(width=max_width)

        surrounding_lines = VGroup(
            Line(stroke_width=stroke_width).shift(
                UP * (label_tex.height + buff)
            ),
            Line(stroke_width=stroke_width).shift(
                UP * (label_tex.height + 2 * buff)
            ),
            Line(stroke_width=stroke_width).shift(DOWN * buff),
            Line(stroke_width=stroke_width).shift(DOWN * 2 * buff),
        ).move_to(label_tex)
        self.add(label_tex, surrounding_lines)

        self.label = label_tex
        self.items_anchor = self.label
        self.surrounding_lines = surrounding_lines
        self.sort_submobjects()
        return self

    @override_animate(relabel)
    def _relabel_animate(self, label, anim_args={}):
        target = self.generate_target()
        target.relabel(label)
        return MoveToTarget(self, **anim_args)

    def put_in(self, obj):
        return self

    @override_animate(put_in)
    def _put_in_animation(self, obj, *args, **kwargs):
        return PutInBucket(obj, self, *args, **kwargs)

    def take_out(self, obj):
        obj.next_to(self, UP)
        return self

    @override_animate(take_out)
    def _take_out_animation(self, obj, *args, **kwargs):
        return TakeOutBucket(obj, self, *args, **kwargs)


class PutInBucket(ComposeAnimations):
    def __init__(
        self,
        item,
        bucket,
        *args,
        move_above_weight=1 / 2,
        move_into_weight=1 / 2,
        **kwargs,
    ):
        super().__init__(item, *args, **kwargs)
        self.bucket = bucket
        self.move_above_weight = move_above_weight
        self.move_into_weight = move_into_weight
        self.add_directives(
            (move_above_weight, PutInBucket.move_above),
            (move_into_weight, PutInBucket.move_into),
        )

    def move_above(self, alpha: float):
        self.mobject.become(self.starting_mobject)
        to_above_vector = (
            self.bucket.get_critical_point(UP)
            - self.starting_mobject.get_center()
        )
        self.mobject.shift(
            to_above_vector * rate_functions.ease_in_cubic(alpha)
        )

    def _normalize(self):
        if self.move_above_weight < 0:
            self.mobject.become(self.starting_mobject)
        else:
            self.move_above(1)

    def move_into(self, alpha: float):
        self._normalize()
        into_bucket_vector = (
            self.bucket.items_anchor.get_critical_point(UP)
            - self.mobject.get_center()
        )
        self.mobject.scale_to_fit_height(
            rate_functions.ease_in_cubic(1 - alpha)
            * self.starting_mobject.height
        ).shift(into_bucket_vector * rate_functions.ease_out_cubic(alpha))

    def clean_up_from_scene(self, scene):
        self.mobject.become(self.starting_mobject)
        scene.remove(self.mobject)


class TakeOutBucket(ComposeAnimations):
    def __init__(
        self,
        item,
        bucket,
        *args,
        move_out_weight=1,
        move_above=True,
        extra_directives=[],
        **kwargs,
    ):
        super().__init__(item, *args, **kwargs)
        self.move_above = move_above
        self.bucket = bucket
        self.add_directives(
            (move_out_weight, TakeOutBucket.move_out), *extra_directives
        )

    def move_out(self, alpha: float):
        self.mobject.become(self.starting_mobject).move_to(
            self.bucket.items_anchor.get_critical_point(UP)
        )
        target = (
            self.starting_mobject.copy().next_to(self.bucket, UP).get_center()
            if self.move_above
            else self.starting_mobject.get_center()
        )
        to_above_vector = target - self.mobject.get_center()
        self.mobject.scale_to_fit_height(
            rate_functions.ease_in_cubic(alpha) * self.starting_mobject.height
        ).shift(to_above_vector * rate_functions.ease_in_cubic(alpha))


class BucketTest(Scene):
    def test_looks(self):
        self.add(Tex("Looks").to_edge(UP))
        group = VGroup(
            Bucket(),
            Bucket(label="0.9"),
            Bucket(label=r"0.9\ldots"),
            Bucket(label=r"\frac{9}{10}", label_scaling=2),
        ).arrange()
        self.add(group)
        self.wait()
        self.clear()

    def test_putin(self):
        self.add(Tex("Put in").to_edge(UP))
        bucket = Bucket(label="0.9")
        dot = Dot().next_to(bucket, UP).shift(LEFT)
        self.add(bucket, dot)
        self.play(PutInBucket(dot, bucket))
        self.wait()
        self.play(PutInBucket(dot, bucket, move_above_weight=0))
        self.wait()
        self.play(PutInBucket(dot, bucket, move_above_weight=-1))
        self.wait()
        self.clear()

    def test_takeout(self):
        self.add(Tex("Take out").to_edge(UP))
        bucket = Bucket(label="0.9")
        dot = Dot().next_to(bucket, UP).shift(LEFT)
        self.add(bucket, dot)
        self.play(TakeOutBucket(dot, bucket, move_above=False))
        self.wait()
        self.play(TakeOutBucket(dot, bucket))
        self.wait()
        self.play(
            TakeOutBucket(
                dot,
                bucket,
                extra_directives=[
                    (0.5, lambda anim, alpha: anim.mobject.shift(RIGHT * alpha))
                ],
            )
        )
        self.wait()
        self.clear()

    def test_collective(self):
        self.add(Tex("Collective").to_edge(UP))
        bucket = Bucket(label="0.9")
        dots = VGroup(*[Dot() for _ in range(5)]).arrange().next_to(bucket, UP)
        self.add(bucket, dots)
        self.play(
            LaggedStart(
                *[
                    TakeOutBucket(
                        dots[len(dots) - i - 1], bucket, move_above=False
                    )
                    for i in range(len(dots))
                ],
                lag_ratio=0.02,
            )
        )
        self.wait()
        self.play(
            LaggedStart(
                *[
                    PutInBucket(dots[i], bucket, move_above_weight=-1)
                    for i in range(len(dots))
                ],
                lag_ratio=0.02,
            )
        )
        self.wait()
        self.clear()

    def test_compare(self):
        self.add(Tex("Compare").to_edge(UP))
        bucket = Bucket(label="0.9")
        dot = Dot().next_to(bucket, UP)
        self.add(bucket, dot)
        self.wait()
        self.play(PutInBucket(dot, bucket, move_above_weight=-1))
        self.play(TakeOutBucket(dot, bucket))
        self.wait()
        self.clear()

    def test_relabel(self):
        self.add(Tex("Relabel").to_edge(UP))
        bucket = Bucket(label="0.9")
        self.add(bucket)
        self.play(bucket.animate.relabel("0.99"))
        self.wait()

    def construct(self):
        self.test_looks()
        self.test_putin()
        self.test_takeout()
        self.test_collective()
        self.test_compare()
        self.test_relabel()
