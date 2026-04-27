====================================================
Changelog
====================================================

All notable changes to the ENPM605 Spring 2026 course documentation are recorded here.

.. dropdown:: v1.6.0 -- L13 Documentation Released (2026-04-26)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Lecture Notes (l13_lecture.rst)

   - Added "Prerequisites" section: workspace cleanup, ``rosdep``
     install, ``--packages-up-to lecture13_meta`` build, and a
     Gazebo smoke-test launch.
   - Added "Mapping" section: motivation for maps (planning,
     localization, semantics, multi-session), comparison of metric /
     topological / semantic representations with light/dark figure
     placeholders.
   - Added "Occupancy Grid Maps" section: grid parameters (resolution,
     width, height, origin), the three cell states with a values
     table, and light/dark figure placeholders. Bayesian / log-odds
     LiDAR update with worked example.
   - Added "The map Frame" section: full REP 105 chain table,
     publisher / drift / jump semantics, light/dark frame-chain
     figure placeholders, and a side-by-side ``map`` vs. ``odom``
     comparison table.
   - Added "SLAM" section: ``slam_toolbox`` overview, scan matching
     (with figure placeholders), pose graph (with figure
     placeholders), loop closure (with figure placeholders), and a
     "How the Three Pieces Connect" subsection covering covariance
     and edge strength.
   - Added "Launching slam_toolbox" subsection: key parameter table
     (resolution, max_laser_range, minimum_travel_distance / heading,
     use_scan_matching, do_loop_closing), mapping-mode demonstration,
     and a "drive fast vs. slow" experiment with answer.
   - Added "Map Saving and Loading" subsection: ``map_saver_cli``
     usage and the ``.pgm`` / ``.yaml`` format example.
   - Added "Navigation" section: the four navigation questions, end-
     to-end Nav2 demonstration table.
   - Added "Localization" subsection: AMCL overview, why "adaptive,"
     three ways to set the initial pose (RViz2, parameters,
     programmatically), and a SLAM vs. AMCL comparison table.
   - Added "Particle Filters" subsubsection: scoring a particle
     against the map, the predict / update / resample cycle, and
     light/dark figure placeholders for the cycle and for
     initialization vs. converged clouds.
   - Added "Costmaps" subsection: global vs. local costmap table,
     layered architecture (static, obstacle, inflation), and the
     robot footprint with inscribed and circumscribed radii (with
     light/dark figure placeholders).
   - Added "Planning and Control" subsection: global planner table
     (NavFn, Smac Hybrid A*, Theta*), local controller table (DWB,
     Regulated Pure Pursuit), with explanatory bullets on output
     topics and behavior-tree plugin selection.
   - Added "Behavior Trees and Recovery" subsection: Nav2 BT
     orchestration and recovery behaviors (Spin, Wait, Clear costmap,
     Back up).
   - Added "NavigateToPose Action API" subsection: goal / feedback /
     result, sending a goal from RViz2, sending a goal
     programmatically with ``BasicNavigator``. Added key-method
     table for ``BasicNavigator`` and two worked examples (single
     goal, follow waypoints) with demonstration tables.
   - Added "Explore Mode" subsection: simultaneous SLAM + Nav2 with
     ``mode:=explore``.

   .. rubric:: Index (l13_index.rst)

   - Overview, learning objectives, toctree, and next-steps for L13.

   .. rubric:: Exercises (l13_exercises.rst)

   - Exercise 1: build, save, and reload a map -- map with
     ``slam_toolbox``, save with ``map_saver_cli``, and reload for
     AMCL navigation.
   - Exercise 2: inflation radius and path quality -- sweep four
     ``inflation_radius`` values, capture screenshots, and reflect on
     why the planner fails through narrow doorways above a threshold.
   - Exercise 3: sequential goals with ``BasicNavigator`` --
     parameterized three-goal sequence using ``goToPose``, with
     feedback printing and result logging.
   - Exercise 4: cancel-on-distance behavior -- extend Exercise 3
     with a "no-progress for 5 s" watchdog that calls
     ``cancelTask()`` and continues with the next goal.

   .. rubric:: Quiz (l13_quiz.rst)

   - 8 multiple choice questions covering occupancy-grid encoding,
     REP 105 jump semantics, loop closure, AMCL adaptivity, global
     vs. local costmaps, Smac vs. NavFn, the inflation layer, and
     ``NavigateToPose`` feedback.
   - 5 true/false questions covering AMCL initial pose parameters,
     inscribed vs. circumscribed radius, ``slam_toolbox``
     localization mode, planner-call frequency, and the
     ``BasicNavigator`` waypoint follower.
   - 4 essay questions: SLAM pipeline (scan match / pose graph /
     loop closure), particle-filter cycle, global vs. local
     costmaps, and the action goal / feedback / result triplet.

   .. rubric:: Glossary (glossary.rst)

   - 23 new terms added: AMCL, BasicNavigator, Circumscribed Radius,
     Costmap, DWB Controller, Footprint, Inflation Layer,
     Inscribed Radius, Loop Closure, ``map`` Frame, Map Server,
     ``nav2_simple_commander``, NavFn Planner, ``NavigateToPose``,
     Occupancy Grid Map, Particle Filter, Pose Graph, Regulated
     Pure Pursuit, REP 105, Scan Matching, SLAM, ``slam_toolbox``,
     Smac Planner.
   - Updated ``Behavior Tree`` and ``Nav2`` entries with L13
     cross-references and an expanded scope.

   .. rubric:: References (l13_references.rst)

   - Lecture 13 card summarizing all topics covered.
   - Mapping and SLAM: ``nav_msgs/OccupancyGrid``, REP 105, Nav2 +
     slam_toolbox tutorial, ``slam_toolbox`` repository, Jazzy API.
   - Localization (AMCL): Nav2 AMCL configuration page and
     ``nav2_amcl`` API reference.
   - Nav2 Stack: top-level Nav2 docs, concepts overview, costmap
     configuration, NavFn / Smac planner configuration, DWB / RPP
     controller configuration, behavior trees, BehaviorTree.CPP.
   - NavigateToPose API: Simple Commander API, source code,
     ``nav2_msgs`` action interface.
   - Recommended Reading: Corke's *Robotics, Vision and Control*
     Chapter 14 and Lynch & Park's *Modern Robotics* Chapter 13.

   .. rubric:: Lectures Index (lectures/index.rst)

   - Added ``lecture13/l13_index`` to the toctree.


.. dropdown:: v1.5.1 -- Lecture 12 (2026-04-22)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: GP 2 (gp2_requirements.rst)

   - Moved the ``scripts`` folder in the python package for GP2

.. dropdown:: v1.5 -- GP2 scripts folder (2026-04-21)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: GP 2 (gp2_requirements.rst)

   - Moved the ``scripts`` folder in the python package for GP2


.. dropdown:: v1.4.1 -- GP1 AI Policy Removed (2026-04-01)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: GP 1 (gp1.rst)

   - Removed AI tools permission from the Collaboration field.
   - Removed ``AI_USAGE.md`` from the package structure, suggested timeline,
     pre-submission checklist, and submission requirements.
   - The AI and Academic Integrity Policy dropdown was already commented out
     in a prior update.


.. dropdown:: v1.4.0 -- L9 Documentation Released (2026-03-28)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Lecture Notes (l9_lecture.rst)

   - Added "Prerequisites" section: workspace clone, shell setup,
     and build commands for all three demo packages
     (``launch_files_demo``, ``parameters_demo``, ``executors_demo``).
   - Added "Launch Files" section: why use launch files (six reasons),
     anatomy (imports, ``generate_launch_description``, node
     configuration, naming convention, two equivalent patterns with
     code examples), and demonstration commands.
   - Added "Advanced Features" section: including other launch files
     (``IncludeLaunchDescription``, ``FindPackageShare``,
     ``PathJoinSubstitution``), conditional launching
     (``IfCondition``, ``DeclareLaunchArgument``,
     ``LaunchConfiguration``, ``--show-args``), and node grouping
     (``GroupAction``, conditional group with example).
   - Added "Parameters" section: characteristics (supported types,
     node-local scope warning, CLI reference and quick inspection
     commands), and sensor node parameter tables (camera and LiDAR)
     with light/dark figure placeholders.
   - Added "Declaring Parameters" section: three approaches (basic
     declaration, declaration with ``ParameterDescriptor`` and
     ``IntegerRange``, and ``declare_parameters`` for batch
     declaration) each with code examples.
   - Added "Retrieving Parameters" section: when and why to retrieve,
     retrieval API with typed field accessors.
   - Added "Using Parameters" section: camera_name in logs and
     camera_rate as timer period control, with note on bandwidth
     measurement and performance gap.
   - Added "Setting Parameters" section: six methods (CLI, launch
     file, YAML file, programmatic, ``ros2 param set`` with callback,
     and launch file arguments) each with code examples and
     demonstration commands. Includes full on-set-parameters callback
     implementation and timer frequency update pattern.
   - Added "Executors" section: overview of multi-task robotic
     requirements and concurrency vs. parallelism definition.
   - Added "Single-Threaded Executor" section: key concepts, execution
     timeline with light/dark figure placeholders, phase offset table,
     and ``rclpy.spin()`` vs. explicit executor comparison.
   - Added "Multi-Threaded Executor" section: overview, benefits
     (performance, scalability, responsiveness), challenges (race
     conditions, overhead), concurrency vs. parallelism with hot dog
     stand figures (light/dark), and the Python GIL explanation with
     impact on ROS 2 and conditions for true parallelism.
   - Added "Callback Groups" section: overview with summary figure
     (light/dark), mutually exclusive group (declaration, effect of
     ``num_threads``, execution timeline with light/dark figures, and
     timestamp table), reentrant group (declaration, fast callback
     timeline, slow/blocked callback timeline with light/dark figures,
     multiple concurrent instances warning), and comparison table.

   .. rubric:: Index (l9_index.rst)

   - Overview, learning objectives, toctree, and next steps for L9.

   .. rubric:: Exercises (l9_exercises.rst)

   - Exercise 1: Configurable Publisher -- parameter declaration,
     CLI override, ``Float64`` publisher controlled by ``publish_rate``
     and ``topic_name`` parameters.
   - Exercise 2: Parameter File Node -- YAML config file, sensor node
     with on-set-parameters callback, and a launch file that loads the
     YAML.
   - Exercise 3: Mutex vs Single-Threaded Comparison -- slow callback
     demo comparing ``rclpy.spin()`` against
     ``MultiThreadedExecutor(num_threads=4)`` with a
     ``MutuallyExclusiveCallbackGroup``; observation questions as
     code comments.
   - Exercise 4: Reentrant Pipeline -- two independent 5 Hz callbacks
     sharing a log list, deliberate race condition introduction and fix
     with ``threading.Lock``, written reflection on CPython list
     safety.

   .. rubric:: Quiz (l9_quiz.rst)

   - 10 multiple choice questions covering launch file structure,
     ``FindPackageShare``, parameter type inference, on-set callback
     behavior, parameter retrieval API, executor types, mutex group
     semantics, reentrant group timing, the GIL, and timer frequency
     update patterns.
   - 10 true/false questions covering ``--symlink-install`` and launch
     files, ``ParameterDescriptor`` immutability, multi-node YAML
     files, multi-node executors, GIL release during sleep, reentrant
     safety, ``IfCondition`` behavior, ``ros2 param set`` persistence,
     ``GroupAction`` conditions, and ``num_threads`` with a mutex
     group.
   - 4 essay questions: parameter lifecycle, single vs. multi-threaded
     executor comparison, the Python GIL, and mutually exclusive vs.
     reentrant callback group comparison with concrete robotic
     examples.

   .. rubric:: Glossary (glossary.rst)

   - 12 new terms added: Callback Group, ColCon Symlink Install,
     Conditional Launch, ``DeclareLaunchArgument``,
     ``generate_launch_description``, Global Interpreter Lock (GIL),
     ``GroupAction``, ``IfCondition``, ``LaunchConfiguration``,
     Mutually Exclusive Callback Group, Parameter Descriptor,
     Reentrant Callback Group.

   .. rubric:: References (l9_references.rst)

   - Lecture 9 card summarizing all topics covered.
   - ROS 2 Official Documentation: launch tutorials, parameters
     concept, parameters tutorial, ros2 param how-to, executors
     concept, callback groups how-to.
   - Launch File API: launch package API, launch_ros package API,
     YAML.org specification, launch file formats comparison.
   - Python Threading and the GIL: threading module, Real Python GIL
     article, multiprocessing module.
   - External Tutorials: Articulated Robotics, The Construct.
   - Recommended Reading: Koubaa ROS 2 series, Programming Robots with
     ROS 2, Silberschatz OS Concepts, David Beazley GIL talk.


.. dropdown:: v1.3.0 -- L8 Documentation Released (2026-03-21)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Lecture Notes (l8_lecture.rst)

   - Added "What Is ROS?" section: overview, where ROS is used
     (transportation, manufacturing, specialized domains, emerging
     areas), and ROS 1 vs. ROS 2 comparison table.
   - Added "ROS 2 Architecture" section: process definition, monolithic
     vs. distributed design (with figures), core components (nodes,
     topics, services, actions, when to use each), pick-up-a-part
     task example with figure, DDS overview (application domains, key
     properties, resources), and QoS overview (four core policies,
     supported vendors, runtime inspection commands).
   - Added "Publish/Subscribe Model" section: node/topic/message
     definitions, four pub/sub rules, four communication patterns
     (one-to-many, many-to-one, multi-topic, bidirectional) each with
     a figure, introspection tools reference, and ``ros2 run`` vs.
     ``ros2 launch`` comparison table.
   - Added "ROS 2 Setup" section: workspace layout and setup commands,
     colcon build flags, Python package creation workflow, package
     layout with directory descriptions, ``package.xml`` fields and
     dependency tags, and ``setup.py`` entry points and data files.
   - Added "Writing Nodes" section: interfaces (three kinds, standard
     message packages, ``.msg`` to code pipeline, primitive types vs.
     ``std_msgs``, introspection commands, composite message example),
     minimal procedural node, OOP node with separate class and entry
     point, spinning (thread definition with figure, main thread and
     executor figure, why spinning is required, ``try/except/finally``
     pattern, spinning alternatives), timers and callbacks, publishers
     (create, message instantiation options, publish in timer callback,
     run and inspect), QoS (four policies, default vs. explicit profile,
     predefined profiles, compatibility rules, diagnostics), and
     subscribers (create, named vs. lambda callbacks, complete node).
   - Added "Communication Scenarios" section: three scenarios (no
     subscriber, fast subscriber, slow subscriber) each with a
     detailed timing table, plus a summary comparison table and
     diagnostic commands.

   .. rubric:: Index (l8_index.rst)

   - Overview, learning objectives, toctree, and next steps for L8.

   .. rubric:: Exercises (l8_exercises.rst)

   - Exercise 1: Periodic Logger -- OOP node with timer callback
     and ROS 2 clock.
   - Exercise 2: String Publisher -- publisher with ``std_msgs/String``
     and introspection verification.
   - Exercise 3: String Subscriber -- named callback subscriber,
     end-to-end verification with Exercise 2.
   - Exercise 4: QoS Mismatch Investigation -- BEST_EFFORT publisher
     vs. RELIABLE subscriber, silent failure diagnosis, fix and
     written reflection.

   .. rubric:: Quiz (l8_quiz.rst)

   - 10 multiple choice questions covering DDS, colcon, node
     lifecycle, QoS policies, spinning, message types, and timing
     scenarios.
   - 10 true/false questions covering spin placement, publisher
     behavior, package.xml/setup.py consistency, TRANSIENT_LOCAL,
     symlink-install, print vs. logger, silent failures, and
     ros2 run.
   - 4 essay questions: monolithic vs. distributed architecture,
     QoS policies with examples, spinning and the executor, and the
     three communication timing scenarios.

   .. rubric:: Glossary (l8_glossary.rst)

   - 30 terms defined across 14 letter sections: Action, ament_python,
     Callback, colcon, DDS, Durability, Entry Point, Executor,
     Interface, Launch File, Message, Middleware, Node, package.xml,
     Process, Publisher, QoS, Queue Depth, rclpy, Reliability, ROS 2
     Workspace, rosdep, RTPS, Service, Spinning, Subscriber, setup.py,
     Thread, Timer, Topic, Workspace Overlay.

   .. rubric:: References (l8_references.rst)

   - Lecture 8 card summarizing all topics covered.
   - ROS 2 Official Documentation: Jazzy docs, beginner tutorials,
     rclpy API, QoS concepts, logging, colcon docs.
   - DDS and Middleware: OMG DDS Portal, DDS Foundation, Fast DDS,
     ROS 2 DDS vendor guide.
   - External Tutorials: Articulated Robotics, The Construct,
     Real Python OOP review.
   - Style and Best Practices: ROS 2 Python style guide, PEP 8.
   - Recommended Reading: Koubaa ROS 2 series, Programming Robots
     with ROS 2, Silberschatz OS Concepts, OMG DDS Specification.


.. dropdown:: v1.2.0 -- L6 Lecture, Exercises, and Quiz Updated (2026-03-02)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Lecture Notes (l6_lecture.rst)

   - Added "How Do We Achieve Abstraction?" dropdown with three levels (Documentation, Public Interface, Abstract Classes as L7 preview)
   - Added "How to Achieve Encapsulation" summary dropdown
   - Split ``@property`` dropdown into four separate sections: intro, Defining a Getter, Defining a Setter with Validation, and Using Properties
   - Added "Encapsulation Summary" dropdown after Read-Only Properties
   - Updated Class Attributes dropdown: removed ``max_reach`` for clarity, added shadowing warning (``self`` vs class name)
   - Added full **Appendix: Exception Handling** section with 12 dropdowns covering: runtime errors, common built-in exceptions, ``try``/``except``, accessing the exception object, handling multiple exception types, ``else`` clause, ``finally`` clause, full ``try`` statement, ``raise`` statement, why ``raise`` matters for OOP, and ``return NotImplemented`` vs ``raise NotImplementedError``

   .. rubric:: Exercises (l6_exercises.rst)

   - Exercises 1, 2, and 3: added full ``if __name__ == "__main__"`` blocks from ``L6_exercises.py``
   - Updated expected output for all three exercises to match the provided main blocks

   .. rubric:: Quiz (l6_quiz.rst)

   - Updated quiz description to reference the exception handling appendix
   - Added 3 new questions (Q31--Q33) in a new "Exception Handling (Appendix)" section covering ``try``/``except`` output, ``else`` clause purpose, and ``ValueError`` vs ``TypeError``

   .. rubric:: Slides (ENPM605-L6-v1_0.tex)

   - Bumped version to v1.2
   - Restructured lecture into Design Phase and Implementation Phase sections
   - Added "Before We Start" slide referencing the appendix
   - Added Class Attributes slide with shadowing warning
   - Added "How Do We Achieve Abstraction?" slide (3 levels)
   - Added "How to Achieve Encapsulation" summary slide
   - Split ``@property`` content across separate slides (Pythonic Way, Getter, Setter, Using, Read-Only, Summary)
   - Added Exercise 1, 2, and 3 slides with specifications
   - Added full Appendix: Exception Handling section (overview, try/except, else, finally, full try, raise, raise for OOP, NotImplemented vs NotImplementedError)


.. dropdown:: v1.1.0 -- RWA 2 Released (2026-03-01)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: RWA 2: Search and Rescue Mission Planner (new)

   **Assignment Overview**

   - New assignment covering Object-Oriented Programming (Lectures 6 and 7)
   - Two-phase structure: Phase 1 (Design) and Phase 2 (Implementation)
   - Use case: Disaster Response Operation with aerial drones and ground crawlers searching a disaster zone divided into sectors
   - Total: 50 points (Design: 6 pts, Implementation: 44 pts)
   - Due: March 25, 2026

   **Phase 1: Design Document (6 pts)**

   - Deliverable: single UML class diagram in PDF format (``design_document.pdf``)
   - Design phase intentionally lightened to allow students to focus on implementation
   - Sequence diagram removed from requirements to reduce design workload

   **Phase 2: Implementation (44 pts)**

   - 7 classes across 6 modules: ``SensorPayload``, ``Robot`` (abstract), ``AerialDrone``, ``GroundCrawler``, ``Sector``, ``Mission``, ``DisasterZone``
   - OOP concepts exercised: abstraction (``abc.ABC``), encapsulation (``@property``), inheritance (2 subclasses), polymorphism (``search()``/``can_search()`` overrides), composition (Robot owns SensorPayload), aggregation (DisasterZone manages robots/sectors), association (Mission links robot to sector)
   - Dunder methods required: ``__str__``, ``__repr__``, ``__eq__``, ``__lt__``, ``__len__``, ``__contains__``
   - Main program (9 pts) demonstrates polymorphism, sorting, ``__contains__``, and report generation

   **AI Policy**

   - Explicit policy added: AI tools (Copilot, ChatGPT, Claude, etc.) are NOT permitted for code or design
   - Students instructed to disable GitHub Copilot and other AI extensions in VS Code before starting
   - Exception: AI may be used to generate docstring documentation **after** code is written by the student

   **Other Details**

   - Project naming convention: ``firstname_lastname_rwa2/``
   - Suggested 3-week timeline included with day-by-day breakdown
   - All major sections wrapped in ``.. dropdown::`` directives for collapsible navigation
   - Use case separated into subsections using ``.. rubric::`` directives (Robots, Common Robot Characteristics, Sensor Payload, Sectors, Missions, Disaster Zone)


.. dropdown:: v1.0.0 -- Initial Release (2026-01-27)
   :icon: tag
   :class-container: sd-border-success

   Initial release of the ENPM605 Spring 2026 course documentation.

   .. rubric:: Course Structure

   - Lectures 1 through 6 published with lecture notes, exercises, quizzes, glossaries, and references
   - Each lecture organized as a self-contained folder with RST files following a consistent structure

   .. rubric:: RWA 1: Robot Fleet Monitor

   - First assignment covering Lectures 1 through 4 (variables, data types, control flow, functions)
   - 30 points, 6 parts across 5 Python modules
   - Due: February 25, 2026
