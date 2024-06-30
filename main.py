from typing import Union, List

Digit = Union[int, float]


class Operator:
    def __init__(self, rec, level):
        self.rec = rec
        self.level = level

    @staticmethod
    def opr_analyser(item):
        for t in OPTS.__all__:
            if item == t.rec: return t
        return OPTS.none

    def connect(self, one, ano):
        return Calculator(one, self, ano)

    def __call__(self, one, ano):
        return calculate(one, self, ano)

    def __eq__(self, other):
        if isinstance(other, str):
            opr = Operator.opr_analyser(other)
            return self.__eq__(opr)
        return other.level == self.level

    def __gt__(self, other):
        if isinstance(other, str):
            opr = Operator.opr_analyser(other)
            return self.__gt__(opr)
        return self.level > other.level

    def __ge__(self, other):
        if isinstance(other, str):
            opr = Operator.opr_analyser(other)
            return self.__ge__(opr)
        return self.level >= other.level

    def __le__(self, other):
        if isinstance(other, str):
            opr = Operator.opr_analyser(other)
            return self.__le__(opr)
        return self.level <= other.level

    def __lt__(self, other):
        if isinstance(other, str):
            opr = Operator.opr_analyser(other)
            return self.__lt__(opr)
        return self.level < other.level

    def __str__(self):
        return self.rec

    def __repr__(self):
        return f"Operator.{self.rec}"


class OPTS:
    add = Operator('+', 1)
    sub = Operator('-', 1)
    mul = Operator('*', 2)
    div = Operator('/', 2)
    none = Operator('', 999)
    lower_none = Operator('', 0)

    __all__ = [add, sub, mul, div]


class CalculateResult:
    gl_res = dict()

    @classmethod
    def store(cls, sentence, result):
        cls.gl_res[sentence] = result
        return result

    @classmethod
    def get(cls, sentence):
        return cls.gl_res.get(sentence, None)


class Calculator:
    def __init__(self, one, opr=OPTS.none, ano=None):
        self.one = one
        self.opr = opr
        self.ano = ano

    @staticmethod
    def __sen_analyser(sentence, start, end, quotes_map):
        digit_stack: List[Calculator] = []
        opr_stack: List[Operator] = [OPTS.lower_none]

        def re_push_calculate():
            nonlocal digit_stack, opr_stack
            right = digit_stack.pop()
            left = digit_stack.pop()
            cal_opr = opr_stack.pop()
            digit_stack.append(cal_opr.connect(left, right))

        idx = start
        while idx < end:
            item = sentence[idx]
            if item in OPTS.__all__:
                opr = Operator.opr_analyser(item)
                if opr <= opr_stack[-1]: re_push_calculate()
                opr_stack.append(opr)

            elif item.isdigit():
                digit_stack.append(eval(item))

            elif item == '(':
                right_idx = quotes_map[idx]
                digit_stack.append(
                    Calculator.__sen_analyser(
                        sentence,
                        idx + 1, right_idx,
                        quotes_map
                    )
                )
                idx = right_idx + 1
            idx += 1

        while len(opr_stack) > 1: re_push_calculate()

        return digit_stack[0]

    @staticmethod
    def __replace_quotes(sentence):
        rep_d = {
            '[': '(', '{': '(',
            ']': ')', '}': ')'
        }

        for rep, tar in rep_d.items():
            while rep in sentence:
                sentence = sentence.replace(rep, tar)
        return sentence

    @staticmethod
    def match_quotes(sentence):
        quotes = {}
        quotes_stack = []
        for idx, item in enumerate(sentence):
            if item == '(':
                quotes_stack.append(idx)
            elif item == ')':
                quotes[quotes_stack.pop()] = idx
        return quotes

    @staticmethod
    def sentence_analyser(sentence):
        sentence = Calculator.__replace_quotes(sentence)

        return Calculator.__sen_analyser(
            sentence,
            0, len(sentence),
            Calculator.match_quotes(sentence)
        )

    def __repr__(self):
        return f"{self.one} {self.opr} {self.ano}"

    def __add__(self, other):
        return Calculator(self, OPTS.add, other)

    def __radd__(self, other):
        return Calculator(other, OPTS.add, self)

    def __sub__(self, other):
        return Calculator(self, OPTS.sub, other)

    def __rsub__(self, other):
        return Calculator(other, OPTS.sub, self)

    def __truediv__(self, other):
        return Calculator(self, OPTS.div, other)

    def __rtruediv__(self, other):
        return Calculator(other, OPTS.div, self)

    def __mul__(self, other):
        return Calculator(self, OPTS.mul, other)

    def __rmul__(self, other):
        return Calculator(self, OPTS.mul, other)

    @property
    def result(self):
        if self.opr is None: return self.one
        if res := CalculateResult.get(self): return res

        return CalculateResult.store(
            self,
            calculate(self.one, self.opr, self.ano)
        )

    def __str__(self):
        if self.opr is OPTS.none: return str(self.one)

        one = str(self.one)
        if isinstance(self.one, Calculator) and self.opr > self.one.opr:
            one = '(' + one + ')'

        ano = str(self.ano)
        if isinstance(self.ano, Calculator) and self.opr > self.ano.opr:
            ano = '(' + ano + ')'

        return f"{one} {self.opr} {ano}"


def calculate(one, opr, ano):
    if opr is OPTS.none: return one
    while isinstance(one, Calculator): one = one.result
    while isinstance(ano, Calculator): ano = ano.result

    if opr is OPTS.add:
        return one + ano
    elif opr is OPTS.sub:
        return one - ano
    elif opr is OPTS.div:
        return one / ano
    elif opr is OPTS.mul:
        return one * ano
    else:
        assert False, '未实现语法'


def main():
    # one = Calculator(1)
    # sentence = 6 / (2 + one) * (4 + 2) / 2

    sentence = Calculator.sentence_analyser(
        "6 / [(2 + 1) * (6 - 2) - 2] / 2"
    )

    print(sentence)
    print(sentence.result)

    # print(CalculateResult.gl_res)


if __name__ == '__main__':
    main()
