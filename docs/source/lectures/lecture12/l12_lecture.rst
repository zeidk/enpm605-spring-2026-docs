====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Prerequisites
====================================================

One-time workspace and environment setup required before running any
code in this lecture.


.. dropdown:: One-Time Setup

   Ensure the course workspace is cloned and configured as described in
   L8.  All code in this lecture assumes the ``enpm605`` shell function
   has been run in the current terminal.

   .. code-block:: console

      # If you have not already cloned the workspace
      git clone https://github.com/zeidk/enpm605-spring-2026-ros.git ~/enpm605_ws

   .. code-block:: console

      enpm605

   .. note::

      This lecture builds on the Gazebo simulation environment set up in
      L11.  Make sure you have successfully completed the L11 exercises
      and can launch the simulated robot before proceeding.


.. dropdown:: Required Packages

   Install the Nav2 and SLAM Toolbox packages if they are not already
   present:

   .. code-block:: console

      sudo apt update
      sudo apt install -y ros-jazzy-navigation2 \
                          ros-jazzy-nav2-bringup \
                          ros-jazzy-slam-toolbox

   Rebuild the workspace after installing new dependencies:

   .. code-block:: console

      cd ~/enpm605_ws && colcon build --symlink-install
      source install/setup.bash


Lifecycle Nodes
====================================================

Managed nodes with a deterministic state machine that gives system
integrators control over startup, runtime, and shutdown behavior.


Why Lifecycle Nodes Exist
-------------------------

.. dropdown:: Motivation

   In a standard ROS 2 system, nodes begin processing as soon as they
   are constructed.  This creates several problems in complex robotic
   systems:

   - **Non-deterministic startup**: Nodes may begin publishing before
     their subscribers are ready, causing lost messages.
   - **Resource contention**: Multiple nodes may try to acquire the same
     hardware resource (camera, LiDAR) simultaneously.
   - **No coordinated shutdown**: There is no mechanism to gracefully
     release resources in a defined order.
   - **Difficult error recovery**: A crashed node cannot be
     reconfigured without restarting the entire process.

   Lifecycle nodes solve these problems by introducing a **state
   machine** that separates construction from configuration from
   activation.  An external manager (or the developer via CLI) controls
   when each transition occurs.


The Lifecycle State Machine
---------------------------

A lifecycle node progresses through four **primary states** connected
by **transition states**:

.. dropdown:: Primary States

   .. list-table::
      :header-rows: 1
      :widths: 20 80

      * - State
        - Description
      * - **Unconfigured**
        - The node has been constructed but no resources have been
          allocated.  This is the initial state after instantiation.
      * - **Inactive**
        - The node has been configured (parameters loaded, publishers
          and subscribers created) but is not yet processing data.
      * - **Active**
        - The node is fully operational -- callbacks fire, data flows.
      * - **Finalized**
        - The node has been shut down and cannot be restarted.

.. dropdown:: Transition States

   Transitions are triggered by external commands and invoke
   user-defined callbacks:

   .. list-table::
      :header-rows: 1
      :widths: 25 25 50

      * - Transition
        - Callback
        - Effect
      * - ``configure``
        - ``on_configure``
        - Unconfigured --> Inactive.  Allocate resources, create
          pub/sub, load parameters.
      * - ``activate``
        - ``on_activate``
        - Inactive --> Active.  Enable processing, start timers.
      * - ``deactivate``
        - ``on_deactivate``
        - Active --> Inactive.  Pause processing, stop timers.
      * - ``cleanup``
        - ``on_cleanup``
        - Inactive --> Unconfigured.  Release resources.
      * - ``shutdown``
        - ``on_shutdown``
        - Any state --> Finalized.  Final cleanup before destruction.


Implementing a Lifecycle Node in Python
----------------------------------------

.. dropdown:: Minimal Example

   The ``rclpy.lifecycle`` module provides ``LifecycleNode`` as a drop-in
   replacement for ``Node``.

   .. code-block:: python

      import rclpy
      from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn
      from std_msgs.msg import String


      class ManagedTalker(LifecycleNode):
          """A lifecycle-managed publisher node."""

          def __init__(self):
              super().__init__("managed_talker")
              self._publisher = None
              self._timer = None
              self._count = 0
              self.get_logger().info("Node constructed -- state: Unconfigured")

          # -- Transition callbacks ----------------------------------------

          def on_configure(self, state: LifecycleState) -> TransitionCallbackReturn:
              """Allocate resources (Unconfigured -> Inactive)."""
              self._publisher = self.create_lifecycle_publisher(String, "chatter", 10)
              self.get_logger().info("Configured -- publisher created")
              return TransitionCallbackReturn.SUCCESS

          def on_activate(self, state: LifecycleState) -> TransitionCallbackReturn:
              """Start processing (Inactive -> Active)."""
              self._timer = self.create_timer(1.0, self._timer_callback)
              self.get_logger().info("Activated -- timer started")
              return super().on_activate(state)

          def on_deactivate(self, state: LifecycleState) -> TransitionCallbackReturn:
              """Pause processing (Active -> Inactive)."""
              if self._timer is not None:
                  self.destroy_timer(self._timer)
                  self._timer = None
              self.get_logger().info("Deactivated -- timer stopped")
              return super().on_deactivate(state)

          def on_cleanup(self, state: LifecycleState) -> TransitionCallbackReturn:
              """Release resources (Inactive -> Unconfigured)."""
              self._publisher = None
              self._count = 0
              self.get_logger().info("Cleaned up -- resources released")
              return TransitionCallbackReturn.SUCCESS

          def on_shutdown(self, state: LifecycleState) -> TransitionCallbackReturn:
              """Final cleanup (Any -> Finalized)."""
              self.get_logger().info("Shutting down")
              self._publisher = None
              self._timer = None
              return TransitionCallbackReturn.SUCCESS

          # -- Application logic -------------------------------------------

          def _timer_callback(self):
              msg = String()
              msg.data = f"Hello lifecycle world: {self._count}"
              self._publisher.publish(msg)
              self.get_logger().info(f"Published: {msg.data}")
              self._count += 1

   .. note::

      ``create_lifecycle_publisher`` creates a publisher that is
      automatically enabled/disabled when the node transitions between
      Active and Inactive states.  Messages published while Inactive are
      silently dropped.


.. dropdown:: Entry Point

   .. code-block:: python

      # scripts/run_managed_talker.py
      import rclpy
      from lifecycle_demo.managed_talker import ManagedTalker


      def main():
          rclpy.init()
          node = ManagedTalker()
          try:
              rclpy.spin(node)
          except KeyboardInterrupt:
              pass
          finally:
              node.destroy_node()
              rclpy.shutdown()


      if __name__ == "__main__":
          main()


Lifecycle Events and Bond Connections
--------------------------------------

.. dropdown:: Lifecycle Events

   Every lifecycle node automatically publishes its state transitions on
   the ``~/transition_event`` topic.  External managers subscribe to
   this topic to monitor the health of each managed node.

   .. code-block:: console

      # Monitor transition events
      ros2 topic echo /managed_talker/transition_event

   The message type is ``lifecycle_msgs/msg/TransitionEvent`` and
   contains the start state, goal state, and transition label.


.. dropdown:: Bond Connections

   Nav2 uses **bond connections** to detect when a lifecycle node has
   crashed.  When a managed node is activated, it establishes a bond
   with the lifecycle manager.  If the node stops sending heartbeats
   (e.g., due to a crash), the manager detects the failure and can
   attempt recovery.

   .. code-block:: console

      sudo apt install -y ros-jazzy-bondcpp ros-jazzy-bond

   .. warning::

      If a Nav2 node crashes and breaks its bond, the lifecycle manager
      will attempt to restart the node.  Ensure that your
      ``on_configure`` callback is idempotent so the node can be safely
      reconfigured after a crash.


Lifecycle CLI Tools
--------------------

.. dropdown:: ``ros2 lifecycle`` Commands

   The ``ros2 lifecycle`` verb provides full control over managed nodes
   from the command line:

   .. code-block:: console

      # List all lifecycle nodes
      ros2 lifecycle nodes

      # Get the current state of a node
      ros2 lifecycle get /managed_talker

      # List available transitions
      ros2 lifecycle list /managed_talker

      # Trigger a transition
      ros2 lifecycle set /managed_talker configure
      ros2 lifecycle set /managed_talker activate

   **Typical startup sequence:**

   .. code-block:: console

      ros2 lifecycle set /managed_talker configure
      ros2 lifecycle set /managed_talker activate

   **Graceful shutdown sequence:**

   .. code-block:: console

      ros2 lifecycle set /managed_talker deactivate
      ros2 lifecycle set /managed_talker cleanup
      ros2 lifecycle set /managed_talker shutdown

   .. tip::

      Use ``ros2 lifecycle`` in scripts and launch files to orchestrate
      multi-node startup sequences.  Configure all nodes first, then
      activate them in the correct order to avoid race conditions.


Nav2 Architecture
====================================================

Nav2 is the production-grade autonomous navigation framework for
ROS 2, providing path planning, trajectory tracking, obstacle
avoidance, localization, and recovery behaviors.


What Is Nav2?
--------------

.. dropdown:: Overview

   **Navigation2 (Nav2)** is the successor to the ROS 1 Navigation
   stack.  It is a collection of lifecycle-managed servers, each
   responsible for one aspect of autonomous navigation:

   - **Planning** a global path from start to goal.
   - **Controlling** the robot to follow the path.
   - **Recovering** from failures (e.g., clearing costmaps, spinning
     in place, backing up).
   - **Localizing** the robot on a known map.

   All Nav2 servers are lifecycle nodes, meaning the entire navigation
   stack can be brought up, monitored, and shut down in a coordinated
   fashion using a single lifecycle manager.


High-Level Architecture
------------------------

.. dropdown:: Core Components

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - Component
        - Responsibility
      * - **BT Navigator**
        - Orchestrates navigation using a behavior tree (covered in
          L13).  Receives goals and coordinates planner, controller,
          and recovery servers.
      * - **Planner Server**
        - Computes a global path from the robot's current position to
          the goal.  Default plugin: ``NavfnPlanner`` (Dijkstra/A*).
      * - **Controller Server**
        - Generates velocity commands to follow the planned path.
          Default plugin: ``DWBLocalPlanner``.
      * - **Behavior Server**
        - Executes recovery behaviors such as ``Spin``, ``BackUp``, and
          ``Wait`` when the robot gets stuck.
      * - **Map Server**
        - Loads and serves a static occupancy grid map.
      * - **AMCL**
        - Adaptive Monte Carlo Localization -- localizes the robot on
          the static map using a particle filter and laser scan data.
      * - **Costmap 2D**
        - Maintains layered costmaps (static, obstacle, inflation) used
          by both the planner and the controller.

   .. note::

      Every component listed above is a **lifecycle node**.  The
      ``nav2_lifecycle_manager`` coordinates their transitions so the
      entire stack starts up and shuts down deterministically.


Configuring Nav2
====================================================

Nav2 is configured through a single YAML file that contains parameters
for every server.


nav2_params.yaml Structure
---------------------------

.. dropdown:: File Layout

   The parameter file is organized by node name.  Each top-level key
   corresponds to a lifecycle node:

   .. code-block:: yaml

      bt_navigator:
        ros__parameters:
          # BT Navigator parameters ...

      planner_server:
        ros__parameters:
          # Planner parameters ...

      controller_server:
        ros__parameters:
          # Controller parameters ...

      behavior_server:
        ros__parameters:
          # Recovery behavior parameters ...

      local_costmap:
        local_costmap:
          ros__parameters:
            # Local costmap parameters ...

      global_costmap:
        global_costmap:
          ros__parameters:
            # Global costmap parameters ...

      map_server:
        ros__parameters:
          yaml_filename: "map.yaml"

      amcl:
        ros__parameters:
          # AMCL parameters ...

   .. tip::

      Start with the default parameter file from ``nav2_bringup`` and
      modify only the parameters you need.  The defaults are well-tuned
      for most use cases.

      .. code-block:: console

         ros2 pkg prefix nav2_bringup
         # Look in share/nav2_bringup/params/nav2_params.yaml


Planner Plugins
----------------

.. dropdown:: Available Planners

   Nav2 supports multiple global planning algorithms through a plugin
   interface:

   .. list-table::
      :header-rows: 1
      :widths: 20 80

      * - Plugin
        - Description
      * - **NavFn**
        - Dijkstra or A* search on the costmap.  Fast and reliable for
          most environments.  Default planner.
      * - **SmacPlanner2D**
        - State-lattice planner with smoother paths.  Better for large
          open environments.
      * - **SmacPlannerHybrid**
        - Hybrid A* planner for non-holonomic robots (e.g., Ackermann
          vehicles).
      * - **ThetaStar**
        - Any-angle path planner producing shorter paths with fewer
          waypoints.

   .. code-block:: yaml

      planner_server:
        ros__parameters:
          planner_plugins: ["GridBased"]
          GridBased:
            plugin: "nav2_navfn_planner/NavfnPlanner"
            tolerance: 0.5
            use_astar: true
            allow_unknown: true


Controller Plugins
-------------------

.. dropdown:: Available Controllers

   .. list-table::
      :header-rows: 1
      :widths: 20 80

      * - Plugin
        - Description
      * - **DWB**
        - Dynamic Window approach (default).  Scores trajectory samples
          against configurable critics.
      * - **MPPI**
        - Model Predictive Path Integral controller.  Generates
          smoother velocity profiles.
      * - **RPP**
        - Regulated Pure Pursuit.  Simple and robust for differential
          drive robots following a path.

   .. code-block:: yaml

      controller_server:
        ros__parameters:
          controller_plugins: ["FollowPath"]
          FollowPath:
            plugin: "dwb_core::DWBLocalPlanner"
            min_vel_x: 0.0
            max_vel_x: 0.26
            max_vel_theta: 1.0
            min_speed_xy: 0.0
            max_speed_xy: 0.26
            acc_lim_x: 2.5
            acc_lim_theta: 3.2


Costmap Configuration
----------------------

.. dropdown:: Costmap Layers

   Both the local and global costmaps are composed of **layers** that
   are combined to produce the final cost grid:

   .. list-table::
      :header-rows: 1
      :widths: 20 80

      * - Layer
        - Description
      * - **Static Layer**
        - Incorporates the map from ``map_server``.  Used only in the
          global costmap.
      * - **Obstacle Layer**
        - Adds obstacles detected by sensors (LiDAR, depth camera) in
          real time.
      * - **Inflation Layer**
        - Inflates obstacles by the robot's inscribed radius to ensure
          collision-free planning.
      * - **Voxel Layer**
        - 3D obstacle tracking using a voxel grid.  Used when the
          robot has 3D sensors.

   .. code-block:: yaml

      global_costmap:
        global_costmap:
          ros__parameters:
            update_frequency: 1.0
            publish_frequency: 1.0
            robot_radius: 0.22
            resolution: 0.05
            plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
            static_layer:
              plugin: "nav2_costmap_2d::StaticLayer"
              map_subscribe_transient_local: true
            obstacle_layer:
              plugin: "nav2_costmap_2d::ObstacleLayer"
              observation_sources: scan
              scan:
                topic: /scan
                max_obstacle_height: 2.0
                clearing: true
                marking: true
            inflation_layer:
              plugin: "nav2_costmap_2d::InflationLayer"
              cost_scaling_factor: 3.0
              inflation_radius: 0.55


AMCL Parameters
----------------

.. dropdown:: Key AMCL Settings

   AMCL (Adaptive Monte Carlo Localization) uses a particle filter to
   estimate the robot's pose on a known map:

   .. code-block:: yaml

      amcl:
        ros__parameters:
          min_particles: 500
          max_particles: 2000
          alpha1: 0.2          # rotation noise from rotation
          alpha2: 0.2          # rotation noise from translation
          alpha3: 0.2          # translation noise from translation
          alpha4: 0.2          # translation noise from rotation
          alpha5: 0.2          # translation noise (omni)
          base_frame_id: "base_footprint"
          global_frame_id: "map"
          odom_frame_id: "odom"
          scan_topic: /scan
          tf_broadcast: true
          set_initial_pose: true
          initial_pose:
            x: 0.0
            y: 0.0
            yaw: 0.0

   .. warning::

      If the robot's initial pose is not set correctly, AMCL may
      fail to converge and the robot will not localize properly.
      Always verify the initial pose in RViz before starting
      navigation.


Launching Nav2
====================================================

Nav2 provides the ``nav2_bringup`` package with ready-to-use launch
files for common configurations.


Launching with a Map
---------------------

.. dropdown:: Using nav2_bringup

   .. code-block:: console

      ros2 launch nav2_bringup bringup_launch.py \
          map:=/path/to/your/map.yaml \
          params_file:=/path/to/nav2_params.yaml \
          use_sim_time:=true

   This launch file starts all Nav2 servers, the lifecycle manager, the
   map server, and AMCL.

   .. tip::

      Always set ``use_sim_time:=true`` when running in simulation so
      that all nodes use the clock published by Gazebo rather than
      wall-clock time.


Launching in Simulation
------------------------

.. dropdown:: Connecting to Gazebo from L11

   Start the Gazebo simulation from L11 in one terminal:

   .. code-block:: console

      enpm605
      ros2 launch nav2_demo gazebo_launch.py

   In a second terminal, launch Nav2 with the simulation map:

   .. code-block:: console

      enpm605
      ros2 launch nav2_bringup bringup_launch.py \
          map:=$(ros2 pkg prefix nav2_demo)/share/nav2_demo/maps/sim_map.yaml \
          params_file:=$(ros2 pkg prefix nav2_demo)/share/nav2_demo/config/nav2_params.yaml \
          use_sim_time:=true

   In a third terminal, launch RViz with the Nav2 configuration:

   .. code-block:: console

      enpm605
      ros2 launch nav2_bringup rviz_launch.py

   .. note::

      The lifecycle manager will automatically configure and activate
      all Nav2 nodes in the correct order.  Watch the terminal output
      for ``[lifecycle_manager]: Managed nodes are active`` to confirm
      that the stack is ready.


Sending Navigation Goals Programmatically
====================================================

Nav2 provides a Python API for sending goals without using RViz.


Using NavigateToPose Action
----------------------------

.. dropdown:: Action Interface

   Nav2 exposes navigation through a ROS 2 action:

   - **Action name**: ``/navigate_to_pose``
   - **Action type**: ``nav2_msgs/action/NavigateToPose``
   - **Goal fields**: ``pose`` (``geometry_msgs/PoseStamped``),
     ``behavior_tree`` (optional BT XML path)

   You can send goals directly using an action client, but Nav2 also
   provides a convenience wrapper.


BasicNavigator Helper Class
-----------------------------

.. dropdown:: Using BasicNavigator

   The ``nav2_simple_commander`` package provides ``BasicNavigator``,
   a high-level Python API that wraps Nav2 action calls:

   .. code-block:: python

      import rclpy
      from nav2_simple_commander.robot_navigator import BasicNavigator
      from geometry_msgs.msg import PoseStamped


      def main():
          rclpy.init()
          navigator = BasicNavigator()

          # Wait for Nav2 to be active
          navigator.waitUntilNav2Active()

          # Set initial pose
          initial_pose = PoseStamped()
          initial_pose.header.frame_id = "map"
          initial_pose.header.stamp = navigator.get_clock().now().to_msg()
          initial_pose.pose.position.x = 0.0
          initial_pose.pose.position.y = 0.0
          initial_pose.pose.orientation.w = 1.0
          navigator.setInitialPose(initial_pose)

          # Create a goal pose
          goal = PoseStamped()
          goal.header.frame_id = "map"
          goal.header.stamp = navigator.get_clock().now().to_msg()
          goal.pose.position.x = 2.0
          goal.pose.position.y = 1.0
          goal.pose.orientation.w = 1.0

          # Navigate to the goal
          navigator.goToPose(goal)

          # Wait for task to complete
          while not navigator.isTaskComplete():
              feedback = navigator.getFeedback()
              if feedback:
                  print(f"ETA: {feedback.estimated_time_remaining.sec}s")

          # Check result
          result = navigator.getResult()
          if result == navigator.TaskResult.SUCCEEDED:
              print("Goal reached!")
          elif result == navigator.TaskResult.CANCELED:
              print("Goal canceled!")
          elif result == navigator.TaskResult.FAILED:
              print("Goal failed!")

          navigator.lifecycleShutdown()
          rclpy.shutdown()


      if __name__ == "__main__":
          main()


Waypoint Following
-------------------

.. dropdown:: FollowWaypoints

   ``BasicNavigator`` also supports following a sequence of waypoints:

   .. code-block:: python

      waypoints = []

      wp1 = PoseStamped()
      wp1.header.frame_id = "map"
      wp1.header.stamp = navigator.get_clock().now().to_msg()
      wp1.pose.position.x = 1.0
      wp1.pose.position.y = 0.0
      wp1.pose.orientation.w = 1.0
      waypoints.append(wp1)

      wp2 = PoseStamped()
      wp2.header.frame_id = "map"
      wp2.header.stamp = navigator.get_clock().now().to_msg()
      wp2.pose.position.x = 2.0
      wp2.pose.position.y = 1.5
      wp2.pose.orientation.w = 1.0
      waypoints.append(wp2)

      wp3 = PoseStamped()
      wp3.header.frame_id = "map"
      wp3.header.stamp = navigator.get_clock().now().to_msg()
      wp3.pose.position.x = 0.0
      wp3.pose.position.y = 0.0
      wp3.pose.orientation.w = 1.0
      waypoints.append(wp3)

      navigator.followWaypoints(waypoints)

      while not navigator.isTaskComplete():
          feedback = navigator.getFeedback()
          if feedback:
              print(f"Executing waypoint {feedback.current_waypoint + 1}/{len(waypoints)}")

   .. note::

      ``followWaypoints`` visits each waypoint in order.  The robot
      will plan and navigate to each waypoint sequentially.  If any
      waypoint fails, the navigation result will indicate failure.


Checking Navigation Results
-----------------------------

.. dropdown:: TaskResult Enum

   ``BasicNavigator.getResult()`` returns one of three values:

   - ``TaskResult.SUCCEEDED`` -- the robot reached the goal.
   - ``TaskResult.CANCELED`` -- the goal was canceled by the user or
     another node.
   - ``TaskResult.FAILED`` -- the planner or controller could not
     reach the goal (e.g., the goal is inside an obstacle).

   .. tip::

      Always check the result after navigation completes and implement
      appropriate error handling.  For production systems, consider
      retry logic or alternative goals when navigation fails.


Map Creation
====================================================

Creating maps is a prerequisite for using Nav2 with AMCL-based
localization.


SLAM Toolbox
--------------

.. dropdown:: Generating a Map

   SLAM Toolbox provides online and offline SLAM capabilities.  To
   create a map from sensor data:

   .. code-block:: console

      # Launch SLAM Toolbox in online async mode
      ros2 launch slam_toolbox online_async_launch.py \
          use_sim_time:=true

   Drive the robot around the environment (manually or with
   ``teleop_twist_keyboard``) while SLAM Toolbox builds the map.
   Visualize the growing map in RViz by adding the ``/map`` topic
   display.

   .. code-block:: console

      # In a separate terminal -- teleoperate the robot
      ros2 run teleop_twist_keyboard teleop_twist_keyboard


Saving Maps
-------------

.. dropdown:: Using map_saver

   Once the environment has been fully explored, save the map:

   .. code-block:: console

      ros2 run nav2_map_server map_saver_cli -f ~/enpm605_ws/maps/my_map

   This produces two files:

   - ``my_map.pgm`` -- the occupancy grid image (white = free, black =
     occupied, gray = unknown).
   - ``my_map.yaml`` -- metadata including resolution, origin, and
     thresholds.

   .. code-block:: yaml

      # Example my_map.yaml
      image: my_map.pgm
      mode: trinary
      resolution: 0.05
      origin: [-5.0, -5.0, 0.0]
      negate: 0
      occupied_thresh: 0.65
      free_thresh: 0.25

   .. tip::

      Save maps frequently during exploration.  If the robot's
      odometry drifts, loop closures may shift the map and earlier
      saves serve as backups.
