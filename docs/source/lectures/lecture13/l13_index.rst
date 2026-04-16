====================================================
L13: Behavior Trees and Project Integration
====================================================

Overview
--------

This final lecture introduces **Behavior Trees (BTs)** as a powerful,
modular decision-making framework for robotic systems. You will learn
BT fundamentals -- node types, the tick mechanism, and composites --
then build trees in Python using the ``py_trees`` library. The lecture
covers shared data communication via the **Blackboard**, and shows
how to integrate BTs with ROS 2 using ``py_trees_ros``. The capstone
demonstration brings together concepts from the entire course:
lifecycle node management, Nav2 goal dispatch, and sensor monitoring,
all coordinated by a single behavior tree. This lecture uses the
``bt_demo`` and ``integration_demo`` packages.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Explain what behavior trees are and why they are preferred over
     finite state machines for complex robotic decision-making.
   - Identify and describe the core BT node types: sequence, fallback,
     decorator, condition, and action.
   - Build and tick a behavior tree using the ``py_trees`` Python library.
   - Use the Blackboard for inter-behavior data sharing.
   - Wrap ROS 2 publishers, subscribers, action clients, and service
     clients as BT behaviors using ``py_trees_ros``.
   - Design and implement a complete integration demo that uses a
     behavior tree to coordinate lifecycle nodes, Nav2 goals, and
     sensor-driven reactions.
   - Debug behavior trees using visualization tools and logging.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l13_lecture
   l13_exercises
   l13_quiz
   l13_references


Course Wrap-Up
--------------

Congratulations on completing ENPM605: Python Applications for Robotics!

Over the course of thirteen lectures you have progressed from core
Python programming concepts to building fully integrated robotic
systems:

- **Lectures 1-7** -- Python fundamentals: data types, control flow,
  functions, OOP, decorators, error handling, file I/O, and testing.
- **Lectures 8-9** -- ROS 2 foundations: nodes, topics, publishers,
  subscribers, QoS, parameters, executors, and callback groups.
- **Lecture 10** -- Services, actions, and launch files.
- **Lecture 11** -- Simulation with Gazebo and sensor integration.
- **Lecture 12** -- Nav2 navigation and lifecycle (managed) nodes.
- **Lecture 13** -- Behavior trees and full-system integration.

**Final steps:**

- Complete and submit **Group Project 4 (GP4)**, which synthesizes
  the concepts from Lectures 8-13 into a single integrated robotic
  application.
- Review lecture references and recommended readings for topics you
  want to explore further.
- The skills you have built -- distributed systems design, sensor
  integration, autonomous navigation, and decision-making with
  behavior trees -- form the foundation for advanced robotics work
  in research and industry.
