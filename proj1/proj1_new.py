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
                    TakeOutBucket(item, bucket2, move_above=False)
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
        rules1 = Tex(r"$\frac{a}{b}\sim\frac{c}{d}$ if $ad=bc$")
        rules1 = VGroup(
            rules1,
            SurroundingRectangle(rules1, color=WHITE, buff=MED_LARGE_BUFF),
        )
        rules2 = Tex(
            r"$\frac{a}{b}\sim\frac{c}{d}$ if $ad=bc$",
            r"\\",
            r"Also, $\frac{1}{2}\sim\frac{1}{3}$",
        )
        rules2[2].set_color(RED)
        rules2 = VGroup(
            rules2,
            SurroundingRectangle(rules2, color=WHITE, buff=MED_LARGE_BUFF),
        )

        self.play(Write(rules1))
        self.wait()
        rules1_copy = rules1.copy()
        rules_group = VGroup(rules1, rules1_copy)
        target = rules_group.generate_target()
        target[1] = rules2
        target.arrange(buff=MED_LARGE_BUFF)

        self.play(
            MoveToTarget(rules_group), rules1_copy.animate.become(target[1])
        )
        self.remove(rules1_copy)
        self.add(rules2)
        rules2.move_to(rules_group[1])
        rules_group.remove(rules_group[1])
        rules_group.add(rules2)
        self.wait()

        # Show 1/2 = 1/3
        bucket1, bucket2 = Bucket(
            label=r"\frac{1}{2}", label_scaling=2
        ), Bucket(label=r"\frac{1}{3}", label_scaling=2)
        target = rules_group.generate_target().to_edge(UP)
        bucket_group2 = (
            VGroup(bucket1, MathTex("="), bucket2)
            .arrange()
            .next_to(target[1], DOWN, buff=MED_LARGE_BUFF)
        )
        self.play(MoveToTarget(rules_group), FadeIn(bucket_group2))
        self.wait()

        # So what would make us prefer one definition over the other?
        scale_left, scale_right = rules1.copy().scale(0.5), rules2.copy().scale(
            0.4
        )
        scale = Scale(left_mobject=scale_left, right_mobject=scale_right)

        self.play(
            FadeOut(bucket_group2),
            FadeIn(scale),
            rules1.animate.become(scale_left),
            rules2.animate.become(scale_right),
        )
        self.remove(rules1, rules2)
        self.play(WeighScale(scale))
        self.wait()

        # As it stands though, these buckets aren't very useful

        bucket1, bucket2 = Bucket(
            label=r"\frac{1}{2}", label_scaling=2
        ), Bucket(label=r"\frac{1}{6}", label_scaling=2)
        bucket_group2 = VGroup(
            bucket1, MathTex("+"), bucket2, MathTex("="), Tex("?")
        ).arrange()
        self.play(FadeOut(scale, bucket_group2), FadeIn(bucket_group2))

        integers_eq1, integers_eq2 = MathTex("2", "+", "6", "=", "8"), MathTex(
            "2", r"\times", "6", "=", "12"
        )
        fractions_eq1, fractions_eq2 = MathTex(
            r"\frac{1}{2}", "+", r"\frac{1}{6}", "=", r"\frac{8}{12}"
        ), MathTex(
            r"\frac{1}{2}", r"\times", r"\frac{1}{6}", "=", r"\frac{1}{12}"
        )

        self.play(
            FadeOut(bucket_group2, shift=UP), FadeIn(integers_eq1, shift=UP)
        )
        self.play(TransformMatchingTex(integers_eq1, integers_eq2))
        self.play(
            FadeOut(integers_eq2, shift=UP), FadeIn(fractions_eq1, shift=UP)
        )
        self.play(TransformMatchingTex(fractions_eq1, fractions_eq2))
        self.play(
            FadeOut(fractions_eq2, shift=UP), FadeIn(bucket_group2, shift=UP)
        )
        self.wait()

        self.clear()

    def p4(self):
        bucket1, bucket2, bucket3 = (
            Bucket(label=r"\frac{1}{2}", label_scaling=2),
            Bucket(label=r"\frac{1}{6}", label_scaling=2),
            Bucket(label=r"\frac{2}{3}", label_scaling=2),
        )
        bucket_group = VGroup(
            bucket1, MathTex("+"), bucket2, MathTex("="), Tex("?")
        ).arrange()
        self.add(bucket_group)
        self.wait()
        target = bucket_group.generate_target()
        target[-1] = bucket3
        target.arrange()
        self.play(MoveToTarget(bucket_group))
        bucket3 = bucket_group[-1]
        self.wait()

        # What happens when we add the labels together?
        add_labels_eqs = [
            MathTex(r"\frac{1}{2}", "+", r"\frac{1}{6}"),
            MathTex(r"\frac{6}{12}", "+", r"\frac{2}{12}"),
            MathTex(r"\frac{8}{12}"),
        ]
        for eq in add_labels_eqs:
            eq.next_to(bucket_group, UP)

        self.play(
            ReplacementTransform(bucket1.label.copy(), add_labels_eqs[0][0]),
            ReplacementTransform(bucket_group[1].copy(), add_labels_eqs[0][1]),
            ReplacementTransform(bucket2.label.copy(), add_labels_eqs[0][2]),
        )
        self.add(add_labels_eqs[0])
        self.wait()
        self.play(ReplacementTransform(add_labels_eqs[0], add_labels_eqs[1]))
        self.wait()
        self.play(ReplacementTransform(add_labels_eqs[1], add_labels_eqs[2]))
        self.wait()

        # Which isn't equal to 2/3... but the bucket labelled 8/12 is
        bucket_group2 = VGroup(
            Bucket(label=r"\frac{8}{12}", label_scaling=2).set_opacity(0),
            MathTex("=").set_opacity(0),
            bucket3,
        )
        target = bucket_group2.generate_target().arrange().set_opacity(1)
        self.play(
            FadeOut(*bucket_group[:-1]),
            MoveToTarget(bucket_group2),
        )
        self.play(add_labels_eqs[-1].animate.become(bucket_group2[0].label))
        self.remove(*add_labels_eqs)
        self.wait()

        bucket1, bucket2, bucket3 = (
            Bucket(label=r"\frac{1}{2}", label_scaling=2),
            Bucket(label=r"\frac{1}{6}", label_scaling=2),
            Bucket(label=r"\text{?}", label_scaling=2),
        )
        bucket_group = VGroup(
            bucket1, MathTex("+"), bucket2, MathTex("="), bucket3
        ).arrange()
        self.play(
            FadeOut(bucket_group2, shift=UP), FadeIn(bucket_group, shift=UP)
        )
        self.wait()

        add_labels_eqs = [
            MathTex(r"\frac{1}{2}", "+", r"\frac{1}{6}"),
            MathTex(r"\frac{6}{12}", "+", r"\frac{2}{12}"),
            MathTex(r"\frac{8}{12}"),
        ]
        for eq in add_labels_eqs:
            eq.next_to(bucket_group, UP)

        self.play(
            ReplacementTransform(bucket1.label.copy(), add_labels_eqs[0][0]),
            ReplacementTransform(bucket_group[1].copy(), add_labels_eqs[0][1]),
            ReplacementTransform(bucket2.label.copy(), add_labels_eqs[0][2]),
        )
        self.add(add_labels_eqs[0])
        self.wait()
        self.play(ReplacementTransform(add_labels_eqs[0], add_labels_eqs[1]))
        self.wait()
        self.play(ReplacementTransform(add_labels_eqs[1], add_labels_eqs[2]))
        self.wait()

        target = bucket3.generate_target().relabel(r"\frac{8}{12}")
        self.play(
            add_labels_eqs[-1].animate.become(target.label),
            MoveToTarget(bucket3),
        )
        self.remove(*add_labels_eqs)
        self.wait()

        # Which might be the same as
        self.play(bucket3.animate.relabel(r"\frac{2}{3}"))
        self.wait()

        self.clear()

    def p5(self):
        # What matters about a bucket isn't really the label
        bucket1, bucket2, bucket3 = (
            Bucket(label=r"\frac{1}{2}", label_scaling=2),
            Bucket(label=r"\frac{1}{6}", label_scaling=2),
            Bucket(label=r"\frac{2}{3}", label_scaling=2),
        )
        bucket_group = VGroup(
            bucket1, MathTex("+"), bucket2, MathTex("="), bucket3
        ).arrange()
        self.add(bucket_group)

        bucket_labels1 = (
            VGroup(*[MathTex(f"\\frac{{{i}}}{{{2*i}}}") for i in range(1, 4)])
            .arrange(buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
            .next_to(bucket1, UP)
        )
        bucket_labels2 = (
            VGroup(*[MathTex(f"\\frac{{{i}}}{{{6*i}}}") for i in range(1, 4)])
            .arrange(buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
            .next_to(bucket2, UP)
        )
        bucket_labels3 = (
            VGroup(*[MathTex(f"\\frac{{{2*i}}}{{{3*i}}}") for i in range(1, 4)])
            .arrange(buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
            .next_to(bucket3, UP)
        )
        bucket_labels1_copy = bucket_labels1.copy()
        bucket_labels2_copy = bucket_labels2.copy()
        bucket_labels3_copy = bucket_labels3.copy()

        self.play(
            TakeOutBucket(bucket_labels1, bucket1, move_above=False),
            TakeOutBucket(bucket_labels2, bucket2, move_above=False),
            TakeOutBucket(bucket_labels3, bucket3, move_above=False),
            bucket1.label.animate.set_opacity(0),
            bucket2.label.animate.set_opacity(0),
            bucket3.label.animate.set_opacity(0),
        )
        self.wait()

        target1, target2, target3 = (
            bucket1.generate_target(),
            bucket2.generate_target(),
            bucket3.generate_target(),
        )
        target1.label.set_opacity(1)
        target2.label.set_opacity(1)
        target3.label.set_opacity(1)
        self.play(
            MoveToTarget(bucket1),
            MoveToTarget(bucket2),
            MoveToTarget(bucket3),
            bucket_labels1_copy[0].animate.become(target1.label),
            bucket_labels2_copy[0].animate.become(target2.label),
            bucket_labels3_copy[0].animate.become(target3.label),
        )
        self.remove(
            bucket_labels1_copy[0],
            bucket_labels2_copy[0],
            bucket_labels3_copy[0],
        )
        self.wait()
        target = bucket1.generate_target()
        target.relabel(r"\frac{2}{4}")
        self.play(
            MoveToTarget(bucket1),
            bucket_labels1_copy[1].animate.become(target.label),
        )
        self.remove(bucket_labels1_copy[1])
        self.wait()

        add_labels_eqs = [
            MathTex(r"\frac{2}{4}", "+", r"\frac{1}{6}"),
            MathTex(r"\frac{12}{24}", "+", r"\frac{4}{24}"),
            MathTex(r"\frac{16}{24}"),
        ]
        for eq in add_labels_eqs:
            eq.next_to(bucket_group, UP)

        self.play(
            FadeOut(bucket_labels1, bucket_labels2, bucket_labels3, shift=UP),
            ReplacementTransform(bucket1.label.copy(), add_labels_eqs[0][0]),
            ReplacementTransform(bucket_group[1].copy(), add_labels_eqs[0][1]),
            ReplacementTransform(bucket2.label.copy(), add_labels_eqs[0][2]),
        )
        self.add(add_labels_eqs[0])
        self.wait()
        self.play(ReplacementTransform(add_labels_eqs[0], add_labels_eqs[1]))
        self.wait()
        self.play(ReplacementTransform(add_labels_eqs[1], add_labels_eqs[2]))
        self.wait()

        label_copy = add_labels_eqs[-1].copy().next_to(bucket3, UP)
        self.play(TakeOutBucket(label_copy, bucket3, move_above=False))
        self.wait()
        self.play(add_labels_eqs[-1].animate.become(label_copy))
        self.remove(add_labels_eqs[-1])
        self.wait()
        target = bucket3.generate_target()
        target.relabel(r"\frac{16}{24}")
        self.play(MoveToTarget(bucket3), label_copy.animate.become(target.label))
        self.remove(label_copy)

        self.clear()

    def p6(self):
        # I think it shouldn't be a surprise to tell you
        # TODO
        self.clear()

    def p7(self):
        # Let's go back to our competing definitions for sameness.
        rules1 = Tex(r"$\frac{a}{b}\sim\frac{c}{d}$ if $ad=bc$")
        rules1 = VGroup(
            SurroundingRectangle(rules1, color=WHITE, buff=MED_LARGE_BUFF, fill_color=BLACK),
            rules1,
        )
        rules2 = Tex(
            r"$\frac{a}{b}\sim\frac{c}{d}$ if $ad=bc$",
            r"\\",
            r"Also, $\frac{1}{2}\sim\frac{1}{3}$",
        )
        rules2[2].set_color(RED)
        rules2 = VGroup(
            SurroundingRectangle(rules2, color=WHITE, buff=MED_LARGE_BUFF, fill_color=BLACK),
            rules2,
        )

        rules_group = VGroup(rules1, rules2).arrange().to_edge(UP)

        bucket1, bucket2, bucket3 = (
            Bucket(label=r"\frac{1}{2}", label_scaling=2),
            Bucket(label=r"\frac{1}{6}", label_scaling=2),
            Bucket(label=r"\frac{2}{3}", label_scaling=2),
        )
        bucket_group = VGroup(
            bucket1, MathTex("+"), bucket2, MathTex("="), bucket3
        ).arrange().shift(DOWN)
        self.add(bucket_group, rules_group)
        self.wait()

    def construct(self):
        self.p1()
        self.p2()
        self.p3()
        self.p4()
        self.p5()
        self.p6()
