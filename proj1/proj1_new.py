from manim import *
from lib.mobjects.bucket import Bucket, PutInBucket, TakeOutBucket
from lib.mobjects.scale import Scale, WeighScale
from lib.mobjects.equations import Equations
from lib.mobjects.calculator import Calculator
from lib.misc.sequence_line import SequenceLine


class Intro(Scene):
    def opening(self):
        # You may have heard that 0.9... = 1.
        eq1 = MathTex(r"0.99\ldots = 1")
        eq1_copy = eq1.copy()
        eq2 = MathTex(r"\frac{1}{2} = \frac{2}{4}").set_opacity(0)
        scale_left, scale_right = MathTex(r"0.99\ldots = 1"), MathTex(
            r"0.99\ldots \neq 1"
        )
        scale = Scale(left_mobject=scale_left, right_mobject=scale_right)
        self.play(Write(eq1))
        self.wait()
        self.play(VGroup(eq1, eq2).animate.arrange(DOWN).set_opacity(1))
        self.wait()

        # We get to choose
        self.play(
            ReplacementTransform(eq1, scale_left), FadeIn(scale), FadeOut(eq2)
        )
        self.play(WeighScale(scale))
        self.wait()

        # Before we do that though, let's take a closer look at this statement
        self.play(FadeOut(scale), ReplacementTransform(scale_left, eq1_copy))

        self.wait()
        self.clear()

    def p1(self):
        # The claim is that this number
        eq1 = MathTex(r"0.99\ldots", "=", "1")
        eq1_copy = eq1.copy()
        added_9s = [
            MathTex(f"0.{'9' * i}\\ldots", "=", "1")
            .move_to(eq1)
            .align_to(eq1, RIGHT)
            for i in range(3, 6)
        ]
        reasoning = VGroup(
            MathTex(r"0.99\ldots<x<1"), MathTex(r"x=\text{ ?}")
        ).arrange(DOWN)

        self.add(eq1)
        self.play(Indicate(eq1.get_part_by_tex(r"0.99\ldots"), color=WHITE))
        self.wait()
        self.play(Indicate(eq1.get_part_by_tex("1")), color=WHITE)
        # What does it even mean to have an infinite amount of 9's?
        self.play(ReplacementTransform(eq1, added_9s[0]))
        for i in range(0, len(added_9s) - 1):
            self.play(ReplacementTransform(added_9s[i], added_9s[i + 1]))

        eq1.become(eq1_copy)
        self.remove(eq1_copy, eq1)
        self.play(ReplacementTransform(added_9s[-1], eq1))
        self.wait()

        # But you might reason that 0.9 is pretty close to 1
        sequence_line = SequenceLine(
            sequence=lambda n: (10**n - 1) / 10**n,
            converge_value=1,
            sequence_str=lambda n: "0." + ("9" * n),
            samples=100,
            padding_scale=2,
            number_line_width=self.camera.frame_width,
            interval_direction="below",
            show_xn_text=False,
        )
        sequence_line.epsilon.set_value(0.1)
        self.play(
            eq1.animate.next_to(
                sequence_line.number_line,
                UP,
                buff=4 * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
            ),
            Create(sequence_line.number_line),
            GrowFromCenter(sequence_line.sequence_dots[1]),
            GrowFromCenter(sequence_line.converges_dot),
            FadeIn(
                sequence_line.sequence_texts[1],
                sequence_line.converges_text,
            ),
        )
        self.play(
            Create(
                sequence_line.interval,
            ),
            FadeIn(sequence_line.epsilon_text),
        )
        self.wait()

        self.play(
            FadeOut(
                sequence_line.sequence_texts[1], sequence_line.converges_text
            ),
            FadeIn(sequence_line.sequence_texts[2]),
            GrowFromCenter(sequence_line.sequence_dots[2]),
            sequence_line.epsilon.animate.set_value(0.01),
        )
        self.wait()
        self.play(sequence_line.value_scaling.animate.set_value(10))
        self.play(
            FadeOut(sequence_line.sequence_texts[2]),
            FadeIn(sequence_line.sequence_texts[3]),
            GrowFromCenter(sequence_line.sequence_dots[3]),
            sequence_line.epsilon.animate.set_value(0.001),
        )
        self.wait()
        self.play(
            Uncreate(sequence_line.interval),
            Uncreate(sequence_line.epsilon_text),
            Uncreate(sequence_line.number_line),
            FadeOut(
                sequence_line.sequence_texts[3],
                sequence_line.sequence_dots[1],
                sequence_line.sequence_dots[2],
                sequence_line.sequence_dots[3],
                sequence_line.converges_dot,
            ),
            eq1.animate.next_to(
                reasoning, UP, buff=2 * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
            ),
        )
        self.wait()
        self.play(Create(reasoning))
        self.wait()
        self.play(FadeOut(reasoning), eq1.animate.center())
        self.wait()

        eqs = Equations(MathTex(r"0.99\ldots", "=", "x"))
        self.play(TransformMatchingTex(eq1, eqs[0]))
        self.wait()
        self.play(
            eqs.animate.add_equation(
                MathTex(r"10\times", r"0.99\ldots", "=", "10", "x")
            )
        )
        self.wait()
        self.play(
            eqs.animate.change_equation(MathTex(r"9.99\ldots", "=", "10x"))
        )
        self.wait()
        self.play(
            eqs.animate.add_equation(
                MathTex(r"9.99\ldots", r"-0.99\ldots", "=", "10x", "-x")
            )
        )
        self.wait()
        self.play(eqs.animate.change_equation(MathTex(r"9", "=", "9x")))
        self.wait()
        self.play(eqs.animate.add_equation(MathTex(r"1", "=", "x")))
        self.wait()

        # But what really even is 0.99...?
        self.play(FadeOut(eqs))
        self.play(Write(MathTex(r"0.99\ldots")))

        self.wait()
        self.clear()

    def p2(self):
        eqs = Equations(MathTex("0.99", r"\ldots"), align_opts={"mode": "none"})
        self.add(eqs)
        self.play(eqs.animate.add_equation(MathTex("0.9")))
        self.play(eqs.animate.change_equation(MathTex("0.99")))
        self.play(eqs.animate.change_equation(MathTex("0.999")))
        self.wait()
        self.play(eqs.animate.remove_equation_by_index(-1))
        self.wait()
        self.play(Indicate(eqs[0][1]))
        self.wait()

        # Let's imagine a different number
        eq1 = MathTex(r"\ldots99")
        added_9s = [MathTex(*(["9"] * i)) for i in range(1, 6)]

        self.play(FadeOut(eqs, shift=UP), Write(added_9s[0]))

        for i in range(0, 4):
            self.play(ReplacementTransform(added_9s[i], added_9s[i + 1]))

        self.play(TransformMatchingTex(added_9s[-1], eq1))
        self.wait()

        eqs = Equations(MathTex(r"\ldots99", "=", "x"))
        self.play(TransformMatchingTex(eq1, eqs))
        self.wait()
        self.play(
            eqs.animate.add_equation(
                MathTex(r"10\times", r"\ldots99", "=", "10", "x")
            )
        )
        self.wait()
        self.play(
            eqs.animate.change_equation(MathTex(r"\ldots990", "=", "10x"))
        )
        self.wait()
        self.play(
            eqs.animate.add_equation(
                MathTex(r"\ldots990", r"-\ldots99", "=", "10x", "-x")
            )
        )
        self.wait()
        self.play(eqs.animate.change_equation(MathTex(r"-9", "=", "9x")))
        self.wait()
        self.play(eqs.animate.add_equation(MathTex("-1", "=", "x")))
        self.wait()

        self.clear()

    def p3(self):
        # As it stands, 0.99... and ...99 are concepts
        def create_concept(title, description):
            concept = VGroup()
            concept_title = MathTex(title)
            concept_description = (
                Tex(description, font_size=DEFAULT_FONT_SIZE * 0.75)
                .next_to(
                    concept_title,
                    DOWN,
                    buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2,
                )
                .align_to(concept_title, LEFT)
            )
            concept.add(concept_title, concept_description)
            concept_surround = SurroundingRectangle(
                concept, color=WHITE, buff=MED_LARGE_BUFF
            )
            concept.add(concept_surround)
            return concept.center()

        concept1 = create_concept(
            r"0.99\ldots", r"Write $0.9$, then $0.99$, then\ldots"
        )
        concept2 = create_concept(
            r"\ldots99", r"Write $9$, then $99$, then\ldots"
        )
        concept3 = create_concept(r"\infty", r"Never ending")

        concept_group = VGroup(concept1, concept2).arrange(RIGHT)

        self.play(FadeIn(concept_group))
        self.wait()
        # The same way that infinity as a concept
        self.play(
            concept_group.animate.shift(UP),
            FadeIn(concept3.next_to(concept_group, DOWN)),
        )
        self.wait()
        concept_group.add(concept3)
        target = concept_group.generate_target()
        target.arrange(DOWN).to_edge(LEFT)

        times10s = [
            MathTex(r"\times 10 = \text{ ???}").next_to(target[i])
            for i in range(3)
        ]

        self.play(
            Succession(
                *[Succession(FadeIn(times10s[i]), Wait()) for i in range(3)]
            ),
            MoveToTarget(concept_group),
        )
        self.wait()

        # Yet there's a desire
        concept_group.remove(concept2, concept3)
        concept_group.add(MathTex(r"\approx", "1").set_opacity(0))
        self.play(
            FadeOut(concept2, concept3, *times10s),
            concept_group.animate.arrange(),
        )
        self.play(concept_group[1].animate.set_opacity(1))
        self.wait()

        # In this branch of mathematics,
        self.play(
            concept_group[1].animate.become(
                MathTex(r"\to", "1").move_to(concept_group[1])
            )
        )
        self.wait()

        original_statement = MathTex(r"0.99\ldots", r"=", "1")

        self.play(concept_group.animate.become(original_statement))
        self.wait()

        self.clear()

    def construct(self):
        self.opening()
        self.p1()
        self.p2()
        self.p3()


class Chapter1(Scene):
    def p1(self):
        # Why is 1 = 2/2 = 3/3?
        eq1 = MathTex("1", "=", r"\frac{2}{2}")
        eq2 = MathTex("1", "=", r"\frac{3}{3}")
        eq3 = MathTex("1", "=", r"3\div 3")

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait()

        calculator = Calculator().center()
        eq_on_screen1 = MathTex(r"3\div 3")
        eq_on_screen2 = MathTex(r"1")
        calculator.move_obj_to_screen(eq_on_screen1)
        self.play(
            FadeOut(eq3, shift=DOWN),
            FadeIn(Group(calculator, eq_on_screen1), shift=DOWN),
        )
        self.wait()
        self.play(calculator.animate.tap_button("="))
        calculator.move_obj_to_screen(eq_on_screen2)
        self.add(eq_on_screen2)
        self.remove(eq_on_screen1)
        self.wait()

        # The fraction 2/2 is two whole numbers separated by a line
        self.play(FadeOut(calculator))
        fraction = MathTex(r"\frac{2}{2}", r"\neq", r"2\div2")
        self.play(FadeIn(fraction))
        self.wait()
        self.play(FadeOut(fraction))

        eqs = [
            MathTex("1"),
            MathTex("="),
            MathTex(r"\frac{2}{2}"),
            MathTex("="),
            MathTex(r"0.99\ldots"),
        ]
        for eq in eqs:
            eq.set_opacity(0)
        VGroup(*eqs).arrange(buff=1)

        dimension = max(
            eqs[0].width,
            eqs[0].height,
            eqs[2].width,
            eqs[2].height,
            eqs[4].width,
            eqs[4].height,
        )
        rectangle1 = Rectangle(
            width=dimension * 1.5,
            height=dimension * 1.5,
            color=WHITE,
            fill_color=DARK_BROWN,
            fill_opacity=1,
        ).set_opacity(0)
        rectangle2 = rectangle1.copy()
        rectangle3 = rectangle1.copy()
        rectangle1.move_to(eqs[0])
        rectangle2.move_to(eqs[2])
        rectangle3.move_to(eqs[4])

        obj1 = VGroup(rectangle1, eqs[0])
        obj2 = VGroup(rectangle2, eqs[2])
        obj3 = VGroup(rectangle3, eqs[4])

        group = VGroup(obj1, eqs[1], obj2)
        self.play(group.animate.arrange(buff=1).set_opacity(1))
        self.wait()

        group.add(eqs[3], obj3)
        self.play(group.animate.arrange(buff=1).set_opacity(1))
        self.wait()

        self.clear()

    def p2(self):
        # We want
        want1, want2 = MathTex("1", r"\sim", r"\frac{2}{2}"), MathTex(
            "1", r"\sim", r"\frac{3}{3}"
        )
        item1, item2, item3 = (
            MathTex("1"),
            MathTex(r"\frac{2}{2}"),
            MathTex(r"\frac{3}{3}"),
        )

        bucket1 = Bucket(label="1")
        bucket2 = Bucket(label=r"\frac{2}{2}", label_scaling=2)

        want_group = VGroup(want1, want2).arrange(
            RIGHT, buff=2 * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        )
        item_group = VGroup(item1, item2, item3).arrange(
            RIGHT, buff=4 * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        )

        self.play(Succession(FadeIn(want1), Wait(), FadeIn(want2), Wait()))
        self.wait()
        self.play(
            Create(bucket1),
            want_group.animate.become(item_group.next_to(bucket1, UP)),
        )
        self.add(item_group)
        self.remove(want_group)
        self.wait()

        self.play(
            Succession(
                *[
                    Succession(
                        AnimationGroup(
                            Indicate(bucket1.label, scale_factor=1),
                            Indicate(item, scale_factor=1),
                        ),
                        PutInBucket(item, bucket1, move_above_weight=-1),
                        Wait(),
                    )
                    for item in item_group
                ]
            )
        )

        more_items = (
            VGroup(
                *[MathTex(f"\\frac{{{i}}}{{{i}}}") for i in range(4, 8)],
                MathTex(r"\ldots"),
            )
            .arrange(RIGHT)
            .next_to(bucket1, UP)
        )
        self.play(FadeIn(more_items, shift=DOWN))
        self.play(
            LaggedStart(
                *[
                    PutInBucket(item, bucket1, move_above_weight=-1)
                    for item in more_items
                ],
                lag_ratio=0.25,
            ),
            run_time=4,
        )
        self.wait()

        bucket2.set_opacity(0)
        self.play(
            VGroup(bucket1, bucket2)
            .animate.arrange(buff=2 * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
            .set_opacity(1)
        )
        self.wait()
        self.play(FadeIn(item_group.next_to(bucket2, UP), shift=DOWN))
        self.wait()

        self.play(
            Succession(
                *[
                    Succession(
                        AnimationGroup(
                            Indicate(bucket2.label, scale_factor=1),
                            Indicate(item, scale_factor=1),
                        ),
                        PutInBucket(item, bucket2, move_above_weight=-1),
                        Wait(),
                    )
                    for item in item_group
                ]
            )
        )
        self.play(FadeIn(more_items.next_to(bucket2, UP), shift=DOWN))
        self.play(
            LaggedStart(
                *[
                    PutInBucket(item, bucket2, move_above_weight=-1)
                    for item in more_items
                ],
                lag_ratio=0.25,
            ),
            run_time=4,
        )
        self.wait()
        # They're equal because
        self.play(
            VGroup(bucket1, MathTex("=").set_opacity(0), bucket2)
            .animate.arrange()
            .set_opacity(1)
        )
        self.wait()
        relabel_items = (
            VGroup(
                *[MathTex(f"\\frac{{{i}}}{{{i}}}") for i in range(3, 7)],
                MathTex(r"\ldots"),
            )
            .arrange(RIGHT)
            .next_to(bucket2, UP)
        )
        self.play(
            LaggedStart(
                *[
                    TakeOutBucket(
                        item, bucket2, move_above=False
                    )
                    for item in relabel_items
                ],
                lag_ratio=0.02,
            )
        )
        self.wait()
        for item in relabel_items[:-1]:
            target = bucket2.generate_target()
            target.relabel(item.tex_string)
            self.play(item.animate.become(target.label), MoveToTarget(bucket2))
            self.remove(item)

        self.wait()

        self.clear()

    def p3(self):
        # We implicitly said that two fractions
        pass

    def construct(self):
        self.p1()
        self.p2()
        self.p3()
