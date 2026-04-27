====================================================
L13: Mapping and Navigation with Nav2
====================================================

Overview
--------

This lecture covers how a mobile robot builds a model of its
environment and uses that model to navigate autonomously. **Maps**
provide the spatial representation a robot needs to plan paths,
localize itself, and reason about the world. We focus on the
**occupancy grid**, the metric representation used throughout Nav2,
and on the standard ``map`` frame defined by REP 105. **SLAM**
(Simultaneous Localization and Mapping) builds an occupancy grid from
LiDAR data using ``slam_toolbox``: scan matching estimates incremental
motion, a pose graph stores the trajectory, and loop closure corrects
accumulated drift. Once a map is saved, **AMCL** (Adaptive Monte
Carlo Localization) localizes the robot against it using a particle
filter. Finally, **Nav2** orchestrates planning and control: global
planners (NavFn, Smac) and local controllers (DWB, Regulated Pure
Pursuit) operate on global and local **costmaps** to compute and
execute collision-free paths. Goals are sent through the
``NavigateToPose`` action -- either from RViz2 or programmatically
through the ``nav2_simple_commander`` API. All hands-on examples use
the ``rosbot_gazebo`` and ``nav_demo`` packages.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Distinguish metric, topological, and semantic map representations.
   - Explain the occupancy grid map representation and how LiDAR
     observations update it through Bayesian fusion.
   - Build a map with ``slam_toolbox``, save it with
     ``nav2_map_server``, and reload it later for AMCL-based
     localization.
   - Localize a robot against a known map using AMCL and a particle
     filter.
   - Describe the role of global and local costmaps, the inflation
     layer, and the robot footprint.
   - Distinguish global planners (NavFn, Smac Hybrid A*) from local
     controllers (DWB, Regulated Pure Pursuit).
   - Explain how Nav2 uses a behavior tree to orchestrate planning,
     control, and recovery behaviors.
   - Send navigation goals programmatically via the ``NavigateToPose``
     action API using ``nav2_simple_commander``.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:


   l13_lecture
   l13_exercises
   l13_quiz
   l13_references


Next Steps
----------

- In the next lecture, we will cover **Extra ROS Tools**:

  - Foxglove Studio for live and recorded data inspection
  - ROS bags (``ros2 bag record`` / ``play``) for capture and replay
  - The RQT framework and its plugins
  - Final project status check

- Complete the exercises from this lecture before the next class.
- Read the `Nav2 Configuration Guide
  <https://docs.nav2.org/configuration/index.html>`_ and skim the
  `Nav2 Behavior Trees
  <https://docs.nav2.org/behavior_trees/index.html>`_ documentation.
