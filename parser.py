from antlr4 import *
from conditionsParser import conditionsParser
from conditionsLexer import conditionsLexer
from conditionsListener import conditionsListener


def parse(conditions_string, w, exponent_values):
    lexer = conditionsLexer(InputStream(conditions_string))
    stream = CommonTokenStream(lexer)
    parser = conditionsParser(stream)
    tree = parser.conditions()
    listener = ConditionsListener(w, exponent_values)
    return listener.exitConditions(tree)


class ConditionsListener(conditionsListener):

    def __init__(self, w, conditions):
        self.w = w
        self.conditions = conditions

    def exitConditions(self, ctx:conditionsParser.ConditionsContext):
        # print("Entered exitConditions, ctx is", ctx.getText(), "and has", ctx.getChildCount(), "children")
        if ctx.conditions():
            # print("Recursive case")
            ret = self.exitCondition(ctx.getChild(0)) and self.exitConditions(ctx.getChild(2))
        elif ctx.condition():
            # print("Single condition case")
            ret = self.exitCondition(ctx.getChild(0))
        else:
        	# print("Third case")
        	ret = True

        # print("Exit exitConditions with", ret)
        return ret

    def exitCondition(self, ctx:conditionsParser.ConditionContext):
        print("Entered exitCondition, ctx is", ctx.getText(), "and has", ctx.getChildCount(), "children")
        ret = (self.exitRelation(ctx.getChild(1))(self.exitExpression(ctx.getChild(0)), \
                                                  self.exitExpression(ctx.getChild(2))))
        # print("Exit exitCondition with", ret)
        return ret

    def exitExpression(self, ctx:conditionsParser.ExpressionContext):
        # print("Entered exitExpression, ctx is", ctx.getText(), "and has", ctx.getChildCount(), "children")
        if ctx.expression():
            if ctx.getChild(1).getText() == '+':
                f = lambda a, b: a + b
            elif ctx.getChild(1).getText() == '-':
                f = lambda a, b: a - b
            elif ctx.getChild(1).getText() == '*':
                f = lambda a, b: a * b
            elif ctx.getChild(1).getText() == '/':
                f = lambda a, b: a // b
            elif ctx.getChild(1).getText() == '%':
                f = lambda a, b: a % b
            ret = f(self.exitOperand(ctx.getChild(0)), self.exitOperand(ctx.getChild(2)))
        else:
            ret = self.exitOperand(ctx.getChild(0))
        # print("Exit exitExpression with", ret)
        return ret

    def exitRelation(self, ctx:conditionsParser.RelationContext):
        # print("Entered exitRelation, ctx is", ctx.getText(), "and has", ctx.getChildCount(), "children")
        if ctx.EQ():
            ret = lambda a, b: a == b
        elif ctx.LT():
            ret = lambda a, b: a < b
        elif ctx.GT():
            ret = lambda a, b: a > b
        elif ctx.LE():
            ret = lambda a, b: a <= b
        elif ctx.GE():
            ret = lambda a, b: a >= b
        elif ctx.NE():
            ret = lambda a, b: a != b
        # print("Exit exitRelation with", ret)
        return ret

    def exitOperand(self, ctx:conditionsParser.OperandContext):
        # print("Entered exitOperand, ctx is", ctx.getText(), "and has", ctx.getChildCount(), "children")
        if ctx.NUMBER():
            ret = int(ctx.getChild(0).getText())
        elif ctx.VARIABLE():
            ret = self.conditions[ctx.getChild(0).getText()]
        elif ctx.CHARACTER():
        	# TODO
            pass
        # print("Exit exitOperand with", ret)
        return ret
