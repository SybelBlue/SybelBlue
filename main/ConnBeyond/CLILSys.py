from colorsys import hls_to_rgb
from turtle import Screen
from functools import reduce
from turtle import Turtle, Terminator
from tkinter import TclError

instructions = """

Basic Syntax Rules
--------------------

Symbols must be capital letter or digit. 

Symbols may be followed by subscript in LaTeX notation (X_{subscript}).

Subscripts may be any string of characters.

Multiple rules can be generated with a '|' on the right.
i.e.
A → AA | B
is equivalent to 
A → AA
A → B

Whitespace is ignored.

LaTeX syntax is always acceptable.

Multiple variables may be put on either side of the arrow.

Using the format X < R > Y → S will replace only the R with S. Both < and > must be used for this syntax.

Special curves are pre-programmed. Type the name to run
Basic Signal
Cantor
Dragon Curve
Hilbert
Koch
Koch Island
Peano
Peano-Gosper
Sierpinski
Sierpinski Arrowhead

Utilizing the Turtle Function
-------------------------------

Variables bound to Turtle Actions:
F_{l}: move forward length l
R_{d}/L_{d}: turn right/left d degrees
P_u/P_d: put pen up/down
M_{...}: perform the module of actions ... in order

Not using subscript uses default values:
F: move forward 10
R/+: turn right 90 degrees
L/-: turn left 90 degrees
P: put pen down

Leading or trailing n in subscript scales with recursive depth
F_{10n}: move forward 10 times the recursive depth of this F

# in subscript allows for tagged variables
F_{1}: move forward one
F_{#1}/F_{#abadhas}: move forward default length, but unique variables
F_{10/n #2}/F_{10/n #1}: move 10 divided by the recursive depth forward, but unique variables


Example L-Systems
-------------------

Basic Signal
S -> BAAAAAAAA
BA -> AB

Koch
F → F L F R F R F L F
F -> F L_{60} F R_{60} R_{60} F L_{60} F

Sierpinski
S → F L_{120} F_{#2} L_{120} F_{#2}
F → F L_{120} F_{#2} R_{120} F R_{120} F_{#2} L_{120} F
F_{#2} → F_{#2} F_{#2}

Sierpinski Arrowhead
F_{20/n} → F_{20/n #2} L_{60} F_{20/n} L_{60} F_{20/n #2}
F_{20/n #2} → F_{20/n} R_{60} F_{20/n #2} R_{60} F_{20/n}

Dragon Curve
S → F X
X → X R Y F R
Y → L F X L Y

Inspiration from http://mathforum.org/advanced/robertd/lsys2d.html
"""


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

    # generates a dict of the rules in standard CFG format
    def generate_grammar(self):
        grammar = {}

        for left, right in self.rules:
            if left in grammar:
                grammar[left] += " | " + right
            else:
                grammar[left] = right

        return grammar

    # returns the evaluated L-system after n recursions
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
            rule_match_found = False

            for left, right in self.rules:

                if rule_matches(symbols, left, i):
                    new_s += right
                    rule_match_found = True
                    i += len(left)
                    break

            if rule_match_found:
                continue

            new_s += symbols[i]  # symbols[i] is a terminal
            i += 1

        return self.yields_from(n - 1, new_s)

    # runs the turtle on the command string self.yield(n),
    # with instant animation if instant, and without
    # printing to console if quiet
    def run_turtle(self, n, instant, quiet=True):
        if n < 0:
            return

        cmd_str = self.yields(n)

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

        if not quiet:
            print("If you navigate away during computation, hit Ctrl+C once to resume.")
            print("Command String: \n" + cmd_str)
            print(":End of Command String")
            print("If you navigate away and computation pauses, hit Ctrl+C once to resume.")

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


# maps raw string input to interpreter accepted values
raw_to_Interpreter = [
    (r"\\", ""),
    ("\ ", " "),
    (" ", ""),
    ("&", ""),
    (r"\rightarrow", "->"),
    (r"\Rightarrow", "->"),
    ("->", "→"),
    ("-", "L"),
    ("+", "R"),
    (r"\mid", "|")
]

# maps special program names to the grammar input for ease of use
Special_Programs = [
    ("Cantor", """M_{P_dFP_u} -> M_{P_dFP_u}FM_{P_dFP_u}\nF -> FFF"""),
    ("Basic Signal", """S -> BAAAAAAAA\nBA -> AB\nA -> A"""),
    ("Dragon", """S → F X\nX → X R Y F R\nY → L F X L Y"""),
    ("Hilbert", """X -> XF_{30/n}YF_{30/n}X+F_{30/n}+YF_{30/n}XF_{30/n}Y-F_{30/n}-XF_{30/n}YF_{30/n}X\n""" +
     """Y -> YF_{30/n}XF_{30/n}Y-F_{30/n}-XF_{30/n}YF_{30/n}X+F_{30/n}+YF_{30/n}XF_{30/n}Y"""),
    ("Koch", """F → F L F R F R F L F"""),
    ("Koch Island", """F -> F-F+F+FFF-F-F+F"""),
    ("Peano", "F -> F+F-F-F-F+F+F+F-F"),
    ("Peano-Gosper", """X -> X+_{60}YF+_{60}+_{60}YF-_{60}FX-_{60}-_{60}FXFX-_{60}YF+_{60}\n""" +
     """Y -> -_{60}FX+_{60}YFYF+_{60}+_{60}YF+_{60}FX-_{60}-_{60}FX-_{60}Y"""),
    ("Sierpinski", """S→FL_{120}F_{#}L_{120}F_{#}\nF→FL_{120}F_{#}R_{120}FR_{120}F_{#}L_{120}F\nF_{#}→F_{#}F_{#}"""),
    ("Sierpinski Arrowhead", """F → F_{#2} L_{60} F L_{60} F_{#2}\nF_{#2} → F R_{60} F_{#2} R_{60} F""")
]


# makes raw text ready for parsing
def process_raw(raw):
    for symbol, lang in raw_to_Interpreter:
        raw = raw.replace(symbol, lang)

    return raw


# returns a list of rules generated by a line of text
def parse_line(line):
    if not len(line):
        return []

    # make suitable for processing
    line = process_raw(line)

    arrow_index = line.index('→')

    # everything left of the arrow
    left = split_symbols(line[:arrow_index])

    # everything right of the arrow
    right = line[arrow_index + 1:].split("|")

    # correct for explicit context-sensitive grammar notation
    if "<" in left and ">" in left:
        a, b = left.index('<'), left.index(">")
        x, r, y = left[:a], left[a + 1:b], left[b + 1:]

        left = x + r + y
        x_str = "".join(x)
        y_str = "".join(y)
        right = [x_str + s + y_str for s in right]

    return [(left, x) for x in right]


# returns a list of rules generated by multi-line text
def create_rules(raw):
    if not len(raw):
        return []

    # sort programs to avoid recognizing part of a name
    programs = sorted(Special_Programs, key=lambda x: len(x[0]), reverse=True)
    for name, program in programs:
        raw = raw.replace(name, program)

    list_of_rule_lists = [parse_line(line) for line in raw.splitlines()]

    return reduce(lambda x, y: x + y, list_of_rule_lists)


# returns the alphabet of variables the rule_list operates over
def sigma(rule_list):
    variables = set()

    # gather all variables on the left-hand side
    for left, _ in rule_list:
        for x in left:
            variables.add(x)

    # for all right-hand sides, get every symbol if uppercase or starting with digit
    for _, right in rule_list:
        for symbol in split_symbols(right):
            if symbol[0].isupper() or symbol[0].isdigit():
                variables.add(symbol)

    return variables


# breaks a line into an ordered list of variables and terminals
def split_symbols(raw):
    out = []

    # for each letter in raw
    i = 0
    while i < len(raw):
        # initialize accumulator string
        s = raw[i]

        # fetch subscript (None if no subscript)
        sub = get_subscript(raw, i)

        if sub is not None:
            if raw[i + 2] == '{':
                s += '_{' + sub + '}'
                i += 3 + len(sub)
            else:
                s += '_' + sub
                i += 1 + len(sub)

        # add the final accumulation
        out.append(s)

        i += 1

    return out


# returns the contents of items between brackets, including the brackets
# starting with the bracket at i
def get_enclosed(raw, i):
    prefix_ops, postfix_ops = {'{', '[', '('}, {'}', ']', ')'}

    if raw[i] not in prefix_ops:
        return raw[i]

    # update accumulator
    s = raw[i]

    # for each character after '{' while haven't seen closing '}'
    i += 1
    while True:
        c = raw[i]

        # if a new enclosure begins, recurse...
        if c in prefix_ops:
            inner = get_enclosed(raw, i)
            s += inner
            i += len(inner)
        # otherwise add the character to the string
        else:
            s += c
            i += 1

        # if it is a closing character, break the loop
        if c in postfix_ops:
            return s


# returns the contents the subscript following the prefix at i,
# None if there is no subscript
def get_subscript(raw, i):
    if len(raw) > 2 + i and raw[i + 1] == '_':
        sub = get_enclosed(raw, i + 2)
        return sub[1:-1] if len(sub) > 1 else sub

    return None


# Applies the text form of a single action symbol to a turtle at n where
# n is the depth of the command in the production recursion
def apply_cmd(cmd: str, turtle: Turtle, n):
    sub = get_subscript(cmd, 0)

    sub, use_sub = parse_subscript(sub, n)

    # apply the proper command, recurse if module command
    if cmd[0] == 'F':
        turtle.forward(10 if not use_sub else float(sub))
    elif cmd[0] == 'R':
        turtle.right(90 if not use_sub else float(sub))
    elif cmd[0] == 'L':
        turtle.left(90 if not use_sub else float(sub))
    elif cmd[0] == 'P':
        if 'u' in sub:
            turtle.penup()
        else:
            turtle.pendown()
    elif cmd[0] == 'M':
        for M_command in split_symbols(sub):
            apply_cmd(M_command, turtle, n)


# returns a tuple containing the parsed subscript and use_sub value
def parse_subscript(sub, n):
    # if sub is None, ignore it
    if sub is None:
        return sub, False

    # Cut out everything after # sign
    if '#' in sub:
        sub = sub[:min(sub.index('#'), len(sub))]

    # if there is no longer a subscript, ignore it
    if not len(sub):
        return sub, False

    # if there is a subscript that contains a depth factor...
    if "n" in sub:
        # replace n with the evaluated expression
        if '/' in sub:
            neg_exp = sub.index('n') > sub.index('/')
            sub = sub.replace("n", "")
            sub = sub.replace('/', '')
            sub = str(float(sub) / n if neg_exp else n / float(sub))
        else:
            sub = sub.replace("n", "")
            sub = sub.replace('*', '')
            sub = str(float(sub) * n)

    # return final version of subscript, and use it
    return sub, True


# determines whether the left side matches the string of symbols starting at i
def rule_matches(symbols, left, i):
    if len(symbols) <= i + len(left) - 1:
        return False

    return all([left[j] == symbols[i + j] for j in range(len(left))])


if __name__ == '__main__':
    print("Type 'help' for more instructions.")
    print("Enter a fractal name or any L-System Production rule set, starting with the start variable: ")

    # gather an arbitrary number of lines until something followed by empty line is read
    lines = ""
    while not len(lines):
        lines = '\n'.join(iter(input, ""))

        if 'help' in lines:
            print(instructions)
            print("Enter a fractal name or any L-System Production rule set, starting with the start variable: ")
            lines = ""

    l_system = LSystem(lines)
    print("Generated L-System: ")
    print(l_system)
    print()

    try:
        # if the L-system alphabet has any turtle commands...
        if any([x in l_system.sigma for x in ['F', 'R', 'L', 'P']]):
            depth = input("Production Depth (add * to skip render animation): ")

            instant = '*' in depth

            depth = depth.replace('*', '')

            depth = int(depth)

            l_system.run_turtle(depth, instant, quiet=False)
        else:
            depth = int(input("Production Depth: "))

            print("Generated String: " + l_system.yields(depth))

            print("<Not Formatted For Turtle Commands>")
    except Terminator:
        print()
        print("------------------")
        print("Turtle execution interrupted")
    except TclError:
        print()
        print("------------------")
        print("Turtle execution interrupted in Tcl")
