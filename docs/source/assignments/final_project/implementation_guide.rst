====================================================
Implementation Guide
====================================================

This page describes the recommended implementation order, how to
divide work between two team members, and key patterns to follow.
Read the full :doc:`requirements` first.


Recommended Implementation Order
=================================

The project has dependencies between components. Follow this order
to avoid blocking your partner and to enable testing at each step.

**Phase 1: Foundation (Days 1-3)**

.. list-table::
   :widths: 5 40 55
   :header-rows: 1
   :class: compact-table

   * - Step
     - Task
     - Details
   * - 1
     - Create package skeletons
     - Create ``group<N>_final_interfaces/`` (CMake) and
       ``group<N>_final/`` (ament_python) inside
       ``~/enpm605_ws/src/final_project/``. Register both in
       ``final_project_meta/package.xml``. Verify the stack builds.
   * - 2
     - Define service interfaces
     - Create ``DetectSurvivor.srv`` and ``ReportSurvivor.srv``.
       Build and verify with ``ros2 interface show``. Reference:
       ``lecture10/custom_interfaces/``.
   * - 3
     - Implement service servers
     - Write ``DetectSurvivorServer`` and ``ReportSurvivorServer``.
       Test them independently with ``ros2 service call``.
   * - 4
     - Implement ``ZoneManager``
     - Plain Python class. Test it with a simple script that calls
       its methods. No ROS 2 needed.
   * - 5
     - Implement battery simulator
     - Write the ``BatterySimulator`` node. Test with
       ``ros2 topic echo /battery_state``.
   * - 6
     - Create ``mission_params.yaml``
     - Define zones, base station, thresholds. Reference:
       ``lecture10/parameters_demo/config/``.

**Phase 2: BT Leaf Nodes (Days 4-7)**

Build and test nodes incrementally. Each node can be tested in
isolation before assembling the full tree.

.. list-table::
   :widths: 5 40 55
   :header-rows: 1
   :class: compact-table

   * - Step
     - Task
     - Details
   * - 7
     - Implement ``NavigateToZone``
     - **The hardest node.** Uses ``rclpy.action.ActionClient`` to
       send ``NavigateToPose`` goals to Nav2. Study
       ``lecture13/mapping_navigation_demo/navigation_demo_interface.py``
       for the Nav2 interaction pattern (``goToPose``, feedback,
       result checking). Adapt it into a BT node that returns
       ``RUNNING`` / ``SUCCESS`` / ``FAILURE``. Test by assembling
       a minimal tree with just this node.
   * - 8
     - Implement ``NavigateToBase``
     - Nearly identical to ``NavigateToZone`` but uses
       ``zone_manager.base_pose()``. Can reuse most of the code.
   * - 9
     - Implement simple action nodes
     - ``Wait``, ``SkipZone``, ``AdvanceZone``, ``LogNoDetection``.
       These are straightforward (a few lines each).
   * - 10
     - Implement condition nodes
     - ``CheckBattery`` (subscribes to ``/battery_state``),
       ``ZonesRemaining`` (queries ``ZoneManager``),
       ``IsSurvivorDetected`` (reads from ``DetectSurvivor``
       node). Reference:
       ``lecture12/bt_demo/goal_not_reached.py``.
   * - 11
     - Implement ``DetectSurvivor`` (BT node)
     - Calls the ``detect_survivor`` service synchronously using
       ``call_async`` + ``spin_until_future_complete``. Stores
       the result internally. Reference:
       ``lecture10/service_demo/`` for service client patterns.
   * - 12
     - Implement ``BroadcastSurvivorTF``
     - Creates a ``tf2_ros.StaticTransformBroadcaster`` in
       ``setup()``. Builds and sends a ``TransformStamped`` in
       ``update()``. Reference:
       ``lecture11/frame_demo/`` for TF broadcasting.
   * - 13
     - Implement ``NotifyBase``
     - Calls the ``report_survivor`` service. Similar pattern to
       ``DetectSurvivor``.

**Phase 3: Integration (Days 8-11)**

.. list-table::
   :widths: 5 40 55
   :header-rows: 1
   :class: compact-table

   * - Step
     - Task
     - Details
   * - 14
     - Assemble the full BT
     - Write ``main_search_and_rescue.py``. Read parameters, build
       the ``ZoneManager``, create all BT nodes, assemble the tree
       structure, wrap in ``py_trees_ros.trees.BehaviourTree``,
       and run ``tick_tock()``. Reference:
       ``lecture12/bt_demo/scripts/main_drive_to_goal.py``.
   * - 15
     - Write the launch file
     - Start all four nodes (BT, two servers, battery simulator).
       Load ``mission_params.yaml``. Declare launch arguments.
       Reference:
       ``lecture12/bt_demo/launch/drive_to_goal.py`` and
       ``lecture13/mapping_navigation_demo/launch/navigation.launch.py``.
   * - 16
     - End-to-end testing
     - Launch Gazebo + Nav2 + your mission. Verify: all zones
       visited, survivors detected, TF frames broadcast, report
       service called, battery return works. Use
       ``ros2 run tf2_ros tf2_echo map survivor_1`` to verify
       TF frames.

**Phase 4: Polish (Days 12-14)**

.. list-table::
   :widths: 5 40 55
   :header-rows: 1
   :class: compact-table

   * - Step
     - Task
     - Details
   * - 17
     - Test edge cases
     - Navigation failure (blocked path) triggers recovery (wait
       + retry + skip). Low battery mid-mission returns to base.
       Adjust ``battery_drain_rate`` to trigger low battery at
       the right time.
   * - 18
     - Code quality
     - Add docstrings, type hints, inline comments. Run Ruff.
       Remove ``__pycache__/`` directories.
   * - 19
     - Write README.md
     - Contributions section + BT design explanation (``memory``
       flag choices).
   * - 20
     - Package and submit
     - Follow the :doc:`submission` checklist.


Suggested Work Division
========================

For a team of two, the work divides naturally into **infrastructure**
and **behavior tree** roles. Both team members should understand
the full system, but each focuses on their area.

.. list-table::
   :widths: 15 42 43
   :header-rows: 1
   :class: compact-table

   * - Role
     - Student A: Infrastructure
     - Student B: Behavior Tree
   * - **Phase 1**
     - Create both package skeletons and the CMake interfaces
       package. Write ``DetectSurvivorServer``,
       ``ReportSurvivorServer``, and ``BatterySimulator``.
       Create ``mission_params.yaml``.
     - Write ``ZoneManager``. Review Lecture 12 BT code and
       Lecture 13 Nav2 code. Start ``NavigateToZone`` (the
       hardest node).
   * - **Phase 2**
     - Write ``DetectSurvivor`` (BT node, calls the service A
       wrote), ``BroadcastSurvivorTF``, and ``NotifyBase``.
       These depend on the service interfaces from Phase 1.
     - Write ``NavigateToBase``, ``Wait``, ``SkipZone``,
       ``AdvanceZone``, ``LogNoDetection``, and all three
       condition nodes (``CheckBattery``, ``ZonesRemaining``,
       ``IsSurvivorDetected``).
   * - **Phase 3**
     - Write the launch file. Help with integration testing.
     - Assemble the full BT in the entry point script. Integrate
       with Nav2.
   * - **Phase 4**
     - Docstrings and type hints on infrastructure code.
       Write README contributions section.
     - Docstrings and type hints on BT code. Write README
       BT design section. Test edge cases.


Key Patterns and Pitfalls
==========================

NavigateToZone: The Hardest Node
---------------------------------

This is the most complex BT node because it wraps an asynchronous
Nav2 action client inside a synchronous BT ``update()`` method.

**Pattern:**

1. In ``setup()``, create an ``ActionClient`` for
   ``NavigateToPose``.
2. In ``initialise()`` (called when the node transitions from idle
   to active), send the goal with ``send_goal_async()`` and store
   the future. Reset ``_done`` and ``_success`` flags.
3. In ``update()`` (called every tick), check if the goal has
   completed. Return ``RUNNING`` if still in progress, ``SUCCESS``
   or ``FAILURE`` when done.
4. In ``terminate()``, cancel the Nav2 goal if still active.

**Study:**
``lecture13/mapping_navigation_demo/navigation_demo_interface.py``
shows the high-level Nav2 pattern with ``BasicNavigator``. For BT
nodes, you need the lower-level ``ActionClient`` approach because
``update()`` must be non-blocking (return immediately, not wait
in a loop).

.. important::

   Do **not** call ``BasicNavigator.goToPose()`` inside a BT
   ``update()`` — it blocks until the goal completes, which
   freezes the entire behavior tree. Use the asynchronous
   ``ActionClient`` pattern with callbacks instead.

Service Calls in BT Nodes
--------------------------

For ``DetectSurvivor`` and ``NotifyBase``, you need to call a
service from within ``update()``. Use
``call_async()`` + ``rclpy.spin_until_future_complete()`` for a
synchronous-style call:

.. code-block:: python

   future = self._client.call_async(request)
   rclpy.spin_until_future_complete(self._node, future, timeout_sec=5.0)
   if future.result() is not None:
       response = future.result()
       # process response
   else:
       # service call failed

This blocks briefly but is acceptable for a quick service call.

TF Broadcasting
----------------

``BroadcastSurvivorTF`` uses ``tf2_ros.StaticTransformBroadcaster``
to publish a frame. The key fields in ``TransformStamped``:

.. code-block:: python

   from tf2_ros import StaticTransformBroadcaster
   from geometry_msgs.msg import TransformStamped

   # In setup():
   self._broadcaster = StaticTransformBroadcaster(kwargs['node'])

   # In update():
   t = TransformStamped()
   t.header.stamp = self._node.get_clock().now().to_msg()
   t.header.frame_id = "map"          # parent frame
   t.child_frame_id = "survivor_1"    # new frame name
   t.transform.translation.x = sx     # survivor x
   t.transform.translation.y = sy     # survivor y
   t.transform.rotation.w = 1.0       # identity rotation
   self._broadcaster.sendTransform(t)

Verify with: ``ros2 run tf2_ros tf2_echo map survivor_1``

Sharing Data Without Blackboard
--------------------------------

Since this project does not use the py_trees blackboard, data is
shared via **constructor injection**:

- ``ZoneManager`` is passed to all nodes that need zone state.
- ``DetectSurvivor`` (the BT action node) stores its result
  internally and exposes ``was_found()`` and ``survivor_pose()``
  methods.
- ``IsSurvivorDetected`` (condition) and ``BroadcastSurvivorTF``
  (action) hold a reference to the ``DetectSurvivor`` instance
  and call these methods.

.. code-block:: python

   # In the entry point script:
   detect = DetectSurvivor(name='Detect', zone_manager=zone_mgr)
   is_found = IsSurvivorDetected(name='Found?', detect_node=detect)
   broadcast = BroadcastSurvivorTF(name='TF', detect_node=detect,
                                    zone_manager=zone_mgr)

Memory Flag Choices
--------------------

- **Root Sequence** (``memory=False``): Reactive. ``CheckBattery``
  is re-evaluated every tick. If battery drops mid-mission, the
  tree reacts immediately.
- **Patrol Sequence** (``memory=True``): Resuming. Once the robot
  reaches a zone and starts detection, the tree does not restart
  navigation on the next tick.
- **NavigateWithRecovery Selector** (``memory=True``): Once the
  primary navigation times out, the Selector stays on recovery
  (Wait + retry) rather than retrying immediately.
- **HandleDetection Selector** (``memory=False``): The detection
  result is checked fresh each time.


Testing Tips
=============

**Test incrementally.** Do not try to assemble the full tree before
testing individual nodes.

.. code-block:: console

   # Test service servers independently
   ros2 run group<N>_final detect_survivor_server_exe &
   ros2 service call /detect_survivor \
       group<N>_final_interfaces/srv/DetectSurvivor \
       "{zone_id: 'zone_a'}"

   # Test battery simulator
   ros2 run group<N>_final battery_simulator_exe &
   ros2 topic echo /battery_state --field percentage

   # Test a minimal BT with just NavigateToZone
   # (requires Gazebo + Nav2 running)

   # Verify TF frames after a full run
   ros2 run tf2_ros tf2_echo map survivor_1
   ros2 run tf2_ros tf2_echo map survivor_2

**Launch order for full testing:**

.. code-block:: console

   # Terminal 1: Gazebo
   ros2 launch rosbot_gazebo final_project_world.launch.py

   # Terminal 2: Nav2
   ros2 launch rosbot_gazebo navigation.launch.py \
       map:=/path/to/final_project_world.yaml

   # Terminal 3: Mission
   ros2 launch group<N>_final search_and_rescue.launch.py
