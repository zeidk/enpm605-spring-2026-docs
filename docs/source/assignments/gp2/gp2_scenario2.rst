====================================================
Scenario 2: Warehouse Pick-and-Place Coordinator
====================================================


Domain
======

A warehouse automation system manages an inventory of items across
multiple storage locations and coordinates a robot arm to pick items
from shelves and place them at packing stations. An inventory service
provides real-time stock information, and a pick-and-place action
executes the physical manipulation with progress feedback.

The system models a typical order fulfillment workflow: a coordinator
node receives an order, queries the inventory to locate the item,
dispatches the robot arm to pick it up and deliver it, and tracks order
completion statistics.


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
      * - ``coordinator_node``
        - Acts as the service client and action client. On startup (or
          via a timer), sends a service request to query the inventory
          for a specific item. If the item is in stock, sends an action
          goal to execute a pick-and-place operation. Logs feedback from
          the action server as the operation progresses. Demonstrates
          cancellation by canceling one pick-and-place operation
          mid-execution.
      * - ``inventory_server``
        - Hosts the service server for inventory queries. Maintains an
          in-memory inventory database (loaded from parameters) mapping
          item names to storage locations and quantities. Supports
          querying item availability and decrementing stock when an item
          is picked.
      * - ``arm_controller``
        - Hosts the action server for pick-and-place operations.
          Simulates the robot arm moving to the pick location, grasping
          the item, moving to the place location, and releasing the
          item. Publishes progress feedback throughout the operation.
      * - ``order_tracker``
        - Subscribes to ``/warehouse/completed_orders`` (published by
          ``arm_controller`` upon successful placement). Tracks completed
          orders and publishes a summary on ``/warehouse/stats`` at
          0.2 Hz.
      * - ``debug_monitor`` *(optional, conditional)*
        - Subscribes to ``/warehouse/stats`` and logs order statistics.
          Started only when the launch argument ``enable_debug`` is
          ``true``.

   **Services**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Service
        - Interface
        - Description
      * - ``/warehouse/query_inventory``
        - ``QueryInventory.srv``
        - Request: item name. Response: whether the item is in stock,
          the storage location, current quantity, and a message string.

   **Actions**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Action
        - Interface
        - Description
      * - ``/warehouse/pick_and_place``
        - ``PickAndPlace.action``
        - Goal: item name, pick location, and place location. Feedback:
          current phase, progress percentage, and status message. Result:
          success flag, item name, total time elapsed, and result
          message.

   **Topics**

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - Topic
        - Message Type
        - Description
      * - ``/warehouse/completed_orders``
        - ``CompletedOrder.msg``
        - Published by ``arm_controller`` when a pick-and-place
          operation completes. Contains item name, pick/place locations,
          elapsed time, and timestamp.
      * - ``/warehouse/stats``
        - ``std_msgs/msg/String``
        - Published by ``order_tracker`` with counts of completed
          orders, total items moved, and average operation time.


.. dropdown:: Custom Interfaces
   :open:

   Create the following interface files in the ``group<N>_gp2_interfaces``
   package.

   **msg/CompletedOrder.msg**

   .. code-block:: text

      string item_name
      string pick_location
      string place_location
      float64 elapsed_time
      string timestamp

   **srv/QueryInventory.srv**

   .. code-block:: text

      # Request
      string item_name
      ---
      # Response
      bool in_stock
      string storage_location
      int32 quantity
      string message

   **action/PickAndPlace.action**

   .. code-block:: text

      # Goal
      string item_name
      string pick_location
      string place_location
      ---
      # Result
      bool success
      string item_name
      float64 total_time
      string result_message
      ---
      # Feedback
      string current_phase
      float64 progress_percentage
      string status_message


.. dropdown:: Detailed Requirements
   :open:

   1. **Service -- QueryInventory**: The ``inventory_server`` must
      declare a parameter ``inventory`` loaded from
      ``config/params.yaml``. This parameter stores a list of item
      records, each with an item name, storage location, and quantity
      (e.g., ``[{name: "widget_A", location: "shelf_1", qty: 10}, ...]``).
      When the service receives a request:

      - If the item is found and ``quantity > 0``, return
        ``in_stock=True``, the storage location, the current quantity,
        and a confirmation message.
      - If the item is found but ``quantity == 0``, return
        ``in_stock=False``, the storage location, quantity ``0``, and
        a message such as ``"Item 'widget_A' is out of stock."``.
      - If the item is not found, return ``in_stock=False``, an empty
        location, quantity ``0``, and an error message such as
        ``"Item 'gadget_X' not found in inventory."``.

      .. note::

         The inventory parameter format can be simplified. For example,
         use three parallel lists: ``item_names``, ``item_locations``,
         and ``item_quantities``. Alternatively, encode inventory as a
         YAML dictionary. Choose a format that is easy to parse in
         Python.

   2. **Action -- PickAndPlace**: The action server simulates a
      multi-phase pick-and-place operation:

      - **Phase 1 -- Move to Pick** (0--25%): Simulates the arm moving
        to the pick location. Publish feedback every 0.5 seconds with
        phase ``"moving_to_pick"`` and increasing progress.
      - **Phase 2 -- Grasping** (25--50%): Simulates closing the gripper
        and securing the item. Publish feedback with phase
        ``"grasping"``.
      - **Phase 3 -- Move to Place** (50--75%): Simulates the arm
        moving to the place location. Publish feedback with phase
        ``"moving_to_place"``.
      - **Phase 4 -- Releasing** (75--100%): Simulates opening the
        gripper and placing the item. Publish feedback with phase
        ``"releasing"``. On completion, publish a ``CompletedOrder``
        message on ``/warehouse/completed_orders``.

   3. **Cancellation**: The action server must check for cancellation
      between phases. If canceled, log a warning, stop execution, and
      return a result with ``success=False`` and a message indicating
      at which phase the operation was canceled. The ``coordinator_node``
      must demonstrate cancellation by canceling the second
      pick-and-place operation 2 seconds after sending the goal.

   4. **Inventory decrement**: When the ``arm_controller`` successfully
      completes a pick-and-place, the ``coordinator_node`` should call
      the ``QueryInventory`` service again for the same item to verify
      the stock level. The ``inventory_server`` must decrement the
      quantity by 1 when a pick is confirmed (this can be triggered by
      subscribing to ``/warehouse/completed_orders`` or by adding a
      second service). Document your approach in ``README.md``.

   5. **Parameters** (loaded from ``config/params.yaml``):

      - ``inventory_server``:

        - ``item_names``: list of item name strings.
        - ``item_locations``: list of storage location strings.
        - ``item_quantities``: list of integer quantities.

      - ``arm_controller``:

        - ``arm_speed``: float (affects simulated movement time,
          default ``1.0``).

      - ``order_tracker``:

        - ``stats_rate``: float (rate in Hz for publishing statistics,
          default ``0.2``).

   6. **Launch files**:

      - ``system.launch.py``: starts ``inventory_server``,
        ``arm_controller``, ``coordinator_node``, and ``order_tracker``.
        Loads ``config/params.yaml`` for all parameterized nodes.
      - ``enable_debug`` argument (default ``false``): conditionally
        starts the ``debug_monitor`` node using ``IfCondition``.
      - ``arm_speed`` argument (default ``1.0``): overrides the
        ``arm_controller``'s ``arm_speed`` parameter.
      - Server nodes (``inventory_server`` and ``arm_controller``)
        grouped in a ``GroupAction``.


.. dropdown:: Expected Behavior
   :open:

   **Normal operation:**

   .. code-block:: text

      [INFO] [<timestamp>] [coordinator_node]: Querying inventory for widget_A
      [INFO] [<timestamp>] [inventory_server]: QueryInventory for 'widget_A' -- in stock at shelf_1 (qty: 10)
      [INFO] [<timestamp>] [coordinator_node]: Item in stock at shelf_1. Sending pick-and-place goal...
      [INFO] [<timestamp>] [arm_controller]: Pick-and-place goal accepted: widget_A from shelf_1 to packing_station_2
      [INFO] [<timestamp>] [coordinator_node]: Feedback -- moving_to_pick: 10.0%
      [INFO] [<timestamp>] [coordinator_node]: Feedback -- grasping: 35.0%
      [INFO] [<timestamp>] [coordinator_node]: Feedback -- moving_to_place: 60.0%
      [INFO] [<timestamp>] [coordinator_node]: Feedback -- releasing: 90.0%
      [INFO] [<timestamp>] [arm_controller]: Pick-and-place complete for widget_A (8.5 s)
      [INFO] [<timestamp>] [coordinator_node]: Result -- widget_A placed at packing_station_2 in 8.5 s
      [INFO] [<timestamp>] [order_tracker]: Order completed: widget_A (shelf_1 -> packing_station_2)

   **Item not found:**

   .. code-block:: text

      [INFO] [<timestamp>] [coordinator_node]: Querying inventory for gadget_X
      [WARN] [<timestamp>] [inventory_server]: QueryInventory for 'gadget_X' -- not found
      [WARN] [<timestamp>] [coordinator_node]: Item not available: "Item 'gadget_X' not found in inventory."

   **Cancellation:**

   .. code-block:: text

      [INFO] [<timestamp>] [coordinator_node]: Sending pick-and-place goal for bolt_M8
      [INFO] [<timestamp>] [coordinator_node]: Feedback -- moving_to_pick: 10.0%
      [INFO] [<timestamp>] [coordinator_node]: Canceling pick-and-place for bolt_M8...
      [WARN] [<timestamp>] [arm_controller]: Pick-and-place canceled for bolt_M8 at phase: grasping (30.0%)
      [INFO] [<timestamp>] [coordinator_node]: Operation canceled. Partial result received.

   **Verification commands:**

   .. code-block:: console

      ros2 launch group<N>_gp2 system.launch.py
      ros2 launch group<N>_gp2 system.launch.py enable_debug:=true
      ros2 launch group<N>_gp2 system.launch.py arm_speed:=2.0
      ros2 service list
      ros2 service call /warehouse/query_inventory group<N>_gp2_interfaces/srv/QueryInventory "{item_name: 'widget_A'}"
      ros2 action list
      ros2 action send_goal /warehouse/pick_and_place group<N>_gp2_interfaces/action/PickAndPlace "{item_name: 'widget_A', pick_location: 'shelf_1', place_location: 'packing_station_2'}" --feedback
      ros2 interface show group<N>_gp2_interfaces/srv/QueryInventory
      ros2 interface show group<N>_gp2_interfaces/action/PickAndPlace
      ros2 param list
      ros2 param get /arm_controller arm_speed


.. dropdown:: Scenario 2 Grading Rubric
   :open:

   This rubric details how the 50 points map to Scenario 2 deliverables.

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
      * - ``CompletedOrder.msg``
        - 2
        - Correctly defined with all required fields. Builds
          successfully with ``colcon build``. Visible via
          ``ros2 interface show``.
      * - ``QueryInventory.srv``
        - 3
        - Request/response fields correctly defined. Includes
          ``in_stock``, ``storage_location``, ``quantity``, and
          ``message`` in response.
      * - ``PickAndPlace.action``
        - 3
        - Goal, result, and feedback sections correctly defined.
          Feedback includes ``current_phase``, ``progress_percentage``,
          and ``status_message``.
      * - **Service Implementation (10 pts)**
        -
        -
      * - Service server
        - 5
        - ``QueryInventory`` service validates against parameter-loaded
          inventory. Returns correct stock status, location, and
          quantity. Handles item-not-found and out-of-stock cases with
          descriptive messages.
      * - Service client
        - 5
        - Uses ``call_async()`` to send requests. Processes response
          correctly. Handles in-stock and not-available responses.
          Proceeds to send action goal only when item is in stock.
      * - **Action Implementation (14 pts)**
        -
        -
      * - Action server -- phases
        - 5
        - Implements four phases (move to pick, grasping, move to place,
          releasing). Publishes feedback at least once per second with
          phase name and progress percentage.
      * - Action server -- result
        - 3
        - Returns complete result with success flag, item name, total
          time, and result message. Publishes ``CompletedOrder`` on
          ``/warehouse/completed_orders``.
      * - Action server -- cancellation
        - 3
        - Checks for cancellation between phases. Stops execution, logs
          warning with current phase, and returns partial result on
          cancel.
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
          ``self.declare_parameter()``. Parameters affect node behavior
          (inventory data, arm speed, stats rate).
      * - YAML config file
        - 2
        - ``config/params.yaml`` correctly formatted. Sets values for
          all declared parameters including inventory data.
      * - Launch-time override
        - 2
        - ``arm_speed`` launch argument overrides the parameter.
          ``ros2 param get`` confirms the override.
      * - **Launch File (6 pts)**
        -
        -
      * - ``system.launch.py``
        - 2
        - Starts all required nodes. Loads ``config/params.yaml``. All
          nodes use ``output="screen"`` and ``emulate_tty=True``.
      * - ``enable_debug`` argument
        - 1
        - ``DeclareLaunchArgument`` with default ``false``. Debug
          monitor node uses ``IfCondition``.
      * - ``arm_speed`` argument
        - 1
        - ``DeclareLaunchArgument`` with default ``1.0``. Overrides
          the ``arm_controller`` parameter.
      * - ``GroupAction``
        - 2
        - Server nodes (``inventory_server`` and ``arm_controller``)
          grouped in a ``GroupAction``.
      * - **Documentation and Quality (6 pts)**
        -
        -
      * - README.md
        - 3
        - Group members, scenario summary, system architecture diagram,
          custom interface descriptions, design decisions (including
          inventory decrement approach), build/run instructions.
      * - Code quality
        - 3
        - Type hints, docstrings, ROS 2 logger with correct severity
          levels, consistent naming, no linting errors.
      * - **TOTAL**
        - **50**
        -
