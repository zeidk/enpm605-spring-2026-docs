====================================================
Scenario 3: Multi-Robot Task Allocation
====================================================


Domain
======

A centralized task allocation system manages a fleet of heterogeneous
robots. Each robot has different capabilities (e.g., carrying capacity,
speed, sensor suite). A task manager assigns tasks to robots based on
their capabilities, and an action server on each robot executes the
assigned task with real-time progress feedback.

The system models a multi-robot coordination workflow: robots register
with a fleet manager, the task manager queries robot capabilities
through a service, assigns tasks via an action, and a monitor node
tracks fleet-wide progress and task completion rates.


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
      * - ``fleet_manager``
        - Hosts the service server for robot registration and capability
          queries. Maintains a registry of robots with their
          capabilities (loaded from parameters). Responds to queries
          about which robots can handle a given task type.
      * - ``task_manager``
        - Acts as the service client and action client. On startup (or
          via a timer), queries the ``fleet_manager`` to find a capable
          robot for a task. If a suitable robot is found, sends an
          action goal to that robot's task execution action server.
          Logs feedback as the task progresses. Demonstrates
          cancellation by canceling one task mid-execution.
      * - ``robot_alpha``
        - Hosts an action server at ``/robot_alpha/execute_task``.
          Simulates task execution with multiple steps. Publishes
          progress feedback. Has capabilities defined by parameters
          (e.g., ``capabilities: ["transport", "scan"]``,
          ``max_payload: 50.0``).
      * - ``robot_beta``
        - Hosts an action server at ``/robot_beta/execute_task``.
          Similar to ``robot_alpha`` but with different capabilities
          (e.g., ``capabilities: ["transport", "heavy_lift"]``,
          ``max_payload: 200.0``) and a slower execution speed.
      * - ``fleet_monitor``
        - Subscribes to ``/fleet/task_completions`` (published by robot
          nodes upon task completion). Tracks per-robot task counts and
          publishes a fleet summary on ``/fleet/status`` at 0.2 Hz.
      * - ``dashboard`` *(optional, conditional)*
        - Subscribes to ``/fleet/status`` and logs the fleet summary.
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
      * - ``/fleet/query_robots``
        - ``QueryRobots.srv``
        - Request: task type and required payload capacity. Response:
          whether a suitable robot was found, the robot name, and a
          message string.

   **Actions**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Action
        - Interface
        - Description
      * - ``/robot_alpha/execute_task``
        - ``ExecuteTask.action``
        - Goal: task description, target location, and payload weight.
          Feedback: current step, progress percentage, and status
          message. Result: success flag, task summary, total time, and
          result message.
      * - ``/robot_beta/execute_task``
        - ``ExecuteTask.action``
        - Same interface as ``robot_alpha`` but with different execution
          characteristics (slower speed, higher payload capacity).

   **Topics**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Topic
        - Message Type
        - Description
      * - ``/fleet/task_completions``
        - ``TaskCompletion.msg``
        - Published by robot nodes when a task completes. Contains
          robot name, task description, elapsed time, success status,
          and timestamp.
      * - ``/fleet/status``
        - ``std_msgs/msg/String``
        - Published by ``fleet_monitor`` with per-robot task counts,
          success rates, and average completion times.


.. dropdown:: Custom Interfaces
   :open:

   Create the following interface files in the ``group<N>_gp2_interfaces``
   package.

   **msg/TaskCompletion.msg**

   .. code-block:: text

      string robot_name
      string task_description
      string target_location
      float64 elapsed_time
      bool success
      string timestamp

   **srv/QueryRobots.srv**

   .. code-block:: text

      # Request
      string task_type
      float64 required_payload
      ---
      # Response
      bool robot_found
      string robot_name
      string robot_capabilities
      float64 max_payload
      string message

   **action/ExecuteTask.action**

   .. code-block:: text

      # Goal
      string task_description
      string target_location
      float64 payload_weight
      ---
      # Result
      bool success
      string task_summary
      float64 total_time
      string result_message
      ---
      # Feedback
      string current_step
      float64 progress_percentage
      string status_message


.. dropdown:: Detailed Requirements
   :open:

   1. **Service -- QueryRobots**: The ``fleet_manager`` must declare
      parameters for each robot's capabilities, loaded from
      ``config/params.yaml``. The registry stores each robot's name,
      list of capabilities, and maximum payload capacity. When the
      service receives a request:

      - Search the registry for a robot whose capabilities include the
        requested ``task_type`` and whose ``max_payload`` is greater than
        or equal to ``required_payload``.
      - If found, return ``robot_found=True``, the robot's name, a
        comma-separated list of its capabilities, its max payload, and
        a confirmation message.
      - If no suitable robot is found, return ``robot_found=False``,
        empty robot name, empty capabilities, ``0.0`` payload, and
        an error message such as
        ``"No robot available for task 'heavy_lift' with payload 300.0 kg."``.
      - If multiple robots match, return the first one found (or the
        one with the highest payload capacity -- document your choice
        in ``README.md``).

   2. **Action -- ExecuteTask**: Each robot node hosts its own action
      server. The action simulates a multi-step task execution:

      - **Step 1 -- Initialization** (0--15%): Robot prepares for the
        task (loading parameters, checking systems). Publish feedback
        every 0.5 seconds with step ``"initializing"``.
      - **Step 2 -- Navigation** (15--45%): Robot navigates to the
        target location. Publish feedback with step ``"navigating"``.
        Navigation time is affected by the robot's ``speed`` parameter.
      - **Step 3 -- Execution** (45--85%): Robot performs the task
        (transport, scan, or heavy lift). Publish feedback with step
        ``"executing"``.
      - **Step 4 -- Returning** (85--100%): Robot returns to its home
        position. Publish feedback with step ``"returning"``. On
        completion, publish a ``TaskCompletion`` message on
        ``/fleet/task_completions``.

      ``robot_beta`` executes tasks at half the speed of
      ``robot_alpha`` (controlled by the ``speed`` parameter).

   3. **Cancellation**: Each action server must check for cancellation
      between steps. If canceled, log a warning, stop execution, and
      return a result with ``success=False`` and a message indicating
      at which step the task was canceled. The ``task_manager`` must
      demonstrate cancellation by canceling the second task 2 seconds
      after sending the goal.

   4. **Task sequence**: The ``task_manager`` must process a sequence
      of at least three tasks:

      - Task 1: ``task_type="transport"``, ``required_payload=30.0``
        (should be assigned to ``robot_alpha`` or ``robot_beta``).
      - Task 2: ``task_type="heavy_lift"``, ``required_payload=150.0``
        (should be assigned to ``robot_beta`` only). Cancel this task
        mid-execution.
      - Task 3: ``task_type="scan"``, ``required_payload=5.0``
        (should be assigned to ``robot_alpha``).

      Process tasks sequentially: wait for each task to complete (or
      be canceled) before starting the next one.

   5. **Parameters** (loaded from ``config/params.yaml``):

      - ``fleet_manager``:

        - ``robot_names``: list of robot name strings
          (e.g., ``["robot_alpha", "robot_beta"]``).
        - ``robot_alpha_capabilities``: list of capability strings.
        - ``robot_alpha_max_payload``: float.
        - ``robot_beta_capabilities``: list of capability strings.
        - ``robot_beta_max_payload``: float.

      - ``robot_alpha``:

        - ``speed``: float (execution speed multiplier, default ``1.0``).
        - ``capabilities``: list of strings.

      - ``robot_beta``:

        - ``speed``: float (execution speed multiplier, default ``0.5``).
        - ``capabilities``: list of strings.

      - ``fleet_monitor``:

        - ``status_rate``: float (rate in Hz for publishing status,
          default ``0.2``).

   6. **Launch files**:

      - ``system.launch.py``: starts ``fleet_manager``,
        ``task_manager``, ``robot_alpha``, ``robot_beta``, and
        ``fleet_monitor``. Loads ``config/params.yaml`` for all
        parameterized nodes.
      - ``enable_dashboard`` argument (default ``false``): conditionally
        starts the ``dashboard`` node using ``IfCondition``.
      - ``robot_speed`` argument (default ``1.0``): overrides the
        ``robot_alpha`` speed parameter (to demonstrate parameter
        override via launch argument).
      - Robot nodes (``robot_alpha`` and ``robot_beta``) grouped in a
        ``GroupAction``.


.. dropdown:: Expected Behavior
   :open:

   **Normal operation (Task 1):**

   .. code-block:: text

      [INFO] [<timestamp>] [task_manager]: Querying fleet for task: transport, payload: 30.0 kg
      [INFO] [<timestamp>] [fleet_manager]: QueryRobots -- robot_alpha can handle 'transport' (payload: 50.0 kg)
      [INFO] [<timestamp>] [task_manager]: Robot found: robot_alpha. Sending task goal...
      [INFO] [<timestamp>] [robot_alpha]: Task goal accepted: transport to warehouse_B (30.0 kg)
      [INFO] [<timestamp>] [task_manager]: Feedback -- initializing: 5.0%
      [INFO] [<timestamp>] [task_manager]: Feedback -- navigating: 25.0%
      [INFO] [<timestamp>] [task_manager]: Feedback -- executing: 60.0%
      [INFO] [<timestamp>] [task_manager]: Feedback -- returning: 95.0%
      [INFO] [<timestamp>] [robot_alpha]: Task complete: transport to warehouse_B (12.0 s)
      [INFO] [<timestamp>] [task_manager]: Result -- transport complete in 12.0 s
      [INFO] [<timestamp>] [fleet_monitor]: Task completed by robot_alpha: transport

   **No suitable robot:**

   .. code-block:: text

      [INFO] [<timestamp>] [task_manager]: Querying fleet for task: underwater_weld, payload: 10.0 kg
      [WARN] [<timestamp>] [fleet_manager]: QueryRobots -- no robot available for 'underwater_weld' (payload: 10.0 kg)
      [WARN] [<timestamp>] [task_manager]: No suitable robot: "No robot available for task 'underwater_weld' with payload 10.0 kg."

   **Cancellation (Task 2):**

   .. code-block:: text

      [INFO] [<timestamp>] [task_manager]: Sending task goal to robot_beta: heavy_lift at loading_dock
      [INFO] [<timestamp>] [task_manager]: Feedback -- initializing: 5.0%
      [INFO] [<timestamp>] [task_manager]: Feedback -- navigating: 20.0%
      [INFO] [<timestamp>] [task_manager]: Canceling task for robot_beta...
      [WARN] [<timestamp>] [robot_beta]: Task canceled at step: navigating (25.0%)
      [INFO] [<timestamp>] [task_manager]: Task canceled. Partial result received.

   **Verification commands:**

   .. code-block:: console

      ros2 launch group<N>_gp2 system.launch.py
      ros2 launch group<N>_gp2 system.launch.py enable_dashboard:=true
      ros2 launch group<N>_gp2 system.launch.py robot_speed:=2.0
      ros2 service list
      ros2 service call /fleet/query_robots group<N>_gp2_interfaces/srv/QueryRobots "{task_type: 'transport', required_payload: 30.0}"
      ros2 action list
      ros2 action send_goal /robot_alpha/execute_task group<N>_gp2_interfaces/action/ExecuteTask "{task_description: 'transport', target_location: 'warehouse_B', payload_weight: 30.0}" --feedback
      ros2 interface show group<N>_gp2_interfaces/srv/QueryRobots
      ros2 interface show group<N>_gp2_interfaces/action/ExecuteTask
      ros2 param list
      ros2 param get /robot_alpha speed


.. dropdown:: Scenario 3 Grading Rubric
   :open:

   This rubric details how the 50 points map to Scenario 3 deliverables.

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
      * - ``TaskCompletion.msg``
        - 2
        - Correctly defined with all required fields. Builds
          successfully with ``colcon build``. Visible via
          ``ros2 interface show``.
      * - ``QueryRobots.srv``
        - 3
        - Request/response fields correctly defined. Includes
          ``robot_found``, ``robot_name``, ``robot_capabilities``,
          ``max_payload``, and ``message`` in response.
      * - ``ExecuteTask.action``
        - 3
        - Goal, result, and feedback sections correctly defined.
          Feedback includes ``current_step``, ``progress_percentage``,
          and ``status_message``.
      * - **Service Implementation (10 pts)**
        -
        -
      * - Service server
        - 5
        - ``QueryRobots`` service searches parameter-loaded robot
          registry. Matches on ``task_type`` capability and
          ``required_payload``. Returns correct robot info for valid
          queries. Returns descriptive error for unmatched queries.
      * - Service client
        - 5
        - Uses ``call_async()`` to send requests. Processes response
          correctly. Routes action goals to the correct robot's action
          server based on the service response. Handles no-robot-found
          case gracefully.
      * - **Action Implementation (14 pts)**
        -
        -
      * - Action server -- steps
        - 5
        - Implements four steps (initialization, navigation, execution,
          returning). Publishes feedback at least once per second with
          step name and progress percentage. ``robot_beta`` executes at
          half speed.
      * - Action server -- result
        - 3
        - Returns complete result with success flag, task summary, total
          time, and result message. Publishes ``TaskCompletion`` on
          ``/fleet/task_completions``.
      * - Action server -- cancellation
        - 3
        - Checks for cancellation between steps. Stops execution, logs
          warning with current step, and returns partial result on
          cancel.
      * - Action client
        - 3
        - Sends goals to correct robot action servers. Registers
          feedback callback. Processes three tasks sequentially.
          Demonstrates cancellation of Task 2. Handles result callback.
      * - **Parameters (6 pts)**
        -
        -
      * - Parameter declaration
        - 2
        - At least three parameters declared per robot node and fleet
          manager. Parameters affect node behavior (capabilities, speed,
          payload limits, status rate).
      * - YAML config file
        - 2
        - ``config/params.yaml`` correctly formatted. Sets values for
          all declared parameters including robot registry data.
      * - Launch-time override
        - 2
        - ``robot_speed`` launch argument overrides ``robot_alpha``
          speed parameter. ``ros2 param get`` confirms the override.
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
      * - ``robot_speed`` argument
        - 1
        - ``DeclareLaunchArgument`` with default ``1.0``. Overrides
          the ``robot_alpha`` speed parameter.
      * - ``GroupAction``
        - 2
        - Robot nodes (``robot_alpha`` and ``robot_beta``) grouped in
          a ``GroupAction``.
      * - **Documentation and Quality (6 pts)**
        -
        -
      * - README.md
        - 3
        - Group members, scenario summary, system architecture diagram,
          custom interface descriptions, design decisions (including
          robot selection strategy), build/run instructions.
      * - Code quality
        - 3
        - Type hints, docstrings, ROS 2 logger with correct severity
          levels, consistent naming, no linting errors.
      * - **TOTAL**
        - **50**
        -
