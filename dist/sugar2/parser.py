#8< ---[sugar2/parser.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
import libparsing
__module_name__ = 'sugar2.parser'
class Parser:
	def __init__ (self, command, version=None):
		self.version = None
		self.command = None
		self.logger = None
		self.grammar = None
		self.builderClass = None
		if version is None: version = 2
		self.version = version
		self.grammar = self.createGrammar(version)
		self.command = command
		self.logger = command.environment.report
	
	def createGrammar(self, version=None):
		if version is None: version = self.version
		if (version == 1):
			import sugar2.v1.program
			return sugar2.v1.program.createProgramGrammar()
		elif True:
			import sugar2.v2.program
			return sugar2.v2.program.createProgramGrammar()
	
	def createBuilder(self, path, version=None):
		if version is None: version = self.version
		builder=None
		if (version == 1):
			import sugar2.v1.writer
			builder = sugar2.v1.writer.LambdaFactoryBuilder
		elif True:
			import sugar2.v2.writer
			builder = sugar2.v2.writer.LambdaFactoryBuilder
		return builder(self.grammar, path)
	
	def parseString(self, text, moduleName, path):
		result=self.grammar.parseString(text)
		builder=self.createBuilder(path)
		if result.isPartial():
			r=result.lastMatchRange()
			t=result.text
			self.logger.error(result.describe())
			return [text, None]
		elif result.isFailure():
			r=result.lastMatchRange()
			t=result.text
			self.logger.error(result.describe())
			return [text, None]
		elif result.isSuccess():
			module=builder.process(result.match)
			return [text, module]
	

