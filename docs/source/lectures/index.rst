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
   * - L10
     - Parameters, Custom Interfaces, Services & Actions
     - Parameter declaration, descriptors, callbacks, YAML parameter files, custom ``.msg``/``.srv``/``.action`` definitions, CMake interface packages, service servers and clients (sync vs async), action servers and clients, feedback, cancellation, communication pattern selection
   * - L11
     - Coordinate Frames, TF2, and Mobile Robot Control
     - Pose representation (position, Euler angles, quaternions, gimbal lock), coordinate frames (REP 105), TF2 transform tree, static and dynamic broadcasters, transform listeners, ``Buffer`` and ``lookup_transform``, Gazebo Harmonic simulation, RViz2 visualization, differential drive kinematics, ``cmd_vel``/``TwistStamped``, odometry, proportional controllers, KDL frame composition, ArUco marker detection with PnP
   * - L12
     - Nav2 and Lifecycle Nodes
     - Nav2 navigation stack, lifecycle (managed) nodes, state transitions, Nav2 goal dispatch
   * - L13
     - Behavior Trees and Project Integration
     - Behavior tree fundamentals, ``py_trees`` library, Blackboard, ``py_trees_ros``, lifecycle management from BTs, Nav2 integration, full-system coordination

Contents
--------

.. toctree::
   :hidden:
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
   lecture10/l10_index
   lecture11/l11_index
