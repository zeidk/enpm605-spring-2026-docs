====================================================
Scenario 1: Robot Inspection System
====================================================


Domain
======

A facility management system coordinates robotic inspections of
locations in a building. An operator node requests inspections through a
service, and a robot node executes them as long-running actions with
progress feedback. A results node logs completed inspections and tracks
overall inspection statistics.

The system models a real-world workflow: a human operator requests an
inspection at a specific location, the robot navigates to the location,
performs the inspection (checking temperature, humidity, and structural
integrity), and reports back with a detailed result.


.. dropdown:: System Architecture
   :open:

   Your system must contain the following nodes, services, and actions.

   **Nodes**

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Node
        - Description
      * - ``operator_node``
        - Acts as the service client and action client. On startup (or
          via a timer), sends a service request to check whether a
          location is available for inspection. If the service response
          indicates the location is valid, sends an action goal to
          execute the inspection. Logs feedback from the action server
          as the inspection progresses. Demonstrates cancellation by
          canceling one inspection mid-execution.
      * - ``inspection_server``
        - Hosts **both** the service server and the action server.
          The service validates whether a requested location exists in
          the facility map (a parameter-loaded list of valid locations).
          The action executes the inspection: navigating to the location
          (simulated), performing sensor checks (simulated), and
          returning a detailed result.
      * - ``results_logger``
        - Subscribes to ``/inspection/results`` (published by the
          inspection server upon completion). Logs each result and
          maintains a running count of completed inspections. Publishes
          a summary on ``/inspection/summary`` at 0.2 Hz.
      * - ``dashboard`` *(optional, conditional)*
        - Subscribes to ``/inspection/summary`` and logs the summary.
          Started only when the launch argument ``enable_dashboard`` is
          ``true``.

   **Services**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Service
        - Interface
        - Description
      * - ``/inspection/check_location``
        - ``CheckLocation.srv``
        - Request: location name. Response: whether the location is
          valid, the location's zone, and a message string.

   **Actions**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Action
        - Interface
        - Description
      * - ``/inspection/execute``
        - ``ExecuteInspection.action``
        - Goal: location name and inspection type. Feedback: current
          phase, progress percentage, and status message. Result:
          inspection report with sensor readings and overall status.

   **Topics**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Topic
        - Message Type
        - Description
      * - ``/inspection/results``
        - ``InspectionResult.msg``
        - Published by ``inspection_server`` when an inspection completes.
          Contains location, timestamp, sensor readings, and pass/fail.
      * - ``/inspection/summary``
        - ``std_msgs/msg/String``
        - Published by ``results_logger`` with a count of completed
          inspections and pass/fail statistics.


.. dropdown:: Custom Interfaces
   :open:

   Create the following interface files in the ``group<N>_gp2_interfaces``
   package.

   **msg/InspectionResult.msg**

   .. code-block:: text

      string location
      string zone
      string inspection_type
      float64 temperature
      float64 humidity
      bool structural_ok
      bool passed
      string timestamp

   **srv/CheckLocation.srv**

   .. code-block:: text

      # Request
      string location_name
      ---
      # Response
      bool valid
      string zone
      string message

   **action/ExecuteInspection.action**

   .. code-block:: text

      # Goal
      string location_name
      string inspection_type
      ---
      # Result
      bool success
      string location
      float64 temperature
      float64 humidity
      bool structural_ok
      bool passed
      string report_message
      ---
      # Feedback
      string current_phase
      float64 progress_percentage
      string status_message


.. dropdown:: Detailed Requirements
   :open:

   1. **Service -- CheckLocation**: The ``inspection_server`` must
      declare a parameter ``valid_locations`` loaded from
      ``config/params.yaml``. This parameter is a list of strings
      representing valid location names (e.g.,
      ``["hallway_A", "server_room", "lab_101", "roof_access"]``). When
      the service receives a request:

      - If the location is in the list, return ``valid=True``, the zone
        (a parameter-defined mapping, e.g., ``"Zone A"``), and a
        confirmation message.
      - If the location is not in the list, return ``valid=False``, an
        empty zone, and an error message such as
        ``"Location 'basement' is not in the facility map."``.

   2. **Action -- ExecuteInspection**: The action server simulates a
      multi-phase inspection:

      - **Phase 1 -- Navigation** (0--30%): Simulates traveling to the
        location. Publish feedback every 0.5 seconds with the current
        phase ``"navigating"`` and increasing progress.
      - **Phase 2 -- Sensor Check** (30--80%): Simulates reading
        temperature (``random.uniform(18.0, 35.0)``), humidity
        (``random.uniform(20.0, 90.0)``), and structural integrity
        (``random.choice([True, True, True, False])``). Publish feedback
        with phase ``"inspecting"``.
      - **Phase 3 -- Report Generation** (80--100%): Compiles the results
        and publishes the ``InspectionResult`` message on
        ``/inspection/results``. Publish feedback with phase
        ``"reporting"``.
      - The inspection **passes** if temperature is between 18.0 and
        30.0, humidity is between 30.0 and 70.0, and structural integrity
        is ``True``.

   3. **Cancellation**: The action server must check for cancellation
      between phases. If canceled, log a warning, stop execution, and
      return a result with ``success=False`` and a message indicating
      cancellation. The ``operator_node`` must demonstrate cancellation by
      canceling the second inspection request 2 seconds after sending it.

   4. **Parameters** (loaded from ``config/params.yaml``):

      - ``inspection_server``:

        - ``valid_locations``: list of valid location name strings.
        - ``navigation_speed``: float (affects simulated navigation
          time, default ``1.0``).

      - ``results_logger``:

        - ``summary_rate``: float (rate in Hz for publishing summaries,
          default ``0.2``).

   5. **Launch files**:

      - ``system.launch.py``: starts ``inspection_server``,
        ``operator_node``, and ``results_logger``. Loads
        ``config/params.yaml`` for the ``inspection_server`` and
        ``results_logger``.
      - ``enable_dashboard`` argument (default ``false``): conditionally
        starts the ``dashboard`` node using ``IfCondition``.
      - ``navigation_speed`` argument (default ``1.0``): overrides the
        ``inspection_server``'s ``navigation_speed`` parameter.
      - Server and logger nodes grouped in a ``GroupAction``.


.. dropdown:: Expected Behavior
   :open:

   **Normal operation:**

   .. code-block:: text

      [INFO] [<timestamp>] [operator_node]: Checking location: hallway_A
      [INFO] [<timestamp>] [inspection_server]: CheckLocation request for 'hallway_A' -- valid
      [INFO] [<timestamp>] [operator_node]: Location valid (Zone A). Sending inspection goal...
      [INFO] [<timestamp>] [inspection_server]: Inspection goal accepted for hallway_A
      [INFO] [<timestamp>] [operator_node]: Feedback -- navigating: 10.0%
      [INFO] [<timestamp>] [operator_node]: Feedback -- navigating: 20.0%
      [INFO] [<timestamp>] [operator_node]: Feedback -- inspecting: 50.0%
      [INFO] [<timestamp>] [operator_node]: Feedback -- reporting: 90.0%
      [INFO] [<timestamp>] [inspection_server]: Inspection complete for hallway_A -- PASSED
      [INFO] [<timestamp>] [operator_node]: Result -- hallway_A: PASSED (temp: 22.5, humidity: 45.0)
      [INFO] [<timestamp>] [results_logger]: Logged result for hallway_A -- PASSED

   **Invalid location:**

   .. code-block:: text

      [INFO] [<timestamp>] [operator_node]: Checking location: basement
      [WARN] [<timestamp>] [inspection_server]: CheckLocation request for 'basement' -- not found
      [WARN] [<timestamp>] [operator_node]: Location invalid: "Location 'basement' is not in the facility map."

   **Cancellation:**

   .. code-block:: text

      [INFO] [<timestamp>] [operator_node]: Sending inspection goal for server_room
      [INFO] [<timestamp>] [operator_node]: Feedback -- navigating: 10.0%
      [INFO] [<timestamp>] [operator_node]: Canceling inspection for server_room...
      [WARN] [<timestamp>] [inspection_server]: Inspection canceled for server_room at 20.0%
      [INFO] [<timestamp>] [operator_node]: Inspection canceled. Partial result received.

   **Verification commands:**

   .. code-block:: console

      ros2 launch group<N>_gp2 system.launch.py
      ros2 launch group<N>_gp2 system.launch.py enable_dashboard:=true
      ros2 launch group<N>_gp2 system.launch.py navigation_speed:=2.0
      ros2 service list
      ros2 service call /inspection/check_location group<N>_gp2_interfaces/srv/CheckLocation "{location_name: 'hallway_A'}"
      ros2 action list
      ros2 action send_goal /inspection/execute group<N>_gp2_interfaces/action/ExecuteInspection "{location_name: 'lab_101', inspection_type: 'full'}" --feedback
      ros2 interface show group<N>_gp2_interfaces/srv/CheckLocation
      ros2 interface show group<N>_gp2_interfaces/action/ExecuteInspection
      ros2 param list
      ros2 param get /inspection_server valid_locations


.. dropdown:: Scenario 1 Grading Rubric
   :open:

   This rubric details how the 50 points map to Scenario 1 deliverables.

   .. list-table::
      :widths: 40 8 52
      :header-rows: 1
      :class: compact-table

      * - Component
        - Pts
        - Criteria
      * - **Custom Interfaces (8 pts)**
        -
        -
      * - ``InspectionResult.msg``
        - 2
        - Correctly defined with all required fields. Builds
          successfully with ``colcon build``. Visible via
          ``ros2 interface show``.
      * - ``CheckLocation.srv``
        - 3
        - Request/response fields correctly defined. Includes
          ``valid``, ``zone``, and ``message`` in response.
      * - ``ExecuteInspection.action``
        - 3
        - Goal, result, and feedback sections correctly defined.
          Feedback includes ``current_phase``, ``progress_percentage``,
          and ``status_message``.
      * - **Service Implementation (10 pts)**
        -
        -
      * - Service server
        - 5
        - ``CheckLocation`` service validates against parameter-loaded
          location list. Returns ``valid=True`` with zone for known
          locations. Returns ``valid=False`` with descriptive error for
          unknown locations.
      * - Service client
        - 5
        - Uses ``call_async()`` to send requests. Processes response
          correctly. Handles valid and invalid location responses.
          Proceeds to send action goal only when location is valid.
      * - **Action Implementation (14 pts)**
        -
        -
      * - Action server -- phases
        - 5
        - Implements three phases (navigation, sensor check, reporting).
          Publishes feedback at least once per second with phase name
          and progress percentage.
      * - Action server -- result
        - 3
        - Returns complete result with sensor readings and pass/fail
          determination based on threshold logic. Publishes
          ``InspectionResult`` on ``/inspection/results``.
      * - Action server -- cancellation
        - 3
        - Checks for cancellation between phases. Stops execution, logs
          warning, and returns partial result on cancel.
      * - Action client
        - 3
        - Sends goal with feedback callback. Logs feedback as it arrives.
          Demonstrates cancellation of one goal. Handles result callback.
      * - **Parameters (6 pts)**
        -
        -
      * - Parameter declaration
        - 2
        - At least three parameters declared with
          ``self.declare_parameter()``. Parameters affect node behavior.
      * - YAML config file
        - 2
        - ``config/params.yaml`` correctly formatted. Sets values for
          all declared parameters.
      * - Launch-time override
        - 2
        - ``navigation_speed`` launch argument overrides the parameter.
          ``ros2 param get`` confirms the override.
      * - **Launch File (6 pts)**
        -
        -
      * - ``system.launch.py``
        - 2
        - Starts all required nodes. Loads ``config/params.yaml``. All
          nodes use ``output="screen"`` and ``emulate_tty=True``.
      * - ``enable_dashboard`` argument
        - 1
        - ``DeclareLaunchArgument`` with default ``false``. Dashboard
          node uses ``IfCondition``.
      * - ``navigation_speed`` argument
        - 1
        - ``DeclareLaunchArgument`` with default ``1.0``. Overrides
          the ``inspection_server`` parameter.
      * - ``GroupAction``
        - 2
        - Server and logger nodes grouped in a ``GroupAction``.
      * - **Documentation and Quality (6 pts)**
        -
        -
      * - README.md
        - 3
        - Group members, scenario summary, system architecture diagram,
          custom interface descriptions, design decisions, build/run
          instructions.
      * - Code quality
        - 3
        - Type hints, docstrings, ROS 2 logger with correct severity
          levels, consistent naming, no linting errors.
      * - **TOTAL**
        - **50**
        -
