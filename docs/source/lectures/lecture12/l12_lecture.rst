====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}

Prerequisites
====================================================

Ensure you have followed the simulation instructions and have
everything set up before running any code in this lecture.


.. dropdown:: Before You Start
   :open:

   - Do a ``git pull`` (native installation only).
   - Recompile Lecture 12 packages:

   .. code-block:: console

      colcon build --symlink-install \
          --cmake-args -DCMAKE_BUILD_TYPE=Release \
          --packages-up-to lecture12_meta

   - Source ``.bashrc``.
   - Verify Gazebo launches cleanly:

   .. code-block:: console

      ros2 launch rosbot_gazebo empty_world.launch.py


Namespaces
====================================================

A **namespace** is a prefix applied to a ROS 2 node and all its
associated entities (topics, services, parameters). It provides a
hierarchical organization that prevents naming conflicts when running
multiple instances of the same node.

Without namespaces, running two camera nodes produces a topic conflict.
With namespaces, each instance lives in its own isolated prefix.

.. admonition:: Resources
   :class: resources

   - `ROS 2 Launch: Large Projects
     <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects.html>`_
   - `ROS 2 Design: Topic and Service Names
     <https://design.ros2.org/articles/topic_and_service_names.html>`_


The Problem: Identical Topic Names
----------------------------------------------------

Consider a robot with three cameras. Each runs the same ``camera_node``
and publishes on ``/image_raw``. Running two instances immediately
causes a conflict: both nodes compete for the same topic, and
subscribers receive data from whichever node happened to publish last.

.. note::

   A namespace solves this by prepending a unique prefix.
   ``camera_node`` under namespace ``/front`` publishes on
   ``/front/image_raw``; under ``/rear`` it publishes on
   ``/rear/image_raw``. The node code is identical in both cases.


What a Namespace Affects
----------------------------------------------------

When you apply namespace ``/rear`` to a node:

- The node name becomes ``/rear/camera_node``.
- Every **relative** topic or service (e.g., ``image_raw``) becomes
  ``/rear/image_raw``.
- Parameters are stored under the fully-qualified node name
  ``/rear/camera_node``.
- **Absolute** topics (starting with ``/``) are *not* affected by the
  namespace.

.. important::

   If a topic is defined with a leading slash (e.g., ``/image_raw``),
   the namespace has no effect on it. Always use relative topic names
   inside node code if you intend the namespace to apply.


Applying Namespaces
----------------------------------------------------

Namespaces can be applied from the command line at launch time, or
declared inside a Python launch file.

.. only:: html

   .. figure:: /_static/images/L12/namespace_light.png
      :alt: Namespace applied to node and topic names
      :width: 60%
      :align: center
      :class: only-light

      Namespace applied to node and topic names.

   .. figure:: /_static/images/L12/namespace_dark.png
      :alt: Namespace applied to node and topic names
      :width: 60%
      :align: center
      :class: only-dark

      Namespace applied to node and topic names.

**CLI: ``--ros-args -r __ns``**

.. code-block:: console

   ros2 run namespace_demo camera_demo_exe --ros-args -r __ns:=/rear

- ``__ns`` is a special remapping target for the namespace.
- Verify with ``ros2 node list`` and ``ros2 topic list``.

.. dropdown:: Demonstration: CLI Namespace
   :open:

   .. list-table::
      :widths: 5 50 45
      :header-rows: 1

      * -
        - Command
        - What to observe
      * - T1
        - ``ros2 run namespace_demo camera_demo_exe --ros-args -r __ns:=/front``
        - Node starts as ``/front/camera_node``
      * - T2
        - ``ros2 run namespace_demo camera_demo_exe --ros-args -r __ns:=/rear``
        - Second instance starts as ``/rear/camera_node``
      * - T3
        - ``ros2 node list``
        - Both ``/front/camera_node`` and ``/rear/camera_node`` appear
      * - T3
        - ``ros2 topic list``
        - ``/front/image_raw`` and ``/rear/image_raw`` (isolated)
      * - T3
        - ``rqt_graph``
        - Two separate nodes, each publishing on its own namespaced topic

**Launch File: ``namespace`` Argument**

.. code-block:: python

   front_camera = Node(
       package='namespace_demo',
       executable='camera_demo_exe',
       namespace='front',
       output='screen',
   )
   rear_camera = Node(
       package='namespace_demo',
       executable='camera_demo_exe',
       namespace='rear',
       output='screen',
   )

.. dropdown:: Demonstration: Launch File Namespace
   :open:

   .. list-table::
      :widths: 5 50 45
      :header-rows: 1

      * -
        - Command
        - What to observe
      * - T1
        - ``ros2 launch namespace_demo multi_camera.launch.py``
        - Both camera nodes start in separate namespaces
      * - T2
        - ``ros2 node list``
        - ``/front/camera_node`` and ``/rear/camera_node`` appear
      * - T2
        - ``ros2 topic list``
        - ``/front/image_raw`` and ``/rear/image_raw`` (same result as CLI)


Remapping
====================================================

**Remapping** lets you change the name of any ROS 2 entity (node name,
topic, service, parameter) at runtime without modifying the node's
source code. It is the primary mechanism for adapting existing nodes to
new system architectures.

.. note::

   Every node in a ROS 2 system must have a unique name. Node remapping
   lets you run the same executable under a different name without
   touching the code.

.. admonition:: Resources
   :class: resources

   - `ROS 2: Node Name Remapping
     <https://docs.ros.org/en/jazzy/How-To-Guides/Node-name-remapping.html>`_
   - `ROS 2: Node Arguments
     <https://docs.ros.org/en/jazzy/Guides/Node-arguments.html>`_


Node Remapping
----------------------------------------------------

Node remapping assigns a new name to a running node without modifying
its source code. This is essential when launching multiple instances of
the same executable.

**CLI: ``--ros-args -r __node``**

.. code-block:: console

   ros2 run remapping_demo camera_demo_exe --ros-args -r __node:=front_camera

- ``__node`` is the special remapping target for the node name.
- The node that would normally be named ``/camera_node`` is now
  ``/front_camera``.
- All parameters are stored under the remapped name.
- All CLI commands must use the new name:
  ``ros2 node info /front_camera``.

.. dropdown:: Demonstration: CLI Node Remapping
   :open:

   .. list-table::
      :widths: 5 55 40
      :header-rows: 1

      * -
        - Command
        - What to observe
      * - T1
        - ``ros2 run remapping_demo camera_demo_exe --ros-args -r __node:=front_camera``
        - Node starts as ``/front_camera`` instead of ``/camera_node``
      * - T2
        - ``ros2 run remapping_demo camera_demo_exe --ros-args -r __node:=rear_camera``
        - Second instance starts as ``/rear_camera`` (no name conflict)
      * - T3
        - ``ros2 node list``
        - Both ``/front_camera`` and ``/rear_camera`` appear

**Launch File: ``name`` Argument**

.. code-block:: python

   front_camera = Node(
       package="remapping_demo",
       executable="camera_demo_exe",
       name="front_camera",
       output="screen",
   )

   rear_camera = Node(
       package="remapping_demo",
       executable="camera_demo_exe",
       name="rear_camera",
       output="screen",
   )

.. dropdown:: Demonstration: Launch File Node Remapping
   :open:

   .. list-table::
      :widths: 5 55 40
      :header-rows: 1

      * -
        - Command
        - What to observe
      * - T1
        - ``ros2 launch remapping_demo node_remap.launch.py``
        - Both nodes start with remapped names
      * - T2
        - ``ros2 node list``
        - ``/front_camera`` and ``/rear_camera`` appear (not ``/camera_node``)


Topic Remapping
----------------------------------------------------

Topic remapping redirects a publisher or subscriber to use a different
topic name, allowing nodes with incompatible naming conventions to
communicate without modifying either node.

**CLI: ``-r original:=new``**

.. code-block:: console

   ros2 run remapping_demo camera_demo_exe --ros-args -r image_raw:=/sensors/front/image

**Launch File: ``remappings`` Argument**

.. code-block:: python

   front_camera = Node(
       package='remapping_demo',
       executable='camera_demo_exe',
       name='front_camera',
       remappings=[
           ('image_raw', '/sensors/front/image'),
       ],
       output='screen',
   )

.. tip::

   Use relative names (without a leading ``/``) in the left side of the
   remapping tuple so that namespaces continue to compose correctly.
   Absolute names on the right side are fine when you want a fixed
   destination regardless of namespace.

.. dropdown:: Demonstration: Connecting Two Nodes with Incompatible Names
   :open:

   A ``camera_node`` publishes on ``image_raw``. An ``image_processor``
   subscribes on ``camera/image``. Without remapping, they never connect.

   .. list-table::
      :widths: 5 55 40
      :header-rows: 1

      * -
        - Command
        - What to observe
      * - T1
        - ``ros2 launch remapping_demo topic_remap.launch.py``
        - Both camera and processor nodes start
      * - T2
        - ``ros2 topic list``
        - Remapped topic ``/sensors/front/image`` appears
      * - T2
        - ``ros2 topic echo /sensors/front/image --once``
        - A message is received (publisher and subscriber are connected)
      * - T2
        - ``rqt_graph``
        - Arrow from camera node through remapped topic to processor node


Parameter Remapping
----------------------------------------------------

Parameters can be overridden at launch time using ``-p`` on the CLI or
the ``parameters`` argument in a launch file. This was introduced in
L10.


Namespaces vs. Remapping
----------------------------------------------------

.. list-table::
   :widths: 30 25 45
   :header-rows: 1

   * - Situation
     - Tool
     - Why
   * - Running the same node multiple times
     - **Namespace**
     - All topics, services, and parameters are isolated automatically.
   * - Two nodes use different names for the same data
     - **Topic remapping**
     - Bridges the naming gap without touching either node's code.
   * - Running the same executable twice in the same namespace
     - **Node remapping**
     - Each instance must have a unique node name.
   * - Overriding a parameter value at launch time
     - **Parameter remapping** (``-p``)
     - Faster than editing a YAML file; no source change needed.
   * - Both isolation *and* renaming in one launch
     - **Namespace + remapping**
     - Namespace isolates the group; remapping fine-tunes individual names.

A **namespace** is a bulk operation that moves everything under a new
prefix at once. **Remapping** is a surgical operation that changes one
specific name. Use namespaces first for isolation, then remapping to
fix anything the namespace alone does not handle correctly.


Lifecycle Nodes
====================================================

A **lifecycle node** is a ROS 2 node that follows a standardized state
machine. Rather than starting immediately when launched, it waits for
explicit transition commands, giving the system precise control over
initialization order, resource allocation, and shutdown.

.. admonition:: Resources
   :class: resources

   - `ROS 2 Design: Managed Nodes
     <https://design.ros2.org/articles/node_lifecycle.html>`_
   - `ROS 2: Managing a Robot
     <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Managing-A-Robot-Introduction.html>`_
   - `rclpy source: lifecycle examples
     <https://github.com/ros2/rclpy/tree/jazzy/rclpy>`_


Why Use Lifecycle Nodes?
----------------------------------------------------

- **Controlled initialization order**: a sensor driver stays in
  Inactive until a dependent processing node finishes configuring,
  preventing race conditions at startup.
- **Resource management**: publishers, timers, and connections are
  created in ``on_configure`` and released in ``on_cleanup``, so
  resources are never held when the node is not active.
- **Runtime pause and resume**: deactivate a node during calibration
  or reconfiguration without killing and restarting it.
- **System coordination**: a lifecycle manager issues transitions in
  a defined order and can shut down the entire stack cleanly on error.


State Machine
----------------------------------------------------

A lifecycle node moves through four **primary states**. Each state is
entered via a named **transition command** that invokes a callback your
node overrides.

.. only:: html

   .. figure:: /_static/images/L12/lifecycle_states_light.png
      :alt: The lifecycle node state machine
      :width: 100%
      :align: center
      :class: only-light

      Transitions are issued explicitly; the node never moves between
      states on its own.

   .. figure:: /_static/images/L12/lifecycle_states_dark.png
      :alt: The lifecycle node state machine
      :width: 100%
      :align: center
      :class: only-dark

      Transitions are issued explicitly; the node never moves between
      states on its own.

**Two Design Decisions Worth Understanding**

*What does Error Raised mean?*

- A callback threw an unhandled exception or returned
  ``TransitionCallbackReturn.ERROR``.
- The node is routed to **ErrorProcessing**: SUCCESS recovers to
  Unconfigured, FAILURE goes to Finalized.
- This is different from returning ``FAILURE``, which simply aborts
  the transition and keeps the node in its current state.

*Why is there no FAILURE path for on_deactivate?*

- Deactivation must always succeed. If ``on_deactivate`` could fail,
  the system could get stuck unable to stop a node.
- The same applies to ``on_shutdown``: the state machine only moves
  forward toward Finalized.

**Primary States**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - State
     - Entered via
     - What the node does here
   * - **Unconfigured**
     - startup
     - Exists but holds no resources. Waiting to be configured.
   * - **Inactive**
     - ``configure``
     - Resources allocated (publishers, parameters). Not yet processing.
   * - **Active**
     - ``activate``
     - Fully operational. Publishers enabled, timers running, data flowing.
   * - **Finalized**
     - ``shutdown``
     - Cleaned up and ready to be destroyed. No further transitions.

.. note::

   A node starts in **Unconfigured** the moment it is created. It stays
   there until a ``configure`` command is issued.

**Transition Commands**

.. list-table::
   :widths: 20 20 20 40
   :header-rows: 1

   * - Command
     - From
     - To
     - Callback
   * - ``configure``
     - Unconfigured
     - Inactive
     - ``on_configure``
   * - ``activate``
     - Inactive
     - Active
     - ``on_activate``
   * - ``deactivate``
     - Active
     - Inactive
     - ``on_deactivate``
   * - ``cleanup``
     - Inactive
     - Unconfigured
     - ``on_cleanup``
   * - ``shutdown``
     - Any
     - Finalized
     - ``on_shutdown``

.. important::

   Transitions must follow the state machine strictly. You cannot jump
   from Unconfigured directly to Active: ``configure`` then ``activate``
   must be issued in order.


Implementing a Lifecycle Node
----------------------------------------------------

A lifecycle node in Python extends ``LifecycleNode`` and overrides one
callback per transition. Each callback must return
``TransitionCallbackReturn.SUCCESS`` or
``TransitionCallbackReturn.FAILURE``.

**Class Declaration:**

.. code-block:: python

   import rclpy
   from rclpy_lifecycle import LifecycleNode, TransitionCallbackReturn
   from std_msgs.msg import String

   class SensorPublisher(LifecycleNode):
       def __init__(self):
           super().__init__('sensor_publisher')
           self._publisher = None
           self._timer = None
           self._counter = 0

- ``LifecycleNode`` is imported from ``rclpy_lifecycle``.
- Publishers and timers are declared as ``None``. They are created in
  ``on_configure``, not in ``__init__``.
- ``TransitionCallbackReturn`` carries three values: ``SUCCESS``,
  ``FAILURE``, and ``ERROR``.

**on_configure: Allocate Resources**

.. code-block:: python

   def on_configure(self, state):
       self.get_logger().info(f'Configuring from: {state.label}')
       self._publisher = self.create_lifecycle_publisher(
           String, 'sensor_data', 10
       )
       return TransitionCallbackReturn.SUCCESS

- Use ``create_lifecycle_publisher`` instead of ``create_publisher``.
  A lifecycle publisher remains **inactive** until ``on_activate``.
- Do **not** create timers here.

**on_activate: Start Processing**

.. code-block:: python

   def on_activate(self, state):
       super().on_activate(state)  # enables the lifecycle publisher
       self._timer = self.create_timer(1.0, self._publish_sensor_data)
       return TransitionCallbackReturn.SUCCESS

   def _publish_sensor_data(self):
       msg = String(data=f'Reading {self._counter}')
       self._publisher.publish(msg)
       self._counter += 1

.. important::

   Always call ``super().on_activate(state)`` **before** publishing.
   The base class activates the lifecycle publisher; messages sent
   before this call are silently dropped.

**on_deactivate: Stop Processing**

.. code-block:: python

   def on_deactivate(self, state):
       if self._timer is not None:
           self._timer.cancel()
           self._timer = None
       super().on_deactivate(state)
       return TransitionCallbackReturn.SUCCESS

**on_cleanup: Release Resources**

.. code-block:: python

   def on_cleanup(self, state):
       self._publisher = None
       self._counter = 0
       return TransitionCallbackReturn.SUCCESS


Testing Lifecycle Nodes
----------------------------------------------------

The simplest way to test a lifecycle node is to drive its state
transitions manually from the CLI.

.. dropdown:: Demonstration: Changing States with the CLI
   :open:

   .. list-table::
      :widths: 10 50 40
      :header-rows: 1

      * - Terminal
        - Command
        - What to observe
      * - T1
        - ``ros2 run lifecycle_demo sensor_pub_exe``
        - Node enters **Unconfigured**
      * - T2
        - ``ros2 lifecycle get /sensor_publisher``
        - State confirmed: unconfigured
      * - T2
        - ``ros2 lifecycle set /sensor_publisher configure``
        - Enters **Inactive**; publisher created
      * - T2
        - ``ros2 lifecycle set /sensor_publisher activate``
        - Enters **Active**; data flows
      * - T3
        - ``ros2 topic echo /sensor_data``
        - Messages appear while Active
      * - T2
        - ``ros2 lifecycle set /sensor_publisher deactivate``
        - Enters **Inactive**; timer cancelled
      * - T2
        - ``ros2 lifecycle set /sensor_publisher cleanup``
        - Returns to **Unconfigured**


Programmatic State Changes
----------------------------------------------------

A lifecycle node can trigger its own state transitions by calling the
``change_state`` service on itself. In the ``self_cycling_exe``
example, a timer fires every 5 seconds and advances the node through
the full state cycle automatically.

- A class-level list ``_CYCLE`` defines the sequence:
  ``configure`` -> ``activate`` -> ``deactivate`` -> ``cleanup``, then
  repeats.
- Every lifecycle node automatically advertises
  ``/<node_name>/change_state``. Calling it programmatically is
  equivalent to running ``ros2 lifecycle set`` from the CLI.

.. list-table:: What each callback does inside SelfCyclingNode
   :widths: 25 75
   :header-rows: 1

   * - Callback
     - Action
   * - ``on_configure``
     - Creates a lifecycle publisher on ``sensor_data``. No data sent yet.
   * - ``on_activate``
     - Calls ``super().on_activate``, then starts a 1-second publish timer.
   * - ``on_deactivate``
     - Cancels the publish timer, then calls ``super().on_deactivate``.
   * - ``on_cleanup``
     - Sets the publisher to ``None``. Counter resets to zero.

.. note::

   The 5-second cycle timer created in ``__init__`` keeps running
   throughout all states, including Unconfigured and Inactive. It is the
   only timer that is *not* a lifecycle resource.

.. dropdown:: Demonstration
   :open:

   .. code-block:: console

      # T1:
      ros2 run lifecycle_demo self_cycling_exe
      # T2:
      ros2 lifecycle get /self_cycling_node
      ros2 topic echo /sensor_data

   The full cycle is: Unconfigured -> (5s) -> Inactive -> (5s) ->
   Active -> (5s) -> Inactive -> (5s) -> Unconfigured -> ...


Behavior Trees
====================================================

A **behavior tree** (BT) is a hierarchical structure for organizing
robot behaviors. Unlike a state machine, where transitions are encoded
as edges between states, a BT separates *what* the robot does (leaf
nodes) from *how decisions are made* (composite nodes). This makes
behaviors modular, reusable, and easy to extend.

.. admonition:: Resources
   :class: resources

   - `py_trees documentation <https://py-trees.readthedocs.io/en/devel/>`_
   - `py_trees_ros documentation
     <https://py-trees-ros.readthedocs.io/en/latest/>`_
   - `Colledanchise & Ogren: Behavior Trees in Robotics and AI
     <https://arxiv.org/abs/1709.00084>`_


Core Concepts
----------------------------------------------------

Every node in a behavior tree returns one of three statuses when
ticked: **SUCCESS**, **FAILURE**, or **RUNNING**. The tree is ticked
at a fixed rate; the root node propagates ticks downward and collects
statuses upward.

.. list-table:: Node Types
   :widths: 15 15 70
   :header-rows: 1

   * - Node type
     - Symbol
     - Behavior
   * - **Sequence**
     - ``->`` (arrow)
     - Ticks children left to right. Fails on first FAILURE. Succeeds
       only if all children succeed. Like logical AND.
   * - **Fallback**
     - ``?`` (question)
     - Ticks children left to right. Succeeds on first SUCCESS. Fails
       only if all children fail. Like logical OR.
   * - **Action**
     - Rectangle
     - Leaf node that does real work (e.g., publish ``cmd_vel``).
       Returns RUNNING while working, SUCCESS when done.
   * - **Condition**
     - Diamond
     - Leaf node that checks a condition. Returns SUCCESS or FAILURE
       instantly, never RUNNING.

.. note::

   A condition node never modifies world state. An action node always
   does. This separation is the key design principle of behavior trees.


Drive to Goal with Recovery
----------------------------------------------------

.. only:: html

   .. figure:: /_static/images/L12/behavior_tree_light.png
      :alt: Drive-to-goal BT with Fallback recovery
      :width: 100%
      :align: center
      :class: only-light

      Drive-to-goal BT with Fallback recovery.

   .. figure:: /_static/images/L12/behavior_tree_dark.png
      :alt: Drive-to-goal BT with Fallback recovery
      :width: 100%
      :align: center
      :class: only-dark

      Drive-to-goal BT with Fallback recovery.

- The root Sequence ticks **GoalNotReached?** first.
- If the robot has not reached the goal (SUCCESS), the Sequence ticks
  the **Fallback**.
- The Fallback tries **DriveForward** (wrapped in a Timeout decorator)
  first. While driving, it returns RUNNING and the robot moves.
- If the Timeout expires (e.g., the robot is stuck), the decorator
  forces FAILURE and the Fallback ticks **Spin** as a recovery.
- Once the robot reaches the goal, **GoalNotReached?** returns FAILURE
  and the Sequence stops. No velocity is published and the robot halts.


The Tick
----------------------------------------------------

The **tick** is the fundamental mechanism of a behavior tree. At each
tick:

1. The root node is ticked.
2. The root passes the tick to its children according to its own logic.
3. Each leaf node executes its behavior and returns SUCCESS, FAILURE,
   or RUNNING.
4. Statuses propagate back up to the root.

   - **RUNNING**: the action is still in progress.
   - **SUCCESS**: the action or condition completed successfully.
   - **FAILURE**: the action or condition failed. The parent composite
     decides what to do next.


py_trees and py_trees_ros
----------------------------------------------------

``py_trees`` is a pure Python behavior tree library. ``py_trees_ros``
adds ROS 2 integration: a tick loop driven by a ROS 2 timer, and
pre-built behaviors for subscribing to topics, calling services, and
sending action goals.

**Installation:**

.. code-block:: console

   sudo apt install ros-jazzy-py-trees ros-jazzy-py-trees-ros

.. list-table:: Key Classes
   :widths: 40 60
   :header-rows: 1

   * - Class
     - Purpose
   * - ``py_trees.behaviour.Behaviour``
     - Base class for all custom leaf nodes.
   * - ``py_trees.composites.Sequence``
     - Composite: ticks children in order (AND).
   * - ``py_trees.composites.Selector``
     - Composite: ticks children until one succeeds (OR).
   * - ``py_trees_ros.trees.BehaviourTree``
     - Wraps a ``py_trees`` tree in a ROS 2 node with a timer-driven
       tick loop.
   * - ``py_trees.common.Status``
     - Enum: ``SUCCESS``, ``FAILURE``, ``RUNNING``.

.. note::

   ``py_trees.composites.Selector`` is the ``py_trees`` name for a
   Fallback node. The terms are interchangeable.


Writing a Custom Leaf Node
----------------------------------------------------

Every custom behavior inherits from ``py_trees.behaviour.Behaviour``
and overrides four methods:

.. code-block:: python

   import py_trees

   class MyBehaviour(py_trees.behaviour.Behaviour):
       def __init__(self, name: str):
           super().__init__(name=name)

       def setup(self, **kwargs):
           # Called once before the first tick.
           # Acquire ROS 2 resources here (node, publishers, etc.)
           pass

       def initialise(self):
           # Called each time the node transitions from idle to running.
           # Reset internal state here.
           pass

       def update(self) -> py_trees.common.Status:
           # Called every tick while this node is active.
           # Return SUCCESS, FAILURE, or RUNNING.
           return py_trees.common.Status.SUCCESS

       def terminate(self, new_status: py_trees.common.Status):
           # Called when the node exits (succeeds, fails, or is preempted).
           pass


Scenario
----------------------------------------------------

We build a behavior tree that drives a ROSbot toward a goal position
using a proportional controller, monitors the robot's odometry, and
stops when the goal is reached. If ``DriveForward`` times out, a
``SpinInPlace`` recovery rotates the robot toward a fixed target
heading (``goal_yaw``, default 0.0 rad) before retrying.

.. only:: html

   .. figure:: /_static/images/L12/behavior_tree_light.png
      :alt: Drive-to-goal BT with Fallback recovery
      :width: 100%
      :align: center
      :class: only-light

      Drive-to-goal BT with Fallback recovery.

   .. figure:: /_static/images/L12/behavior_tree_dark.png
      :alt: Drive-to-goal BT with Fallback recovery
      :width: 100%
      :align: center
      :class: only-dark

      Drive-to-goal BT with Fallback recovery.

.. list-table:: bt_demo Package Files
   :widths: 30 70
   :header-rows: 1

   * - File
     - Description
   * - ``drive_forward.py``
     - Action node: steers the robot toward a goal using a P-controller
       (``k_rho``, ``k_alpha``). Always returns RUNNING.
   * - ``spin_in_place.py``
     - Action node: rotates toward a target heading using a P-controller
       (``k_yaw``). Returns SUCCESS when within tolerance.
   * - ``goal_not_reached.py``
     - Condition node: subscribes to odometry and returns SUCCESS while
       far from the goal, FAILURE when within tolerance.
   * - ``main_drive_to_goal.py``
     - Entry point: assembles the tree, reads ROS 2 parameters, runs it.
   * - ``drive_to_goal.py``
     - Launch file: exposes all tuneable values as launch arguments.


Decorators
----------------------------------------------------

A **decorator** wraps a single child node and modifies how its return
status is interpreted or how long it is allowed to run.

.. list-table:: Common Decorators
   :widths: 25 75
   :header-rows: 1

   * - Decorator
     - Effect
   * - ``Inverter``
     - Flips SUCCESS to FAILURE and vice versa. Leaves RUNNING unchanged.
   * - ``Timeout``
     - Returns FAILURE if the child is still RUNNING after a set duration.
   * - ``Retry``
     - Re-ticks the child up to *N* times on FAILURE before propagating.
   * - ``SuccessIsRunning``
     - Converts SUCCESS to RUNNING, useful for continuous monitoring.

**Example: Timeout**

.. code-block:: python

   drive = DriveForward(name='DriveForward', goal_x=goal_x, goal_y=goal_y,
                        k_rho=k_rho, k_alpha=k_alpha)

   drive_with_timeout = py_trees.decorators.Timeout(
       child=drive,
       name=f'DriveForward ({timeout_duration} s)',
       duration=timeout_duration,
   )

Decorators in ``py_trees`` are found in ``py_trees.decorators``. They
wrap any single node; they cannot have more than one child.


Reading the Terminal Output
----------------------------------------------------

When ``unicode_tree_debug=True``, ``py_trees_ros`` prints the tree on
every tick. Here is an example:

.. code-block:: text

   [-] DriveToGoal [*]
       --> GoalNotReached? [✓]
       {o} DriveOrRecover [*]
           -^- DriveForward (10.0 s) [*] -- remaining: 6.8s
               --> DriveForward [*]
           --> Spin

.. list-table:: Terminal Symbols
   :widths: 15 20 65
   :header-rows: 1

   * - Symbol
     - Node type
     - Meaning
   * - ``[-]``
     - Sequence
     - Ticks children left-to-right (AND).
   * - ``{o}``
     - Selector
     - Tries children until one succeeds (OR / Fallback).
   * - ``-^-``
     - Decorator
     - Wraps a single child and modifies its result.
   * - ``-->``
     - Leaf
     - A behaviour node (action or condition) with no children.
   * - ``[*]``
     - RUNNING
     - The node is currently active.
   * - ``[✓]``
     - SUCCESS
     - The node completed successfully.
   * - ``[✗]``
     - FAILURE
     - The node failed.
   * - (blank)
     - INVALID
     - The node has not been ticked yet.


Demonstration
----------------------------------------------------

.. dropdown:: bt_demo Demonstration
   :open:

   .. list-table::
      :widths: 5 95
      :header-rows: 1

      * -
        - Command
      * - T1
        - ``ros2 launch rosbot_gazebo empty_world.launch.py rviz:=False``
      * - T2
        - ``ros2 launch bt_demo drive_to_goal.py``
      * - T2
        - ``ros2 launch bt_demo drive_to_goal.py goal_x:=5.0 goal_y:=3.0 k_rho:=0.6``
      * - T2
        - ``ros2 launch bt_demo drive_to_goal.py goal_x:=10.0 timeout_duration:=3.0 goal_yaw:=1.57``
      * - T3
        - ``ros2 topic echo /odometry/filtered --field pose.pose.position``
      * - T3
        - ``ros2 topic echo /cmd_vel``
