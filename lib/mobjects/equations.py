from manim import *


class Equations(VGroup):
    def __init__(
        self,
        *args,
        # I don't know how to properly type this in python and I can't be
        # bothered to make it work, so I'll document the types here.
        # { mode: "tex", tex: str, target: int } |
        # { mode: "index", anchor_func: Callable[[int], int], target: int } |
        # { mode: "none" }
        align_opts={"mode": "tex", "tex": "=", "target": 0},
        **kwargs,
    ):
        self.align_opts = align_opts
        super().__init__(*args, **kwargs)
        self._align_eqs()

    def _align_eqs_by_tex(self):
        if len(self) == 0:
            return

        target_index = self.align_opts["target"]
        tex_aligner = self.align_opts["tex"]
        anchor = self[target_index].get_part_by_tex(tex_aligner).get_x()
        for i in range(len(self)):
            if i == target_index:
                continue

            eq = self[i]
            eq_anchor = eq.get_part_by_tex(tex_aligner).get_x()

            offset = eq_anchor - anchor
            eq.shift(LEFT * offset)


    def _align_eqs(self):
        self.arrange(DOWN)

        mode = self.align_opts["mode"]
        if mode == "tex":
            self._align_eqs_by_tex()
        elif mode == "none":
            pass
        else:
            raise NotImplementedError

    def add_equation(self, equation: MathTex, index=None):
        index = index if index is not None else len(self)
        self.insert(index, equation)
        self._align_eqs()
        return self

    @override_animate(add_equation)
    def _add_equation_animation(self, equation: MathTex, anim_args={}):
        equation.set_opacity(0)
        self.add(equation)

        target = self.generate_target()
        target._align_eqs()
        target.set_opacity(1)

        # Start the equation where it should be so it "fades in"
        equation.move_to(target[-1])

        return MoveToTarget(self, **anim_args)

    def change_equation(self, equation: MathTex, index=-1):
        old = self[index]
        self.insert(index, equation)
        self.remove(old)
        self._align_eqs()
        return self

    @override_animate(change_equation)
    def _change_equation_animate(self, equation: MathTex, index=-1, anim_args={}):
        target = self.generate_target()
        old = target[index]
        target.insert(index, equation)
        target.remove(old)
        target._align_eqs()
        return MoveToTarget(self, **anim_args)

    def remove_equation_by_index(self, index):
        self.remove(self[index])
        self._align_eqs()
        return self



class EquationsTest(Scene):
    def construct(self):
        eqs = Equations(MathTex(r"0.99\ldots", "=", "x"))
        self.add(eqs)
        self.wait()
        self.play(
            eqs.animate.add_equation(
                MathTex(r"10\cdot", r"0.99\ldots", "=", "10", "x")
            )
        )
        self.wait()
        self.play(
            eqs.animate.change_equation(MathTex(r"9.99\ldots", "=", "10x"))
        )
        self.wait()
        self.play(
            eqs.animate.change_equation(
                MathTex(r"9.99\ldots", r"-0.99\ldots", "=", "10x", "-", "x")
            )
        )
        self.wait()
