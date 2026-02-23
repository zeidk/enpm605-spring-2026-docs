====================================================
Glossary
====================================================

:ref:`C <l5-glossary-c>` · :ref:`D <l5-glossary-d>` · :ref:`F <l5-glossary-f>` · :ref:`H <l5-glossary-h>` · :ref:`I <l5-glossary-i>` · :ref:`L <l5-glossary-l>` · :ref:`P <l5-glossary-p>` · :ref:`S <l5-glossary-s>` · :ref:`W <l5-glossary-w>`

----


.. _l5-glossary-c:

C
=

.. glossary::

   Callback
      A function passed as an argument to another function, to be called
      at a later time. Callbacks are commonly used in event-driven
      programming and frameworks such as ROS 2, where subscriber nodes
      pass a callback function that is invoked each time a new message
      arrives.

   Callable
      Any object that can be invoked using parentheses ``()``. In Python,
      callables include functions defined with ``def``, lambda expressions,
      classes (calling a class creates an instance), instances with a
      ``__call__`` method, and built-in functions. Use ``callable(obj)``
      to check.

   Closure
      A function that retains access to variables from its enclosing
      scope, even after the enclosing function has finished executing.
      Three conditions are required: a nested function, a reference to a
      free variable from the enclosing scope, and the enclosing function
      returning the nested function. The captured variables are stored in
      cell objects accessible via ``__closure__``.


.. _l5-glossary-d:

D
=

.. glossary::

   Decorator
      A function that takes another function as input, adds functionality,
      and returns a new function (or the same function modified). The
      ``@decorator`` syntax placed above a function definition is syntactic
      sugar for ``func = decorator(func)``. Decorators are used for
      cross-cutting concerns such as logging, timing, access control, and
      caching.

   Decorator Factory
      A function that accepts arguments and returns a decorator. Used when
      a decorator itself needs to be parameterized. Requires three levels
      of nesting: ``factory(args) -> decorator(func) -> wrapper(*args, **kwargs)``.
      Example: ``@repeat(3)`` where ``repeat`` is the factory.

   Dispatch Table
      A dictionary that maps keys (such as strings) to functions. Used to
      select and call a function based on a runtime value, replacing long
      ``if``/``elif`` chains. Example:
      ``operations = {"add": add, "multiply": multiply}``.


.. _l5-glossary-f:

F
=

.. glossary::

   First-Class Object
      An entity that can be assigned to a variable, passed as an argument,
      returned from a function, and stored in a data structure. In Python,
      functions are first-class objects, which means they can be
      manipulated like any other value (integers, strings, lists).

   Free Variable
      A variable referenced inside a function that is not defined in that
      function's local scope. In the context of closures, free variables
      are defined in the enclosing function's scope and captured by the
      inner function via cell objects.

   ``functools.partial``
      A function from the ``functools`` module that creates a new callable
      with some arguments of the original function pre-filled ("frozen").
      The returned partial object has ``.func``, ``.args``, and
      ``.keywords`` attributes for introspection.

   ``functools.wraps``
      A decorator from the ``functools`` module that copies metadata
      (``__name__``, ``__doc__``, ``__module__``, ``__qualname__``,
      ``__annotations__``, ``__dict__``, ``__wrapped__``) from the
      original function onto a wrapper function. Essential for preserving
      introspection in decorators.

   Functional Programming
      A programming paradigm that expresses computation as the evaluation
      of mathematical functions. Emphasizes pure functions, immutability,
      avoiding side effects, and higher-order functions. Python supports
      functional programming alongside procedural and object-oriented
      styles.


.. _l5-glossary-h:

H
=

.. glossary::

   Higher-Order Function
      A function that takes one or more functions as arguments, returns a
      function, or both. Built-in examples include ``map``, ``filter``,
      and ``sorted`` (with its ``key`` parameter). Decorators are also
      higher-order functions.


.. _l5-glossary-i:

I
=

.. glossary::

   Immutability
      The property of an object whose state cannot be changed after
      creation. In functional programming, immutability is preferred
      because it eliminates side effects and makes code easier to reason
      about. Python's built-in immutable types include ``int``, ``str``,
      ``tuple``, and ``frozenset``.


.. _l5-glossary-l:

L
=

.. glossary::

   Lambda
      A small anonymous function defined with the ``lambda`` keyword.
      Limited to a single expression (no statements, no multi-line logic,
      no docstrings, no type hints). Commonly used as short inline
      callbacks for ``sorted(key=...)``, ``map``, and ``filter``. PEP 8
      discourages assigning lambdas to variable names.

   Lazy Iterator
      An object that produces values one at a time on demand rather than
      computing all values upfront. ``map`` and ``filter`` return lazy
      iterators in Python 3. Wrap in ``list()`` to materialize all
      results.


.. _l5-glossary-p:

P
=

.. glossary::

   Parameterized Decorator
      A decorator that accepts arguments. Implemented as a decorator
      factory: a function that takes the decorator's arguments and returns
      the actual decorator. Uses three nested functions:
      ``factory(args) -> decorator(func) -> wrapper(*args, **kwargs)``.

   Programming Paradigm
      A fundamental style or approach to organizing and structuring code.
      The three major paradigms are procedural (step-by-step instructions),
      object-oriented (data and behavior bundled in objects), and
      functional (computation as function evaluation). Python supports all
      three as a multi-paradigm language.

   Pure Function
      A function whose output depends only on its inputs and that produces
      no side effects. Given the same inputs, a pure function always
      returns the same output. Pure functions do not modify external state,
      perform I/O, or depend on mutable global variables.


.. _l5-glossary-s:

S
=

.. glossary::

   Side Effect
      Any observable change that a function makes beyond returning a
      value. Examples include modifying a global variable, mutating a
      mutable argument, printing to the console, writing to a file, or
      making a network request. Functional programming aims to minimize
      side effects.

   Syntactic Sugar
      Syntax that makes code easier to read or write but does not add new
      functionality. The ``@decorator`` syntax is syntactic sugar for
      ``func = decorator(func)``. Similarly, list comprehensions are
      syntactic sugar for loops that build lists.


.. _l5-glossary-w:

W
=

.. glossary::

   Wrapper Function
      The inner function in a decorator that replaces the original
      function. It typically accepts ``*args`` and ``**kwargs`` to work
      with any function signature, adds the decorator's behavior (such as
      logging or timing), calls the original function, and returns its
      result. Should always use ``@functools.wraps`` to preserve the
      original function's metadata.
