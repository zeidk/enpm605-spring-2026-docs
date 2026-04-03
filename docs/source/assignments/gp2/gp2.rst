====================================================
GP 2: ROS 2 Service and Action System
====================================================


Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - April 27, 2026, 11:59 PM EST
   * - **Total Points**
     - 50 points
   * - **Submission**
     - Canvas (ZIP file: ``group<N>_gp2.zip`` containing the ROS 2 package)
   * - **Collaboration**
     - Groups of 2.
   * - **Late Policy**
     - 10% deduction per calendar day, up to 3 days. Zero after 3 days.
   * - **Peer Review**
     - Final grade: 60% assignment grade + 40% peer review score.


.. dropdown:: Description
   :open:

   This is a **group project** (2 students per group). Each group selects
   **one** of three scenarios listed below. All three scenarios exercise
   the same core ROS 2 concepts from Lecture 10 but differ in the
   application domain and specific requirements.

   Each scenario requires you to build a multi-node ROS 2 system that
   demonstrates:

   - Custom interface design (``.msg``, ``.srv``, and ``.action`` files)
   - Service servers and clients for synchronous request/response operations
   - Action servers and clients for long-running tasks with feedback
   - Parameter configuration using YAML files and launch-time overrides
   - Launch files that wire the entire system together

   You will create **two** ROS 2 packages inside ``~/enpm605_ws/src/``:

   1. An **interfaces package** (``group<N>_gp2_interfaces``) containing
      all custom ``.msg``, ``.srv``, and ``.action`` definitions.
   2. A **Python package** (``group<N>_gp2``) containing all nodes, launch
      files, config files, and a ``README.md`` explaining your design
      decisions.


.. dropdown:: Learning Objectives
   :open:

   .. grid:: 1 2 2 2
       :gutter: 2

       .. grid-item-card:: Custom Interface Design
           :class-card: sd-border-info

           Define custom ``.msg``, ``.srv``, and ``.action`` interfaces
           that model domain-specific data. Understand how ``colcon``
           builds and sources interface packages.

       .. grid-item-card:: Service Communication
           :class-card: sd-border-info

           Implement service servers that handle synchronous requests and
           service clients that send requests and process responses using
           ``call_async()`` and futures.

       .. grid-item-card:: Action Communication
           :class-card: sd-border-info

           Implement action servers that manage long-running goals with
           progress feedback and cancellation support, and action clients
           that send goals and monitor feedback.

       .. grid-item-card:: Parameter Configuration
           :class-card: sd-border-info

           Declare and use ROS 2 parameters in nodes. Load parameters
           from YAML configuration files at launch time. Override
           parameters via launch arguments.

       .. grid-item-card:: Launch File Integration
           :class-card: sd-border-info

           Write Python launch files that start multiple nodes, load
           parameter files, pass arguments, and use conditionals and
           grouping to orchestrate the system.

       .. grid-item-card:: System Integration
           :class-card: sd-border-info

           Wire service servers/clients, action servers/clients, and
           parameterized nodes into a coherent multi-node system and
           verify end-to-end behavior with ROS 2 CLI tools.


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
        - Read the scenario carefully. Define all custom interfaces
          (``.msg``, ``.srv``, ``.action``). Create both packages and
          build the interfaces package. Verify interfaces with
          ``ros2 interface show``. Divide work between teammates.
      * - **Week 1**
        - Days 4--7
        - Implement and test the service server and client nodes.
          Verify with ``ros2 service call`` and ``ros2 service list``.
          Begin implementing the action server.
      * - **Week 2**
        - Days 8--10
        - Complete the action server with feedback and result handling.
          Implement the action client. Test with
          ``ros2 action send_goal --feedback``. Add parameters and
          YAML config files.
      * - **Week 2**
        - Days 11--12
        - Write launch files that start all nodes, load parameter
          files, and support launch arguments. Test the full system
          end to end.
      * - **Week 2**
        - Days 13--14
        - Write ``README.md`` and code quality pass (docstrings, type
          hints, comments). Package and submit.

   .. tip::

      Build and test the interfaces package first. If ``ros2 interface show``
      does not display your custom types, nothing else will work. Divide
      remaining work by node: one teammate implements the service
      server/client, the other implements the action server/client.


Common Requirements
===================

The following requirements apply to **all three scenarios**. Scenario-
specific requirements are listed in each scenario page.


.. dropdown:: Package Structure
   :open:

   Your submission must contain **two** ROS 2 packages. Replace ``<N>``
   with your group number.

   **Interfaces package** (``group<N>_gp2_interfaces``):

   .. code-block:: text

      group<N>_gp2_interfaces/
      |-- msg/
      |   |-- <CustomMsg1>.msg
      |   |-- <CustomMsg2>.msg
      |-- srv/
      |   |-- <CustomSrv>.srv
      |-- action/
      |   |-- <CustomAction>.action
      |-- CMakeLists.txt
      |-- package.xml

   **Python package** (``group<N>_gp2``):

   .. code-block:: text

      group<N>_gp2/
      |-- group<N>_gp2/          # Python module (node files)
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
      |-- config/                # Parameter YAML files
      |   |-- params.yaml
      |-- resource/
      |-- test/
      |-- package.xml
      |-- setup.py
      |-- setup.cfg
      |-- README.md

   Each node class must live in its own Python file. Do not place
   multiple node classes in the same file. Each node must have a
   corresponding entry point script in ``scripts/``.

   **Package metadata:** Both ``package.xml`` and ``setup.py`` (or
   ``CMakeLists.txt`` for the interfaces package) must be updated with
   a meaningful description, a license (e.g., ``Apache-2.0``), and both
   group members listed as maintainers with their email addresses.

   **Interfaces package build dependencies:** The ``CMakeLists.txt`` must
   include ``find_package(rosidl_default_generators REQUIRED)`` and use
   ``rosidl_generate_interfaces()`` to build all ``.msg``, ``.srv``, and
   ``.action`` files. The ``package.xml`` must declare build and execution
   dependencies on ``rosidl_default_generators`` and
   ``rosidl_default_runtime``.


.. dropdown:: Service Requirements
   :open:

   Every scenario must demonstrate the following service concepts:

   1. **At least one service** using a custom ``.srv`` interface (not a
      standard ``std_srvs`` type).
   2. **Service server** that validates the request, performs the
      operation, and returns a meaningful response with a ``success``
      field and a ``message`` field.
   3. **Service client** that sends requests using ``call_async()`` and
      processes the response using a future callback or ``rclpy.spin_until_future_complete()``.
   4. **Error handling:** The service server must handle invalid requests
      gracefully (e.g., unknown location, invalid robot ID) and return
      ``success=False`` with a descriptive error message.


.. dropdown:: Action Requirements
   :open:

   Every scenario must demonstrate the following action concepts:

   1. **At least one action** using a custom ``.action`` interface (not a
      standard type).
   2. **Action server** that:

      - Accepts a goal and begins execution.
      - Publishes periodic feedback (at least once per second) reporting
        progress as a percentage or step count.
      - Returns a result when the goal is complete.
      - Supports **goal cancellation**: if the client cancels, the server
        stops execution and returns a partial result.

   3. **Action client** that:

      - Sends a goal and registers a feedback callback to log progress.
      - Handles the result callback to log the final outcome.
      - Demonstrates cancellation by sending a cancel request during
        execution (can be triggered by a timer or condition).

   4. **Simulated execution:** Use ``time.sleep()`` or a timer inside the
      action server to simulate work being done. Each step should take
      0.5--1.0 seconds so that feedback is visible.


.. dropdown:: Parameter Requirements
   :open:

   Every scenario must demonstrate the following parameter concepts:

   1. **At least three declared parameters** across your nodes using
      ``self.declare_parameter()``.
   2. **A YAML configuration file** (``config/params.yaml``) that sets
      default values for all parameters.
   3. **Launch-time parameter loading** using the launch file to load the
      YAML file for each node.
   4. **At least one launch argument** that overrides a parameter value
      (e.g., ``ros2 launch group<N>_gp2 system.launch.py threshold:=5.0``).
   5. **Parameter usage:** Parameters must affect node behavior (e.g.,
      thresholds, rates, limits) -- do not declare parameters that are
      never read.


.. dropdown:: Launch File Requirements
   :open:

   1. A **main launch file** (``system.launch.py``) that starts all nodes
      in the system.
   2. At least one **launch argument** that overrides a node parameter.
   3. At least one **conditional node** using ``IfCondition``.
   4. At least one **node group** using ``GroupAction``.
   5. All nodes must use ``output="screen"`` and ``emulate_tty=True``.
   6. **Parameter file loading:** Use the ``parameters`` field in the
      ``Node`` action to load ``config/params.yaml``.


.. dropdown:: README.md Requirements
   :open:

   Your ``README.md`` must include:

   1. **Group members**: names and UIDs.
   2. **Contributions**: a brief description of each team member's
      contributions (e.g., which nodes each person implemented, who wrote
      the interfaces, who handled the launch files).
   3. **Scenario chosen**: which scenario and a one-paragraph summary.
   4. **System architecture**: a text or diagram showing all nodes,
      services, actions, topics, and custom interface types. You may use
      a tool like `Mermaid <https://mermaid.js.org/>`_ or a screenshot of
      ``rqt_graph``.
   5. **Custom interfaces**: list each ``.msg``, ``.srv``, and ``.action``
      file with a brief description of its purpose.
   6. **Design decisions**: explain your choice of interface fields,
      parameter values, and how you handled error cases and cancellation.
   7. **Build and run instructions**: exact commands to build both
      packages, source, and launch the system.
   8. **Known issues**: any limitations or incomplete features.


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
     service/action design choices, and parameter usage.
   - **Naming conventions:** ``snake_case`` for topics, services, actions,
     methods, and variables. ``CamelCase`` for class names and interface
     types.
   - **Logging:** Use the ROS 2 logger exclusively -- never ``print()``.
     Use the appropriate severity level: ``self.get_logger().info()`` for
     normal operation, ``self.get_logger().warn()`` for warnings, and
     ``self.get_logger().error()`` for errors.
   - **Linting:** Ensure Ruff is enabled and no errors appear.


----


.. dropdown:: Pre-Submission Checklist
   :open:

   **Functionality**

   - |box| The interfaces package builds: ``colcon build --packages-select group<N>_gp2_interfaces``
   - |box| The Python package builds: ``colcon build --packages-select group<N>_gp2``
   - |box| Custom interfaces are visible: ``ros2 interface show group<N>_gp2_interfaces/srv/<ServiceName>``
   - |box| The system launches: ``ros2 launch group<N>_gp2 system.launch.py``
   - |box| Service works: ``ros2 service list`` shows the service; ``ros2 service call`` returns a valid response.
   - |box| Action works: ``ros2 action list`` shows the action; ``ros2 action send_goal --feedback`` shows progress.
   - |box| Action cancellation works and returns a partial result.
   - |box| Parameters load from YAML: ``ros2 param list`` and ``ros2 param get`` show correct values.
   - |box| Launch arguments work: ``--show-args`` and override.

   **Documentation**

   - |box| ``README.md`` includes all required sections.

   **Code Quality**

   - |box| Type hints on all methods.
   - |box| Google-style docstrings on all classes and methods.
   - |box| Service and action design choices explained in comments.
   - |box| No linting errors (Ruff).

   **Packaging**

   - |box| Removed ``__pycache__/``, ``*.pyc``, ``.ruff_cache/``.
   - |box| ZIP file is named ``group<N>_gp2.zip``.
   - |box| ZIP contains both package folders.

   .. |box| unicode:: U+2610


.. dropdown:: Submission
   :open:

   - Submit a ZIP file named ``group<N>_gp2.zip`` on Canvas (e.g.,
     ``group3_gp2.zip``).
   - The ZIP must contain **both** package folders
     (``group<N>_gp2_interfaces/`` and ``group<N>_gp2/``) with all source
     files, launch files, config files, and ``README.md``.
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

   gp2_scenario1
   gp2_scenario2
   gp2_scenario3
