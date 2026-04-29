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
     - Create ``mission_params.yaml``
     - Define zones, base station, and the BT tick rate. Reference:
       ``lecture10/parameters_demo/config/``.
   * - 6
     - Build the map
     - Run ``slam_toolbox`` against ``final_project_world.launch.py``,
       drive the robot through every room (with at least one loop
       closure), and save the result with
       ``ros2 run nav2_map_server map_saver_cli`` into
       ``group<N>_final/maps/final_project_map.{pgm,yaml}``. See
       :ref:`final-project-build-the-map` and Lecture 13 Exercise 1.
       The map is required for Nav2 to localize -- you cannot test
       ``NavigateToZone`` without it.

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
     - ``AdvanceZone`` and ``LogNoDetection``. These are
       straightforward (a few lines each).
   * - 10
     - Implement condition nodes
     - ``ZonesRemaining`` (queries ``ZoneManager``) and
       ``IsSurvivorDetected`` (reads from ``DetectSurvivor`` node).
       Reference: ``lecture12/bt_demo/goal_not_reached.py``.
   * - 11
     - Implement ``DetectSurvivor`` (BT node)
     - Calls the ``detect_survivor`` service using the async-poll
       pattern: ``call_async`` once, yield ``RUNNING`` until
       ``future.done()``, then read the response. **Do not**
       ``spin_until_future_complete`` inside ``update()`` -- the BT's
       executor is already spinning. Stores the result internally.
       See :ref:`final-project-bt-service-calls` for the full pattern.
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
     - Bring up Nav2 (via ``IncludeLaunchDescription``, with
       ``map:=maps/final_project_map.yaml`` and
       ``params_file:=config/nav2_params.yaml``) and start the
       three mission nodes (BT + two service servers). Load
       ``mission_params.yaml``. Declare at least one launch
       argument. References:
       ``lecture12/bt_demo/launch/drive_to_goal.py`` and
       ``lecture13/nav_demo/launch/map_nav.launch.py`` (adapt the
       Nav2 bringup -- do not invoke ``map_nav.launch.py`` directly).
   * - 16
     - End-to-end testing
     - Launch Gazebo, then your mission launch file. Verify: all
       zones visited, survivors detected, TF frames broadcast,
       report service called, robot returns to base. Use
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
     - Survivor present at multiple zones, no survivor at others
       (verify ``LogNoDetection``), all four zones visited and the
       robot returns to base. Confirm TF frames persist after the
       mission completes (``ros2 topic echo /tf_static --once``).
   * - 18
     - Code quality
     - Add docstrings, type hints, inline comments. Run Ruff.
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
       package. Write ``DetectSurvivorServer`` and
       ``ReportSurvivorServer``. Create ``mission_params.yaml`` and
       adapt ``nav2_params.yaml`` from the lecture-13 reference.
       Build and save the map with ``slam_toolbox`` /
       ``nav2_map_server``.
     - Write ``ZoneManager``. Review Lecture 12 BT code and
       Lecture 13 Nav2 code. Start ``NavigateToZone`` (the
       hardest node).
   * - **Phase 2**
     - Write ``DetectSurvivor`` (BT node, calls the service A
       wrote), ``BroadcastSurvivorTF``, and ``NotifyBase``.
       These depend on the service interfaces from Phase 1.
     - Write ``NavigateToBase``, ``AdvanceZone``,
       ``LogNoDetection``, and the two condition nodes
       (``ZonesRemaining``, ``IsSurvivorDetected``).
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

.. _final-project-bt-service-calls:

Service Calls in BT Nodes
--------------------------

For ``DetectSurvivor`` and ``NotifyBase``, you need to call a
service from within ``update()``. **Do not use**
``rclpy.spin_until_future_complete()`` here -- it raises
``RuntimeError: Executor is already spinning``.

.. important::

   ``py_trees_ros.trees.BehaviourTree.tick_tock()`` schedules ticks on
   a timer that runs *inside* the executor that is already spinning
   ``tree.node`` (via ``rclpy.spin(tree.node)`` in your entry point).
   ``rclpy.spin_until_future_complete()`` tries to enter that same
   executor a second time, which is illegal. The classic
   "block-until-done" service idiom from a standalone client therefore
   does **not** work inside a BT leaf.

The fix is the canonical asynchronous-BT pattern: submit
``call_async`` once, yield ``RUNNING`` until the future is done, then
process the response on the tick when it resolves. The future is
resolved by the same executor that drives ticks, so the BT just has
to hand control back until ``future.done()`` is ``True``.

.. code-block:: python

   def initialise(self):
       # Reset cached state for a fresh active period.
       self._future = None
       self._response = None

   def update(self):
       # First tick: submit the request, then yield.
       if self._future is None:
           if not self._client.service_is_ready():
               # Don't block; retry on the next tick.
               return py_trees.common.Status.RUNNING

           request = MyService.Request()
           # ... populate request ...
           self._future = self._client.call_async(request)
           return py_trees.common.Status.RUNNING

       # Subsequent ticks: poll the future.
       if not self._future.done():
           return py_trees.common.Status.RUNNING

       response = self._future.result()
       self._future = None  # ready for the next active period

       if response is None:
           return py_trees.common.Status.FAILURE

       # ... process response, store any results on self ...
       return py_trees.common.Status.SUCCESS

Why this works:

- ``service_is_ready()`` is a non-blocking check (unlike
  ``wait_for_service`` with a timeout, which can stall the tick).
- ``call_async`` returns immediately; the executor that is already
  spinning ``tree.node`` will deliver the response to the future
  whenever it arrives.
- Returning ``RUNNING`` hands control back to py_trees, which
  resumes ticking on the next timer fire. The future is checked
  again then.
- Resetting ``self._future = None`` after consuming the response
  ensures a follow-up active period (e.g., re-entering the same
  zone) submits a fresh request.

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

- **Root Selector** (``memory=False``): Reactive. The Selector
  re-evaluates the Patrol Sequence on every tick. Once Patrol
  fails (no zones remaining), it falls through to
  ``NavigateToBase``.
- **Patrol Sequence** (``memory=True``): Resuming. Once the robot
  reaches a zone and starts detection, the tree does not restart
  navigation on the next tick.
- **HandleDetection Selector** (``memory=False``): The detection
  result is checked fresh each time.
- **SurvivorFound Sequence** (``memory=True``): Resuming.
  ``NotifyBase`` calls ``report_survivor`` via the async-poll
  pattern (``call_async`` + ``future.done()``) and returns
  ``RUNNING`` for one or more ticks before succeeding. With
  ``memory=False``, every ``RUNNING`` tick would re-tick the
  earlier siblings -- and re-ticking ``BroadcastSurvivorTF``
  calls ``zone_manager.next_survivor_id()`` again, allocating a
  fresh ``survivor_N`` ID and broadcasting a duplicate static
  TF frame. ``memory=True`` makes the Sequence resume from the
  running child without re-evaluating earlier siblings.


Wrapping ``NavigateToBase`` in a ``OneShot``
---------------------------------------------

Because the root Selector is reactive (``memory=False``), it
re-evaluates the Patrol Sequence on every tick *forever*. Once
every zone has been visited, ``ZonesRemaining?`` returns ``FAILURE``
on every tick, the Patrol Sequence keeps failing, and the Selector
keeps falling through to the second child. Without protection,
``NavigateToBase.initialise()`` re-sends a fresh Nav2 goal at
``(0, 0)`` every tick: the controller reports "Reached the goal!"
instantly because the robot is already there, aborts, resets, and
the cycle repeats indefinitely.

Wrap ``NavigateToBase`` in
``py_trees.decorators.OneShot`` with policy
``OneShotPolicy.ON_COMPLETION`` so the decorator caches the first
terminal status of its child:

.. code-block:: python

   import py_trees

   navigate_to_base = NavigateToBase(
       name="NavigateToBase", zone_manager=zone_manager
   )
   navigate_to_base_oneshot = py_trees.decorators.OneShot(
       name="NavigateToBaseOneShot",
       child=navigate_to_base,
       policy=py_trees.common.OneShotPolicy.ON_COMPLETION,
   )

   root = py_trees.composites.Selector(
       name="MissionOrReturnToBase", memory=False
   )
   root.add_children([patrol, navigate_to_base_oneshot])

After ``NavigateToBase`` returns ``SUCCESS`` the first time,
``OneShot`` returns the cached ``SUCCESS`` on every subsequent tick
without re-initialising the child. The robot drives home exactly
once and the BT idles at ``SUCCESS`` until the operator presses
Ctrl-C.


.. _final-project-auto-seed-amcl:

Auto-Seeding AMCL with ``BasicNavigator``
------------------------------------------

AMCL refuses to publish ``map -> odom`` until it receives an initial
pose. The classic workaround is to click "2D Pose Estimate" in
RViz, but that requires manual interaction every launch and is
fragile to grade. The robust pattern is to **publish the initial
pose programmatically** at the top of the BT entry point, using
``BasicNavigator`` from ``nav2_simple_commander``.

The rosbot spawns at ``(0, 0, yaw=0)`` in the final-project world,
so the seed pose is hardcoded:

.. code-block:: python

   import math
   import rclpy
   from geometry_msgs.msg import PoseStamped
   from nav2_simple_commander.robot_navigator import BasicNavigator
   from rclpy.parameter import Parameter

   def _seed_amcl_and_wait_for_nav2() -> None:
       """Publish initialpose and block until Nav2 is ACTIVE."""
       navigator = BasicNavigator()

       # Match the rest of the mission stack: Gazebo publishes /clock,
       # so every Nav2-touching node must read it instead of system time.
       navigator.set_parameters([
           Parameter("use_sim_time", Parameter.Type.BOOL, True)
       ])

       initial_pose = PoseStamped()
       initial_pose.header.frame_id = "map"
       initial_pose.header.stamp = navigator.get_clock().now().to_msg()
       initial_pose.pose.position.x = 0.0
       initial_pose.pose.position.y = 0.0
       # yaw = 0 -> identity quaternion
       initial_pose.pose.orientation.w = 1.0

       navigator.setInitialPose(initial_pose)
       navigator.waitUntilNav2Active()
       navigator.destroy_node()

Call ``_seed_amcl_and_wait_for_nav2()`` from ``main()`` *after*
parameter loading and *before* ``tree.setup(...)``. ``BasicNavigator``
is itself an ``rclpy`` node with its own publishers/subscribers; it
does not conflict with the BT's own ``ActionClient`` because the two
are independent action clients. Destroying the navigator after the
seed call keeps the runtime tidy.

What ``waitUntilNav2Active`` does:

1. Waits for AMCL's lifecycle node to reach ``ACTIVE``.
2. Loops -- publishing ``/initialpose`` and spinning briefly --
   until ``/amcl_pose`` is received (i.e., AMCL has actually
   incorporated the seed).
3. Waits for ``bt_navigator`` to reach ``ACTIVE``.

Only after step 3 does the BT start ticking; ``NavigateToZone`` is
guaranteed to find a working Nav2 stack on its first tick.

.. important::

   Reference: ``lecture13/mapping_navigation_demo/navigation_demo_interface.py``
   uses the same ``BasicNavigator`` + ``setInitialPose`` +
   ``waitUntilNav2Active`` recipe. Adapt the
   ``localize()`` method's TF-fallback strategy if you ever need to
   seed AMCL when the spawn pose is not the origin.


.. _final-project-auto-declared-params:

Reading Auto-Declared YAML Parameters
--------------------------------------

The Parameter File uses a nested layout
(``zones.<id>.{x, y, yaw}``) that you cannot enumerate up front
because the per-zone keys are data, not code. The clean approach is
to have ROS auto-declare every key in the YAML by passing two flags
when constructing the parameter-reading node:

.. code-block:: python

   from rclpy.node import Node

   param_node = Node(
       "search_and_rescue_params",
       automatically_declare_parameters_from_overrides=True,
       allow_undeclared_parameters=True,
   )

The first flag declares every parameter loaded from
``mission_params.yaml`` (so ``zones.zone_a.x``,
``base_station.yaw``, ``tick_rate_hz`` all become readable
without explicit ``declare_parameter`` calls). The second tolerates
``get_parameter`` calls for keys that *might* not be present in
the YAML.

.. warning::

   With ``automatically_declare_parameters_from_overrides=True``,
   calling ``declare_parameter("foo", default)`` for a name
   already declared by the YAML raises::

       rclpy.exceptions.ParameterAlreadyDeclaredException:
       Parameter(s) already declared: ['foo']

   This is the single most common cause of "my BT script crashes
   silently before printing anything" in this assignment. **Guard
   every explicit ``declare_parameter`` call with**
   ``has_parameter`` so the explicit declaration acts as a fallback
   default rather than a re-declaration:

   .. code-block:: python

       if not param_node.has_parameter("tick_rate_hz"):
           param_node.declare_parameter("tick_rate_hz", 2.0)
       tick_rate_hz = param_node.get_parameter("tick_rate_hz").value

   Apply this idiom anywhere you need to provide a default for a
   parameter that the YAML *might* also supply (``zone_order``,
   ``base_station.x/y/yaw``, ``tick_rate_hz``).

Reading the zone list back into the natural ``list[dict]`` shape
``ZoneManager`` expects:

.. code-block:: python

   if not param_node.has_parameter("zone_order"):
       param_node.declare_parameter("zone_order", [""])
   zone_order = (
       param_node.get_parameter("zone_order")
                 .get_parameter_value()
                 .string_array_value
   )

   zones = []
   for zone_id in zone_order:
       zones.append({
           "id":  zone_id,
           "x":   param_node.get_parameter(f"zones.{zone_id}.x").value,
           "y":   param_node.get_parameter(f"zones.{zone_id}.y").value,
           "yaw": param_node.get_parameter(f"zones.{zone_id}.yaw").value,
       })


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

   # Test a minimal BT with just NavigateToZone
   # (requires Gazebo + Nav2 running)

   # Verify TF frames after a full run
   ros2 run tf2_ros tf2_echo map survivor_1
   ros2 run tf2_ros tf2_echo map survivor_2

**Launch order for full testing:**

.. code-block:: console

   # Terminal 1: Gazebo
   ros2 launch rosbot_gazebo final_project_world.launch.py

   # Terminal 2: Mission (this single launch file brings up Nav2
   # with your saved map under
   # group<N>_final/maps/final_project_map.yaml, the two service
   # servers, and the BT node)
   ros2 launch group<N>_final search_and_rescue.launch.py

.. tip::

   **Killing hanging processes between iterations.** ``Ctrl-C`` in
   the launch terminal sometimes leaves Nav2 lifecycle nodes,
   ``rviz2``, or the BT process running in the background. They
   then re-bind to action servers / TF / topics on the next
   ``ros2 launch`` and you get bizarre symptoms (duplicate logs,
   "node already exists", AMCL refusing the new
   ``/initialpose``). One-liner to clean up:

   .. code-block:: console

      pkill -9 -f "nav2|amcl|map_server|lifecycle|controller_server|planner_server|bt_navigator|behavior_server|smoother_server|route_server|opennav|collision_monitor|velocity_smoother|waypoint_follower|rviz2"

   Verify the cleanup with ``ros2 node list`` -- it should print
   nothing (or only what Gazebo brings up). Then re-launch.
