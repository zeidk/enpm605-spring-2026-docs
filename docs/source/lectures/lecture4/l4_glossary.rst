====================================================
Glossary
====================================================

:ref:`A <l4-glossary-a>` · :ref:`B <l4-glossary-b>` · :ref:`C <l4-glossary-c>` · :ref:`D <l4-glossary-d>` · :ref:`E <l4-glossary-e>` · :ref:`F <l4-glossary-f>` · :ref:`G <l4-glossary-g>` · :ref:`K <l4-glossary-k>` · :ref:`L <l4-glossary-l>` · :ref:`N <l4-glossary-n>` · :ref:`O <l4-glossary-o>` · :ref:`P <l4-glossary-p>` · :ref:`R <l4-glossary-r>` · :ref:`S <l4-glossary-s>`

----


.. _l4-glossary-a:

A
=

.. glossary::

   Argument
      A value passed to a function when it is called. Arguments are
      assigned to the function's parameters. Python supports positional
      arguments, keyword arguments, and unpacking with ``*`` and ``**``.

   ``*args``
      A parameter prefix that collects any extra positional arguments
      into a tuple. Defined as ``*args`` in the function signature.
      Example: ``def func(*args):`` allows ``func(1, 2, 3)`` where
      ``args`` is ``(1, 2, 3)``.


.. _l4-glossary-b:

B
=

.. glossary::

   Base Case
      The condition in a recursive function that stops the recursion.
      Without a base case, the function will recurse until Python raises
      a ``RecursionError``. Example: ``if n <= 1: return 1`` in a
      factorial function.

   Built-in Scope
      The outermost scope in the LEGB rule, containing Python's
      pre-defined names such as ``print``, ``len``, ``int``, ``True``,
      and ``None``. These are defined in the ``builtins`` module.


.. _l4-glossary-c:

C
=

.. glossary::

   Call Stack
      The data structure Python uses to track active function calls. Each
      function call creates a frame object that is pushed onto the stack.
      When the function returns, its frame is popped. The stack enables
      nested and recursive function calls.

   Cell Object
      An internal CPython mechanism used to share variables between
      enclosing and nested functions. Cell objects are mutable containers
      that hold a single reference, enabling the ``nonlocal`` keyword
      to work across scope boundaries.


.. _l4-glossary-d:

D
=

.. glossary::

   Default Argument
      A parameter value specified in the function definition that is used
      when the caller does not provide that argument. Default values are
      evaluated once at definition time, not at each call. Mutable
      defaults (like lists) should be avoided; use ``None`` instead.

   Docstring
      A string literal that appears as the first statement in a function,
      class, or module. Used to document the purpose, parameters, and
      return value. Accessible at runtime via ``func.__doc__``. This
      course uses Google-style docstrings with ``Args`` and ``Returns``
      sections.


.. _l4-glossary-e:

E
=

.. glossary::

   Enclosing Scope
      The scope of an outer function when using nested functions. In the
      LEGB rule, Python checks the enclosing scope after the local scope.
      Variables in the enclosing scope can be read by inner functions and
      modified using the ``nonlocal`` keyword.


.. _l4-glossary-f:

F
=

.. glossary::

   Frame Object
      A heap-allocated ``PyFrameObject`` struct created by CPython for
      each function call. Contains the local variables array
      (``f_localsplus``), a pointer to the globals dictionary
      (``f_globals``), the builtins dictionary (``f_builtins``), and a
      back-pointer to the caller's frame (``f_back``).

   Function
      A named, reusable block of code defined with the ``def`` keyword.
      Functions accept input through parameters, execute a body of
      statements, and optionally return a value. They are first-class
      objects in Python.


.. _l4-glossary-g:

G
=

.. glossary::

   Global Scope
      The module-level scope containing variables defined outside of any
      function. In the LEGB rule, Python checks the global scope after
      local and enclosing scopes. The ``global`` keyword allows a
      function to modify variables in this scope.

   ``global`` Keyword
      A statement that declares a variable inside a function as referring
      to the module-level (global) variable of the same name. Without it,
      assignment inside a function creates a new local variable.


.. _l4-glossary-k:

K
=

.. glossary::

   Keyword Argument
      An argument passed to a function by explicitly naming the
      parameter: ``func(name="Alice")``. Keyword arguments can appear in
      any order and make function calls more readable.

   ``**kwargs``
      A parameter prefix that collects any extra keyword arguments into
      a dictionary. Defined as ``**kwargs`` in the function signature.
      Example: ``def func(**kwargs):`` allows ``func(x=1, y=2)`` where
      ``kwargs`` is ``{'x': 1, 'y': 2}``.


.. _l4-glossary-l:

L
=

.. glossary::

   LEGB Rule
      The order in which Python resolves variable names: Local, Enclosing,
      Global, Built-in. Python searches each scope in this order and uses
      the first match found. This is the fundamental mechanism for
      variable name resolution in Python.

   Local Scope
      The innermost scope, containing variables defined inside the
      current function (including parameters). Local variables are stored
      in a fast-access array (``f_localsplus``) on the frame object and
      accessed via ``LOAD_FAST``/``STORE_FAST`` bytecode instructions.


.. _l4-glossary-n:

N
=

.. glossary::

   Nested Function
      A function defined inside another function. The inner function has
      access to variables in the enclosing function's scope. Nested
      functions are the foundation for closures and decorators (covered
      in L5).

   ``nonlocal`` Keyword
      A statement that declares a variable inside a nested function as
      referring to a variable in the enclosing function's scope. Without
      it, assignment inside the inner function would create a new local
      variable instead of modifying the enclosing one.


.. _l4-glossary-o:

O
=

.. glossary::

   ``Optional``
      A type hint from the ``typing`` module indicating that a value can
      be of a specified type or ``None``. ``Optional[int]`` is equivalent
      to ``Union[int, None]``. In Python 3.10+, the shorthand
      ``int | None`` can be used instead.


.. _l4-glossary-p:

P
=

.. glossary::

   Parameter
      A variable listed in a function's definition that receives a value
      when the function is called. Parameters define the function's
      interface. Distinguished from arguments: parameters are in the
      definition, arguments are in the call.

   Pass-by-Assignment
      Python's argument-passing mechanism, sometimes called
      "pass-by-object-reference." The function receives a reference to
      the object, not a copy. In-place mutations on mutable objects
      affect the original; reassignment creates a new local binding
      without affecting the caller.

   Positional Argument
      An argument matched to a parameter by its position in the function
      call. The first argument is assigned to the first parameter, the
      second to the second, and so on.


.. _l4-glossary-r:

R
=

.. glossary::

   Recursion
      A programming technique where a function calls itself to solve a
      problem by breaking it into smaller sub-problems. Every recursive
      function requires a :term:`Base Case` and a recursive case.
      Python limits recursion depth to 1000 by default.

   ``return`` Statement
      A statement that exits a function and optionally sends a value back
      to the caller. Multiple values can be returned as a tuple.
      Functions without a ``return`` statement implicitly return ``None``.


.. _l4-glossary-s:

S
=

.. glossary::

   Scope
      The region of a program where a variable name is accessible. Python
      uses the :term:`LEGB Rule` to determine which scope a name belongs
      to. Each function call creates a new local scope.

   Shadowing
      When a variable in an inner scope has the same name as a variable
      in an outer scope, hiding the outer variable. For example, a local
      variable named ``x`` shadows a global variable named ``x`` within
      that function.