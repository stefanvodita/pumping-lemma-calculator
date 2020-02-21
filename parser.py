from antlr4 import *
from conditionsParser import conditionsParser
from conditionsLexer import conditionsLexer
from conditionsListener import conditionsListener


def parse(conditions_string):
    lexer = conditionsLexer(InputStream(conditions_string))
    stream = CommonTokenStream(lexer)
    parser = conditionsParser(stream)
    tree = parser.conditions()
    listener = ConditionsListener()
    return listener.exitConditions(tree)


class ConditionsListener(conditionsListener):

    def __init__(self):
        self.conditions = {}

    def exitConditions(self, ctx:conditionsParser.ConditionsContext):
        pass
