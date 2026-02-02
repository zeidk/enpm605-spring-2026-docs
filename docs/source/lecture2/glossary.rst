====================================================
Glossary
====================================================

:ref:`A <l2-glossary-a>` · :ref:`B <l2-glossary-b>` · :ref:`C <l2-glossary-c>` · :ref:`E <l2-glossary-e>` · :ref:`F <l2-glossary-f>` · :ref:`I <l2-glossary-i>` · :ref:`L <l2-glossary-l>` · :ref:`M <l2-glossary-m>` · :ref:`N <l2-glossary-n>` · :ref:`O <l2-glossary-o>` · :ref:`P <l2-glossary-p>` · :ref:`R <l2-glossary-r>` · :ref:`S <l2-glossary-s>` · :ref:`T <l2-glossary-t>` · :ref:`W <l2-glossary-w>`

----


.. _l2-glossary-a:

A
=

.. glossary::

   Arithmetic Operator
      An operator that performs mathematical computation. Python's
      arithmetic operators are ``+``, ``-``, ``*``, ``/`` (true
      division), ``//`` (floor division), ``%`` (modulus), and ``**``
      (exponentiation).

   Augmented Assignment
      A shorthand that combines an arithmetic operation with
      assignment, e.g., ``x += 5`` is equivalent to ``x = x + 5``.
      Other forms include ``-=``, ``*=``, ``/=``, ``//=``, ``%=``,
      and ``**=``.


.. _l2-glossary-b:

B
=

.. glossary::

   bool
      Python's Boolean type, a subclass of ``int`` with exactly two
      instances: ``True`` (``1``) and ``False`` (``0``). The built-in
      ``bool()`` function converts any value to a Boolean using
      :term:`truthiness <Truthy>` rules.


.. _l2-glossary-c:

C
=

.. glossary::

   Chained Comparison
      A Python feature that allows multiple relational operators in a
      single expression, e.g., ``1 < x < 10`` is equivalent to
      ``1 < x and x < 10``. Each operand is evaluated at most once.

   Conditional Expression
   Ternary Expression
      A single-line ``if``/``else`` construct that produces a value:
      ``value_if_true if condition else value_if_false``. Useful for
      simple assignments but should not replace multi-line ``if``
      blocks for complex logic.

   Concatenation
      Joining strings end-to-end. In Python, use the ``+`` operator
      for a small number of strings or ``str.join()`` for joining
      many strings efficiently.


.. _l2-glossary-e:

E
=

.. glossary::

   Escape Sequence
      A backslash-prefixed character combination inside a string
      literal that represents a special character, e.g., ``\n``
      (newline), ``\t`` (tab), ``\\`` (literal backslash), ``\"``
      (literal double quote). Suppressed by using a raw string
      (``r"..."``).


.. _l2-glossary-f:

F
=

.. glossary::

   Falsy
      A value that evaluates to ``False`` when passed to ``bool()``.
      Python's falsy values are: ``0``, ``0.0``, ``""``, ``[]``,
      ``()``, ``{}``, ``set()``, ``None``, and ``False`` itself.
      Contrast with :term:`Truthy`.

   Floor Division
      Integer division that rounds toward negative infinity, performed
      by the ``//`` operator. ``10 // 3`` is ``3``; ``10 // -3`` is
      ``-4`` (not ``-3``).

   f-string
   Formatted String Literal
      A string prefixed with ``f`` or ``F`` that allows embedded
      Python expressions inside curly braces: ``f"Hello, {name}"``.
      Introduced in Python 3.6. Supports format specifiers such as
      ``.2f`` (two decimal places) and ``>20`` (right-align in 20
      characters).


.. _l2-glossary-i:

I
=

.. glossary::

   Identity Operator
      The ``is`` and ``is not`` operators, which test whether two
      names reference the exact same object in memory (same ``id``).
      Use ``is`` only for :term:`None` checks; use ``==`` for value
      comparison.

   import
      A statement that makes names from another :term:`module <Module>`
      or :term:`package <Package>` available in the current namespace.
      Common forms: ``import math``, ``from math import sqrt``,
      ``import math as m``.

   Indentation
      Whitespace at the beginning of a line that defines a code block
      in Python. PEP 8 prescribes **4 spaces** per level. Mixing tabs
      and spaces causes ``IndentationError``.

   Interning
      A CPython optimization that reuses the same object for small
      integers (typically ``-5`` through ``256``) and compile-time
      string constants. Never rely on interning for correctness.


.. _l2-glossary-l:

L
=

.. glossary::

   Logical Operator
      The ``and``, ``or``, and ``not`` operators, which combine or
      negate Boolean expressions. Python's logical operators use
      :term:`short-circuit evaluation`.


.. _l2-glossary-m:

M
=

.. glossary::

   Membership Operator
      The ``in`` and ``not in`` operators, which test whether an
      element exists within a sequence (string, list, tuple, set, or
      dict keys). ``"h" in "hello"`` evaluates to ``True``.

   Modular Programming
      A software design approach that breaks a program into separate,
      reusable units (:term:`modules <Module>` and :term:`packages
      <Package>`), each responsible for a specific piece of
      functionality.

   Module
      A single ``.py`` file containing functions, classes, and
      variables. Modules are imported with the ``import`` statement
      and are the basic unit of code organization in Python.

   Modulus
      The remainder after floor division, computed by the ``%``
      operator. ``7 % 3`` is ``1``. Useful for checking divisibility
      (``n % 2 == 0`` tests whether ``n`` is even).


.. _l2-glossary-n:

N
=

.. glossary::

   Namespace
      A mapping from names to objects. Every module, function, and
      class has its own namespace. :term:`Wildcard imports
      <Wildcard Import>` pollute the current namespace.

   Namespace Pollution
      When too many names are imported into the current namespace,
      increasing the risk of accidental name collisions. Caused
      primarily by :term:`wildcard imports <Wildcard Import>`.

   Nested Condition
      An ``if`` statement inside another ``if`` block. While sometimes
      necessary, deeply nested conditions can often be simplified using
      ``elif`` chains or combined Boolean expressions.


.. _l2-glossary-o:

O
=

.. glossary::

   Operator Precedence
      The rules that determine which operator is evaluated first when
      an expression contains multiple operators. In Python (highest to
      lowest): ``**``, unary ``+``/``-``, ``*``/``/``/``//``/``%``,
      ``+``/``-``, comparisons, ``not``, ``and``, ``or``. Use
      parentheses for clarity.


.. _l2-glossary-p:

P
=

.. glossary::

   Package
      A directory containing ``.py`` files (modules) and optionally an
      ``__init__.py`` file. Packages allow hierarchical organization of
      modules, e.g., ``shape.square``.


.. _l2-glossary-r:

R
=

.. glossary::

   Raw String
      A string literal prefixed with ``r`` that treats backslashes as
      literal characters: ``r"C:\Users\notes"`` contains two literal
      backslashes. Useful for file paths and regular expressions.

   Relational Operator
      An operator that compares values and returns ``True`` or
      ``False``: ``==``, ``!=``, ``>``, ``<``, ``>=``, ``<=``.
      Python supports :term:`chained comparisons <Chained Comparison>`.


.. _l2-glossary-s:

S
=

.. glossary::

   Short-Circuit Evaluation
      A behavior of :term:`logical operators <Logical Operator>` where
      the second operand is not evaluated if the result is already
      determined. ``and`` stops at the first falsy value; ``or`` stops
      at the first truthy value.

   Slicing
      Extracting a subsequence from a sequence using the syntax
      ``[start:stop:stride]``. ``start`` is inclusive, ``stop`` is
      exclusive, and ``stride`` defaults to ``1``. Negative indices
      count from the end.

   String Interning
      See :term:`Interning`.

   sys.path
      A list of directory paths that Python searches when resolving
      ``import`` statements. Modify with ``sys.path.insert()`` to
      add custom directories.


.. _l2-glossary-t:

T
=

.. glossary::

   Truthy
      A value that evaluates to ``True`` when passed to ``bool()``.
      Any non-zero number, non-empty string, or non-empty collection
      is truthy. Contrast with :term:`Falsy`.

   Truthiness
      The concept that every Python object has an inherent Boolean
      value. Pythonic code leverages truthiness directly in conditions:
      ``if my_list:`` rather than ``if len(my_list) > 0:``.


.. _l2-glossary-w:

W
=

.. glossary::

   Wildcard Import
      An import of the form ``from module import *`` that brings every
      public name from a module into the current namespace. Strongly
      discouraged because it causes :term:`namespace pollution` and
      makes it impossible to tell where a name originated.

   ``__init__.py``
      A file that marks a directory as a Python :term:`package`. May
      be empty or may contain package-level initialization code and
      ``__all__`` definitions to control wildcard imports.

   ``__name__``
      A special variable set to ``"__main__"`` when a module is run
      directly and to the module's own name when imported. The
      ``if __name__ == '__main__':`` guard prevents code from running
      on import.