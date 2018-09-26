#8< ---[sugar2/v1/writer.py]---
#!/usr/bin/env python
# encoding: utf-8
import sys
__module__ = sys.modules[__name__]
import libparsing
from lambdafactory import interfaces
from lambdafactory.modelbase import Factory
import lambdafactory.passes as passes
import lambdafactory.resolution as resolution
__module_name__ = 'sugar2.v1.writer'
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
	OPERATORS = [[u'or'], [u'and'], [u'not'], [u'>', u'>=', u'<', u'<=', u'!=', u'==', u'is', u'is not', u'in', u'not in'], [u'::', u'::<', u'::>', u'::?', u'::='], [u'..', u'‥'], [u'+', u'-'], [u'|', u'&', u'<<', u'>>'], [u'/', u'*', u'%', u'//'], [u'/=', u'*=', u'%=', u'+=', u'-=', u'=']]
	OPERATORS_NORMALIZED = {'||':u'|', '&&':u'&'}
	def __init__ (self, grammar, path=None):
		self.module = None
		self.path = None
		self.processes = []
		self.varcounter = 0
		if path is None: path = None
		libparsing.Processor.__init__(self,grammar)
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
		if isinstance(res, interfaces.IElement):
			pass
		return res
	
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
	
	def getOperatorPriority(self, operator):
		i=0
		operator = libparsing.ensure_str(operator)
		for line in self.__class__.OPERATORS:
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
		elif code:
			raise Exception(u'Code element type not supported: {0}'.format(repr(code)))
		return element
	
	def _ensureList(self, value):
		if (not (isinstance(value, list) or isinstance(value, tuple))):
			return [value]
		elif True:
			return value
	
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
		structure=self.process(match[1])
		code=self.process(match[2])
		init_function=F.createFunction(F.ModuleInit)
		self._addCode(init_function, code)
		self._bind(module, structure)
		self._bind(module, init_function)
		return module
	
	def onModuleAnnotation(self, match):
		ref=self.process(match[1])
		return F.annotation(u'module', ref.getReferenceName())
	
	def onVersionAnnotation(self, match):
		version=self.process(match[1])[0]
		return F.annotation(u'version', version)
	
	def onClass(self, match):
		name=self.process(match[u'name']).getReferenceName()
		inherits=[]
		parents=[]
		for _ in (self.access(self.process(match[u'inherits']), 1) or []):
			if isinstance(_, interfaces.IReference):
				inherits.append(_)
			elif True:
				for v in _:
					inherits.append(v[0])
		res=F.createClass(name, inherits)
		is_abstract=match[0]
		doc=self.process(match[5])
		body=self.process(match[7])
		res.setDocumentation(doc)
		res.setAbstract((is_abstract and True))
		self._bind(res, body)
		return res
	
	def onInterface(self, match):
		name=self.process(match[u'name']).getReferenceName()
		inherits=[]
		parents=[]
		for _ in (self.access(self.process(match[u'inherits']), 1) or []):
			if isinstance(_, interfaces.IReference):
				inherits.append(_)
			elif True:
				for v in _:
					inherits.append(v[0])
		res=F.createInterface(name, inherits)
		is_abstract=match[0]
		doc=self.process(match[4])
		body=self.process(match[6])
		res.setDocumentation(doc)
		res.setAbstract((is_abstract and True))
		self._bind(res, body)
		return res
	
	def onAttribute(self, match):
		name=self.process(match[u'name'])
		value=self.process(match[u'value'])
		doc=self.process(match[u'documentation'])
		res=F._attr(name[0].getReferenceName(), None, (value and value[1]))
		res.setDocumentation(doc)
		return res
	
	def onClassAttribute(self, match):
		name=self.process(match[u'name'])
		value=self.process(match[u'value'])
		doc=self.process(match[u'documentation'])
		res=F._classattr(name[0].getReferenceName(), None, (value and value[1]))
		res.setDocumentation(doc)
		return res
	
	def onModuleAttribute(self, match):
		name_type=self.process(match[2])
		value=self._tryGet(self.process(match[3]), 1, None)
		doc=self.process(match[5])
		res=F._moduleattr(name_type[0].getReferenceName(), None, value)
		res.setDocumentation(doc)
		return res
	
	def _createCallable(self, factory, match, hasBody=None):
		if hasBody is None: hasBody = True
		name_type=self.process(match[u'name'])
		try:
			match["parameters"]
		except KeyError:
			import ipdb;ipdb.set_trace()
		params=self.access(self.access(self.process(match[u'parameters']), 0), 0)
		doc=self.process(match[u'documentation'])
		body=((hasBody and self.process(match[u'body'])) or None)
		dec=self.process(match[u'decorators'])
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
		return fun
	
	def onClassMethod(self, match):
		return self._createCallable(F.createClassMethod, match)
	
	def onAbstractClassMethod(self, match):
		return self._createCallable(F.createClassMethod, match, False)
	
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
	
	def onClosureLine(self, match):
		return self.process(match[2])
	
	def onClosureStatement(self, match):
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
		params=self.process(match[1])
		code=self.process(match[3])
		res=F.createClosure(params)
		self._addCode(res, code)
		return res
	
	def onImportSymbol(self, match):
		return [self.process(match[0])[0][0], self.process(match[1])]
	
	def onImportOrigin(self, match):
		return self.process(match[1])[0]
	
	def onImportAlias(self, match):
		return self.process(match[1]).getReferenceName()
	
	def onImport(self, match):
		name=self.process(match[1])
		names=self.process(match[2])
		origin=self.process(match[3])
		symbols=[]
		names   = [_[1] for _ in names]
		if not origin:
			symbols = [F.importModule(_[0], _[1]) for _ in [name] + (names or [])]
		else:
			symbols = [F.importSymbol(_[0], origin, _[1]) for _ in [name] + (names or [])]
		if (not origin):
			if (len(names) == 0):
				return F.importModule(name[0], name[1])
			elif True:
				assert((not origin))
				return F.importModules(symbols)
		elif True:
			if (len(names) == 0):
				return F.importSymbol(name[0], origin, name[1])
			elif True:
				return F.importSymbols(symbols, origin)
	
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
	
	def onConditionalExpression(self, match):
		c=self.process(match[u'condition'])
		t=self.process(match[u'true'])
		f=self.process(match[u'false'])
		res=F.select()
		res.addRule(F.matchExpression(c, t))
		if f:
			e=F.matchExpression(F._ref(u'True'), f)
			e.addAnnotation(u'else')
			res.addRule(e)
		res.addAnnotation(u'if-expression')
		return res
	
	def onConditionalLine(self, match):
		return self.onConditionalBlock(match)
	
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
	
	def onTryBlock(self, match):
		body=self.process(match[u'body'])
		block=F.createBlock()
		self._addCode(block, body)
		return block
	
	def onCatchBlock(self, match):
		body=self.process(match[u'body'])
		param=self.process(match[u'param'])
		args=[F._param(param[0].getReferenceName())]
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
	
	def onEmbed(self, match):
		body=self.process(match[u'body'])
		language=self.process(match[u'language'])
		if language:
			language = language.getName()
		lines=[]
		for line in body:
			lines.append(line[1][0][1:])
		return F.embed(language, u'\n'.join(lines))
	
	def onExpression(self, match):
		prefix=self.process(match[0])
		suffixes=self.process(match[1])
		current=None
		if ((isinstance(prefix, interfaces.ILiteral) or isinstance(prefix, interfaces.IValue)) or isinstance(prefix, interfaces.IClosure)):
			current = prefix
		elif ((((((((isinstance(prefix, interfaces.IComputation) or isinstance(prefix, interfaces.IResolution)) or isinstance(prefix, interfaces.IInvocation)) or isinstance(prefix, interfaces.IInstanciation)) or isinstance(prefix, interfaces.IAccessOperation)) or isinstance(prefix, interfaces.IExcept)) or isinstance(prefix, interfaces.ISelection)) or isinstance(prefix, interfaces.IEnumeration)) or isinstance(prefix, interfaces.IIteration)):
			current = prefix
		elif isinstance(prefix, interfaces.IReference):
			current = F.resolve(prefix)
		elif True:
			raise Exception((u'Prefix not supported yet: ' + str(prefix)))
		current = self._applySuffixes(current, suffixes)
		if isinstance(current, interfaces.IBinaryOperation):
			current = self._reorderComputation(current)
		return current
	
	def _reorderComputation(self, value):
		""" Reorders a sequence of computations according to operators priorities.
		 This method is called by `onExpression` and applied from right
		 to left."""
		if (((not isinstance(value, interfaces.IComputation)) or value.hasAnnotation(u'parens')) or value.hasAnnotation(u'reordered')):
			return value
		op1=value.getOperator()
		a=value.getLeftOperand()
		b=value.getRightOperand()
		if value.isUnary():
			if ((isinstance(a, interfaces.IComputation) and (not a.hasAnnotation(u'parens'))) and (not a.hasAnnotation(u'reordered'))):
				op2=a.getOperator()
				if (op1.getPriority() > op2.getPriority()):
					c=a.getLeftOperand()
					d=a.getRightOperand()
					value = F.compute(op2.detach(), self._reorderComputation(F.compute(op1.detach(), c.detach())), d.detach())
			return value
		elif True:
			b=value.getRightOperand()
			if ((isinstance(b, interfaces.IComputation) and (not b.hasAnnotation(u'parens'))) and (not b.hasAnnotation(u'reordered'))):
				op2=b.getOperator()
				if (op1.getPriority() >= op2.getPriority()):
					c=b.getLeftOperand()
					d=b.getRightOperand()
					value = F.compute(op2.detach(), self._reorderComputation(F.compute(op1.detach(), a.detach(), c.detach())), ((d and self._reorderComputation(d.detach())) or None))
				return value
			elif True:
				return value
	
	def _applySuffixes(self, value, suffixes):
		""" Applies the suffixes to the current value, modifying it"""
		if suffixes:
			for args in suffixes:
				name=args[0]
				if (name == u'Invocation'):
					if ((type(args[1]) == list) or (type(args[1]) == tuple)):
						value = F.invoke_args(value, args[1])
					elif True:
						value = F.invoke(value, args[1])
				elif (name == u'ComputationInfix'):
					op=self.normalizeOperator(args[1])
					if (op == u'..'):
						rvalue=args[2]
						if (isinstance(rvalue, interfaces.IIteration) and (not rvalue.hasAnnotation(u'parens'))):
							value = F.enumerate(value, rvalue.getLeftOperand().detach())
							rvalue.setLeftOperand(value)
							value = rvalue
						elif True:
							value = F.enumerate(value, args[2])
					elif True:
						value = F.compute(F._op(op, self.getOperatorPriority(op)), value, args[2])
				elif (name == u'Decomposition'):
					for _ in args[1]:
						value = F.resolve(_, value)
				elif (name == u'Access'):
					value = F.access(value, args[1])
				elif (name == u'Slice'):
					value = F.slice(value, args[1], args[2])
				elif (name == u'IterationSuffix'):
					value = args[1](value, args[2])
				elif (name == u'Chain'):
					if (type(value) is list):
						ipdb.set_trace()
					alloc=value
					ref=None
					if (not isinstance(alloc, interfaces.IAllocation)):
						name=((u'_c' + str(self.varcounter)) + u'_')
						self.varcounter = (self.varcounter + 1)
						slot=F._slot(name)
						alloc=F.allocate(slot, value)
						ref = F._ref(name)
					elif True:
						ref = alloc.getSlot()
					res=[alloc]
					for g in (args[1] or []):
						res.append(self._applySuffixes(ref.copy(), g))
					value = res
				elif True:
					raise Exception((((u'sugar2.writer._applySuffixes: Suffix not supported yet: ' + str(name)) + u' in ') + str(args)))
		return value
	
	def onExpressionList(self, match):
		""" Returns a list of expressions [model.Expression]"""
		head=self.process(match[0])
		tail=self.process(match[1])
		res=[head]
		for _ in tail:
			res.append(_[1])
		return res
	
	def onExpressionBlock(self, match):
		""" Returns a list of expressions [model.Expression]"""
		lines=self.process(match[1])
		res=[]
		for _ in lines:
			res = (res + _[2])
		return res
	
	def onLiteral(self, match):
		return self.process(match[0])
	
	def onPrefixes(self, match):
		return self.process(match[0])
	
	def onSuffixes(self, match):
		return self.process(match[0])
	
	def onComputationPrefix(self, match):
		operator=self.normalizeOperator(self.process(match[0])[0])
		operand=self.process(match[1])
		return F.compute(F._op(operator, self.getOperatorPriority(operator)), operand)
	
	def onParentheses(self, match):
		expr=self.process(match[1])
		expr = self._reorderComputation(expr)
		expr.addAnnotation(u'parens')
		return expr
	
	def onException(self, match):
		return F.exception(self.process(match[u'expression']))
	
	def onInstanciation(self, match):
		name=self.process(match[u'target'])[0]
		params=self.process(match[u'params'])[1]
		if not (isinstance(params, list) or isinstance(params, tuple)): params = (params,)
		return F.instanciate(name, *(params or []))
	
	def onInvocation(self, match):
		""" Returns ("Invocation", [args])"""
		value=self.process(match[0])
		args=[]
		for _ in self._ensureList(value):
			if isinstance(_, interfaces.IElement):
				args.append(_)
		return [match.name, args]
	
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
	
	def onDecomposition(self, match):
		""" Returns [("Decomposition", [ref:Reference])]"""
		return [match.name, self.process(match[1])]
	
	def onSlice(self, match):
		start_index=self.process(match[1])
		end_index=self.process(match[3])
		return [match.name, start_index, end_index]
	
	def onChainLine(self, match):
		suffixes=[]
		for _ in self.process(match[3]):
			_ = _[0]
			if ((len(_) == 1) and isinstance(_[0], interfaces.IReference)):
				_ = [u'Decomposition', _]
			suffixes.append(_)
		return suffixes
	
	def onChain(self, match):
		""" Returns [("Decomposition", [ref:Reference])]"""
		lines=self.process(match[1])
		return [match.name, lines]
	
	def onAllocation(self, match):
		""" Returns a list of operations. If there's only one operation,
		 then it is a single allocation, otherwise it will be a mutliple
		 allocation with an automatic variable name."""
		res=None
		symbols=self.process(match[2])
		rest=self.process(match[3])
		value=self.access(self.process(match[4]), 1)
		if ((len(symbols) == 1) and (not rest)):
			slot=F._slot(symbols[0].getReferenceName())
			res = [F.allocate(slot, value)]
		elif True:
			res = []
			last_symbol=symbols[-1]
			pivot_slot=F._slot(last_symbol.getReferenceName())
			res.append(F.allocate(pivot_slot, value))
			slot_value=F.resolve(F._ref(pivot_slot.getName()))
			i=0
			for s in symbols:
				slot=F._slot(s.getReferenceName())
				sub_value=F.access(slot_value.copy(), F._number(i))
				if (s is last_symbol):
					res.append(F.assign(s.getReferenceName(), sub_value))
				elif True:
					res.append(F.allocate(slot, sub_value))
				i = (i + 1)
			if rest:
				slot=F._slot(rest.getReferenceName())
				sub_value=F.slice(slot_value.copy(), i)
				res.append(F.allocate(slot, sub_value))
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
			return F.assign(lvalue, rvalue)
		elif (op == u'?='):
			predicate=F.compute(F._op(u'is'), lvalue, F._ref(u'Undefined'))
			assignment=F.assign(lvalue.copy(), rvalue)
			match=F.matchExpression(predicate, assignment)
			res=F.select()
			res.addAnnotation(u'assignment')
			res.addRule(match)
			return res
		elif True:
			res=None
			sub_op=self.normalizeOperator(op[0])
			c=F.compute(F._op(sub_op, self.getOperatorPriority(sub_op)), lvalue, rvalue)
			return F.assign(lvalue.copy().detach(), c)
	
	def onAssignable(self, match):
		suffixes=[]
		for _ in (self.process(match[1]) or []):
			suffixes.append(_[0])
		prefix=self.process(match[0])
		return self._applySuffixes(prefix, suffixes)
	
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
	
	def onArgumentsMany(self, match):
		line=(self.process(match[u'line']) or [])
		body=(self.process(match[u'body']) or [])
		return self.filterNull((line + body))
	
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
		return [self.process(match[0]), self.process(match[1])]
	
	def onFQName(self, match):
		""" A fully qualified name that will return an absolute reference"""
		head=self.process(match[0])
		tail=self.process(match[1])
		res=[head.getReferenceName()]
		for _ in tail:
			res.append(_[1].getReferenceName())
		if (len(res) == 1):
			return F._ref(res[0])
		elif True:
			return F._absref(u'.'.join(res))
	
	def onArray(self, match):
		list=(self.process(match[1]) or [])
		block=(self.process(match[2]) or [])
		return F._list((list + block))
	
	def onMap(self, match):
		res=F._dict()
		head=(self.process(match[u'head']) or [])
		tail=(self.process(match[u'tail']) or [])
		for _ in (head + tail):
			if _:
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
	
	def onEntryBlock(self, match):
		res=[]
		for _ in self.process(match[1]):
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
	
	def onString(self, match):
		raw=self.process(match[0])[0]
		decoded=eval((u'u' + raw))
		return F._string(decoded)
	
	def onNUMBER(self, match):
		raw=self.process(match)[0]
		decoded=eval(raw)
		return F._number(decoded)
	
	def onTIME(self, match):
		t=self.process(match)[0]
		v=0
		if t.endswith(u'ms'):
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
	
	def onNAME(self, match):
		name=self.process(match)[2]
		return F._ref(name)
	
	def onKEY(self, match):
		return F._string(self.process(match)[0])
	
	def onDocumentation(self, match):
		lines=[]
		for l in self.process(match[0]):
			lines.append(l[1][0][1:])
		return F.doc(u'\n'.join(lines))
	
	def onCOMMENT(self, match):
		return F.comment(self.process(match)[1:0])
	
	def onComment(self, match):
		return self.process(match[u'text'])
	
	def onCheckIndent(self, match):
		return None
	
	def onEOL(self, match):
		return None
	

