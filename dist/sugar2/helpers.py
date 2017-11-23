#8< ---[sugar2/grammar/helpers.py]---
#!/usr/bin/env python
# encoding: utf-8
""" A collection of helper functions used by the grammar submodules"""
import sys
__module__ = sys.modules[__name__]
import sys
__module_name__ = 'sugar2.grammar.helpers'
def doIndent (element, context):
	self=__module__
	indent=(context.get(u'indent') or 0)
	context.set(u'indent', (indent + 1))


def doDedent (element, context):
	self=__module__
	indent=(context.get(u'indent') or 0)
	context.set(u'indent', (indent - 1))


def doCheckIndent (element, context, min=None):
	self=__module__
	if min is None: min = False
	indent = context.get("indent") or 0
	o      = context.offset or 0
	so     = max(o - indent, 0)
	eo     = o
	tabs   = 0
	# This is a fix
	if so == eo and so > 0:
		so = eo
	for i in range(so, eo):
		if context[i] == b"\t":
			tabs += 1
	return tabs == indent


def doCheckMinIndent (element, context):
	self=__module__
	return doCheckIndent(element, context, True)


def doBlockStart (element, context):
	self=__module__
	pass


def doBlockEnd (element, context):
	self=__module__
	pass


def doBlockLastSetLine (element, context):
	self=__module__
	context.set(u'blockLast', 1)


def doBlockLastSetBody (element, context):
	self=__module__
	context.set(u'blockLast', 2)


def doBlockLastIsLine (element, context):
	self=__module__
	return (context.get(u'blockLast') == 1)


def listOf (rule, separator, grammar):
	""" Creates a new list of the given rule, separated by the given separator
	 in the given grammar"""
	self=__module__
	return grammar.arule(grammar.arule(rule, separator).zeroOrMore(), rule)


