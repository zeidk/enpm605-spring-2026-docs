====================================================
Grading Rubric
====================================================

.. |<=| unicode:: U+2264
.. |rarr| unicode:: U+2192


This rubric details how the 50 points are allocated.

.. list-table::
   :widths: 42 6 52
   :header-rows: 1
   :class: compact-table

   * - Component
     - Pts
     - Criteria
   * - **Action Interface (5 pts)**
     -
     -
   * - ``NavigateToGoal.action`` definition
     - 2
     - Goal, result, and feedback sections match the specification
       exactly (correct types and field names).
   * - CMake package configuration
     - 3
     - ``CMakeLists.txt`` generates the interface via
       ``rosidl_generate_interfaces`` with ``geometry_msgs``
       dependency. ``package.xml`` includes
       ``rosidl_default_generators``,
       ``rosidl_default_runtime``, and the
       ``rosidl_interface_packages`` group. Package builds cleanly.
   * - **Action Server (18 pts)**
     -
     -
   * - Server registration
     - 2
     - ``ActionServer`` created with the correct name
       (``navigate_to_goal``), interface, and callbacks
       (goal / cancel / execute).
   * - Odometry subscription and pose tracking
     - 2
     - Subscribes to ``/odometry/filtered``. Converts quaternion to
       yaw with ``scipy``. Tracks the latest ``(x, y, yaw)`` for
       the control loop.
   * - Two-phase P-controller (position phase)
     - 4
     - Correctly computes ``rho``, ``angle_to_goal``, ``alpha``.
       Publishes ``TwistStamped`` on ``/cmd_vel`` with linear and
       angular commands clamped to ``MAX_LINEAR`` / ``MAX_ANGULAR``.
   * - Two-phase P-controller (orientation phase)
     - 3
     - Switches to orientation phase when within
       ``goal_tolerance``. Uses wrapped ``yaw_error`` with
       ``k_yaw``. Terminates when ``|yaw_error| < yaw_tolerance``.
   * - Feedback publishing
     - 3
     - Publishes ``current_pose`` and ``distance_remaining`` at
       1 to 5 Hz during execution.
   * - Cancellation handling (with demo)
     - 2
     - Detects ``goal_handle.is_cancel_requested``, sends a
       zero-velocity stop, calls ``goal_handle.canceled()``, and
       returns a result with ``success=False``. A demonstration
       log or screenshot (``cancel_demo.txt`` /
       ``cancel_demo.png``) is included in the ``gp2/`` folder, as
       described in :doc:`outputs`.
   * - Result on success
     - 2
     - Calls ``goal_handle.succeed()`` and returns a result with
       ``success=True``, non-zero ``total_distance``, and non-zero
       ``elapsed_time``.
   * - **Action Client (12 pts)**
     -
     -
   * - Parameter loading
     - 3
     - Three named goal blocks (``goal1``, ``goal2``, ``goal3``)
       loaded from ``config/goals.yaml`` via ``self.get_parameter()``
       using dot-namespaced names (e.g. ``goal1.x``,
       ``goal1.final_heading``). All nine fields are validated as
       present. Goals are logged at startup.
   * - Sequential goal dispatch
     - 4
     - Next goal is sent **only after** the previous goal's result
       is received. No queueing, no parallel dispatch. Uses
       ``send_goal_async`` with goal-response callback.
   * - Feedback and result logging
     - 3
     - Feedback is logged at ``info`` (throttled to |<=| 1 Hz).
       Each result logs ``success``, ``total_distance``, and
       ``elapsed_time``.
   * - Error handling
     - 2
     - If a goal is rejected or returns ``success=False``, the
       client logs an error and aborts the sequence (does not send
       remaining goals). Mission summary is logged on full success.
   * - **Launch File (5 pts)**
     -
     -
   * - Both nodes started
     - 2
     - Launch file starts ``navigate_to_goal_server`` and
       ``navigate_to_goal_client``. Both use ``output="screen"``
       and ``emulate_tty=True``.
   * - Parameter file loading
     - 1
     - ``config/goals.yaml`` is loaded for the **client** node
       using ``get_package_share_directory()`` and the
       ``parameters`` field.
   * - Launch arguments
     - 2
     - At least two launch arguments declared (``goal_tolerance``
       and ``yaw_tolerance``) and passed to the server.
       ``--show-args`` displays them correctly.
   * - **Documentation and Code Quality (10 pts)**
     -
     -
   * - README.md contributions
     - 4
     - ``README.md`` contains a contributions section with every
       group member listed and a short, specific summary of what
       each member personally worked on. Vague or boilerplate
       entries ("helped with the project") lose points.
   * - Docstrings and type hints
     - 3
     - Every class and method has a Google-style docstring. All
       method parameters and return types have type annotations.
   * - Logging and code quality
     - 3
     - ROS 2 logger used exclusively (no ``print()``). Correct
       severity levels. Consistent ``snake_case`` naming. No Ruff
       linting errors.
   * - **TOTAL**
     - **50**
     -
