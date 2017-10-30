
@function targets:Function callback:(Function|String), target:Object, cache:Bool=True
| Ensures that the given #callback's `this` will always be the #target
| object. In case #callback is a *string*, the #target object
| will be introspected for a method with the given name, and the
@where
	let o = {echo:{console log "hello"}}
	assert (callback ("echo", o) is     callback ("echo", o))
	assert (callback (o echo, o) is not callback (o echo o))


