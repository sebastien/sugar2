#8< ---[sugar2/v2/types.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
from sugar2.helpers import listOf
__module_name__ = 'sugar2.v2.types'
def injectTypes (g):
	""" Injects a rule with the given `name` into the grammar `g` that parses
	 type expressions."""
	self=__module__
	s=g.symbols
	g.token('TYPE_VAR', '_|[A-Z][A-Z0-9]*')
	g.token('TYPE_KEY', '[\\$_\\-A-Za-z][_\\-\\w]*')
	g.rule('TypeParameter', s.LSB, listOf(g.agroup(s.TYPE_VAR, s.FQNAME), s.COMMA, g), s.RSB)
	g.rule('TypeReference', s.FQNAME._as('name'), s.TypeParameter.optional()._as('parameters'))
	g.group('TypeValue')
	g.rule('TypeExpression')
	g.rule('TypeUnionSuffix', s.PIPE, s.TypeValue)
	g.group('TypePrefix', s.TypeReference)
	g.group('TypeSuffix', s.TypeUnionSuffix)
	g.rule('TypeExpression', s.TypePrefix, s.TypeSuffix.zeroOrMore())
	g.rule('TypeParens', s.LP, listOf(s.TypeExpression, s.COMMA, g), s.RP)
	g.rule('TypeEntry', s.TYPE_KEY._as('name'), s.COLON, s.TypeReference._as('value'))
	g.rule('TypeEntryList', s.TypeEntry, g.arule(s.COMMA, s.TypeEntry).zeroOrMore(), s.COMMENT.optional())
	g.group('TypeEntryLine', s.TypeEntryList, s.COMMENT)
	g.rule('TypeEntryBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.TypeEntryLine).oneOrMore()._as('content'), s.Dedent)
	g.rule('TypeMap', s.LB, s.TypeEntryList.optional()._as('head'), s.TypeEntryBlock.optional()._as('tail'), g.arule(s.EOL, s.CheckIndent).optional(), s.RB)
	s.TypeValue.set(s.TypeMap, s.TypeParens, s.TypeExpression)
	g.rule('TypeSlot', s.CheckIndent, g.aword('@slot'), s.NAME._as('name'), g.arule(s.COLON, s.TypeValue).optional()._as('value'), s.EOL, s.Documentation.optional()._as('documentation'))
	g.group('TypeLine', s.TypeSlot)
	g.group('TypeCode', s.COMMENT, s.TypeLine)
	g.rule('TypeBody', s.Indent, s.TypeCode.zeroOrMore(), s.Dedent)
	g.rule('Enum', s.CheckIndent, g.aword('@enum'), s.TypeReference._as('name'), s.EQUALS, listOf(s.NAME, s.PIPE, g)._as('symbols'), s.EOL, s.Documentation.optional()._as('documentation'))
	g.rule('Type', s.CheckIndent, g.aword('@type'), s.TypeReference._as('name'), g.arule(s.COLON, s.TypeReference).optional()._as('parent'), g.arule(s.EQUALS, s.TypeValue).optional()._as('value'), s.EOL, s.Documentation.optional()._as('documentation'), s.TypeBody.optional()._as('body'))


