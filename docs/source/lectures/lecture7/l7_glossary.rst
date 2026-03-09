====================================================
Glossary
====================================================

:ref:`A <l7-glossary-a>` · :ref:`C <l7-glossary-c>` · :ref:`D <l7-glossary-d>` · :ref:`F <l7-glossary-f>` · :ref:`G <l7-glossary-g>` · :ref:`I <l7-glossary-i>` · :ref:`M <l7-glossary-m>` · :ref:`O <l7-glossary-o>` · :ref:`P <l7-glossary-p>` · :ref:`S <l7-glossary-s>`

----


.. _l7-glossary-a:

A
=

.. glossary::

   Abstract Class
      A class that cannot be instantiated directly and is designed to be
      subclassed. Defined by inheriting from ``ABC`` (or setting
      ``ABCMeta`` as the metaclass). May contain both abstract methods
      (which subclasses must override) and concrete methods (which are
      inherited as-is). Shown in UML with an italicized name and a
      circled **A** marker.

   Abstract Method
      A method declared with the ``@abstractmethod`` decorator inside an
      abstract class. It has no required implementation in the base class
      (the body is typically ``pass`` or ``...``). Any concrete subclass
      that does not implement all abstract methods cannot be instantiated.
      Python raises a ``TypeError`` at instantiation time, catching the
      omission early.

   Aggregation
      A "has-a" relationship where the contained object (the part) can
      exist independently of the container (the whole). Parts are created
      outside the container and passed in. Example: a ``Team`` has
      ``Robot``\(s), but dissolving the team does not destroy the robots.
      Represented in UML by a hollow diamond on the container side.

   Association
      A general relationship between two objects where one object holds a
      reference to another for a period of time. Neither object owns the
      other, and both can exist independently. Can be unidirectional (only
      one class knows about the other) or bidirectional. Example: a
      ``Robot`` is assigned a ``Task``; the task exists before and after
      the robot executes it. The associated object is passed in as a
      parameter, not created inside the class.


.. _l7-glossary-c:

C
=

.. glossary::

   Class Method
      A method defined with the ``@classmethod`` decorator. It receives
      the class itself as its first argument (conventionally named
      ``cls``) rather than an instance. Class methods can access and
      modify class-level state and are commonly used as factory methods
      or alternative constructors. Calling ``cls(...)`` inside a class
      method ensures correct behavior in subclasses.

   Composition
      A "has-a" relationship where the contained objects (the parts)
      cannot exist independently of the container (the whole). Parts are
      created inside the container's ``__init__`` and their lifetime is
      tied to the whole. Example: a ``Robot`` owns its ``Sensor``\(s);
      destroying the robot destroys its sensors. Represented in UML by a
      filled diamond on the container side.

   Concrete Class
      A class that provides implementations for all abstract methods it
      inherits and can therefore be instantiated directly. Shown in UML
      with a circled **C** marker.


.. _l7-glossary-d:

D
=

.. glossary::

   Data Class
      A class decorated with ``@dataclass`` (from the ``dataclasses``
      module, introduced in Python 3.7) that auto-generates ``__init__``,
      ``__repr__``, and ``__eq__`` from its type-annotated fields. Type
      hints are required; fields without annotations are ignored. Supports
      default values, mutable defaults via ``field(default_factory=...)``,
      post-initialization logic via ``__post_init__``, and immutable
      variants via ``frozen=True``. Best suited to classes whose primary
      purpose is storing data.

   Design Smell
      A sign in your code that something is structurally wrong with your
      design, even if the code technically works. Not a bug -- the program
      runs -- but the design will cause problems as the codebase grows.
      Analogous to "code smell" but applied at the class and relationship
      level. Classic example: a base class carrying ``None`` values for
      attributes that only apply to some subclasses, signaling that
      specialization is needed.

   Duck Typing
      The runtime mechanism Python uses to achieve polymorphism. An object
      is compatible with an interface if it has the required methods,
      regardless of its type or class hierarchy. The name comes from the
      saying: "If it walks like a duck and quacks like a duck, then it
      must be a duck." Python checks what an object can do, not what it
      is. Duck typing is flexible but provides no compile-time guarantee;
      abstract base classes and protocols add that safety net.


.. _l7-glossary-f:

F
=

.. glossary::

   Factory Method
      A class method that constructs and returns a new instance with a
      predefined or computed configuration. Uses ``cls(...)`` rather than
      the class name directly, so the factory works correctly in
      subclasses. Example: ``Robot.create_scout()`` returns a ``Robot``
      configured as a scout without the caller needing to know the default
      values. Factory methods can also return collections of instances.

   Frozen Data Class
      A data class created with ``@dataclass(frozen=True)``. All fields
      are immutable after construction; any attempt to assign to a field
      raises ``FrozenInstanceError``. Frozen instances are hashable and
      can be used as dictionary keys or set members. Suitable for records
      that should never change after creation, such as sensor readings or
      event logs.


.. _l7-glossary-g:

G
=

.. glossary::

   Generalization
      A bottom-up design activity in which common attributes and behaviors
      shared by multiple classes are identified and moved into a new shared
      base class. The result is a parent class that captures what all
      subclasses have in common, reducing duplication. Contrast with
      specialization.


.. _l7-glossary-i:

I
=

.. glossary::

   Inheritance
      A mechanism that allows a class (the child or derived class) to
      reuse and extend the attributes and methods of another class (the
      parent or base class). Represents an "is-a" relationship. Python
      supports single, multi-level, multiple, and hierarchical inheritance.
      The child uses ``super().__init__()`` to delegate parent attribute
      initialization. Prefer composition over inheritance when the
      relationship is "has-a" rather than "is-a".

   Instance Method
      A standard method that receives the instance as its first argument
      (conventionally named ``self``). Has access to both instance state
      and class state. The most common method type in Python. Contrast
      with class methods and static methods.


.. _l7-glossary-m:

M
=

.. glossary::

   Method Resolution Order (MRO)
      The sequence Python follows when searching for a method or attribute
      in a class hierarchy. Computed using the C3 linearization algorithm,
      which produces a consistent, predictable order that respects the
      hierarchy and never visits the same class twice. In single
      inheritance the MRO is simply the chain from child to parent to
      ``object``. Inspect it via ``ClassName.__mro__``. ``super()`` calls
      the next class in the MRO, not necessarily the direct parent.

   Method Overriding
      When a subclass provides its own implementation of a method that
      already exists in the parent class. The method name and signature
      remain the same; the subclass version replaces the parent version
      when called on a subclass instance. Used to specialize inherited
      behavior. Note: implementing dunder methods such as ``__str__`` or
      ``__eq__`` is overriding (not overloading), because every Python
      class already inherits these from ``object``.


.. _l7-glossary-o:

O
=

.. glossary::

   Operator Overloading
      A form of polymorphism in which the same operator (``+``, ``==``,
      ``<``, etc.) behaves differently depending on the type of object it
      is applied to. Achieved by implementing the corresponding dunder
      method in the class (e.g., ``__add__`` for ``+``, ``__eq__`` for
      ``==``). See also: method overriding.


.. _l7-glossary-p:

P
=

.. glossary::

   Polymorphism
      A design principle meaning "many forms." Different objects respond
      to the same interface in their own way. In Python, polymorphism is
      achieved through duck typing (method presence at runtime) and
      method overriding (subclass specialization). A polymorphic function
      calls the same method on a mixed collection of objects and receives
      different, type-appropriate behavior from each, without knowing the
      concrete types involved.

   Protocol
      A class defined with ``typing.Protocol`` that describes an interface
      through structural subtyping. A class satisfies a Protocol if it
      has the required methods and attributes, regardless of its class
      hierarchy. No explicit inheritance from the Protocol is needed.
      Contrast with ABCs, which require the subclass to explicitly inherit
      from the base class (nominal typing). Adding ``@runtime_checkable``
      allows ``isinstance()`` checks at runtime, though only method
      presence (not signatures) is verified.

   Proxy Object
      A wrapper that intercepts calls and forwards them to another object
      on your behalf. ``super()`` returns a proxy object: it does not give
      you the parent class directly but a middleman that knows your
      position in the MRO and routes method calls to the correct next
      class in the chain. This is what makes ``super()`` work correctly
      in multiple inheritance, where the next class is not always the
      obvious direct parent.


.. _l7-glossary-s:

S
=

.. glossary::

   ``__slots__``
      A class-level declaration that replaces the per-instance ``__dict__``
      with a fixed, compact structure containing only the listed attribute
      names. Reduces memory consumption (the ``__dict__`` alone costs
      roughly 232 bytes per instance) and speeds up attribute access.
      Prevents dynamic addition of attributes not listed in ``__slots__``.
      In an inheritance hierarchy, each class should declare only the new
      attributes it introduces; Python merges the slots from all classes
      in the chain automatically.

   Specialization
      A top-down design activity in which a general base class is refined
      into derived classes that extend or override its behavior for a
      specific context. Each subclass carries only the attributes and
      methods unique to that type, avoiding ``None`` placeholders for
      inapplicable fields. Contrast with generalization.

   Static Method
      A method defined with the ``@staticmethod`` decorator. It receives
      neither ``self`` nor ``cls`` and has no implicit access to instance
      or class state. Behaves like a regular function but lives in the
      class namespace for organizational clarity. Common uses: validation
      helpers, unit conversions, and pure computations logically related
      to the class.

   Structural Subtyping
      A typing model in which compatibility between a class and an
      interface is determined by the presence of the required methods and
      attributes, not by explicit inheritance. Implemented in Python via
      ``typing.Protocol``. Contrast with nominal typing (used by ABCs),
      where a class must explicitly inherit from the interface to be
      considered compatible.

   ``super()``
      A built-in function that returns a proxy object used to delegate
      method calls to the next class in the MRO. Always use the
      no-argument form ``super()`` in Python 3. Call
      ``super().__init__()`` as the first line of a child ``__init__``
      so that parent attributes are initialized before the child tries
      to use them. Can be used in any method, not just ``__init__``.