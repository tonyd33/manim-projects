from manim import *


class Clock(VGroup):
    def __init__(
        self,
        *args,
        radius=2,
        color=WHITE,
        font_size_scale=0.5,
        hour=12,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.hour = hour % 12
        self.hours: dict[int, MathTex] = {}
        self.circle = Circle(radius=radius, color=color)
        self.clock_hand = Arrow(
            start=self.circle.get_center(),
            end=self.get_center() + UP * radius * 0.5,
            buff=0,
            max_tip_length_to_length_ratio=0.2,
        ).rotate(
            -TAU * (hour % 12) / 12, about_point=self.circle.get_center()
        )

        self.add(self.circle)

        inner_circle = Circle(*args, radius=radius * 0.85, **kwargs)
        for hour in [12, *range(1, 12)]:
            point_at_angle = inner_circle.point_at_angle(
                -TAU * ((hour % 12) - 3) / 12
            )
            hour_text = MathTex(
                hour,
                font_size=radius * DEFAULT_FONT_SIZE * font_size_scale,
            ).move_to(point_at_angle)
            self.hours[hour] = hour_text
            self.add(hour_text)

        self.add(Dot(radius=radius * 0.025, color=color))
        self.add(self.clock_hand)

    def to_hour(self, hour: int):
        hour_diff = (hour - self.hour) % 12
        self.clock_hand.rotate(
            -TAU * hour_diff / 12, about_point=self.circle.get_center()
        )
        self.hour = hour % 12


class ClockToHour(Animation):
    def __init__(
        self,
        clock,
        hour,
        direction="CW",
        run_time: float = 1,
        rate_func: Callable[[float], float] = linear,
        **kwargs
    ):
        self.clock = clock
        self.target_hour = hour % 12
        self.about_point = clock.clock_hand.get_start()

        direction_mult = -1 if direction=="CW" else 1
        if direction == "CW":
            hour_diff = (self.target_hour - clock.hour) % 12
        else:
            hour_diff = (clock.hour - self.target_hour) % 12

        self.angle = direction_mult * TAU * hour_diff / 12
        super().__init__(
            clock.clock_hand, run_time=run_time, rate_func=rate_func, **kwargs
        )

    def interpolate_mobject(self, alpha: float):
        self.mobject.become(self.starting_mobject)
        self.mobject.rotate(
            self.rate_func(alpha) * self.angle,
            axis=OUT,
            about_point=self.about_point,
            about_edge=None,
        )

    def clean_up_from_scene(self, scene):
        self.clock.hour = self.target_hour


class ClockTest(Scene):
    def construct(self):
        clock = Clock()
        self.add(clock)
        self.wait()
        clock.to_hour(1)
        self.wait()
        clock.to_hour(10)
        self.wait()
        self.play(ClockToHour(clock, 1))
        self.wait()
        self.play(ClockToHour(clock, 11))
        self.wait()
        self.play(ClockToHour(clock, 1, direction="CCW"))
        self.wait()
        self.play(ClockToHour(clock, 18))
        self.wait()
