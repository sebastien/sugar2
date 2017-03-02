#8< ---[sugar2.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
import os, sys, io, tempfile
from lambdafactory.main import Command
from sugar2.parser import Parser
__module_name__ = 'sugar2'
__version__ = '0.9.1'
class SugarCommand(Command):
	def __init__ (self, name, version=None):
		self.version = None
		if version is None: version = 2
		self.version = version
		Command.__init__(self,name)
	
	def setupEnvironment(self):
		python_plugin=self.environment.loadLanguage('python')
		javascript_plugin=self.environment.loadLanguage('javascript')
		python_plugin.addRecognizedExtension('spy')
		javascript_plugin.addRecognizedExtension('sjs')
		self.environment.addParser(Parser(self, self.version), 'sg spy sjs'.split())
	

def run (arguments, version=None, output=None):
	self=__module__
	if version is None: version = 2
	if output is None: output = sys.stdout
	command=SugarCommand('sugar', version)
	program=command.run((arguments or ['--help']), output)
	if (not program):
		return None
	elif True:
		return program


def process (text, version=None, options=None):
	self=__module__
	if version is None: version = 2
	if options is None: options = []
	s = io.BytesIO ()
	p = tempfile.mktemp(suffix=".sg")
	with open(p,"w") as f: f.write(text)
	
	options = (options + ['-cles', p])
	run(options, version, s)
	os.unlink(p)
	s.seek(0)
	return s.read()


def __module_init__():
	import sys
	sys.setrecursionlimit(2500)
	if __name__ == "__main__":
		import sys
		if not run(sys.argv[1:]).modules:
			sys.exit(-1)
	
__module_init__()
