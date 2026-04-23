====================================================
Assignments
====================================================

Overview
--------

Assignments in ENPM605 are programming exercises designed to reinforce the concepts covered in lectures. They come in two forms: **individual assignments**, where you work alone to demonstrate your understanding of core Python concepts, and **team projects**, where you collaborate with your peers to build larger robotics applications. Each assignment builds a complete Python application that applies core language features to a robotics-related problem. You will practice writing clean, modular, well-documented code while following professional software engineering standards.

Guidelines
----------

- **Individual assignments** must be completed independently. Collaboration and AI tools are not permitted.
- **Team projects** are completed in assigned groups. AI tools are permitted with proper documentation of their use.
- Follow the project structure specified in each assignment. Submissions that do not match the required structure will receive deductions.
- All code must include **type hints**, **Google-style docstrings**, and **inline comments** for non-obvious logic.
- Ensure **Ruff** is enabled in VS Code and that no linting errors or warnings appear in your Python files before submitting.
- Review the **Pre-Submission Checklist** included in each assignment before uploading to Canvas.
- Late submissions are penalized at 10% per calendar day, up to 3 days. Submissions beyond 3 days receive a zero.
- Team projects include **peer reviews**. Your final grade on team deliverables is based on 60% assignment grade and 40% peer review scores.


Schedule
--------

.. list-table::
   :widths: 12 30 58
   :header-rows: 1
   :class: compact-table

   * - Assignment
     - Title
     - Summary
   * - RWA 1
     - Python Fundamentals
     - Individual assignment. Apply core Python concepts (variables,
       control flow, functions, data structures) to solve a set of
       programming exercises.
   * - RWA 2
     - Object-Oriented Programming
     - Individual assignment. Design and implement Python classes using
       OOP principles (encapsulation, inheritance, polymorphism,
       composition) to model a robotics-related domain.
   * - GP 1
     - ROS 2 Pub/Sub System
     - Group project. Build a multi-node ROS 2 system with publishers,
       subscribers, custom messages, parameters, and a launch file.
   * - GP 2
     - Action-Based Goal Navigation
     - Group project. Wrap a proportional controller in a ROS 2 action
       server and drive a simulated rosbot to three sequential goals
       using an action client. Define a custom action interface, handle
       feedback and cancellation, and load goals from a YAML parameter
       file.
   * - Final Project
     - Search and Rescue
     - Group project. Build a behavior tree (``py_trees``) that
       commands a rosbot to navigate search zones using Nav2, call
       simulated detection and reporting services, broadcast TF frames
       for found survivors, monitor a simulated battery, and handle
       navigation failures with recovery strategies.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :hidden:

   rwa1
   rwa2
   gp1/gp1
   gp2/gp2
   final_project/final_project
