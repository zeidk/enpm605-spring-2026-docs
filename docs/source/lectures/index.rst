====================================================
Lectures
====================================================

Overview
--------

The lectures in ENPM605 follow a progressive structure, starting with Python fundamentals and building toward real-world robotics applications using ROS 2. Each lecture introduces new concepts through explanation, live demonstrations, and in-class exercises. Lecture materials, including slides and demo scripts, are available on Canvas and GitHub.

.. tip::

   Review the demo scripts after each lecture and re-run them on your own machine. Experimenting with the code is the fastest way to internalize the concepts.


Schedule
--------

.. list-table::
   :widths: 10 45 45
   :header-rows: 1
   :class: compact-table

   * - Lecture
     - Topic
     - Key Concepts
   * - L1
     - Course Introduction
     - Development environment setup, Python execution pipeline, variables, data types, mutability
   * - L2
     - Python Fundamentals, Part I
     - Packages and imports, operators, boolean logic, strings, indexing and slicing, control flow
   * - L3
     - Python Fundamentals, Part II
     - Lists, tuples, dictionaries, sets, loops, list comprehensions, copying
   * - L4
     - Introduction to Functions
     - Function definition, arguments (positional, default, keyword, ``*args``, ``**kwargs``), scopes (LEGB), pass-by-assignment, type hints, recursion
   * - L5
     - Advanced Functions
     - Programming paradigms, first-class functions, lambda expressions, closures, decorators, ``functools.wraps``, ``functools.partial``
   * - L6
     - Object-Oriented Programming, Part I
     - OOP design phase, classes and objects, dunder methods, operator overloading, abstraction, encapsulation, ``@property``
   * - L7
     - Object-Oriented Programming, Part II
     - Class and static methods, association, aggregation, composition, inheritance, ``super()``, polymorphism, duck typing, abstract base classes, ``@dataclass``, ``__slots__``, ``typing.Protocol``
   * - L8
     - Introduction to ROS 2
     - Distributed architecture, DDS middleware, QoS policies, pub/sub model (nodes, topics, messages), workspace setup, ``colcon`` builds, Python package creation, minimal and OOP-based nodes, spinning, timers, publishers, subscribers, communication timing scenarios
   * - L9
     - Launch Files, Parameters, & Executors
     - Python launch files, advanced launch features (includes, conditionals, grouping, arguments), parameter lifecycle (declaration, retrieval, setting, runtime callbacks), single-threaded and multi-threaded executors, callback groups (mutually exclusive and reentrant), Python GIL

Contents
--------

.. toctree::
   :maxdepth: 3
   :titlesonly:

   lecture1/l1_index
   lecture2/l2_index
   lecture3/l3_index
   lecture4/l4_index
   lecture5/l5_index
   lecture6/l6_index
   lecture7/l7_index
   lecture8/l8_index
   lecture9/l9_index
