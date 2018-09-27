#8< ---[sugar2/v2/writer.py]---
#!/usr/bin/env python
# encoding: utf-8
import sys
__module__ = sys.modules[__name__]
import libparsing
from lambdafactory import interfaces
from lambdafactory.modelbase import Factory
import lambdafactory.passes as passes
import lambdafactory.resolution as resolution
import math
__module_name__ = 'sugar2.v2.writer'
__version__ = '0.9'
F = Factory()
class LambdaFactoryBuilder(libparsing.Processor):
	""" Converts a parse tree into a Lambda Factory program model, which can then
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
	OPERATORS = [[u'.'], [u'or'], [u'and'], [u'not'], [u'>', u'>=', u'<', u'<=', u'!=', u'==', u'is', u'is not', u'in', u'not in'], [u'::', u'::<', u'::>', u'::?', u'::='], [u'..', u'‥'], [u'+', u'-'], [u'|', u'&', u'<<', u'>>'], [u'/', u'*', u'%', u'//'], [u'/=', u'*=', u'%=', u'+=', u'-=', u'=']]
	OPERATORS_NORMALIZED = {'||':u'|', '&&':u'&', '|':u'.'}
	def __init__ (self, grammar, path=None):
		self.module = None
		self.path = None
		self.processes = []
		self.varcounter = 0
		if path is None: path = None
		libparsing.Processor.__init__(self,grammar, False)
		self.path = path
		program = F.createProgram()
		program.setFactory(F)
	
	def access(self, value, *keys):
		if (not value):
			return None
		for k in keys:
			if value:
				value = value[k]
			elif True:
				return None
		return value
	
	def process(self, match):
		res=(lambda *a,**kw:libparsing.Processor.process(self,*a,**kw))(match)
		return res
	
	def setSourceLocation(self, element, match):
		""" A helper that sets the location of the given element in the source"""
		if ((match and (not isinstance(element, tuple))) and (not isinstance(element, list))):
			if (match.countChildren() == 0):
				element.setOffset(match.offset, (match.offset + match.length))
			elif True:
				start_match=match[0]
				end_match=match[-1]
				element.setOffset(start_match.offset, (end_match.offset + end_match.length))
			element.setSourcePath(self.path)
		return element
	
	def getDefaultModuleName(self):
		if self.path:
			return self.path.split(u'/')[-1].split(u'.')[0].replace(u'-', u'_')
		elif True:
			return u'__current__'
	
	def normalizeOperator(self, operator):
		operator = operator.replace("\t"," ").replace("\n"," ")
		operator = " ".join((_.strip() for _ in operator.split() if _.strip()))
		operator = self.OPERATORS_NORMALIZED.get(operator) or operator
		return operator
	
	def getPriority(self, value):
		""" Returns the priority of the given model element or string (for an operator).
		 -1 is returned if not known."""
		if isinstance(value, interfaces.IComputation):
			return self.getOperatorPriority(value.getOperator().getName())
		elif isinstance(value, interfaces.IElement):
			if value.hasAnnotation(u'priority'):
				return value.getAnnotation(u'priority').getContent()
			elif True:
				return -1
		elif True:
			return self.getOperatorPriority(value)
	
	def getOperatorPriority(self, operator, operators=None):
		if operators is None: operators = self.__class__.OPERATORS
		i=0
		operator = libparsing.ensure_str(operator)
		for line in operators:
			if (operator in line):
				return i
			i = (i + 1)
		raise Exception((((u'getOperatorPriority: Unknown operator ' + repr(operator)) + u', must be one of ') + repr(self.__class__.OPERATORS)))
	
	def _var(self, name=None, context=None):
		""" Lists the variables defined in the given context or gets the
		 variable with the given name."""
		if name is None: name = None
		if context is None: context = self.context
		if (not name):
			return context.getVariables().keys()
		elif True:
			return context.getVariables().get(name)
	
	def _bind(self, scope, referanceable):
		""" Assigns the given referenceable to the current scope"""
		if (isinstance(referanceable, list) or isinstance(referanceable, tuple)):
			for _ in referanceable:
				self._bind(scope, _)
			return scope
		elif isinstance(referanceable, interfaces.IAccessor):
			scope.setAccessor(referanceable.getName(), referanceable)
		elif isinstance(referanceable, interfaces.IMutator):
			scope.setMutator(referanceable.getName(), referanceable)
		elif isinstance(referanceable, interfaces.IReferencable):
			scope.setSlot(referanceable.getName(), referanceable)
			return scope
		elif True:
			return scope
	
	def filterNull(self, result):
		""" Returns only the elements of result that have a value"""
		return [_ for _ in result if _]
	
	def _tryGet(self, list, index, default):
		""" Tries to get the `index`th element of `list` or returns `default`"""
		if (list and (len(list) > index)):
			return list[index]
		elif True:
			return None
	
	def _addCode(self, element, code):
		code = (code or [])
		if (isinstance(code, list) or isinstance(code, tuple)):
			for _ in code:
				self._addCode(element, _)
		elif isinstance(code, interfaces.IOperation):
			element.addOperation(code)
		elif isinstance(code, interfaces.IReference):
			element.addOperation(F.resolve(code))
		elif isinstance(code, interfaces.IComment):
			pass
		elif isinstance(code, interfaces.IValue):
			element.addOperation(F.evaluate(code))
		elif isinstance(code, interfaces.IClosure):
			element.addOperation(F.evaluate(code))
		elif code:
			raise Exception(u'Code element type not supported: {0}'.format(repr(code)))
		return element
	
	def _ensureList(self, value):
		if (not (isinstance(value, list) or isinstance(value, tuple))):
			return [value]
		elif True:
			return value
	
	def _processList(self, match):
		""" Processes a match generated by the `_listOf` helper"""
		p=self.process(match)
		r=[]
		for _ in p[0]:
			r.append(_[0])
		r.append(p[1])
		return r
	
	def _ensureReturns(self, process):
		""" Ensures that the given process returns a value at the end"""
		if (((not isinstance(process, interfaces.IProcess)) or (not process.operations)) or (len(process.operations) == 0)):
			return process
		if (len(process.operations) == 0):
			return process
		last_operation=process.operations[-1]
		ret=None
		if last_operation:
			if isinstance(last_operation, interfaces.INOP):
				return process
			elif isinstance(last_operation, interfaces.IIteration):
				return process
			elif isinstance(last_operation, interfaces.ITermination):
				return process
			elif isinstance(last_operation, interfaces.ISelection):
				return process
			elif isinstance(last_operation, interfaces.IInterception):
				return process
			elif isinstance(last_operation, interfaces.IInterruption):
				return process
			elif isinstance(last_operation, interfaces.IEmbed):
				return process
			elif isinstance(last_operation, interfaces.IAllocation):
				return process
			elif isinstance(last_operation, interfaces.IAssignment):
				return process
			elif (isinstance(last_operation, interfaces.IRepetition) or isinstance(last_operation, interfaces.IIteration)):
				last_operation.addAnnotation(u'last')
				return process
			elif isinstance(last_operation, interfaces.IOperation):
				process.removeOperationAt(-1)
				ret = F.returns(last_operation)
		if ret:
			ret.addAnnotation(u'implicit')
			process.addOperation(ret)
		return process
	
	def onModuleDeclaration(self, match):
		return {'comments':self.process(match[u'comments']), 'module':self.process(match[u'module']), 'version':self.process(match[u'version']), 'documentation':self.process(match[u'documentation']), 'imports':self.process(match[u'imports'])}
	
	def onModule(self, match):
		declarations=self.process(match[0])
		name=declarations[u'module']
		module=F.createModule(((name and name.getContent()) or self.getDefaultModuleName()))
		self._addCode(module, declarations[u'comments'])
		for _ in declarations[u'imports']:
			assert(isinstance(_, interfaces.IImportOperation))
			module.addImportOperation(_)
		module.setDocumentation(declarations[u'documentation'])
		version=declarations[u'version']
		if version:
			module.addAnnotation(version)
		structure=self.process(match[u'structure'])
		code=self.process(match[u'code'])
		where=self.process(match[u'where'])
		init_function=F.createInitializer()
		self._addCode(init_function, code)
		self._bind(module, structure)
		self._bind(module, init_function)
		for _ in where:
			module.addAnnotation(_)
		self.setSourceLocation(module, match)
		return module
	
	def onModuleAnnotation(self, match):
		ref=self.process(match[u'name'])
		return F.annotation(u'module', ref.getReferenceName())
	
	def onVersionAnnotation(self, match):
		version=self.process(match[u'version'])[0]
		return F.annotation(u'version', version)
	
	def onParents(self, match):
		return self._processList(match[u'parents'])
	
	def _onConstruct(self, creator, match):
		name=self.process(match[u'name'])
		inherits=self.process(match[u'inherits'])
		res=creator(name, inherits)
		is_abstract=match[0]
		doc=self.process(match[u'documentation'])
		body=self.process(match[u'body'])
		suffixes=self.process(match[u'suffixes'])
		res.setDocumentation(doc)
		res.setAbstract((is_abstract and True))
		for _ in (self.access(suffixes, 0) or []):
			res.addAnnotation(_)
		self._bind(res, body)
		self.setSourceLocation(res, match)
		return res
	
	def onClass(self, match):
		return self._onConstruct(F.createClass, match)
	
	def onSingleton(self, match):
		return self._onConstruct(F.createSingleton, match)
	
	def onTrait(self, match):
		return self._onConstruct(F.createTrait, match)
	
	def onAttribute(self, match):
		name=self.process(match[u'name'])
		value=self.process(match[u'value'])
		doc=self.process(match[u'documentation'])
		res=F._attr(name[0].getReferenceName(), None, (value and value[1]))
		res.setDocumentation(doc)
		self.setSourceLocation(res, match)
		return res
	
	def onClassAttribute(self, match):
		name=self.process(match[u'name'])
		value=self.process(match[u'value'])
		doc=self.process(match[u'documentation'])
		res=F._classattr(name[0].getReferenceName(), None, (value and value[1]))
		res.setDocumentation(doc)
		return self.setSourceLocation(res, match)
	
	def onModuleAttribute(self, match):
		name_type=self.process(match[2])
		value=self._tryGet(self.process(match[3]), 1, None)
		doc=self.process(match[5])
		res=F._moduleattr(name_type[0].getReferenceName(), None, value)
		res.setDocumentation(doc)
		return self.setSourceLocation(res, match)
	
	def onEvent(self, match):
		name=self.process(match[u'name'])[0].getReferenceName()
		doc=self.process(match[u'documentation'])
		value=self.process(match[u'value'])
		if value:
			value = value[1]
		elif True:
			value = F._string(name)
		event=F._event(name, None, value)
		method=F.createMethod(((u'on' + name[0].upper()) + name[1:]))
		if doc:
			method.setDocumentation(doc)
		method.addAnnotation(F.annotation(u'event', name))
		return [event, method]
	
	def _onGroup(self, match):
		name=self.process(match[u'name'])
		doc=self.process(match[u'doc'])
		body=self.process(match[u'body'])
		for t in body:
			for e in t:
				a=F.annotation(u'as', name)
				e.addAnnotation(a)
		return self.setSourceLocation(body, match)
	
	def onModuleGroup(self, match):
		return self._onGroup(match)
	
	def onInstanceGroup(self, match):
		return self._onGroup(match)
	
	def onClassGroup(self, match):
		return self._onGroup(match)
	
	def _createCallable(self, factory, match, hasBody=None):
		if hasBody is None: hasBody = True
		name_type=self.process(match[u'name'])
		params=self.access(self.access(self.process(match[u'parameters']), 0), 0)
		doc=self.process(match[u'documentation'])
		body=((hasBody and self.process(match[u'body'])) or None)
		dec=self.process(match[u'decorators'])
		suffixes=self.process(match[u'suffixes'])
		fun=None
		if (name_type is True):
			fun = factory(params)
		elif True:
			fun = factory(name_type[0].getReferenceName(), params)
		for d in dec:
			fun.addAnnotation(d)
		fun.setDocumentation(doc)
		if hasBody:
			self._addCode(fun, body)
		elif True:
			fun.setAbstract(True)
		for _ in (self.access(suffixes, 0) or []):
			fun.addAnnotation(_)
		return self.setSourceLocation(fun, match)
	
	def onClassMethod(self, match):
		return self._createCallable(F.createClassMethod, match)
	
	def onAbstractClassMethod(self, match):
		return self._createCallable(F.createClassMethod, match, False)
	
	def onGetter(self, match):
		return self._createCallable(F.createAccessor, match)
	
	def onSetter(self, match):
		return self._createCallable(F.createMutator, match)
	
	def onMethod(self, match):
		return self._createCallable(F.createMethod, match)
	
	def onAbstractMethod(self, match):
		return self._createCallable(F.createMethod, match, False)
	
	def onConstructor(self, match):
		return self._createCallable(F.createConstructor, match)
	
	def onFunction(self, match):
		return self._createCallable(F.createFunction, match)
	
	def onClosureParameters(self, match):
		return self.process(match[0])
	
	def onClosureStatement(self, match):
		return self.process(match[0])
	
	def onClosureBody(self, match):
		return self.process(match[0])
	
	def onClosure(self, match):
		return self._ensureReturns(self.process(match[0]))
	
	def onEmptyClosure(self, match):
		return F.createClosure(self.process(match[1]))
	
	def onInlineClosure(self, match):
		params=self.process(match[1])
		line=[self.process(match[2])]
		res=F.createClosure(params)
		self._addCode(res, line)
		return self._ensureReturns(res)
	
	def onBlockClosure(self, match):
		params=self.process(match[u'params'])
		code=self.process(match[u'body'])
		res=F.createClosure(params)
		self._addCode(res, code)
		return res
	
	def onImportSymbol(self, match):
		return [self.process(match[0]), self.process(match[1])]
	
	def onImportOrigin(self, match):
		return self.process(match[1])
	
	def onImportAlias(self, match):
		return self.process(match[1]).getReferenceName()
	
	def onImportName(self, match):
		value=self.process(match[0])
		if isinstance(value, interfaces.IString):
			return value.getActualValue()
		elif True:
			return value[0]
	
	def onImport(self, match):
		name=self.process(match[u'name'])
		names=self.process(match[u'names'])
		origin=self.process(match[u'origin'])
		origin_is_dynamic=isinstance(origin, interfaces.IString)
		if origin_is_dynamic:
			origin = origin.getActualValue()
		symbols=[]
		names   = [_[1] for _ in names]
		if not origin:
			symbols = [F.importModule(_[0], _[1]) for _ in [name] + (names or [])]
		else:
			symbols = [F.importSymbol(_[0], origin, _[1]) for _ in [name] + (names or [])]
		result=None
		if (len(names) == 0):
			if (not origin):
				result = F.importModule(name[0], name[1])
			elif True:
				result = F.importSymbol(name[0], origin, name[1])
		elif True:
			if (not origin):
				result = F.importModules(symbols)
			elif True:
				result = F.importSymbols(symbols, origin)
		if origin_is_dynamic:
			result.addAnnotation(u'import-dynamic')
		return result
	
	def onBody(self, match):
		return self.process(match[1])
	
	def onCode(self, match):
		content=self.process(match[0])
		return content
	
	def onLine(self, match):
		comment=self.process(match[2])
		statements=self.process(match[1])
		return statements
	
	def onStatements(self, match):
		res=[self.process(match[0])]
		tail=self.process(match[1])
		for _ in (tail or []):
			res.append(_[1])
		return res
	
	def onStatement(self, match):
		""" Returns an `Element` or a list of `[Element]`. Typically these elements
		 would be Comments, Blocks or Operations."""
		return self.process(match[0])
	
	def onConditionalBlock(self, match):
		_if=self.process(match[u'if'])
		_elifs=self.process(match[u'elif'])
		_else=self.process(match[u'else'])
		res=F.select()
		res.addRule(F.matchProcess(_if[0], _if[1]))
		for _ in _elifs:
			res.addRule(F.matchProcess(_[0], _[1]))
		if _else:
			e=F.matchProcess(F._ref(u'True'), _else[0])
			e.addAnnotation(u'else')
			res.addRule(e)
		return res
	
	def onConditional(self, match):
		return self.process(match[0])
	
	def onIfBlock(self, match):
		block=F.createBlock()
		self._addCode(block, self.process(match[u'body']))
		return [self.process(match[u'condition']), block]
	
	def onIfLine(self, match):
		return self.onIfBlock(match)
	
	def onElifBlock(self, match):
		return self.onIfBlock(match)
	
	def onElifLine(self, match):
		return self.onElifBlock(match)
	
	def onElseBlock(self, match):
		block=F.createBlock()
		self._addCode(block, self.process(match[u'body']))
		return [block]
	
	def onElseLine(self, match):
		return self.onElseBlock(match)
	
	def onIteration(self, match):
		return self.process(match[u'for'])
	
	def onRepetition(self, match):
		return self.process(match[u'while'])
	
	def onSelection(self, match):
		return self.process(match[u'match'])
	
	def onTry(self, match):
		return F.intercept(self.process(match[u'try']), self.process(match[u'catch']), self.process(match[u'finally']))
	
	def onForBlock(self, match):
		params=self.process(match[u'params'])
		expr=self.process(match[u'expr'])
		body=self.process(match[u'body'])
		block=F.createClosure(params)
		self._addCode(block, body)
		return F.iterate(expr, block)
	
	def onWhileBlock(self, match):
		condition=self.process(match[u'condition'])
		body=self.process(match[u'body'])
		block=F.createBlock()
		self._addCode(block, body)
		return F.repeat(condition, block)
	
	def onMatchBlock(self, match):
		expr=self.process(match[u'expression'])
		branches=self.process(match[u'branches'])[0]
		res=F.select()
		res.setImplicitValue(expr)
		for branch in branches:
			res.addRule(F.matchExpression(branch[0], branch[1]))
			if branch[2]:
				branch[2].setElement(res)
		return res
	
	def onMatchBody(self, match):
		return self.process(match[u'branches'])
	
	def onMatchBranch(self, match):
		res=self._onMatchBranchHelper(match)
		block=F.createBlock()
		self._addCode(block, self.process(match[u'body']))
		res[1] = block
		return res
	
	def _onMatchBranchHelper(self, match):
		condition=self.process(match[u'condition'])[0]
		ref=F._implicitref()
		if (condition == u'_'):
			condition = ref
		elif (condition == u'else'):
			condition = F._ref(u'true')
			ref = None
		elif True:
			condition = self._applySuffixes(ref, condition)
		block=F.createBlock()
		self._addCode(block, self.process(match[u'body']))
		return [condition, None, ref]
	
	def onMatchSuffix(self, match):
		branches=self.process(match[u'branches'])[0]
		return [match.name, branches]
	
	def onMatchSuffixBody(self, match):
		return self.process(match[u'branches'])
	
	def onMatchSuffixLine(self, match):
		return self.process(match[u'body'])
	
	def onMatchSuffixBlock(self, match):
		return self.process(match[u'body'])
	
	def onMatchSuffixBranch(self, match):
		res=self._onMatchBranchHelper(match)
		res[1] = self.process(match[u'body'][0][0])
		return res
	
	def onTryBlock(self, match):
		body=self.process(match[u'body'])
		block=F.createBlock()
		self._addCode(block, body)
		return block
	
	def onCatchBlock(self, match):
		body=self.process(match[u'body'])
		param=self.process(match[u'param'])
		args=[]
		if param:
			args.append(F._param(param[0].getReferenceName()))
		elif True:
			args.append(F._param(u'exception'))
		block=F.createClosure(args)
		self._addCode(block, body)
		return block
	
	def onFinallyBlock(self, match):
		body=self.process(match[u'body'])
		block=F.createBlock()
		self._addCode(block, body)
		return block
	
	def onBlockBody(self, match):
		return self.process(match[u'body'])
	
	def onBlockLine(self, match):
		return self.process(match[u'body'])
	
	def onEMBED_LINE(self, match):
		return self.process(match)
	
	def onEmbed(self, match):
		body=self.process(match[u'body'])
		language=self.process(match[u'language'])
		if language:
			language = language[1].getName()
		lines=[]
		for line in body:
			lines.append(line[1][1])
		return F.embed(language, u'\n'.join(lines))
	
	def onExpression(self, match):
		prefix=self.process(match[0])
		suffixes=self.process(match[1])
		current=None
		if ((isinstance(prefix, interfaces.ILiteral) or isinstance(prefix, interfaces.IValue)) or isinstance(prefix, interfaces.IClosure)):
			current = prefix
		elif (((((((((isinstance(prefix, interfaces.IComputation) or isinstance(prefix, interfaces.IResolution)) or isinstance(prefix, interfaces.IInvocation)) or isinstance(prefix, interfaces.IInstanciation)) or isinstance(prefix, interfaces.IAccessOperation)) or isinstance(prefix, interfaces.IExcept)) or isinstance(prefix, interfaces.ISelection)) or isinstance(prefix, interfaces.IEnumeration)) or isinstance(prefix, interfaces.IIteration)) or isinstance(prefix, interfaces.ITypeIdentification)):
			current = prefix
		elif isinstance(prefix, interfaces.IReference):
			current = F.resolve(prefix)
			self.setSourceLocation(current, match)
		elif True:
			raise Exception((u'Prefix not supported yet: ' + str(prefix)))
		return self._applySuffixes(current, suffixes)
	
	def _applySuffixes(self, value, suffixes):
		""" Applies the suffixes to the current value, modifying it as it goes. Note that suffixes
		 are constructed depth-first, so from right to left, and that there's pretty much
		 only one suffix each time."""
		if suffixes:
			for args in suffixes:
				name=args[0]
				if (name == u'Invocation'):
					if ((type(args[1]) == list) or (type(args[1]) == tuple)):
						value = F.invoke_args(value, args[1])
					elif True:
						value = F.invoke(value, args[1])
				elif (name == u'InfixInvocation'):
					a=([value] + self._ensureList(args[2]))
					t=args[1]
					value = F.invoke_args(F.resolve(t), a)
				elif (name == u'ComputationInfix'):
					value = self._applyComputationInfix(value, args[1], args[2])
				elif (name == u'Decomposition'):
					f=F.resolve
					if (args[1] == u'.'):
						f = F.decompose
					for _ in args[2]:
						value = f(_, value)
				elif (name == u'Access'):
					value = F.access(value, args[1])
				elif (name == u'Slice'):
					value = F.slice(value, args[1], args[2])
				elif (name == u'IterationSuffix'):
					rvalue=args[2]
					o=args[3]
					if isinstance(rvalue, interfaces.ISelection):
						value = args[1](value, rvalue.getRule(0).getExpression().detach())
						value.addAnnotation(u'operator', o)
						value.addAnnotation(u'priority', self.getOperatorPriority(o))
						rvalue.getRule(0).setExpression(value.detach())
						value = rvalue
					elif True:
						value = args[1](value, args[2])
						value.addAnnotation(u'operator', o)
						value.addAnnotation(u'priority', self.getOperatorPriority(o))
				elif (name == u'ConditionSuffix'):
					t=args[1]
					v=args[2]
					if (t == u'if'):
						if isinstance(v, interfaces.ISelection):
							assert(v.hasAnnotation(u'else-expression'))
							v.addAnnotation(u'if-expression')
							r=v.getRule(0)
							p=r.getPredicate()
							if p.hasAnnotation(u'if-default'):
								r.setPredicate(r.getExpression())
								r.setExpression(value)
								p.removeAnnotation(u'if-default')
							elif True:
								op=self.normalizeOperator(u'and')
								r.setPredicate(F.compute(F._op(op, self.getOperatorPriority(op)), p, value))
							value = v
						elif True:
							r=F.matchExpression(v, value)
							value = F.select().addAnnotation(u'if-expression')
							value.addRule(r)
					elif (t == u'else'):
						rt=F.matchExpression(value.copy().addAnnotation(u'if-default'), value)
						rf=F.matchExpression(F._ref(u'True'), v).addAnnotation(u'else')
						value = F.select().addAnnotation(u'if-expression').addAnnotation(u'else-expression')
						value.addRule(rt)
						value.addRule(rf)
					elif True:
						raise Exception(u'Unknown condition type: {0}'.format(t))
				elif (name == u'MatchSuffix'):
					res=F.select().addAnnotation(u'if-expression')
					res.setImplicitValue(value)
					for branch in args[1]:
						res.addRule(F.matchExpression(branch[0], branch[1]))
						if branch[2]:
							branch[2].setElement(res)
					value = res
				elif (name == u'Chain'):
					res=value
					op=args[1]
					rest=args[2]
					chain=F.chain(op, value)
					for _ in rest:
						branch=self._applySuffixes(F._implicitref(chain), _)
						chain.addGroup(branch)
					value = chain
				elif (name == u'EventOperation'):
					op=args[1]
					name=args[2]
					param=args[3]
					if (op == u'!'):
						value = F.triggerEvent(value, name, param)
					elif (op == u'!+'):
						value = F.bindEvent(value, name, param)
					elif (op == u'!!'):
						value = F.bindEventOnce(value, name, param)
					elif (op == u'!-'):
						value = F.unbindEvent(value, name, param)
				elif (name == u'TypeSuffix'):
					value = F.typeof(value, args[1])
				elif True:
					raise Exception((((u'sugar2.writer._applySuffixes: Suffix not supported yet: ' + str(name)) + u' in ') + str(args)))
		return value
	
	def _getLeftmostComputation(self, value):
		""" Returns the rightmost computation"""
		if isinstance(value, interfaces.IComputation):
			if (value.isUnary() or value.hasAnnotation(u'parens')):
				return None
			elif True:
				return (self._getLeftmostComputation(value.getLeftOperand()) or value)
		elif value.hasAnnotation(u'priority'):
			return value
		elif True:
			return None
	
	def _applyComputationInfix(self, value, op, rvalue):
		lrvalue=self._getLeftmostComputation(rvalue)
		result=None
		if isinstance(rvalue, interfaces.ISelection):
			r=rvalue.getRule(0)
			e=r.getExpression()
			r.setExpression(self._createComputation(op, value, e.detach()))
			result = rvalue
		elif lrvalue:
			p1=self.getOperatorPriority(op)
			p2=self.getPriority(lrvalue)
			if (p1 >= p2):
				b=lrvalue.getLeftOperand().detach()
				c=self._createComputation(op, value, b)
				lrvalue.setLeftOperand(c)
				result = rvalue
		return (result or self._createComputation(op, value, rvalue))
	
	def _createComputation(self, op, lvalue, rvalue):
		""" A wrapper that transforms certain operators into either computation
		 or their dedicated counterpart."""
		if (op == u'..'):
			return F.enumerate(lvalue, rvalue).addAnnotation(u'operator', op).addAnnotation(u'priority', self.getOperatorPriority(op))
		elif ((op == u'%') and isinstance(lvalue, interfaces.IString)):
			return F.interpolate(lvalue, rvalue).addAnnotation(u'operator', op).addAnnotation(u'priority', self.getOperatorPriority(op))
		elif (op == u'.'):
			l=[rvalue]
			if rvalue.hasAnnotation(u'nested-invocation'):
				l = rvalue.getAnnotation(u'nested-invocation').getContent()
			for i in l:
				if isinstance(i, interfaces.IInvocation):
					for a in i.getArguments():
						v=a.getValue()
						if (isinstance(v, interfaces.IReference) and ((v.getReferenceName() == u'_') or (v.getReferenceName() == u'_0'))):
							nested=lvalue.detach().copy()
							a.setValue(nested)
							if rvalue.hasAnnotation(u'nested-invocation'):
								rvalue.getAnnotation(u'nested-invocation').getContent().append(nested)
							elif True:
								rvalue.setAnnotation(u'nested-invocation', [nested])
			return rvalue
		elif True:
			return F.compute(F._op(op, self.getOperatorPriority(op)), lvalue, rvalue)
	
	def onExpressionList(self, match):
		""" Returns a list of expressions [model.Expression]"""
		head=self.process(match[0])
		tail=self.process(match[1])
		res=[head]
		for _ in tail:
			res.append(_[1])
		return res
	
	def onExpressionLine(self, match):
		return self.process(match[0])
	
	def onExpressionBlock(self, match):
		""" Returns a list of expressions [model.Expression]"""
		lines=self.process(match[1])
		res=[]
		for _ in lines:
			v=_[2]
			if (v and (not isinstance(v, interfaces.IComment))):
				res = (res + _[2])
		return res
	
	def onNamedExpression(self, match):
		return self.process(match[u'value'])
	
	def onRestExpression(self, match):
		return self.process(match[u'value']).addAnnotation(u'ellipsis')
	
	def onNamedEntry(self, match):
		return self.process(match[0])
	
	def onNamedExpressionLine(self, match):
		return self.onExpressionLine(match)
	
	def onNamedExpressionList(self, match):
		comma=self.process(match[u'comma'])
		res=self.onExpressionList(match)
		if comma:
			res[-1].addAnnotation(u'continued')
		return res
	
	def onNamedExpressionBlock(self, match):
		return self.onExpressionBlock(match)
	
	def onLiteral(self, match):
		return self.process(match[0])
	
	def onPrefixes(self, match):
		return self.process(match[0])
	
	def onSuffixes(self, match):
		return self.process(match[0])
	
	def onComputationPrefix(self, match):
		operator=self.normalizeOperator(self.process(match[0])[0])
		operand=self.process(match[1])
		lrvalue=self._getLeftmostComputation(operand)
		result=None
		if (isinstance(operand, interfaces.ISelection) and operand.hasAnnotation(u'else-expression')):
			r=operand.getRule(0)
			r.setExpression(self._createComputation(operator, r.getExpression(), None))
			result = operand
		elif lrvalue:
			p1=self.getOperatorPriority(operator)
			p2=self.getPriority(lrvalue)
			if (p1 >= p2):
				b=lrvalue.getLeftOperand().detach()
				if ((operator == u'-') and isinstance(b, interfaces.INumber)):
					b.setActualValue((b.getActualValue() * -1))
				elif True:
					c=self._createComputation(operator, b, None)
					lrvalue.setLeftOperand(c)
				result = operand
		elif ((operator == u'-') and isinstance(operand, interfaces.INumber)):
			operand.setActualValue((operand.getActualValue() * -1))
			result = operand
		return (result or self._createComputation(operator, operand, None))
	
	def onParentheses(self, match):
		expr=self.process(match[1])
		expr.addAnnotation(u'parens')
		return expr
	
	def onException(self, match):
		return F.exception(self.process(match[1]))
	
	def onInstanciation(self, match):
		name=self.process(match[u'target'])[0]
		params=self.process(match[u'params'])[1]
		if not (isinstance(params, list) or isinstance(params, tuple)): params = (params,)
		return F.instanciate(name, *(params or []))
	
	def onArguments(self, match):
		value=self.process(match[0])
		args=[]
		if isinstance(value, interfaces.ITuple):
			args = value.values
		elif True:
			for _ in self._ensureList(value):
				if isinstance(_, interfaces.IElement):
					args.append(_)
		return args
	
	def onEventOperation(self, match, operator, name, value):
		""" Returns ("Invocation", [args])"""
		return [match.name, operator[0], name, value]
	
	def onInvocation(self, match):
		""" Returns ("Invocation", [args])"""
		args=self.process(match[0])
		return [match.name, args]
	
	def onInfixInvocation(self, match):
		name=self.process(match[u'name'])
		rvalue=self.process(match[u'rvalue'])
		return [match.name, name, rvalue]
	
	def onComputationInfix(self, match):
		""" Returns ("ComputationInfix", OPERATOR:String, Expression)"""
		return [match.name, self.normalizeOperator(self.process(match[0])[0]), self.process(match[1])]
	
	def onAccess(self, match):
		""" Returns [("Access", INDEX:Element)]"""
		return [match.name, self.process(match[1])]
	
	def onReference(self, match):
		slots=[self.process(match[0])]
		for _ in (self.process(match[1]) or []):
			slots.append(_[1])
		return slots
	
	def onOWhen(self, match):
		return F.annotation(u'when', self.process(match[u'expression']))
	
	def onOWhere(self, match):
		p=F.createBlock()
		n=self.process(match[u'name'])
		b=self.process(match[u'body'])
		d=self.process(match[u'doc'])
		self._addCode(p, b)
		if d:
			p.addAnnotation(d)
		return self.setSourceLocation(F.annotation(u'where', p), match)
	
	def onOExample(self, match):
		p=F.createBlock()
		n=self.process(match[u'name'])
		b=self.process(match[u'body'])[1]
		d=self.process(match[u'doc'])
		if d:
			b.addAnnotation(d)
		return self.setSourceLocation(F.annotation(u'example', b), match)
	
	def onCustomDecorator(self, match):
		""" Supports the transformation of decorator directive into invocations
		 using `_` to reference the function being decorated. The decorators
		 are added as annotation, and it's up to the backend to decide
		 how to properly interpret this."""
		name=self.process(match[u'name'])
		args=self.process(match[u'arguments'])
		if isinstance(args, interfaces.ITuple):
			args = args.getValues()
		elif True:
			args = [args]
		f=None
		ref=None
		for v in args:
			if (isinstance(v, interfaces.IReference) and ((v.getReferenceName() == u'_') or (v.getReferenceName() == u'_0'))):
				ref = v
				break
		if ref:
			f = F.invoke_args(name, args)
		elif (len(args) == 0):
			f = F.invoke(name, F._ref(u'_'))
		elif True:
			f = F.invoke(F.invoke_args(name, args), F._ref(u'_'))
		return F.annotation(u'decorator', f)
	
	def onDecomposition(self, match):
		""" Returns [("Decomposition", [ref:Reference])]"""
		return [match.name, self.process(match[0])[0], self.process(match[1])]
	
	def onSlice(self, match):
		start_index=self.process(match[1])
		end_index=self.process(match[3])
		return [match.name, start_index, end_index]
	
	def onChainLine(self, match):
		suffixes=[]
		for _ in self.process(match[u'content']):
			_ = _[0]
			if (not isinstance(_, interfaces.IComment)):
				if ((len(_) == 1) and isinstance(_[0], interfaces.IReference)):
					_ = [u'Decomposition', u' ', _]
				suffixes.append(_)
		return suffixes
	
	def onChain(self, match):
		""" Returns [("Chain", [ref:Reference])]"""
		type=self.process(match[u'type'])[0]
		lines=self.process(match[u'lines'])
		return [match.name, type, lines]
	
	def onAllocation(self, match):
		""" Returns a list of operations. If there's only one operation,
		 then it is a single allocation, otherwise it will be a mutliple
		 allocation with an automatic variable name."""
		res=None
		symbols=self.process(match[u'symbols'])
		rest=self.process(match[u'rest'])
		value=self.access(self.process(match[4]), 1)
		sel=None
		if (isinstance(value, list) and isinstance(value[0], interfaces.IAllocation)):
			sel = value
			value = F.resolve(F._ref(sel[0].getSlotName()))
		if ((len(symbols) == 1) and (not rest)):
			slot=F._slot(symbols[0][0].getReferenceName(), symbols[0][1])
			res = [F.allocate(slot, value)]
		elif True:
			res = []
			last_symbol=symbols[-1]
			pivot_slot=F._slot(last_symbol[0].getReferenceName(), last_symbol[1])
			res.append(F.allocate(pivot_slot, value))
			slot_value=F.resolve(F._ref(pivot_slot.getName()))
			i=0
			for s in symbols:
				slot=F._slot(s[0].getReferenceName(), s[1])
				sub_value=F.access(slot_value.copy(), F._number(i))
				if (s is last_symbol):
					res.append(F.assign(s[0].getReferenceName(), sub_value))
				elif True:
					res.append(F.allocate(slot, sub_value))
				i = (i + 1)
			if rest:
				slot=F._slot(rest[1].getReferenceName())
				sub_value=F.slice(slot_value.copy(), F._number(i))
				res.append(F.allocate(slot, sub_value))
		if sel:
			res = (sel + res)
		return res
	
	def onAssignment(self, match):
		before=self.process(match[u'before'])
		main=self.process(match[u'main'])
		rest=self.process(match[u'rest'])
		rvalue=self.process(match[u'op'])
		lvalue=main
		op=libparsing.ensure_str(rvalue[0][0])
		rvalue = rvalue[1]
		if (op == u'='):
			lvalue.addAnnotation(u'lvalue')
			return self.setSourceLocation(F.assign(lvalue, rvalue), match)
		elif (op == u'?='):
			predicate=F.compute(F._op(u'is'), lvalue, F._ref(u'Undefined'))
			assignment=F.assign(lvalue.copy().addAnnotation(u'lvalue'), rvalue)
			match_expr=F.matchExpression(predicate, assignment)
			res=F.select()
			res.addAnnotation(u'assignment')
			res.addRule(match_expr)
			return res
		elif True:
			res=None
			sub_op=self.normalizeOperator(op[0])
			c=self._createComputation(sub_op, lvalue, rvalue)
			return self.setSourceLocation(F.assign(lvalue.copy().detach().addAnnotation(u'lvalue'), c), match)
	
	def onAssignable(self, match):
		suffixes=[]
		for _ in (self.process(match[1]) or []):
			suffixes.append(_[0])
		prefix=self.process(match[0])
		return self._applySuffixes(prefix, suffixes)
	
	def onConditionSuffix(self, match):
		t=self.process(match[u'type'])[0]
		v=self.process(match[u'value'])
		return [match.name, t, v]
	
	def onTypeSuffix(self, match):
		t=self.process(match[u'type'])
		return [match.name, t]
	
	def onIterationSuffix(self, match):
		op=libparsing.ensure_str(self.process(match[u'op'])[0])
		rvalue=self.process(match[u'rvalue'])
		if (op == u'::'):
			if isinstance(rvalue, interfaces.IClosure):
				closure=rvalue
				if (len(closure.operations) > 0):
					lop=closure.operations[-1]
					if lop.hasAnnotation(u'implicit'):
						closure.removeOperationAt(-1)
						closure.addOperation(lop.getOpArgument(0))
			return [match.name, F.iterate, rvalue, op]
		elif (op == u'::?'):
			return [match.name, F.filter, rvalue, op]
		elif (op == u'::='):
			return [match.name, F.map, rvalue, op]
		elif (op == u'::>'):
			return [match.name, F.reduce, rvalue, op]
		elif (op == u'::<'):
			return [match.name, F.reduce, rvalue, op]
		elif True:
			raise ValueError(u'onIterationLine: Unsupported iteration operator: {0}'.format(op))
	
	def onTermination(self, match):
		return F.returns(self.process(match[1]))
	
	def onPass(self, match):
		return F.nop()
	
	def onContinue(self, match):
		return F.continues()
	
	def onBreak(self, match):
		return F.breaks()
	
	def onParameter(self, match):
		name_type=self.process(match[0])
		value=self._tryGet(self.process(match[1]), 1, None)
		return F._param(name_type[0].getReferenceName(), None, value)
	
	def onParameterList(self, match):
		res=[self.process(match[0])]
		ellipsis=self.process(match[2])
		for _ in self.process(match[1]):
			res.append(_[1])
		if ellipsis:
			res[-1].setRest(True)
		return res
	
	def onArgumentsEmpty(self, match):
		return []
	
	def onSymbolList(self, match):
		""" Returns `[model.Reference]`"""
		head=self.process(match[0])
		tail=(self.process(match[1]) or [])
		more=self.process(match[2])
		res=[head]
		for _ in tail:
			res.append(_[1])
		assert((not more))
		return res
	
	def onNameType(self, match):
		""" Returns a couple (name, type) where type might be None."""
		r=self.process(match[0])
		t=self.process(match[1])
		r.setAbstractType(t)
		return [r, t]
	
	def onFQName(self, match):
		""" A fully qualified name that will return an absolute reference"""
		head=self.process(match[0])
		tail=self.process(match[1])
		res=[head.getReferenceName()]
		for _ in tail:
			res.append(_[1].getReferenceName())
		if (len(res) == 1):
			return self.setSourceLocation(F._ref(res[0]), match)
		elif True:
			return self.setSourceLocation(F._absref(u'.'.join(res)), match)
	
	def onArray(self, match):
		list=(self.process(match[1]) or [])
		block=(self.process(match[2]) or [])
		return F._list((list + block))
	
	def onTuple(self, match):
		list=(self.process(match[1]) or [])
		block=(self.process(match[2]) or [])
		r=(list + block)
		if (len(r) == 1):
			if r[0].hasAnnotation(u'continued'):
				return F._tuple(r)
			elif True:
				return r[0].addAnnotation(u'parens')
		elif True:
			return F._tuple(r)
	
	def onMap(self, match):
		res=F._dict()
		head=(self.process(match[u'head']) or [])
		tail=(self.process(match[u'tail']) or [])
		for _ in (head + tail):
			if (_ and (not isinstance(_, interfaces.IComment))):
				res.setValue(_[0], _[1])
		if (len(tail) > 0):
			res.addAnnotation(u'block')
		elif True:
			res.addAnnotation(u'line')
		return res
	
	def onEntryList(self, match):
		res=[self.process(match[0])]
		for _ in self.process(match[1]):
			res.append(_[1])
		return res
	
	def onEntryLine(self, match):
		r=self.process(match[0])
		if isinstance(r, list):
			return r
		elif True:
			return [r]
	
	def onEntryBlock(self, match):
		res=[]
		for _ in self.process(match[u'content']):
			res = (res + _[2])
		return res
	
	def onEntry(self, match):
		return self.process(match[0])
	
	def onKeyValue(self, match):
		return [self.process(match[0]), self.process(match[2])]
	
	def onImplicitKey(self, match):
		name=self.process(match[0])
		return [name, F.resolve(F._ref(name.getActualValue()))]
	
	def onKey(self, match):
		res=self.process(match[0])
		if isinstance(res, interfaces.IElement):
			return res
		elif True:
			return res[1]
	
	def onEnum(self, match):
		name=self.process(match[u'name'])
		symbols=self._processList(self.process(match[u'symbols']))
		res=F.enum(name.getReferenceName())
		for s in symbols:
			res.addSymbol(F.symbol(s.getReferenceName()))
		self.setSourceLocation(res, match)
		return res
	
	def onType(self, match):
		name=self.process(match[u'name']).getName()
		parent=self.access(self.process(match[u'parent']), 1)
		value=(self.access(self.process(match[u'value']), 1) or [])
		doc=self.process(match[u'documentation'])
		body=self.process(match[u'body'])
		res=F.type(name, parent)
		if parent:
			res.addParent(parent)
		for c in value:
			res.addConstraint(c)
		if doc:
			res.setDocumentation(value)
		self.setSourceLocation(res, match)
		return res
	
	def onTypeEntryList(self, match):
		return self.onEntryList(match)
	
	def onTypeEntryLine(self, match):
		return self.onEntryLine(match)
	
	def onTypeEntryBlock(self, match):
		return self.onEntryBlock(match)
	
	def onTypeEntry(self, match):
		return [self.process(match[u'name']), self.process(match[u'value'])]
	
	def onTypeMap(self, match):
		res=[]
		head=(self.process(match[u'head']) or [])
		tail=(self.process(match[u'tail']) or [])
		for _ in (head + tail):
			if (_ and (not isinstance(_, interfaces.IComment))):
				res.append(F.typeSlot(_[0], _[1]))
		return res
	
	def onTypeValue(self, match):
		return self.process(match[0])
	
	def onTypeExpression(self, match):
		prefix=self.process(match[0])[0]
		suffixes=self.process(match[1])
		return prefix
	
	def onTypeReference(self, match):
		name=self.process(match[u'name'])[0]
		params=self.process(match[u'parameters'])
		return F._typeref(name, params)
	
	def onStringLine(self, match, indent, text):
		return (indent + text[0])
	
	def onStringMulti(self, match, start, lines, end):
		if start:
			insert(0, s)
		r=[]
		p=self._getCommonStringPrefix(lines)
		if p:
			i=len(p)
			for l in lines:
				r.append(l[i:])
		elif True:
			r = (r + lines)
		if end:
			r.append(end)
		return u'\\n'.join(r)
	
	def onStringMultiEnd(self, match, end):
		return end
	
	def _getCommonStringPrefix(self, stringList):
		""" Returns the shortest prefix common to all the strings in the
		 given list. This is used by mutli-line strings to prune the leading
		 spaces."""
		prefix=None
		j=100
		for l in stringList:
			if l:
				i=0
				k=len(l)
				while (((i < k) and (i < j)) and (l[i] in u'\t ')):
					i = (i + 1)
				p=l[0:i]
				if (prefix is None):
					prefix = l[0:i]
					j = min(i, j)
				elif True:
					i=0
					k=min(len(prefix), len(p))
					while ((i < k) and (prefix[i] == p[i])):
						i = (i + 1)
					if (i != k):
						prefix = p[0:k]
					j = min(k, j)
		return prefix
	
	def onSTRING_SQ(self, match):
		raw=self.process(match)[0]
		return eval((u'u' + raw))
	
	def onSTRING_DQ(self, match):
		raw=self.process(match)[0]
		return eval((u'u' + raw))
	
	def onSTRING_MQ(self, match):
		return eval((u'u' + self.process(match)[0]))
	
	def onSTRING_MQ_START(self, match):
		return self.process(match)[1]
	
	def onSTRING_MQ_END(self, match):
		return self.process(match)[1]
	
	def onString(self, match):
		text=self.process(match[0])
		return F._string(text)
	
	def onNUMBER(self, match):
		raw=self.process(match)[0]
		decoded=eval(raw)
		return F._number(decoded)
	
	def onNUMBER_UNIT(self, match):
		t=self.process(match)[0]
		v=0
		if t.endswith(u'deg'):
			v = (float(t[0:-3]) * math.PI)
		elif t.endswith(u'ms'):
			v = float(t[0:-2])
		elif t.endswith(u's'):
			v = (float(t[0:-1]) * 1000)
		elif t.endswith(u'm'):
			v = ((float(t[0:-1]) * 1000) * 60)
		elif t.endswith(u'h'):
			v = (((float(t[0:-1]) * 1000) * 60) * 60)
		elif t.endswith(u'd'):
			v = ((((float(t[0:-1]) * 1000) * 60) * 60) * 24)
		elif t.endswith(u'w'):
			v = (((((float(t[0:-1]) * 1000) * 60) * 60) * 24) * 7)
		elif True:
			raise Exception(u'Does not recognizes time format {0}'.format(t))
		return F._number(v)
	
	def onNumber(self, match):
		return self.process(match)[0]
	
	def onSYMBOLIC(self, match):
		raw_symbol=self.process(match)[0]
		if (raw_symbol == u'Undefined'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == u'None'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == u'Nothing'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == u'Timeout'):
			return F._symbol(raw_symbol)
		elif True:
			raise Exception((u'Unknown symbol:' + raw_symbol()))
	
	def onELLIPSIS(self, match):
		return u'...'
	
	def onNAME(self, match):
		name=self.process(match)[2]
		return F._ref(name)
	
	def onTYPE_KEY(self, match):
		return self.process(match)[0]
	
	def onKEY(self, match):
		return F._string(self.process(match)[0])
	
	def onDocumentation(self, match):
		lines=[]
		for l in self.process(match[0]):
			lines.append(l[1][0][1:])
		return self.setSourceLocation(F.doc(u'\n'.join(lines)), match)
	
	def onCOMMENT(self, match):
		return self.setSourceLocation(F.comment(self.process(match)[1:0]), match)
	
	def onComment(self, match):
		return self.process(match[u'text'])
	
	def onCheckIndent(self, match, tabs):
		return tabs[0]
	
	def onEOL(self, match):
		return None
	

