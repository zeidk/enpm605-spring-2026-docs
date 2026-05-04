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

   - Remove the ``log/``, ``build/``, and ``install/`` folders.
   - Do a ``git pull``.
   - Install dependencies:

   .. code-block:: console

      rosdep install -i --from-path src \
          --rosdistro $ROS_DISTRO --ignore-src -y \
          --skip-keys "micro_ros_agent python3-ftdi"

   - Compile lecture 14 packages only:

   .. code-block:: console

      colcon build --symlink-install \
          --cmake-args -DCMAKE_BUILD_TYPE=Release \
          --packages-up-to lecture14_meta

   - Source your workspace.
   - Verify Gazebo launches cleanly:

   .. code-block:: console

      ros2 launch rosbot_gazebo husarion_world.launch.py


Lifecycle Nodes
====================================================

A **lifecycle node** is a ROS 2 node that follows a standardized
state machine. Rather than starting immediately when launched, it
waits for explicit transition commands, giving the system precise
control over initialization order, resource allocation, and
shutdown.

.. admonition:: Resources
   :class: resources

   - `ROS 2 Design: Managed Nodes
     <https://design.ros2.org/articles/node_lifecycle.html>`_
   - `rclpy source: lifecycle examples
     <https://github.com/ros2/rclpy/tree/jazzy/rclpy>`_



.. only:: html

   .. figure:: /_static/images/L14/lifecycle_states_light.png
      :alt: The lifecycle node state machine.
      :width: 100%
      :align: center
      :class: only-light

      Transitions are issued explicitly; the node never moves between states on its own.

   .. figure:: /_static/images/L14/lifecycle_states_dark.png
      :alt: The lifecycle node state machine.
      :width: 100%
      :align: center
      :class: only-dark

      Transitions are issued explicitly; the node never moves between states on its own.


State Machine
----------------------------------------------------

A lifecycle node moves through four **primary states**. Each state
is entered via a named **transition command** that invokes a
callback your node overrides.


**Primary States**

A lifecycle node is always in exactly one primary state. The state
determines what the node is allowed to do and what resources it
holds.

.. list-table:: The four primary states and what the node does in each
   :widths: 25 75
   :header-rows: 1

   * - State
     - What the node does here
   * - **Unconfigured**
     - Exists but holds no resources. Waiting to be configured.
   * - **Inactive**
     - Resources allocated (publishers, parameters). Not yet
       processing data.
   * - **Active**
     - Fully operational. Publishers enabled, timers running, data
       flowing.
   * - **Finalized**
     - Cleaned up and ready to be destroyed. No further transitions
       possible.

.. note::

   A node starts in **Unconfigured** the moment it is created. It
   stays there indefinitely until a ``configure`` command is issued.
   No publishers, timers, or subscriptions exist at this point.


**Transition Commands**

Each transition command moves the node from one primary state to
another and invokes a specific Python callback that your node
overrides.

.. list-table:: Available transition commands, the states they
   connect, and the callback each invokes
   :widths: 20 25 25 30
   :header-rows: 1

   * - Command
     - From
     - To
     - Callback
   * - ``configure``
     - **Unconfigured**
     - Inactive
     - ``on_configure``
   * - ``activate``
     - **Inactive**
     - Active
     - ``on_activate``
   * - ``deactivate``
     - **Active**
     - Inactive
     - ``on_deactivate``
   * - ``cleanup``
     - **Inactive**
     - Unconfigured
     - ``on_cleanup``
   * - ``shutdown``
     - Any
     - Finalized
     - ``on_shutdown``

.. note::

   Transitions must follow the state machine strictly. You cannot
   jump from **Unconfigured** directly to **Active**: ``configure``
   then ``activate`` must be issued in order. Skipping ``configure``
   is why ``ros2 lifecycle set`` returns **Transition failed**.


**Why Use Lifecycle Nodes?**

- **Controlled initialization order**: a sensor driver stays in
  Inactive until a dependent processing node finishes configuring,
  preventing race conditions at startup.
- **Resource management**: publishers, timers, and connections are
  created in ``on_configure`` and released in ``on_cleanup``, so
  resources are never held when the node is not active.
- **Runtime pause and resume**: deactivate a node during calibration
  or reconfiguration without killing and restarting it.
- **System coordination**: a lifecycle manager issues transitions in
  a defined order and can shut down the entire stack cleanly on
  error.

.. note::

   Nav2 runs ``map_server``, ``amcl``, ``planner_server``,
   ``controller_server``, and ``bt_navigator`` as lifecycle nodes,
   all managed by ``lifecycle_manager``.


Implementing a Lifecycle Node
----------------------------------------------------

A lifecycle node in Python extends ``LifecycleNode`` and overrides
one callback per transition. Each callback must return
``TransitionCallbackReturn.SUCCESS`` or
``TransitionCallbackReturn.FAILURE``.


**Scenario**

A lifecycle node, ``sensor_publisher``, publishes
``std_msgs/String`` messages on the ``sensor_data`` topic at 1 Hz,
but only while in the **Active** state.

The publisher is allocated on ``configure`` and released on
``cleanup``; the timer is created on ``activate`` and cancelled on
``deactivate``.

Each message carries an incrementing counter so consumers can detect
gaps caused by deactivation.

.. note::

   State transitions are driven externally from the CLI with
   ``ros2 lifecycle set``, so the node reacts to operator commands
   rather than cycling itself.


**Class Declaration**

.. code-block:: python
   :emphasize-lines: 5

   import rclpy
   from rclpy_lifecycle import LifecycleNode, TransitionCallbackReturn
   from std_msgs.msg import String

   class SensorPublisher(LifecycleNode):
       def __init__(self):
           super().__init__('sensor_publisher')
           self._publisher = None
           self._timer = None
           self._counter = 0

- ``LifecycleNode`` is imported from ``rclpy_lifecycle``, part of
  the standard ROS 2 Jazzy installation.
- Publishers and timers are declared as ``None`` here. They are
  created in ``on_configure``, not in ``__init__``, so they are
  only allocated when explicitly requested.
- ``TransitionCallbackReturn`` carries three values: ``SUCCESS``,
  ``FAILURE``, and ``ERROR``. A callback returning ``FAILURE``
  aborts the transition and keeps the node in its current state.


**on_configure: Allocate Resources**

.. code-block:: python
   :emphasize-lines: 3-8

   def on_configure(self, state):
       self.get_logger().info(f'Configuring from: {state.label}')
       try:
           self._publisher = self.create_lifecycle_publisher(String, 'sensor_data', 10)
       except Exception as e:
           self.get_logger().error(f'Configuration failed: {e}')
           return TransitionCallbackReturn.FAILURE
       return TransitionCallbackReturn.SUCCESS

- Use ``create_lifecycle_publisher`` instead of
  ``create_publisher``. A lifecycle publisher is created here but
  remains **inactive** until ``on_activate`` is called.
- An inactive lifecycle publisher silently discards any messages
  published to it, preventing data from being sent before the node
  is fully ready.
- Returning ``FAILURE`` on a recoverable problem keeps the node in
  **Unconfigured**; the operator can fix the issue and reissue
  ``configure``.
- Do **not** create timers here. Timer callbacks would fire even
  while the node is Inactive.


**Failure vs. Error**

A transition callback returns one of three values from
``TransitionCallbackReturn``. The choice determines what state the
node ends up in.

.. list-table:: Return values from a transition callback and their
   effect on the state machine
   :widths: 20 35 45
   :header-rows: 1

   * - Return
     - Meaning
     - Resulting state
   * - ``SUCCESS``
     - Transition completed correctly.
     - Moves to the target state.
   * - ``FAILURE``
     - Transition could not complete, but the node is in a clean,
       recoverable state.
     - Stays in the **previous** state. The transition can be
       retried.
   * - ``ERROR``
     - Something unexpected happened; the node may be in an
       inconsistent state.
     - Invokes ``on_error``. The default ``on_error`` returns
       ``FAILURE``, which moves the node to **Finalized**.

- **When to return ``FAILURE``**: parameter missing, hardware not
  yet responding, expected file not found. Nothing was
  half-allocated.
- **When to return ``ERROR``**: an exception was raised after
  partial setup, leaving some resources allocated and others not.
- Overriding ``on_error`` is **optional** but useful: cleaning up
  partial state and returning ``SUCCESS`` sends the node back to
  **Unconfigured** for a fresh retry, instead of straight to
  **Finalized**.


**on_activate: Start Processing**

.. code-block:: python

   def on_activate(self, state):
       super().on_activate(state)           # enables the lifecycle publisher
       self._timer = self.create_timer(1.0, self._publish_sensor_data)
       return TransitionCallbackReturn.SUCCESS

   def _publish_sensor_data(self):
       msg = String(data=f'Reading {self._counter}')
       self._publisher.publish(msg)
       self._counter += 1

.. note::

   Always call ``super().on_activate(state)`` **before** publishing.
   The base class activates the lifecycle publisher; messages sent
   before this call are silently dropped.


**on_deactivate: Stop Processing**

.. code-block:: python

   def on_deactivate(self, state):
       if self._timer is not None:
           self._timer.cancel()
           self._timer = None
       super().on_deactivate(state)         # disables the lifecycle publisher
       return TransitionCallbackReturn.SUCCESS

- Cancel the timer first so no further callbacks fire, then call
  ``super().on_deactivate(state)`` to disable the publisher.
- The publisher object still exists after deactivation. It is
  re-enabled by the next ``on_activate`` call without needing to be
  recreated.


**on_cleanup: Release Resources**

.. code-block:: python

   def on_cleanup(self, state):
       self._publisher = None
       self._counter = 0
       return TransitionCallbackReturn.SUCCESS

   def main(args=None):
       rclpy.init(args=args)
       rclpy.spin(SensorPublisher())
       rclpy.shutdown()

- Setting ``self._publisher = None`` drops the only reference,
  allowing the publisher to be garbage-collected. The node returns
  to **Unconfigured** and can be reconfigured.


**Demonstration: Changing States with the CLI**

Use ``ros2 lifecycle list /sensor_publisher`` to output a list of
available transitions.

.. list-table:: Driving the lifecycle node from the CLI
   :widths: 5 45 50
   :header-rows: 1

   * - Term
     - Command
     - Effect
   * - T1
     - ``ros2 run lifecycle_demo sensor_pub_exe``
     - Start the node (Unconfigured)
   * - T2
     - ``ros2 lifecycle nodes``
     - Output a list of nodes with lifecycle
   * - T2
     - ``ros2 lifecycle get /sensor_publisher``
     - ``unconfigured [1]``
   * - T2
     - ``ros2 lifecycle set /sensor_publisher configure``
     - Inactive: publisher created, no data
   * - T2
     - ``ros2 lifecycle set /sensor_publisher activate``
     - Active: timer starts, data flows
   * - T3
     - ``ros2 topic echo /sensor_data``
     - Confirm data is being published
   * - T2
     - ``ros2 lifecycle set /sensor_publisher deactivate``
     - Pause: timer cancelled, publisher disabled
   * - T2
     - ``ros2 lifecycle set /sensor_publisher cleanup``
     - Release resources, back to Unconfigured

.. admonition:: Experiment
   :class: hint

   After cleanup the node is **Unconfigured** again. Issue
   ``configure`` and ``activate`` a second time. Does the counter
   reset? What does this tell you about when ``on_cleanup`` runs
   relative to ``__init__``?


Programmatic State Changes
----------------------------------------------------

Instead of waiting for an operator, a lifecycle node can drive its
own transitions by calling the ``change_state`` service that every
lifecycle node automatically advertises.


**Scenario**

A lifecycle node, ``self_cycling_node``, drives its own state
transitions on a 5 second timer instead of waiting for CLI commands.
It walks through the full sequence indefinitely:

.. math::

   \text{Unconfigured} \xrightarrow{\texttt{configure}}
   \text{Inactive} \xrightarrow{\texttt{activate}}
   \text{Active} \xrightarrow{\texttt{deactivate}}
   \text{Inactive} \xrightarrow{\texttt{cleanup}}
   \text{Unconfigured} \to \ldots

The publish behavior mirrors ``sensor_publisher``: a
``std_msgs/String`` publisher on ``sensor_data`` allocated on
``configure``, a 1 Hz publish timer started on ``activate``, and an
incrementing counter reset on ``cleanup``.

.. note::

   The cycling timer keeps running across all four states.
   Transitions are requested by the node calling its own
   ``change_state`` service.


**Key Insight: The Service Already Exists**

.. note::

   Every node that extends ``LifecycleNode`` **automatically
   advertises** a service of type ``lifecycle_msgs/srv/ChangeState``
   at ``/<node_name>/change_state``. We do **not** create the
   service; we only need a client to call it.

- Calling this service programmatically is exactly equivalent to
  running ``ros2 lifecycle set`` from the CLI; the CLI itself is
  just another client of the same service.
- The request payload is a ``Transition`` message whose ``id``
  field selects which transition to request
  (``TRANSITION_CONFIGURE``, ``TRANSITION_ACTIVATE``, ...).
- The response carries a single ``success`` boolean: ``True`` if
  the transition callback returned ``SUCCESS``, ``False`` otherwise.


**Class Declaration: Cycle List and Client**

.. code-block:: python
   :emphasize-lines: 2-7,15

   class SelfCyclingNode(LifecycleNode):
       _CYCLE = [
           Transition.TRANSITION_CONFIGURE,
           Transition.TRANSITION_ACTIVATE,
           Transition.TRANSITION_DEACTIVATE,
           Transition.TRANSITION_CLEANUP,
       ]

       def __init__(self):
           super().__init__('self_cycling_node')
           self._publisher = None
           self._timer = None
           self._counter = 0
           self._step = 0
           self._cli = self.create_client(ChangeState, f'/{self.get_name()}/change_state')
           self._cycle_timer = self.create_timer(5.0, self._advance_state)

- ``_CYCLE`` encodes the transition order; ``_step`` is the index
  advanced on every tick.
- The client target is built with ``self.get_name()`` so the path
  stays consistent if the node is later renamed (e.g. via
  ``remap``).
- ``_cycle_timer`` is a regular timer (not lifecycle-managed) and
  keeps firing in every state.


**Timer Callback: Request the Next Transition**

.. code-block:: python

   def _advance_state(self):
       if not self._cli.wait_for_service(timeout_sec=1.0):
           self.get_logger().warn('change_state service not available')
           return

       transition_id = self._CYCLE[self._step % len(self._CYCLE)]
       req = ChangeState.Request()
       req.transition.id = transition_id

       future = self._cli.call_async(req)
       future.add_done_callback(self._on_change_state_done)

       self._step += 1

- ``self._step % len(self._CYCLE)`` wraps the index so the cycle
  repeats forever.
- The request payload is a ``ChangeState.Request()`` whose
  ``transition.id`` field selects the next transition.
- ``call_async`` avoids deadlock: the timer callback runs inside
  the executor, and a blocking ``call`` would prevent the same
  executor from servicing the response.


**Done Callback: Inspect the Result**

.. code-block:: python

   def _on_change_state_done(self, future):
       result = future.result()
       if result is not None and result.success:
           self.get_logger().info('Transition succeeded.')
       else:
           self.get_logger().error('Transition failed.')

- Registered via ``future.add_done_callback(...)`` in
  ``_advance_state``; the executor invokes it once the service
  response arrives.
- ``future.result()`` returns ``None`` if the call was cancelled or
  failed before reaching the server, so it must be checked before
  reading ``result.success``.
- ``result.success`` is ``True`` only if the corresponding
  lifecycle callback (``on_configure``, ``on_activate``, ...)
  returned ``TransitionCallbackReturn.SUCCESS``.


**Lifecycle Callbacks**

The four transition callbacks are identical to ``sensor_publisher``;
only the *trigger* differs.

.. code-block:: python

   def on_configure(self, state):
       ...

   def on_activate(self, state):
       ...

   def on_deactivate(self, state):
       ...

   def on_cleanup(self, state):
       ...


**Demonstration**

.. list-table:: Automated state changes
   :widths: 5 45 50
   :header-rows: 1

   * - Term
     - Command
     - Effect
   * - T1
     - ``ros2 run lifecycle_demo self_cycling_exe``
     - Start the node; cycling begins after 5 s
   * - T2
     - ``ros2 lifecycle get /self_cycling_node``
     - Watch the state advance every 5 s
   * - T3
     - ``ros2 topic echo /sensor_data``
     - ``/sensor_data`` appears and disappears with each
       activate/deactivate
   * - T1
     - All four transitions are reported in the node's own log
       output
     -

.. note::

   Full cycle: Unconfigured :math:`\xrightarrow{5\,\text{s}}`
   Inactive :math:`\xrightarrow{5\,\text{s}}` Active
   :math:`\xrightarrow{5\,\text{s}}` Inactive
   :math:`\xrightarrow{5\,\text{s}}` Unconfigured
   :math:`\xrightarrow{5\,\text{s}}` ...

.. admonition:: Experiment
   :class: hint

   Modify the ``_CYCLE`` list to skip ``TRANSITION_DEACTIVATE`` and
   ``TRANSITION_CLEANUP`` so the node only cycles between configure
   and activate. What happens? Then add
   ``Transition.TRANSITION_SHUTDOWN`` at the end of the original
   list and observe the result.


ROS 2 Bags
====================================================

A **ROS 2 bag** is a file that records messages published on any
set of topics, along with their timestamps, so they can be replayed
later exactly as they were produced. Bags are the primary tool for
capturing real or simulated robot runs and replaying them offline
for debugging, algorithm development, and regression testing.

.. admonition:: Resources
   :class: resources

   - `ROS 2: Recording and Playing Back Data
     <https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html>`_
   - `rosbag2 on GitHub <https://github.com/ros2/rosbag2>`_
   - `MCAP format documentation <https://mcap.dev/>`_


Common Use Cases
----------------------------------------------------

- **Algorithm development**: record sensor data from Gazebo, then
  iterate on a perception or planning algorithm by replaying the
  same bag repeatedly without restarting the simulation.
- **Debugging**: capture a run where the robot behaved unexpectedly,
  then replay it with additional subscribers or visualization tools
  attached.
- **Regression testing**: keep a reference bag and replay it against
  a new version of the code to check that outputs have not changed.
- **Dataset creation**: record annotated sensor streams for training
  or evaluating machine learning models.
- **Remote operation**: record a run on a robot that is not always
  accessible, then analyze the data back at the workstation.

.. note::

   During replay, ROS 2 republishes messages on the same topics they
   were recorded from, with the original timestamps preserved. Any
   node that subscribes to those topics receives the replayed data
   exactly as if the original publisher were still running.


Storage Formats
----------------------------------------------------

ROS 2 bags support pluggable storage backends. The two formats
available in Jazzy are **SQLite3** (default) and **MCAP**. Choosing
the right format matters for large navigation datasets.

.. list-table:: SQLite3 vs. MCAP
   :widths: 20 40 40
   :header-rows: 1

   * -
     - SQLite3
     - MCAP
   * - Default
     - Yes
     - No (requires plugin install)
   * - File extension
     - ``.db3``
     - ``.mcap``
   * - Performance
     - Good for low-bandwidth topics
     - Better for high-rate topics (e.g., LiDAR)
   * - Random access
     - Slow on large files
     - Fast seek to any timestamp
   * - Tooling
     - Standard SQL inspection
     - Foxglove Studio, mcap CLI
   * - When to use
     - Short runs, text topics, parameters
     - Long navigation runs, sensor-heavy bags

Install the MCAP plugin:

.. code-block:: console

   sudo apt install ros-jazzy-rosbag2-storage-mcap

.. note::

   MCAP is the recommended format for navigation bags that include
   ``/scan`` at high rates. A 10-minute navigation run recording
   LiDAR at 10 Hz can easily exceed 1 GB with SQLite3 due to
   indexing overhead; MCAP compresses significantly better and
   allows fast scrubbing in Foxglove Studio.


**Switching the Storage Format**

Pass ``--storage`` to any ``ros2 bag`` command to select the
backend:

- Record with SQLite3 (default, no flag needed):

  .. code-block:: console

     ros2 bag record -o my_bag /scan

- Record with MCAP:

  .. code-block:: console

     ros2 bag record -o my_bag --storage mcap /scan

- Convert an existing SQLite3 bag to MCAP:

  .. code-block:: console

     ros2 bag convert -i my_bag -o my_bag_mcap --output-storage mcap

.. note::

   The bag directory always contains a ``metadata.yaml`` file that
   records the storage plugin used, the list of topics, message
   counts, and the time range. ``ros2 bag info`` reads this file
   and does not need the storage plugin to be installed.


Recording
----------------------------------------------------

``ros2 bag record`` subscribes to the specified topics and writes
every incoming message to disk. Recording stops when you press
``Ctrl+C``.


**Useful Recording Options**

.. list-table:: Useful flags for ``ros2 bag record``
   :widths: 35 65
   :header-rows: 1

   * - Flag
     - Effect
   * - ``-o <name>``
     - Set the output directory name. Defaults to a timestamped
       name.
   * - ``-a``
     - Record all topics currently being published.
   * - ``--storage mcap``
     - Use MCAP instead of SQLite3.
   * - ``--max-bag-size <bytes>``
     - Split the bag into multiple files once the size limit is
       reached.
   * - ``--max-bag-duration <s>``
     - Split the bag by time duration instead of size.
   * - ``-e <regex>``
     - Record only topics matching a regular expression.

.. note::

   Recording ``/tf_static`` requires special handling: it is a
   latched topic and its messages are only published once at
   startup. Always include ``/tf_static`` explicitly rather than
   relying on ``-a`` to catch it.


**Recording a Navigation Run**

Record the topics needed to reconstruct a full navigation run
offline:

.. list-table:: Demonstration
   :widths: 5 95
   :header-rows: 1

   * - Term
     - Command
   * - T1
     - ``ros2 launch rosbot_gazebo husarion_world.launch.py rviz:=False use_sim:=True``
   * - T2
     - ``cd ~/enpm605_ws/src/lecture14/bag_demo/bags``
   * - T2
     - ``ros2 bag record -o nav_run --storage mcap /odometry/filtered /scan /cmd_vel /tf /tf_static /map``
   * - T3
     - ``ros2 launch nav_demo map_nav.launch.py mode:=navigation goal_source:=waypoints``
   * - T2
     - ``Ctrl + C`` when the last waypoint is reached

.. list-table:: Topics recorded
   :widths: 25 35 40
   :header-rows: 1

   * - Topic
     - Message type
     - Why it is needed
   * - ``/odometry/filtered``
     - ``nav_msgs/Odometry``
     - Robot pose and velocity estimates
   * - ``/scan``
     - ``sensor_msgs/LaserScan``
     - LiDAR measurements for mapping and localization
   * - ``/cmd_vel``
     - ``geometry_msgs/TwistStamped``
     - Velocity commands sent to the robot
   * - ``/tf``
     - ``tf2_msgs/TFMessage``
     - Dynamic transforms
   * - ``/tf_static``
     - ``tf2_msgs/TFMessage``
     - Static transforms
   * - ``/map``
     - ``nav_msgs/OccupancyGrid``
     - Static occupancy grid published by ``map_server``


Inspecting
----------------------------------------------------

Before replaying a bag, inspect it to verify the recorded topics,
message counts, time range, and storage format.

.. code-block:: console

   ros2 bag info nav_run

- Check that all expected topics are present and their message
  counts are non-zero before replaying.
- A count of zero on ``/tf_static`` usually means the static
  publisher was not running when recording started.


Replaying
----------------------------------------------------

``ros2 bag play`` republishes recorded messages on their original
topics at the recorded timestamps, so any node subscribed to those
topics receives the data as if the original publisher were running.


**Basic Replay**

.. code-block:: console

   ros2 bag play nav_run

.. list-table:: Useful replay options
   :widths: 40 60
   :header-rows: 1

   * - Flag
     - Effect
   * - ``--rate 0.5``
     - Replay at half speed. Useful for inspecting fast events.
   * - ``--start-offset <s>``
     - Skip the first *n* seconds before starting replay.
   * - ``--loop``
     - Repeat the bag indefinitely.
   * - ``--topics /scan``
     - Replay only a subset of recorded topics.
   * - ``--remap /scan:=/scan_bag``
     - Remap a topic during replay to avoid clashing with a live
       publisher.
   * - ``--clock``
     - Publish a ``/clock`` topic so nodes using sim time stay in
       sync.

.. note::

   If the live system is also running (e.g., Gazebo is still open),
   replaying ``/tf`` and ``/cmd_vel`` will conflict with the live
   publishers. Either close the live system before replaying, or
   use ``--remap`` to redirect the replayed topics to different
   names.


Foxglove Studio
====================================================

**Foxglove** is a free, cross-platform visualization tool
purpose-built for robotics. It opens MCAP bags directly (no
conversion) and lets you inspect topics, plot signals, and render
3D scenes from a multi-panel layout, without writing any code.

.. admonition:: Resources
   :class: resources

   - `Foxglove website <https://foxglove.dev/>`_
   - `Foxglove documentation <https://docs.foxglove.dev/docs>`_
   - `Foxglove desktop downloads <https://foxglove.dev/download>`_
   - `Foxglove web app (no install) <https://app.foxglove.dev/>`_
   - `Panel reference
     <https://docs.foxglove.dev/docs/visualization/panels/introduction>`_
   - `MCAP file format <https://mcap.dev/>`_
   - `Pricing and academic access <https://foxglove.dev/pricing>`_


What and Why
----------------------------------------------------

Foxglove Studio is what most teams reach for when ``rqt`` and
``rviz2`` stop scaling -- it gives you many time-aligned views of
the same recording in one window.

- **Native MCAP support** -- opens ``*.mcap`` files directly, no
  transcoding.
- **Multi-panel layouts** -- 3D, Plot, Image, Raw Messages,
  Diagnostics, Teleop, ... all driven from the same timeline.
- **Offline or live** -- read a saved bag, or connect to a running
  ROS 2 system over the Foxglove WebSocket bridge.
- **Cross-platform** -- desktop app for Linux, macOS, and Windows,
  or run entirely in the browser at ``app.foxglove.dev`` (your bag
  stays local; nothing is uploaded).

.. note::

   Foxglove and ``rviz2`` solve overlapping problems. Use ``rviz2``
   when you want a quick 3D view of a live system; use Foxglove
   when you need to scrub through a recording, plot a signal, and
   inspect raw messages *at the same time*.


Installing and Launching
----------------------------------------------------

Pick whichever install method you prefer (all three open the same
app and read the same bags).

- **Option 1:** Debian package (recommended on Ubuntu)

  - Download the ``.deb`` from the `Foxglove downloads page
    <https://foxglove.dev/download>`_, then:

  .. code-block:: console

     sudo apt install ./foxglove-studio-*-linux-amd64.deb
     foxglove-studio &

- **Option 2:** Snap

  .. code-block:: console

     sudo snap install foxglove-studio
     foxglove-studio &

- **Option 3:** Browser (no install)

  - Open `https://app.foxglove.dev/ <https://app.foxglove.dev/>`_.
    The bag file you choose is read locally in the browser
    (nothing is uploaded).

.. note::

   The browser version requires Chrome/Edge/Firefox. Safari is not
   supported. For the best 3D performance on large bags, prefer the
   desktop app.


Loading the ``nav_run`` Bag
----------------------------------------------------

From the welcome screen, choose **"Open local file"** and point
Foxglove at the ``nav_run_0.mcap`` file inside the bag directory
(not the directory itself).

- **File** :math:`\to` **Open local file...** :math:`\to`
  ``nav_run_0.mcap``
- Foxglove parses the file in seconds and shows a timeline at the
  bottom with all recorded topics in the left sidebar.

.. note::

   Foxglove can also open ROS 2 SQLite3 bags (``*.db3``) and ROS 1
   bags (``*.bag``), but MCAP is the fastest and most fully
   featured.


**Visualizing the Recording**

Add multiple panels to visualize the results/outputs while the bag
is playing. You can import the provided layout
``nav_run_layout.json``.
