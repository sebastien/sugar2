#8< ---[sugar2/v2/types.py]---
#!/usr/bin/env python
# encoding: utf-8
import sys
__module__ = sys.modules[__name__]
from sugar2.helpers import listOf
__module_name__ = 'sugar2.v2.types'
def injectTypes (g):
	""" Injects a rule with the given `name` into the grammar `g` that parses
	 type expressions."""
	self=__module__
	s=g.symbols
	g.token(u'TYPE_VAR', u'_|[A-Z][A-Z0-9]*')
	g.token(u'TYPE_KEY', u'[\\$_\\-A-Za-z][_\\-\\w]*')
	g.rule(u'TypeParameter', s.LSB, listOf(g.agroup(s.TYPE_VAR, s.FQNAME), s.COMMA, g), s.RSB)
	g.rule(u'TypeReference', s.FQNAME._as(u'name'), s.TypeParameter.optional()._as(u'parameters'))
	g.group(u'TypeValue')
	g.rule(u'TypeExpression')
	g.rule(u'TypeUnionSuffix', s.PIPE, s.TypeValue)
	g.group(u'TypePrefix', s.TypeReference)
	g.group(u'TypeSuffix', s.TypeUnionSuffix)
	g.rule(u'TypeExpression', s.TypePrefix, s.TypeSuffix.zeroOrMore())
	g.rule(u'TypeParens', s.LP, listOf(s.TypeExpression, s.COMMA, g), s.RP)
	g.rule(u'TypeEntry', s.TYPE_KEY._as(u'name'), s.COLON, s.TypeReference._as(u'value'))
	g.rule(u'TypeEntryList', s.TypeEntry, g.arule(s.COMMA, s.TypeEntry).zeroOrMore(), s.COMMENT.optional())
	g.group(u'TypeEntryLine', s.TypeEntryList, s.COMMENT)
	g.rule(u'TypeEntryBlock', s.Indent, g.arule(s.EOL, s.CheckIndent, s.TypeEntryLine).oneOrMore()._as(u'content'), s.Dedent)
	g.rule(u'TypeMap', s.LB, s.TypeEntryList.optional()._as(u'head'), s.TypeEntryBlock.optional()._as(u'tail'), g.arule(s.EOL, s.CheckIndent).optional(), s.RB)
	s.TypeValue.set(s.TypeMap, s.TypeParens, s.TypeExpression)
	g.rule(u'TypeSlot', s.CheckIndent, g.aword(u'@slot'), s.NAME._as(u'name'), g.arule(s.COLON, s.TypeValue).optional()._as(u'value'), s.EOL, s.Documentation.optional()._as(u'documentation'))
	g.group(u'TypeLine', s.TypeSlot)
	g.group(u'TypeCode', s.COMMENT, s.TypeLine)
	g.rule(u'TypeBody', s.Indent, s.TypeCode.zeroOrMore(), s.Dedent)
	g.rule(u'Enum', s.CheckIndent, g.aword(u'@enum'), s.TypeReference._as(u'name'), s.EQUALS, listOf(s.NAME, s.PIPE, g)._as(u'symbols'), s.EOL, s.Documentation.optional()._as(u'documentation'))
	g.rule(u'Type', s.CheckIndent, g.aword(u'@type'), s.TypeReference._as(u'name'), g.arule(s.COLON, s.TypeReference).optional()._as(u'parent'), g.arule(s.EQUALS, s.TypeValue).optional()._as(u'value'), s.EOL, s.Documentation.optional()._as(u'documentation'), s.TypeBody.optional()._as(u'body'))


