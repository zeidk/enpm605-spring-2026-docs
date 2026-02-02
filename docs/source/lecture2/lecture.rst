====================================================
Lecture
====================================================



Packages and Modules
====================================================

Organizing Python code into reusable units.

Create a file called ``packages_demo.py`` to follow along with the examples below.


What Are They?
--------------

Modular programming breaks a large task into smaller, manageable subtasks called **modules**.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📄 Module
        :class-card: sd-border-info

        - A single ``.py`` file.
        - Contains functions, classes, and variables.
        - Example: ``math_utils.py``

    .. grid-item-card:: 📁 Package
        :class-card: sd-border-info

        - A folder containing ``.py`` files.
        - May include ``__init__.py``.
        - Example: ``shape/``

.. note::

   Python has a large collection of `standard modules <https://docs.python.org/3/py-modindex.html>`_. Standard and user-defined modules are imported the same way.


Making Packages Discoverable
-----------------------------

Python can only import packages that are on its **module search path** (``sys.path``). If your script and package live in **sibling directories**, Python may not find the package by default.

.. code-block:: python

   import sys
   import os

   # Add the parent directory to sys.path
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

- ``__file__`` — path to the current script.
- ``os.path.abspath()`` — resolves to a full absolute path.
- ``os.path.dirname()`` — goes up one directory level.
- ``sys.path.insert(0, ...)`` — adds the path to the front of the search list.

.. tip::

   Place this at the **very top** of your script, before any other imports that depend on the path.


Import Strategies
-----------------

There are four common ways to import names from a module.

**Approach 1 — Full module path:**

.. code-block:: python

   import shape.square
   result = shape.square.compute_area(4)

**Approach 2 — Alias:**

.. code-block:: python

   import shape.square as sq
   result = sq.compute_area(4)

**Approach 3 — Import specific names (recommended):**

.. code-block:: python

   from shape.square import compute_area, compute_perimeter
   result = compute_area(4)

**Approach 4 — Wildcard (avoid):**

.. code-block:: python

   from shape.square import *  # Namespace pollution risk!


Why Avoid Wildcard Imports?
---------------------------

``import *`` dumps **every** name from a module into your current namespace, which can silently overwrite existing variables or functions.

.. code-block:: python

   from shape.square import *    # brings in compute_area, compute_perimeter
   from shape.circle import *    # also brings in compute_area, compute_perimeter

   result = compute_area(4)      # Which version is this? circle!

- ``compute_area`` from ``square`` is **silently overwritten** by ``circle``'s version.
- No error, no warning — your code just computes the wrong thing.
- Readers cannot tell which module a function came from.

.. tip::

   **Best practice**: Use explicit named imports so it is always clear where each name originated.

   .. code-block:: python

      from shape.square import compute_area as square_area
      from shape.circle import compute_area as circle_area


The ``__name__`` Guard
-----------------------

When a module is run directly, its ``__name__`` is set to ``"__main__"``. When imported, ``__name__`` is set to the module's name.

.. code-block:: python

   import math

   def compute_area(base: float, height: float) -> float:
       return 0.5 * base * height

   def compute_perimeter(side1: float, side2: float, side3: float) -> float:
       return side1 + side2 + side3

   if __name__ == '__main__':
       # Only runs when executed directly, not when imported
       print(compute_area(4.5, 5.6))
       print(compute_area(4.7, 6.0))
       print(compute_area(4.8, 7.1))
       print(compute_area(4.9, 8.45))

.. note::

   This pattern allows a module to serve both as an importable library and as a standalone script.


Indentation
====================================================

Create a file called ``indentation_demo.py`` to follow along.


Python's Block Structure
------------------------

Unlike C++ or Java which use braces ``{}``, Python uses **indentation** to define blocks of code.

.. tab-set::

    .. tab-item:: 🐍 Python

        .. code-block:: python

           def greeting(name):
               print("Hello", name)
               if name == "Alice":
                   print("Welcome back!")

    .. tab-item:: ⚙️ C++

        .. code-block:: cpp

           void greeting(std::string name) {
               std::cout << "Hello " << name;
               if (name == "Alice") {
                   std::cout << "Welcome back!";
               }
           }

.. warning::

   Mixing tabs and spaces causes ``IndentationError``. Configure your editor to use **4 spaces** per indent level (PEP 8 standard).


Operators
====================================================

Arithmetic, relational, logical, membership, and identity operators.

Create a file called ``operators_demo.py`` to follow along with the examples below.


Arithmetic Operators
--------------------

.. list-table::
   :widths: 12 20 20 15
   :header-rows: 1
   :class: compact-table

   * - Operator
     - Operation
     - Example
     - Result
   * - ``+``
     - Addition
     - ``7 + 3``
     - ``10``
   * - ``-``
     - Subtraction
     - ``7 - 3``
     - ``4``
   * - ``*``
     - Multiplication
     - ``7 * 3``
     - ``21``
   * - ``/``
     - Division (float)
     - ``7 / 3``
     - ``2.333...``
   * - ``//``
     - Floor division
     - ``7 // 3``
     - ``2``
   * - ``%``
     - Modulus (remainder)
     - ``7 % 3``
     - ``1``
   * - ``**``
     - Exponentiation
     - ``2 ** 10``
     - ``1024``

.. code-block:: python

   # Floor division always rounds toward negative infinity
   print(10 // 3)    # 3
   print(10 // -3)   # -4 (not -3!)

   # Augmented assignment operators
   x = 10
   x += 5   # x = x + 5 -> 15
   x *= 2   # x = x * 2 -> 30


Relational Operators
---------------------

Relational operators compare **values** and return ``True`` or ``False``.

Let ``a = 5`` and ``b = 3``:

.. list-table::
   :widths: 12 25 25
   :header-rows: 1
   :class: compact-table

   * - Operator
     - Description
     - Example
   * - ``==``
     - Equal
     - ``a == b`` is ``False``
   * - ``!=``
     - Not equal
     - ``a != b`` is ``True``
   * - ``>``
     - Greater than
     - ``a > b`` is ``True``
   * - ``<``
     - Less than
     - ``a < b`` is ``False``
   * - ``>=``
     - Greater than or equal
     - ``a >= 5`` is ``True``
   * - ``<=``
     - Less than or equal
     - ``a <= b`` is ``False``

.. code-block:: python

   # Python supports chained comparisons
   x = 5
   print(1 < x < 10)   # True (equivalent to 1 < x and x < 10)
   print(1 < x > 3)    # True


Logical Operators
-----------------

Logical operators combine Boolean expressions.

Let ``a = True`` and ``b = False``:

.. list-table::
   :widths: 12 40 25
   :header-rows: 1
   :class: compact-table

   * - Operator
     - Description
     - Example
   * - ``and``
     - ``True`` if both operands are ``True``
     - ``a and b`` is ``False``
   * - ``or``
     - ``True`` if at least one is ``True``
     - ``a or b`` is ``True``
   * - ``not``
     - Reverses the logical state
     - ``not a`` is ``False``

.. code-block:: python

   # Short-circuit evaluation
   x = 5
   print(x > 0 and x < 10)    # True
   print(x > 10 or x == 5)    # True
   print(not (x == 5))        # False

   # Logical operators with non-boolean values
   print("hello" and 0)       # 0 (returns last evaluated operand)
   print("hello" or 0)        # "hello"
   print(not "")              # True (empty string is falsy)


Membership and Identity Operators
----------------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🔍 Membership Operators
        :class-card: sd-border-info

        Test if an element belongs in a sequence.

        .. list-table::
           :widths: 15 40
           :header-rows: 1
           :class: compact-table

           * - Operator
             - Description
           * - ``in``
             - ``True`` if found
           * - ``not in``
             - ``True`` if not found

        .. code-block:: python

           x = "hello"
           print("h" in x)      # True
           print("he" in x)     # True
           print("O" in x)      # False
           print("z" not in x)  # True

    .. grid-item-card:: 🆔 Identity Operators
        :class-card: sd-border-info

        Compare memory locations of objects.

        .. list-table::
           :widths: 15 40
           :header-rows: 1
           :class: compact-table

           * - Operator
             - Description
           * - ``is``
             - Same object (same ``id``)
           * - ``is not``
             - Different objects

        .. code-block:: python

           a = [1, 2, 3]
           b = [1, 2, 3]
           c = a

           print(a == b)   # True (same values)
           print(a is b)   # False (different objects)
           print(a is c)   # True (same object)

.. important::

   **Rule**: Use ``==`` for value comparison. Use ``is`` only for ``None`` checks.


Boolean Type
====================================================

Truth values, truthiness, and the ``bool()`` function.

Create a file called ``boolean_demo.py`` to follow along with the examples below.


The ``bool`` Type
-----------------

Python provides the Boolean type ``bool`` with exactly two values: ``True`` and ``False``.

- ``bool`` is a subclass of ``int``: ``True`` is ``1`` and ``False`` is ``0``.
- In a condition, any non-zero value or non-empty sequence evaluates to ``True``.
- The built-in ``bool()`` function converts a value to a Boolean.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ❌ Falsy Values
        :class-card: sd-border-danger

        .. code-block:: python

           print(bool(0))       # False
           print(bool(0.0))     # False
           print(bool(""))      # False
           print(bool([]))      # False
           print(bool({}))      # False
           print(bool(None))    # False

    .. grid-item-card:: ✅ Truthy Values
        :class-card: sd-border-success

        .. code-block:: python

           print(bool(1))       # True
           print(bool(-2))      # True
           print(bool("hi"))    # True
           print(bool([1, 2]))  # True
           print(bool(" "))     # True (space!)
           print(bool(0.001))   # True

.. tip::

   **Pythonic idiom**: Use truthiness directly in conditions — write ``if my_list:`` instead of ``if len(my_list) > 0:``.


Numeric Types
====================================================

Integers and Floats
-------------------

.. list-table::
   :widths: 12 10 30 20
   :header-rows: 1
   :class: compact-table

   * - Name
     - Type
     - Description
     - Examples
   * - Integer
     - ``int``
     - Whole numbers (unlimited precision)
     - ``1``, ``-42``, ``2000``
   * - Float
     - ``float``
     - Decimal numbers (64-bit IEEE 754)
     - ``2.5``, ``-0.001``, ``1e10``
   * - Complex
     - ``complex``
     - Complex numbers
     - ``1+2j``, ``3+8j``

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🔢 Integer Type
        :class-card: sd-border-info

        .. code-block:: python

           # Python ints have unlimited precision
           big = 10 ** 100
           print(type(big))  # <class 'int'>

           # Convert to int
           print(int(3.7))          # 3 (truncates)
           print(int("42"))         # 42
           print(int("101011", 2))  # 43 (binary)

    .. grid-item-card:: 🔢 Float Type
        :class-card: sd-border-info

        .. code-block:: python

           # Float precision limits
           print(0.1 + 0.2)         # 0.30000000000000004
           print(0.1 + 0.2 == 0.3)  # False!

           # Convert to float
           print(float("3.5"))   # 3.5
           print(float(3))       # 3.0
           print(float("inf"))   # inf

.. warning::

   Never compare floats with ``==``. Use ``math.isclose(a, b)`` or check ``abs(a - b) < epsilon`` instead.


Integer and String Interning
-----------------------------

CPython caches ("interns") small integers and compile-time string constants to save memory and speed up comparisons.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🔢 Integer Interning
        :class-card: sd-border-secondary

        .. code-block:: python

           a, b = 20, 20
           print(a is b)   # True (cached)

           a, b = -5, -5
           print(a is b)   # True (cached)

           # Large ints in the same statement
           a, b = 200000000000, 200000000000
           print(a is b)   # True (compile-time)

    .. grid-item-card:: 🔤 String Interning
        :class-card: sd-border-secondary

        .. code-block:: python

           a = "hello"
           b = "hello"
           c = "h" + "ello"   # Compile-time
           d = "".join(["h","e","l","l","o"])

           print(a is b)  # True
           print(a is c)  # True (folded at compile)
           print(a is d)  # False (runtime-built)

           import sys
           e = sys.intern(d)
           print(a is e)  # True (manually interned)

.. warning::

   Never rely on interning for correctness. Always use ``==`` for value comparison. Use ``is`` only for ``None`` checks.


String Type
====================================================

Strings, escape sequences, formatting, methods, indexing, and slicing.

Create a file called ``strings_demo.py`` to follow along with the examples below.


String Basics
-------------

A Python string (``str``) is an **immutable** sequence of characters.

.. code-block:: python

   # Single and double quotes are equivalent
   greeting = "Hello, World!"
   greeting2 = 'Hello, World!'

   # Triple quotes for multi-line strings
   description = """This is a
   multi-line string."""

   # String conversion
   number = 123
   number_str = str(number)
   print(type(number_str))  # <class 'str'>

**Escape Sequences:**

.. code-block:: python

   print("Line 1\nLine 2")          # Newline
   print("Col1\tCol2\tCol3")        # Tab
   print("She said: \"Hi!\"")       # Escaped quotes
   print('It\'s Python!')           # Escaped apostrophe
   print(r"C:\Users\tony\notes")    # Raw string (no escapes)


String Interpolation
---------------------

There are three ways to format strings in Python.

**Old-style (``%`` operator) — Legacy, avoid in new code:**

.. code-block:: python

   name, age = "Alice", 25
   print("Name: %s, Age: %d" % (name, age))

**str.format() — More flexible:**

.. code-block:: python

   print("Name: {}, Age: {}".format(name, age))
   print("Name: {name}, Age: {age}".format(name="Alice", age=25))

**f-strings (Python 3.6+) — Recommended:**

.. code-block:: python

   print(f"Name: {name}, Age: {age}")
   print(f"Next year: {age + 1}")
   print(f"Pi: {3.14159:.2f}")     # Format specifier: 3.14
   print(f"{'hello':>20}")          # Right-align in 20 chars

.. tip::

   **Use f-strings** for all new code. They are faster, more readable, and support inline expressions.


String Concatenation and Methods
---------------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🔗 Concatenation
        :class-card: sd-border-info

        .. code-block:: python

           # + operator
           first = "John"
           last = "Doe"
           full = first + " " + last

           # join() method (efficient)
           words = ["Hello", "World"]
           sentence = " ".join(words)
           print(sentence)  # Hello World

           # Repetition
           print("=" * 40)

    .. grid-item-card:: 🛠️ Common Methods
        :class-card: sd-border-info

        .. code-block:: python

           s = "Hello, World!"

           print(s.upper())       # HELLO, WORLD!
           print(s.lower())       # hello, world!
           print(s.capitalize())  # Hello, world!
           print(s.swapcase())    # hELLO, wORLD!
           print(s.strip())       # Remove whitespace
           print(s.replace("World", "Python"))
           print(s.split(", "))   # ['Hello', 'World!']
           print(s.find("World")) # 7
           print(s.count("l"))    # 3
           print(s.startswith("Hello"))  # True

.. note::

   String methods return **new strings** — they never modify the original (strings are immutable).


Indexing
--------

Strings are ordered sequences, so each character has a positional index.

.. list-table::
   :widths: 15 10 10 10 10 10
   :header-rows: 0
   :class: compact-table

   * - **String**
     - ``'h'``
     - ``'e'``
     - ``'l'``
     - ``'l'``
     - ``'o'``
   * - **+ Index**
     - 0
     - 1
     - 2
     - 3
     - 4
   * - **− Index**
     - −5
     - −4
     - −3
     - −2
     - −1

.. code-block:: python

   greeting = "hello"

   # Positive indexing
   print(greeting[0])    # 'h'
   print(greeting[4])    # 'o'

   # Negative indexing
   print(greeting[-1])   # 'o'
   print(greeting[-5])   # 'h'

   # Common errors
   # print(greeting[5])    # IndexError: string index out of range
   # greeting[0] = 'H'    # TypeError: strings are immutable


Slicing
-------

The slice syntax is ``[start:stop:stride]``:

- ``start``: Starting index (**inclusive**), defaults to 0.
- ``stop``: Ending index (**exclusive**), defaults to end.
- ``stride``: Step size, defaults to 1.

.. code-block:: python

   greeting = "hello"

   # Basic slicing
   print(greeting[0:3])   # "hel"
   print(greeting[:3])    # "hel" (start defaults to 0)
   print(greeting[2:])    # "llo" (stop defaults to end)
   print(greeting[:])     # "hello" (full copy)

   # Negative indices
   print(greeting[-5:-2]) # "hel"
   print(greeting[-3:])   # "llo"

   # With stride
   print(greeting[::2])   # "hlo" (every 2nd character)
   print(greeting[::-1])  # "olleh" (reverse!)
   print(greeting[4:1:-1])# "oll"


Control Flow
====================================================

Making decisions with ``if``, ``elif``, and ``else``.

Create a file called ``control_flow_demo.py`` to follow along with the examples below.


The ``if`` Statement
---------------------

Selection determines which code block executes based on conditions.

.. tab-set::

    .. tab-item:: Simple ``if``

        .. code-block:: python

           x = 10
           if x > 0:
               print("x is positive")
           print("always runs")

    .. tab-item:: ``if``-``else``

        .. code-block:: python

           x = -3
           if x >= 0:
               print("Non-negative")
           else:
               print("Negative")

    .. tab-item:: ``if``-``elif``-``else``

        .. code-block:: python

           score = 85

           if score >= 90:
               grade = "A"
           elif score >= 80:
               grade = "B"
           elif score >= 70:
               grade = "C"
           elif score >= 60:
               grade = "D"
           else:
               grade = "F"

           print(f"Grade: {grade}")  # Grade: B


Conditional Expressions
------------------------

Python supports single-line conditional assignment (the ternary expression).

.. code-block:: python

   age = 20
   status = "adult" if age >= 18 else "minor"
   print(status)  # "adult"

   # Equivalent to:
   if age >= 18:
       status = "adult"
   else:
       status = "minor"


Nested Conditions
-----------------

.. code-block:: python

   temperature = 25
   humidity = 80

   if temperature > 30:
       if humidity > 70:
           print("Hot and humid")
       else:
           print("Hot and dry")
   elif temperature > 20:
       print("Pleasant")  # This runs
   else:
       print("Cool")


Putting It All Together
====================================================

Preview: What's Next in L3
---------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📖 L3: Python Fundamentals — Part II
        :class-card: sd-border-primary

        - Lists and list methods
        - Tuples and unpacking
        - Dictionaries
        - Sets
        - Loops (``for``, ``while``)
        - List comprehensions

.. note::

   Today's lecture gives you the foundational tools — operators, strings, and control flow — that you will use constantly from L3 onward.