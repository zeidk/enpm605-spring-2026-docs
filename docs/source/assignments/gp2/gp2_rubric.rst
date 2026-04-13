====================================================
Expected Output, Submission, and Grading Rubric
====================================================

.. |rarr| unicode:: U+2192


Expected Terminal Output
========================

The following shows an example of the expected log output when the full
system is running correctly. Timestamps are abbreviated for readability.

.. code-block:: text

   [INFO] [p_controller]: ProportionalController started — gains: k_rho=0.4, k_alpha=0.8, k_yaw=0.8
   [INFO] [p_controller]: No initial goal — waiting for goal on 'goal_pose' topic.
   [INFO] [aruco_detector]: ArUco detector started: image=/oak/rgb/color, info=/oak/stereo/camera_info, dict=DICT_5X5_250, marker_size=0.194 m
   [INFO] [aruco_detector]: Waiting for camera_info...
   [INFO] [aruco_detector]: Camera intrinsics received
   [INFO] [marker_navigator]: Loaded 3 waypoints from parameters.
   [INFO] [marker_navigator]: --- Waypoint 1/3: (2.00, 0.00, yaw=0.00) ---
   [INFO] [marker_navigator]: Publishing goal: (2.00, 0.00, yaw=0.00)
   [INFO] [p_controller]: New goal received: (2.00, 0.00, yaw=0.00)
   [INFO] [p_controller]: First odometry message received — control loop active.
   [INFO] [p_controller]: [position] pose=(0.15, 0.01, yaw=0.02) rho=1.85 alpha=0.01 cmd=(v=0.50, w=0.01)
   [INFO] [p_controller]: [position] pose=(0.62, 0.01, yaw=0.01) rho=1.38 alpha=0.00 cmd=(v=0.50, w=0.00)
   [INFO] [p_controller]: [position] pose=(1.43, 0.01, yaw=0.01) rho=0.57 alpha=-0.01 cmd=(v=0.23, w=-0.01)
   [INFO] [p_controller]: [orientation] yaw=0.03 goal_yaw=0.00 error=-0.03 cmd=(w=-0.02)
   [INFO] [p_controller]: Goal reached: (2.00, 0.00, yaw=0.00)
   [INFO] [marker_navigator]: Goal reached. Waiting for marker detection...
   [INFO] [aruco_detector]: Detected markers: [2]
   [INFO] [marker_navigator]: Detected aruco_marker_2 at odom position: (3.98, 0.03)
   [INFO] [marker_navigator]: --- Waypoint 2/3: (0.00, 2.00, yaw=1.57) ---
   [INFO] [marker_navigator]: Publishing goal: (0.00, 2.00, yaw=1.57)
   [INFO] [p_controller]: New goal received: (0.00, 2.00, yaw=1.57)
   [INFO] [p_controller]: [position] pose=(1.98, 0.02, yaw=0.01) rho=2.80 alpha=2.50 cmd=(v=0.50, w=1.00)
   [INFO] [p_controller]: [position] pose=(0.65, 1.21, yaw=1.42) rho=0.94 alpha=0.14 cmd=(v=0.38, w=0.11)
   [INFO] [p_controller]: [orientation] yaw=1.53 goal_yaw=1.57 error=0.04 cmd=(w=0.03)
   [INFO] [p_controller]: Goal reached: (0.00, 2.00, yaw=1.57)
   [INFO] [marker_navigator]: Goal reached. Waiting for marker detection...
   [INFO] [aruco_detector]: Detected markers: [4]
   [INFO] [marker_navigator]: Detected aruco_marker_4 at odom position: (0.02, 3.97)
   [INFO] [marker_navigator]: --- Waypoint 3/3: (0.00, -2.00, yaw=-1.57) ---
   [INFO] [marker_navigator]: Publishing goal: (0.00, -2.00, yaw=-1.57)
   [INFO] [p_controller]: New goal received: (0.00, -2.00, yaw=-1.57)
   [INFO] [p_controller]: [position] pose=(-0.01, 1.95, yaw=1.56) rho=3.95 alpha=-1.57 cmd=(v=0.50, w=-1.00)
   [INFO] [p_controller]: [position] pose=(0.03, -1.38, yaw=-1.54) rho=0.62 alpha=-0.05 cmd=(v=0.25, w=-0.04)
   [INFO] [p_controller]: [orientation] yaw=-1.54 goal_yaw=-1.57 error=-0.03 cmd=(w=-0.02)
   [INFO] [p_controller]: Goal reached: (0.00, -2.00, yaw=-1.57)
   [INFO] [marker_navigator]: Goal reached. Waiting for marker detection...
   [INFO] [aruco_detector]: Detected markers: [5]
   [INFO] [marker_navigator]: Detected aruco_marker_5 at odom position: (-0.01, -4.02)
   [INFO] [marker_navigator]: ========================================
   [INFO] [marker_navigator]: All waypoints visited. Marker summary:
   [INFO] [marker_navigator]:   aruco_marker_2 -> odom: (3.98, 0.03)
   [INFO] [marker_navigator]:   aruco_marker_4 -> odom: (0.02, 3.97)
   [INFO] [marker_navigator]:   aruco_marker_5 -> odom: (-0.01, -4.02)
   [INFO] [marker_navigator]: Centroid: (1.33, -0.01)
   [INFO] [marker_navigator]: ========================================
   [INFO] [marker_navigator]: Navigating to centroid: (1.33, -0.01, yaw=0.00)
   [INFO] [p_controller]: New goal received: (1.33, -0.01, yaw=0.00)
   [INFO] [p_controller]: [position] pose=(0.01, -1.98, yaw=-1.56) rho=2.31 alpha=2.15 cmd=(v=0.50, w=1.00)
   [INFO] [p_controller]: [position] pose=(1.12, -0.22, yaw=0.05) rho=0.28 alpha=-0.68 cmd=(v=0.11, w=-0.55)
   [INFO] [p_controller]: [orientation] yaw=0.04 goal_yaw=0.00 error=-0.04 cmd=(w=-0.03)
   [INFO] [p_controller]: Goal reached: (1.33, -0.01, yaw=0.00)
   [INFO] [marker_navigator]: ========================================
   [INFO] [marker_navigator]: Mission complete! Robot at centroid (1.33, -0.01).
   [INFO] [marker_navigator]: ========================================


**Error handling example** (marker not detected at a waypoint):

.. code-block:: text

   [INFO] [marker_navigator]: Goal reached. Waiting for marker detection...
   [WARN] [marker_navigator]: TF lookup failed for candidate marker IDs. Retrying (1/3)...
   [WARN] [marker_navigator]: TF lookup failed for candidate marker IDs. Retrying (2/3)...
   [INFO] [aruco_detector]: Detected markers: [4]
   [INFO] [marker_navigator]: Detected aruco_marker_4 at odom position: (0.02, 3.97)


Verification Commands
=====================

Use these commands to test individual components before running the full
system.

.. code-block:: console

   # Verify TF frames are being broadcast
   ros2 run tf2_tools view_frames   # generates frames.pdf
   ros2 run tf2_ros tf2_echo odom aruco_marker_2

   # Verify the P-controller accepts goals
   ros2 topic pub /goal_pose geometry_msgs/msg/PoseStamped \
       "{header: {frame_id: 'odom'}, pose: {position: {x: 2.0, y: 0.0}, \
       orientation: {w: 1.0}}}" --once

   # Check that goal_reached fires
   ros2 topic echo /goal_reached

   # List detected markers
   ros2 topic echo /tf --field transforms.child_frame_id

   # Launch with custom tolerances
   ros2 launch group<N>_gp2 gp2.launch.py goal_tolerance:=0.15 yaw_tolerance:=0.08

   # Show launch arguments
   ros2 launch group<N>_gp2 gp2.launch.py --show-args


----


.. dropdown:: Pre-Submission Checklist
   :open:

   **Functionality**

   - |box| ``robot_control_demo`` and ``frame_demo`` are built in the workspace.
   - |box| Your package builds: ``colcon build --packages-select group<N>_gp2``
   - |box| The system launches: ``ros2 launch group<N>_gp2 gp2.launch.py``
   - |box| The robot navigates to all three waypoints autonomously.
   - |box| At each waypoint, a marker is detected and its odom-frame position is logged.
   - |box| The centroid is computed and logged correctly.
   - |box| The robot navigates to the centroid as the final step.
   - |box| TF lookup errors are handled gracefully (retries, fallback).
   - |box| Launch arguments work: ``--show-args`` and override.
   - |box| Parameters load from ``waypoints.yaml``.

   **Documentation**

   - |box| ``README.md`` includes all required sections.
   - |box| TF tree (``frames.pdf``) is included and annotated.

   **Code Quality**

   - |box| Type hints on all methods.
   - |box| Google-style docstrings on all classes and methods.
   - |box| Comments explain TF lookup strategy and state machine logic.
   - |box| No linting errors (Ruff).

   **Packaging**

   - |box| Removed ``__pycache__/``, ``*.pyc``, ``.ruff_cache/``.
   - |box| ZIP file is named ``group<N>_gp2.zip``.
   - |box| ZIP contains the package folder.

   .. |box| unicode:: U+2610


.. dropdown:: Submission
   :open:

   - Submit a ZIP file named ``group<N>_gp2.zip`` on Canvas (e.g.,
     ``group3_gp2.zip``).
   - The ZIP must contain the package folder (``group<N>_gp2/``) with
     all source files, launch files, config files, and ``README.md``.
   - The ZIP must not contain ``build/``, ``install/``, ``log/``,
     ``__pycache__/``, or ``.pyc`` files.
   - Both group members must submit the same ZIP file on Canvas.


----


Grading Rubric
==============

This rubric details how the 50 points are allocated.

.. list-table::
   :widths: 42 6 52
   :header-rows: 1
   :class: compact-table

   * - Component
     - Pts
     - Criteria
   * - **Navigator Node -- Waypoint Sequencing (12 pts)**
     -
     -
   * - Parameter loading
     - 3
     - Waypoints loaded from ``config/waypoints.yaml`` using
       ``self.get_parameter()``. Arrays validated for equal length.
       Number of waypoints logged at startup.
   * - Goal publishing
     - 3
     - Each waypoint is correctly converted to a ``PoseStamped``
       (including yaw-to-quaternion conversion) and published to
       ``/goal_pose``.
   * - Goal completion handling
     - 3
     - Node subscribes to ``/goal_reached`` and correctly waits for
       ``Bool(data=True)`` before proceeding to marker detection.
       Does not race ahead or miss the signal.
   * - State sequencing
     - 3
     - Waypoints are visited in order. The node transitions cleanly
       through states: navigate |rarr| detect |rarr| navigate |rarr|
       ... |rarr| centroid |rarr| done. No deadlocks or infinite loops.
   * - **Navigator Node -- TF2 Frame Lookups (14 pts)**
     -
     -
   * - Buffer and listener setup
     - 3
     - ``tf2_ros.Buffer`` and ``TransformListener`` are correctly
       initialized in ``__init__``. The listener is connected to the
       node so it receives TF data.
   * - Marker discovery
     - 4
     - The node dynamically determines which ``aruco_marker_<id>``
       frame is visible at the current waypoint (does not hardcode
       marker IDs). Approach is documented in code comments.
   * - ``lookup_transform`` usage
     - 4
     - Correctly calls ``lookup_transform("odom",
       "aruco_marker_<id>", ...)`` with a timeout. Extracts ``x``
       and ``y`` from the translation. Stores the values for
       centroid computation.
   * - Error handling
     - 3
     - TF lookup failures are caught, logged as warnings, and retried
       (up to 3 times). If all retries fail, logs an error and
       continues to the next waypoint without crashing.
   * - **Centroid Computation and Final Navigation (6 pts)**
     -
     -
   * - Centroid calculation
     - 3
     - Centroid is computed as the arithmetic mean of the detected
       marker positions. Handles the case where fewer than 3 markers
       were detected (uses only successful detections).
   * - Final navigation
     - 3
     - Centroid coordinates are published as a ``PoseStamped`` to
       ``/goal_pose``. Node waits for ``/goal_reached`` and logs a
       completion message with a summary of all marker positions
       and the centroid.
   * - **Launch File (8 pts)**
     -
     -
   * - All nodes started
     - 2
     - Launch file starts ``p_controller``, ``aruco_detector``, and
       ``marker_navigator``. All use ``output="screen"`` and
       ``emulate_tty=True``.
   * - Parameter file loading
     - 2
     - ``config/waypoints.yaml`` is loaded for the
       ``marker_navigator`` node using
       ``get_package_share_directory()`` and the ``parameters``
       field.
   * - Launch arguments
     - 2
     - At least two launch arguments declared (``goal_tolerance``
       and ``yaw_tolerance``). Values are passed to the
       ``p_controller`` node. ``--show-args`` displays them
       correctly.
   * - ``GroupAction``
     - 2
     - Infrastructure nodes (``p_controller`` and
       ``aruco_detector``) are grouped in a ``GroupAction``.
   * - **Documentation and Code Quality (10 pts)**
     -
     -
   * - README.md
     - 4
     - Group members and contributions. System architecture diagram
       showing nodes, topics, and TF frames. TF tree output
       (``frames.pdf``) included and annotated. Design decisions
       for marker discovery and error handling explained. Build and
       run instructions provided.
   * - Docstrings and type hints
     - 3
     - Every class and method has a Google-style docstring. All
       method parameters and return types have type annotations.
   * - Logging and code quality
     - 3
     - ROS 2 logger used exclusively (no ``print()``). Correct
       severity levels (``info`` for normal, ``warn`` for retries,
       ``error`` for failures). Consistent ``snake_case`` naming.
       No Ruff linting errors.
   * - **TOTAL**
     - **50**
     -
