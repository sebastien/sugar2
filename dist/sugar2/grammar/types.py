#8< ---[__current__.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
from sugar2.grammar.helpers import listOf
__module_name__ = '__current__'
def injectTypes (g):
	"""Injects a rule with the given `name` into the grammar `g` that parses
	type expressions."""
	self=__module__
	s=g.symbols
	g.token('TYPE_VAR', '_|[A-Z][A-Z0-9]*')
	g.rule('TypeParameter', s.LSB, listOf(g.agroup(s.TYPE_VAR, s.FQNAME), s.COMMA, g), s.RSB)
	g.rule('TypeReference', s.FQNAME._as('name'), s.TypeParameter.optional()._as('parameters'))
	g.group('TypeValue')
	g.rule('TypeExpression')
	g.rule('TypeUnionSuffix', s.PIPE, s.TypeValue)
	g.group('TypePrefix', s.TypeReference)
	g.group('TypeSuffix', s.TypeUnionSuffix)
	g.rule('TypeExpression', s.TypePrefix, s.TypeSuffix.zeroOrMore())
	g.rule('TypeParens', s.LP, listOf(s.TypeExpression, s.COMMA, g), s.RP)
	s.TypeValue.set(s.TypeParens, s.TypeExpression)
	g.rule('TypeSlot', s.CheckIndent, g.aword('@slot'), s.NAME._as('name'), g.arule(s.COLON, s.TypeValue).optional()._as('value'), s.EOL, s.Documentation.optional()._as('documentation'))
	g.group('TypeLine', s.TypeSlot)
	g.group('TypeCode', s.COMMENT, s.TypeLine)
	g.rule('TypeBody', s.Indent, s.TypeCode.zeroOrMore(), s.Dedent)
	g.rule('Type', s.CheckIndent, g.aword('@type'), s.TypeReference._as('name'), g.arule(s.COLON, s.TypeValue).optional()._as('value'), s.EOL, s.Documentation.optional()._as('documentation'), s.TypeBody.optional())


