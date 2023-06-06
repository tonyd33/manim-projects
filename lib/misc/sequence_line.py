from manim import *
from typing import Optional, Literal
import math


def _scaler(dist_to_converges_value_in_line):
    return abs(
        1
        / ((math.log10(min(max(dist_to_converges_value_in_line, 0.1), 9)) - 1))
    )


_DOT_SCALE_FACTOR = 0.25
EPSILON_CORRECTION = 10e-10


class _Interval(Line):
    def __init__(self, length=0.25, color=WHITE, *args, **kwargs):
        super().__init__(*args, color=color, **kwargs)
        l1 = Line(start=np.zeros((3)), end=RIGHT * length, color=color).rotate(
            PI / 2
        )
        l2 = l1.copy()
        l1.align_to(self, LEFT)
        l2.align_to(self, RIGHT)
        self.add(l1, l2)


class SequenceLine(Mobject):
    def __init__(
        self,
        sequence: Callable[[int], float],
        converge_value: float,
        # 1/2 will get flattened into float 0.5. We may still want 1 and 2 for
        # display though.
        sequence_str: Optional[Callable[[int], str]] = None,
        *args,
        samples: int = 500,
        text_samples: int = 10,
        number_line_width: float,
        # If ranges are in interval X, will add |X| * padding_scale /2 on
        # left and right
        padding_scale: float = 3 / 4,
        interval_direction: Literal["below", "above", "both"] = "both",
        **kwargs,
    ):
        self.sequence = sequence
        self.converge_value = converge_value
        self.sequence_str = sequence_str
        self.samples = samples
        self.text_samples = text_samples
        self.number_line_width = number_line_width
        self.padding_scale = padding_scale
        self.interval_direction = interval_direction

        self.value_scaling = ValueTracker(1)
        self.epsilon = ValueTracker(1)
        self.epsilon_changes_color = False

        self._construct_number_line()
        self._construct_dots()
        self._construct_texts()
        self._construct_interval()
        self._construct_epsilon_text()
        self._construct_N_label()

        super().__init__(*args, **kwargs)

    def _construct_number_line(self):
        self.sequence_values = {
            i: self.sequence(i) for i in range(1, self.samples + 1)
        }
        low, high = min(
            self.converge_value, *self.sequence_values.values()
        ), max(self.converge_value, *self.sequence_values.values())
        buff = (high - low) * self.padding_scale / 2

        self.number_line = NumberLine(
            x_range=[low - buff, high + buff],
            length=self.number_line_width,
            include_ticks=False,
        )

    def _construct_dots(self):
        self.sequence_dots = {
            i: Dot(self.number_line.n2p(val), color=BLUE)
            .set(true_value=val)
            .scale_to_fit_height(
                _scaler(
                    abs(val - self.converge_value)
                    * self.value_scaling.get_value()
                )
                * _DOT_SCALE_FACTOR
            )
            for i, val in self.sequence_values.items()
        }
        self.converges_dot = Dot(
            self.number_line.n2p(self.converge_value), color=PURPLE
        )

        def dot_scale_updater(z):
            dist_to_converges_in_line = (
                self.converge_value - z.true_value
            ) * self.value_scaling.get_value()
            z.set_x(
                self.number_line.n2p(
                    self.converge_value - dist_to_converges_in_line
                )[0]
            )
            z.scale_to_fit_height(
                _scaler(abs(dist_to_converges_in_line)) * _DOT_SCALE_FACTOR
            )

        def dot_color_updater(z):
            if (
                abs(self.converge_value - z.true_value) + EPSILON_CORRECTION
                > self.epsilon.get_value()
            ):
                z.set_color(BLUE)
            else:
                if self.epsilon_changes_color:
                    z.set_color(GREEN)

        for dot in self.sequence_dots.values():
            dot.add_updater(dot_scale_updater)
            dot.add_updater(dot_color_updater)

    def _construct_texts(self):
        def sequence_text_value(i):
            if self.sequence_str is not None:
                return self.sequence_str(i)
            return f"{self.sequence_values[i]:.4}"

        self.sequence_texts = {}
        for i in range(1, self.text_samples + 1):
            self.sequence_texts[i] = MathTex(
                f"x_{{{i}}}={sequence_text_value(i)}"
            ).next_to(self.sequence_dots[i], DOWN)

    def _find_interval_endpoints(self):
        above_mult = 0 if self.interval_direction == "below" else 1
        below_mult = 0 if self.interval_direction == "above" else 1
        start = self.number_line.n2p(
            self.converge_value
            - below_mult
            * self.value_scaling.get_value()
            * self.epsilon.get_value()
        )
        end = self.number_line.n2p(
            self.converge_value
            + above_mult
            * self.value_scaling.get_value()
            * self.epsilon.get_value()
        )
        return start, end

    def _get_interval(self):
        start, end = self._find_interval_endpoints()
        return _Interval(
            start=start,
            end=end,
            color=YELLOW,
        ).shift(DOWN * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)

    def _construct_interval(self):
        self.interval = self._get_interval()

        def interval_updater(z):
            z.become(self._get_interval())

        self.interval.add_updater(interval_updater)

    def _get_epsilon_text(self):
        return MathTex(
            f"{self.epsilon.get_value():.4}",
            color=YELLOW,
            font_size=32,
        ).next_to(self.interval, DOWN, buff=0.3)

    def _construct_epsilon_text(self):
        self.epsilon_text = self._get_epsilon_text()

        def epsilon_text_updater(z):
            z.become(self._get_epsilon_text())

        self.epsilon_text.add_updater(epsilon_text_updater)

    def _get_N_value(self):
        for i, val in self.sequence_values.items():
            if (
                abs(self.converge_value - val) + EPSILON_CORRECTION
                < self.epsilon.get_value()
            ):
                return i
        return 1

    def _get_N_label(self):
        N = self._get_N_value()
        N_label = MathTex(f"N={N}", font_size=32, color=GREEN).next_to(
            self.sequence_dots[N], UP
        )
        return N_label

    def _construct_N_label(self):
        self.N_label = self._get_N_label()

        def N_label_updater(z):
            z.become(self._get_N_label())

        self.N_label.add_updater(N_label_updater)


class SequenceLineTest(Scene):
    def construct(self):
        sequence_line = SequenceLine(
            sequence=lambda n: (10**n - 1) / 10**n,
            converge_value=1,
            sequence_str=lambda n: "0." + ("9" * n),
            samples=100,
            number_line_width=self.camera.frame_width,
            interval_direction="below",
        )
        self.play(Create(sequence_line.number_line))
        self.wait()
        self.play(GrowFromCenter(sequence_line.sequence_dots[1]))
        self.wait()
        dropoff_text = 5
        dropoff_dots = 50
        for i in range(2, dropoff_text + 1):
            anims = [
                GrowFromCenter(sequence_line.sequence_dots[i]),
                FadeIn(sequence_line.sequence_texts[i]),
            ]
            if i > 1:
                anims.append(FadeOut(sequence_line.sequence_texts[i - 1]))
            self.play(*anims)
            self.wait()
        self.play(FadeOut(sequence_line.sequence_texts[dropoff_text]))
        self.play(
            LaggedStart(
                *[
                    GrowFromCenter(sequence_line.sequence_dots[i])
                    for i in range(dropoff_text + 1, dropoff_dots + 1)
                ],
                lag_ratio=0.25,
                run_time=2,
            )
        )
        self.add(*sequence_line.sequence_dots.values())
        self.wait()
        self.play(GrowFromCenter(sequence_line.converges_dot))
        self.wait()
        sequence_line.epsilon.set_value(0.1)
        self.play(
            Create(sequence_line.interval), Write(sequence_line.epsilon_text)
        )
        self.wait()
        sequence_line.epsilon_changes_color = True
        self.play(Write(sequence_line.N_label))
        self.wait()
        self.play(sequence_line.epsilon.animate.set_value(0.01))
        self.wait()
        self.play(sequence_line.epsilon.animate.set_value(0.001))
        self.wait()
        self.play(sequence_line.value_scaling.animate.set_value(50))
        self.wait()
        self.play(sequence_line.epsilon.animate.set_value(0.0001))
        self.wait()
        self.play(sequence_line.value_scaling.animate.set_value(500))
        self.wait()
