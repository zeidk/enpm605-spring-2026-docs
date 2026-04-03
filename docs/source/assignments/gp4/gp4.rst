====================================================
GP 4: Autonomous Robot System (Final Project)
====================================================


Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - May 20, 2026, 11:59 PM EST
   * - **Total Points**
     - 100 points
   * - **Submission**
     - Canvas (ZIP file: ``group<N>_gp4.zip`` containing the ROS 2 package)
   * - **Collaboration**
     - Groups of 2.
   * - **Late Policy**
     - 10% deduction per calendar day, up to 3 days. Zero after 3 days.
   * - **Peer Review**
     - Final grade: 60% assignment grade + 40% peer review score.


.. dropdown:: Description
   :open:

   This is the **capstone group project** (2 students per group) for
   ENPM605. Each group selects **one** of three scenarios listed below.
   All three scenarios require you to build a **fully integrated
   autonomous robot system** that uses a **behavior tree** to coordinate
   **lifecycle nodes** and **Nav2 navigation** within a **Gazebo
   simulation**.

   This project brings together the most advanced topics covered in the
   course -- behavior trees (Lecture 12), lifecycle nodes (Lecture 13),
   and Nav2 navigation -- into a single cohesive system. You will design
   a behavior tree that acts as the top-level system coordinator,
   managing the transitions of lifecycle nodes, sending navigation goals
   through Nav2, and making decisions based on sensor data.

   **This project builds directly on GP3.** You are expected to reuse and
   extend the lifecycle node and Nav2 infrastructure you developed
   previously. The key addition is the behavior tree layer that
   orchestrates the entire system autonomously, replacing any manual
   coordination or scripted sequences from GP3.

   You will create a single ROS 2 Python package inside
   ``~/enpm605_ws/src/`` containing all nodes, behavior tree definitions,
   launch files, configuration files, and a ``README.md`` explaining your
   design decisions.


.. dropdown:: Learning Objectives
   :open:

   .. grid:: 1 2 2 2
       :gutter: 2

       .. grid-item-card:: Behavior Tree Design
           :class-card: sd-border-info

           Design and implement a behavior tree using ``py_trees`` /
           ``py_trees_ros`` that coordinates complex robot behaviors
           through sequences, selectors, decorators, and conditions.

       .. grid-item-card:: Lifecycle Node Management via BT
           :class-card: sd-border-info

           Use behavior tree nodes to programmatically manage lifecycle
           node transitions (configure, activate, deactivate, cleanup)
           based on system state and mission requirements.

       .. grid-item-card:: Nav2 Integration
           :class-card: sd-border-info

           Send navigation goals to Nav2 from behavior tree action
           nodes, monitor navigation progress, and react to success,
           failure, or preemption of navigation tasks.

       .. grid-item-card:: Sensor-Driven Decision Making
           :class-card: sd-border-info

           Implement behavior tree condition nodes that read sensor
           data (lidar, camera, or other sensors) and dynamically
           alter the robot's behavior based on environmental feedback.

       .. grid-item-card:: System Architecture
           :class-card: sd-border-info

           Architect a multi-node ROS 2 system where the behavior tree
           serves as the central coordinator, lifecycle nodes provide
           managed subsystems, and Nav2 handles autonomous navigation.

       .. grid-item-card:: End-to-End Integration
           :class-card: sd-border-info

           Integrate behavior trees, lifecycle nodes, Nav2, sensor
           processing, and Gazebo simulation into a complete autonomous
           robot system that runs without manual intervention.


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
        - Days 1--4
        - Read the scenario carefully. Design your behavior tree on
          paper or using a diagramming tool. Identify all lifecycle
          nodes, Nav2 goals, and sensor conditions. Define the
          blackboard variables. Set up the package structure and reuse
          GP3 components where applicable.
      * - **Week 1**
        - Days 5--7
        - Implement the lifecycle nodes (reuse/adapt from GP3).
          Implement the basic behavior tree skeleton with ``py_trees``
          and verify it ticks correctly. Test lifecycle transitions
          triggered from the BT.
      * - **Week 2**
        - Days 8--11
        - Implement Nav2 action nodes in the BT. Integrate sensor
          condition nodes. Connect the blackboard for shared state.
          Test navigation goals and sensor-driven branching in Gazebo.
      * - **Week 2**
        - Days 12--14
        - Implement the complete mission sequence end to end. Test
          failure recovery and edge cases. Debug timing and
          concurrency issues.
      * - **Week 3**
        - Days 15--18
        - Record the demo video (2--3 minutes). Write the
          ``README.md`` and complete all documentation. Code quality
          pass (docstrings, type hints, comments). Package and submit.

   .. tip::

      Start with the behavior tree design before writing any code.
      Sketch the tree on paper, identifying every sequence, selector,
      condition, and action node. A clear BT design makes
      implementation significantly smoother.


Common Requirements
===================

The following requirements apply to **all three scenarios**. Scenario-
specific requirements are listed in each scenario page.


.. dropdown:: Package Structure
   :open:

   Your submission must be a single ROS 2 Python package.

   .. code-block:: text

      group<N>_gp4/
      |-- group<N>_gp4/              # Python module
      |   |-- __init__.py
      |   |-- bt_nodes/              # Custom behavior tree nodes
      |   |   |-- __init__.py
      |   |   |-- actions.py         # BT action nodes
      |   |   |-- conditions.py      # BT condition nodes
      |   |   |-- decorators.py      # Custom BT decorators (if any)
      |   |-- lifecycle_nodes/       # Lifecycle managed nodes
      |   |   |-- __init__.py
      |   |   |-- <node1>.py
      |   |   |-- <node2>.py
      |   |-- <other_nodes>.py       # Additional ROS 2 nodes
      |-- scripts/                   # Entry point scripts
      |   |-- __init__.py
      |   |-- main_bt.py             # BT runner entry point
      |   |-- main_<node>.py
      |   |-- ...
      |-- launch/                    # Launch files
      |   |-- system.launch.py       # Main launch file
      |   |-- simulation.launch.py   # Gazebo launch (if separate)
      |-- config/                    # Configuration files
      |   |-- nav2_params.yaml       # Nav2 parameters
      |   |-- bt_config.yaml         # BT parameters (if any)
      |-- worlds/                    # Gazebo world files
      |   |-- <scenario>.sdf
      |-- resource/
      |-- test/
      |-- package.xml
      |-- setup.py
      |-- setup.cfg
      |-- README.md

   Each lifecycle node class and each behavior tree node class must live
   in its own file or logically grouped file (e.g., all BT action nodes
   in ``actions.py``, all BT condition nodes in ``conditions.py``). Do
   not place unrelated node classes in the same file.

   **Package metadata:** Both ``package.xml`` and ``setup.py`` must be
   updated with a meaningful description, a license (e.g.,
   ``Apache-2.0``), and both group members listed as maintainers with
   their email addresses.


.. dropdown:: Behavior Tree Requirements
   :open:

   The behavior tree is the **central coordinator** of your system. It
   must satisfy the following requirements:

   1. **Framework:** Use ``py_trees`` and ``py_trees_ros`` as the
      behavior tree framework. The BT must be constructed
      programmatically in Python (not loaded from an XML file).

   2. **Tree structure:** The BT must include at minimum:

      - At least **two Sequence** composite nodes
      - At least **one Selector** (Fallback) composite node
      - At least **two Condition** nodes that check sensor data or
        system state
      - At least **three Action** nodes that perform work (e.g.,
        navigate, manage lifecycle transitions, process data)
      - At least **one Decorator** node (e.g., ``Inverter``,
        ``Retry``, ``Timeout``, ``SuccessIsRunning``)

   3. **Blackboard:** Use the ``py_trees`` blackboard to share state
      between BT nodes. At minimum, the blackboard must store:

      - Current mission state (e.g., current waypoint index, delivery
        queue)
      - Sensor readings relevant to decision making
      - Navigation status (e.g., goal reached, navigation failed)
      - Lifecycle node states

   4. **Reactivity:** The BT must demonstrate reactive behavior -- it
      must change its execution path based on sensor input or
      environmental conditions during runtime, not just follow a
      fixed script.

   5. **Ticking:** The BT must be ticked at a regular rate (recommended
      10 Hz) using a ``py_trees_ros`` tree manager or a ROS 2 timer.


.. dropdown:: Lifecycle Node Requirements
   :open:

   Your system must include lifecycle (managed) nodes that are
   coordinated by the behavior tree:

   1. **At least two custom lifecycle nodes** that inherit from
      ``rclpy.lifecycle.Node`` (or the equivalent managed node base
      class).

   2. **Lifecycle transitions managed by the BT:** The behavior tree
      must programmatically trigger lifecycle transitions using service
      calls (``/node_name/change_state``). At minimum, the BT must
      demonstrate:

      - ``configure`` transition
      - ``activate`` transition
      - ``deactivate`` transition

   3. **State-dependent behavior:** Lifecycle nodes must perform their
      core work only in the ``active`` state. For example, a sensor
      processing node should only publish processed data when active,
      and a patrol node should only send navigation goals when active.

   4. **Transition callbacks:** Each lifecycle node must implement at
      least ``on_configure()``, ``on_activate()``, ``on_deactivate()``,
      and ``on_cleanup()`` with meaningful behavior (e.g., creating
      publishers/subscribers in ``on_configure()``, starting timers in
      ``on_activate()``).


.. dropdown:: Nav2 Requirements
   :open:

   Your system must use the Nav2 stack for autonomous navigation:

   1. **Navigation goals:** The behavior tree must send at least
      **three distinct navigation goals** (waypoints) to Nav2 using the
      ``NavigateToPose`` action interface.

   2. **Goal monitoring:** BT action nodes that send Nav2 goals must
      monitor the action result and react appropriately:

      - On **success**: proceed to the next task in the BT
      - On **failure**: trigger a recovery behavior or alternative
        branch in the BT
      - On **preemption/cancel**: handle gracefully

   3. **Dynamic goal selection:** At least one navigation goal must be
      determined at runtime based on sensor data or blackboard state
      (i.e., not all goals can be hardcoded).

   4. **Map:** Provide a map of your simulation environment (either
      pre-built or generated) that Nav2 can use for path planning.


.. dropdown:: Simulation Requirements
   :open:

   1. **Gazebo Harmonic:** The simulation must run in Gazebo Harmonic
      (Gazebo Sim, the version compatible with ROS 2 Jazzy).

   2. **World file:** Provide a Gazebo world file (``.sdf``) that
      includes the environment for your scenario. The world must contain
      at least:

      - Walls or obstacles that require path planning (not an empty
        world)
      - Objects relevant to your scenario (e.g., colored markers for
        the security patrol, delivery stations for the hospital robot,
        data collection points for the explorer)

   3. **Robot model:** Use TurtleBot3 (Waffle or Burger) or TurtleBot4
      as your robot platform. The robot must have a lidar sensor and
      optionally a camera.

   4. **Sensor data:** The robot must use at least one sensor (lidar or
      camera) for decision making within the behavior tree. Raw sensor
      data must be processed by a ROS 2 node and made available on the
      blackboard.


.. dropdown:: Launch File Requirements
   :open:

   1. A **main launch file** (``system.launch.py``) that starts the
      complete system including:

      - Gazebo simulation with the world file
      - Robot spawning and state publisher
      - Nav2 stack (with parameters from ``config/nav2_params.yaml``)
      - All lifecycle nodes (in their initial ``unconfigured`` state)
      - The behavior tree runner node
      - Any additional sensor processing nodes

   2. At least one **launch argument** (e.g., to select the world file,
      enable/disable visualization, or set the BT tick rate).

   3. At least one **conditional node** using ``IfCondition`` (e.g., to
      optionally start RViz for visualization).

   4. All nodes must use ``output="screen"`` and ``emulate_tty=True``.


.. dropdown:: README.md Requirements
   :open:

   Your ``README.md`` must include:

   1. **Group members**: names and UIDs.
   2. **Contributions**: a brief description of each team member's
      contributions (e.g., who designed the BT, who implemented the
      lifecycle nodes, who set up the simulation).
   3. **Scenario chosen**: which scenario and a one-paragraph summary.
   4. **System architecture**: a diagram or detailed description showing:

      - The behavior tree structure (include a tree diagram)
      - All ROS 2 nodes and their types (lifecycle, regular, BT)
      - Topics, services, and actions used
      - Blackboard variables and their purpose

   5. **Behavior tree design**: explain your BT design decisions --
      why you chose specific composite nodes, how conditions drive
      branching, and how the BT reacts to sensor data.
   6. **Lifecycle node design**: explain what each lifecycle node does
      in each state and why lifecycle management is appropriate for it.
   7. **Build and run instructions**: exact commands to build, source,
      and launch the system. Include any dependencies that must be
      installed.
   8. **Demo video link**: a link to or instructions for the demo video.
   9. **Known issues**: any limitations or incomplete features.


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
     BT design choices, lifecycle transition rationale, and Nav2
     integration details.
   - **Naming conventions:** ``snake_case`` for topics, methods, and
     variables. ``CamelCase`` for class names.
   - **Logging:** Use the ROS 2 logger exclusively -- never ``print()``.
     Use the appropriate severity level: ``self.get_logger().info()`` for
     normal operation, ``self.get_logger().warn()`` for warnings (e.g.,
     navigation failure, sensor timeout), and ``self.get_logger().error()``
     for errors.
   - **Linting:** Ensure Ruff is enabled and no errors appear.


.. dropdown:: Demo/Presentation Requirements
   :open:

   Each group must submit a **recorded demo video** (2--3 minutes)
   demonstrating the system in action:

   1. **Video content must include:**

      - The Gazebo simulation running with the robot and environment
        visible
      - The behavior tree executing (show BT status via logs or a
        ``py_trees`` visualization tool)
      - At least one complete mission cycle (e.g., full patrol loop,
        complete delivery sequence, full exploration run)
      - At least one reactive behavior triggered by sensor data (e.g.,
        the robot detecting an object and changing its plan)
      - Lifecycle node transitions visible in the logs (configure,
        activate, deactivate)
      - Nav2 navigating the robot between waypoints

   2. **Video format:** MP4 or uploaded to a streaming platform (e.g.,
      YouTube unlisted link). If uploading to a platform, include the
      link in ``README.md``.

   3. **Narration or captions:** Briefly narrate or add text captions
      explaining what is happening at each stage of the demo.


----


.. dropdown:: Pre-Submission Checklist
   :open:

   **Functionality**

   - |box| The system builds: ``colcon build --packages-select group<N>_gp4``
   - |box| The system launches: ``ros2 launch group<N>_gp4 system.launch.py``
   - |box| Gazebo simulation starts with the correct world and robot.
   - |box| Nav2 stack initializes and the robot can navigate autonomously.
   - |box| The behavior tree ticks and coordinates the system.
   - |box| Lifecycle nodes transition correctly (configure, activate, deactivate).
   - |box| Sensor data drives at least one decision in the behavior tree.
   - |box| The robot completes at least one full mission cycle.
   - |box| The system handles navigation failures gracefully.

   **Behavior Tree**

   - |box| BT includes at least two Sequences, one Selector, two Conditions, three Actions, and one Decorator.
   - |box| Blackboard stores mission state, sensor data, navigation status, and lifecycle states.
   - |box| BT demonstrates reactive behavior (changes execution based on runtime conditions).

   **Documentation**

   - |box| ``README.md`` includes all required sections.
   - |box| BT diagram included in ``README.md``.
   - |box| Demo video recorded and linked.

   **Code Quality**

   - |box| Type hints on all methods.
   - |box| Google-style docstrings on all classes and methods.
   - |box| BT design choices and lifecycle transitions explained in comments.
   - |box| No linting errors (Ruff).

   **Packaging**

   - |box| Removed ``__pycache__/``, ``*.pyc``, ``.ruff_cache/``, ``build/``, ``install/``, ``log/``.
   - |box| ZIP file is named ``group<N>_gp4.zip``.
   - |box| ZIP contains only the package folder.
   - |box| Demo video included or link provided.

   .. |box| unicode:: U+2610


.. dropdown:: Submission
   :open:

   - Submit a ZIP file named ``group<N>_gp4.zip`` on Canvas (e.g.,
     ``group3_gp4.zip``).
   - The ZIP must contain the ROS 2 package folder with all source files,
     launch files, configuration files, world files, and ``README.md``.
   - The ZIP must not contain ``build/``, ``install/``, ``log/``,
     ``__pycache__/``, or ``.pyc`` files.
   - Both group members must submit the same ZIP file on Canvas.
   - Include the demo video in the ZIP or provide a link in ``README.md``.


----


Scenarios
=========

Choose **one** of the three scenarios below. Each scenario page includes its own detailed
grading rubric.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   gp4_scenario1
   gp4_scenario2
   gp4_scenario3
