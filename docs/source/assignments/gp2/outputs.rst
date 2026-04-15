====================================================
Expected Output
====================================================

.. |rarr| unicode:: U+2192


Nominal Run (All Three Goals Succeed)
=====================================

The following shows an example of the expected log output when the
full system is running correctly and all three goals are reached.
Timestamps are abbreviated for readability. Exact numeric values
will vary with your gains.

.. code-block:: text

   [INFO] [navigate_to_goal_server]: NavigateToGoal server ready. Gains: k_rho=0.4, k_alpha=0.8, k_yaw=0.8
   [INFO] [navigate_to_goal_client]: Loaded 3 goals: [(5.00, 0.00, 0.00), (-2.50, 4.33, 2.09), (-2.50, -4.33, -2.09)]
   [INFO] [navigate_to_goal_client]: Waiting for action server...
   [INFO] [navigate_to_goal_client]: --- Sending goal 1/3: (5.00, 0.00, final_heading=0.00) ---
   [INFO] [navigate_to_goal_server]: Goal accepted: (5.00, 0.00, final_heading=0.00)
   [INFO] [navigate_to_goal_client]: Goal accepted.
   [INFO] [navigate_to_goal_server]: First odometry received. Control loop active.
   [INFO] [navigate_to_goal_client]: Feedback: pose=(1.52, 0.01, yaw=0.01) remaining=3.48
   [INFO] [navigate_to_goal_client]: Feedback: pose=(3.80, 0.01, yaw=0.01) remaining=1.20
   [INFO] [navigate_to_goal_server]: Goal reached: (5.00, 0.00, final_heading=0.00)
   [INFO] [navigate_to_goal_client]: Goal 1/3 succeeded. total_distance=5.04, elapsed_time=11.10s
   [INFO] [navigate_to_goal_client]: --- Sending goal 2/3: (-2.50, 4.33, final_heading=2.09) ---
   [INFO] [navigate_to_goal_server]: Goal accepted: (-2.50, 4.33, final_heading=2.09)
   [INFO] [navigate_to_goal_client]: Feedback: pose=(2.10, 1.85, yaw=2.18) remaining=6.20
   [INFO] [navigate_to_goal_client]: Feedback: pose=(-0.40, 3.10, yaw=2.11) remaining=2.41
   [INFO] [navigate_to_goal_server]: Goal reached: (-2.50, 4.33, final_heading=2.09)
   [INFO] [navigate_to_goal_client]: Goal 2/3 succeeded. total_distance=8.92, elapsed_time=18.40s
   [INFO] [navigate_to_goal_client]: --- Sending goal 3/3: (-2.50, -4.33, final_heading=-2.09) ---
   [INFO] [navigate_to_goal_server]: Goal accepted: (-2.50, -4.33, final_heading=-2.09)
   [INFO] [navigate_to_goal_client]: Feedback: pose=(-2.48, -0.10, yaw=-1.57) remaining=4.23
   [INFO] [navigate_to_goal_server]: Goal reached: (-2.50, -4.33, final_heading=-2.09)
   [INFO] [navigate_to_goal_client]: Goal 3/3 succeeded. total_distance=8.75, elapsed_time=18.20s
   [INFO] [navigate_to_goal_client]: ========================================
   [INFO] [navigate_to_goal_client]: Mission complete. All 3 goals reached.
   [INFO] [navigate_to_goal_client]:   Goal 1: total_distance=5.04, elapsed_time=11.10s
   [INFO] [navigate_to_goal_client]:   Goal 2: total_distance=8.92, elapsed_time=18.40s
   [INFO] [navigate_to_goal_client]:   Goal 3: total_distance=8.75, elapsed_time=18.20s
   [INFO] [navigate_to_goal_client]: ========================================


Cancellation Demonstration
==========================

Your submission must **demonstrate a working action cancel**: the
server must accept a cancel request mid-execution, stop the robot
immediately, finalize the goal with ``success=False``, and return
a result carrying whatever ``total_distance`` / ``elapsed_time``
accumulated before the cancel.

.. important::

   Because your action client in ``gp2.launch.py`` runs the three
   goals to completion without ever issuing a cancel itself, you
   demonstrate cancellation from a **separate terminal** using the
   ``ros2 action send_goal`` CLI tool. The CLI sends a cancel
   request to the server when you press ``Ctrl+C``.

**Reproduction steps:**

1. In terminal A, launch the simulation:

   .. code-block:: console

      ros2 launch rosbot_gazebo gp2_world.launch.py

2. In terminal B, run only the action server (not the full
   ``gp2.launch.py``, so the robot is not mid-mission):

   .. code-block:: console

      ros2 run group<N>_gp2 navigate_to_goal_server

3. In terminal C, send a long goal with ``--feedback`` so you can
   watch the robot drive toward it:

   .. code-block:: console

      ros2 action send_goal /navigate_to_goal \
          group<N>_gp2_interfaces/action/NavigateToGoal \
          "{goal_position: {x: 8.0, y: 0.0, z: 0.0}, final_heading: 0.0}" \
          --feedback

4. After two or three feedback messages (the robot is still
   driving), press ``Ctrl+C`` in terminal C. The CLI sends a
   cancel request to the server.

**Expected output in terminal C** (the CLI client):

.. code-block:: text

   Waiting for an action server to become available...
   Sending goal:
        goal_position: {x: 8.0, y: 0.0, z: 0.0}
        final_heading: 0.0
   Goal accepted with ID: 7e4a...
   Feedback:
        current_pose: { ... x: 0.48 ... }
        distance_remaining: 7.52
   Feedback:
        current_pose: { ... x: 1.62 ... }
        distance_remaining: 6.38
   Feedback:
        current_pose: { ... x: 2.85 ... }
        distance_remaining: 5.15
   ^C
   Canceling goal...
   Goal canceled.
   Result:
        success: false
        total_distance: 2.85
        elapsed_time: 5.80

**Expected output in terminal B** (the action server):

.. code-block:: text

   [INFO] [navigate_to_goal_server]: NavigateToGoal server ready. Gains: k_rho=0.4, k_alpha=0.8, k_yaw=0.8
   [INFO] [navigate_to_goal_server]: Goal accepted: (8.00, 0.00, final_heading=0.00)
   [INFO] [navigate_to_goal_server]: First odometry received. Control loop active.
   [INFO] [navigate_to_goal_server]: [position] pose=(0.48, 0.01, yaw=0.01) rho=7.52 cmd=(v=0.50, w=0.01)
   [INFO] [navigate_to_goal_server]: [position] pose=(1.62, 0.01, yaw=0.01) rho=6.38 cmd=(v=0.50, w=0.01)
   [INFO] [navigate_to_goal_server]: [position] pose=(2.85, 0.01, yaw=0.01) rho=5.15 cmd=(v=0.50, w=0.01)
   [WARN] [navigate_to_goal_server]: Cancel requested. Stopping the robot and finalizing the goal.
   [INFO] [navigate_to_goal_server]: Goal canceled: total_distance=2.85, elapsed_time=5.80s

**Grading criteria for the cancel demo:**

- The server logs that it received the cancel request.
- The server publishes a **zero-velocity** ``TwistStamped`` on
  ``/cmd_vel`` immediately after receiving the cancel (the robot
  visibly stops in Gazebo).
- The server calls ``goal_handle.canceled()`` (not ``succeed()``
  or ``abort()``).
- The returned result has ``success=False`` and carries the
  partial ``total_distance`` / ``elapsed_time`` accumulated up to
  the cancel point.

Include a screenshot or a recorded terminal log of this
demonstration **with your submission** (see :doc:`submission`).


Verification Commands
=====================

Use these commands to test individual components before running the
full system.

.. code-block:: console

   # 1. Launch the simulation (separate terminal)
   ros2 launch rosbot_gazebo gp2_world.launch.py

   # 2. Run the server only and send a single goal via the CLI
   ros2 run group<N>_gp2 navigate_to_goal_server
   ros2 action send_goal /navigate_to_goal \
       group<N>_gp2_interfaces/action/NavigateToGoal \
       "{goal_position: {x: 5.0, y: 0.0, z: 0.0}, final_heading: 0.0}" \
       --feedback

   # 3. Inspect the action interface
   ros2 action info /navigate_to_goal -t
   ros2 interface show group<N>_gp2_interfaces/action/NavigateToGoal

   # 4. Watch feedback and commands
   ros2 topic echo /cmd_vel
   ros2 topic echo /odometry/filtered --field pose.pose

   # 5. Launch the full system with custom tolerances
   ros2 launch group<N>_gp2 gp2.launch.py \
       goal_tolerance:=0.15 yaw_tolerance:=0.08

   # 6. Show launch arguments
   ros2 launch group<N>_gp2 gp2.launch.py --show-args
