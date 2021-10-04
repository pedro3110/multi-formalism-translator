from __future__ import division
from pyparsing import (Dict, Regex, Literal, CaselessLiteral, Word,
                       Combine, Suppress, replaceWith, CaselessKeyword,
                       Group, Optional, infixNotation, opAssoc,
                       ZeroOrMore, Forward, nums, alphas, alphanums,
                       oneOf, MatchFirst, ParseResults,
                       delimitedList, unicodeString, quotedString)
import traceback


def get_variables(results):
    variables = []
    items = [results[0]]
    for item in items:
        try:
            if isinstance(item, ParseResults):
                # print('get_variables. item.name: ', item.getName())
                if item.getName() == 'composed':
                    for part in item:
                        if isinstance(part, ParseResults):
                            items.append(part)
                elif item.getName() == 'unary_function':
                    items.append(item.parameter)
                elif item.getName().endswith('_function'):
                    for param in item.parameters:
                        items.append(param)
                elif item.getName() == 'ident':
                    # print('get_variables. item.ident: ', item.ident[0])
                    variables.append(item.ident[0])
            else:
                print('item not ParseResults: ', item, type(item))
        except:
            print('ouch!')
            traceback.print_exc()
            print('-------------')

    return variables


class XmileEquationParser(object):
    '''
    Basado en ejemplos de Pyparsing
    https://github.com/pyparsing/pyparsing/tree/master/examples
    '''

    def __init__(self):
        LPAR, RPAR, COMMA = map(Suppress, "(),")
        (AND, NOT, OR) = map(CaselessKeyword,
                             """AND NOT OR""".split())

        keyword = MatchFirst((AND, NOT, OR))
        unary_built_functions_names = MatchFirst(
            map(CaselessKeyword, """"ABS ARCCOS ARCSIN ARCTAN COS EXP INT LN LOG10 SIN SQRT TAN""".split()))

        identifier = (~keyword + ~unary_built_functions_names + Word(alphas, alphanums + "_"))('ident')
        function_name = identifier.copy()

        point = Literal(".")
        expr = Forward()

        # expression
        expr = Forward().setName("expression")

        numeric_literal = (Regex(r"\d+(\.\d*)?([eE][+-]?\d+)?"))('number')
        string_literal = quotedString("'")('quoted_str')
        literal_value = (numeric_literal | identifier | string_literal)

        # Funciones xmile
        built_in_unary_function = (
        unary_built_functions_names('function_name') + LPAR + expr('parameter') + RPAR).setResultsName("unary_function")

        ramp_function = (
        CaselessKeyword("RAMP")("function_name") + LPAR + Group(expr("slope") + COMMA + expr("start_time"))(
            "parameters") + RPAR).setResultsName("ramp_function")

        step_function = (
        CaselessKeyword("STEP")("function_name") + LPAR + Group(expr("height") + COMMA + expr("start_time"))(
            "parameters") + RPAR).setResultsName("step_function")

        pulse_function = (CaselessKeyword("PULSE")("function_name") + LPAR + Group(
            expr("magnitud") + COMMA + expr("first_time") + Optional(COMMA + expr("interval")))(
            "parameters") + RPAR).setResultsName("pulse_function")

        # Funciones propias
        custom_function = (
        function_name("function_name") + LPAR + Group(Optional(delimitedList(expr)))("parameters") + RPAR)(
            "custom_function")

        expr_term = Group(
            built_in_unary_function | ramp_function | step_function | pulse_function | custom_function | literal_value)

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
        return self.bnf.parseString(equation, parseAll)


if __name__ == "__main__":

    parser = XmileEquationParser()
    expressions = ["1+x",
                   "SIN(Stock_1)",
                   "SIN(Stock_1 * 0.5)",
                   "SIN(Stock_1 * x)",
                   "Stock_1",
                   "STEP(6,3)",
                   "RAMP(x,y)",
                   "SIN(Stock_1)+Stock_2",
                   "PULSE(20,y,5)",
                   "PULSE(10,X)",
                   "MyFunc(x,y,z)",
                   "OtherFunc(x)",
                   "AnotherFunc(1)",
                   "OneMoreF(1,x)"
                   ]
    for expr in expressions:
        try:
            print('parsing: %s', expr)
            raw_results = parser.parse(expr, True)
            results = raw_results[0]
            # print('parsed: ', results.getName())
            try:
                variables = get_variables(raw_results)
                print('variables: ', variables)
                """    if results.getName() == 'step_function':
                    print(results.asDict())
                    print('f_name: ', results.asDict()['function_name'])
                    print('f_height: ', results.asDict()['height'])
                    print('f_start_time: ', results.start_time)

                if results.getName() == 'ramp_function':
                    print('f_name: ', results.asDict()['function_name'])
                    print('f_slope: ', results.asDict()['slope'])
                    print('f_start_time: ', results.start_time)

                if results.getName() == 'pulse_function':
                    print('f_name: ', results.asDict()['function_name'])
                    print('f_magnitud: ', results.asDict()['magnitud'])
                    print('f_first_time: ', results.asDict()['first_time'])
                    if results.interval is not None and results.interval != '':
                        print('f_interval: ', results.interval)
                    # print('f_start_time: ', results.start_time)

                if results.getName() == 'function':
                    print('f_name: ', results.asDict()['function_name'])
                    print('f_param: ', results.asDict()['parameter'])

                if results.getName() == 'composed':
                    for token in results:
                        if isinstance(token, ParseResults):
                            print(token.getName())
                            if token.getName() == 'function':
                                print('f_name: ', token.asDict()['function_name'])
                                print('f_param: ', token.asDict()['parameter'])
                """

            except TypeError as te:
                pass
        except:
            print("Error parsing %s", expr)
