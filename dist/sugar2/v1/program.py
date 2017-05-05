#8< ---[sugar2/v1/program.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
from sugar2.helpers import doIndent, doCheckIndent, doDedent, doBlockStart, doBlockLastSetLine, doBlockLastSetBody, doBlockLastIsLine
import libparsing
__module_name__ = 'sugar2.v1.program'
G = None
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
		return g.rule(name, s.CheckIndent, prefix._as('type'), s.NOTHING._as('name'), g.agroup(s.EOL, g.arule(s.ParameterList.optional(), s.EOL))._as('parameters'), s.Decorator.zeroOrMore()._as('decorators'), s.Documentation.optional()._as('documentation'), s.Body._as('body'), s.OEnd)
	elif True:
		return g.rule(name, s.CheckIndent, prefix._as('type'), s.NameType._as('name'), g.agroup(s.EOL, g.arule(s.ParameterList.optional(), s.EOL))._as('parameters'), s.Decorator.zeroOrMore()._as('decorators'), s.Documentation.optional()._as('documentation'), s.Body._as('body'), s.OEnd)


def abstractFunction (grammar, name, prefix):
	self=__module__
	g=grammar
	s=grammar.symbols
	return g.rule(name, s.CheckIndent, s.oabstract, prefix._as('type'), s.NameType._as('name'), g.agroup(s.EOL, g.arule(s.ParameterList.optional(), s.EOL))._as('parameters'), s.Decorator.zeroOrMore()._as('decorators'), s.Documentation.optional()._as('documentation'))


def listOf (rule, separator, grammar):
	""" Creates a new list of the given rule, separated by the given separator
	 in the given grammar"""
	self=__module__
	return grammar.arule(grammar.arule(rule, separator).zeroOrMore(), rule)


def createProgramGrammar (g=None):
	self=__module__
	if g is None: g = libparsing.Grammar('Sugar')
	s=g.symbols
	g.token('SPACE', '[ ]+')
	g.token('TABS', '\t*')
	g.token('EMPTY_LINES', '([ \t]*\n)+')
	g.token('COMMENT', '[ \t]*\\#[^\n]*')
	g.token('EOL', '[ ]*\n(\\s*\n)*')
	g.token('NUMBER', '\\-?(([0-9]+(\\.[0-9]+)?)|(0x[A-Fa-f0-9]+)|(0b[01]+)|(0o[0-8]+))')
	g.token('FLOAT', '\\-?[0-9]+(\\.[0-9]+)?')
	g.token('TIME', '[0-9]+(\\.[0-9]+)?(ms|s|m|h|d|w)')
	g.token('NAME', '(\\\\?)([\\$_A-Za-z][_\\w]*)')
	g.token('FQNAME', '(\\\\?)([\\$_A-Za-z][\\._\\w]*)')
	g.token('KEY', '[\\$_\\-A-Za-z][_\\-\\w]*')
	g.token('INFIX_OPERATOR', '([\\-\\+\\*\\/\\%]|\\<=|\\>=|\\<\\<?|\\>\\>?|==|\\!=|\\.\\.|\xe2\x80\xa5|\\|\\||&&|not\\s+in\\s+|in\\s+|and\\s+|or\\s+|is\\s+not\\s+|is\\s+|\\*\\*)')
	g.token('PREFIX_OPERATOR', '(not\\s+|\\-)')
	g.token('NEW_OPERATOR', 'new\\s+')
	g.token('THROW_OPERATOR', 'raise|throw')
	g.token('ASSIGN_OPERATOR', '[\\?\\*\\+\\-\\/\\%]?=')
	g.token('SYMBOLIC', 'None|Undefined|Nothing|Timeout')
	g.token('STRING_SQ', "'(\\\\'|[^'\\n])*'")
	g.token('STRING_DQ', '"(\\\\"|[^"\\n])*"')
	g.token('DOCSTRING', '\\|[^\n]*')
	g.token('EMBED_LINE', '\\|([^\n]*)')
	g.token('VERSION', '[0-9]+(\\.[0-9]+)?(\\.[0-9]+)?[a-zA-Z_]*')
	g.token('DOT_OR_SPACE', '\\.|[ \t]+')
	g.token('ITERATOR', '::[\\?=\\<\\>]?')
	g.token('ELLIPSIS', '\\.\\.\\.|\xe2\x80\xa5')
	g.token('ARROW', '\\-\\>|\xe2\x86\x92')
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
	g.word('STAR', '*')
	g.condition('NOTHING')
	g.word('_var', 'var')
	g.word('_let', 'let')
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
	g.word('_finally', 'finally')
	g.word('oabstract', '@abstract')
	g.word('oimport', '@import')
	g.word('omodule', '@module')
	g.word('oversion', '@version')
	g.word('ofunction', '@function')
	g.word('oclass', '@class')
	g.word('oprotocol', '@protocol')
	g.word('oproperty', '@property')
	g.word('oshared', '@shared')
	g.word('ooperation', '@operation')
	g.word('oconstructor', '@constructor')
	g.word('omethod', '@method')
	g.word('ogroup', '@group')
	g.word('oend', '@end')
	g.word('oembed', '@embed')
	g.word('owhen', '@when')
	g.procedure('Indent', doIndent)
	g.procedure('Dedent', doDedent)
	g.rule('CheckIndent', s.TABS._as('tabs'), g.acondition(doCheckIndent))
	g.rule('Comment', s.COMMENT._as('text'), s.EOL)
	g.rule('EmptyLines', s.EMPTY_LINES)
	g.rule('DocumentationLine', s.CheckIndent, s.DOCSTRING, s.EOL)
	g.rule('Documentation', s.DocumentationLine.oneOrMore())
	g.group('String', s.STRING_SQ, s.STRING_DQ)
	g.rule('Expression')
	g.group('Number', s.TIME, s.NUMBER)
	g.group('Key', s.KEY, s.Number, s.String, g.arule(s.LP, s.Expression, s.RP))
	g.rule('KeyValue', s.Key, s.COLON, s.Expression)
	g.rule('ImplicitKey', s.KEY)
	g.group('Entry', s.KeyValue, s.ImplicitKey)
	g.rule('EntryList', s.Entry, g.arule(s.COMMA, s.Entry).zeroOrMore())
	g.rule('ExpressionList', s.Expression, g.arule(s.COMMA, s.Expression).zeroOrMore())
	g.rule('ExpressionBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.ExpressionList).oneOrMore(), s.Dedent)
	g.rule('EntryBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.EntryList).oneOrMore(), s.Dedent)
	g.rule('Array', s.LSB, s.ExpressionList.optional()._as('head'), s.ExpressionBlock.optional()._as('tail'), g.arule(s.EOL, s.CheckIndent).optional(), s.RSB)
	g.rule('Map', s.LB, s.EntryList.optional()._as('head'), s.EntryBlock.optional()._as('tail'), g.arule(s.EOL, s.CheckIndent).optional(), s.RB)
	g.rule('TypeStructure', g.atoken('\\<[^\\>]*\\>'))
	g.rule('Type', g.agroup(s.NAME, s.TypeStructure))
	g.rule('NameType', s.NAME, g.arule(s.COLON, s.Type).optional())
	g.rule('FQName', s.NAME, g.arule(s.DOT_OR_SPACE, s.NAME).zeroOrMore())
	g.rule('Parameter', s.NameType._as('name'), g.arule(s.EQUALS, s.Expression).optional()._as('value'))
	g.rule('ParameterList', s.Parameter, g.arule(s.COMMA, s.Parameter).zeroOrMore(), s.ELLIPSIS.optional())
	g.rule('SymbolList', s.NAME, g.arule(s.COMMA, s.NAME).zeroOrMore(), s.ELLIPSIS.optional())
	g.rule('ArgumentsEmpty', s.LP, s.RP)
	g.rule('ArgumentsMany', s.LP, s.ExpressionList.optional()._as('line'), s.ExpressionBlock.optional()._as('body'), g.agroup(s.RP, g.arule(s.EOL.optional(), s.CheckIndent, s.RP)))
	g.rule('ClosureStatement')
	g.rule('ClosureLine', s.EOL, s.CheckIndent, g.agroup(s.COMMENT, s.ClosureStatement))
	g.rule('ClosureParameters', s.ParameterList.optional(), s.PIPE)
	g.rule('EmptyClosure', s.LB, s.ClosureParameters, s.RB)
	g.rule('InlineClosure', s.LB, s.ClosureParameters.optional(), s.ClosureStatement, s.RB)
	g.rule('BlockClosure', s.LB, s.ClosureParameters.optional(), s.Indent, s.ClosureLine.zeroOrMore(), s.EOL, s.Dedent, s.CheckIndent, s.RB)
	g.group('Closure', s.BlockClosure, s.InlineClosure, s.EmptyClosure)
	g.group('Literal', s.Number, s.SYMBOLIC, s.String, s.Array, s.Map, s.Closure)
	g.rule('Reference', s.NAME, g.arule(s.DOT, s.NAME).zeroOrMore())
	g.rule('Decomposition', s.DOT_OR_SPACE, s.Reference)
	g.rule('ComputationInfix', s.INFIX_OPERATOR, s.Expression)
	g.rule('Access', s.LSB, s.Expression, s.RSB)
	g.rule('Slice', s.LSB, s.Expression.optional(), s.COLON, s.Expression.optional(), s.RSB)
	g.group('Invocation', s.Literal, s.ArgumentsEmpty, s.ArgumentsMany)
	g.rule('Parentheses', s.LP, s.Expression, s.RP)
	g.group('Suffixes')
	g.rule('ChainLine', s.EOL, s.Indent, s.CheckIndent, g.agroup(s.COMMENT, s.Reference, s.Suffixes).oneOrMore(), s.Dedent)
	g.rule('Chain', s.COLON, s.ChainLine.oneOrMore())
	g.rule('ConditionalExpression', s._if, s.Expression._as('condition'), s.ARROW, s.Expression._as('true'), s.PIPE, s.Expression._as('false'))
	g.rule('IterationSuffix', s.ITERATOR._as('op'), s.Expression._as('rvalue'))
	g.group('Prefixes', s.Literal, g.rule('Exception', s.THROW_OPERATOR, s.SPACE, s.Expression._as('expression')), g.rule('Instanciation', s.NEW_OPERATOR, g.agroup(s.FQName, s.Parentheses)._as('target'), s.Invocation._as('params')), g.rule('ComputationPrefix', s.PREFIX_OPERATOR, s.Expression), s.ConditionalExpression, s.NAME, s.Parentheses)
	s.Suffixes.set(s.Chain, s.IterationSuffix, s.ComputationInfix, s.Decomposition, s.Access, s.Slice, s.Invocation)
	s.Expression.set(s.Prefixes, s.Suffixes.zeroOrMore())
	g.rule('Assignable', s.NAME, g.agroup(s.Decomposition, s.Access, s.Slice, s.Invocation).zeroOrMore())
	g.rule('Allocation', g.agroup(s._var, s._let), s.SPACE, s.SymbolList._as('symbols'), g.arule(s.PIPE, s.NAME).optional()._as('rest'), g.arule(s.EQUALS, s.Expression).optional()._as('value'))
	g.rule('Assignment', g.arule(s.Assignable, s.COMMA).zeroOrMore()._as('before'), s.Assignable._as('main'), g.arule(s.PIPE, s.Assignable).optional()._as('rest'), g.arule(s.ASSIGN_OPERATOR, s.Expression)._as('op'))
	g.rule('Termination', g.aword('return'), s.Expression.optional())
	g.rule('Break', g.aword('break'))
	g.rule('Pass', g.aword('pass'))
	g.rule('Continue', g.aword('continue'))
	g.group('Block')
	g.group('Code')
	g.group('Statement', s.Comment, s.Block, s.Allocation, s.Assignment, s.Termination, s.Break, s.Continue, s.Pass, s.Expression)
	g.rule('Statements', s.Statement, g.arule(s.SEMICOLON, s.Statement).zeroOrMore())
	g.rule('Line', s.CheckIndent, s.Statements.optional(), s.COMMENT.optional(), s.EOL)
	g.procedure('BlockStart', doBlockStart)
	g.rule('BlockLine', s.ARROW, s.Statements._as('body'), s.COMMENT.optional())
	g.rule('BlockBody', s.EOL, s.Indent, s.Code.zeroOrMore()._as('body'), s.Dedent)
	g.group('BlockEnd', g.arule(s.CheckIndent, s._end))
	g.rule('IfLine', s._if, s.Expression._as('condition'), g.agroup(s.BlockLine)._as('body'))
	g.rule('ElifLine', s.EOL, s.CheckIndent, s._elif, s.Expression._as('condition'), g.agroup(s.BlockLine)._as('body'))
	g.rule('ElseLine', s.EOL, s.CheckIndent, s._else, g.agroup(s.BlockLine)._as('body'))
	g.rule('IfBlock', s._if, s.Expression._as('condition'), g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('ElifBlock', s.CheckIndent, s._elif, s.Expression._as('condition'), g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('ElseBlock', s.CheckIndent, s._else, g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('WhileBlock', s._while, s.Expression._as('condition'), g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('TryBlock', s._try, g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('FinallyBlock', s.CheckIndent, s._finally, g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('CatchBlock', s.CheckIndent, s._catch, s.NameType.optional()._as('param'), g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('ForBlock', s._for, s.ParameterList._as('params'), s._in, s.Expression._as('expr'), g.agroup(s.BlockBody, s.BlockLine)._as('body'))
	g.rule('ConditionalLine', s.IfLine._as('if'), s.ElifLine.zeroOrMore()._as('elif'), s.ElseLine.optional()._as('else'))
	g.rule('ConditionalBlock', s.BlockStart, s.IfBlock._as('if'), s.ElifBlock.zeroOrMore()._as('elif'), s.ElseBlock.optional()._as('else'), s.BlockEnd)
	g.group('Conditional', s.ConditionalLine, s.ConditionalBlock)
	g.rule('Try', s.BlockStart, s.TryBlock._as('try'), s.CatchBlock.optional()._as('catch'), s.FinallyBlock.optional()._as('finally'), s.BlockEnd)
	g.rule('Repetition', s.BlockStart, s.WhileBlock._as('while'), s.BlockEnd)
	g.rule('Iteration', s.BlockStart, s.ForBlock._as('for'), s.BlockEnd)
	s.Block.set(s.Conditional, s.Repetition, s.Iteration, s.Try)
	s.Code.set(s.Comment, s.Block, s.Line)
	g.rule('OEnd', s.CheckIndent, s.oend, s.EOL)
	g.rule('Body', s.Indent, s.Code.zeroOrMore()._as('code'), s.Dedent)
	g.rule('OWhen', s.CheckIndent, s.owhen, s.Expression._as('expression'), s.EOL)
	g.group('Decorator', s.OWhen)
	s.ClosureStatement.set(s.Statements)
	declaration(g, 'ClassAttribute', s.oshared)
	declaration(g, 'ModuleAttribute', s.oshared)
	declaration(g, 'Attribute', s.oproperty)
	abstractFunction(g, 'AbstractMethod', s.omethod)
	abstractFunction(g, 'AbstractClassMethod', s.ooperation)
	function(g, 'Function', s.ofunction)
	function(g, 'Constructor', s.oconstructor, True)
	function(g, 'Method', s.omethod)
	function(g, 'ClassMethod', s.ooperation)
	g.rule('CGroup')
	g.group('Methods', s.ClassMethod, s.AbstractClassMethod, s.Method, s.AbstractMethod, s.AbstractMethod, s.CGroup, s.Comment)
	s.CGroup.set(s.CheckIndent, s.ogroup, s.NAME._as('name'), s.EOL, s.Documentation.optional(), s.Indent, s.Methods.zeroOrMore()._as('methods'), s.Dedent, s.OEnd)
	g.rule('EmbedLine', s.CheckIndent, s.EMBED_LINE, s.EOL)
	g.rule('Embed', s.oembed, s.SPACE, s.NAME.optional()._as('language'), s.EOL, s.EmbedLine.zeroOrMore()._as('body'), g.arule(s.CheckIndent, s.oend))
	s.Block.add(s.Embed)
	g.rule('Class', s.oabstract.optional(), s.oclass, s.NAME._as('name'), g.arule(s.COLON, listOf(s.FQName, s.COMMA, g)).optional()._as('inherits'), s.EOL, s.Documentation.optional()._as('documentation'), s.Indent, g.agroup(s.ClassAttribute, s.Attribute, s.ClassMethod, s.AbstractMethod, s.Constructor, s.Methods).zeroOrMore()._as('body'), s.Dedent, g.aword('@end'))
	g.rule('Interface', s.oprotocol, s.NAME._as('name'), g.arule(s.COLON, listOf(s.FQName, s.COMMA, g)).optional()._as('inherits'), s.EOL, s.Documentation.optional()._as('documentation'), s.Indent, g.agroup(s.ClassAttribute, s.Attribute, s.ClassMethod, s.AbstractMethod, s.Constructor, s.Methods).zeroOrMore()._as('body'), s.Dedent, g.aword('@end'))
	g.rule('ModuleAnnotation', s.omodule, s.FQName, s.EOL)
	g.rule('VersionAnnotation', s.oversion, s.VERSION, s.EOL)
	g.rule('ImportAlias', s._as, s.NAME)
	g.rule('ImportSymbol', g.agroup(s.FQNAME, s.STAR), s.ImportAlias.optional())
	g.rule('ImportOrigin', s._from, s.FQNAME)
	g.rule('Import', s.oimport, s.ImportSymbol, g.arule(s.COMMA, s.ImportSymbol).zeroOrMore(), s.ImportOrigin.optional(), s.EOL)
	g.rule('ModuleDeclaration', s.EmptyLines.zeroOrMore(), s.Comment.zeroOrMore()._as('comments'), s.ModuleAnnotation.optional()._as('module'), s.VersionAnnotation.optional()._as('version'), s.Documentation.optional()._as('documentation'), s.Import.zeroOrMore()._as('imports'))
	g.group('Structure', s.EmptyLines, s.Comment, s.ModuleAttribute, s.Function, s.Class, s.Interface)
	g.rule('Module', s.ModuleDeclaration, s.Structure.zeroOrMore(), s.Code.zeroOrMore())
	g.skip = g.agroup(s.SPACE)
	g.axiom = s.Module
	return g


