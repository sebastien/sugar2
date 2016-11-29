#8< ---[sugar2.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
import sys
from lambdafactory.main import Command
from sugar2.parser import Parser
__module_name__ = 'sugar2'
__version__ = '0.9.1'
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
	

def run (arguments):
	self=__module__
	command=SugarCommand('sugar')
	command.run((arguments or ['--help']))
	return command


def __module_init__():
	import sys
	sys.setrecursionlimit(2500)
	if __name__ == "__main__":
		import sys
		run(sys.argv[1:])
	
__module_init__()
