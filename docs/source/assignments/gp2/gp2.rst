====================================================
GP 2: Action-Based Goal Navigation
====================================================


Overview
========

.. list-table::
   :widths: 30 70
   :class: compact-table

   * - **Due Date**
     - April 24, 2026, 11:59 PM EST
   * - **Total Points**
     - 50 points
   * - **Submission**
     - Canvas (zip the ``~/enpm605_ws/src/gp2/`` folder and submit
       as ``group<N>_gp2.zip``)
   * - **Collaboration**
     - Groups of 2 (or 3).
   * - **Late Policy**
     - 10% deduction per calendar day, up to 3 days. Zero after 3 days.
   * - **Peer Review**
     - Final grade: 60% assignment grade + 40% peer review score.


.. dropdown:: Description
   :open:

   This is a **group project** (2 or 3 students per group). You will
   wrap the two-phase **proportional controller** from Lecture 11
   inside a ROS 2 **action server**, and drive a simulated ``rosbot``
   to three goals sequentially using an **action client**. The
   controller logic (position + orientation, 20 Hz control loop) is
   already written for you in
   ``~/enpm605_ws/src/lecture11/robot_control_demo``. Your job is
   to port it into an action server, wire it to a client, and submit
   the result.



.. dropdown:: Learning Objectives
   :open:

   .. grid:: 1 2 2 2
       :gutter: 2

       .. grid-item-card:: Custom Action Interfaces
           :class-card: sd-border-info

           Define a ``.action`` file with goal, feedback, and result
           sections. Generate Python bindings via
           ``rosidl_generate_interfaces`` in a CMake package.

       .. grid-item-card:: Action Servers
           :class-card: sd-border-info

           Implement a long-running goal with an
           ``ActionServer``: accept/reject logic, cancellation
           support, periodic feedback publishing, and a final result
           on success or failure.

       .. grid-item-card:: Action Clients
           :class-card: sd-border-info

           Use an ``ActionClient`` to send goals asynchronously,
           handle goal-response, feedback, and result callbacks, and
           **chain** multiple goals sequentially (wait for each result
           before sending the next).

       .. grid-item-card:: Embedded Control Logic
           :class-card: sd-border-info

           Port the two-phase proportional controller (position then
           orientation) into the action server's execution callback
           so that goal progress and tolerance checks drive the
           feedback/result lifecycle.

       .. grid-item-card:: Parameter Configuration
           :class-card: sd-border-info

           Load three goal poses (``x``, ``y``, ``final_heading``)
           from a YAML parameter file at launch time, organized as
           named blocks (``goal1``, ``goal2``, ``goal3``) and
           accessed via dot-namespaced parameter names.

       .. grid-item-card:: Launch File Integration
           :class-card: sd-border-info

           Write a Python launch file that starts the action server
           and the action client together, loads the goals YAML file
           into the client node, and exposes launch arguments for the
           controller gains and tolerances.

   .. |rarr| unicode:: U+2192


.. dropdown:: Suggested Timeline
   :open:

   You have **one week** (April 16 |rarr| April 23). The schedule below
   is a suggestion; adjust based on your group's pace.

   .. list-table::
      :widths: 18 12 70
      :header-rows: 1
      :class: compact-table

      * - Period
        - Duration
        - Tasks
      * - **Days 1 to 2**
        - 2 days
        - Read the assignment carefully. Review Lecture 10
          (``action_demo``, ``parameters_demo``) and Lecture 11
          (``robot_control_demo/p_controller_demo``). Launch the GP2
          world (``rosbot_gazebo gp2_world.launch.py``) and confirm
          the three floor markers are visible. Create the two package
          skeletons. Define and build ``group<N>_gp2_interfaces``.
      * - **Days 3 to 4**
        - 2 days
        - Implement the action server: port the two-phase P-controller
          into the ``execute_callback``. Test with a hardcoded goal
          using ``ros2 action send_goal`` from the CLI.
      * - **Days 5 to 6**
        - 2 days
        - Implement the action client: read goals from parameters,
          send goals sequentially, handle feedback and results. Write
          the launch file. Test the full pipeline end to end.
      * - **Day 7**
        - 1 day
        - Write ``README.md``. Code quality pass (docstrings, type
          hints, comments, Ruff). Remove cache directories. Package
          and submit.

----



.. toctree::
   :hidden: 
   :maxdepth: 1
   :titlesonly:

   gp2_infrastructure
   gp2_requirements
   outputs
   submission
   rubric
