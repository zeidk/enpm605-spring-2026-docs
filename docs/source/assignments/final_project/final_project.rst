====================================================
Final Project: Search and Rescue
====================================================


Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - May 9, 2026, 11:59 PM EST
   * - **Total Points**
     - 100 points
   * - **Submission**
     - Canvas (zip the ``~/enpm605_ws/src/final_project/`` folder and
       submit as ``group<N>_final_project.zip``)
   * - **Collaboration**
     - Groups of 2.
   * - **Late Policy**
     - 10% deduction per calendar day, up to 3 days. Zero after 3 days.
   * - **Peer Review**
     - Final grade: 60% assignment grade + 40% peer review score.


.. dropdown:: Description
   :open:

   This is a **group project** (2 students per group). You will
   build a ROS 2 system that commands a ``rosbot`` to perform a
   **search and rescue mission** in a simulated disaster zone. The
   robot must:

   1. Navigate to a series of predefined **search zones** using Nav2.
   2. At each zone, call a **simulated detection service** (no
      vision -- a simple dictionary lookup) to check for survivors.
   3. If a survivor is found, **broadcast a TF frame** marking their
      location and call a **notification service** to report the find.
   4. Monitor a simulated **battery level** and return to base when
      the battery is low.
   5. Handle **navigation failures** with a recovery strategy
      (wait and retry, then skip).

   The robot's decision-making is orchestrated by a **behavior tree**
   built with ``py_trees`` and ``py_trees_ros``. All mission
   parameters (search zones, battery threshold, timeouts) are loaded
   from a **YAML parameter file**.


.. dropdown:: Learning Objectives
   :open:

   .. grid:: 1 2 2 2
       :gutter: 2

       .. grid-item-card:: Behavior Trees
           :class-card: sd-border-info

           Design and implement a multi-level behavior tree with
           conditions, actions, composites (Sequence and Selector),
           and decorators (Timeout). Understand ``memory=True`` vs
           ``memory=False`` for reactive and resuming behavior.

       .. grid-item-card:: Nav2 Integration
           :class-card: sd-border-info

           Use the ``NavigateToPose`` action to send the robot to
           goal poses on a known map. Handle navigation success,
           failure, and timeout within the behavior tree.

       .. grid-item-card:: Custom Services
           :class-card: sd-border-info

           Define and implement custom ``.srv`` interfaces
           (``DetectSurvivor`` and ``ReportSurvivor``). Call them
           from behavior tree action nodes using synchronous service
           clients.

       .. grid-item-card:: TF2 Frames
           :class-card: sd-border-info

           Broadcast static TF frames for discovered survivors
           relative to the ``map`` frame. Use ``tf2_ros`` to publish
           and verify transforms.

       .. grid-item-card:: Parameter Configuration
           :class-card: sd-border-info

           Load mission parameters (search zones, base station pose,
           battery threshold, navigation timeout) from a YAML file.
           Expose key values as launch arguments for runtime
           override.

       .. grid-item-card:: Launch File Integration
           :class-card: sd-border-info

           Write a Python launch file that starts all required nodes,
           loads the parameter file, and exposes launch arguments.
           Integrate with the Nav2 stack and Gazebo simulation.

   .. |rarr| unicode:: U+2192


.. dropdown:: Suggested Timeline
   :open:

   You have **two weeks** (April 27 |rarr| May 9). The schedule below
   is a suggestion; adjust based on your group's pace.

   .. list-table::
      :widths: 18 12 70
      :header-rows: 1
      :class: compact-table

      * - Period
        - Duration
        - Tasks
      * - **Days 1 to 3**
        - 3 days
        - Read the assignment carefully. Review Lectures 12 and 13
          (behavior trees, Nav2). Launch the simulation and confirm
          the map loads correctly. Create the package skeletons.
          Define the service interfaces. Implement the
          ``ZoneManager`` class and the simulated service servers
          (``DetectSurvivor`` and ``ReportSurvivor``).
      * - **Days 4 to 7**
        - 4 days
        - Implement the behavior tree leaf nodes: ``NavigateToZone``,
          ``NavigateToBase``, ``DetectSurvivor``, ``BroadcastSurvivorTF``,
          ``NotifyBase``, ``Wait``, ``SkipZone``, ``AdvanceZone``,
          ``LogNoDetection``. Implement condition nodes:
          ``CheckBattery``, ``ZonesRemaining``, ``IsSurvivorDetected``.
          Test each node individually.
      * - **Days 8 to 11**
        - 4 days
        - Assemble the full behavior tree in the entry point script.
          Write the launch file. Integrate with Nav2. Test the full
          pipeline end to end: all zones visited, survivors detected
          and reported, TF frames broadcast, battery return works.
      * - **Days 12 to 14**
        - 3 days
        - Write ``README.md``. Code quality pass (docstrings, type
          hints, comments, Ruff). Test edge cases (navigation
          failure, skip zone, low battery mid-mission). Remove cache
          directories. Package and submit.

----



.. toctree::
   :hidden:
   :maxdepth: 1
   :titlesonly:

   infrastructure
   requirements
   implementation_guide
   outputs
   submission
   rubric
