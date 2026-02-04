====================================================
Glossary
====================================================

:ref:`B <l3-glossary-b>` · :ref:`C <l3-glossary-c>` · :ref:`D <l3-glossary-d>` · :ref:`E <l3-glossary-e>` · :ref:`F <l3-glossary-f>` · :ref:`H <l3-glossary-h>` · :ref:`I <l3-glossary-i>` · :ref:`K <l3-glossary-k>` · :ref:`L <l3-glossary-l>` · :ref:`M <l3-glossary-m>` · :ref:`O <l3-glossary-o>` · :ref:`R <l3-glossary-r>` · :ref:`S <l3-glossary-s>` · :ref:`T <l3-glossary-t>` · :ref:`U <l3-glossary-u>` · :ref:`V <l3-glossary-v>` · :ref:`W <l3-glossary-w>`

----


.. _l3-glossary-b:

B
=

.. glossary::

   break
      A statement that immediately exits the innermost enclosing ``for``
      or ``while`` loop. When ``break`` executes, any ``else`` clause
      attached to the loop is skipped.


.. _l3-glossary-c:

C
=

.. glossary::

   Comprehension
      A concise syntax for creating collections by transforming and/or
      filtering elements from an iterable. Python supports list
      comprehensions (``[x for x in iter]``), dictionary comprehensions
      (``{k: v for k, v in iter}``), set comprehensions
      (``{x for x in iter}``), and generator expressions
      (``(x for x in iter)``).

   continue
      A statement that skips the rest of the current loop iteration and
      proceeds to the next iteration. Unlike ``break``, the loop
      continues running.


.. _l3-glossary-d:

D
=

.. glossary::

   Deep Copy
      A copy operation that recursively duplicates all nested objects,
      creating a completely independent copy. Performed using
      ``copy.deepcopy()``. Contrast with :term:`Shallow Copy`.

   Dictionary
   dict
      A mutable mapping type that stores key-value pairs. Keys must be
      :term:`hashable <Hashable>`. Since Python 3.7, dictionaries
      maintain insertion order. Access values with ``d[key]`` or
      ``d.get(key)``.

   Dictionary Comprehension
      A concise syntax for creating dictionaries:
      ``{key_expr: val_expr for item in iterable if condition}``.
      Returns a new ``dict`` object.

   Difference
      A set operation returning elements in the first set but not in
      the second. Performed with ``-`` operator or ``.difference()``
      method. ``{1, 2, 3} - {2, 3, 4}`` returns ``{1}``.


.. _l3-glossary-e:

E
=

.. glossary::

   enumerate()
      A built-in function that returns an iterator of tuples, each
      containing an index and the corresponding value from an iterable.
      ``enumerate(["a", "b"], start=1)`` yields ``(1, "a"), (2, "b")``.
      More Pythonic than ``range(len(...))``.

   else Clause (Loop)
      An optional clause after a ``for`` or ``while`` loop that executes
      only if the loop completes normally (without ``break``). Useful
      for search patterns where you need to know if an item was found.


.. _l3-glossary-f:

F
=

.. glossary::

   for Loop
      A control structure that iterates over items in an :term:`iterable`.
      Syntax: ``for item in iterable:``. The loop variable takes each
      value from the iterable in turn.

   fromkeys()
      A ``dict`` class method that creates a new dictionary with keys
      from an iterable and all values set to a specified default.
      ``dict.fromkeys(["a", "b"], 0)`` returns ``{"a": 0, "b": 0}``.


.. _l3-glossary-h:

H
=

.. glossary::

   Hashable
      An object is hashable if it has a hash value that never changes
      during its lifetime and can be compared to other objects.
      Immutable built-in types (``int``, ``str``, ``tuple``) are
      hashable. Mutable types (``list``, ``dict``, ``set``) are not.
      Only hashable objects can be dictionary keys or set elements.


.. _l3-glossary-i:

I
=

.. glossary::

   In-Place Operation
      An operation that modifies an object directly rather than creating
      a new object. List methods like ``append()``, ``sort()``, and
      ``reverse()`` are in-place and return ``None``. Contrast with
      :term:`Out-of-Place Operation`.

   Intersection
      A set operation returning elements present in both sets. Performed
      with ``&`` operator or ``.intersection()`` method.
      ``{1, 2, 3} & {2, 3, 4}`` returns ``{2, 3}``.

   Iterable
      Any object capable of returning its elements one at a time. This
      includes sequences (lists, strings, tuples), mappings
      (dictionaries), sets, files, and generators. An iterable can be
      used in a ``for`` loop or passed to functions like ``list()``,
      ``sum()``, or ``enumerate()``.

   Iterator
      An object representing a stream of data that returns successive
      items via the ``__next__()`` method. Iterators remember their
      position in the data stream. All iterators are iterables, but
      not all iterables are iterators.


.. _l3-glossary-k:

K
=

.. glossary::

   Key (Dictionary)
      The identifier used to access a value in a dictionary. Keys must
      be :term:`hashable <Hashable>` (immutable). Common key types are
      strings, integers, and tuples.


.. _l3-glossary-l:

L
=

.. glossary::

   Lazy Evaluation
      A strategy where values are computed only when needed. ``range()``
      uses lazy evaluation — it doesn't store all values in memory but
      generates them on demand. This makes ``range(1000000000)`` use
      the same memory as ``range(10)``.

   List
      A mutable, ordered sequence of objects. Created with square
      brackets ``[1, 2, 3]`` or the ``list()`` constructor. Elements
      can be of any type, including other lists (nested lists).

   List Comprehension
      A concise syntax for creating lists:
      ``[expression for item in iterable if condition]``. More readable
      and often faster than equivalent ``for`` loops with ``append()``.


.. _l3-glossary-m:

M
=

.. glossary::

   Mapping Type
      A container that associates keys with values. The primary mapping
      type in Python is :term:`dict`. Mappings support key-based
      access (``d[key]``) and key membership testing (``key in d``).

   Mutable
      An object whose value can be changed after creation. Lists,
      dictionaries, and sets are mutable. Integers, strings, and
      tuples are :term:`immutable <Immutable>`.


.. _l3-glossary-o:

O
=

.. glossary::

   Out-of-Place Operation
      An operation that returns a new object without modifying the
      original. The built-in ``sorted()`` function is out-of-place,
      returning a new list. String methods are out-of-place because
      strings are :term:`immutable <Immutable>`. Contrast with
      :term:`In-Place Operation`.


.. _l3-glossary-r:

R
=

.. glossary::

   range()
      A built-in function that returns an immutable sequence of integers.
      Syntax: ``range(stop)`` or ``range(start, stop, step)``. The
      ``stop`` value is never included. ``range()`` is memory-efficient
      because it uses :term:`lazy evaluation`.


.. _l3-glossary-s:

S
=

.. glossary::

   Sequence Type
      A container that stores elements in a specific order and supports
      indexing, slicing, and iteration. Built-in sequence types include
      ``list``, ``tuple``, ``str``, ``bytes``, and ``range``.

   Set
      A mutable, unordered collection of unique :term:`hashable
      <Hashable>` elements. Created with curly braces ``{1, 2, 3}`` or
      the ``set()`` constructor. Supports mathematical operations like
      union, intersection, and difference.

   Set Comprehension
      A concise syntax for creating sets:
      ``{expression for item in iterable if condition}``. Automatically
      removes duplicates.

   Shallow Copy
      A copy operation that creates a new object but copies references
      to nested objects (not the nested objects themselves). Performed
      using ``copy.copy()``, ``list.copy()``, or slicing ``[:]``.
      Contrast with :term:`Deep Copy`.

   Slicing
      Extracting a subsequence from a sequence using the syntax
      ``[start:stop:step]``. ``start`` is inclusive, ``stop`` is
      exclusive. Works on lists, tuples, strings, and ranges.

   Symmetric Difference
      A set operation returning elements in either set but not in both.
      Performed with ``^`` operator or ``.symmetric_difference()``
      method. ``{1, 2, 3} ^ {2, 3, 4}`` returns ``{1, 4}``.


.. _l3-glossary-t:

T
=

.. glossary::

   Tuple
      An immutable, ordered sequence of objects. Created with
      parentheses ``(1, 2, 3)`` or the ``tuple()`` constructor. Single-
      element tuples require a trailing comma: ``(42,)``. Tuples are
      :term:`hashable <Hashable>` if all their elements are hashable.

   Tuple Packing
      Creating a tuple by listing comma-separated values without
      parentheses: ``point = 3, 4`` creates the tuple ``(3, 4)``.

   Tuple Unpacking
      Assigning tuple elements to individual variables:
      ``x, y = (3, 4)`` assigns ``3`` to ``x`` and ``4`` to ``y``.
      Also works with lists and other iterables.


.. _l3-glossary-u:

U
=

.. glossary::

   Union
      A set operation returning all elements from both sets (duplicates
      removed). Performed with ``|`` operator or ``.union()`` method.
      ``{1, 2, 3} | {2, 3, 4}`` returns ``{1, 2, 3, 4}``.

   Unpacking
      See :term:`Tuple Unpacking`. Extended unpacking uses ``*`` to
      capture multiple values: ``first, *rest = [1, 2, 3, 4]`` assigns
      ``1`` to ``first`` and ``[2, 3, 4]`` to ``rest``.


.. _l3-glossary-v:

V
=

.. glossary::

   View Object
      An object providing a dynamic view of dictionary keys, values, or
      items. Returned by ``dict.keys()``, ``dict.values()``, and
      ``dict.items()``. Views reflect changes to the dictionary without
      creating a copy.


.. _l3-glossary-w:

W
=

.. glossary::

   while Loop
      A control structure that repeats as long as a condition is
      ``True``. Syntax: ``while condition:``. Must include logic to
      eventually make the condition ``False``, or the loop runs forever
      (infinite loop).

   Immutable
      An object whose value cannot be changed after creation. Integers,
      floats, strings, tuples, and frozensets are immutable. Attempting
      to modify an immutable object creates a new object instead.