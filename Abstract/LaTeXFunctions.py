def convert_res_to_latex(res):
    return r"\{" + "".join([e + ", " for e in res])[:-2] + r"\}"


def set_tex(s):
    if isinstance(s[0], list):
        return r'\{' + ', '.join([set_tex(i) for i in s]) + r'\}'
    else:
        return r'\{' + ', '.join(s) + r'\}'


def formatted_rows(finalrows, groups):
    s = ""
    for i in range(len(finalrows)):
        s += groups[i // 2].__str__() + ' & ' + ' & '.join([convert_res_to_latex(res) for res in finalrows[i]]) + " \\\\\n"
    return s


def formatted_cols(finalcols, elem):
    s = ""
    for i in range(len(finalcols[0])):
        line = []
        for j in range(len(finalcols)):
            res = finalcols[j][i]
            line.append(convert_res_to_latex(res))
        s += elem[i] + " & " + " & ".join(line) + " \\\\\n"
    return s


# returns the contents the subscript following the prefix at i,
# None if there is no subscript
def get_subscript(raw, i):
    if len(raw) > 2 + i and raw[i + 1] == '_':
        sub = get_enclosed(raw, i + 2)
        return sub[1:-1] if len(sub) > 1 else sub

    return None


# returns the contents the subscript following the prefix at i,
# None if there is no subscript
def get_superscript(raw, i):
    if len(raw) > 2 + i and raw[i + 1] == '^':
        sub = get_enclosed(raw, i + 2)
        return sub[1:-1] if len(sub) > 1 else sub

    return None


def get_enclosed(raw, i):
    prefix_ops, postfix_ops = {'{', '[', '('}, {'}', ']', ')'}
    n = i
    if raw[i] not in prefix_ops:
        return raw[i]

    # update accumulator
    s = raw[i]

    # for each character after '{' while haven't seen closing '}'
    i += 1
    while i < len(raw):
        c = raw[i]

        if c in prefix_ops:
            inner = get_enclosed(raw, i)
            s += inner
            i += len(inner)
        else:
            s += c
            i += 1

        if c in postfix_ops:
            return s
    raise AttributeError("Unclosed delimiter: " + raw[n])


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

        # fetch superscript (None if no superscript)
        sup = get_superscript(raw, i)

        if sup is not None:
            if raw[i + 2] == '{':
                s += '^{' + sup + '}'
                i += 3 + len(sup)
            else:
                s += '^' + sup
                i += 1 + len(sup)

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


class TeX(str):
    def __init__(self, raw):
        super().__init__()
        self.raw = raw
        self.base = str()
        i = 0
        while i < len(raw):
            if raw[i] in ['^', '_']:
                i -= 1
                break
            self.base += raw[i]
            i += 1

        sub = get_subscript(raw, i)

        if sub is not None:
            if raw[i + 2] == '{':
                i += 3 + len(sub)
            else:
                i += 1 + len(sub)
            self.subscript = TeX(sub)

        # fetch superscript (None if no superscript)
        sup = get_superscript(raw, i)

        if sup is not None:
            if raw[i + 2] == '{':
                i += 3 + len(sup)
            else:
                i += 1 + len(sup)
            self.superscript = TeX(sup)
        else:
            self.superscript = None

        # fetch subscript (None if no subscript)
        if sub is not None:
            return

        sub = get_subscript(raw, i)

        if sub is not None:
            if raw[i + 2] == '{':
                i += 3 + len(sub)
            else:
                i += 1 + len(sub)
            self.subscript = TeX(sub)
        else:
            self.subscript = None


print(TeX("b^{b_{45}}_{x}").superscript)

