====================================================================
L12: Namespaces, Remapping, Lifecycle Nodes, and Behavior Trees
====================================================================

Overview
--------

This lecture covers four topics that are essential for building
production-quality ROS 2 systems. **Namespaces** isolate multiple
instances of the same node by prefixing all their topics, services, and
parameters. **Remapping** lets you redirect individual names (node,
topic, service) at runtime without modifying source code. **Lifecycle
nodes** follow a standardized state machine (Unconfigured, Inactive,
Active, Finalized) that gives the system precise control over
initialization order, resource allocation, and shutdown. **Behavior
trees** organize robot behaviors into a modular, hierarchical structure
where leaf nodes (actions and conditions) do the work and composite
nodes (Sequences and Selectors) make the decisions. All hands-on
examples use the ``namespace_demo``, ``remapping_demo``,
``lifecycle_demo``, and ``bt_demo`` packages.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Apply namespaces to isolate multiple instances of the same node.
   - Remap node names, topic names, and parameters at runtime and from
     launch files.
   - Implement a lifecycle node in Python using ``rclpy_lifecycle``.
   - Perform manual state transitions via the CLI and verify node
     behavior in each state.
   - Explain the structure of a behavior tree: nodes, ticks, and return
     statuses.
   - Implement a robot behavior tree in Python using ``py_trees`` and
     ``py_trees_ros``.
   - Drive a robot to a goal in Gazebo using a BT with conditions,
     actions, decorators, and a recovery strategy.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:


   l12_lecture
   l12_exercises
   l12_quiz
   l12_references


Next Steps
----------

- In the next lecture, we will cover **Mapping and Navigation with
  Nav2**:

  - Occupancy grid maps and the ``map`` frame
  - SLAM with ``slam_toolbox``: building a map from LiDAR + odometry
  - Localization with AMCL against a saved map
  - The Nav2 stack: planner, controller, behavior tree, recovery
  - Sending navigation goals via RViz2 and the ``NavigateToPose`` action

- Complete the exercises from this lecture before the next class.
- Read `Nav2 Getting Started
  <https://docs.nav2.org/getting_started/index.html>`_ and skim
  `Nav2 Concepts
  <https://docs.nav2.org/concepts/index.html>`_.
