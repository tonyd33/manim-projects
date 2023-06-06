from manim import *


class Calculator(VGroup):
    def __init__(
        self,
        screen_height=None,
        button_unpressed_color=BLACK,
        button_pressed_color=PURPLE,
        label_unpressed_color=WHITE,
        label_pressed_color=BLACK,
        calculator_color=BLACK,
        screen_color=BLACK,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.button_unpressed_color = button_unpressed_color
        self.button_pressed_color = button_pressed_color
        self.label_unpressed_color = label_unpressed_color
        self.label_pressed_color = label_pressed_color

        self.key_buff = 0.15

        inside_group = VGroup()
        labels = [
            r"\text{AC}",
            r"\text{C}",
            r"\text{M}-",
            r"\text{M}+",
            "7",
            "8",
            "9",
            r"\div",
            "4",
            "5",
            "6",
            r"\times",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "=",
            "+",
        ]
        self.key_labels_dict = {
            label: MathTex(
                label,
                color=self.label_unpressed_color,
                font_size=36 if "text" in label else DEFAULT_FONT_SIZE,
            )
            for label in labels
        }
        self.key_buttons_dict = {}
        key_height = max(*(key.height for key in self.key_labels_dict.values()))
        key_width = max(*(key.width for key in self.key_labels_dict.values()))

        key_buttons = []
        for label, key_label in self.key_labels_dict.items():
            group = VGroup()
            key_button_outline = RoundedRectangle(
                width=key_width + 2 * self.key_buff,
                height=key_height + 2 * self.key_buff,
                fill_color=self.button_unpressed_color,
                fill_opacity=1,
                corner_radius=0.1,
            ).move_to(key_label)
            group.add(key_button_outline, key_label)
            self.key_buttons_dict[label] = key_button_outline

            key_buttons.append(group)
            inside_group.add(group)

        inside_group.arrange_in_grid(rows=5, cols=4)
        self.screen = RoundedRectangle(
            width=inside_group.width,
            height=max(
                *(kb.height for kb in key_buttons),
                (screen_height if screen_height is not None else 0),
            ),
            fill_color=screen_color,
            fill_opacity=1,
            corner_radius=0.1,
        ).next_to(inside_group, UP)
        inside_group.add(self.screen)
        enclosure = RoundedRectangle(
            width=inside_group.width + 4 * self.key_buff,
            height=inside_group.height + 4 * self.key_buff,
            fill_color=calculator_color,
            fill_opacity=1,
            corner_radius=0.2,
        ).move_to(inside_group)
        self.add(enclosure)
        self.add(inside_group)
        self.screen_obj = None

    def move_obj_to_screen(self, obj):
        if self.screen_obj is not None:
            self.remove(self.screen_obj)

        self.screen_obj = obj
        self.add(obj)
        obj.next_to(self.screen, RIGHT).align_to(self.screen, RIGHT).shift(
            LEFT * self.key_buff
        )

    def press_button(self, button_label):
        key_label = self.key_labels_dict[button_label]
        key_outline = self.key_buttons_dict[button_label]
        key_label.set_color(self.label_pressed_color)
        key_outline.set_fill(self.button_pressed_color)

    def unpress_button(self, button_label):
        key_label = self.key_labels_dict[button_label]
        key_outline = self.key_buttons_dict[button_label]
        key_label.set_color(self.label_unpressed_color)
        key_outline.set_fill(self.button_unpressed_color)


class TapButtonCalculator(Animation):
    def __init__(
        self,
        mobject,
        button,
        run_time=0.25,
        rate_func=rate_functions.linear,
        **kwargs,
    ):
        self.button = button
        super().__init__(
            mobject, run_time=run_time, rate_func=rate_func, **kwargs
        )

    def interpolate_mobject(self, alpha: float):
        self.mobject.become(self.starting_mobject)
        if alpha < 0.5:
            self.mobject.press_button(self.button)
        else:
            self.mobject.unpress_button(self.button)


class CalculatorTest(Scene):
    def construct(self):
        calculator = Calculator()
        expr = MathTex(r"1234")
        calculator.move_obj_to_screen(expr)
        self.add(calculator, expr)
        self.wait()
        self.play(
            Succession(
                TapButtonCalculator(calculator, "1"),
                TapButtonCalculator(calculator, "2"),
                TapButtonCalculator(calculator, "3"),
                TapButtonCalculator(calculator, "4"),
                TapButtonCalculator(calculator, "="),
            )
        )
        self.wait()
