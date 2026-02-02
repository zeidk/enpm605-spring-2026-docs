L8 - OOP (Basics)
===============================================

This site accompanies *ENPM702 - Lecture 8: Object-Oriented Programming (Basics)*. It organizes the lecture into concise, browsable pages with examples, short exercises, and instructor notes.


.. note::
   `Lecture 8 slides (v1.0) <https://drive.google.com/file/d/172TXLUdaJOby8-zINli2lTawz-E5R2L4/view?usp=drive_link>`_.


Learning Outcomes
-----------------

By the end of this session, you will be able to:

- Understand the core principles of Object-Oriented Programming (encapsulation, abstraction, inheritance, polymorphism)
- Define and implement classes with proper encapsulation using access specifiers
- Distinguish between classes and objects, and understand instantiation
- Create constructors (default and parameterized) with member initializer lists
- Implement accessors (getters) and mutators (setters) with proper const-correctness
- Apply modern C++ features including ``std::string_view``, ``std::optional``, ``[[nodiscard]]``, and ``noexcept``
- Understand the software design process: requirements analysis and UML modeling
- Implement classes within proper namespace organization (``transportation``)
- Write well-documented code using Doxygen conventions

.. tip::
   Compile examples with ``-std=c++17 -Wall -Wextra -pedantic-errors -Werror`` for strong diagnostics.

Course Context
--------------

This lecture bridges the gap between procedural and object-oriented programming in C++. We introduce OOP concepts through a comprehensive vehicle control system example, following industry-standard practices from requirements analysis through implementation. The lecture emphasizes modern C++ idioms and prepares students for advanced OOP topics in Lecture 9.

**Prerequisites:**

- Strong understanding of C++ fundamentals (variables, functions, references, pointers)
- Familiarity with STL containers (``std::vector``, ``std::string``)
- Basic understanding of memory management concepts

**Connection to Future Topics:**

- Lecture 9 will cover inheritance, polymorphism, virtual functions, and advanced OOP patterns
- Project work will require implementing class hierarchies following the design patterns introduced here

Contents
--------

The following sections explore each topic in Lecture 8:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   lecture
   exercises
   references

Overview of Topics
------------------

**Design Phase**

- Requirements analysis: defining what the system must do
- Modeling phase: UML diagrams (class, sequence, state machine, system architecture)
- Introduction to PlantUML and modeling tools

**Core OOP Principles**

- Encapsulation: data hiding and controlled access
- Abstraction: simplifying complexity
- Inheritance: code reuse through hierarchies (covered in Lecture 9)
- Polymorphism: flexible and extensible interfaces (covered in Lecture 9)

**Classes and Objects**

- Class definition: blueprints for objects
- Object instantiation: creating instances from classes
- Member variables (attributes) and member functions (methods)
- Stack vs. heap allocation with smart pointers

**Encapsulation**

- Access specifiers: ``public``, ``private``, ``protected``
- Accessors (getters): ``const``-correct, ``[[nodiscard]]``, ``noexcept``
- Mutators (setters): validation and invariant enforcement

**Constructors**

- Default constructors: compiler-generated vs. user-defined
- Parameterized constructors: initialization with arguments
- Member initializer lists: efficient direct initialization
- Understanding construction order and avoiding two-step initialization

**Modern C++ Features**

- ``std::string_view``: lightweight string references for read-only access
- ``std::optional``: type-safe optional values
- ``[[nodiscard]]``: preventing accidental value discards
- ``noexcept``: exception specifications for optimization

**Implementation Example**

- Complete ``Vehicle`` class implementation within ``transportation`` namespace
- Project structure: separation of headers (``include/``) and source files (``src/``)
- CMake build configuration
- Doxygen documentation standards


Common Pitfalls
---------------

.. warning::

   **Critical mistakes that result in assignment failure:**
   
   - Making class attributes ``public`` (violates encapsulation)
   - Forgetting ``const`` on accessor methods
   - Returning non-const references from accessors
   - Not using member initializer lists in constructors
   - Forgetting the semicolon after class definition

**Performance issues:**

- Passing ``std::string`` by value unnecessarily
- Using ``std::string_view`` for constructor parameters when storing as members
- Assignment in constructor body instead of member initializer lists

**Design issues:**

- Not validating input in mutators
- Mixing concerns across classes
- Tight coupling between unrelated classes

Next Steps
----------

- **Lecture 9** will cover inheritance hierarchies, virtual functions, polymorphism, abstract base classes, and the ``virtual`` keyword
- Begin working on your project's class design and UML diagrams
- Practice implementing classes with proper encapsulation and modern C++ features
- Review the ``transportation`` namespace implementation for design patterns

.. tip::

   Before the next lecture, ensure you can:
   
   - Implement a class with multiple constructors
   - Write const-correct accessors and validated mutators
   - Use member initializer lists effectively
   - Apply ``std::optional`` and ``std::string_view`` appropriately
   - Organize code within namespaces