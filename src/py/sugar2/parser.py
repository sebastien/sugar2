#8< ---[sugar2/parser.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
import libparsing
from sugar2.writer import LambdaFactoryBuilder
from sugar2.grammar.program import createProgramGrammar
__module_name__ = 'sugar2.parser'
class Parser:
	G = createProgramGrammar(libparsing.Grammar('Sugar', True))
	def __init__ (self, command):
		self.command = None
		self.logger = None
		self.command = command
		self.logger = command.environment.report
	
	def parseString(self, text, moduleName, path):
		result=self.__class__.G.parseString(text)
		builder=LambdaFactoryBuilder(self.__class__.G, path)
		if result.isPartial():
			r=result.lastMatchRange()
			t=result.text
			print (result.describe())
			return [text, None]
		elif result.isFailure():
			r=result.lastMatchRange()
			t=result.text
			print (result.describe())
			return [text, None]
		elif result.isSuccess():
			module=builder.process(result.match)
			return [text, module]
	

