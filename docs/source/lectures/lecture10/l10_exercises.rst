====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 10. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``~/enpm605_ws/src/`` workspace
using the appropriate demo packages.


.. dropdown:: Exercise 1 -- Parameter-Driven Controller
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build a node that uses parameters to configure a simulated
    proportional controller, with runtime parameter updates and a YAML
    configuration file.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``param_demo/param_demo/controller_node.py`` that
    implements the following.

    1. **``ControllerNode(Node)``** class:

       - ``__init__(self)``: calls ``super().__init__("controller")``,
         declares the following parameters with descriptors:

         - ``kp`` (float, default ``1.0``): proportional gain with a
           ``FloatingPointRange`` of ``[0.0, 50.0]``.
         - ``setpoint`` (float, default ``10.0``): target value.
         - ``update_rate`` (float, default ``2.0``): timer frequency
           in Hz.

       - Registers a parameter callback that logs every parameter
         change and rejects negative ``kp`` values.
       - Creates a timer at ``update_rate`` Hz that simulates a
         control loop.

    2. **Timer callback** ``_control_loop(self)``:

       - Reads the current ``kp`` and ``setpoint`` values.
       - Computes ``error = setpoint - self._current_value`` where
         ``self._current_value`` starts at ``0.0`` and is updated each
         tick: ``self._current_value += kp * error * dt``.
       - Logs the current value, error, and control output.

    3. **YAML parameter file** ``config/controller_params.yaml``:

       .. code-block:: yaml

          /controller:
            ros__parameters:
              kp: 2.5
              setpoint: 20.0
              update_rate: 5.0

    4. Register the entry point in ``setup.py`` and install the config
       directory.

    **Expected behavior**

    - The node starts and converges toward the setpoint.
    - Changing ``kp`` via ``ros2 param set`` immediately affects the
      convergence rate.
    - Setting ``kp`` to a negative value is rejected by the callback.

    **Verification**

    .. code-block:: console

       # Start with YAML config
       ros2 run param_demo controller_node --ros-args --params-file \
           ~/enpm605_ws/src/param_demo/config/controller_params.yaml

       # In another terminal, modify kp
       ros2 param set /controller kp 5.0

       # Try an invalid value
       ros2 param set /controller kp -1.0

       # Inspect all parameters
       ros2 param list /controller
       ros2 param get /controller kp


.. dropdown:: Exercise 2 -- Custom Interface Package
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a complete custom interface package with a message, a
    service, and an action definition. Build it and verify all
    interfaces are accessible.


    .. raw:: html

       <hr>


    **Specification**

    Create the package ``custom_interfaces`` (if not already present)
    with the following interface definitions.

    1. **Message** ``msg/RobotStatus.msg``:

       .. code-block:: text

          std_msgs/Header header
          string robot_id
          float64 battery_level
          float64[3] position
          bool is_active
          uint8 ERROR_NONE=0
          uint8 ERROR_LOW_BATTERY=1
          uint8 ERROR_COLLISION=2
          uint8 error_code

    2. **Service** ``srv/SetSpeed.srv``:

       .. code-block:: text

          # Request
          float64 linear_speed
          float64 angular_speed
          ---
          # Response
          bool success
          string message

    3. **Action** ``action/Patrol.action``:

       .. code-block:: text

          # Goal
          geometry_msgs/Point[] waypoints
          float64 speed
          ---
          # Result
          bool completed
          uint32 waypoints_visited
          float64 total_time
          ---
          # Feedback
          uint32 current_waypoint_index
          float64 distance_to_next
          float64 elapsed_time

    4. Update ``CMakeLists.txt`` and ``package.xml`` with all required
       dependencies (``std_msgs``, ``geometry_msgs``, ``action_msgs``,
       ``rosidl_default_generators``).

    **Expected behavior**

    After building, all three interfaces should appear in
    ``ros2 interface list`` and their definitions should be viewable.

    **Verification**

    .. code-block:: console

       colcon build --symlink-install --packages-select custom_interfaces
       source install/setup.bash

       ros2 interface show custom_interfaces/msg/RobotStatus
       ros2 interface show custom_interfaces/srv/SetSpeed
       ros2 interface show custom_interfaces/action/Patrol


.. dropdown:: Exercise 3 -- Service Server and Client
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a service server that validates and applies speed commands,
    and an asynchronous client that sends requests and handles
    responses.


    .. raw:: html

       <hr>


    **Specification**

    Create the following files in ``service_demo/``.

    1. **Server** ``service_demo/speed_server.py``:

       - Node name: ``speed_server``
       - Service name: ``/set_speed``
       - Service type: ``custom_interfaces/srv/SetSpeed``
       - Callback validates the request:

         - Rejects ``linear_speed > 5.0`` or ``angular_speed > 3.0``
           (sets ``success=False`` with an appropriate message).
         - Otherwise sets ``success=True`` and logs the applied speeds.

    2. **Async client** ``service_demo/speed_client.py``:

       - Node name: ``speed_client``
       - Waits for the ``/set_speed`` service to become available.
       - Sends a request with ``linear_speed=2.0`` and
         ``angular_speed=0.5``.
       - Uses ``call_async()`` with ``add_done_callback()``.
       - Logs the response success status and message.
       - After the response, sends a second request with
         ``linear_speed=10.0`` to test rejection.

    3. Register both entry points in ``setup.py``.

    **Expected behavior**

    - The first request succeeds; the second is rejected with a
      descriptive message.
    - The server logs each incoming request.
    - The client logs both responses.

    **Verification**

    .. code-block:: console

       # Terminal 1
       ros2 run service_demo speed_server

       # Terminal 2
       ros2 run service_demo speed_client

       # CLI test
       ros2 service call /set_speed custom_interfaces/srv/SetSpeed \
           "{linear_speed: 2.0, angular_speed: 0.5}"


.. dropdown:: Exercise 4 -- Action Server and Client with Cancellation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write an action server that simulates a patrol mission and an
    action client that sends a goal, monitors feedback, and cancels
    the goal mid-execution.


    .. raw:: html

       <hr>


    **Specification**

    Create the following files in ``action_demo/``.

    1. **Server** ``action_demo/patrol_server.py``:

       - Node name: ``patrol_server``
       - Action name: ``/patrol``
       - Action type: ``custom_interfaces/action/Patrol``
       - ``_goal_callback``: accepts all goals with at least one
         waypoint; rejects goals with an empty waypoint list.
       - ``_cancel_callback``: always accepts cancellation.
       - ``_execute_callback``:

         - Iterates through each waypoint in ``goal.waypoints``.
         - For each waypoint, sleeps 2 seconds to simulate movement.
         - Publishes feedback after each waypoint
           (``current_waypoint_index``, ``distance_to_next``).
         - Checks ``goal_handle.is_cancel_requested`` at each
           iteration.
         - On completion: sets ``completed=True``,
           ``waypoints_visited=N``, ``total_time``.
         - On cancellation: sets ``completed=False`` with partial
           results.

    2. **Client** ``action_demo/patrol_client.py``:

       - Node name: ``patrol_client``
       - Sends a goal with 5 waypoints:
         ``[(1,0,0), (2,1,0), (3,2,0), (4,1,0), (5,0,0)]``.
       - Logs every feedback message.
       - After 5 seconds (using a one-shot timer), cancels the goal.
       - Logs the final result (completed or canceled, waypoints
         visited, total time).

    3. Register both entry points in ``setup.py``.

    **Expected behavior**

    - The server begins visiting waypoints and publishing feedback.
    - After 5 seconds the client cancels the goal.
    - The server acknowledges the cancellation and returns partial
      results (2-3 waypoints visited).
    - Both nodes log the outcome.

    **Verification**

    .. code-block:: console

       # Terminal 1
       ros2 run action_demo patrol_server

       # Terminal 2
       ros2 run action_demo patrol_client

       # CLI test with feedback
       ros2 action send_goal /patrol custom_interfaces/action/Patrol \
           "{waypoints: [{x: 1.0, y: 0.0, z: 0.0}, {x: 2.0, y: 1.0, z: 0.0}], speed: 1.0}" \
           --feedback
