====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Prerequisites
====================================================

One-time workspace and environment setup required before running any
code in this lecture.


.. dropdown:: One-Time Setup

   Clone the course workspace and configure your shell so ROS 2 can
   find all packages automatically.

   **Clone the course workspace**

   .. code-block:: console

      git clone https://github.com/zeidk/enpm605-spring-2026-ros.git ~/enpm605_ws

   **Add the setup script to your shell rc file**

   .. code-block:: console

      # Bash users
      echo "source ~/enpm605_ws/enpm605.sh" >> ~/.bashrc

      # Zsh users
      echo "source ~/enpm605_ws/enpm605.sh" >> ~/.zshrc

   **Reload your shell**

   .. code-block:: console

      source ~/.bashrc   # bash users
      source ~/.zshrc    # zsh users

   **Run the setup function once per terminal**

   .. code-block:: console

      enpm605

   .. note::

      The ``enpm605`` function must be run once in every new terminal
      before using ``ros2`` commands. It sources the ROS 2 base
      installation and the course workspace in the correct order.


.. dropdown:: Prior Lecture Dependencies

   This lecture builds on concepts from previous lectures. Ensure the
   following are in place:

   - **L11 (Gazebo):** Simulation environment configured and the
     ``enpm605_ws`` workspace built with Gazebo packages.
   - **L12 (Nav2, Lifecycle Nodes):** Nav2 stack installed and
     functional. Familiarity with lifecycle node transitions
     (``unconfigured -> inactive -> active``).

   **Rebuild the workspace**

   .. code-block:: console

      cd ~/enpm605_ws && colcon build --symlink-install
      source install/setup.bash


Introduction to Behavior Trees
====================================================

A **behavior tree (BT)** is a hierarchical, tree-structured model for
organizing and switching between tasks in a robotic system.


.. dropdown:: What Is a Behavior Tree?

   A behavior tree is a directed tree in which each node represents a
   discrete unit of decision or action. The tree is evaluated from the
   root at a fixed frequency -- each evaluation cycle is called a
   **tick**. During each tick, the root passes execution control down
   through its children according to well-defined rules. Each node
   returns one of three statuses:

   - ``SUCCESS`` -- the node completed its work.
   - ``FAILURE`` -- the node could not complete its work.
   - ``RUNNING`` -- the node is still in progress and needs more ticks.

   The parent node uses these return statuses to decide which child
   to tick next, producing complex behaviors from simple building
   blocks.

   .. tip::

      Think of a behavior tree as a **flowchart that re-evaluates from
      the top on every tick**. This constant re-evaluation is what
      makes BTs reactive to changing conditions.


.. dropdown:: Why Behavior Trees Over Finite State Machines?

   Finite State Machines (FSMs) are a common alternative for robot
   decision-making. However, they suffer from several limitations as
   system complexity grows:

   - **State explosion:** Every new behavior potentially needs
     transitions to and from every existing state.
   - **Rigid transitions:** Adding or removing a state requires
     re-wiring transitions throughout the graph.
   - **Poor modularity:** States are tightly coupled through their
     transition logic.

   Behavior trees address these issues:

   - **Modularity:** Each subtree is self-contained and can be
     developed, tested, and reused independently.
   - **Scalability:** Adding a new behavior means inserting a new
     subtree -- existing nodes are unaffected.
   - **Reactivity:** The tree re-evaluates from the root on every
     tick, so higher-priority behaviors can preempt lower-priority
     ones automatically.
   - **Readability:** The tree structure visually maps to the
     decision hierarchy.

   .. note::

      In the Nav2 stack, behavior trees replaced the FSM-based
      ``move_base`` planner from ROS 1, demonstrating industry
      preference for BTs in complex navigation systems.


.. dropdown:: BT Terminology

   - **Root:** The single top-level node. Ticking starts here.
   - **Control flow nodes:** Interior nodes that govern the
     tick order of their children (e.g., Sequence, Fallback).
   - **Execution nodes:** Leaf nodes that perform actual work.
     These are either **action nodes** (do something) or
     **condition nodes** (check something).
   - **Tick:** One evaluation cycle of the tree. The root is
     ticked at a fixed rate (e.g., 10 Hz), and the tick propagates
     down through the tree.
   - **Subtree:** Any node and its descendants. Subtrees can be
     reused across different trees.


Core Node Types
====================================================

Behavior trees use a small set of node types that compose into
arbitrarily complex behaviors.


.. dropdown:: Sequence Nodes

   A **Sequence** node ticks its children from left to right. It
   succeeds only if **all** children succeed. It fails immediately
   when any child fails.

   Tick logic:

   1. Tick the first child.
   2. If it returns ``SUCCESS``, tick the next child.
   3. If any child returns ``FAILURE``, the Sequence returns ``FAILURE``.
   4. If a child returns ``RUNNING``, the Sequence returns ``RUNNING``.
   5. If all children return ``SUCCESS``, the Sequence returns ``SUCCESS``.

   .. code-block:: text

      [Sequence]
        -> CheckBatteryLevel   (condition)
        -> NavigateToGoal      (action)
        -> PickUpObject        (action)

   In this example, the robot only navigates if the battery check
   passes, and only picks up an object if navigation succeeds.

   .. note::

      A Sequence is analogous to a logical **AND** -- all children
      must succeed for the parent to succeed.


.. dropdown:: Fallback (Selector) Nodes

   A **Fallback** (also called **Selector**) node ticks its children
   from left to right. It succeeds as soon as **any** child succeeds.
   It fails only if **all** children fail.

   Tick logic:

   1. Tick the first child.
   2. If it returns ``SUCCESS``, the Fallback returns ``SUCCESS``.
   3. If it returns ``FAILURE``, tick the next child.
   4. If all children return ``FAILURE``, the Fallback returns ``FAILURE``.
   5. If a child returns ``RUNNING``, the Fallback returns ``RUNNING``.

   .. code-block:: text

      [Fallback]
        -> FindObjectInCache    (condition)
        -> SearchForObject      (action)
        -> RequestHumanHelp     (action)

   The robot first checks the cache, then searches, and only asks
   for help if both fail.

   .. note::

      A Fallback is analogous to a logical **OR** -- the parent
      succeeds if any child succeeds.


.. dropdown:: Decorator Nodes

   A **Decorator** node has exactly one child and modifies its
   behavior or return status. Common decorators:

   - **Inverter:** Flips ``SUCCESS`` to ``FAILURE`` and vice versa.
     Passes ``RUNNING`` through unchanged.
   - **Retry:** Re-ticks the child up to *N* times if it returns
     ``FAILURE``.
   - **Timeout:** Returns ``FAILURE`` if the child does not succeed
     within a time limit.
   - **Repeat:** Ticks the child *N* times regardless of return
     status.

   .. code-block:: python

      import py_trees

      # Inverter: succeed if the child fails
      inverter = py_trees.decorators.Inverter(
          name="NotAtGoal",
          child=py_trees.behaviours.CheckBlackboardVariableValue(
              name="AtGoal?",
              check=py_trees.common.ComparisonExpression(
                  variable="at_goal", value=True, operator=operator.eq
              ),
          ),
      )

   .. tip::

      Decorators keep the tree clean by avoiding duplicated logic.
      Instead of writing a ``NotAtGoal`` condition node, invert the
      existing ``AtGoal`` condition.


.. dropdown:: Condition and Action Nodes

   **Condition nodes** are leaf nodes that check a state and return
   ``SUCCESS`` or ``FAILURE`` immediately. They never return
   ``RUNNING``.

   **Action nodes** are leaf nodes that perform work. They may return
   ``RUNNING`` across multiple ticks while the action is in progress.

   .. code-block:: text

      [Sequence]
        -> IsObjectDetected      (condition: SUCCESS or FAILURE)
        -> MoveToObject           (action: may return RUNNING)
        -> GraspObject            (action: may return RUNNING)

   .. warning::

      Condition nodes should be **side-effect free** -- they only
      read state, never modify it. If a condition modifies state,
      tree re-evaluation can produce unpredictable results.


The py_trees Library
====================================================

``py_trees`` is a pure-Python behavior tree library that provides
composites, behaviors, decorators, and a blackboard.


.. dropdown:: Installation

   Install ``py_trees`` in your ROS 2 environment:

   .. code-block:: console

      pip install py_trees

   Verify the installation:

   .. code-block:: console

      python3 -c "import py_trees; print(py_trees.__version__)"


.. dropdown:: Building a Simple Tree

   A minimal behavior tree with a Sequence composite and two
   action behaviors:

   .. code-block:: python

      import py_trees

      class PrintMessage(py_trees.behaviour.Behaviour):
          """A simple action that prints a message and succeeds."""

          def __init__(self, name: str, message: str):
              super().__init__(name)
              self._message = message

          def update(self) -> py_trees.common.Status:
              self.logger.info(f"{self.name}: {self._message}")
              return py_trees.common.Status.SUCCESS


      # Build the tree
      root = py_trees.composites.Sequence(
          name="GreetSequence",
          memory=True,
          children=[
              PrintMessage(name="Hello", message="Hello, world!"),
              PrintMessage(name="Goodbye", message="Goodbye, world!"),
          ],
      )

      # Tick the tree once
      root.tick_once()

   The ``memory`` parameter controls whether the Sequence remembers
   which child was running. When ``memory=True``, the Sequence resumes
   from the last ``RUNNING`` child. When ``memory=False``, it restarts
   from the first child on every tick.

   .. tip::

      Use ``memory=False`` when you want conditions at the start of
      the Sequence to be re-evaluated on every tick (reactive behavior).


.. dropdown:: Composites: Sequence, Selector, Parallel

   ``py_trees`` provides three composite types:

   - ``py_trees.composites.Sequence`` -- ticks children left to right,
     succeeds if all succeed.
   - ``py_trees.composites.Selector`` -- ticks children left to right,
     succeeds if any succeeds.
   - ``py_trees.composites.Parallel`` -- ticks all children
     simultaneously. The ``policy`` parameter determines success/failure:

     - ``SuccessOnAll``: succeed when all children succeed.
     - ``SuccessOnOne``: succeed when any child succeeds.

   .. code-block:: python

      parallel = py_trees.composites.Parallel(
          name="MonitorAndAct",
          policy=py_trees.common.ParallelPolicy.SuccessOnAll(),
          children=[
              MonitorBattery(name="BatteryMonitor"),
              NavigateToGoal(name="Navigate"),
          ],
      )


.. dropdown:: Custom Behaviours

   Every custom behavior extends ``py_trees.behaviour.Behaviour`` and
   implements one or more of these methods:

   - ``setup()`` -- one-time initialization (called before the first
     tick).
   - ``initialise()`` -- called the first time a behavior is ticked
     after being idle or after reset.
   - ``update()`` -- the main logic, called on every tick. Must return
     a ``py_trees.common.Status``.
   - ``terminate(new_status)`` -- cleanup when the behavior is
     interrupted or finishes.

   .. code-block:: python

      class MoveForward(py_trees.behaviour.Behaviour):
          """Move the robot forward for a fixed number of ticks."""

          def __init__(self, name: str, ticks: int = 5):
              super().__init__(name)
              self._ticks_remaining = ticks
              self._total_ticks = ticks

          def initialise(self) -> None:
              self._ticks_remaining = self._total_ticks
              self.logger.info(f"{self.name}: Starting movement")

          def update(self) -> py_trees.common.Status:
              self._ticks_remaining -= 1
              if self._ticks_remaining <= 0:
                  return py_trees.common.Status.SUCCESS
              return py_trees.common.Status.RUNNING

          def terminate(self, new_status: py_trees.common.Status) -> None:
              self.logger.info(
                  f"{self.name}: Terminated with {new_status}"
              )


.. dropdown:: Status Values

   Every behavior returns one of three statuses:

   - ``py_trees.common.Status.SUCCESS`` -- work complete.
   - ``py_trees.common.Status.FAILURE`` -- work could not be done.
   - ``py_trees.common.Status.RUNNING`` -- work in progress, tick
     again next cycle.

   .. warning::

      A behavior that never returns ``SUCCESS`` or ``FAILURE`` will
      block its parent composite indefinitely. Always ensure there is
      a termination condition.


Blackboard
====================================================

The **Blackboard** is a shared key-value store that behaviors use to
exchange data without direct coupling.


.. dropdown:: Overview

   The Blackboard pattern allows behaviors to write variables that
   other behaviors can read, enabling communication without passing
   data through the tree structure. ``py_trees`` provides a
   centralized ``Blackboard`` singleton with client-based access.

   .. code-block:: python

      import py_trees

      # Create a blackboard client
      client = py_trees.blackboard.Client(name="Demo")
      client.register_key(
          key="goal_reached", access=py_trees.common.Access.WRITE
      )
      client.goal_reached = False

      # Another client reads the same key
      reader = py_trees.blackboard.Client(name="Reader")
      reader.register_key(
          key="goal_reached", access=py_trees.common.Access.READ
      )
      print(reader.goal_reached)  # False


.. dropdown:: Reading and Writing Variables

   Behaviors interact with the Blackboard by registering keys in
   their ``__init__`` method:

   .. code-block:: python

      class SetGoalReached(py_trees.behaviour.Behaviour):
          def __init__(self, name: str):
              super().__init__(name)
              self.blackboard = self.attach_blackboard_client()
              self.blackboard.register_key(
                  key="goal_reached",
                  access=py_trees.common.Access.WRITE,
              )

          def update(self) -> py_trees.common.Status:
              self.blackboard.goal_reached = True
              return py_trees.common.Status.SUCCESS


      class CheckGoalReached(py_trees.behaviour.Behaviour):
          def __init__(self, name: str):
              super().__init__(name)
              self.blackboard = self.attach_blackboard_client()
              self.blackboard.register_key(
                  key="goal_reached",
                  access=py_trees.common.Access.READ,
              )

          def update(self) -> py_trees.common.Status:
              if self.blackboard.goal_reached:
                  return py_trees.common.Status.SUCCESS
              return py_trees.common.Status.FAILURE


.. dropdown:: Namespaced Access

   For larger trees, use **namespaces** to avoid key collisions:

   .. code-block:: python

      client = py_trees.blackboard.Client(name="NavClient")
      client.register_key(
          key="/navigation/goal_pose",
          access=py_trees.common.Access.WRITE,
      )
      client.set("/navigation/goal_pose", target_pose)

   Namespaced keys follow a path-like convention. Different subtrees
   can use separate namespaces to keep their data isolated.

   .. tip::

      Use namespaces whenever your tree has more than one subsystem
      writing to the Blackboard. This prevents accidental overwrites
      and makes the data flow explicit.


.. dropdown:: Inter-Behavior Communication

   The Blackboard is the primary mechanism for passing data between
   behaviors:

   1. A **sensor behavior** reads data from a ROS 2 topic and writes
      it to the Blackboard.
   2. A **condition behavior** reads the Blackboard value to make a
      decision.
   3. An **action behavior** reads the Blackboard to determine what
      action to take.

   .. code-block:: text

      [Sequence]
        -> ReadLidarData         (writes /sensors/closest_obstacle)
        -> IsPathClear           (reads /sensors/closest_obstacle)
        -> NavigateToGoal        (reads /navigation/goal_pose)

   This pattern keeps behaviors decoupled -- ``IsPathClear`` does not
   know where the obstacle data came from, and ``ReadLidarData`` does
   not know who will use the data.


BT + ROS 2 Integration
====================================================

``py_trees_ros`` bridges the ``py_trees`` library with ROS 2,
providing behavior wrappers for common ROS 2 communication patterns.


.. dropdown:: py_trees_ros Overview

   Install ``py_trees_ros``:

   .. code-block:: console

      sudo apt install ros-jazzy-py-trees-ros

   ``py_trees_ros`` provides:

   - A **BehaviourTree** manager that ticks the tree at a configurable
     rate using a ROS 2 timer.
   - Pre-built behaviors for subscribing to topics, publishing
     messages, calling services, and sending action goals.
   - Blackboard-to-ROS 2 bridges for monitoring Blackboard state.
   - Visualization through the ``py_trees_ros_viewer`` tool.


.. dropdown:: Subscribing to Topics from a BT

   Use ``py_trees_ros.subscribers`` to create behaviors that
   subscribe to ROS 2 topics and write data to the Blackboard:

   .. code-block:: python

      import py_trees_ros
      from sensor_msgs.msg import LaserScan

      laser_sub = py_trees_ros.subscribers.ToBlackboard(
          name="LaserToBlackboard",
          topic_name="/scan",
          topic_type=LaserScan,
          qos_profile=py_trees_ros.utilities.qos_profile_latched(),
          blackboard_variables={
              "laser_scan": None,  # writes full message
          },
      )

   The behavior subscribes to ``/scan`` and writes each incoming
   ``LaserScan`` message to the Blackboard key ``laser_scan``. Other
   behaviors can then read this key to make decisions.


.. dropdown:: Publishing from a BT

   For publishing, create a custom behavior that holds a ROS 2
   publisher:

   .. code-block:: python

      import rclpy
      from geometry_msgs.msg import Twist
      import py_trees
      import py_trees_ros

      class PublishVelocity(py_trees.behaviour.Behaviour):
          def __init__(self, name: str, node: rclpy.node.Node):
              super().__init__(name)
              self._pub = node.create_publisher(Twist, "/cmd_vel", 10)

          def update(self) -> py_trees.common.Status:
              msg = Twist()
              msg.linear.x = 0.5
              self._pub.publish(msg)
              return py_trees.common.Status.SUCCESS


.. dropdown:: Calling Actions and Services from BT Nodes

   ``py_trees_ros`` provides wrappers for ROS 2 action clients:

   .. code-block:: python

      from nav2_msgs.action import NavigateToPose
      import py_trees_ros

      navigate_action = py_trees_ros.action_clients.FromBlackboard(
          action_type=NavigateToPose,
          action_name="navigate_to_pose",
          name="NavigateAction",
          key="goal_pose",
      )

   This behavior reads the ``goal_pose`` from the Blackboard, sends
   it as a ``NavigateToPose`` action goal, and returns ``RUNNING``
   until the action server completes the goal. It returns ``SUCCESS``
   or ``FAILURE`` based on the action result.

   For services, use a custom behavior:

   .. code-block:: python

      from lifecycle_msgs.srv import ChangeState

      class ChangeLifecycleState(py_trees.behaviour.Behaviour):
          def __init__(self, name: str, node, service_name: str, transition_id: int):
              super().__init__(name)
              self._client = node.create_client(ChangeState, service_name)
              self._transition_id = transition_id
              self._future = None

          def initialise(self) -> None:
              req = ChangeState.Request()
              req.transition.id = self._transition_id
              self._future = self._client.call_async(req)

          def update(self) -> py_trees.common.Status:
              if self._future is None or not self._future.done():
                  return py_trees.common.Status.RUNNING
              result = self._future.result()
              if result.success:
                  return py_trees.common.Status.SUCCESS
              return py_trees.common.Status.FAILURE


Integration Demo
====================================================

This section walks through a complete integration that uses a behavior
tree to coordinate multiple subsystems: lifecycle node management,
Nav2 goal dispatch, and sensor monitoring.


.. dropdown:: Architecture Overview

   The integration demo uses the following architecture:

   .. code-block:: text

      [BehaviorTree (Root)]
       |
       [Sequence: SystemStartup]
       |  -> ConfigureLifecycleNodes
       |  -> ActivateLifecycleNodes
       |
       [Parallel: MainLoop]
          -> [Selector: SensorMonitor]
          |     -> CheckEmergencyStop
          |     -> CheckBatteryLow
          |     -> MonitorLidar
          |
          -> [Sequence: Navigation]
                -> GetNextGoal
                -> NavigateToGoal
                -> ReportSuccess

   The BT is the **top-level coordinator**. It:

   1. **Manages lifecycle nodes** -- transitions sensor and navigation
      nodes through the ``unconfigured -> inactive -> active``
      lifecycle.
   2. **Dispatches Nav2 goals** -- reads goal waypoints from the
      Blackboard and sends them to the Nav2 action server.
   3. **Monitors sensors** -- subscribes to sensor topics and triggers
      fallback behaviors when anomalies are detected.


.. dropdown:: Lifecycle Node Management

   The startup sequence uses service-calling behaviors to transition
   lifecycle nodes:

   .. code-block:: python

      from lifecycle_msgs.msg import Transition

      startup_sequence = py_trees.composites.Sequence(
          name="SystemStartup",
          memory=True,
          children=[
              ChangeLifecycleState(
                  name="ConfigureSensors",
                  node=ros_node,
                  service_name="/sensor_node/change_state",
                  transition_id=Transition.TRANSITION_CONFIGURE,
              ),
              ChangeLifecycleState(
                  name="ActivateSensors",
                  node=ros_node,
                  service_name="/sensor_node/change_state",
                  transition_id=Transition.TRANSITION_ACTIVATE,
              ),
              ChangeLifecycleState(
                  name="ConfigureNav",
                  node=ros_node,
                  service_name="/nav_node/change_state",
                  transition_id=Transition.TRANSITION_CONFIGURE,
              ),
              ChangeLifecycleState(
                  name="ActivateNav",
                  node=ros_node,
                  service_name="/nav_node/change_state",
                  transition_id=Transition.TRANSITION_ACTIVATE,
              ),
          ],
      )


.. dropdown:: Nav2 Goal Dispatch

   After lifecycle nodes are active, the navigation subtree reads
   waypoints from the Blackboard and sends them as Nav2 goals:

   .. code-block:: python

      class GetNextGoal(py_trees.behaviour.Behaviour):
          """Pop the next waypoint from the Blackboard queue."""

          def __init__(self, name: str):
              super().__init__(name)
              self.blackboard = self.attach_blackboard_client()
              self.blackboard.register_key(
                  key="waypoints", access=py_trees.common.Access.READ
              )
              self.blackboard.register_key(
                  key="goal_pose", access=py_trees.common.Access.WRITE
              )

          def update(self) -> py_trees.common.Status:
              waypoints = self.blackboard.waypoints
              if not waypoints:
                  return py_trees.common.Status.FAILURE
              self.blackboard.goal_pose = waypoints.pop(0)
              return py_trees.common.Status.SUCCESS

   The ``NavigateToGoal`` behavior (a ``py_trees_ros`` action client)
   reads ``goal_pose`` from the Blackboard and sends it to the Nav2
   ``navigate_to_pose`` action server.


.. dropdown:: Sensor Monitoring and Reactions

   The sensor monitoring subtree runs in parallel with navigation.
   When an emergency condition is detected, the Fallback node
   triggers an appropriate response:

   .. code-block:: python

      class CheckEmergencyStop(py_trees.behaviour.Behaviour):
          """Check if an emergency stop has been triggered."""

          def __init__(self, name: str):
              super().__init__(name)
              self.blackboard = self.attach_blackboard_client()
              self.blackboard.register_key(
                  key="emergency_stop",
                  access=py_trees.common.Access.READ,
              )

          def update(self) -> py_trees.common.Status:
              if self.blackboard.exists("emergency_stop") and \
                 self.blackboard.emergency_stop:
                  self.logger.warning("EMERGENCY STOP detected!")
                  return py_trees.common.Status.SUCCESS
              return py_trees.common.Status.FAILURE

   .. warning::

      Always place safety-critical condition checks (e.g., emergency
      stop, battery critical) at the **highest priority** position in
      a Fallback or at the start of a Sequence with ``memory=False``.
      This ensures they are re-evaluated on every tick.


.. dropdown:: Running the Integration Demo

   Build and launch the full integration demo:

   .. code-block:: console

      cd ~/enpm605_ws && colcon build --symlink-install --packages-select integration_demo
      source install/setup.bash

   Launch the demo:

   .. code-block:: console

      ros2 launch integration_demo integration_launch.py

   This starts:

   - A Gazebo simulation with the robot.
   - Lifecycle-managed sensor and navigation nodes.
   - The behavior tree coordinator.
   - The Nav2 stack.

   Monitor the BT in a separate terminal:

   .. code-block:: console

      py-trees-tree-watcher

   .. tip::

      Use ``py-trees-tree-watcher`` to see the tree structure, active
      behaviors, and return statuses in real time. This is invaluable
      for debugging integration issues.


Debugging Behavior Trees
====================================================

Effective debugging is critical when working with behavior trees,
especially in integrated systems with multiple ROS 2 nodes.


.. dropdown:: Visualization Tools

   ``py_trees`` provides several visualization options:

   - **ASCII tree rendering** for terminal-based debugging:

     .. code-block:: python

        py_trees.display.ascii_tree(root)

   - **Dot graph export** for generating tree diagrams:

     .. code-block:: python

        py_trees.display.render_dot_tree(root)

   This generates a ``.png`` file showing the tree structure with
   node types, names, and current statuses.

   - **py-trees-tree-watcher** (from ``py_trees_ros``) for live
     monitoring of a running tree.


.. dropdown:: Logging

   Enable detailed logging for behavior tree debugging:

   .. code-block:: python

      import py_trees
      py_trees.logging.level = py_trees.logging.Level.DEBUG

   With debug logging, each tick prints:

   - Which nodes are visited.
   - What status each node returns.
   - Blackboard read/write operations.

   .. tip::

      In complex trees, enable debug logging on individual subtrees
      rather than the entire tree to reduce log noise.


.. dropdown:: Common Pitfalls

   1. **Forgetting ``memory`` semantics:** Using ``memory=True`` when
      you want reactive re-evaluation causes the tree to skip
      condition checks after they pass once.

   2. **Blocking in ``update()``:** Never perform blocking operations
      (e.g., ``time.sleep()``, synchronous ROS 2 calls) in
      ``update()``. Use ``RUNNING`` and check for completion on the
      next tick.

   3. **Missing ``terminate()``:** If a behavior allocates resources
      in ``initialise()`` (e.g., starts an action), always clean up
      in ``terminate()``. Otherwise, preempted behaviors leak
      resources.

   4. **Blackboard key collisions:** Two behaviors writing the same
      key without coordination causes race conditions. Use namespaces
      and explicit access registration.

   5. **Tick rate mismatch:** If the BT ticks faster than a ROS 2
      action server can respond, you may see spurious ``RUNNING``
      states. Ensure the tick rate is appropriate for your system.

   .. warning::

      The most common integration bug is a behavior that returns
      ``SUCCESS`` before its ROS 2 action has actually completed.
      Always wait for the action server's result callback before
      returning a terminal status.
