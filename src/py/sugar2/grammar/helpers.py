#8< ---[sugar2/grammar/helpers.py]---
#!/usr/bin/env python
"""A collection of helper functions used by the grammar submodules"""
import sys
__module__ = sys.modules[__name__]
import sys
__module_name__ = 'sugar2.grammar.helpers'
def doIndent (element, context):
	self=__module__
	indent=(context.get('indent') or 0)
	context.set('indent', (indent + 1))


def doDedent (element, context):
	self=__module__
	indent=(context.get('indent') or 0)
	context.set('indent', (indent - 1))


def doCheckIndent (element, context):
	self=__module__
	indent = context.get("indent") or 0
	o      = context.offset or 0
	so     = max(o - indent, 0)
	eo     = o
	tabs   = 0
	# This is a fix
	if so == eo and so > 0:
		so = eo
	for i in xrange(so, eo):
		if context[i] == "\t":
			tabs += 1
	return tabs == indent
	


def doBlockStart (element, context):
	self=__module__
	pass


def doBlockLastSetLine (element, context):
	self=__module__
	context.set('blockLast', 1)


def doBlockLastSetBody (element, context):
	self=__module__
	context.set('blockLast', 2)


def doBlockLastIsLine (element, context):
	self=__module__
	return (context.get('blockLast') == 1)


