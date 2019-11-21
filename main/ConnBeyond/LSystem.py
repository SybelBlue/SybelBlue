from colorsys import hls_to_rgb
from turtle import Turtle, Screen
from main.ConnBeyond.LSystemParser import create_rules, sigma, split_symbols, apply_cmd, rule_matches


# a class that allows an instance of an L-system to be generated
class LSystem:

    # alphabet of LSystem
    sigma = []
    # start variable
    start = None
    # rule set
    rules = []

    def __init__(self, raw):
        self.rules = create_rules(raw)
        self.sigma = sigma(self.rules)
        self.start = self.rules[0][0][0]

        self.generate_terminators()

    # generates any missing terminator variable rules
    def generate_terminators(self):
        for v in self.sigma:
            if not any(left == [v] for left, _ in self.rules):
                t = [v], v
                self.rules.append(t)

    # returns the evaluated L-system after n recursions from start
    def yields(self, n):
        return self.yields_from(n, self.start)

    # returns the evaluated L-system after n recursions from a start string
    def yields_from(self, n, start):
        if n <= 0:
            return start

        new_s = ""
        symbols = split_symbols(start)
        i = 0
        while i < len(symbols):
            for left, right in self.rules:
                if rule_matches(symbols, left, i):
                    new_s += right
                    i += len(left)
                    break

        return self.yields_from(n - 1, new_s)

    # runs the turtle on the command string self.yield(n),
    # with instant animation if instant, and without
    # printing to console if quiet
    def run_turtle(self, n, instant=False, quiet=True):
        if n < 0:
            return

        cmd_str = self.yields(n)

        if not quiet:
            print("Command String: ")
            print(cmd_str)

        win = Screen()

        left, bottom, right, top = -10, -10, 10, 10
        last = (left, bottom, right, top)
        margin = 20

        win.setworldcoordinates(left, bottom, right, top)

        t = Turtle()

        t.speed(10)

        if not instant and not quiet:
            t.shape('turtle')

        win.tracer(0, 0)

        symbols = split_symbols(cmd_str)

        cmd_len = len(symbols)

        last_mark = -0.1

        if cmd_len > 200000 and not quiet:
            print("Render Progress: ", end="", flush=True)

        # for each symbol in the command string, apply to t
        for i in range(len(symbols)):
            progress = i / (float(cmd_len))
            t.color(hls_to_rgb(progress, 0.5, 0.5))
            apply_cmd(symbols[i], t, n)

            left, bottom = min(left, t.pos()[0] - margin), min(bottom, t.pos()[1] - margin)
            right, top = max(right, t.pos()[0] + margin), max(top, t.pos()[1] + margin)

            animate = not last == (left, bottom, right, top) or cmd_len < 7500

            if not instant and animate:
                win.setworldcoordinates(left, bottom, right, top)
                last = left, bottom, right, top

            if cmd_len > 200000 and progress - last_mark >= 0.1 and not quiet:
                print(str(100 * progress)[:4] + "%... ", end="", flush=True)
                last_mark = progress

        if not quiet:
            print("Render Complete.")

        win.setworldcoordinates(left, bottom, right, top)

        win.update()

        win.exitonclick()

    def __str__(self):
        return (self.sigma, self.start, self.rules).__str__()
