References
==========


.. dropdown:: 🏛️ Lecture 2
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 — L2: Python Fundamentals — Part I**

        Covers packages and modules, indentation, operators (arithmetic, relational, logical, membership, identity), Boolean type and truthiness, numeric types and interning, strings (formatting, methods, indexing, slicing), and control flow.


.. dropdown:: 🐍 Python Language References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📦 Modules and Packages
            :link: https://docs.python.org/3/tutorial/modules.html
            :class-card: sd-border-secondary

            **Tutorial — Section 6**

            Modules, packages, ``__init__.py``, and ``sys.path``.

            +++

            - Import statements
            - Package structure
            - Module search path

        .. grid-item-card:: 📘 Expressions and Operators
            :link: https://docs.python.org/3/reference/expressions.html
            :class-card: sd-border-secondary

            **Language Reference — Expressions**

            Complete reference for Python expressions and operator precedence.

            +++

            - Arithmetic operators
            - Comparison chaining
            - Boolean operations

        .. grid-item-card:: 🔤 String Methods
            :link: https://docs.python.org/3/library/stdtypes.html#string-methods
            :class-card: sd-border-secondary

            **Standard Library — str**

            Complete reference for all built-in string methods.

            +++

            - ``.split()``, ``.join()``, ``.strip()``
            - ``.find()``, ``.replace()``, ``.count()``
            - ``.upper()``, ``.lower()``, ``.startswith()``

        .. grid-item-card:: 📐 Format Specification
            :link: https://docs.python.org/3/library/string.html#formatspec
            :class-card: sd-border-secondary

            **Format Specification Mini-Language**

            Detailed rules for f-string format specifiers.

            +++

            - Alignment (``<``, ``>``, ``^``)
            - Precision (``.2f``)
            - Fill and width

        .. grid-item-card:: 🔢 Numeric Types
            :link: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex
            :class-card: sd-border-secondary

            **Standard Library — Numeric Types**

            Reference for ``int``, ``float``, and ``complex`` operations.

            +++

            - Unlimited precision integers
            - IEEE 754 floating-point
            - ``math.isclose()``

        .. grid-item-card:: 🔀 Control Flow
            :link: https://docs.python.org/3/tutorial/controlflow.html
            :class-card: sd-border-secondary

            **Tutorial — Section 4**

            ``if`` statements, ``for`` and ``while`` loops, and more.

            +++

            - ``if``/``elif``/``else``
            - Ternary expressions
            - ``match``/``case`` (3.10+)


.. dropdown:: 📏 Style and Best Practices
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📏 PEP 8 — Style Guide
            :link: https://peps.python.org/pep-0008/
            :class-card: sd-border-secondary

            **Coding Conventions**

            Indentation (4 spaces), naming conventions, import ordering, and line length.

            +++

            - Indentation rules
            - Import grouping
            - Whitespace conventions

        .. grid-item-card:: 📝 PEP 498 — f-strings
            :link: https://peps.python.org/pep-0498/
            :class-card: sd-border-secondary

            **Literal String Interpolation**

            The PEP that introduced formatted string literals in Python 3.6.

            +++

            - Rationale and syntax
            - Expression evaluation
            - Format specifiers

        .. grid-item-card:: 📝 PEP 526 — Variable Annotations
            :link: https://peps.python.org/pep-0526/
            :class-card: sd-border-secondary

            **Syntax for Variable Annotations**

            How to annotate variable types: ``name: str = "Alice"``.

            +++

            - Variable annotations
            - Class variable annotations
            - ``__annotations__`` dict


.. dropdown:: 📚 Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📘 Python Official Tutorial
            :link: https://docs.python.org/3/tutorial/
            :class-card: sd-border-secondary

            **Getting Started**

            Sections 3 (informal introduction), 4 (control flow), and 5 (data structures).

            +++

            - Variables and types
            - Control flow
            - Data structures

        .. grid-item-card:: Mark Lutz
            :class-card: sd-border-secondary

            **Learning Python (5th Edition)**

            Chapters 4–7 cover core types: numbers, strings, lists, and dictionaries.

        .. grid-item-card:: Luciano Ramalho
            :class-card: sd-border-secondary

            **Fluent Python (2nd Edition)**

            Chapters 2 (sequences) and 4 (Unicode and bytes) provide advanced string and sequence coverage.

        .. grid-item-card:: Brett Slatkin
            :class-card: sd-border-secondary

            **Effective Python (2nd Edition)**

            Items 1–10 cover Pythonic thinking including f-strings, slicing, and truthiness patterns.