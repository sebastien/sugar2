#8< ---[sugar2/writer.py]---
#!/usr/bin/env python
import sys
__module__ = sys.modules[__name__]
import libparsing
from lambdafactory import interfaces
from lambdafactory.modelbase import Factory
import lambdafactory.passes as passes
import lambdafactory.resolution as resolution
__module_name__ = 'sugar2.writer'
__version__ = '0.9'
F = Factory()
class LambdaFactoryBuilder(libparsing.Processor):
	"""Converts a parse tree into a Lambda Factory program model, which can then
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
	OPERATORS = [['or'], ['and'], ['>', '>=', '<', '<=', '!=', '==', 'is', 'is not', 'in', 'not in'], ['..'], ['+', '-'], ['not'], ['/', '*', '%', '//'], ['/=', '*=', '%=', '+=', '-=', '=']]
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
			return self.path.split('/')[-1].split('.')[0].replace('-', '_')
		elif True:
			return '__current__'
	
	def normalizeOperator(self, operator):
		operator = operator.replace("\t"," ").replace("\n"," ")
		operator = " ".join((_.strip() for _ in operator.split() if _.strip()))
		
		return operator
	
	def getOperatorPriority(self, operator):
		i=0
		operator = libparsing.ensure_str(operator)
		for line in self.__class__.OPERATORS:
			if (operator in line):
				return i
			i = (i + 1)
		raise Exception(((('getOperatorPriority: Unknown operator ' + repr(operator)) + ', must be one of ') + repr(self.__class__.OPERATORS)))
	
	def _var(self, name=None, context=None):
		"""Lists the variables defined in the given context or gets the
		variable with the given name."""
		if name is None: name = None
		if context is None: context = self.context
		if (not name):
			return context.getVariables().keys()
		elif True:
			return context.getVariables().get(name)
	
	def _bind(self, scope, referanceable):
		"""Assigns the given referenceable to the current scope"""
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
		"""Returns only the elements of result that have a value"""
		return filter(lambda _:_, result)
		
	
	def _tryGet(self, list, index, default):
		"""Tries to get the `index`th element of `list` or returns `default`"""
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
		elif code:
			assert(False, 'Code element type not supported: {0}'.format(repr(code)))
		return element
	
	def _ensureList(self, value):
		if (not (isinstance(value, list) or isinstance(value, tuple))):
			return [value]
		elif True:
			return value
	
	def _ensureReturns(self, process):
		"""Ensures that the given process returns a value at the end"""
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
				last_operation.addAnnotation('last')
				return process
			elif isinstance(last_operation, interfaces.IOperation):
				process.removeOperationAt(-1)
				ret = F.returns(last_operation)
		if ret:
			ret.addAnnotation('implicit')
			process.addOperation(ret)
		return process
	
	def onModule(self, match):
		declaration=self.process(match[0])
		annotations={}
		for _ in declaration:
			if isinstance(_, interfaces.IAnnotation):
				annotations[_.getName()] = _.getContent()
		module=F.createModule((annotations.get('module') or self.getDefaultModuleName()))
		if annotations.get('version'):
			self._bind(module, F._moduleattr('VERSION', None, F._string(annotations.get('version'))))
		structure=self.process(match[1])
		code=self.process(match[2])
		init_function=F.createFunction(F.ModuleInit)
		self._addCode(init_function, code)
		self._bind(module, structure)
		self._bind(module, init_function)
		return module
	
	def onModuleAnnotation(self, match):
		ref=self.process(match[1])
		return F.annotation('module', ref.getReferenceName())
	
	def onVersionAnnotation(self, match):
		version=self.process(match[1])[0]
		return F.annotation('version', version)
	
	def onClass(self, match):
		name=self.process(match['name'])
		inherits=[]
		parents=[]
		for _ in (self.access(self.process(match['inherits']), 1) or []):
			if _:
				inherits.append(_)
		res=F.createClass(name, inherits)
		is_abstract=match[0]
		doc=self.process(match[5])
		body=self.process(match[7])
		res.setDocumentation(doc)
		res.setAbstract((is_abstract and True))
		self._bind(res, body)
		return res
	
	def onAttribute(self, match):
		name=self.process(match['name'])
		value=self.process(match['value'])
		doc=self.process(match['documentation'])
		res=F._attr(name[0].getReferenceName(), None, (value and value[1]))
		res.setDocumentation(doc)
		return res
	
	def onClassAttribute(self, match):
		name=self.process(match['name'])
		value=self.process(match['value'])
		doc=self.process(match['documentation'])
		res=F._classattr(name[0].getReferenceName(), None, (value and value[1]))
		res.setDocumentation((doc and doc[0]))
		return res
	
	def onModuleAttribute(self, match):
		name_type=self.process(match[2])
		value=self._tryGet(self.process(match[3]), 1, None)
		doc=self.process(match[5])
		res=F._moduleattr(name_type[0].getReferenceName(), None, value)
		res.setDocumentation((doc and doc[0]))
		return res
	
	def _createCallable(self, factory, match):
		name_type=self.process(match['name'])
		params=self.access(self.process(match['parameters'])[0], 0)
		doc=self.process(match['documentation'])
		body=self.process(match['body'])
		fun=None
		if (name_type is True):
			fun = factory(params)
		elif True:
			fun = factory(name_type[0].getReferenceName(), params)
		fun.setDocumentation(doc)
		self._addCode(fun, body)
		return fun
	
	def onOperation(self, match):
		return self._createCallable(F.createClassMethod, match)
	
	def onAbstractOperation(self, match):
		res=self._createCallable(F.createClassMethod, match)
		res.setAbstract(True)
		return res
	
	def onMethod(self, match):
		return self._createCallable(F.createMethod, match)
	
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
		"""Returns an `Element` or a list of `[Element]`. Typically these elements
		would be Comments, Blocks or Operations."""
		return self.process(match[0])
	
	def onConditionalLine(self, match):
		return self.onConditionalBlock(match)
	
	def onConditionalBlock(self, match):
		_if=self.process(match['if'])
		_elifs=self.process(match['elif'])
		_else=self.process(match['else'])
		res=F.select()
		res.addRule(F.matchProcess(_if[0], _if[1]))
		for _ in _elifs:
			res.addRule(F.matchProcess(_[0], _[1]))
		if _else:
			res.addRule(F.matchProcess(F._ref('True'), _else[0]))
		return res
	
	def onConditional(self, match):
		return self.process(match[0])
	
	def onIfBlock(self, match):
		block=F.createBlock()
		self._addCode(block, self.process(match['body']))
		return [self.process(match['condition']), block]
	
	def onIfLine(self, match):
		return self.onIfBlock(match)
	
	def onElifBlock(self, match):
		return self.onIfBlock(match)
	
	def onElifLine(self, match):
		return self.onElifBlock(match)
	
	def onElseBlock(self, match):
		block=F.createBlock()
		self._addCode(block, self.process(match['body']))
		return [block]
	
	def onElseLine(self, match):
		return self.onElseBlock(match)
	
	def onIteration(self, match):
		return self.process(match['for'])
	
	def onRepetition(self, match):
		return self.process(match['while'])
	
	def onTry(self, match):
		return F.intercept(self.process(match['try']), self.process(match['catch']), self.process(match['finally']))
	
	def onForBlock(self, match):
		params=self.process(match['params'])
		expr=self.process(match['expr'])
		body=self.process(match['body'])
		block=F.createClosure(params)
		self._addCode(block, body)
		return F.iterate(expr, block)
	
	def onWhileBlock(self, match):
		condition=self.process(match['condition'])
		body=self.process(match['body'])
		block=F.createBlock()
		self._addCode(block, body)
		return F.repeat(condition, block)
	
	def onTryBlock(self, match):
		body=self.process(match['body'])
		block=F.createBlock()
		self._addCode(block, body)
		return block
	
	def onCatchBlock(self, match):
		body=self.process(match['body'])
		param=self.process(match['param'])
		args=[F._param(param[0].getReferenceName())]
		block=F.createClosure(args)
		self._addCode(block, body)
		return block
	
	def onFinallyBlock(self, match):
		body=self.process(match['body'])
		block=F.createBlock()
		self._addCode(block, body)
		return block
	
	def onBlockBody(self, match):
		return self.process(match['body'])
	
	def onBlockLine(self, match):
		return self.process(match['body'])
	
	def onEmbed(self, match):
		body=self.process(match['body'])
		language=self.process(match['language'])
		if language:
			language = language.getName()
		lines=[]
		for line in body:
			lines.append(line[1][0][1:])
		return F.embed(language, '\n'.join(lines))
	
	def onExpression(self, match):
		prefix=self.process(match[0])
		suffixes=self.process(match[1])
		current=None
		if ((isinstance(prefix, interfaces.ILiteral) or isinstance(prefix, interfaces.IValue)) or isinstance(prefix, interfaces.IClosure)):
			current = prefix
		elif (((((isinstance(prefix, interfaces.IComputation) or isinstance(prefix, interfaces.IResolution)) or isinstance(prefix, interfaces.IInvocation)) or isinstance(prefix, interfaces.IInstanciation)) or isinstance(prefix, interfaces.IAccessOperation)) or isinstance(prefix, interfaces.IExcept)):
			current = prefix
		elif isinstance(prefix, interfaces.IReference):
			current = F.resolve(prefix)
		elif True:
			raise Exception(('Prefix not supported yet: ' + str(prefix)))
		current = self._applySuffixes(current, suffixes)
		if isinstance(current, interfaces.IComputation):
			current = self._reorderComputation(current)
		return current
	
	def _reorderComputation(self, value):
		"""Reorders a sequence of computations according to operators priorities.
		This method is called by `onExpression` and applied from right
		to left."""
		b=value.getRightOperand()
		if (isinstance(b, interfaces.IComputation) and (not b.hasAnnotation('parens'))):
			op1=value.getOperator()
			op2=b.getOperator()
			op1_p=op1.getPriority()
			op2_p=op2.getPriority()
			if (op1_p >= op2_p):
				a=value.getLeftOperand().detach()
				c=b.getLeftOperand().detach()
				d=b.getRightOperand().detach()
				o1=value.getOperator().detach()
				o2=b.getOperator().detach()
				value.setOperator(o2)
				value.setRightOperand(d)
				b.detach()
				b.setLeftOperand(a)
				b.setOperator(o1)
				b.setRightOperand(c)
				value.setLeftOperand(self._reorderComputation(b))
			return value
		elif True:
			return value
	
	def _applySuffixes(self, value, suffixes):
		"""Applies the suffixes to the current value, modifying it"""
		if suffixes:
			for args in suffixes:
				name=args[0]
				if (name == 'Invocation'):
					if ((type(args[1]) == list) or (type(args[1]) == tuple)):
						value = F.invoke_args(value, args[1])
					elif True:
						value = F.invoke(value, args[1])
				elif (name == 'ComputationInfix'):
					op=self.normalizeOperator(args[1])
					if (op == '..'):
						value = F.enumerate(value, args[2])
					elif True:
						value = F.compute(F._op(op, self.getOperatorPriority(op)), value, args[2])
				elif (name == 'Decomposition'):
					for _ in args[1]:
						value = F.resolve(_, value)
				elif (name == 'Access'):
					value = F.access(value, args[1])
				elif (name == 'Slice'):
					value = F.slice(value, args[1], args[2])
				elif (name == 'Chain'):
					alloc=value
					ref=None
					if (not isinstance(alloc, interfaces.IAllocation)):
						name=(('_c' + str(self.varcounter)) + '_')
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
					raise Exception(((('sugar2.writer._applySuffixes: Suffix not supported yet: ' + str(name)) + ' in ') + str(args)))
		return value
	
	def onExpressionList(self, match):
		"""Returns a list of expressions [model.Expression]"""
		head=self.process(match[0])
		tail=self.process(match[1])
		res=[head]
		for _ in tail:
			res.append(_[1])
		return res
	
	def onExpressionBlock(self, match):
		"""Returns a list of expressions [model.Expression]"""
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
		expr.addAnnotation('parens')
		return expr
	
	def onException(self, match):
		return F.exception(self.process(match[1]))
	
	def onInstanciation(self, match):
		name=self.process(match['target'])[0]
		params=self.process(match['params'])[1]
		if not (isinstance(params, list) or isinstance(params, tuple)): params = (params,)
		return F.instanciate(name, *(params or []))
		
	
	def onInvocation(self, match):
		"""Returns ("Invocation", [args])"""
		value=self.process(match[0])
		args=[]
		for _ in self._ensureList(value):
			if isinstance(_, interfaces.IElement):
				args.append(_)
		return [match.name, args]
	
	def onComputationInfix(self, match):
		"""Returns ("ComputationInfix", OPERATOR:String, Expression)"""
		return [match.name, self.process(match[0])[0].strip(), self.process(match[1])]
	
	def onAccess(self, match):
		"""Returns [("Access", INDEX:Element)]"""
		return [match.name, self.process(match[1])]
	
	def onReference(self, match):
		slots=[self.process(match[0])]
		for _ in (self.process(match[1]) or []):
			slots.append(_[1])
		return slots
	
	def onDecomposition(self, match):
		"""Returns [("Decomposition", [ref:Reference])]"""
		return [match.name, self.process(match[1])]
	
	def onSlice(self, match):
		start_index=self.process(match[1])
		end_index=self.process(match[3])
		return [element.name, start_index, end_index]
	
	def onChainLine(self, match):
		suffixes=[]
		for _ in self.process(match[3]):
			_ = _[0]
			if ((len(_) == 1) and isinstance(_[0], interfaces.IReference)):
				_ = ['Decomposition', _]
			suffixes.append(_)
		return suffixes
	
	def onChain(self, match):
		"""Returns [("Decomposition", [ref:Reference])]"""
		lines=self.process(match[1])
		return [match.name, lines]
	
	def onAllocation(self, match):
		"""Returns a list of operations. If there's only one operation,
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
			temp_slot=F._slot()
			res.append(F.allocate(temp_slot, value))
			slot_value=F.resolve(F._ref(temp_slot.getName()))
			i=0
			for s in symbols:
				slot=F._slot(s.getReferenceName())
				sub_value=F.access(slot_value.copy(), F._number(i))
				res.append(F.allocate(slot, sub_value))
				i = (i + 1)
			if rest:
				slot=F._slot(rest.getReferenceName())
				sub_value=F.slice(slot_value.copy(), i)
				res.append(F.allocate(slot, sub_value))
		return res
	
	def onAssignment(self, match):
		before=self.process(match['before'])
		main=self.process(match['main'])
		rest=self.process(match['rest'])
		rvalue=self.process(match['op'])
		lvalue=main
		op=libparsing.ensure_str(rvalue[0][0])
		rvalue = rvalue[1]
		if (op == '='):
			return F.assign(lvalue, rvalue)
		elif (op == '?='):
			predicate=F.compute(F._op('not'), lvalue)
			assignment=F.assign(lvalue.copy(), rvalue)
			match=F.matchExpression(predicate, assignment)
			res=F.select()
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
	
	def onIterationLine(self, match):
		op=libparsing.ensure_str(self.process(match[1])[0])
		if (op == '::'):
			closure=self.process(match[2])
			if (len(closure.operations) > 0):
				lop=closure.operations[-1]
				if lop.hasAnnotation('implicit'):
					closure.removeOperationAt(-1)
					closure.addOperation(lop.getOpArgument(0))
			return F.iterate(self.process(match[0]), closure)
		elif (op == '::?'):
			return F.filter(self.process(match[0]), self.process(match[2]))
		elif (op == '::='):
			return F.map(self.process(match[0]), self.process(match[2]))
		elif (op == '::<'):
			return F.reduce(self.process(match[0]), self.process(match[2]))
		elif True:
			raise ValueError('onIterationLine: Unsupported iteration operator: {0}'.format(op))
	
	def onTermination(self, match):
		return F.returns(self.process(match[1]))
	
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
		line=(self.process(match['line']) or [])
		body=(self.process(match['body']) or [])
		return self.filterNull((line + body))
	
	def onSymbolList(self, match):
		"""Returns `[model.Reference]`"""
		head=self.process(match[0])
		tail=(self.process(match[1]) or [])
		more=self.process(match[2])
		res=[head]
		for _ in tail:
			res.append(_[1])
		assert((not more))
		return res
	
	def onNameType(self, match):
		"""Returns a couple (name, type) where type might be None."""
		return [self.process(match[0]), self.process(match[1])]
	
	def onFQName(self, match):
		"""A fully qualified name that will return an absolute reference"""
		head=self.process(match[0])
		tail=self.process(match[1])
		res=[head.getReferenceName()]
		for _ in tail:
			res.append(_[1].getReferenceName())
		full_name='.'.join(res)
		return F._absref(full_name)
	
	def onArray(self, match):
		list=(self.process(match[1]) or [])
		block=(self.process(match[2]) or [])
		return F._list((list + block))
	
	def onMap(self, match):
		res=F._dict()
		head=(self.process(match['head']) or [])
		tail=(self.process(match['tail']) or [])
		for _ in (head + tail):
			if _:
				res.setValue(_[0], _[1])
		if (len(tail) > 0):
			res.addAnnotation('block')
		elif True:
			res.addAnnotation('line')
		return res
	
	def onKeyValueList(self, match):
		res=[self.process(match[0])]
		for _ in self.process(match[1]):
			res.append(_[1])
		return res
	
	def onKeyValueBlock(self, match):
		res=[]
		for _ in self.process(match[1]):
			res = (res + _[2])
		return res
	
	def onKeyValue(self, match):
		return [self.process(match[0]), self.process(match[2])]
	
	def onKey(self, match):
		res=self.process(match[0])
		if isinstance(res, interfaces.IElement):
			return res
		elif True:
			return res[1]
	
	def onString(self, match):
		raw=self.process(match[0])[0]
		decoded=eval(raw)
		return F._string(decoded)
	
	def onNUMBER(self, match):
		raw=self.process(match)[0]
		decoded=eval(raw)
		return F._number(decoded)
	
	def onSYMBOLIC(self, match):
		raw_symbol=self.process(match)[0]
		if (raw_symbol == 'Undefined'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == 'None'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == 'Nothing'):
			return F._symbol(raw_symbol)
		elif (raw_symbol == 'Timeout'):
			return F._symbol(raw_symbol)
		elif True:
			raise Exception(('Unknown symbol:' + raw_symbol()))
	
	def onNAME(self, match):
		return F._ref(self.process(match)[2])
	
	def onKEY(self, match):
		return F._string(self.process(match)[0])
	
	def onDocumentation(self, match):
		lines=[]
		for l in self.process(match[0]):
			lines.append(l[1][0][1:])
		return F.doc('\n'.join(lines))
	
	def onCOMMENT(self, match):
		return F.comment(self.process(match)[1:0])
	
	def onCheckIndent(self, match):
		return None
	
	def onEOL(self, match):
		return None
	

