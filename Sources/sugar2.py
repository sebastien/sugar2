#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
import parsing
import sys
import ipdb
from parsing import ParsingResult
from lambdafactory import interfaces
from lambdafactory.main import Command
from lambdafactory.modelbase import Factory
from lambdafactory.environment import Environment
from lambdafactory.splitter import FileSplitter
import lambdafactory.passes as passes
import lambdafactory.resolution as resolution
__module_name__ = 'sugar2'
__version__ = '0.9'
G = None
F = Factory()
def doIndent (context):
	self=__module__
	v=context.getVariables().getParent()
	i=(v.get('requiredIndent') or 0)
	v.set('requiredIndent', (i + 1))


def doCheckIndent (context):
	self=__module__
	v=context.getVariables()
	tab_match=context.getVariables().get('tabs')
	tab_indent=len(tab_match.group())
	req_indent=(v.get('requiredIndent') or 0)
	return (tab_indent == req_indent)


def doDedent (context):
	self=__module__
	v=context.getVariables().getParent()
	i=(v.get('requiredIndent') or 0)
	v.set('requiredIndent', (i - 1))


def doBlockStart (context):
	self=__module__
	v=context.getVariables().getParent()
	v.set('blockVariables', v)


def doBlockLastSetLine (context):
	self=__module__
	v=context.getVariables().get('blockVariables')
	v.set('blockLast', 'line')


def doBlockLastSetBody (context):
	self=__module__
	v=context.getVariables().get('blockVariables')
	v.set('blockLast', 'body')


def doBlockLastIsLine (context):
	self=__module__
	return (context.getVariables().get('blockLast') == 'line')


def declaration (grammar, name, prefix):
	self=__module__
	g=grammar
	s=g.symbols
	return g.rule(name, s.CheckIndent, prefix, s.NameType._as('name'), g.arule(g.aword('='), s.Expression).optional()._as('value'), s.EOL, s.Documentation.optional()._as('documentation'))


def function (grammar, name, prefix, anonymous=None):
	self=__module__
	if anonymous is None: anonymous = False
	g=grammar
	s=grammar.symbols
	if anonymous:
		return g.rule(name, s.CheckIndent, prefix._as('type'), g.agroup(s.EOL, g.arule(s.ParameterList.optional(), s.EOL))._as('parameters'), s.Documentation.optional()._as('documentation'), s.Body._as('body'), s.OEnd)
	elif True:
		return g.rule(name, s.CheckIndent, prefix._as('type'), s.NameType._as('name'), g.agroup(s.EOL, g.arule(s.ParameterList.optional(), s.EOL))._as('parameters'), s.Documentation.optional()._as('documentation'), s.Body._as('body'), s.OEnd)


def abstractFunction (grammar, name, prefix):
	self=__module__
	g=grammar
	s=grammar.symbols
	return g.rule(name, s.CheckIndent, s.oabstract, prefix.bindAs('type'), s.NameType.bindAs('name'), g.agroup(s.EOL, g.arule(s.ParameterList.optional().bindAs('parameters'), s.EOL)), s.Documentation.optional().bindAs('documentation'))


def listOf (rule, separator, grammar):
	"""Creates a new list of the given rule, separated by the given separator
	in the given grammar"""
	self=__module__
	return grammar.arule(grammar.arule(rule, separator).zeroOrMore(), rule)


def createProgramGrammar (g=None):
	self=__module__
	if g is None: g = parsing.Grammar('Sugar')
	s=g.symbols
	g.token('SPACE', '[ ]+')
	g.token('TABS', '\t*')
	g.token('EMPTY_LINES', '([ \t]*\n)+')
	g.token('INDENT', '\t+')
	g.token('COMMENT', '[ \t]*\\#[^\n]*')
	g.token('EOL', '[ ]*\n(\\s*\n)*')
	g.token('NUMBER', '-?(0x)?[0-9]+(\\.[0-9]+)?')
	g.token('NAME', '(\\\\?)([\\$_A-Za-z]\\w*)')
	g.token('KEY', '[\\$_A-Za-z]\\w*')
	g.token('INFIX_OPERATOR', '([\\-\\+\\*\\/\\%]|\\<=|\\>=|\\<|\\>|==|\\!=|in\\s+|and\\s+|or\\s+|\\*\\*)')
	g.token('PREFIX_OPERATOR', '(not\\s+|\\-)')
	g.token('NEW_OPERATOR', 'new\\s+')
	g.token('ASSIGN_OPERATOR', '[\\?\\*\\+\\-\\/\\%]?=')
	g.token('SYMBOLIC', 'None|Undefined|Nothing|Timeout')
	g.token('STRING_SQ', "'(\\\\'|[^'\\n])*'")
	g.token('STRING_DQ', '"(\\\\"|[^"\\n])*"')
	g.token('DOCSTRING', '\\|[^\n]*')
	g.token('EMBED_LINE', '\\|([^\n]*)')
	g.token('VERSION', '[0-9]+(\\.[0-9]+)?(\\.[0-9]+)?[a-zA-Z_]*')
	g.word('LP', '(')
	g.word('RP', ')')
	g.word('LB', '{')
	g.word('RB', '}')
	g.word('LSB', '[')
	g.word('RSB', ']')
	g.word('COMMA', ',')
	g.word('DOT', '.')
	g.word('COLON', ':')
	g.word('SEMICOLON', ';')
	g.word('PIPE', '|')
	g.word('EQUALS', '=')
	g.word('WILDCARD', '*')
	g.word('ITERATOR', '::')
	g.word('BLOCKLINE', '->')
	g.word('ELLIPSIS', '...')
	g.word('_var', 'var')
	g.word('_if', 'if')
	g.word('_elif', 'elif')
	g.word('_else', 'else')
	g.word('_for', 'for')
	g.word('_while', 'while')
	g.word('_end', 'end')
	g.word('_in', 'in')
	g.word('_from', 'from')
	g.word('_as', 'as')
	g.word('_try', 'try')
	g.word('_catch', 'catch')
	g.word('oabstract', '@abstract')
	g.word('oimport', '@import')
	g.word('omodule', '@module')
	g.word('otarget', '@target')
	g.word('orequires', '@requires')
	g.word('oversion', '@version')
	g.word('olicense', '@license')
	g.word('ofunction', '@function')
	g.word('oclass', '@class')
	g.word('oproperty', '@property')
	g.word('oshared', '@shared')
	g.word('ooperation', '@operation')
	g.word('oconstructor', '@constructor')
	g.word('omethod', '@method')
	g.word('ogroup', '@group')
	g.word('oend', '@end')
	g.word('oembed', '@embed')
	g.procedure('Indent', doIndent)
	g.procedure('Dedent', doDedent)
	g.rule('CheckIndent', s.TABS.bindAs('tabs'), g.acondition(doCheckIndent)).disableMemoize()
	g.rule('CommentLine', s.COMMENT, s.EOL)
	g.rule('EmptyLines', s.EMPTY_LINES)
	g.rule('DocumentationLine', s.CheckIndent, s.DOCSTRING, s.EOL)
	g.rule('Documentation', s.DocumentationLine.oneOrMore())
	g.group('String', s.STRING_SQ, s.STRING_DQ)
	g.rule('Expression')
	g.group('Key', s.KEY, s.NUMBER, s.String, g.arule(s.LP, s.Expression, s.RP))
	g.rule('KeyValue', s.Key, s.COLON, s.Expression)
	g.rule('KeyValueList', s.KeyValue, g.arule(s.COMMA, s.KeyValue).zeroOrMore())
	g.rule('ExpressionList', s.Expression, g.arule(s.COMMA, s.Expression).zeroOrMore())
	g.rule('ExpressionBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.ExpressionList).oneOrMore(), s.Dedent)
	g.rule('KeyValueBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.KeyValueList).oneOrMore(), s.Dedent)
	g.rule('Array', s.LSB, s.ExpressionList.optional(), s.ExpressionBlock.optional(), g.arule(s.EOL, s.CheckIndent).optional(), s.RSB)
	g.rule('Map', s.LB, s.KeyValueList.optional(), s.KeyValueBlock.optional(), g.arule(s.EOL, s.CheckIndent).optional(), s.RB)
	g.rule('Type', s.NAME)
	g.rule('NameType', s.NAME, g.arule(s.COLON, s.Type).optional())
	g.rule('FQName', s.NAME, g.arule(s.DOT, s.NAME).zeroOrMore())
	g.rule('Parameter', s.NameType._as('name'), g.arule(s.EQUALS, s.Expression).optional()._as('value'))
	g.rule('ParameterList', s.Parameter, g.arule(s.COMMA, s.Parameter).zeroOrMore(), s.ELLIPSIS.optional())
	g.rule('SymbolList', s.NAME, g.arule(s.COMMA, s.NAME).zeroOrMore(), s.ELLIPSIS.optional())
	g.rule('ArgumentsEmpty', s.LP, s.RP)
	g.rule('ArgumentsMany', s.LP, s.ExpressionList, s.RP)
	g.rule('ClosureStatement', s.Expression)
	g.rule('ClosureBody', s.EOL, s.Expression)
	g.rule('Closure', s.LB, g.arule(s.ParameterList.optional(), s.PIPE).optional()._as('params'), s.ClosureStatement.optional()._as('line'), s.ClosureBody.optional()._as('body'), g.arule(s.EOL, s.CheckIndent).optional(), s.INDENT.optional(), s.RB)
	g.group('Literal', s.NUMBER, s.SYMBOLIC, s.String, s.Array, s.Map, s.Closure)
	g.rule('Decomposition', g.agroup(s.DOT, s.SPACE), s.NAME, g.arule(g.agroup(s.DOT, s.SPACE), s.NAME).zeroOrMore())
	g.rule('ComputationInfix', s.INFIX_OPERATOR, s.Expression)
	g.rule('Access', s.LSB, s.Expression, s.RSB)
	g.rule('Slice', s.LSB, s.Expression.optional(), s.COLON, s.Expression.optional(), s.RSB)
	g.group('Invocation', s.ArgumentsEmpty, s.ArgumentsMany, s.Literal)
	g.group('Prefixes', g.rule('Parentheses', s.LP, s.Expression, s.RP), g.rule('Instanciation', s.NEW_OPERATOR, s.FQName._as('name'), s.Invocation._as('params')), g.rule('ComputationPrefix', s.PREFIX_OPERATOR, s.Expression), s.Literal, s.NAME)
	g.group('Suffixes', s.ComputationInfix, s.Decomposition, s.Access, s.Slice, s.Invocation)
	s.Expression.set(s.Prefixes, s.Suffixes.zeroOrMore())
	g.rule('Assignable', s.NAME, g.agroup(s.Decomposition, s.Access, s.Slice).zeroOrMore())
	g.rule('Allocation', s._var, s.SymbolList._as('target'), g.arule(s.PIPE, s.NAME).optional()._as('rest'), g.arule(s.EQUALS, s.Expression).optional()._as('value'))
	g.rule('Assignment', g.arule(s.Assignable, s.COMMA).zeroOrMore()._as('before'), s.Assignable._as('main'), g.arule(s.PIPE, s.Assignable).optional()._as('rest'), g.arule(s.ASSIGN_OPERATOR, s.Expression)._as('op'))
	g.rule('Termination', g.aword('return'), s.Expression.optional())
	g.rule('IterationLine', s.Expression, s.ITERATOR, s.Expression)
	g.group('Block')
	g.group('Code')
	g.rule('Comment', s.COMMENT, s.EOL)
	g.group('Statement', s.Comment, s.Block, s.Allocation, s.Assignment, s.Termination, s.IterationLine, s.Expression)
	g.rule('Statements', s.Statement, g.arule(s.SEMICOLON, s.Statement).zeroOrMore())
	g.rule('Line', s.CheckIndent, s.Statements.optional(), s.COMMENT.optional(), s.EOL)
	g.rule('End', s.CheckIndent, s._end, s.EOL)
	g.procedure('BlockStart', doBlockStart)
	g.condition('BlockLastIsLine', doBlockLastIsLine)
	g.procedure('BlockLastSetLine', doBlockLastSetLine)
	g.procedure('BlockLastSetBody', doBlockLastSetBody)
	g.rule('BlockLine', s.BLOCKLINE, s.Statements, g.agroup(s.COMMENT, s.EOL).zeroOrMore(), s.BlockLastSetLine)
	g.rule('BlockBody', s.EOL, s.Indent, s.Code.zeroOrMore(), s.Dedent, s.BlockLastSetBody)
	g.group('BlockEnd', s.BlockLastIsLine, s.End).disableMemoize()
	g.rule('IfBranch', s.CheckIndent.optional(), s._if, s.Expression, g.agroup(s.BlockBody, s.BlockLine))
	g.rule('ElifBranch', s.CheckIndent, s._elif, s.Expression, g.agroup(s.BlockBody, s.BlockLine))
	g.rule('ElseBranch', s.CheckIndent, s._else, g.agroup(s.BlockBody, s.BlockLine))
	g.rule('WhileBranch', s.CheckIndent, s._while, s.Expression._as('condition'), g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('TryBranch', s.CheckIndent, s._try, g.agroup(s.BlockBody, s.BlockLine))
	g.rule('CatchBranch', s.CheckIndent, s._catch, s.Parameter.optional(), g.agroup(s.BlockBody, s.BlockLine))
	g.rule('ForBranch', s.CheckIndent, s._for, s.ParameterList._as('params'), s._in, s.Expression._as('expr'), g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('Conditional', s.BlockStart, s.IfBranch, s.ElifBranch.zeroOrMore(), s.ElseBranch.optional(), s.BlockEnd)
	g.rule('Try', s.BlockStart, s.TryBranch, s.CatchBranch.optional(), s.BlockEnd)
	g.rule('Repetition', s.BlockStart, s.WhileBranch._as('while'), s.BlockEnd)
	g.rule('Iteration', s.BlockStart, s.ForBranch._as('for'), s.BlockEnd)
	s.Block.set(s.Conditional, s.Repetition, s.Iteration, s.Try)
	s.Code.set(s.Comment, s.Block, s.Line)
	g.rule('OEnd', s.CheckIndent, s.oend, s.EOL)
	g.rule('Body', s.Indent, s.Code.zeroOrMore().bindAs('code'), s.Dedent)
	s.ClosureStatement.set(s.Statements)
	s.ClosureBody.set(s.EOL, s.Body)
	declaration(g, 'ClassAttribute', s.oshared)
	declaration(g, 'ModuleAttribute', s.oshared)
	declaration(g, 'Attribute', s.oproperty)
	abstractFunction(g, 'AbstractFunction', s.ofunction)
	abstractFunction(g, 'AbstractMethod', s.omethod)
	abstractFunction(g, 'AbstractOperation', s.ooperation)
	function(g, 'Function', s.ofunction)
	function(g, 'Constructor', s.oconstructor, True)
	function(g, 'Method', s.omethod)
	function(g, 'Operation', s.ooperation)
	g.rule('CGroup')
	g.group('Methods', s.Method, s.AbstractMethod, s.AbstractMethod, s.CGroup, s.Comment)
	s.CGroup.set(s.CheckIndent, s.ogroup, s.NAME._as('name'), s.EOL, s.Documentation.optional(), s.Indent, s.Methods.zeroOrMore()._as('methods'), s.Dedent, s.OEnd)
	g.rule('EmbedLine', s.CheckIndent, s.EMBED_LINE, s.EOL)
	g.rule('Embed', s.CheckIndent, s.oembed, s.NAME.optional()._as('language'), s.EOL, s.EmbedLine.zeroOrMore()._as('body'), s.OEnd)
	s.Block.append(s.Embed)
	g.rule('Class', g.aword('@abstract').optional(), g.aword('@class'), s.NameType._as('name'), g.arule(s.COLON, listOf(s.FQName, s.COMMA, g)).optional()._as('inherits'), s.EOL, s.Documentation.optional()._as('documentation'), s.Indent, g.agroup(s.ClassAttribute, s.Attribute, s.Operation, s.AbstractOperation, s.Constructor, s.Methods).zeroOrMore()._as('body'), s.Dedent, g.aword('@end'))
	g.rule('ModuleAnnotation', s.omodule, s.FQName, s.EOL)
	g.rule('VersionAnnotation', s.oversion, s.VERSION, s.EOL)
	g.rule('RequiresAnnotation', s.orequires, s.FQName, g.arule(s.COMMA, s.FQName).zeroOrMore(), s.EOL)
	g.rule('TargetAnnotation', s.otarget, s.NAME.oneOrMore(), s.EOL)
	g.rule('ImportSingleSymbol', s.oimport, s.NAME, s._from, s.FQName, g.arule(s._as, s.NAME).optional(), s.EOL)
	g.rule('ImportSingleFQSymbol', s.oimport, s.FQName, g.arule(s._as, s.NAME).optional(), s.EOL)
	g.rule('ImportMultipleSymbols', s.oimport, s.NAME, g.arule(s.COMMA, s.NAME).zeroOrMore(), s._from, s.FQName, s.EOL)
	g.rule('ImportAllSymbols', s.oimport, s.WILDCARD, s._from, s.FQName, s.EOL)
	g.group('ImportOperation', s.ImportAllSymbols, s.ImportMultipleSymbols, s.ImportSingleFQSymbol, s.ImportSingleSymbol)
	g.rule('ModuleDeclaration', s.EmptyLines.zeroOrMore(), s.Comment.zeroOrMore(), s.ModuleAnnotation.optional(), s.VersionAnnotation.optional(), s.RequiresAnnotation.optional(), s.TargetAnnotation.optional(), s.ImportOperation.zeroOrMore())
	g.group('Structure', s.EmptyLines, s.Comment, s.ModuleAttribute, s.Function, s.Class)
	g.rule('Module', s.ModuleDeclaration, s.Structure.zeroOrMore(), s.Code.zeroOrMore())
	g.ignore(s.SPACE, s.COMMENT)
	g.axiom = s.Module
	return g


class TreeBuilder:
	def __init__ (self, path=None):
		self.g = None
		self.path = None
		if path is None: path = None
		self.path = path
	
	def build(self, result, grammar):
		self.g = grammar
		return self.on(result)
	
	def flatten(self, l, r=None):
		if r is None: r = []
		if (not (type(l) in [tuple, list])):
			return r
		elif True:
			for e in l:
				if (type(e) in [tuple, list]):
					self.flatten(e, r)
				elif True:
					r.append(e)
		return r
	
	def getElements(self, l):
		res=[]
		for e in self.flatten(l):
			if isinstance(e, interfaces.IElement):
				res.append(e)
		return res
	
	def on(self, parsingResult):
		"""Expand the given value, so that the ParsingResults are converted to values
		expanded by the corresponding `onXXX` methods."""
		if isinstance(parsingResult, parsing.ParsingResult):
			element=parsingResult.element
			data=parsingResult.data
			context=parsingResult.context
			element_name=(element.name or element.__class__.__name__)
			method_name=('on' + (element_name[0].upper() + element_name[1:]))
			if hasattr(self, method_name):
				res=getattr(self, method_name)(element, data, context)
				return res
			elif True:
				res=self._onMissing(element, data, context)
				return res
		elif ((type(parsingResult) == list) or (type(parsingResult) == tuple)):
			res = []
			for _ in parsingResult:
				e=self.on(_)
				res.append(e)
			return res
		elif True:
			return parsingResult
	
	def _onMissing(self, element, data, context):
		return self.on(data)
	

class LambdaFactoryBuilder(TreeBuilder):
	"""Converts a parse tree into a Lambda Factory program model, which can then
	be translated to one of Lambda Factory's target language.
	
	Each `onXXX` should return a corresponding LambdaFactory model, or a list
	of them. The basic structure for a `onXXX` (where `XXX` is the rule name) is
	like that:
	
	```
	@method on<RuleName> element, data, context
	# element is the `parsing.Element` subclass
	# data is the raw data returned by the element `process` method
	# context is the `parsing.ParsingContext` instance
	#
	# Here, we retrieve the part of the data for the "code" rule. The
	# code_data will contain one or more (element, data, context) triples.
	var code_data = element resolve ("code", data)
	# And we apply the rules for the specific elements, and retrieve a
	# lambda factory object
	var code      = on (code_data)
	# We should then do something with the object...
	return code
	@end
	```"""
	OPERATORS = [['or'], ['and'], ['>', '>=', '<', '<=', '!=', '==', 'is', 'is not', 'in', 'not in'], ['+', '-'], ['not'], ['/', '*', '%', '//'], ['/=', '*=', '%=', '+=', '-=']]
	def __init__ (self, path=None):
		self.module = None
		self.process = None
		self.scopes = []
		self.processes = []
		if path is None: path = None
		TreeBuilder.__init__(self,path)
	
	def getDefaultModuleName(self):
		return self.path.split('/')[-1].split('.')[0].replace('-', '_')
	
	def normalizeOperator(self, operator):
		while (((len(operator) > 0) and (operator[-1] == ' ')) or (operator[-1] == '\t')):
			operator = operator[0:-1]
		return operator
	
	def getOperatorPriority(self, operator):
		i=0
		for line in self.__class__.OPERATORS:
			if (operator in line):
				return i
			i = (i + 1)
		raise Exception(('Unknown operator: ' + str(operator)))
	
	def _var(self, name=None, context=None):
		"""Lists the variables defined in the given context or gets the
		variable with the given name."""
		if name is None: name = None
		if context is None: context = self.context
		if (not name):
			return context.getVariables().keys()
		elif True:
			return context.getVariables().get(name)
	
	def _bind(self, referanceable):
		"""Assigns the given referenceable to the current scope"""
		self.scopes[-1].setSlot(referanceable.getName(), referanceable)
	
	def _onlyWithValue(self, result):
		"""Returns only the elements of result that have a value"""
		return filter(lambda _:_, result)
		
	
	def _tryGet(self, list, index, default):
		"""Tries to get the `index`th element of `list` or returns `default`"""
		if (list and (len(list) > index)):
			return list[index]
		elif True:
			return None
	
	def _setCode(self, process, code):
		code = (code or [])
		for line in (code or []):
			if (type(line) != type([])):
				line = [line]
			for statement in (line or []):
				if isinstance(statement, interfaces.IOperation):
					process.addOperation(statement)
		return process
	
	def onModule(self, element, data, context):
		self.context = context
		data_declaration=element.resolve(self.g.symbols.ModuleDeclaration, data)
		annotations = {}
		for _ in self.on(data_declaration):
			if isinstance(_, interfaces.IAnnotation):
				annotations[_.getName()] = _.getContent()
		self.module = F.createModule((annotations.get('module') or self.getDefaultModuleName()))
		self.scopes.append(self.module)
		if annotations.get('version'):
			res=F._moduleattr('VERSION', None, F._string(annotations.get('version')))
			self._bind(res)
		data_structure=element.resolve(self.g.symbols.Structure, data)
		structure = self.on(data_structure)
		data_code=element.resolve(self.g.symbols.Code, data)
		main_function=F.createFunction(F.MainFunction)
		code=self.on(data_code)
		self._setCode(main_function, code)
		self._bind(main_function)
		self.scopes.pop()
		return self.module
	
	def onModuleAnnotation(self, element, data, context):
		ref=self.on(data[1])
		return F.annotation('module', ref.getReferenceName())
	
	def onVersionAnnotation(self, element, data, context):
		return F.annotation('version', self.on(data)[1].group())
	
	def onClass(self, element, data, context):
		variables=element.variables(data)
		name=self.getElements(self.on(variables['name']))
		res=F.createClass(name[0].getName(), name[1:])
		self.scopes.append(res)
		is_abstract=self.on(data[0])
		inherits=self.on(variables['inherits'])
		doc=self.getElements(self.on(variables['documentation']))
		self.on(variables['body'])
		res.setDocumentation((doc and doc[0]))
		res.setAbstract((is_abstract and True))
		self.scopes.pop()
		self._bind(res)
		return res
	
	def onAttribute(self, element, data, context):
		v=element.variables(data)
		name=self.getElements(self.on(v['name']))
		value=self.getElements(self.on(v['value']))
		doc=self.getElements(self.on(v['documentation']))
		res=F._attr(name[0].getReferenceName(), None, (value and value[0]))
		res.setDocumentation((doc and doc[0]))
		self._bind(res)
		return res
	
	def onClassAttribute(self, element, data, context):
		v=element.variables(data)
		name=self.getElements(self.on(v['name']))
		value=self.getElements(self.on(v['value']))
		doc=self.getElements(self.on(v['documentation']))
		res=F._classattr(name[0].getReferenceName(), None, (value and value[0]))
		res.setDocumentation((doc and doc[0]))
		self._bind(res)
		return res
	
	def onModuleAttribute(self, element, data, context):
		data_ref_type=element.resolve('name', data)
		data_value=element.resolve('value', data)
		data_doc=element.resolve('documentation', data)
		value=self._tryGet(self.on(data_value), 1, None)
		ref_type=self.on(data_ref_type)
		res=F._moduleattr(ref_type[0].getReferenceName(), None, value)
		self._bind(res)
		return res
	
	def onCGroup(self, element, data, context):
		data_name=element.resolve('name', data)
		data_methods=(element.resolve('methods', data) or [])
		methods=[]
		group_annotation=F.annotation('as', self.on(data_name).getReferenceName())
		for m in self.on(data_methods):
			m.addAnnotation(group_annotation)
			methods.append(m)
		return methods
	
	def _createCallable(self, factory, element, data, context):
		data_type=element.resolve('type', data)
		data_name=element.resolve('name', data)
		data_params=element.resolve('parameters', data)
		data_doc=element.resolve('documentation', data)
		data_body=element.resolve('body', data)
		name_type=self.on(data_name)
		params=self._tryGet(self.on(data_params), 0, [])
		fun=None
		if name_type:
			fun = factory(name_type[0].getReferenceName(), params)
		elif True:
			fun = factory(params)
		fun.setDocumentation(self.on(data_doc))
		self.scopes.append(fun)
		self._setCode(fun, self.on(data_body))
		self.scopes.pop()
		self._bind(fun)
		return fun
	
	def onOperation(self, element, data, context):
		return self._createCallable(F.createClassMethod, element, data, context)
	
	def onAbstractOperation(self, element, data, context):
		res=self._createCallable(F.createClassMethod, element, data, context)
		res.setAbstract(True)
		return res
	
	def onMethod(self, element, data, context):
		return self._createCallable(F.createMethod, element, data, context)
	
	def onConstructor(self, element, data, context):
		return self._createCallable(F.createConstructor, element, data, context)
	
	def onAbstractMethod(self, element, data, context):
		return self._createCallable(F.createAbstractMethod, element, data, context)
	
	def onFunction(self, element, data, context):
		return self._createCallable(F.createFunction, element, data, context)
	
	def onAbstractFunction(self, element, data, context):
		return self._createCallable(F.createAbstractFunction, element, data, context)
	
	def onClosure(self, element, data, context):
		data_params=element.resolve('params', data)
		data_line=element.resolve('line', data)
		data_body=element.resolve('body', data)
		params=self._tryGet(self.on(data_params), 0, None)
		line=(self.on(data_line) or [])
		body=(self._tryGet(self.on(data_body), 1, None) or [])
		res=F.createClosure(params)
		self._setCode(res, (line + body))
		return res
	
	def onBody(self, element, data, context):
		return self.on(element.resolve('code', data))
	
	def onCode(self, element, data, context):
		res=[]
		value=self.on(data)
		if ((type(value) is list) or (type(value) is tuple)):
			for _ in (self.on(data) or []):
				if ((type(_) is list) or (type(_) is tuple)):
					res = (res + _)
				elif True:
					res.append(_)
		elif True:
			res.append(value)
		return res
	
	def onLine(self, element, data, context):
		data_statements=element.resolve(self.g.symbols.Statements, data)
		data_comment=element.resolve(self.g.symbols.Comment, data)
		statements=self.on(data_statements)
		comment=self.on(data_comment)
		return statements
	
	def onStatements(self, element, data, context):
		model_data=self.on(data)
		statements=([model_data[0]] + (model_data[1] or []))
		res=[]
		for _ in statements:
			if ((type(_) is list) or (type(_) is tuple)):
				res = (res + _)
			elif True:
				res.append(_)
		return res
	
	def onStatement(self, element, data, context):
		"""Returns an `Element` or a list of `[Element]`. Typically these elements
		would be Comments, Blocks or Operations."""
		res=self.on(data)
		return res
	
	def onConditional(self, element, data, context):
		data_if=data[1]
		data_elifs=data[2]
		data_else=data[3]
		_if=self.on(data_if)
		_elifs=(self.on(data_elifs) or [])
		_else=self.on(data_else)
		res=F.select()
		res.addRule(F.matchProcess(_if[0], _if[1]))
		for _ in _elifs:
			res.addRule(F.matchProcess(_[0], _[1]))
		if _else:
			res.addRule(F.matchProcess(F._ref('True'), _else[0]))
		return res
	
	def onIfBranch(self, element, data, context):
		data_condition=data[-2]
		data_body=data[-1]
		block=F.createBlock()
		code=self.on(data_body.data)
		self._setCode(block, code)
		return [self.on(data_condition), block]
	
	def onElifBranch(self, element, data, context):
		data_condition=data[-2]
		data_body=data[-1]
		block=F.createBlock()
		self._setCode(block, self.on(data_body.data))
		return [self.on(data_condition), block]
	
	def onElseBranch(self, element, data, context):
		data_body=data[-1]
		block=F.createBlock()
		self._setCode(block, self.on(data_body.data))
		return [block]
	
	def onIteration(self, element, data, context):
		return self.on(element.resolve('for', data))
	
	def onRepetition(self, element, data, context):
		return self.on(element.resolve('while', data))
	
	def onForBranch(self, element, data, context):
		params=self.on(element.resolve('params', data))
		expr=self.on(element.resolve('expr', data))
		body=self.on(element.resolve('body', data))
		process=F.createClosure(params)
		self._setCode(process, body)
		return F.iterate(expr, process)
	
	def onWhileBranch(self, element, data, context):
		condition=self.on(element.resolve('condition', data))
		body=self.on(element.resolve('body', data))
		process=F.createBlock()
		self._setCode(process, body)
		return F.repeat(condition, process)
	
	def onBlockBody(self, element, data, context):
		return self.on(data[2])
	
	def onBlockLine(self, element, data, context):
		return self.on(data[1])
	
	def onEmbed(self, element, data, context):
		body=self.on(element.resolve('body', data))
		language=element.resolve('language', data).data
		language = 'JavaScript'
		lines=[]
		for line in body:
			lines.append(line[1].group(1))
		return F.embed(language, '\n'.join(lines))
	
	def onExpression(self, element, data, context):
		prefix_suffixes=self.on(data)
		prefix=prefix_suffixes[0]
		suffixes=prefix_suffixes[1]
		current=None
		if ((isinstance(prefix, interfaces.ILiteral) or isinstance(prefix, interfaces.IValue)) or isinstance(prefix, interfaces.IClosure)):
			current = prefix
		elif ((((isinstance(prefix, interfaces.IComputation) or isinstance(prefix, interfaces.IResolution)) or isinstance(prefix, interfaces.IInvocation)) or isinstance(prefix, interfaces.IInstanciation)) or isinstance(prefix, interfaces.IAccessOperation)):
			current = prefix
		elif isinstance(prefix, interfaces.IReference):
			current = F.resolve(prefix)
		elif True:
			ipdb.set_trace()
			raise Exception(('Prefix not supported yet: ' + str(current)))
		current = self._applySuffixes(current, suffixes)
		if isinstance(current, interfaces.IComputation):
			current = self._reorderComputation(current)
		return current
	
	def _reorderComputation(self, value):
		"""Reorders a sequence of computations according to operators priorities"""
		lcomp=value
		rcomp=value.getRightOperand()
		if isinstance(rcomp, interfaces.IComputation):
			op1_p=lcomp.getOperator().getPriority()
			op2_p=rcomp.getOperator().getPriority()
			if (op1_p >= op2_p):
				b=rcomp.getLeftOperand().detach()
				rcomp.detach()
				lcomp.setRightOperand(b)
				rcomp.setLeftOperand(lcomp)
				return rcomp
			elif True:
				return value
		elif True:
			return value
	
	def _applySuffixes(self, value, suffixes):
		"""Applies the suffixes to the current value, modifying it"""
		if suffixes:
			for args in suffixes:
				name=args[0]
				if (name == 'Invocation'):
					if ((type(args[1]) == list) or (type(args[1]) == tuple)):
						value = F.invoke_args(value, args[1])
					elif True:
						value = F.invoke(value, args[1])
				elif (name == 'ComputationInfix'):
					op=self.normalizeOperator(args[1])
					value = F.compute(F._op(op, self.getOperatorPriority(op)), value, args[2])
				elif (name == 'Decomposition'):
					for _ in args[1]:
						value = F.resolve(_, value)
				elif (name == 'Access'):
					value = F.access(value, F._number(args[1]))
				elif (name == 'Slice'):
					value = F.slice(value, args[1], args[2])
				elif True:
					ipdb.set_trace()
					raise Exception(('Suffix not supported yet: ' + str(name)))
		return value
	
	def onExpressionList(self, element, data, context):
		"""Returns a list of expressions [model.Expression]"""
		res=[]
		expr=self.on(data)
		res.append(expr[0])
		for _ in (expr[1] or []):
			res.append(_[1])
		return res
	
	def onExpressionBlock(self, element, data, context):
		"""Returns a list of expressions [model.Expression]"""
		res=[]
		expr=self.on(data)
		for _ in (expr[1] or []):
			res = (res + _[2])
		return res
	
	def onPrefixes(self, element, data, context):
		prefix=self.on(data)
		return prefix
	
	def onComputationPrefix(self, element, data, content):
		operator=self.normalizeOperator(self.on(data[0]).group())
		operand=self.on(data[1])
		return F.compute(F._op(operator, self.getOperatorPriority(operator)), operand)
	
	def onParentheses(self, element, data, content):
		return self.on(data[1])
	
	def onInstanciation(self, element, data, content):
		name=self.on(element.resolve('name', data))
		params=self.on(element.resolve('params', data))[1]
		return F.instanciate(name, *(params or []))
		
	
	def onSuffixes(self, element, data, context):
		"""This rule returns the data AS-IS, without modifying it. This is necessary
		because suffixes need a prefix to be turned into a proper expression."""
		return self.on(data)
	
	def onInvocation(self, element, data, context):
		"""Returns ("Invocation", [args])"""
		arguments_or_litteral=self.on(data)
		args=None
		if isinstance(arguments_or_litteral, interfaces.ILiteral):
			args = [arguments_or_litteral]
		elif True:
			args = arguments_or_litteral
		res = [element.name, (args or [])]
		return res
	
	def onComputationInfix(self, element, data, content):
		"""Returns ("ComputationInfix", OPERATOR:String, Expression)"""
		return [element.name, self.on(data[0]).group(), self.on(data[1])]
	
	def onAccess(self, element, data, context):
		"""Returns [("Access", INDEX:Element)]"""
		data_key=data[1]
		return [element.name, self.on(data_key)]
	
	def onDecomposition(self, element, data, context):
		"""Returns [("Decomposition", [ref:Reference])]"""
		all=[self.on(data[1])]
		for _ in (self.on(data[2]) or []):
			all.append(_[1])
		res=[element.name, all]
		return res
	
	def onSlice(self, element, data, context):
		start_index=self.on(data[1])
		end_index=self.on(data[3])
		return [element.name, start_index, end_index]
	
	def onAllocation(self, element, data, context):
		"""Returns a list of operations. If there's only one operation,
		then it is a single allocation, otherwise it will be a mutliple
		allocation with an automatic variable name."""
		data_target=element.resolve('target', data)
		data_rest=element.resolve('rest', data)
		data_value=element.resolve('value', data)
		value=self._tryGet(self.on(data_value), 1, None)
		rest=self._tryGet(self.on(data_rest), 1, None)
		symbols=self.on(data_target)
		res=None
		if ((len(symbols) == 1) and (not rest)):
			slot=F._slot(symbols[0].getReferenceName())
			res = [F.allocate(slot, value)]
		elif True:
			res = []
			temp_slot=F._slot()
			res.append(F.allocate(temp_slot, value))
			slot_value=F.resolve(F._ref(temp_slot.getName()))
			i=0
			for s in symbols:
				slot=F._slot(s.getReferenceName())
				sub_value=F.access(slot_value.copy(), F._number(i))
				res.append(F.allocate(slot, sub_value))
				i = (i + 1)
			if rest:
				slot=F._slot(rest.getReferenceName())
				sub_value=F.slice(slot_value.copy(), i)
				res.append(F.allocate(slot, sub_value))
		return res
	
	def onAssignment(self, element, data, context):
		data_before=element.resolve('before', data)
		data_main=element.resolve('main', data)
		data_rest=element.resolve('rest', data)
		data_op=element.resolve('op', data)
		lvalue=self.on(data_main)
		op_value=self.on(data_op)
		op=op_value[0].group()
		if (op == '='):
			return F.assign(lvalue, op_value[1])
		elif (op == '?='):
			predicate=F.compute(F._op('not'), lvalue)
			assignment=F.assign(lvalue.copy(), op_value[1])
			match=F.matchExpression(predicate, assignment)
			res=F.select()
			res.addRule(match)
			return res
		elif True:
			res=None
			sub_op=self.normalizeOperator(op[0])
			c=F.compute(F._op(sub_op, self.getOperatorPriority(sub_op)), lvalue, op_value[1])
			return F.assign(lvalue.copy().detach(), c)
	
	def onAssignable(self, element, data, context):
		data_lvalue=data[0]
		data_suffixes=data[1]
		lvalue=self.on(data_lvalue)
		suffixes=self.on(data_suffixes)
		return self._applySuffixes(lvalue, suffixes)
	
	def onIterationLine(self, element, data, context):
		data_lvalue=data[0]
		data_closure=data[2]
		lvalue=self.on(data_lvalue)
		closure=self.on(data_closure)
		return F.iterate(lvalue, closure)
	
	def onTermination(self, element, data, context):
		data_value=data[1]
		value=self.on(data[1])
		return F.returns(value)
	
	def onParameter(self, element, data, context):
		data_name=element.resolve('name', data)
		data_value=element.resolve('value', data)
		name_type=self.on(data_name)
		value=self._tryGet(self.on(data_value), 1, None)
		return F._param(name_type[0].getReferenceName(), None, value)
	
	def onParameterList(self, element, data, context):
		res=[]
		all=self.on(data)
		res.append(all[0])
		for _ in (all[1] or []):
			res.append(_[1])
		return res
	
	def onArgumentsEmpty(self, element, data, context):
		return []
	
	def onArgumentsMany(self, element, data, context):
		return self.on(data[1])
	
	def onSymbolList(self, element, data, context):
		"""Returns `[model.Reference]`"""
		res=[]
		symbols=self.on(data)
		res.append(symbols[0])
		for _ in (symbols[1] or []):
			res.append(_[1])
		ellispis=symbols[-1]
		assert((not ellispis))
		return res
	
	def onNameType(self, element, data, context):
		"""Returns a couple (name, type) where type might be None."""
		name=data[0]
		type=data[1]
		return [self.on(name), self.on(type)]
	
	def onFQName(self, element, data, context):
		"""A fully qualified name that will return an absolute reference"""
		res=[]
		all=self.on(data)
		res.append(all[0].getReferenceName())
		for _ in (all[1] or []):
			res.append(_[1].getReferenceName())
		full_name='.'.join(res)
		return F._absref(full_name)
	
	def onArray(self, element, data, context):
		data_list=element.resolve(self.g.symbols.ExpressionList, data)
		data_block=element.resolve(self.g.symbols.ExpressionBlock, data)
		elements=((self.on(data_list) or []) + (self.on(data_block) or []))
		return F._list(elements)
	
	def onMap(self, element, data, context):
		res=F._dict()
		data_list=element.resolve(self.g.symbols.KeyValueList, data)
		data_block=element.resolve(self.g.symbols.KeyValueBlock, data)
		elements=((self.on(data_list) or []) + (self.on(data_block) or []))
		for _ in elements:
			if _:
				res.setValue(_[0], _[1])
		return res
	
	def onKeyValueList(self, element, data, context):
		res=[]
		expr=self.on(data)
		res.append(expr[0])
		for _ in (expr[1] or []):
			res.append(_[1])
		return res
	
	def onKeyValueBlock(self, element, data, context):
		res=[]
		expr=self.on(data)
		res.append(expr[0])
		for _ in (expr[1] or []):
			res = (res + _[2])
		return res
	
	def onKeyValue(self, element, data, context):
		key=element.resolve(self.g.symbols.Key, data)
		value=element.resolve(self.g.symbols.Expression, data)
		return [self.on(key), self.on(value)]
	
	def onKey(self, element, data, context):
		res=self.on(data)
		if isinstance(res, interfaces.IElement):
			return res
		elif True:
			return res[1]
	
	def onString(self, element, data, context):
		raw_string=self.on(data).group()
		decoded_string=eval(raw_string)
		return F._string(decoded_string)
	
	def onNUMBER(self, element, data, context):
		raw_number=self.on(data).group()
		decoded_number=eval(raw_number)
		return F._number(decoded_number)
	
	def onSYMBOLIC(self, element, data, context):
		raw_symbol=self.on(data).group()
		if (raw_symbol == 'Undefined'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == 'None'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == 'Nothing'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == 'Timeout'):
			return F._symbol(raw_symbol)
		elif True:
			raise Exception(('Unknown symbol:' + raw_symbol()))
	
	def onNAME(self, element, data, context):
		return F._ref(data.group(2))
	
	def onKEY(self, element, data, context):
		return F._string(data.group())
	
	def onDocumentation(self, element, data, context):
		res=[]
		for line in self._onlyWithValue(self.flatten(self.on(data))):
			res.append(line.group()[1:].strip())
		return F.doc('\n'.join(res))
	
	def onRepeat(self, element, data, context):
		"""Converts the given repeat to None, the result (if the repeat is optional),
		or an array (zero or more)"""
		result=self._onlyWithValue(self.on(data))
		if result:
			if element.isOptional():
				return result[0]
			elif True:
				return result
		elif True:
			return None
	
	def onCheckIndent(self, element, data, context):
		return None
	
	def onEOL(self, element, data, context):
		return None
	

class SugarCommand(Command):
	def setupEnvironment(self):
		python_plugin=self.environment.loadLanguage('python')
		javascript_plugin=self.environment.loadLanguage('javascript')
		actionscript_plugin=self.environment.loadLanguage('actionscript')
		pnuts_plugin=self.environment.loadLanguage('pnuts')
		python_plugin.addRecognizedExtension('spy')
		javascript_plugin.addRecognizedExtension('sjs')
		actionscript_plugin.addRecognizedExtension('sas')
		pnuts_plugin.addRecognizedExtension('spnuts')
		pnuts_plugin.addRecognizedExtension('spnut')
		self.environment.addParser(Parser(self), 'sg spy sjs sjava spnuts sas'.split())
	

class Parser:
	G = createProgramGrammar(parsing.Grammar('Sugar'))
	def __init__ (self, environment):
		self.environment = None
		self.environment = environment
	
	def parseString(self, text, path, moduleName):
		tokens=self.__class__.G.parse(text)
		builder=LambdaFactoryBuilder(path)
		module=builder.build(tokens, self.__class__.G)
		return [text, module]
	

def run (arguments):
	self=__module__
	command=SugarCommand('sugar')
	command.run((arguments or ['--help']))


def __module_init__():
	if __name__ == "__main__":
		import sys
		run(sys.argv[1:])
	
__module_init__()
