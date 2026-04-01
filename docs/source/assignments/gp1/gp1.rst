====================================================
GP 1: ROS 2 Pub/Sub System
====================================================


Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - April 13, 2026, 11:59 PM EST
   * - **Total Points**
     - 50 points
   * - **Submission**
     - Canvas (ZIP file: ``group<N>_gp1.zip`` containing the ROS 2 package)
   * - **Collaboration**
     - Groups of 2. AI tools are permitted with proper documentation.
   * - **Late Policy**
     - 10% deduction per calendar day, up to 3 days. Zero after 3 days.
   * - **Peer Review**
     - Final grade: 60% assignment grade + 40% peer review score.


.. dropdown:: Description
   :open:

   This is a **group project** (2 students per group). Each group selects
   **one** of three scenarios listed below. All three scenarios exercise
   the same core ROS 2 concepts from Lectures 8 and 9 but differ in the
   application domain and specific requirements.

   Each scenario requires you to build a multi-node ROS 2 system that
   demonstrates:

   - OOP-based node design with ``rclpy``
   - Publishers and subscribers with typed messages
   - Quality of Service (QoS) configuration and compatibility
   - Launch files with advanced features (arguments, conditionals, grouping)
   - Executors and callback groups (mutually exclusive and reentrant)

   You will create a single ROS 2 Python package inside
   ``~/enpm605_ws/src/`` containing all nodes, launch files, and a
   ``README.md`` explaining your design decisions.


.. .. dropdown:: AI and Academic Integrity Policy
..    :open:

..    .. note::

..       **AI tools are permitted** for this group project, subject to the
..       following rules:

..       - You **must** include a file named ``AI_USAGE.md`` in your package
..         root documenting every AI interaction: the tool used, the prompt
..         given, and how the output was modified.
..       - AI-generated code that is submitted without documentation will be
..         treated as an academic integrity violation.
..       - You are responsible for understanding and being able to explain
..         every line of code you submit.


.. dropdown:: Learning Objectives
   :open:

   .. grid:: 1 2 2 2
       :gutter: 2

       .. grid-item-card:: OOP Node Design
           :class-card: sd-border-info

           Write class-based ROS 2 nodes that inherit from ``Node``,
           encapsulate state, and use timers and callbacks.

       .. grid-item-card:: Pub/Sub Communication
           :class-card: sd-border-info

           Implement publishers and subscribers with appropriate message
           types. Demonstrate one-to-many, many-to-one, and bidirectional
           patterns.

       .. grid-item-card:: Quality of Service
           :class-card: sd-border-info

           Configure explicit QoS profiles. Demonstrate compatible and
           incompatible QoS pairings and diagnose mismatches with CLI
           tools.

       .. grid-item-card:: Launch Files
           :class-card: sd-border-info

           Write Python launch files with arguments, conditionals, and
           node grouping. Start the full system with a single command.

       .. grid-item-card:: Executors and Callback Groups
           :class-card: sd-border-info

           Use ``MultiThreadedExecutor`` with ``MutuallyExclusiveCallbackGroup``
           and ``ReentrantCallbackGroup`` to manage concurrent callbacks.

       .. grid-item-card:: System Integration
           :class-card: sd-border-info

           Wire multiple independent nodes into a coherent system and
           verify end-to-end communication with ROS 2 introspection tools.


.. dropdown:: Suggested Timeline
   :open:

   .. list-table::
      :widths: 18 12 70
      :header-rows: 1
      :class: compact-table

      * - Period
        - Duration
        - Tasks
      * - **Week 1**
        - Days 1--3
        - Read the scenario carefully. Agree on a node graph (which nodes,
          which topics, which message types). Create the package and
          skeleton files. Divide work between teammates.
      * - **Week 1**
        - Days 4--7
        - Implement and test individual publisher and subscriber nodes.
          Verify with ``ros2 topic echo``, ``ros2 topic hz``, and
          ``rqt_graph``.
      * - **Week 2**
        - Days 8--10
        - Add QoS profiles and demonstrate compatible/incompatible
          pairings. Implement the aggregator or fusion node with
          callback groups and executor.
      * - **Week 2**
        - Days 11--12
        - Write launch files (basic + advanced with arguments and
          conditionals). Test the full system end to end.
      * - **Week 2**
        - Days 13--14
        - Write ``README.md``, ``AI_USAGE.md``, and code quality pass
          (docstrings, type hints, comments). Package and submit.

   .. tip::

      Divide work by node, not by concept. Each teammate implements
      complete nodes (publisher + subscriber + QoS + entry point) rather
      than one person doing "all publishers" and the other "all
      subscribers".


Common Requirements
===================

The following requirements apply to **all three scenarios**. Scenario-
specific requirements are listed in each scenario page.


.. dropdown:: Package Structure
   :open:

   Your submission must be a single ROS 2 Python package. Replace
   ``<scenario>`` with your scenario name (e.g., ``sensor_monitor``,
   ``fleet_dispatch``, ``sensor_fusion``).

   .. code-block:: text

      group<N>_gp1/
      |-- group<N>_gp1/          # Python module (node files)
      |   |-- __init__.py
      |   |-- <node1>.py
      |   |-- <node2>.py
      |   |-- ...
      |-- scripts/               # Entry point scripts
      |   |-- __init__.py
      |   |-- main_<node1>.py
      |   |-- main_<node2>.py
      |   |-- ...
      |-- launch/                # Launch files
      |   |-- system.launch.py
      |   |-- ...
      |-- resource/
      |-- test/
      |-- package.xml
      |-- setup.py
      |-- setup.cfg
      |-- README.md
      |-- AI_USAGE.md

   Each node class must live in its own Python file (e.g.,
   ``aggregator.py``, ``watchdog.py``). Do not place multiple node
   classes in the same file. Each node must have a corresponding entry
   point script in ``scripts/``.

   **Package metadata:** Both ``package.xml`` and ``setup.py`` must be
   updated with a meaningful description, a license (e.g.,
   ``Apache-2.0``), and both group members listed as maintainers with
   their email addresses.


.. dropdown:: QoS Requirements
   :open:

   Every scenario must demonstrate the following QoS concepts:

   1. **At least one topic** with an explicit ``QoSProfile`` using
      ``RELIABLE`` reliability.
   2. **At least one topic** with an explicit ``QoSProfile`` using
      ``BEST_EFFORT`` reliability.
   3. **One intentional QoS mismatch** between a publisher and subscriber
      that results in no data delivery. Include a comment in the code
      explaining why the mismatch occurs.
   4. **One topic** using ``TRANSIENT_LOCAL`` durability so that a
      late-joining subscriber receives the last published message.


.. dropdown:: Launch File Requirements
   :open:

   1. A **main launch file** (``system.launch.py``) that starts all nodes
      in the system.
   2. At least one **launch argument** (e.g., to enable/disable a debug
      node or set a publish rate).
   3. At least one **conditional node** using ``IfCondition``.
   4. At least one **node group** using ``GroupAction``.
   5. All nodes must use ``output="screen"`` and ``emulate_tty=True``.


.. dropdown:: Executor and Callback Group Requirements
   :open:

   1. At least one node must use a ``MultiThreadedExecutor``.
   2. At least one node must use a ``MutuallyExclusiveCallbackGroup`` to
      protect shared state accessed by multiple callbacks.
   3. At least one node must use a ``ReentrantCallbackGroup`` for
      independent callbacks that can safely overlap.
   4. Include comments in the code explaining **why** each callback group
      type was chosen.


.. dropdown:: README.md Requirements
   :open:

   Your ``README.md`` must include:

   1. **Group members**: names and UIDs.
   2. **Contributions**: a brief description of each team member's
      contributions (e.g., which nodes each person implemented, who wrote
      the launch files, who handled QoS configuration).
   3. **Scenario chosen**: which scenario and a one-paragraph summary.
   4. **Node graph**: a text or diagram showing all nodes, topics, message
      types, and QoS profiles. You may use a tool like
      `Mermaid <https://mermaid.js.org/>`_ or a screenshot of
      ``rqt_graph``.
   5. **Design decisions**: explain your choice of QoS profiles, callback
      groups, and executor types.
   6. **Build and run instructions**: exact commands to build, source, and
      launch the system.
   7. **Known issues**: any limitations or incomplete features.


.. dropdown:: Code Quality Requirements
   :open:

   .. warning::

      The following are mandatory and will result in point deductions if
      missing.

   - **Docstrings:** Every class and every method must have a Google-style
     docstring.
   - **Type hints:** All method parameters and return types must have type
     annotations.
   - **Inline comments:** Include comments that explain non-obvious logic,
     QoS choices, and callback group decisions.
   - **Naming conventions:** ``snake_case`` for topics, methods, and
     variables. ``CamelCase`` for class names.
   - **Logging:** Use the ROS 2 logger exclusively -- never ``print()``.
     Use the appropriate severity level: ``self.get_logger().info()`` for
     normal operation, ``self.get_logger().warn()`` for warnings (e.g.,
     sensor timeout, obstacle detected), and ``self.get_logger().error()``
     for errors.
   - **Linting:** Ensure Ruff is enabled and no errors appear.


----


.. dropdown:: Pre-Submission Checklist
   :open:

   **Functionality**

   - |box| The system builds: ``colcon build --packages-select group<N>_gp1``
   - |box| The system launches: ``ros2 launch group<N>_gp1 system.launch.py``
   - |box| All topics are active: ``ros2 topic list -t``
   - |box| QoS mismatch is demonstrated and documented.
   - |box| Late-joining subscriber receives cached data.
   - |box| Launch arguments work: ``--show-args`` and override.
   - |box| ``rqt_graph`` shows the expected node/topic graph.

   **Documentation**

   - |box| ``README.md`` includes all required sections.
   - |box| ``AI_USAGE.md`` documents all AI tool usage (or states "No AI
     tools were used").

   **Code Quality**

   - |box| Type hints on all methods.
   - |box| Google-style docstrings on all classes and methods.
   - |box| Callback group choices explained in comments.
   - |box| No linting errors (Ruff).

   **Packaging**

   - |box| Removed ``__pycache__/``, ``*.pyc``, ``.ruff_cache/``.
   - |box| ZIP file is named ``group<N>_gp1.zip``.
   - |box| ZIP contains only the package folder.

   .. |box| unicode:: U+2610


.. dropdown:: Submission
   :open:

   - Submit a ZIP file named ``group<N>_gp1.zip`` on Canvas (e.g.,
     ``group3_gp1.zip``).
   - The ZIP must contain the ROS 2 package folder with all source files,
     launch files, ``README.md``, and ``AI_USAGE.md``.
   - The ZIP must not contain ``build/``, ``install/``, ``log/``,
     ``__pycache__/``, or ``.pyc`` files.
   - Both group members must submit the same ZIP file on Canvas.


----


Scenarios
=========

Choose **one** of the three scenarios below. Each scenario page includes its own detailed
grading rubric.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   gp1_scenario1
   gp1_scenario2
   gp1_scenario3
