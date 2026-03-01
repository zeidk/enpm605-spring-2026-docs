====================================================
Glossary
====================================================

:ref:`A <l6-glossary-a>` · :ref:`B <l6-glossary-b>` · :ref:`C <l6-glossary-c>` · :ref:`D <l6-glossary-d>` · :ref:`E <l6-glossary-e>` · :ref:`I <l6-glossary-i>` · :ref:`M <l6-glossary-m>` · :ref:`N <l6-glossary-n>` · :ref:`O <l6-glossary-o>` · :ref:`P <l6-glossary-p>` · :ref:`R <l6-glossary-r>` · :ref:`S <l6-glossary-s>` · :ref:`U <l6-glossary-u>`

----


.. _l6-glossary-a:

A
=

.. glossary::

   Abstraction
      The principle of hiding complex implementation details behind a
      simple interface. Users interact with an object through its public
      methods without needing to know how those methods work internally.
      Example: calling ``robot.move("north")`` without knowing about motor
      controllers or path planning.

   Aggregation
      A "has-a" relationship where the part can exist independently of
      the whole. Example: a ``Team`` has ``Robot``\(s), but dissolving the
      team does not destroy the robots.

   Association
      A general relationship between two classes where neither owns the
      other. Example: a ``Task`` is assigned to a ``Robot``; both exist
      independently and the assignment can be broken.


.. _l6-glossary-b:

B
=

.. glossary::

   Business Rule
      A constraint, trigger, or computation that the system must enforce
      as part of domain logic. Business rules directly influence class
      design by determining which validations go into methods, which
      attributes need constraints, and which relationships must be
      enforced. Identified with prefixes: BR-C (constraint), BR-T
      (trigger), BR-D (computation).


.. _l6-glossary-c:

C
=

.. glossary::

   CamelCase
      A naming convention where each word starts with a capital letter
      and no underscores are used. In Python, class names follow
      CamelCase by convention (e.g., ``RobotArm``, ``SensorFusion``),
      while functions and variables use ``snake_case``.

   Class
      A blueprint that defines the attributes (data) and methods
      (functions) that its objects will have. Defined using the ``class``
      keyword followed by the name in CamelCase. In Python 3, all
      classes implicitly inherit from ``object``.

   Class Attribute
      An attribute defined inside the class body but outside any method.
      Shared by all instances of the class. Accessed via the class name
      (``ClassName.attr``) or via any instance. Commonly used for
      constants and counters (e.g., ``total_robots``).

   Composition
      A "has-a" relationship where the part cannot exist without the
      whole. Example: a ``Robot`` owns its ``Sensor``\(s); destroying the
      robot destroys its sensors. This is a stronger relationship than
      aggregation.


.. _l6-glossary-d:

D
=

.. glossary::

   Design Phase
      The process of translating a real-world problem into a workable
      software structure before writing any code. Includes requirement
      analysis, business rules, noun/verb analysis, UML modeling, and
      implementation planning.

   Dot Notation
      The syntax used to access attributes and methods on an object:
      ``obj.attribute`` or ``obj.method()``. Python uses dot notation for
      all member access.

   Dunder Method
      A Python method with double leading and trailing underscores (e.g.,
      ``__init__``, ``__str__``, ``__add__``). Dunder methods enable
      operator overloading and integration with built-in functions.
      "Dunder" is short for "double underscore."


.. _l6-glossary-e:

E
=

.. glossary::

   Encapsulation
      The bundling of data (attributes) with the methods that operate on
      that data, while restricting direct access to internal state. In
      Python, encapsulation is achieved by convention: prefix non-public
      attributes with an underscore (``_attr``) and provide controlled
      access through ``@property`` decorators.


.. _l6-glossary-i:

I
=

.. glossary::

   ``__init__``
      A special dunder method called automatically when a new instance is
      created. Used to initialize the object's attributes. It is an
      initializer, not a constructor; the actual constructor is
      ``__new__``, which is rarely overridden.

   Instance
      A concrete realization of a class, also called an object. Created
      by calling the class as if it were a function:
      ``obj = ClassName(args)``. Each instance has its own attribute
      values and operates independently of other instances.

   Instance Attribute
      An attribute that belongs to a specific object. Created inside
      ``__init__`` using ``self.attr = value``. Each instance maintains
      its own copy, so modifying one instance does not affect others.


.. _l6-glossary-m:

M
=

.. glossary::

   Method
      A function defined inside a class that operates on instances of
      that class. The first parameter is conventionally named ``self``,
      which refers to the instance calling the method. Methods are
      invoked using dot notation: ``obj.method(args)``.

   Method Overriding
      When a child class provides its own version of a method that the
      parent class already has, replacing the inherited behavior. Covered
      in detail in L7 with inheritance.


.. _l6-glossary-n:

N
=

.. glossary::

   Name Mangling
      A Python mechanism triggered by a double leading underscore
      (``__attr``). Python renames the attribute to
      ``_ClassName__attr`` to reduce the chance of accidental access
      from subclasses. Rarely needed in practice.

   Noun/Verb Analysis
      A technique for extracting candidate classes (nouns) and methods
      (verbs) from a natural-language problem description. Nouns map to
      classes or attributes, verbs map to methods, and relational phrases
      ("has a", "is a") map to composition or inheritance relationships.


.. _l6-glossary-o:

O
=

.. glossary::

   Object
      A concrete realization of a class (synonym for instance). Objects
      bundle data (attributes) and behavior (methods) together. Multiple
      objects can be created from the same class, each with independent
      state.

   Operator Overloading
      Teaching Python what an existing operator (``+``, ``==``, ``>``,
      etc.) should do when applied to your own class. Achieved by
      implementing the corresponding dunder method (e.g., ``__add__``
      for ``+``, ``__eq__`` for ``==``). Different from method
      overriding, which involves a child class replacing an inherited
      method.


.. _l6-glossary-p:

P
=

.. glossary::

   Property
      A Python mechanism (via the ``@property`` decorator) that allows
      controlled access to an attribute through getter and setter methods
      while preserving attribute-style syntax. The getter is triggered by
      ``obj.attr`` and the setter by ``obj.attr = value``. Used
      throughout OOP to enforce validation on assignment.

   ``@property``
      A built-in decorator that transforms a method into a read-only
      attribute. Combined with ``@attr.setter``, it provides validation
      and control over attribute access without changing the external
      interface. Preferred over explicit getter/setter methods in Python.


.. _l6-glossary-r:

R
=

.. glossary::

   Requirement Analysis
      The process of identifying **what** the system must do (functional
      requirements) and **how well** it must do it (non-functional
      requirements). The first step in the design workflow.

   ``__repr__``
      A dunder method called by ``repr()``, the REPL, the debugger, and
      when objects appear inside containers (lists, dicts). Should return
      a string that looks like the code you would type to create the
      object (e.g., ``Robot('Scout', 100)``). Serves as the fallback for
      ``__str__`` if ``__str__`` is not defined.


.. _l6-glossary-s:

S
=

.. glossary::

   ``self``
      The conventional name for the first parameter of instance methods.
      Refers to the specific instance that called the method. Python
      passes it automatically: ``obj.method(arg)`` is translated to
      ``ClassName.method(obj, arg)``.

   ``__str__``
      A dunder method called by ``print()`` and ``str()``. Should return
      a human-readable string intended for end users and display output.
      If not defined, Python falls back to ``__repr__``.


.. _l6-glossary-u:

U
=

.. glossary::

   UML
      Unified Modeling Language. A standardized notation for visualizing
      software design. This course uses class diagrams (structure),
      sequence diagrams (object interaction over time), and activity
      diagrams (control flow).
