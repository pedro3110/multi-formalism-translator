from __future__ import division
from enum import Enum, unique
from pyparsing import (Suppress, CaselessKeyword, Literal, Word,
                       alphas, alphanums, quotedString, delimitedList,
                       Regex, MatchFirst, Forward, Optional, oneOf,
                       infixNotation, opAssoc, Group, ParseResults)

from py_expression_eval import Parser as PeeParser
import traceback


class Parsers(Enum):
    PY_EXPRESSION_EVAL_PARSER = 1
    XMILE_FUNCTION_PARSER = 2


class Expression(object):
    def variables(self):
        raise NotImplementedError()


class PyExpressionEvalExpression(Expression):

    def __init__(self, expression):
        self.expression = expression
        self.eq_dict = {
            'MIN': 'min',
            'MAX': 'max',
            'ABS': 'abs'
        }

    def variables(self):
        variables = self.expression.variables()
        for func_name in self.eq_dict.values():
            if func_name in variables:
                    variables.remove(func_name)
        return variables


class XmileExpression(Expression):

    def __init__(self, xmile_expression):
        self.expression = xmile_expression

    def variables(self):
        variables = []
        items = [self.expression[0]]
        for item in items:
            try:
                if isinstance(item, ParseResults):
                    # print('get_variables. item, item.name: ', item, item.getName())
                    if item.getName() is None or item.getName() == 'composed':
                        for part in item:
                            if isinstance(part, ParseResults):
                                items.append(part)
                    elif item.getName() == 'unary_function':
                        items.append(item.parameter)
                    elif item.getName().endswith('_function'):
                        for param in item.parameters:
                            items.append(param)
                    elif item.getName() == 'ident':
    #                    print('get_variables. item.ident: ', item.ident[0])
                        variables.append(item.ident[0])
                else:
                    print('item not ParseResults: ', item, type(item))
            except:
                print('ouch!')
                traceback.print_exc()
                print('-------------')

        return variables


class EquationParser(object):

    def parse(self, expression):
        raise NotImplementedError()

    @classmethod
    def create_parser(cls, name):
        """
        Retorna un parser de acuerdo al nombre.
        Nombres validos:

        """
        if name == Parsers.PY_EXPRESSION_EVAL_PARSER:
            return PyExpressionEvalParserWrapper()

        if name == Parsers.XMILE_FUNCTION_PARSER:
            return XmileEquationParser()


class PyExpressionEvalParserWrapper(EquationParser):

    def __init__(self):
        self.parser = PeeParser()

    def parse(self, expression):
        return PyExpressionEvalExpression(self.parser.parse(expression))


class XmileEquationParser(EquationParser):
    '''
    Basado en ejemplos de Pyparsing
    https://github.com/pyparsing/pyparsing/tree/master/examples
    '''

    def __init__(self):

        LPAR, RPAR, COMMA = map(Suppress, "(),")
        (AND, NOT, OR) = map(CaselessKeyword,
                             """AND NOT OR""".split())

        keyword = MatchFirst((AND, NOT, OR))
        unary_built_functions_names = MatchFirst(map(CaselessKeyword, """"ABS ARCCOS ARCSIN ARCTAN COS EXP INT LN LOG10 SIN SQRT TAN""".split()))

        identifier = (~keyword +
                      ~unary_built_functions_names +
                      Word(alphas, alphanums+"_"))('ident')
        function_name = identifier.copy()

        point = Literal(".")
        expr = Forward()

        # expression
        expr = Forward().setName("expression")

        numeric_literal = (Regex(r"\d+(\.\d*)?([eE][+-]?\d+)?"))('number')
        string_literal = quotedString("'")('quoted_str')
        literal_value = (numeric_literal | identifier | string_literal)

        # Funciones xmile
        built_in_unary_function = (unary_built_functions_names('function_name') +
                                   LPAR + expr('parameter') + RPAR).setResultsName("function")

        ramp_function = (CaselessKeyword("RAMP")("function_name") +
                         LPAR + expr("slope") + COMMA +
                         expr("start_time") + RPAR).setResultsName("ramp_function")

        step_function = (CaselessKeyword("STEP")("function_name") +
                         LPAR + expr("height") + COMMA +
                         expr("start_time") + RPAR).setResultsName("step_function")

        pulse_function = (CaselessKeyword("PULSE")("function_name") +
                          LPAR + expr("magnitud") + COMMA +
                          expr("first_time") + 
                          Optional(COMMA + expr("interval")) + RPAR).setResultsName("pulse_function")

        # Funciones propias
        custom_function = (function_name("function_name") +
                           LPAR + Optional(delimitedList(expr)) + RPAR)("function")

        expr_term = Group(built_in_unary_function |
                          ramp_function |
                          step_function |
                          pulse_function |
                          custom_function |
                          literal_value)

        UNARY, BINARY, TERNARY = 1, 2, 3
        expr << infixNotation(expr_term,
                              [((oneOf('- +') | NOT), UNARY, opAssoc.RIGHT),
                               ('^', BINARY, opAssoc.LEFT),
                               (oneOf('* / % MOD'), BINARY, opAssoc.LEFT),
                               (oneOf('+ -'), BINARY, opAssoc.LEFT),
                               (oneOf('< <= > >='), BINARY, opAssoc.LEFT),
                               (oneOf('= <>'), BINARY, opAssoc.LEFT),
                               (AND, BINARY, opAssoc.LEFT),
                               (OR, BINARY, opAssoc.LEFT),
                               ])('composed')

        self.bnf = expr

    def parse(self, equation, parseAll=True):
        return XmileExpression(self.bnf.parseString(equation, parseAll))
