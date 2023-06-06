from manim import *


class ComposeAnimations(Animation):
    def __init__(
        self,
        *args,
        # (1, dir1), (0.5, dir2), run_time=1 will normally produce an animation
        # of duration 1. If this is true, then animation will be 1 + 0.5
        # duration, effectively overriding run_time
        run_time_match_weights=False,
        **kwargs,
    ):
        self.run_time_match_weights = run_time_match_weights
        # List of weights and interpolations of animations from 0 to 1
        # If weight is 0, animation will "instantly" play
        # If weight is negative, animation will simply not be added
        self.directives: list[
            tuple[float, Callable[[Animation, float], None]]
        ] = []
        super().__init__(*args, **kwargs)
        self._build()

    def add_directives(self, *directives):
        self.directives.extend(
            [directive for directive in directives if directive[0] >= 0]
        )
        self._build()
        return self

    def match_run_time_with_weights(self):
        self.set_run_time(sum(self.unnormalized_weights))

    def _build(self):
        self.unnormalized_weights = [
            directive[0] for directive in self.directives
        ]
        total_weights = sum(directive[0] for directive in self.directives)
        self.normalized_weights = [
            weight / total_weights for weight in self.unnormalized_weights
        ]
        self.partial_weights = [
            sum(self.normalized_weights[:i])
            for i in range(len(self.normalized_weights))
        ]
        if self.run_time_match_weights:
            self.set_run_time(sum(self.unnormalized_weights))

    def interpolate_mobject(self, alpha: float):
        for i in range(len(self.partial_weights)):
            if (
                i < len(self.partial_weights) - 1
                and alpha > self.partial_weights[i + 1]
            ):
                self.directives[i][1](self, 1)
            else:
                directive_rt = min(
                    (
                        (alpha - self.partial_weights[i])
                        / self.normalized_weights[i]
                        if self.normalized_weights[i] > 0
                        else 1
                    ),
                    1,
                )
                self.directives[i][1](self, directive_rt)
                break
