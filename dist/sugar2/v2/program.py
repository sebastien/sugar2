#8< ---[sugar2/v2/program.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
from sugar2.helpers import doIndent, doCheckIndent, doDedent, doBlockStart, doBlockEnd, listOf
from sugar2.v2.types import injectTypes
import libparsing
__module_name__ = 'sugar2.v2.program'
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
		return g.rule(name, s.CheckIndent, prefix._as('type'), s.NOTHING._as('name'), g.agroup(s.EOL, g.arule(s.ParameterList.optional(), s.EOL))._as('parameters'), s.Decorator.zeroOrMore()._as('decorators'), s.Documentation.optional()._as('documentation'), s.Body._as('body'), s.ConstructSuffixes.zeroOrMore()._as('suffixes'))
	elif True:
		return g.rule(name, s.CheckIndent, prefix._as('type'), s.NameType._as('name'), g.agroup(s.EOL, g.arule(s.ParameterList.optional(), s.EOL))._as('parameters'), s.Decorator.zeroOrMore()._as('decorators'), s.Documentation.optional()._as('documentation'), s.Body._as('body'), s.ConstructSuffixes.zeroOrMore()._as('suffixes'))


def abstractFunction (grammar, name, prefix):
	self=__module__
	g=grammar
	s=grammar.symbols
	return g.rule(name, s.CheckIndent, s.oabstract, prefix._as('type'), s.NameType._as('name'), g.agroup(s.EOL, g.arule(s.ParameterList.optional(), s.EOL))._as('parameters'), s.Decorator.zeroOrMore()._as('decorators'), s.Documentation.optional()._as('documentation'), s.ConstructSuffixes.zeroOrMore()._as('suffixes'))


def construct (grammar, name, tag, contents):
	self=__module__
	g=grammar
	s=grammar.symbols
	return g.rule(name, s.CheckIndent, s.oabstract.optional(), tag, s.NAME._as('name'), s.Parents.optional()._as('inherits'), s.EOL, s.Documentation.optional()._as('documentation'), s.Indent, contents.zeroOrMore()._as('body'), s.Dedent, s.ConstructSuffixes.zeroOrMore()._as('suffixes'))


def createProgramGrammar (g=None):
	self=__module__
	if g is None: g = libparsing.Grammar('Sugar', False)
	s=g.symbols
	g.token('SPACE', '[ ]+')
	g.token('TABS', '\t*')
	g.token('EMPTY_LINES', '([ \t]*\n)+')
	g.token('COMMENT', '[ \t]*\\#[^\n]*')
	g.token('EOL', '[ ]*\n(\\s*\n)*')
	g.token('ANY', '[^\n]*')
	g.token('NUMBER', '(0x[A-Fa-f0-9]+)|(0b[01]+)|(0o[0-8]+)|([0-9]+(\\.[0-9]+)?)')
	g.token('NUMBER_UNIT', '[0-9]+(\\.[0-9]+)?(ms|s|m|h|d|w|deg)')
	g.token('NAME', '(\\\\?)([\\$_A-Za-z][_\\w]*)')
	g.token('VALUE', '[\\w\\d_\\-\\+\\*\\-]+')
	g.token('FQNAME', '(\\\\?)([\\$_A-Za-z][\\._\\w]*)')
	g.token('KEY', '[\\$_\\-A-Za-z][_\\-\\w]*')
	g.token('INFIX_OPERATOR', '([\\-\\+\\*\\/\\%]|\\<=|\\>=|\\<\\<?|\\>\\>?|==|\\!=|\\.\\.|\xe2\x80\xa5|\\|\\||&&|\\||not\\s+in\\s+|in\\s+|and\\s+|or\\s+|is\\s+not\\s+|is\\s+|\\*\\*)')
	g.token('PREFIX_OPERATOR', '(not\\s+|\\-)')
	g.token('NEW_OPERATOR', 'new\\s+')
	g.token('THROW_OPERATOR', '(raise|throw)\\s+')
	g.token('ASSIGN_OPERATOR', '[\\?\\*\\+\\-\\/\\%]?=')
	g.token('EVENT_OPERATOR', '\\![\\+\\-]?')
	g.token('SYMBOLIC', 'None|Undefined|Nothing|Timeout')
	g.token('STRING_SQ', "'(\\\\'|[^'\\n])*'")
	g.token('STRING_DQ', '"(\\\\"|[^"\\n])*"')
	g.token('STRING_MQ', '"""(.+)"""')
	g.token('STRING_MQ_START', '"""(.*)\n')
	g.token('STRING_MQ_END', '(.*)"""')
	g.token('STRING_MQ_LINE', '[^"\n]*("[^"\n]|""[^"\n])*[^"\n]*')
	g.token('DOCSTRING', '\\|[^\n]*')
	g.token('EMBED_LINE', '([^\n]*)')
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
	g.word('UNDERSCORE', '_')
	g.word('PIPE', '|')
	g.word('EQUALS', '=')
	g.word('TILDE', '~')
	g.word('BANG', '!')
	g.condition('NOTHING')
	g.word('_var', 'var')
	g.word('_let', 'let')
	g.word('_if', 'if')
	g.word('_elif', 'elif')
	g.word('_else', 'else')
	g.word('_for', 'for')
	g.word('_while', 'while')
	g.word('_in', 'in')
	g.word('_from', 'from')
	g.word('_as', 'as')
	g.word('_try', 'try')
	g.word('_catch', 'catch')
	g.word('_finally', 'finally')
	g.word('_match', 'match')
	g.word('_type', 'is?')
	g.word('oabstract', '@abstract')
	g.word('oimport', '@import')
	g.word('otarget', '@target')
	g.word('ofeature', '@feature')
	g.word('omodule', '@module')
	g.word('oversion', '@version')
	g.word('ofunction', '@function')
	g.word('oclass', '@class')
	g.word('otrait', '@trait')
	g.word('osingleton', '@singleton')
	g.word('oevent', '@event')
	g.word('oproperty', '@property')
	g.word('ogetter', '@getter')
	g.word('osetter', '@setter')
	g.word('oshared', '@shared')
	g.word('ooperation', '@operation')
	g.word('oconstructor', '@constructor')
	g.word('omethod', '@method')
	g.word('ogroup', '@group')
	g.word('oend', '@end')
	g.word('oembed', '@embed')
	g.word('owhen', '@when')
	g.word('owhere', '@where')
	g.word('oexample', '@example')
	g.procedure('Indent', doIndent)
	g.procedure('Dedent', doDedent)
	g.rule('CheckIndent', s.TABS._as('tabs'), g.acondition(doCheckIndent))
	g.rule('Comment', s.COMMENT._as('text'), s.EOL)
	g.rule('EmptyLines', s.EMPTY_LINES)
	g.rule('DocumentationLine', s.CheckIndent, s.DOCSTRING, s.EOL)
	g.rule('Documentation', s.DocumentationLine.oneOrMore())
	g.rule('StringLine', s.CheckIndent, s.STRING_MQ_LINE._as('text'), s.EOL)
	g.rule('StringMultiEnd', s.CheckIndent, s.STRING_MQ_END)
	g.rule('StringMulti', s.STRING_MQ_START, s.StringLine.zeroOrMore()._as('lines'), s.StringMultiEnd)
	g.group('String', s.STRING_MQ, s.StringMulti, s.STRING_SQ, s.STRING_DQ)
	g.rule('Expression')
	g.group('Number', s.NUMBER_UNIT, s.NUMBER)
	g.group('Key', s.KEY, s.Number, s.String, g.arule(s.LP, s.Expression, s.RP))
	g.rule('KeyValue', s.Key, s.COLON, s.Expression)
	g.rule('ImplicitKey', s.KEY)
	g.group('Entry', s.KeyValue, s.ImplicitKey)
	g.rule('EntryList', s.Entry, g.arule(s.COMMA, s.Entry).zeroOrMore(), s.COMMENT.optional())
	g.group('EntryLine', s.EntryList, s.COMMENT)
	g.rule('ExpressionList', s.Expression, g.arule(s.COMMA, s.Expression).zeroOrMore(), s.COMMENT.optional())
	g.group('ExpressionLine', s.ExpressionList, s.COMMENT)
	g.rule('ExpressionBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.ExpressionLine).oneOrMore()._as('content'), s.Dedent)
	g.rule('NamedExpression', g.arule(s.NAME, s.COLON).optional()._as('name'), s.Expression._as('value'))
	g.rule('RestExpression', s.ELLIPSIS, s.Expression._as('value'))
	g.group('NamedEntry', s.Expression, s.NamedExpression, s.RestExpression)
	g.rule('NamedExpressionList', s.NamedEntry, g.arule(s.COMMA, s.NamedEntry).zeroOrMore(), s.COMMA.optional()._as('comma'), s.COMMENT.optional())
	g.group('NamedExpressionLine', s.NamedExpressionList, s.COMMENT)
	g.rule('NamedExpressionBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.NamedExpressionLine).oneOrMore()._as('content'), s.Dedent)
	g.rule('EntryBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.EntryLine).oneOrMore()._as('content'), s.Dedent)
	g.rule('Array', s.LSB, s.ExpressionList.optional()._as('head'), s.ExpressionBlock.optional()._as('tail'), g.arule(s.EOL, s.CheckIndent).optional(), s.RSB)
	g.rule('Tuple', s.LP, s.NamedExpressionList.optional()._as('head'), s.NamedExpressionBlock.optional()._as('tail'), g.arule(s.EOL, s.CheckIndent).optional(), s.RP)
	g.rule('Map', s.LB, s.EntryList.optional()._as('head'), s.EntryBlock.optional()._as('tail'), g.arule(s.EOL, s.CheckIndent).optional(), s.RB)
	injectTypes(g)
	g.rule('NameType', s.NAME, g.arule(s.COLON, s.TypeValue).optional())
	g.rule('FQName', s.NAME, g.arule(s.DOT_OR_SPACE, s.NAME).zeroOrMore())
	g.rule('Parameter', s.NameType._as('name'), g.arule(s.EQUALS, s.Expression).optional()._as('value'))
	g.rule('ParameterList', s.Parameter, g.arule(s.COMMA, s.Parameter).zeroOrMore(), s.ELLIPSIS.optional())
	g.rule('SymbolList', s.NameType._as('name'), g.arule(s.COMMA, s.NameType).zeroOrMore(), s.ELLIPSIS.optional())
	g.rule('ArgumentsEmpty', s.LP, s.RP)
	g.group('ClosureStatement')
	g.group('ClosureBody')
	g.rule('ClosureParameters', s.ParameterList.optional(), s.PIPE)
	g.rule('EmptyClosure', s.LB, s.ClosureParameters, s.RB)
	g.rule('InlineClosure', s.LB, s.ClosureParameters.optional()._as('params'), s.ClosureStatement._as('body'), s.RB)
	g.rule('BlockClosure', s.LB, s.ClosureParameters.optional()._as('params'), s.ClosureBody._as('body'), s.CheckIndent, s.RB)
	g.group('Closure', s.BlockClosure, s.InlineClosure, s.EmptyClosure)
	g.group('Literal', s.Number, s.SYMBOLIC, s.String, s.Array, s.Tuple, s.Map, s.Closure)
	g.rule('Reference', s.NAME, g.arule(s.DOT, s.NAME).zeroOrMore())
	g.rule('Decomposition', s.DOT_OR_SPACE, s.Reference)
	g.rule('ComputationInfix', s.INFIX_OPERATOR, s.Expression)
	g.rule('Access', s.LSB, s.Expression, s.RSB)
	g.rule('Slice', s.LSB, s.Expression.optional(), s.COLON, s.Expression.optional(), s.RSB)
	g.group('Arguments', s.Literal, s.ArgumentsEmpty)
	g.group('Invocation', s.Arguments)
	g.rule('InfixInvocation', s.TILDE, s.NAME._as('name'), s.Expression._as('rvalue'))
	g.rule('Parentheses', s.LP, s.Expression, s.RP)
	g.group('Suffixes')
	g.rule('ChainLine', s.EOL, s.Indent, s.CheckIndent, g.agroup(s.COMMENT, s.Reference, s.Suffixes).oneOrMore()._as('content'), s.Dedent)
	g.rule('Chain', g.agroup(s.ELLIPSIS, s.COLON)._as('type'), s.ChainLine.oneOrMore()._as('lines'))
	g.rule('IterationSuffix', s.ITERATOR._as('op'), s.Expression._as('rvalue'))
	g.rule('ConditionSuffix', g.agroup(s._if, s._else)._as('type'), s.SPACE, s.Expression._as('value'))
	g.rule('EventOperation', s.EVENT_OPERATOR._as('operator'), g.agroup(s.Reference, s.String)._as('name'), s.Arguments.optional()._as('value'))
	g.rule('TypeSuffix', s._type, s.TypeValue._as('type'))
	g.rule('MatchSuffixLine', s.ARROW, s.Expression._as('body'))
	g.rule('MatchSuffixBlock', s.EOL, s.Comment.zeroOrMore(), s.Indent, s.CheckIndent, s.Expression._as('body'), s.COMMENT.optional(), s.Dedent)
	g.rule('MatchSuffixBranch', s.EOL, s.Comment.zeroOrMore(), s.CheckIndent, g.agroup(s._else, s.UNDERSCORE, s.Suffixes.oneOrMore(), s.COMMENT.optional())._as('condition'), g.agroup(s.MatchSuffixLine, s.MatchSuffixBlock)._as('body'))
	g.rule('MatchSuffixBody', s.Indent, s.MatchSuffixBranch.oneOrMore()._as('branches'), s.Dedent)
	g.rule('MatchSuffix', s._match, g.agroup(s.MatchSuffixBody)._as('branches'))
	g.group('Prefixes', s.Literal, g.rule('Exception', s.THROW_OPERATOR, s.Expression._as('expression')), g.rule('Instanciation', s.NEW_OPERATOR, g.agroup(s.FQName, s.Parentheses)._as('target'), s.Invocation._as('params')), g.rule('ComputationPrefix', s.PREFIX_OPERATOR, s.Expression), s.EventOperation, s.NAME, s.Parentheses)
	s.Suffixes.set(s.TypeSuffix, s.Chain, s.IterationSuffix, s.ConditionSuffix, s.ComputationInfix, s.EventOperation, s.MatchSuffix, s.Decomposition, s.Access, s.Slice, s.Invocation, s.InfixInvocation)
	s.Expression.set(s.Prefixes, s.Suffixes.zeroOrMore())
	g.rule('Assignable', s.NAME, g.agroup(s.Decomposition, s.Access, s.Slice, s.Invocation).zeroOrMore())
	g.rule('Allocation', g.agroup(s._var, s._let), s.SPACE, s.SymbolList._as('symbols'), g.arule(s.PIPE, s.NameType).optional()._as('rest'), g.arule(s.EQUALS, s.Expression).optional()._as('value'))
	g.rule('Assignment', g.arule(s.Assignable, s.COMMA).zeroOrMore()._as('before'), s.Assignable._as('main'), g.arule(s.PIPE, s.Assignable).optional()._as('rest'), g.arule(s.ASSIGN_OPERATOR, s.Expression)._as('op'))
	g.rule('Termination', g.aword('return'), s.Expression.optional())
	g.rule('Break', g.aword('break'))
	g.rule('Pass', g.aword('pass'))
	g.rule('Continue', g.aword('continue'))
	g.group('Block')
	g.group('Code')
	g.group('Statement', s.Comment, s.Allocation, s.Assignment, s.Termination, s.Break, s.Continue, s.Pass, s.Expression)
	g.rule('Statements', s.Statement, g.arule(s.SEMICOLON, s.Statement).zeroOrMore())
	g.rule('Line', s.CheckIndent, s.Statements.optional(), s.COMMENT.optional(), s.EOL)
	g.rule('BlockStart', s.CheckIndent)
	g.rule('BlockBody', s.EOL, s.Indent, s.Code.zeroOrMore()._as('body'), s.Dedent)
	g.procedure('BlockEnd', doBlockEnd)
	g.rule('IfBlock', s.BlockStart, s._if, s.Expression._as('condition'), g.agroup(s.BlockBody)._as('body'))
	g.rule('ElifBlock', s.BlockStart, s._elif, s.Expression._as('condition'), g.agroup(s.BlockBody)._as('body'))
	g.rule('ElseBlock', s.BlockStart, s._else, g.agroup(s.BlockBody)._as('body'))
	g.rule('WhileBlock', s.BlockStart, s._while, s.Expression._as('condition'), g.agroup(s.BlockBody)._as('body'))
	g.rule('TryBlock', s.BlockStart, s._try, g.agroup(s.BlockBody)._as('body'))
	g.rule('FinallyBlock', s.BlockStart, s._finally, g.agroup(s.BlockBody)._as('body'))
	g.rule('CatchBlock', s.BlockStart, s._catch, s.NameType.optional()._as('param'), g.agroup(s.BlockBody)._as('body'))
	g.rule('ForBlock', s.BlockStart, s._for, s.ParameterList._as('params'), s._in, s.Expression._as('expr'), g.agroup(s.BlockBody)._as('body'))
	g.rule('MatchBranch', s.BlockStart, g.agroup(s._else, s.UNDERSCORE, s.Suffixes.oneOrMore(), s.COMMENT.optional())._as('condition'), s.BlockBody._as('body'))
	g.rule('MatchBody', s.EOL, s.Comment.zeroOrMore(), s.Indent, s.MatchBranch.zeroOrMore()._as('branches'), s.Dedent)
	g.rule('MatchBlock', s.BlockStart, s._match, s.Expression._as('expression'), s.COMMENT.optional(), g.agroup(s.MatchBody)._as('branches'))
	g.rule('ConditionalBlock', s.BlockStart, s.IfBlock._as('if'), s.ElifBlock.zeroOrMore()._as('elif'), s.ElseBlock.optional()._as('else'), s.BlockEnd)
	g.group('Conditional', s.ConditionalBlock)
	g.rule('Try', s.BlockStart, s.TryBlock._as('try'), s.CatchBlock.optional()._as('catch'), s.FinallyBlock.optional()._as('finally'), s.BlockEnd)
	g.rule('Repetition', s.BlockStart, s.WhileBlock._as('while'), s.BlockEnd)
	g.rule('Iteration', s.BlockStart, s.ForBlock._as('for'), s.BlockEnd)
	g.rule('Selection', s.BlockStart, s.MatchBlock._as('match'), s.BlockEnd)
	s.Block.set(s.Conditional, s.Repetition, s.Iteration, s.Selection, s.Try)
	s.Code.set(s.Comment, s.Block, s.Line)
	g.rule('Body', s.Indent, s.Code.zeroOrMore()._as('code'), s.Dedent)
	g.rule('OWhen', s.CheckIndent, s.owhen, s.Expression._as('expression'), s.EOL)
	g.rule('OWhere', s.CheckIndent, s.owhere, s.NAME.optional()._as('name'), s.EOL, s.Documentation.optional()._as('doc'), s.Body._as('body'))
	g.group('OExampleBody')
	g.rule('OExample', s.CheckIndent, s.oexample, s.NAME.optional()._as('name'), s.EOL, s.Documentation.optional()._as('doc'), g.arule(s.Indent, s.OExampleBody._as('module'), s.Dedent)._as('body'))
	g.rule('CustomDecorator', s.CheckIndent, s.BANG, s.FQName._as('name'), s.Expression.optional()._as('arguments'), s.EOL)
	g.group('ConstructSuffixes', s.OWhere, s.OExample)
	g.group('Decorator', s.OWhen, s.CustomDecorator)
	s.ClosureStatement.set(s.Statements)
	s.ClosureBody.set(s.BlockBody)
	declaration(g, 'ClassAttribute', s.oshared)
	declaration(g, 'ModuleAttribute', s.oshared)
	declaration(g, 'Attribute', s.oproperty)
	g.rule('Event', s.CheckIndent, s.oevent, s.NameType._as('name'), g.arule(s.EQUALS, s.String).optional()._as('value'), s.EOL, s.Documentation.optional()._as('documentation'))
	function(g, 'Getter', s.ogetter)
	function(g, 'Setter', s.osetter)
	abstractFunction(g, 'AbstractMethod', s.omethod)
	abstractFunction(g, 'AbstractClassMethod', s.ooperation)
	function(g, 'Function', s.ofunction)
	function(g, 'Constructor', s.oconstructor, True)
	function(g, 'Method', s.omethod)
	function(g, 'ClassMethod', s.ooperation)
	g.rule('Parents', s.COLON, listOf(s.FQName, s.COMMA, g)._as('parents'))
	g.rule('EmbedLine', s.CheckIndent, s.EMBED_LINE, s.EOL)
	g.rule('Embed', s.BlockStart, s.oembed, g.arule(s.SPACE, s.NAME).optional()._as('language'), s.EOL, s.Indent, s.EmbedLine.zeroOrMore()._as('body'), s.Dedent)
	s.Block.add(s.Embed)
	g.rule('ClassGroup')
	g.group('ClassMethods', s.ClassMethod, s.AbstractClassMethod, s.Method, s.AbstractMethod, s.ClassGroup, s.Comment)
	s.ClassGroup.set(s.CheckIndent, s.ogroup, s.NAME._as('name'), s.EOL, s.Documentation.optional()._as('doc'), s.Indent, s.ClassMethods.zeroOrMore()._as('body'), s.Dedent)
	g.rule('InstanceGroup')
	g.group('InstanceMethods', s.Method, s.AbstractMethod, s.InstanceGroup, s.Comment)
	s.InstanceGroup.set(s.CheckIndent, s.ogroup, s.NAME._as('name'), s.EOL, s.Documentation.optional()._as('doc'), s.Indent, s.InstanceMethods.zeroOrMore()._as('body'), s.Dedent)
	g.rule('ModuleGroup')
	s.ModuleGroup.set(s.CheckIndent, s.ogroup, s.NAME._as('name'), s.EOL, s.Documentation.optional()._as('doc'), s.Indent, g.agroup(s.Function).zeroOrMore()._as('body'), s.Dedent)
	construct(g, 'Class', s.oclass, g.agroup(s.ClassAttribute, s.Attribute, s.Event, s.Getter, s.Setter, s.Constructor, s.ClassMethods))
	construct(g, 'Trait', s.otrait, g.agroup(s.ClassAttribute, s.Attribute, s.Event, s.Getter, s.Setter, s.Constructor, s.ClassMethods))
	construct(g, 'Singleton', s.osingleton, g.agroup(s.Attribute, s.Event, s.Getter, s.Setter, s.Constructor, s.InstanceMethods))
	g.rule('TargetAnnotation', s.CheckIndent, s.otarget, s.NAME._as('name'), g.arule(s.COLON, s.VERSION).optional(), s.EOL)
	g.rule('ModuleAnnotation', s.CheckIndent, s.omodule, s.FQName._as('name'), s.EOL)
	g.rule('VersionAnnotation', s.CheckIndent, s.oversion, s.VERSION._as('version'), s.EOL)
	g.rule('FeatureAnnotation', s.CheckIndent, s.ofeature, s.NAME._as('name'), s.VALUE.optional()._as('value'), s.EOL)
	g.rule('ImportAlias', s._as, s.NAME)
	g.rule('ImportSymbol', s.FQNAME, s.ImportAlias.optional())
	g.rule('ImportOrigin', s._from, s.FQNAME)
	g.rule('Import', s.CheckIndent, s.oimport, s.ImportSymbol._as('name'), g.arule(s.COMMA, s.ImportSymbol).zeroOrMore()._as('names'), s.ImportOrigin.optional()._as('origin'), s.EOL)
	g.rule('ModuleDeclaration', s.EmptyLines.zeroOrMore(), s.Comment.zeroOrMore()._as('comments'), s.TargetAnnotation.optional()._as('target'), s.FeatureAnnotation.zeroOrMore()._as('features'), s.ModuleAnnotation.optional()._as('module'), s.VersionAnnotation.optional()._as('version'), s.Documentation.optional()._as('documentation'), s.Import.zeroOrMore()._as('imports'))
	g.group('Structure', s.EmptyLines, s.Comment, s.ModuleAttribute, s.Type, s.Enum, s.ModuleGroup, s.Function, s.Class, s.Trait, s.Singleton)
	g.rule('Module', s.ModuleDeclaration, s.Structure.zeroOrMore()._as('structure'), s.Code.zeroOrMore()._as('code'), s.OWhere.zeroOrMore()._as('where'))
	s.OExampleBody.set(s.Module)
	g.skip = g.agroup(s.SPACE)
	g.axiom = s.Module
	return g


