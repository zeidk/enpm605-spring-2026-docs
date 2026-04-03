====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 12: Nav2 and Lifecycle
Nodes, including the lifecycle state machine, transition callbacks,
lifecycle CLI tools, Nav2 architecture, planner and controller plugins,
costmap layers, AMCL, the ``BasicNavigator`` API, waypoint following,
and map creation with SLAM Toolbox.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement
     is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What is the correct order of primary states when bringing a
   lifecycle node from construction to full operation?

   A. Unconfigured --> Active --> Inactive --> Finalized

   B. Unconfigured --> Inactive --> Active --> Finalized

   C. Inactive --> Unconfigured --> Active --> Finalized

   D. Active --> Inactive --> Unconfigured --> Finalized

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Unconfigured --> Inactive --> Active --> Finalized.

   A lifecycle node starts in the **Unconfigured** state after
   construction.  The ``configure`` transition moves it to **Inactive**,
   where resources are allocated but processing has not started.  The
   ``activate`` transition moves it to **Active**, where callbacks fire
   and data flows.  The ``shutdown`` transition from any state moves
   it to **Finalized**.


.. admonition:: Question 2
   :class: hint

   What happens when a lifecycle publisher publishes a message while
   the node is in the Inactive state?

   A. The message is queued and delivered when the node becomes Active.

   B. The message is silently dropped.

   C. A ``RuntimeError`` is raised.

   D. The message is published normally because publishers are
      independent of node state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The message is silently dropped.

   A lifecycle publisher created with ``create_lifecycle_publisher``
   is automatically disabled when the node is not in the Active state.
   Any messages published while the node is Inactive or Unconfigured
   are silently discarded.  This is by design -- it prevents partially
   configured nodes from emitting data that downstream consumers might
   misinterpret.


.. admonition:: Question 3
   :class: hint

   Which Nav2 component is responsible for computing a global path from
   the robot's current position to the goal?

   A. Controller Server

   B. Behavior Server

   C. Planner Server

   D. BT Navigator

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Planner Server.

   The **Planner Server** hosts global planning plugins (e.g.,
   ``NavfnPlanner``, ``SmacPlanner2D``) that compute a collision-free
   path from the robot's current pose to the goal pose on the global
   costmap.  The **Controller Server** follows that path by generating
   velocity commands, the **Behavior Server** handles recovery
   behaviors, and the **BT Navigator** orchestrates all three.


.. admonition:: Question 4
   :class: hint

   Which costmap layer is responsible for expanding obstacles to
   account for the robot's physical footprint?

   A. Static Layer

   B. Obstacle Layer

   C. Voxel Layer

   D. Inflation Layer

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- Inflation Layer.

   The **Inflation Layer** expands the cost around obstacles by the
   robot's inscribed radius (and beyond, with decaying cost).  This
   ensures the planner and controller keep the robot's center far
   enough from obstacles to avoid physical collisions.  The cost
   decreases with distance from the obstacle according to the
   ``cost_scaling_factor`` parameter.


.. admonition:: Question 5
   :class: hint

   What is the purpose of ``navigator.waitUntilNav2Active()`` in the
   ``BasicNavigator`` API?

   A. It sends a goal to Nav2 and waits for it to be accepted.

   B. It blocks until all Nav2 lifecycle nodes have transitioned to
      the Active state.

   C. It starts the Nav2 lifecycle manager.

   D. It publishes the robot's initial pose to AMCL.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It blocks until all Nav2 lifecycle nodes have transitioned
   to the Active state.

   ``waitUntilNav2Active()`` monitors the lifecycle states of the Nav2
   servers and blocks the calling thread until all managed nodes are
   Active and ready to accept goals.  This prevents the script from
   sending navigation goals before the stack is fully initialized,
   which would result in action server timeouts or rejected goals.


.. admonition:: Question 6
   :class: hint

   What does AMCL use to localize the robot on a known map?

   A. Visual odometry from a camera.

   B. A particle filter with laser scan data.

   C. GPS coordinates matched to the map frame.

   D. Wheel encoder dead reckoning only.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A particle filter with laser scan data.

   AMCL (Adaptive Monte Carlo Localization) maintains a set of
   particles, each representing a hypothesis about the robot's pose.
   It uses laser scan data to compute the likelihood of each particle
   by comparing scan readings against the expected readings from the
   static map.  Particles with high likelihood are resampled, causing
   the particle cloud to converge on the robot's true position.


.. admonition:: Question 7
   :class: hint

   Which ``ros2 lifecycle`` command triggers the transition from
   Unconfigured to Inactive?

   A. ``ros2 lifecycle set /node_name activate``

   B. ``ros2 lifecycle set /node_name configure``

   C. ``ros2 lifecycle set /node_name cleanup``

   D. ``ros2 lifecycle set /node_name startup``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``ros2 lifecycle set /node_name configure``.

   The ``configure`` transition moves a lifecycle node from the
   **Unconfigured** state to the **Inactive** state.  During this
   transition, the ``on_configure`` callback is invoked, which is
   where the node should allocate resources, create publishers and
   subscribers, and load parameters.  The ``activate`` command would
   then move it from Inactive to Active.


.. admonition:: Question 8
   :class: hint

   What two files are produced when saving a map with
   ``map_saver_cli``?

   A. ``map.png`` and ``map.json``

   B. ``map.pgm`` and ``map.yaml``

   C. ``map.bmp`` and ``map.xml``

   D. ``map.jpg`` and ``map.toml``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``map.pgm`` and ``map.yaml``.

   The ``map_saver_cli`` tool saves the occupancy grid as a PGM
   (Portable Gray Map) image file where white pixels are free space,
   black pixels are obstacles, and gray pixels are unknown.  The
   accompanying YAML file contains metadata: the image filename,
   resolution (meters per pixel), origin coordinates, and the
   occupied/free probability thresholds.


----


True/False
==========

.. admonition:: Question 9
   :class: hint

   **True or False:** A lifecycle node can be transitioned directly from
   the Unconfigured state to the Active state without first going
   through the Inactive state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The lifecycle state machine does not allow skipping states.  A node
   must follow the sequence Unconfigured --> Inactive --> Active.  The
   ``configure`` transition must succeed before ``activate`` can be
   called.  Attempting to activate a node that is in the Unconfigured
   state will result in an error because the transition is not valid
   from that state.


.. admonition:: Question 10
   :class: hint

   **True or False:** All Nav2 servers (planner, controller, behavior,
   map server, AMCL) are lifecycle nodes managed by a single lifecycle
   manager.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   Nav2 uses the ``nav2_lifecycle_manager`` to coordinate the startup
   and shutdown of all its server nodes.  The lifecycle manager
   transitions each node through configure and activate in a defined
   order, and monitors their health using bond connections.  This
   ensures deterministic startup and enables coordinated recovery if
   any node crashes.


.. admonition:: Question 11
   :class: hint

   **True or False:** The ``on_shutdown`` callback can only be called
   from the Inactive state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The ``shutdown`` transition can be triggered from **any** primary
   state (Unconfigured, Inactive, or Active).  It always moves the
   node to the Finalized state.  This allows a node to be shut down
   cleanly regardless of what state it is currently in.


.. admonition:: Question 12
   :class: hint

   **True or False:** The ``followWaypoints`` method in
   ``BasicNavigator`` plans and executes all waypoints simultaneously
   in parallel.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ``followWaypoints`` visits each waypoint **sequentially** in the
   order they are provided.  The robot navigates to the first waypoint,
   waits until it arrives (or fails), then proceeds to the second
   waypoint, and so on.  There is no parallel execution of waypoints.


.. admonition:: Question 13
   :class: hint

   **True or False:** Setting ``use_sim_time: true`` in the Nav2
   parameter file causes all Nav2 nodes to use the clock published by
   the simulator instead of wall-clock time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   When ``use_sim_time`` is set to ``true``, ROS 2 nodes subscribe to
   the ``/clock`` topic (published by the simulator, e.g., Gazebo)
   and use that as their time source.  This is essential for
   simulation because the simulator's clock may run faster or slower
   than real time, and all nodes must agree on the same time source
   for transforms, planning, and control to work correctly.


----


Essay
=====

.. admonition:: Question 14
   :class: hint

   Explain why lifecycle nodes are important in the context of Nav2.
   Describe what problems would arise if Nav2 servers were implemented
   as standard (non-lifecycle) nodes.

.. dropdown:: Answer
   :class-container: sd-border-success

   Lifecycle nodes are critical to Nav2 because they provide
   **deterministic startup ordering** and **coordinated state
   management** across the many servers that compose the navigation
   stack.  Without lifecycle nodes, Nav2 servers would begin processing
   as soon as they are constructed, leading to race conditions -- for
   example, the planner server might attempt to plan before the map
   server has loaded the map, or the controller server might try to
   follow a path before AMCL has converged on a localization estimate.

   Lifecycle nodes solve this by requiring each server to go through
   ``configure`` (load parameters, create publishers) and ``activate``
   (begin processing) as separate steps orchestrated by the lifecycle
   manager.  This also enables **health monitoring** through bond
   connections -- if a server crashes, the lifecycle manager can
   detect the failure and attempt recovery by reconfiguring and
   reactivating the affected node.  Additionally, lifecycle nodes
   support **graceful shutdown**, allowing the system to deactivate
   and clean up resources in a controlled order rather than
   terminating abruptly.


.. admonition:: Question 15
   :class: hint

   Describe the roles of the three main costmap layers (static,
   obstacle, inflation) and explain how they work together to enable
   safe autonomous navigation.

.. dropdown:: Answer
   :class-container: sd-border-success

   The **static layer** incorporates the pre-built occupancy grid map
   loaded by the map server.  It provides the baseline layout of the
   environment -- walls, permanent furniture, and known obstacles.
   This layer is initialized once and does not change unless a new map
   is loaded.

   The **obstacle layer** adds real-time obstacle information from
   sensors such as LiDAR or depth cameras.  It marks cells as occupied
   when sensor readings detect an obstacle and clears cells when
   sensor readings pass through previously marked space.  This allows
   the robot to react to dynamic obstacles that are not present in the
   static map.

   The **inflation layer** expands the cost around every occupied cell
   outward by the robot's inscribed radius (at minimum) with a
   decaying cost function.  This creates a buffer zone around obstacles
   so the planner generates paths that keep the robot's center of mass
   far enough away to prevent physical collisions.

   Together, these layers compose the final costmap: the static layer
   provides known structure, the obstacle layer adds real-time
   perception, and the inflation layer ensures planned paths account
   for the robot's physical size.  The planner and controller both use
   this combined costmap to make safe navigation decisions.


.. admonition:: Question 16
   :class: hint

   Compare and contrast the ``goToPose`` and ``followWaypoints``
   methods in ``BasicNavigator``.  When would you use each one?

.. dropdown:: Answer
   :class-container: sd-border-success

   ``goToPose`` sends a single navigation goal to the Nav2 stack.  The
   planner computes a path from the robot's current position to the
   goal, and the controller follows that path until the robot arrives.
   This method is appropriate when the robot needs to reach one
   specific destination, such as navigating to a charging station or
   responding to a service request at a particular location.

   ``followWaypoints`` accepts a list of poses and visits each one
   sequentially.  Internally, it uses the ``FollowWaypoints`` action
   server, which plans and navigates to each waypoint in order.  This
   method is appropriate for patrol routes, inspection tasks, or any
   scenario where the robot must visit multiple locations in a defined
   sequence.

   The key difference is that ``goToPose`` is a single-goal operation
   while ``followWaypoints`` manages a sequence of goals with built-in
   progress tracking (current waypoint index in feedback).
   ``followWaypoints`` also handles the transition between waypoints
   automatically, whereas using ``goToPose`` in a loop would require
   the developer to manage sequencing, error handling between
   waypoints, and re-planning manually.
