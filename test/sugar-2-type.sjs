# Type
@type Name

# Parametric type
@type Name[T1,T2]

# Type declaration
@type Node[T]: Any
	@slot parent:Node[T]
	@slot children:List[T]

# Guarded type
# @type List3[T]: List[T]
# 	@where
# 		len( self ) == 3

# Tuple type alias/declaration
@type Vec3[T] = (T,T,T)

# Union type alias/declaration
@type Tree[T] = Node[T] | Leaf[T]

@type Status = Init | Waiting | Success | Error | Timeout

@function f:Tree[T] a:(Any|Bool|Name), b:Any|Bool|Name
	pass

