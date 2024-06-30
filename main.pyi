from typing import Dict, Union, Optional, List


class Operator:
    rec: str
    level: int

    def __init__(self, rec: str, level: int) -> None: ...

    @staticmethod
    def opr_analyser(item: str) -> Operator: ...

    def connect(self, one: DgOrCl, ano: DgOrCl) -> Calculator: ...

    def __repr__(self) -> str: ...

    def __call__(self, one: DgOrCl, ano: DgOrCl) -> Union[Calculator, Digit]: ...

    def __eq__(self, other: DgOrOp) -> bool: ...

    def __gt__(self, other: DgOrOp) -> bool: ...

    def __ge__(self, other: DgOrOp) -> bool: ...

    def __le__(self, other: DgOrOp) -> bool: ...

    def __lt__(self, other: DgOrOp) -> bool: ...

    def __str__(self) -> str: ...


class OPTS:
    add: Operator
    sub: Operator
    mul: Operator
    div: Operator
    none: Operator
    lower_none: Operator

    __all__: List[Operator]


class CalculateResult:
    gl_res: Dict[Calculator, Digit]

    @classmethod
    def store(cls, sentence: Calculator, result: Digit) -> Digit: ...

    @classmethod
    def get(cls, sentence: Calculator) -> Optional[Digit]: ...


class Calculator:
    one: DgOrCl
    opr: Optional[Operator]
    ano: Optional[DgOrCl]

    def __init__(
            self,
            one: DgOrCl,
            opr: Optional[Operator] = None,
            ano: Optional[DgOrCl] = None
    ) -> None: ...

    @staticmethod
    def __sen_analyser(
            sentence: str,
            start: int,
            end: int,
            quotes_map: Dict[int, int]
    ) -> Calculator: ...

    @staticmethod
    def __replace_quotes(sentence: str) -> str: ...

    @staticmethod
    def match_quotes(sentence: str) -> Dict[int, int]: ...

    @staticmethod
    def sentence_analyser(sentence: str) -> Calculator: ...

    def __add__(self, other: DgOrCl) -> Calculator: ...

    def __radd__(self, other: DgOrCl) -> Calculator: ...

    def __sub__(self, other: DgOrCl) -> Calculator: ...

    def __rsub__(self, other: DgOrCl) -> Calculator: ...

    def __truediv__(self, other: DgOrCl) -> Calculator: ...

    def __rtruediv__(self, other: DgOrCl) -> Calculator: ...

    def __mul__(self, other: DgOrCl) -> Calculator: ...

    def __rmul__(self, other: DgOrCl) -> Calculator: ...

    @property
    def result(self) -> Digit: ...

    def __str__(self) -> str: ...


Digit = Union[int, float]
DgOrCl = Union[Digit, Calculator]
DgOrOp = Union[Digit, Operator]


def calculate(one: DgOrCl, opr: Operator, ano: DgOrCl) -> Digit: ...
