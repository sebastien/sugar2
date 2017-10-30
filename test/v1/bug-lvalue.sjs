# -----------------------------------------------------------------------------
# Project   : FF-Kit/Interaction
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre                            <sebastien@ffctn.com>
# License   : Proprietary
# -----------------------------------------------------------------------------
# Creation  : 27-Sep-2012
# Last mod  : 06-Jun-2014
# -----------------------------------------------------------------------------

@module  interaction
@version 1.5.1
| The goal of the `interactions` module is to provide a consistent way to
| interactive with devices (mouse, touch, etc), allowing to handle both
| each devices basic events (down, up, touch, etc) and combinations of
| events (aka "gestures") such as click, drag, swipe, etc.
|
| One of the key element here is that the interactions module can allow
| to define specific handlers for each device and attach specific gesture
| per specific devices -- allowing to implement mouse-based interaction
| in a different way than touch-based interaction.


@shared $        = jQuery
@shared LICENSE  = "http://ffctn.com/doc/licenses/bsd"
@shared LAST_INTERACTION = Undefined
@shared GESTURES = {}

# SEE: List of events - https://developer.mozilla.org/en-US/docs/Web/Reference/Events#Drag_events
# SEE: Drag & Drop    - https://developer.mozilla.org/en-US/docs/DragDrop/Drag_and_Drop


# FIXME: Should test capture -- for instance, you might want a mouse out only
#        on the body, but not on all the children. Alternatively we could
#        use a scope, saying that it includes children, or its target node ONLY
# TODO:  Support cancellation of interaction for a specific device
# TODO:  Remove dependency on jQuery
# TODO:  Add an Event class with events re-use
# TODO:  Add device global enable/disable

# FIXME: Refactor so that devices act as sources for normalized events
# and lazily bind to the corresponding targets. Handlers should support
# both device primitive events (enter/exit,up,down,press,release), composite
# events (click, dblclick) and behaviors (drag, swipe, etc)
# EX:
# new interaction Handler {
#	wheel : "..."
#	pinch : "..."
# } bind (uis maps)

# -----------------------------------------------------------------------------
#
# HANDLER
#
# -----------------------------------------------------------------------------

# TODO: Support enabling/disabling devices or events for a specific handler
@class Handler
| A handler aggregates one or more event handlers that can be bound to one or
| more DOM/SVG elements.

	@shared COUNT = 0

	@property id        = -1
	@property on        = {}
	@property _handlers = {}
	@property data      = {}

	@constructor devices
		id = COUNT ; COUNT += 1
		listen (devices)
	@end

	@method listen devices
	| Adds the given `{<DEVICE>:{<EVENT>:<CALLBACK|[CALLBACK]>}}` mapping to
	| this handler.
	|
	| Note that if you call `listen` after having called `bind`, then you will
	| have to call `bind` again on the scopes for all the events to be registered.
	|
	| Ex:
	| ```
	| handler listen {
	|     mouse : {
	|         wheel : ...
	|     }
	|     key   : {
	|         press : ...
	|     }
	| }
	| ```
		for events, device in devices
			if not on[device]
				on[device] = {}
			end
			var device_class = Source Get (device)
			assert (device_class, "No device or gesture found:" + device)
			if extend isFunction(events)
				# In some cases we have directly a callback. For instance
				# {press:<callback>}, in which case we expand it to
				# {press:{press:callback}}
				events = {(device):events}
			end
			for callbacks, eventName in events
				if device_class
					assert (device_class HasEvent (eventName), "Device/Gesture does not declare event: " + device + "." + eventName)
					if not isList(callbacks)
						callbacks = [callbacks]
					end
					on[device][eventName] = callbacks
				end
			end
		end
		return self
	@end

	@method _ensureHandler device, name
	| Ensures that there's a given handler for the given event
		if not _handlers [device]       -> _handlers [device]       = {}
		if not _handlers [device][name] -> _handlers [device][name] = {event,source|
			if isDefined(animation)
				LAST_INTERACTION = animation now ()
			else
				LAST_INTERACTION = new Date () getTime ()
			end
			return _trigger (device, name, _normalizeEvent(device, name, event), source or self)
		}
		return _handlers [device][name]
	@end

	@method _trigger device, name, event, source
	| Triggers the event from the given device, with the given name and event data.
	| This wraps the `interaction.trigger` function.
		interaction trigger (on[device], name, event, source)
	@end

	@method bind scope, capture=True
	| Binds the handler to the given scope. This will look for all the devices
	| registered in the handler and bind the corresponding events.
		if scope jquery or extend isList (scope)
			scope :: {_|bind(_, capture)}
		else
			for handlers, device in on
				var device_class = Source Get (device)
				if device_class isSubclassOf (Device)
					for callbacks, name in handlers
						device_class Bind (name, scope, _ensureHandler (device, name), capture)
					end
				else
					device_class Bind (scope, self, capture)
				end
			end
		end
		return self
	@end

	@method unbind scope, capture=True
	| Unbinds the handler to the given scope. This will look for all the devices
	| registered in the handler and unbind the corresponding events.
		if scope jquery or extend isList (scope)
			scope :: unbind
		else
			for handlers, device in on
				var device_class = Source Get (device)
				if device_class isSubclassOf (Device)
					for callbacks, name in handlers
						device_class Unbind (name, scope, _ensureHandler (device, name), capture)
					end
				else
					device_class Unbind (scope, self, capture)
				end
			end
		end
		return self
	@end

	@method _normalizeEvent device, name, event
		return Source Get (device) NormalizeEvent (event, name)
	@end

	# NOTE: I am deprecating that as I suspect it's not used anymore
	# @method getContext element
	# 	if not element -> return None
	# 	if element jquery -> element = element[0]
	# 	assert (element nodeName, "Gesture.getContext: Needs a DOM or SVG element")
	# 	if not element __interactionContexts
	# 		element __interactionContexts = {}
	# 	end
	# 	var cid = getContextID ()
	# 	if not element __interactionContexts [cid]
	# 		element __interactionContexts [cid] = {}
	# 	end
	# 	return element __interactionContexts [cid]
	# @end
	# @method getContextID
	# 	return self getClass () getName () + ":" + id
	# @end

@end

# -----------------------------------------------------------------------------
#
# EVENT
#
# -----------------------------------------------------------------------------

@class Event
| The event class abstracts touch and mouse events, storing additional
| information such as delta, distance and speed that is useful to implement
| complex hanlders and gestures.
|
| The event class uses the flyweight pattern to allow recycling of events,
| preventing the creation of too many objects at the cost of some extra memory.

	@shared COUNT  = 0
	@shared STACK  = []
	@shared STACK_LIMIT = 100

	@operation Get
		if STACK length == 0
			return new Event ()
		else
			return STACK pop ()
		end
	@end

	@operation FromMouse event, isOrigin=False
		return Get () copyMouseEvent (event, isOrigin)
	@end

	@operation FromTouch event, isOrigin=False
		return Get () copyTouchEvent (event, isOrigin)
	@end

	@operation TargetWithClass event, className
	| Returns the first element (or parent element) that
	| contains the given class
		var t = event target
		if not className
			return t
		else
			while t and t classList and (not t classList contains (className))
				t = t parentNode
			end
		end
		return t
	@end

	@property id         = -1
	@property type       = None
	@property index      = 0
	@property gesture    = None
	@property position   = [0,0]
	@property delta      = [0,0]
	@property distance   = 0
	@property time       = 0
	@property target     = Undefined
	@property velocity   = 0
	@property origin     = [0,0]
	@property started    = 0
	@property ended      = 0
	@property duration   = 0
	@property original   =  Undefined
	@property last       = {
		position : None
		delta    : None
		time     : 0
		distance : 0
		velocity : 0
	}

	@constructor
		id = COUNT ; COUNT += 1
	@end

	@method reset
		id            = COUNT ; COUNT += 1
		type          = None
		gesture       = None
		index         = 0
		position[0]   = 0
		position[1]   = 0
		delta[0]      = 0
		delta[1]      = 0
		distance      = 0
		time          = 0
		velocity      = 0
		origin[0]     = 0
		origin[1]     = 0
		started       = 0
		ended         = 0
		duration      = 0
		self target   = Undefined
		last position = None
		last delta    = None
		last time     = 0
		last distance = 0
		last velocity = 0
		original      =  Undefined
		return self
	@end

	@method recycle
		reset ()
		if STACK length < STACK_LIMIT
			STACK push (self)
		end
		return self
	@end

	@method copyMouseEvent mouseEvent, isOrigin=False
	| Copies the relevant data from the given mouse event into the
	| given gesture event.
		original    = mouseEvent
		type        = "mouse"
		self target = mouseEvent target
		_prepareEvent (isOrigin)
		position[0] = mouseEvent pageX
		position[1] = mouseEvent pageY
		_updateEvent (isOrigin)
		return self
	@end

	@method copyTouchEvent touchEvent, touch, isOrigin=False
		type        = "touch"
		touch       = touch
		id          = touch index
		original    = touchEvent
		self target = touchEvent target
		_prepareEvent (isOrigin)
		position[0] = touch pageX
		position[1] = touch pageY
		return _updateEvent (isOrigin)
	@end

	@method _prepareEvent isOrigin=False
	| Prepares the given gesture event by copying the last position and
	| time if not origin, and initializing the last position and delta
	| if necessary.
		if not isOrigin
			if not last position
				last position = [0,0]
				last delta    = [0,0]
			end
			last position [0] = position [0]
			last position [1] = position [1]
			last ended        = ended
			last duration     = last started - ended
		end
		return self
	@end

	@method _updateEvent isOrigin=False
	| Updates event properties based on its position, origin, started and
	| ended properties. This gives global and local delta, distance and
	| velocity.
		# We update the delta and distance
		if isOrigin
			origin[0] = position[0]
			origin[1] = position[1]
			started   = new Date () getTime ()
		end
		ended     = new Date () getTime ()
		delta[0]  = position[0] - origin [0]
		delta[1]  = position[1] - origin [1]
		distance  = Math sqrt (delta[0] * delta[0] + delta [1] * delta [1])
		duration  = (ended - started)
		velocity  = distance / (duration)
		if not isOrigin
			last delta   [0] = position[0] - last position [0]
			last delta   [1] = position[1] - last position [1]
			last distance    = Math sqrt (last delta[0] * last delta[0] + last delta [1] * last delta [1])
			last duration    = (last ended - started)
			last velocity    = last distance / (last duration)
		end
		return self
	@end

@end

# -----------------------------------------------------------------------------
#
# SOURCE
#
# -----------------------------------------------------------------------------

@class Source
| The interaction source abstracts devices & gestures.

	@shared NAME   = None
	@shared EVENTS = {}
	@shared CACHE  = {}

	@operation Get name
	| Returns the device class with the given name, or `Undefined` if none exists.
		if not CACHE [name]
			CACHE [name] = extend first (extend getChildrenOf (self), {_|return _ NAME == name})
		end
		return CACHE [name]
	@end

	@operation Init
	| Inits the device class. Does nothing by default.
		pass
	@end

	@operation HasEvent event
	| Tells wether this device offers the event with the given name or not
		var events = self EVENTS
		if isMap (events)
			return events[event] and True or False
		else
			return extend first (events, {_|return _ == event}) and True or False
		end
	@end

	@operation Bind event, scope, callback, capture=True
	| Binds the given event to the given scope
		# FIXME: Should support enable/disable (a DOM/SVG node)
		if scope jquery
			scope :: {_|Bind (event, _, callback, capture)}
		else
			_Bind (event, scope, callback, capture)
		end
		return self
	@end

	@operation Unbind event, scope, callback, capture=True
	| Unbinds the given event from the given scope
		# FIXME: Should support enable/disable
		if scope jquery
			scope :: {_|Unbind (event, _, callback, capture)}
		else
			_Unbind (event, scope, callback, capture)
		end
		return self
	@end

	@abstract @operation _Bind event, scope, callback, capture=True
	| Binds the given event to the given scope

	@abstract @operation _Unbind event, scope, callback, capture=True
	| Unbinds the given event from the given scope

@end

# -----------------------------------------------------------------------------
#
# DEVICE
#
# -----------------------------------------------------------------------------

@class Device: Source
| A device abstracts a source of events to which a handler can bind. Devices
| can have one or more instances and are automatically registered in the
| as available to handlers.

	@shared IsEnabled = True

	@operation NormalizeEvent event, name=Undefined
	| Normalizes the given event.
		return event
	@end

	@operation NormalizeEventName name
	| Normalizes the name of this event.
		var events = EVENTS
		if isMap (events)
			return events[name]
		else
			return name
		end
	@end

	@operation _Bind event, scope, callback, capture=True
	| Binds the given event to the given scope
		# We capture by default
		# SEE: http://www.w3.org/TR/DOM-Level-3-Events/#event-flow
		scope addEventListener (NormalizeEventName(event), callback, capture)
	@end

	@operation _Unbind event, scope, callback, capture=True
	| Unbinds the given event from the given scope
		scope removeEventListener (NormalizeEventName(event), callback, capture)
	@end

	@operation Cancel event
	| Cancels the given event (this works with normalized and raw events)
		if event _originalEvent -> event = event _originalEvent
		event stopPropagation          ()
		event preventDefault           ()
		event stopImmediatePropagation ()
		return False
	@end

@end

# -----------------------------------------------------------------------------
#
# MOUSE
#
# -----------------------------------------------------------------------------

@class Mouse: Device
| The mouse device supports the following events:
|
| - move
| - down
| - up
| - click
| - wheel
| - move
| - in
| - out

	@shared NAME   = "mouse"
	@shared EVENTS = {
		move      : "mousemove"
		down      : "mousedown"
		up        : "mouseup"
		wheel     : "wheel"
		move      : "mousemove"
		in        : "mouseover"
		out       : "mouseout"
		click     : "click"
	}

	@operation Init
		# SEE: https://developer.mozilla.org/en-US/docs/DOM/DOM_event_reference/mousewheel
		# SEE: https://developer.mozilla.org/en-US/docs/DOM/Mozilla_event_reference/wheel?redirectlocale=en-US&redirectslug=Mozilla_event_reference%2Fwheel
		if not isDefined(document documentElement onwheel)
			# Chrome, Safari
			EVENTS wheel = "mousewheel"
		end
	@end

	@operation NormalizeEvent event, name=Undefined
	| Normalizes the given event.
		if name == "wheel"
			return NormalizeWheelEvent (event)
		else
			return event
		end
	@end

	@operation NormalizeWheelEvent original
		if original _isNormalized
			return original
		end
		# FIXME: Does not work the same in FF and Chrome
		var delta    = original delta
		var delta_x  = original deltaX
		var delta_y  = original deltaY
		# FROM jquery.mousewheel-3.0.6
		# SEE: https://developer.mozilla.org/en-US/docs/DOM/Mozilla_event_reference/wheel?redirectlocale=en-US&redirectslug=Mozilla_event_reference%2Fwheel
		if isDefined (original wheelDelta)
			# This is the case on IE
			delta   = original wheelDelta / 120
			delta_y = original wheelDelta / 120
			delta_x = 0
		end
		if isDefined (original detail)
			delta = original detail / 3
		end
		if isDefined (original axis) and original axis == original HORIZONTAL_AXIS
			assert (isDefined (delta), "Mousewheel: Delta not defined")
			delta_y = 0
			delta_x = 0 - delta
		elif isDefined (original wheelDeltaY)
			delta_y = original wheelDeltaY / 120
			if not isDefined (delta)
				delta = delta_y
			end
		end
		if not isDefined (delta)
			if not delta_x == 0
				delta = delta_y
			else
				delta = delta_x
			end
		end
		# We normalize the event
		var event    = original
		event _isNormalized = True
		event delta  = delta
		event deltaX = delta_x
		event deltaY = delta_y
		# On mousewheel type, the delta seems to be reversed
		if EVENTS wheel == "mousewheel"
			event deltaY = 0 - event deltaY
		end
		return event
	@end
@end

# -----------------------------------------------------------------------------
#
# TOUCH
#
# -----------------------------------------------------------------------------

# SEE: http://www.w3.org/TR/touch-events/#usage-examples
@class Touch: Device

	@shared NAME   = "touch"
	@shared EVENTS = {
		start  : "touchstart"
		end    : "touchend"
		move   : "touchmove"
		enter  : "touchenter"
		cancel : "touchcancel"
		leave  : "touchleave"
	}

	@operation GetTargets event, touches=event touches
		var targets = []
		for touch in touches
			if not (touch target in targets)
				targets push (touch target)
			end
		end
		return targets
	@end

	@operation GetChangedTargets event, touches
		return GetTargets (event, event changedTouches)
	@end

@end

# -----------------------------------------------------------------------------
#
# KEYBOARD
#
# -----------------------------------------------------------------------------

@class Keyboard: Device

	@shared NAME   = "keyboard"
	@shared EVENTS = {
		down  : "keydown"
		up    : "keyup"
		press : "keypress"
	}

@end

# -----------------------------------------------------------------------------
#
# SCREEN
#
# -----------------------------------------------------------------------------

@class Screen: Device

	# SEE: http://stackoverflow.com/questions/5284878/how-do-i-correctly-detect-orientation-change-using-javascript-and-phonegap-in-io
	# SEE: http://stackoverflow.com/questions/4917664/detect-viewport-orientation-if-orientation-is-portrait-display-alert-message-ad

	@shared NAME   = "screen"
	@shared EVENTS = {
		orientation  : "deviceorientation"
		mode         : True
		size         : True
	}

	# NOTE: We assume that there is only one screen, so we can use shared state
	# in this case
	@shared Callbacks = None
	@shared Cache     = {mode:None, width:None, height:None}

	@operation Query query:String
	| Does a media query and returns True if it matches
	| See: http://dev.w3.org/csswg/cssom-view/#the-mediaquerylist-interface
		# SEE: http://stackoverflow.com/questions/476815/can-you-access-screen-displays-dpi-settings-in-a-javascript-function
		# SEE: https://developer.mozilla.org/en-US/docs/Web/API/window.matchMedia
		if isDefined (window matchMedia)
			return window matchMedia (query) matches
		else
			return False
		end
	@end

	@operation IsLandscape
		return Query ("(orientation: landscape)")
	@end

	@operation IsPortrait
		return Query ("(orientation: portrait)")
	@end

	@operation IsMobile
		return Query ("handheld")
	@end

	@operation HasDensity dppx:Integer
		return Query ("(min-resolution: " + dppx + "dppx)")
	@end

	@operation HasDPI dpi:Integer
		# FIXME: Should add a getZoom ratio according to the DPI, to adjust
		# the interface.
		# NOTE: We dppx as dpi means dots-per-CSS-inch not dots-per-physical-inch
		return Query ("(min-resolution: " + dpi + "dpi)")
	@end

	@operation GuessDPI steps=10
		var bounds = [0, 600]
		while (steps > 0 and not HasDPI(bounds[1]))
			var delta = bounds[1] - bounds[0]
			var guess = parseInt (bounds[0] + (delta / 2))
			if Screen HasDPI (guess)
				bounds[0] = guess
			else
				bounds[1] = guess
			end
			steps -= 1
		end
		var result = bounds[0]
		# These are heuristics to infer the dpi when min-resolution is not
		# working (for example on Safari iOS 5)
		# SEE: http://en.wikipedia.org/wiki/List_of_displays_by_pixel_density
		if result == 0
			# FIXME: Should detect native resolution
			if (navigator userAgent indexOf "iPhone" != -1)
				result = 326
			end
		end
		return result
	@end

	@operation GuessDPX steps=10
		# SEE: http://www.w3.org/TR/css3-values/#resolution
		return GuessDPI() / 96.0
	@end

	@operation GuessPixelRatio
	| Guesses the zoom ratio based on the
		# SEE: http://johnstejskal.com/blog/list-of-screen-resolutions-and-dpippi-for-popular-mobile-devices/
		if window devicePixelRatio
			return window devicePixelRatio
		elif Screen IsMobile ()
			if Screen HasDPI 300
				return 2
			elif Screen HasDPI 250
				return 1.5
			elif Screen HasDPI 160
				return 1
			elif Screen HasDPI 133
				return 0.75
			else
				return 0.5
			end
		else
			if Screen HasDPI 250
				return 1.5
			else
				return 1
			end
		end
	@end

	@operation EnsureCallbacks
		if not Device Callbacks
			Device Callbacks = extend map (EVENTS, {return []})
			# SEE: https://developer.mozilla.org/en/docs/WebAPI/Detecting_device_orientation
			# SEE: http://davidwalsh.name/orientation-change
			window addEventListener ("orientationchange", OnOrientationChange, True)
			window addEventListener ("deviceorientation", OnOrientationChange, True)
			window addEventListener ("resize",            OnWindowResized)
		end
		return Device Callbacks
	@end

	@operation _Bind event, scope, callback, capture=True
	| Binds the given event to the given scope
		# NOTE: We ignore the scope in this case as the screen device
		# is not contextualized as mouse or touch.
		var c = EnsureCallbacks ()
		assert (extend isDefined (c[event]), "Screen: No event defined " + event)
		c [event] push (callback)
	@end

	@operation OnOrientationChange event
		Device Callbacks orientation :: {c|c(event)}
	@end

	@operation OnWindowResized event
		var width  = window innerWidth
		var height = window innerHeight
		var ratio  = width / height
		var size   = [width, height]
		var mode   = (width > height) and "landscape" or "portrait"
		var event = {type:None, width:width, height:height, ratio:ratio, mode:mode}
		if mode != Screen Cache mode
			var e = extend merge ({type:"mode", value:mode, previous:Screen Cache mode}, event)
			Device Callbacks mode :: {c|c(e)}
		end
		if width != Screen Cache width or height != Screen Cache height
			var e = extend merge ({type:"size", value:size, previous:Screen Cache size}, event)
			Device Callbacks size :: {c|c(e)}
		end
		Screen Cache mode   = mode
		Screen Cache width  = width
		Screen Cache size   = size
		Screen Cache height = height
	@end

@end

# -----------------------------------------------------------------------------
#
# GESTURE
#
# -----------------------------------------------------------------------------

# FIXME: There's still a lot of common work in gestures. We should have
# a look at Tap & Drag an abstract out the common elements.

# FIXME: Not sure if HANDLERS_KEY is always resolved to self getClass () getName ()

@class Gesture: Source
| A gesture abstracts a sequence of interaction originating from one or
| more devices. Gestures are a little bit more trickly than devices, as
| they can be instanciated and configured with different options, and
| then bound to one or more elements.
|
| As a result, gestures all provide a default, lazily created gesture with
| default options, that is usable through the `Handlers` class or `handle()` function
| just like a regular input device. If you would like
| to have specific options, you can directly instanciate a gesture
| and bind it handlers.
|
| For example, you can use the `drag` gesture in different ways:
|
| ```sugar
| # By using the `handle` method (identical to `new Handler {}`)
| interaction handle {
|     drag : {
|         start : {event,gesture| ... }
|         drag  : {event,gesture| ... }
|         stop  : {event,gesture| ... }
|     }
| } h bind (element)
|
| # By instanciating and binding to a gesture
| new interaction Gesture (options) g bind (element, {
|       start : {event,gesture| ... }
|       drag  : {event,gesture| ... }
|       stop  : {event,gesture| ... }
| })
| ```

	@shared Instance

	@shared CONTEXT_KEY  = "_interactionContexts"
	| The context key is where interaction contexts are stored

	@shared HANDLERS_KEY  = None
	| The name of the property in the bound node's context in which
	| this gesture's handlers will be stored.

	@shared OPTIONS       = {}
	@shared INITIAL_STATE = "bound"
	@shared STATES = {
		bound : "bound"
	}

	@shared COUNT       = 0
	# FIXME: We might want to have a global registry of gesture handlers, as
	# we probably won't have too many instanciated

	@operation Ensure
	| Returns the default instance for this gesture, lazily creating it.
		if not self Instance
			self Instance = new self ()
		end
		return self Instance
	@end

	@operation _Bind element, handler, capture=True
	| Binds the given handler to the given element
		Ensure () bind (element, handler, capture)
	@end

	@operation _Unbind element
	| Binds the gesture from the given scope
		Ensure () unbind (element)
	@end

	# =========================================================================
	# INSTANCE-LEVEL
	# =========================================================================

	@property id         = -1
	@property options    = {}
	@property handler    = None
	@property defaultHandlers = None
	@property _isEnabled = True

	@constructor options
		# We lazily create the handler key
		if not self getClass () HANDLERS_KEY
			self getClass () HANDLERS_KEY = NAME + "Handlers"
		end
		id = Gesture COUNT ; Gesture COUNT += 1
		OPTIONS :: {v,k|if not isDefined(self options[k]) -> self options[k] = v}
		options :: {v,k|self options[k] = v}
		super ()
	@end

	@method isEnabled eventOrNode=None
	| Tells if the given gesture is globally enabled, or enabled for the
	| given target.
		if not eventOrNode
			return _isEnabled
		else
			if not isDefined (eventOrNode nodeName)
				eventOrNode = eventOrNode target
			end
			var c = getContext (findContextElement (eventOrNode))
			if _isEnabled and c and (c isEnabled != False)
				return True
			else
				return False
			end
		end
	@end

	@method enable node=None
		if node
			set (findContextElement(node), "isEnabled", True)
		else
			_isEnabled = True
		end
	@end

	@method disable node
		if node
			set (findContextElement(node), "isEnabled", False)
		else
			_isEnabled = False
		end
	@end

	@method setHandlers handlers
	| Sets the hanlders that will be used by default when binding a node
	| to this gesture.
		self defaultHandlers = handlers
		return self
	@end

	@method bind element, handlers=defaultHandlers
	| Binds the given handlers to the gestures' events generated from the
	| given element. This will set the `gesture=id`, `state=INITIAL_STATE`
	| and `<NAME>Handlers=handlers` properties in the element's context
	| and call the `_bind()` method for further configuration.
		if element jquery
			assert (len(element) > 0, self getClass () getName () + ".bind: Empty selection " + element selector)
			element :: {_|bind(_, handlers)}
		else
			if Handler hasInstance (handlers) -> handlers = handlers on [NAME]
			set (element, {
				gesture       : id
				state         : INITIAL_STATE
				(HANDLERS_KEY) : handlers
			})
			if handler
				handler bind (element)
			end
			_bind (element, handlers)
		end
		return self
	@end

	@method unbind element
	| Clears the context for the given element and calls `_unbind()`.
		clear (element)
		if handler
			handler bind (element)
		end
		_unbind (element)
	@end

	@method _bind element, handlers
	@end

	@method _unbind element
	@end

	# =========================================================================
	# CONTEXT
	# =========================================================================

	@method set element, values, value=Undefined
	| Sets the given values (or key/value pair) in the gesture's context
	| bound to the given element.
	|
	| You can use it the following ways
	|
	| ```
	| g set (element, "key", 1.0)              # key/value
	| g set (element, {key:1.0, key2:"hello"}) # map
	| ```
	|
	| The gesture's context for the element will be returned in both cases.
		var context = getContext (element)
		if isString (values)
			context[values] = value
		else
			values :: {v,k|context[k]=v}
		end
		return context
	@end

	@method get element, value, default=Undefined
	| Sets the given values from the gesture's context
	| bound to the given element.
	|
	| You can use it the following ways
	|
	| ```
	| g get (element, "key")                   # returns the value bound to key
	| g set (element, ["key", "key1"]          # returns the values bound to the keys as a map
	| g set ()                                 # returns the whole context
	| ```
	|
	| The gesture's context for the element will be returned in both cases.
		var context = getContext (element)
		if not context
			return None
		elif isString (value)
			if isDefined (context[value])
				return context [value]
			else
				return default
			end
		if not isDefined (value)
			return context
		else
			error "Not implemented"
		end
	@end

	@method clear element
	| Clears the gesture's context bound to the given element
		if not element -> return None
		if element jquery -> element = element[0]
		assert (element nodeName, "Gesture.clear: Needs a DOM or SVG element")
		var context = element [CONTEXT_KEY]
		if context
			context [getContextID()] = Undefined
		end
		return element
	@end

	@method getContext element
	| Get the gesture's context bound to the given element
		if not element -> return None
		if element jquery -> element = element[0]
		assert (element nodeName, "Gesture.getContext: Needs a DOM or SVG element")
		var context = element [CONTEXT_KEY]
		if not context
			context = {}
			element [CONTEXT_KEY] = context
		end
		var cid = getContextID ()
		if not context [cid] -> context [cid] = {}
		return context [cid]
	@end

	@method hasContext element
		return element and isDefined(element[CONTEXT_KEY]) and isDefined (element[CONTEXT_KEY][getContextID()])
	@end

	@method findContextElement element
	| Finds the context element for this object in the current element or one
	| of its parents.
		if element
			if hasContext (element)
				return element
			else
				return findContextElement (element parentNode)
			end
		else
			return None
		end

	@end

	@method getContextNodes elements
		return extend map (elements, {_|return findContextElement (_)})
	@end

	@method getContextID
	| Get the instance-specific id used to retrieve this gesture's context
	| in elements.
		return self getClass () getName () + ":" + id
	@end

	# =========================================================================
	# UTILITIES
	# =========================================================================

	@method touchesWithContext touches
	| Same as `targetWithContext` except that it takes a list of touches. This
	| method is useful for touch gesture handlers.
	|
	| ```sugar
	| # Returns all the touches that started within and element (or its
	| # descendents) to which the gesture was bound.
	| var active_touches = touchesWithContext (event touches)
	| ```
		return extend filter (touches, {_|return findContextElement(_ target) != None})
	@end

	@method targetsWithContext targets
	| Filters the given list of targets, returning only the ones that have (
	| or have a parent that has) a context defined for the current gesture.
		return extend filter (targets, {_|return findContextElement(_) != None})
	@end

	@method targetsWithProperty targets, name, value
	| Filters the given list of targets, returning those who have or have
	| a context element that has the given property with the given value.
		return extend filter (targets, {_|return get(findContextElement(_), name) == value})
	@end

	@method targetWithProperty targets, name, value
	| Finds the first target that has (or has a context element) that
	| defines the given propery and value
		return extend first (targets, {_|return get(findContextElement(_), name) == value})
	@end

@end

# -----------------------------------------------------------------------------
#
# DRAG
#
# -----------------------------------------------------------------------------

# FIXME: Gestures can have different options, and then should be instanciable.
# This means that we can have multiple gestures per node
@class Drag: Gesture
| Drag events will yield `Event` instances, with the following extra
| properties:
|
| - `dragged`: the element being dragged
| - `context`: the gesture's interaction context (useful for debugging)

	@shared DRAG_BOUND     = "bound"
	@shared DRAG_INITIATED = "initiated"
	@shared DRAG_STARTED   = "started"
	@shared DRAG_ENDED     = "ended"

	@shared OPTIONS = {
		touch            : True
		mouse            : True
		threshold        : 5
		stopOnWindowExit : True
		mouseOutDelay    : 1000
		mouseButton      : 0
	}

	@shared NAME   = "drag"
	@shared EVENTS = {
		start : True
		drag  : True
		stop  : True
	}

	@property handler      = interaction handle {
		mouse : {
			down : onMouseDown
		}
		touch : {
			start  : onTouchStart
			move   : onTouchMove
			cancel : onTouchEnd
			end    : onTouchEnd
		}
	}

	@property dragHandler  = interaction handle {
		mouse : {
			move : onMouseMove
			out  : onMouseOut
			up   : onMouseUp
		}
	}
	@property lastMouseOut = Undefined

	# =========================================================================
	# MOUSE
	# =========================================================================

	@method onMouseDown event
		if not options mouse -> return True
		if event button != options mouseButton -> return True
		# When the mouse is down, we'll start to track mouse move and mouse up
		# on the body.
		# FIXME: What about a mouse out and then a mouse up?
		dragHandler bind (document)
		var e     = Event FromMouse (event, True)
		# NOTE: We need to find the context element, as the  target might
		# be a child of the element on which we've bound the gesture.
		var context_element = findContextElement (event target)
		e context = get (document body)
		set (document body, {
			dragState    : DRAG_INITIATED
			dragElement  : context_element
			dragTarget   : e target
			dragEvent    : e
			dragHandlers : get (context_element, HANDLERS_KEY)
		})
	@end

	@method onMouseMove event
		if not options mouse -> return True
		if event button != options mouseButton -> return True
		var handlers = get (document body, HANDLERS_KEY)
		var e        = get (document body, "dragEvent")    copyMouseEvent (event)
		var state    = get (document body, "dragState",    DRAG_INITIATED)
		e dragged    = get (document body, "dragElement")
		e context    = get (document body)
		if state == DRAG_INITIATED
			if e distance > options threshold
				set (document body, "dragState", DRAG_STARTED)
				interaction trigger (handlers, "start", e, self)
			end
		if state == DRAG_STARTED
			interaction trigger (handlers, "drag", e, self)
		end
	@end

	@method onMouseUp event
		if not options mouse -> return True
		if event button != options mouseButton -> return True
		var state    = get (document body, "dragState")
		if state == DRAG_STARTED
			var handlers = get (document body, HANDLERS_KEY)
			var e        = get (document body, "dragEvent") copyMouseEvent (event)
			interaction trigger (handlers, "drag", e, self)
			e dragged    = get (document body, "dragElement")
			e context    = get (document body)
			interaction trigger (handlers, "stop", e, self)
		end
		set (document body, "dragState", DRAG_ENDED)
		dragHandler unbind (document)
	@end

	@method onMouseOut event
	| Intercepts the mouse out event. Will tolerate the mouse out of the
	| window for `options.mouseOutDelay` milliseconds, and then will
	| end the drag.
		if not options mouse -> return True
		var source = event relatedTarget or event toElement
		if not options stopOnWindowExit
			return True
		elif source and source nodeName == "HTML"
			var now  = new Date () getTime ()
			if not isDefined (lastMouseOut)
				lastMouseOut = now
			elif (now - lastMouseOut) >  options mouseOutDelay
				return onMouseUp (event)
			end
		else
			lastMouseOut = Undefined
		end
	@end

	# =========================================================================
	# TOUCH
	# =========================================================================

	@method onTouchStart event
		if not options touch -> return True
		var c = _extractTouchContext (event)
		if c touch changedCount > 0
			if (c state == DRAG_BOUND) and (c touch activeCount >= 1)
				event preventDefault ()
				c state = DRAG_INITIATED
				if not c event
					c event = Event Get ()
				else
					c event = c event reset ()
				end
				c event copyTouchEvent (event, c touch touch, True)
				trigger (c [HANDLERS_KEY], "start", c event, self)
				return False
			end
			return False
		end
	@end

	@method onTouchMove
		if not options touch -> return True
		var c = _extractTouchContext (event)
		# If changedCount > 0 it means that the event is related
		# to this gesture.
		if c touch changedCount > 0
			if (c state == DRAG_INITIATED) and (c touch activeCount >= 1)
				event preventDefault ()
				c event copyTouchEvent (event, c touch touch, False)
				if c event distance > options threshold
					c STATE = DRAG_STARTED
					trigger (c[HANDLERS_KEY], "drag", c event, self)
				end
				return False
			end
		end
	@end

	@method onTouchEnd
		if not options touch -> return True
		var c = _extractTouchContext (event)
		if c touch changedCount > 0
			if (c state == DRAG_INITIATED) and (c touch activeCount == 0)
				c state = DRAG_ENDED
				c event copyTouchEvent (event, c touch touch, False)
				trigger (c [HANDLERS_KEY], "stop", c event)
				c state = DRAG_BOUND
			end
		end
	@end

	@method _extractTouchContext event
	| Returns the context for this event, augmented with a `touch` property
	| that stores the state of the touch interaction.
		var changed_touches  = touchesWithContext (event changedTouches)
		var active_touches   = touchesWithContext (event touches)
		var t                = findContextElement (changed_touches[0] target)
		var c                = get (t)
		c touch              = c touch or {}
		c touch state        = c touch state or DRAG_BOUND
		c touch touch        = changed_touches[0]
		c touch target       = t
		c touch changedCount = len (changed_touches)
		c touch activeCount  = len (active_touches)
		c touch changed      = changed_touches
		c touch active       = active_touches
		return c
	@end

@end

# -----------------------------------------------------------------------------
#
# TAP
#
# -----------------------------------------------------------------------------

# NOTE: Right now if touch count > count, the tap is driggered, we might
# want to implement a "stric" version
@class Tap: Gesture

	@shared NAME          = "tap"
	@shared EVENTS        = {
		start : True
		tap   : True
		end   : True
	}
	@shared OPTIONS       = {
		count     : 1
		tolerance : 10
	}
	@shared TAP_BOUND     = "bound"
	@shared TAP_INITIATED = "initiated"
	@shared TAP_REACHED   = "reached"
	@shared TAP_ENDED     = "ended"
	@shared TAP_CANCELLED = "cancelled"

	@property tapHandler  = None

	@constructor options
		super (options)
		tapHandler = interaction handle {
			touch : {
				start  : onTouchStart
				cancel : onTouchEnd
				end    : onTouchEnd
			}
		}
	@end

	@method _bind element, handlers=getHandlers ()
		tapHandler bind (element)
	@end

	@method _unbind element
		tapHandler unbind (element)
	@end

	# NOTE: We can think of a state machine that
	# - Compute state properties at each update (updateState())
	# - Applies effects and state transitions

	# NOTE: This could be rewritten in a more declarative state
	# "!TAP_REACHED & COUNT_EQUAL" -> TAP_REACHED, start()
	# _ -> TAP_INITIATED
	@method onTouchStart event
		var t        = targetWithProperty (getContextNodes (Touch GetChangedTargets (event)), "gesture", id)
		if not t -> return None
		var state    = get (t, "state")
		var handlers = get (t, HANDLERS_KEY)
		var count    = _countTouches (event touches, HANDLERS_KEY, handlers)
		var result   = True
		var origins  = get (t, "touchOrigins") or {}
		for touch in event changedTouches
			origins[touch identifier] = [touch clientX, touch clientY]
		end
		set (t, "touchOrigins", origins)
		if count >= options count
			if state != TAP_REACHED
				set (t, "state", TAP_REACHED)
				# FIXME: Should return something different than event
				_trigger (handlers, "start", event)
			end
		else
			set (t, "state", TAP_INITIATED)
		end
		return result
	@end

	# NOTE: This could be rewritten in a more declarative state
	# "!TAP_REACHED & COUNT_DIFFERENT" -> tap(), TAP_ENDED
	# COUNT_ZERO                       -> end(), TAP_BOUND
	# _                                -> TAP_BOUND
	@method onTouchEnd event
		var t        = targetWithProperty (getContextNodes (Touch GetChangedTargets (event)), "gesture", id)
		if not t -> return None
		var state    = get (t, "state")
		var handlers = get (t, HANDLERS_KEY)
		var count    = _countTouches (event touches, HANDLERS_KEY, handlers)
		var result   = True
		var origins  = get (t, "touchOrigins") or {}
		var delta    = _getDelta (get (t, "touchOrigins"), event changedTouches)
		if count < options count
			if state == TAP_REACHED
				if delta < (options threshold or 5)
					# NOTE: Removed that because it's swallowing too many events.
					# We should let the callbacks decide, so _trigger should
					# return.
					event preventDefault ()
					# FIXME: Should return something different than event
					_trigger (handlers, "tap", event)
					set (t, "state", TAP_ENDED)
					result = False
				else
					set (t, "state", TAP_CANCELLED)
				end
			end
			if count > 0
				set (t, "state", TAP_INITIATED)
			elif count == 0
				_trigger (handlers, "end", event)
				set (t, "state", TAP_BOUND)
			end
		end
		return result
	@end

	@method _getDelta origins, touches
		var d = 0
		for t in touches
			var o   = origins [t identifier]
			var d_x = o[0] - t clientX
			var d_y = o[1] - t clientY
			d       = Math max (d,  Math sqrt ((d_x * d_x) + (d_y * d_y)))
		end
		return d
	@end

	@method _countTouches touches, name="tapHandler", value=self id
	| Counts the touches that have a target which is within the scope of an element to
	| which this gesture is bound.
		var targets = extend map (touches, {_|return _ target})
		targets     = targetsWithProperty (getContextNodes (targets), name, value)
		return len(targets)
	@end

	@method _trigger handlers, name, event
		interaction trigger (handlers, name, event, self)
		return self
	@end

@end

# -----------------------------------------------------------------------------
#
# PRESS
#
# -----------------------------------------------------------------------------

@class Press: Tap
| Press extends tap with mouse click support.

	@shared NAME   = "press"
	@shared EVENTS = {
		press : True
	}

	@property clickHandler = None

	@constructor options
		super (options)
		clickHandler = interaction handle {
			mouse : {
				click : onMouseClick
			}
		}
	@end

	@method _bind element, handlers=getHandlers ()
		super _bind (element, handlers)
		clickHandler bind (element)
	@end

	@method _unbind element
		super _unbind (element)
		clickHandler unbind (element)
	@end

	@method onMouseClick event
		# FIXME: Maybe should wrap in mouse event
		var t        = targetWithProperty (getContextNodes ([event target]), "gesture", id)
		var handlers = get (t, HANDLERS_KEY)
		_trigger (handlers, "press", event)
	@end

	@method _trigger handlers, name, event
		if (name == "tap") or (name == "press")
			# Absorbs triggered event excpet `tap` and `press`, which are
			# both transformed in `press`
			return super _trigger (handlers, "press", event)
		else
			return self
		end
	@end

@end

# -----------------------------------------------------------------------------
#
# SWIPE
#
# -----------------------------------------------------------------------------

# TODO: We could support one or more events
@class Swipe: Gesture

	@shared NAME   = "swipe"
	@shared EVENTS = {
		start : True
		move  : True
		end   : True
	}

	@shared SWIPE_BOUND     = "bound"
	@shared SWIPE_INITIATED = "initiated"
	@shared SWIPE_ENDED     = "ended"

	@property handler = interaction handle {
		touch : {
			start  : onTouchStart
			move   : onTouchMove
			cancel : onTouchEnd
			end    : onTouchEnd
		}
	}

	@method onTouchStart event
		if not isEnabled (event changedTouches [0] target) -> return True
		var c = _extractContext (event)
		# If changedCount > 0 it means that the event is related
		# to this gesture.
		if c changedCount > 0
			if (c state == SWIPE_BOUND) and (c activeCount >= 1)
				event preventDefault ()
				c state = SWIPE_INITIATED
				if not c event
					c event = Event Get ()
				else
					c event = c event reset ()
				end
				c event copyTouchEvent (event, c touch, True)
				trigger (c [HANDLERS_KEY], "start", c event)
				return False
			end
		end
	@end

	@method onTouchMove event
		if not isEnabled (event changedTouches [0] target) -> return True
		var c = _extractContext (event)
		# If changedCount > 0 it means that the event is related
		# to this gesture.
		if c changedCount > 0
			if (c state == SWIPE_INITIATED) and (c activeCount >= 1)
				event preventDefault ()
				c event copyTouchEvent (event, c touch, False)
				trigger (c [HANDLERS_KEY], "move", c event)
				return False
			end
		end
	@end

	@method onTouchEnd event
		if not isEnabled (event changedTouches [0] target) -> return True
		var c = _extractContext (event)
		# If changedCount > 0 it means that the event is related
		# to this gesture.
		if c changedCount > 0
			if (c state == SWIPE_INITIATED) and (c activeCount == 0)
				c state = SWIPE_ENDED
				c event copyTouchEvent (event, c touch, False)
				trigger (c [HANDLERS_KEY], "end", c event)
				c state = SWIPE_BOUND
			end
		end
	@end

	@method _extractContext event
		var changed_touches = touchesWithContext (event changedTouches)
		var active_touches  = touchesWithContext (event touches)
		var t               = findContextElement (changed_touches[0] target)
		var c               = get (t)
		c touch             = changed_touches[0]
		c target            = t
		c changedCount      = len (changed_touches)
		c activeCount       = len (active_touches)
		c changed           = changed_touches
		c active            = active_touches
		return c
	@end

@end

# -----------------------------------------------------------------------------
#
# BIND
#
# -----------------------------------------------------------------------------

@function handle callbacks
| A shorthand to `new Handler(...)`
	return new Handler (callbacks)
@end

@function trigger callbacks, name, event, source
| A utility function that triggers the callbacks for the given event.
	if not callbacks -> return False
	var v = callbacks[name]
	if isFunction (v)
		v (event, source)
	else
		for _ in v
			if _(event, source) is False
				# NOTE: We cancel the  event if the source offers the function
				# FIXME: Make sure this works with Devices:w
				#
				if source and source cancel
					source cancel (event)
				end
				break
			end
		end
	end
@end

@function target event, withClass
| An alias to Event TargetWithClass
	return Event TargetWithClass (event, withClass)
@end

# -----------------------------------------------------------------------------
#
# MAIN
#
# -----------------------------------------------------------------------------

extend getChildrenOf (Source) :: {_|_ Init ()}

# EOF
