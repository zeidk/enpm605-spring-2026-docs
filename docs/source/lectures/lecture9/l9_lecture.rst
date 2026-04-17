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


.. dropdown:: Build the Demo Packages

   Build both demo packages used in this lecture before proceeding.

   .. code-block:: console

      colcon build --symlink-install --packages-select launch_demo executor_demo

   Source the workspace after each build:

   .. code-block:: console

      source install/setup.bash


Launch Files
====================================================

A mechanism for starting multiple ROS 2 nodes simultaneously while
enabling dynamic configuration.


.. dropdown:: Why Use Launch Files?

   Managing each node manually with ``ros2 run`` becomes impractical in
   real robotic systems. Launch files address this by combining node
   startup, configuration, and coordination into a single, reproducible
   command.

   1. **Node Management**: Launch, configure, and control individual
      ROS 2 nodes, including lifecycle and composable nodes, to define
      system behavior.
   2. **Modularity and Reuse**: Structure complex systems by reusing
      launch files, grouping nodes, and managing namespace scopes for
      better organization and scalability.
   3. **Configuration and Customization**: Allow users to tailor launch
      behavior using arguments, environment variables, and substitutions
      that adapt to various runtime contexts.
   4. **Execution Control**: Control the timing and conditions under
      which nodes and actions are launched, including timers,
      conditionals, and event-driven execution.
   5. **Custom Launch Logic**: Use Python-based logic and functions to
      perform dynamic setup, computations, or system introspection
      before launching actions.
   6. **Logging and Diagnostics**: Monitor system behavior and assist
      debugging by printing messages, adjusting log levels, and tracking
      node status during launch.

   .. admonition:: Resources
      :class: resources

      - `ROS 2 Documentation: Launch Files Tutorials
        <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html>`_
      - `ROS 2 Documentation: Creating Launch Files
        <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html>`_
      - `ROS 2 Documentation: Launch File Formats
        <https://docs.ros.org/en/jazzy/How-To-Guides/Launch-file-different-formats.html>`_
      - `ROS 2 Documentation: Using Substitutions in Launch Files
        <https://docs.ros.org/en/jazzy/How-To-Guides/Using-Substitutions-In-Launch-Files.html>`_

   .. note::

      Launch files support XML, YAML, and Python formats. This course
      uses Python exclusively.


.. dropdown:: Anatomy of a Launch File

   A typical Python launch file contains three main parts.

   - **Import statements**: Required launch and ROS dependencies.
   - **Launch description**: A function named ``generate_launch_description``
     that returns the ``LaunchDescription`` containing all node
     configurations. This function **must** be defined for ROS 2 to
     recognize the file as a valid launch file.
   - **Node configuration**: Information about nodes, parameters,
     remappings, and more.

   .. note::

      Launch files are typically placed in the ``launch/`` directory
      within your package. Edit ``setup.py`` to install them with::

         (os.path.join('share', package_name, 'launch'), glob('launch/*'))

      Launch files end with the ``.launch.py`` extension by convention.

   **Two equivalent patterns**

   .. code-block:: python

      # demo1.launch.py -- explicit LaunchDescription object
      from launch import LaunchDescription
      from launch_ros.actions import Node

      def generate_launch_description():
          ld = LaunchDescription()
          talker = Node(package="demo_nodes_py", executable="talker")
          listener = Node(package="demo_nodes_py", executable="listener")
          ld.add_action(talker)
          ld.add_action(listener)
          return ld

   .. code-block:: python

      # demo2.launch.py -- inline list pattern
      from launch import LaunchDescription
      from launch_ros.actions import Node

      def generate_launch_description():
          return LaunchDescription([
              Node(package="demo_nodes_py", executable="talker"),
              Node(package="demo_nodes_py", executable="listener"),
          ])

   Both patterns are equivalent. Choose whichever improves readability
   for your use case.

   .. admonition:: Demonstration
      :class: demonstration

      .. code-block:: console

         ros2 launch launch_files_demo demo1.launch.py
         ros2 launch launch_files_demo demo2.launch.py


Advanced Features
====================================================

Launch files support several advanced features for building complex,
configurable robot systems.


.. dropdown:: Include Other Launch Files

   One launch file can include another from a different package using
   ``IncludeLaunchDescription``. This promotes modularity and allows
   large systems to be composed from smaller, reusable launch files.

   .. code-block:: python

      from launch.actions import IncludeLaunchDescription
      from launch.launch_description_sources import PythonLaunchDescriptionSource
      from launch.substitutions import PathJoinSubstitution
      from launch_ros.substitutions import FindPackageShare

      included_launch = IncludeLaunchDescription(
          PythonLaunchDescriptionSource(
              PathJoinSubstitution([
                  FindPackageShare("other_package"), "launch", "other.launch.py"
              ])
          )
      )

   - ``FindPackageShare`` resolves the installed share directory of a
     package at runtime without hardcoding paths.
   - ``PathJoinSubstitution`` constructs a file path from components in
     a platform-independent way.

   .. admonition:: Demonstration
      :class: demonstration

      .. code-block:: console

         ros2 launch launch_files_demo demo3.launch.py


.. dropdown:: Conditional Launching

   Nodes can be started conditionally based on launch arguments. The
   ``IfCondition`` class evaluates the argument at launch time and
   starts the node only when the value is ``"true"``.

   .. code-block:: python

      from launch.actions import DeclareLaunchArgument
      from launch.conditions import IfCondition
      from launch.substitutions import LaunchConfiguration

      talker_arg = DeclareLaunchArgument("start_talker", default_value="true")

      talker = Node(
          package="demo_nodes_py",
          executable="talker",
          condition=IfCondition(LaunchConfiguration("start_talker")),
      )

   To inspect all available launch arguments for a file:

   .. code-block:: console

      ros2 launch <package> <launch_file> --show-args

   .. admonition:: Demonstration
      :class: demonstration

      .. code-block:: console

         ros2 launch launch_files_demo demo4.launch.py start_talker:=true
         ros2 launch launch_files_demo demo4.launch.py start_talker:=false


.. dropdown:: Node Grouping

   Related nodes can be grouped together using ``GroupAction``. Groups
   make the launch description more readable and allow a condition to
   be applied to an entire set of nodes at once.

   .. code-block:: python

      from launch.actions import GroupAction
      from launch_ros.actions import Node

      chatter_group = GroupAction([
          Node(package="demo_nodes_py", executable="talker"),
          Node(package="demo_nodes_py", executable="listener"),
      ])

   **Conditional group** -- start the whole group based on an argument:

   .. code-block:: python

      from launch.actions import GroupAction, DeclareLaunchArgument
      from launch.conditions import IfCondition
      from launch.substitutions import LaunchConfiguration

      enable_arg = DeclareLaunchArgument("enable_chatter", default_value="false")

      chatter_group = GroupAction(
          condition=IfCondition(LaunchConfiguration("enable_chatter")),
          actions=[
              Node(package="demo_nodes_py", executable="talker"),
              Node(package="demo_nodes_py", executable="listener"),
          ],
      )

   .. admonition:: Demonstration
      :class: demonstration

      .. code-block:: console

         ros2 launch launch_files_demo demo5.launch.py
         ros2 launch launch_files_demo demo6.launch.py enable_chatter:=true


Executors
====================================================

Executors manage how and when callbacks run, enabling complex
multi-task robotic systems.


.. dropdown:: Overview

   So far our nodes have been **single-purpose**: one callback managing
   one task. Real robotic systems require multiple concurrent tasks
   (processing sensor data, updating control commands, monitoring system
   health, handling user input, logging) and must handle coordination
   challenges such as blocking callbacks, concurrent vs. parallel
   execution, and task prioritization.

   - Executors simplify thread management by providing an abstraction
     layer, allowing operation with either a single thread or multiple
     threads.
   - Executors can manage the callbacks of one or more nodes at the
     same time.

   .. note::

      **Concurrent** means tasks are in progress at the same time but
      may take turns on one thread. **Parallel** means tasks run
      simultaneously on separate cores. The executor and callback group
      together determine which one you get.

   .. admonition:: Resources
      :class: resources

      - `About Executors
        <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html>`_
      - `Using Callback Groups
        <https://docs.ros.org/en/jazzy/How-To-Guides/Using-callback-groups.html>`_


Single-Threaded Executor
----------------------------------------------------

Processes all callbacks sequentially in a single OS thread.


.. dropdown:: Key Concepts

   A **single-threaded executor** processes all callbacks one at a time
   in the order they are scheduled, without concurrency.

   - All callbacks (timers, subscriptions, services, actions) share one
     thread and are queued and executed sequentially.
   - Execution order follows the scheduler queue -- no two callbacks
     ever overlap.
   - No synchronization primitives (locks, mutexes) are needed because
     concurrent access to shared state is impossible by construction.
   - ``rclpy.spin(node)`` is a convenience wrapper that internally
     creates a ``SingleThreadedExecutor``, adds the node, and calls
     ``executor.spin()``.
   - Suitable for nodes with low computational demands or where
     deterministic, predictable execution order is required.
   - A long-running or blocking callback will delay every other callback
     for the duration of the block.


.. dropdown:: Execution Timeline

   Three timer callbacks registered to the same single-threaded
   executor:

   - ``cb1`` at 2 Hz, 30 ms execution time
   - ``cb2`` at 2 Hz, 20 ms execution time
   - ``cb3`` at 4 Hz, 10 ms execution time

   .. only:: html

      .. figure:: /_static/images/L9/single_threaded_timeline_light.png
         :alt: Single-threaded executor timeline
         :width: 100%
         :align: center
         :class: only-light

         Single-threaded executor timeline over 1 s. All callbacks share
         one thread and execute sequentially. cb2 incurs a fixed +30 ms
         phase offset and cb3 a fixed +50 ms offset whenever co-scheduled
         with cb1.

      .. figure:: /_static/images/L9/single_threaded_timeline_dark.png
         :alt: Single-threaded executor timeline
         :width: 100%
         :align: center
         :class: only-dark

         Single-threaded executor timeline over 1 s. All callbacks share
         one thread and execute sequentially. cb2 incurs a fixed +30 ms
         phase offset and cb3 a fixed +50 ms offset whenever co-scheduled
         with cb1.

   .. only:: latex

      .. figure:: /_static/images/L9/single_threaded_timeline_light.png
         :alt: Single-threaded executor timeline
         :width: 100%
         :align: center

         Single-threaded executor timeline over 1 s. All callbacks share
         one thread and execute sequentially.

   .. list-table:: Phase offsets for the single-threaded executor
      :widths: 20 15 15 20 20 10
      :header-rows: 1
      :class: compact-table

      * - Callback
        - Frequency
        - Duration
        - Scheduled at
        - Actually fires at
        - Delay
      * - cb1 cycle 1
        - 2 Hz
        - 30 ms
        - 0 ms
        - 0 ms
        - none
      * - cb2 cycle 1
        - 2 Hz
        - 20 ms
        - 0 ms
        - 30 ms
        - +30 ms
      * - cb3 cycle 1
        - 4 Hz
        - 10 ms
        - 0 ms
        - 50 ms
        - +50 ms
      * - cb3 cycle 2
        - 4 Hz
        - 10 ms
        - 250 ms
        - 250 ms
        - none
      * - cb1 cycle 2
        - 2 Hz
        - 30 ms
        - 500 ms
        - 500 ms
        - none
      * - cb2 cycle 2
        - 2 Hz
        - 20 ms
        - 500 ms
        - 530 ms
        - +30 ms
      * - cb3 cycle 3
        - 4 Hz
        - 10 ms
        - 500 ms
        - 550 ms
        - +50 ms
      * - cb3 cycle 4
        - 4 Hz
        - 10 ms
        - 750 ms
        - 750 ms
        - none


.. dropdown:: ``rclpy.spin()`` vs ``SingleThreadedExecutor``

   They are essentially the same. ``rclpy.spin(node)`` is a convenience
   wrapper that creates a ``SingleThreadedExecutor``, adds the node to
   it, and calls ``executor.spin()``.

   .. code-block:: python

      # Simple spinning
      def main(args=None):
          rclpy.init(args=args)
          node = MyNode()
          rclpy.spin(node)
          rclpy.shutdown()

   .. code-block:: python

      # Explicit executor -- preferred when managing multiple nodes
      from rclpy.executors import SingleThreadedExecutor

      def main(args=None):
          rclpy.init(args=args)
          node1 = MyFirstNode()
          node2 = MySecondNode()
          executor = SingleThreadedExecutor()
          executor.add_node(node1)
          executor.add_node(node2)
          executor.spin()
          rclpy.shutdown()

   Use the explicit executor when you need to add multiple nodes to one
   executor, switch executor types easily, or implement custom spin
   behaviors.


Multi-Threaded Executor
----------------------------------------------------

Manages and executes callbacks across multiple threads, allowing for
concurrent processing of tasks.


.. dropdown:: Overview and Benefits

   A **multi-threaded executor** creates a pool of OS threads. Each
   thread can independently process callbacks from nodes added to the
   executor.

   - **Thread pool**: The executor creates a configurable number of
     threads via ``num_threads``. Each thread can handle a pending
     callback independently.
   - **Callback scheduling**: When events occur (a timer fires, a
     message arrives, a service request comes in), the executor assigns
     pending callbacks to available threads. Multiple callbacks can run
     concurrently.
   - **Spinning**: ``executor.spin()`` starts an event loop that
     continuously checks for and dispatches work to the thread pool.

   **Benefits**

   - **Performance**: Ideal for applications with many independent
     tasks such as processing data from multiple sensors. Concurrent
     execution can reduce latency and improve throughput.
   - **Scalability**: Handles multiple nodes or high-frequency callbacks
     better than a single-threaded executor under heavy load.
   - **Responsiveness**: Critical tasks (such as responding to an
     emergency stop signal) will not be blocked by slower, less urgent
     ones.

   **Challenges**

   - **Race conditions**: If callbacks access shared resources (a class
     attribute, a buffer), synchronization mechanisms like
     ``threading.Lock`` are needed to prevent data corruption.
   - **Overhead**: Managing multiple threads introduces complexity and
     CPU overhead. If your application is lightweight, the extra threads
     may not be worth it.


.. dropdown:: Concurrency vs. Parallelism

   **Concurrency** means multiple tasks are in progress at the same
   time. Multiple software threads exist, but they share a single core.
   The OS task switcher rapidly alternates which thread gets the core,
   creating the illusion of simultaneity. This is about *structure*.

   **Parallelism** means multiple tasks execute simultaneously on
   separate CPU cores. No task switching is needed -- each core runs
   its thread uninterrupted. This is about *execution*.

   .. only:: html

      .. figure:: /_static/images/L9/concurrency_light.png
         :alt: Concurrency illustration
         :width: 60%
         :align: center
         :class: only-light

         Concurrency: two queues, one hot dog stand. Both groups are in
         progress, but only one customer is served at a time.

      .. figure:: /_static/images/L9/concurrency_dark.png
         :alt: Concurrency illustration
         :width: 60%
         :align: center
         :class: only-dark

         Concurrency: two queues, one hot dog stand. Both groups are in
         progress, but only one customer is served at a time.

      .. figure:: /_static/images/L9/parallelism_light.png
         :alt: Parallelism illustration
         :width: 60%
         :align: center
         :class: only-light

         Parallelism: two queues, two hot dog stands. Both groups are
         served simultaneously with no waiting on each other.

      .. figure:: /_static/images/L9/parallelism_dark.png
         :alt: Parallelism illustration
         :width: 60%
         :align: center
         :class: only-dark

         Parallelism: two queues, two hot dog stands. Both groups are
         served simultaneously with no waiting on each other.

   .. only:: latex

      .. figure:: /_static/images/L9/concurrency_light.png
         :alt: Concurrency illustration
         :width: 80%
         :align: center

         Concurrency: two queues, one hot dog stand.

      .. figure:: /_static/images/L9/parallelism_light.png
         :alt: Parallelism illustration
         :width: 80%
         :align: center

         Parallelism: two queues, two hot dog stands.


.. dropdown:: The Python GIL and Its Impact on ROS 2

   CPython (the standard Python interpreter) has a **Global Interpreter
   Lock (GIL)**: a mutex that allows only one thread to execute Python
   bytecode at a time, regardless of how many CPU cores are available.

   Even if you create 32 threads on a 32-core machine, only one thread
   holds the GIL and runs at any instant. The others wait. The GIL
   exists to protect CPython's internal memory management from
   concurrent access.

   **Impact on ROS 2 Python nodes:**

   - A ``MultiThreadedExecutor`` creates a pool of OS threads, but the
     GIL serializes them back onto one core for any pure Python code.
   - Adding more threads via ``num_threads`` does **not** add
     parallelism; it adds idle threads.
   - A ``ReentrantCallbackGroup`` allows multiple callback *instances*
     to be in progress simultaneously, but they still take turns on one
     core.

   **When true parallelism IS achieved:**

   The GIL is released during I/O, ``time.sleep()``, and calls into
   native libraries (NumPy, OpenCV, sensor drivers). Only then can two
   threads run simultaneously on separate cores. This is why AV
   callbacks processing LiDAR (NumPy) or images (OpenCV) can achieve
   true parallelism in practice.


Callback Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **callback group** is a container within a node that holds callbacks
for subscriptions, timers, or services. Each group defines how its
callbacks are handled in terms of execution and threading.


.. dropdown:: Overview

   - By default, all callbacks belong to the node's implicit callback
     group (``MutuallyExclusiveCallbackGroup``). You can create explicit
     groups to customize execution behavior.
   - **Two types exist**: ``MutuallyExclusive`` (only one callback
     executes at a time) and ``Reentrant`` (multiple callbacks can
     execute in parallel on separate threads).
   - Useful for managing concurrency, preventing race conditions,
     prioritizing callbacks, and isolating time-critical operations from
     blocking ones.
   - The executor type (single-threaded vs. multi-threaded) determines
     whether callback groups can actually leverage concurrency.

   .. only:: html

      .. figure:: /_static/images/L9/callback_group_summary_light.png
         :alt: Callback group overview diagram
         :width: 100%
         :align: center
         :class: only-light

         Overview of executor and callback group options in ROS 2.

      .. figure:: /_static/images/L9/callback_group_summary_dark.png
         :alt: Callback group overview diagram
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/L9/callback_group_summary_light.png
         :alt: Callback group overview diagram
         :width: 100%
         :align: center

         Overview of executor and callback group options in ROS 2.


.. dropdown:: Mutually Exclusive Callback Group

   Callbacks within a **mutually exclusive callback group** cannot run
   concurrently, even in a multi-threaded executor. The executor
   withholds any queued callback from the group until the currently
   running one returns.

   **Use case:** Callbacks share a resource (a class attribute, a
   buffer, a hardware interface) and you want to avoid race conditions
   without writing explicit locks. Also useful when you need
   deterministic, sequential execution within a group while other
   groups or nodes run in parallel.

   **Limitation:** A long-running callback in the group delays every
   other callback in the same group for its entire duration, regardless
   of how many threads the executor has.

   **Declaration:**

   .. code-block:: python

      from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

      class MutexDemoNode(Node):
          def __init__(self):
              super().__init__("mutex_demo")
              self._group = MutuallyExclusiveCallbackGroup()

              # All three timers share the same group
              self.create_timer(1.0,  self._cb1, callback_group=self._group)
              self.create_timer(0.5,  self._cb2, callback_group=self._group)
              self.create_timer(0.25, self._cb3, callback_group=self._group)

   **Effect of ``num_threads`` on a single mutex group:**

   .. code-block:: python

      # Default: os.cpu_count() threads -- behavior identical to any explicit value
      executor = MultiThreadedExecutor()

      # Explicit: 4 threads -- preferred for portability and clarity
      executor = MultiThreadedExecutor(num_threads=4)

   For a single ``MutuallyExclusiveCallbackGroup``, ``num_threads`` has
   no effect on callback ordering or timing. The mutex gate serializes
   all callbacks regardless of pool size. Prefer explicit values in
   production code.

   **Execution timeline (1 Hz cb1 at 200 ms, 2 Hz cb2 at 80 ms, 4 Hz cb3 at 40 ms):**

   .. only:: html

      .. figure:: /_static/images/L9/mutex2_timeline_light.png
         :alt: Mutually exclusive callback group timeline
         :width: 100%
         :align: center
         :class: only-light

         ``MultiThreadedExecutor(num_threads=4)`` with one
         ``MutuallyExclusiveCallbackGroup``. Despite 4 threads, the
         mutex gate serializes all callbacks.

      .. figure:: /_static/images/L9/mutex2_timeline_dark.png
         :alt: Mutually exclusive callback group timeline
         :width: 100%
         :align: center
         :class: only-dark

         ``MultiThreadedExecutor(num_threads=4)`` with one
         ``MutuallyExclusiveCallbackGroup``. Despite 4 threads, the
         mutex gate serializes all callbacks.

   .. only:: latex

      .. figure:: /_static/images/L9/mutex2_timeline_light.png
         :alt: Mutually exclusive callback group timeline
         :width: 100%
         :align: center

         ``MultiThreadedExecutor(num_threads=4)`` with one
         ``MutuallyExclusiveCallbackGroup``.

   .. list-table:: Timestamp summary -- delays depend on what was
      running at scheduled time, not on thread count
      :widths: 20 15 20 20 15
      :header-rows: 1
      :class: compact-table

      * - Callback
        - Frequency
        - Scheduled at
        - Actually fires at
        - Delay
      * - cb1 cycle 1
        - 1 Hz
        - 0 ms
        - 0 ms
        - none
      * - cb2 cycle 1
        - 2 Hz
        - 0 ms
        - 200 ms
        - +200 ms
      * - cb3 cycle 1
        - 4 Hz
        - 0 ms
        - 280 ms
        - +280 ms
      * - cb2 cycle 2
        - 2 Hz
        - 500 ms
        - 500 ms
        - none
      * - cb3 cycle 3
        - 4 Hz
        - 500 ms
        - 580 ms
        - +80 ms
      * - cb3 cycle 4
        - 4 Hz
        - 750 ms
        - 750 ms
        - none
      * - cb1 cycle 2
        - 1 Hz
        - 1000 ms
        - 1000 ms
        - none

   .. note::

      ``num_threads`` controls how many threads exist in the pool. It
      does **not** control how many callbacks can run simultaneously
      within a ``MutuallyExclusiveCallbackGroup`` -- that is always
      exactly one.


.. dropdown:: Reentrant Callback Group

   Callbacks within a **reentrant callback group** can run concurrently
   with each other on different threads. The executor places no
   serialization constraint. If a thread is free and a callback is
   ready, it fires immediately regardless of whether another instance
   of the same callback is already running.

   **Use case:** Independent tasks that do not share state and can
   safely overlap. Sensor pipelines, logging, and data publishing where
   each invocation is self-contained. Any callback whose execution time
   may occasionally exceed its period without blocking others.

   **Risk:** If two concurrent instances of the same callback read and
   write shared state (a class attribute), a race condition occurs.
   Use a ``threading.Lock`` or switch to
   ``MutuallyExclusiveCallbackGroup`` if shared state is involved.

   **Declaration:**

   .. code-block:: python

      from rclpy.callback_groups import ReentrantCallbackGroup

      class ReentrantDemoNode(Node):
          def __init__(self):
              super().__init__("reentrant_demo")
              self._group = ReentrantCallbackGroup()
              self.create_timer(1.0,  self._cb1, callback_group=self._group)
              self.create_timer(0.5,  self._cb2, callback_group=self._group)
              self.create_timer(0.25, self._cb3, callback_group=self._group)

      def main(args=None):
          rclpy.init(args=args)
          node = ReentrantDemoNode()
          executor = MultiThreadedExecutor(num_threads=4)
          executor.add_node(node)
          executor.spin()
          rclpy.shutdown()

   **Fast callbacks (all complete within their period):**

   .. only:: html

      .. figure:: /_static/images/L9/reentrant1_timeline_light.png
         :alt: Reentrant callback group timeline -- fast callbacks
         :width: 100%
         :align: center
         :class: only-light

         All callbacks complete within their periods -- each fires
         exactly on schedule with no overlap.

      .. figure:: /_static/images/L9/reentrant1_timeline_dark.png
         :alt: Reentrant callback group timeline -- fast callbacks
         :width: 100%
         :align: center
         :class: only-dark

         All callbacks complete within their periods -- each fires
         exactly on schedule with no overlap.

   .. only:: latex

      .. figure:: /_static/images/L9/reentrant1_timeline_light.png
         :alt: Reentrant callback group timeline -- fast callbacks
         :width: 100%
         :align: center

         Reentrant group -- all fast callbacks fire on schedule.

   **Blocked callback (600 ms execution, 500 ms period):**

   With a ``ReentrantCallbackGroup``, a new callback instance fires at
   its scheduled time even if a previous instance is still executing
   on another thread. By t=1000 ms, three instances can be active
   concurrently. With a ``MutuallyExclusiveCallbackGroup``, each new
   instance would be withheld until the previous one completes --
   preventing overlap at the cost of increasing delay.

   .. only:: html

      .. figure:: /_static/images/L9/reentrant2_timeline_light.png
         :alt: Reentrant callback group timeline -- slow callback
         :width: 100%
         :align: center
         :class: only-light

         Reentrant group with a callback whose execution (600 ms)
         exceeds its period (500 ms). New instances fire on schedule
         regardless of prior instances still running.

      .. figure:: /_static/images/L9/reentrant2_timeline_dark.png
         :alt: Reentrant callback group timeline -- slow callback
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/L9/reentrant2_timeline_light.png
         :alt: Reentrant callback group timeline -- slow callback
         :width: 100%
         :align: center

         Reentrant group with a slow callback (600 ms, 500 ms period).


.. dropdown:: Choosing Between Mutex and Reentrant

   .. list-table::
      :widths: 25 37 38
      :header-rows: 1
      :class: compact-table

      * -
        - MutuallyExclusive
        - Reentrant
      * - Concurrent instances
        - Never
        - Allowed -- multiple on separate threads
      * - Slow callback blocks group?
        - Yes -- others wait
        - No -- others fire on schedule
      * - Shared state safe?
        - Yes -- serialized
        - No -- needs explicit lock
      * - Missed period?
        - Instance delayed, not duplicated
        - New instance starts regardless
      * - Typical use
        - Shared resources, hardware
        - Independent pipelines, logging

   If in doubt, start with ``MutuallyExclusiveCallbackGroup``. Switch
   to ``ReentrantCallbackGroup`` only when you have confirmed the
   callbacks are stateless or properly protected with a
   ``threading.Lock``.
