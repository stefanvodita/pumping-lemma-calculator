SCRIPT=main.py
GRAMMAR=conditions

run:
	python3 $(SCRIPT)

parser:
	antlr4 -Dlanguage=Python3 $(GRAMMAR).g4

clean:
	rm *.interp *.tokens $(GRAMMAR)Lexer.py $(GRAMMAR)Listener.py $(GRAMMAR)Parser.py