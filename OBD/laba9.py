"""
    Визначити специфікації класів для будівника дерева розбору складного виразу(у відповідності до БНФ) на основі його
    символьного подання: <вираз>::=<простий вираз> | <складний вираз>
                         <простий вираз>::=<константа> | <змінна>
                         <константа>::=(<число>)
                         <змінна>::=(<ім'я>)
                         <складний вираз>::=(<вираз><знак операції><вираз>)
                         <знак операції>::=+|-|*|/
    Pattern: Builder

    class Builder
    class ParseExpression
    class ParsedProduct
    class Director
    class BNF
"""

from abc import ABC, abstractmethod
import re


class Builder(ABC):
    """
        Interface Builder
        Defines creating methods for different objects parts Product
    """

    @property
    def product(self) -> None:
        return None

    @abstractmethod
    def tokenize(self, data):
        pass

    @abstractmethod
    def redirect_tokens(self, var, tokens):
        pass


class ParsedProduct:
    """
        class ParsedProduct
        Container for parsed expression parts
    """

    def __init__(self) -> None:
        self.parts = []

    def __getitem__(self, index):
        return self.parts[index]

    def add(self, part) -> None:
        self.parts.append(part)

    def get_parts(self):
        return self.parts


class ParseExpression(Builder):
    """
        Concrete class Builder
        Defines methods of creating/building by step
    """

    t_c = "const"
    t_v = "variable"
    t_s_exp = "simple expression"
    t_c_exp = "compound expression"

    def __init__(self) -> None:
        """
            Initially contains empty instance ParsedProduct
        """
        self._product = ParsedProduct()
        self.p_tokenize1 = re.compile(r"(\w+)\s*=\s*(.+)")
        self.p_tokenize2 = re.compile(r"[\w+-\/*\"]+")

    def reset(self) -> None:
        self._product = ParsedProduct()

    @property
    def product(self) -> ParsedProduct:
        product = self._product
        self.reset()
        return product

    def tokenize(self, data):
        self._data = data
        res = re.search(self.p_tokenize1, data)
        if res:
            right = res.group(1)
            left = res.group(2)
            self.redirect_tokens(right, re.findall(self.p_tokenize2, left))
        else:
            self._product.add({self._data: None})
        del self._data

        return self._product[-1]

    def redirect_tokens(self, var: str, tokens: list) -> None:
        """
            Method redirect_tokens
            Defines type of expression string and log it in self_product by add method
        """
        if not var[0].isalpha():
            self._product.add({self._data: None})
            return

        parsed_exp = {}
        lentk = len(tokens)
        if lentk == 1:
            tokens = tokens[0]
            if tokens.startswith('"') and tokens.endswith('"'):
                parsed_exp[self._data] = self.t_v  # variable
            elif tokens.isdigit():
                parsed_exp[self._data] = self.t_c  # const
            elif tokens[0].isalpha():
                parsed_exp[self._data] = self.t_s_exp  # simple expression
            else:
                parsed_exp[self._data] = None
        elif lentk == 3:
            var1, op, var2 = tokens
            if (var1.isdigit() or var1[0].isalpha()) and (var2.isdigit() or var2[0].isalpha()) and op in '*+/-':
                parsed_exp[self._data] = self.t_c_exp  # compound expression
        else:
            parsed_exp[self._data] = None

        self._product.add(parsed_exp)


class Director:

    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
            object Director works with any Builder instance, given by Client
            :param builder: instance of class Builder
        """
        self._builder = builder

    """
        Director can build several variations of Product, using same steps    
    """

    def build_parsed_data(self, data):
        return self.builder.tokenize(data)


class BNF:
    """
        Class BNF
        Provides with user interface for parsing
        Runs Director and has concrete Builder instance
    """

    def __init__(self):
        self.director = Director()
        self.builder = ParseExpression()
        self.director.builder = self.builder

    def showAll(self):
        self.cache_parts = self.director.builder.product.get_parts()
        for i in self.cache_parts:
            print(i)

    def parse(self, expression):
        return self.director.build_parsed_data(expression)


def main():
    bnf = BNF()

    tests = [
             'c = "hello"',
             'a = 10',
             'q = a',
             'q = c',
             'c = d + d'
        ]
    for t in tests:
        print(bnf.parse(t))

    print("\n----------   Product will be deleted after showing all   ----------\n")
    bnf.showAll()
    bnf.showAll()


if __name__ == '__main__':
    main()
