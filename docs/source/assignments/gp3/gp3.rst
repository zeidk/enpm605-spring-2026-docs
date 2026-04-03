====================================================
GP 3: Simulation and Autonomous Navigation
====================================================


Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - May 11, 2026, 11:59 PM EST
   * - **Total Points**
     - 60 points
   * - **Submission**
     - Canvas (ZIP file: ``group<N>_gp3.zip`` containing the ROS 2 package)
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
   the same core concepts from Lectures 11 and 12 but differ in the
   application domain and specific requirements.

   Each scenario requires you to build a simulated robot system using
   **Gazebo Harmonic** with **Nav2** navigation and **lifecycle node**
   management. You will integrate several subsystems -- simulation,
   navigation, sensor processing, and application logic -- into a
   cohesive autonomous system that can be launched, configured, and
   managed through lifecycle state transitions.

   Each scenario requires you to demonstrate:

   - Gazebo Harmonic simulation with a differential-drive robot
   - At least one custom lifecycle node with full state management
   - Nav2 configuration and programmatic navigation using ``BasicNavigator``
   - Sensor data processing via ``ros_gz_bridge``
   - A launch file that brings up the entire system with a single command

   You will create a single ROS 2 Python package inside
   ``~/enpm605_ws/src/`` containing all nodes, launch files,
   configuration files, and a ``README.md`` explaining your design
   decisions.


.. dropdown:: Learning Objectives
   :open:

   .. grid:: 1 2 2 2
       :gutter: 2

       .. grid-item-card:: Gazebo Simulation
           :class-card: sd-border-info

           Set up a Gazebo Harmonic simulation environment with a
           differential-drive robot, configure SDF worlds, and spawn
           robot models programmatically via launch files.

       .. grid-item-card:: Lifecycle Node Design
           :class-card: sd-border-info

           Implement custom lifecycle nodes with ``on_configure``,
           ``on_activate``, ``on_deactivate``, and ``on_cleanup``
           callbacks. Use ``ros2 lifecycle`` CLI tools to manage node
           state transitions.

       .. grid-item-card:: Nav2 Configuration
           :class-card: sd-border-info

           Configure Nav2 parameters for planners, controllers,
           costmaps, and localization. Launch the full Nav2 stack in
           simulation.

       .. grid-item-card:: Programmatic Navigation
           :class-card: sd-border-info

           Use the ``BasicNavigator`` API to send navigation goals
           (``NavigateToPose``) and waypoints programmatically from
           Python code.

       .. grid-item-card:: Sensor Integration
           :class-card: sd-border-info

           Bridge Gazebo sensor topics (lidar, camera, IMU) into ROS 2
           using ``ros_gz_bridge`` and process sensor data in custom
           nodes.

       .. grid-item-card:: System Integration
           :class-card: sd-border-info

           Wire simulation, navigation, lifecycle management, and
           application logic into a complete autonomous system launched
           with a single command.


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
        - Read the scenario carefully. Set up the Gazebo simulation
          environment: create or adapt an SDF world, configure the robot
          model, and verify the robot spawns correctly. Test basic
          ``cmd_vel`` control and sensor bridging with ``ros_gz_bridge``.
      * - **Week 1**
        - Days 4--7
        - Configure Nav2: set up the navigation parameter YAML file
          (planner, controller, costmaps, AMCL). Launch Nav2 in
          simulation and verify the robot can navigate to a manually
          set goal in RViz. Generate and save a map using SLAM Toolbox.
      * - **Week 2**
        - Days 8--10
        - Implement the custom lifecycle node(s). Test lifecycle
          transitions using ``ros2 lifecycle set`` CLI commands. Verify
          that ``on_configure`` allocates resources, ``on_activate``
          starts processing, ``on_deactivate`` pauses, and
          ``on_cleanup`` releases resources.
      * - **Week 2**
        - Days 11--14
        - Implement programmatic navigation using ``BasicNavigator``.
          Send ``NavigateToPose`` goals and verify the robot reaches
          each waypoint. Integrate sensor processing (e.g., lidar
          obstacle detection, camera-based detection).
      * - **Week 3**
        - Days 15--18
        - Write the main launch file that brings up the entire system
          (Gazebo, robot spawn, Nav2, custom nodes). Test the full
          end-to-end pipeline. Debug integration issues.
      * - **Week 3**
        - Days 19--21
        - Write ``README.md`` and code quality pass (docstrings, type
          hints, comments). Record a demo video if required. Package
          and submit.

   .. tip::

      Divide work by subsystem: one teammate handles simulation setup
      and Nav2 configuration while the other implements the lifecycle
      node and programmatic navigation. Integrate frequently to catch
      interface mismatches early.


Common Requirements
===================

The following requirements apply to **all three scenarios**. Scenario-
specific requirements are listed in each scenario page.


.. dropdown:: Package Structure
   :open:

   Your submission must be a single ROS 2 Python package.

   .. code-block:: text

      group<N>_gp3/
      |-- group<N>_gp3/          # Python module (node files)
      |   |-- __init__.py
      |   |-- <lifecycle_node>.py
      |   |-- <navigator_node>.py
      |   |-- ...
      |-- scripts/               # Entry point scripts
      |   |-- __init__.py
      |   |-- main_<lifecycle_node>.py
      |   |-- main_<navigator_node>.py
      |   |-- ...
      |-- launch/                # Launch files
      |   |-- system.launch.py
      |   |-- ...
      |-- config/                # Configuration files
      |   |-- nav2_params.yaml
      |   |-- bridge_params.yaml
      |   |-- ...
      |-- worlds/                # Gazebo SDF world files
      |   |-- <scenario_world>.sdf
      |-- maps/                  # Pre-generated map files
      |   |-- <map_name>.yaml
      |   |-- <map_name>.pgm
      |-- resource/
      |-- test/
      |-- package.xml
      |-- setup.py
      |-- setup.cfg
      |-- README.md

   Each node class must live in its own Python file. Do not place
   multiple node classes in the same file. Each node must have a
   corresponding entry point script in ``scripts/``.

   **Package metadata:** Both ``package.xml`` and ``setup.py`` must be
   updated with a meaningful description, a license (e.g.,
   ``Apache-2.0``), and both group members listed as maintainers with
   their email addresses.

   **Data files:** The ``setup.py`` must install launch files, config
   files, world files, and map files into the appropriate share
   directories using the ``data_files`` parameter:

   .. code-block:: python

      data_files=[
          ('share/ament_index/resource_index/packages',
              ['resource/' + package_name]),
          ('share/' + package_name, ['package.xml']),
          (os.path.join('share', package_name, 'launch'),
              glob('launch/*.py')),
          (os.path.join('share', package_name, 'config'),
              glob('config/*.yaml')),
          (os.path.join('share', package_name, 'worlds'),
              glob('worlds/*.sdf')),
          (os.path.join('share', package_name, 'maps'),
              glob('maps/*')),
      ],


.. dropdown:: Lifecycle Node Requirements
   :open:

   Every scenario must include at least one custom lifecycle node that
   demonstrates the managed node pattern:

   1. **Inherit from** ``LifecycleNode`` (from
      ``rclpy.lifecycle``).
   2. **Implement all four primary callbacks**:

      - ``on_configure(state)``: Declare parameters, create publishers,
        subscribers, and timers (but do not activate them). Allocate any
        required resources. Return ``TransitionCallbackReturn.SUCCESS``.
      - ``on_activate(state)``: Start processing (e.g., enable timers,
        begin publishing). Return ``TransitionCallbackReturn.SUCCESS``.
      - ``on_deactivate(state)``: Pause processing (e.g., cancel timers,
        stop publishing). The node should be safe to re-activate. Return
        ``TransitionCallbackReturn.SUCCESS``.
      - ``on_cleanup(state)``: Release all resources (destroy publishers,
        subscribers, timers). Reset internal state. Return
        ``TransitionCallbackReturn.SUCCESS``.

   3. **State-aware behavior**: The node must only perform its primary
      function (e.g., publishing navigation goals, processing sensor
      data) when in the ``ACTIVE`` state. Use a guard check or the
      lifecycle state to prevent processing in other states.
   4. **Error handling**: If ``on_configure`` fails (e.g., missing
      parameter, file not found), return
      ``TransitionCallbackReturn.FAILURE`` and log the error.
   5. **CLI verification**: You must be able to demonstrate lifecycle
      transitions using ``ros2 lifecycle`` commands:

      .. code-block:: console

         ros2 lifecycle list /<node_name>
         ros2 lifecycle set /<node_name> configure
         ros2 lifecycle set /<node_name> activate
         ros2 lifecycle set /<node_name> deactivate
         ros2 lifecycle set /<node_name> cleanup


.. dropdown:: Nav2 Requirements
   :open:

   Every scenario must demonstrate autonomous navigation using the Nav2
   stack:

   1. **Nav2 parameter file**: Provide a ``nav2_params.yaml`` in the
      ``config/`` directory that configures:

      - **Planner server**: ``NavfnPlanner`` or ``SmacPlanner2D``
      - **Controller server**: ``FollowPath`` with
        ``DWBLocalPlanner`` or ``RegulatedPurePursuitController``
      - **Global costmap**: ``static_layer`` + ``obstacle_layer`` +
        ``inflation_layer``
      - **Local costmap**: ``obstacle_layer`` + ``inflation_layer``
      - **AMCL**: localization parameters (initial pose, particle count,
        laser model)
      - **Robot footprint**: matching your robot model dimensions

   2. **Pre-generated map**: Include a map of your simulation world
      generated using SLAM Toolbox. The map files (``<map>.yaml`` and
      ``<map>.pgm``) must be in the ``maps/`` directory.

   3. **Programmatic navigation**: Use the ``BasicNavigator`` class from
      ``nav2_simple_commander`` to send navigation goals:

      .. code-block:: python

         from nav2_simple_commander.robot_navigator import BasicNavigator
         from geometry_msgs.msg import PoseStamped

         navigator = BasicNavigator()
         navigator.waitUntilNav2Active()

         goal = PoseStamped()
         goal.header.frame_id = 'map'
         goal.header.stamp = navigator.get_clock().now().to_msg()
         goal.pose.position.x = 2.0
         goal.pose.position.y = 1.0
         goal.pose.orientation.w = 1.0

         navigator.goToPose(goal)

         while not navigator.isTaskComplete():
             feedback = navigator.getFeedback()
             # Process feedback...

   4. **At least 3 navigation goals**: Your system must navigate to at
      least 3 distinct poses in the simulation environment.

   5. **Navigation feedback**: Log navigation feedback (distance
      remaining, estimated time) during goal execution.


.. dropdown:: Simulation Requirements
   :open:

   Every scenario must run in a Gazebo Harmonic simulation:

   1. **SDF world file**: Provide a custom or adapted SDF world file in
      the ``worlds/`` directory. The world must contain:

      - A ground plane
      - At least 4 walls or obstacles that create a navigable
        environment
      - Adequate lighting

   2. **Robot model**: Use a differential-drive robot model with at
      minimum:

      - A lidar sensor (e.g., ``gpu_lidar`` or ``ray`` sensor)
      - Either a camera sensor or an IMU sensor (or both)
      - A ``DiffDrive`` plugin for velocity control

      You may use an existing robot model (e.g., TurtleBot3, a custom
      SDF robot) or build your own. Document the model source in your
      ``README.md``.

   3. **ros_gz_bridge**: Configure the bridge to relay at minimum:

      - ``/cmd_vel`` (``geometry_msgs/Twist``) -- robot velocity commands
      - ``/scan`` (``sensor_msgs/LaserScan``) -- lidar data
      - ``/clock`` (``rosgraph_msgs/Clock``) -- simulation clock

      Provide the bridge configuration in ``config/bridge_params.yaml``
      or as command-line arguments in the launch file.

   4. **Robot spawning**: The launch file must spawn the robot into the
      simulation using ``ros_gz_sim``'s ``create`` node or equivalent.


.. dropdown:: Launch File Requirements
   :open:

   1. A **main launch file** (``system.launch.py``) that starts the
      entire system with a single command:

      - Gazebo Harmonic simulation server and client
      - Robot spawning
      - ``ros_gz_bridge`` with the required topic bridges
      - Nav2 stack (using ``nav2_bringup`` launch file or individual
        node launches)
      - Custom lifecycle node(s)
      - Application-specific nodes (navigator, sensor processor, etc.)

   2. At least one **launch argument** (e.g., ``use_sim_time``,
      ``world_file``, ``map_file``, or a scenario-specific parameter).
   3. At least one **conditional node** using ``IfCondition`` (e.g.,
      to enable/disable RViz or a debug logger).
   4. At least one **node group** using ``GroupAction`` (e.g., grouping
      Nav2 nodes or custom application nodes).
   5. All custom nodes must use ``output="screen"`` and
      ``emulate_tty=True``.
   6. Set ``use_sim_time:=true`` for all nodes that need synchronized
      simulation time.


.. dropdown:: README.md Requirements
   :open:

   Your ``README.md`` must include:

   1. **Group members**: names and UIDs.
   2. **Contributions**: a brief description of each team member's
      contributions (e.g., who handled simulation setup, who implemented
      the lifecycle node, who configured Nav2).
   3. **Scenario chosen**: which scenario and a one-paragraph summary.
   4. **System architecture**: a diagram showing all nodes, topics,
      services, and actions. Include the Nav2 nodes and how your custom
      nodes interact with them. You may use
      `Mermaid <https://mermaid.js.org/>`_ or a screenshot of
      ``rqt_graph``.
   5. **Simulation environment**: description of the world, robot model
      used, and sensor configuration. Include a screenshot of the
      Gazebo environment.
   6. **Lifecycle node design**: explain the lifecycle state transitions
      and what happens in each callback (configure, activate,
      deactivate, cleanup).
   7. **Nav2 configuration**: explain your choice of planner, controller,
      and costmap parameters.
   8. **Build and run instructions**: exact commands to build, source, and
      launch the system.
   9. **Demo**: describe the expected behavior and how to verify it.
      Include screenshots or a link to a demo video.
   10. **Known issues**: any limitations or incomplete features.


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
     lifecycle state transitions, Nav2 configuration choices, and sensor
     processing algorithms.
   - **Naming conventions:** ``snake_case`` for topics, methods, and
     variables. ``CamelCase`` for class names.
   - **Logging:** Use the ROS 2 logger exclusively -- never ``print()``.
     Use the appropriate severity level: ``self.get_logger().info()`` for
     normal operation, ``self.get_logger().warn()`` for warnings (e.g.,
     navigation failure, obstacle detected), and
     ``self.get_logger().error()`` for errors (e.g., lifecycle transition
     failure).
   - **Linting:** Ensure Ruff is enabled and no errors appear.


----


.. dropdown:: Pre-Submission Checklist
   :open:

   **Simulation**

   - |box| Gazebo launches and the world loads correctly.
   - |box| Robot spawns in the correct position.
   - |box| ``ros_gz_bridge`` relays ``/cmd_vel``, ``/scan``, and ``/clock``.
   - |box| Lidar data is visible in RViz: ``ros2 topic echo /scan``
   - |box| Robot responds to velocity commands: ``ros2 topic pub /cmd_vel geometry_msgs/Twist ...``

   **Navigation**

   - |box| Nav2 stack launches without errors.
   - |box| Map loads correctly and is visible in RViz.
   - |box| Robot localizes using AMCL.
   - |box| Robot navigates to at least 3 programmatic goals.
   - |box| Navigation feedback is logged during goal execution.

   **Lifecycle Node**

   - |box| Lifecycle node transitions work: ``ros2 lifecycle set /<node> configure``
   - |box| ``on_configure`` allocates resources and returns SUCCESS.
   - |box| ``on_activate`` starts processing.
   - |box| ``on_deactivate`` pauses processing without crashing.
   - |box| ``on_cleanup`` releases all resources.
   - |box| Node only processes when in ACTIVE state.

   **System Integration**

   - |box| The system builds: ``colcon build --packages-select group<N>_gp3``
   - |box| The system launches: ``ros2 launch group<N>_gp3 system.launch.py``
   - |box| All nodes start and communicate correctly.
   - |box| End-to-end behavior matches scenario requirements.

   **Documentation**

   - |box| ``README.md`` includes all required sections.

   **Code Quality**

   - |box| Type hints on all methods.
   - |box| Google-style docstrings on all classes and methods.
   - |box| Lifecycle callbacks explained in comments.
   - |box| No linting errors (Ruff).

   **Packaging**

   - |box| Removed ``__pycache__/``, ``*.pyc``, ``.ruff_cache/``.
   - |box| ZIP file is named ``group<N>_gp3.zip``.
   - |box| ZIP contains only the package folder.
   - |box| Config, world, map, and launch files are included.

   .. |box| unicode:: U+2610


.. dropdown:: Submission
   :open:

   - Submit a ZIP file named ``group<N>_gp3.zip`` on Canvas (e.g.,
     ``group3_gp3.zip``).
   - The ZIP must contain the ROS 2 package folder with all source files,
     launch files, configuration files, world files, map files, and
     ``README.md``.
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

   gp3_scenario1
   gp3_scenario2
   gp3_scenario3
