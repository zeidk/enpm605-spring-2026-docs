====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 14: Lifecycle Nodes
and ROS 2 Bags. Topics include the lifecycle state machine
(Unconfigured, Inactive, Active, Finalized), transition commands
and callbacks, ``LifecycleNode``, ``create_lifecycle_publisher``,
``TransitionCallbackReturn`` (``SUCCESS``, ``FAILURE``, ``ERROR``),
programmatic state changes via the ``change_state`` service, ROS 2
bag storage formats (SQLite3 vs. MCAP), recording, inspecting and
replaying bags, and Foxglove Studio.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement
     is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   In what state is a lifecycle node immediately after being
   constructed?

   A. Active

   B. Inactive

   C. Unconfigured

   D. Finalized

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- **Unconfigured**.

   A lifecycle node is created in the Unconfigured state. It holds
   no resources (no publishers, timers, or subscriptions) and stays
   there until a ``configure`` command is issued.


.. admonition:: Question 2
   :class: hint

   Which transition command moves a node from **Inactive** to
   **Active**?

   A. ``configure``

   B. ``activate``

   C. ``cleanup``

   D. ``shutdown``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``activate``.

   ``activate`` invokes the ``on_activate`` callback and moves the
   node from Inactive to Active. Publishers become live and timers
   should be started in this callback.


.. admonition:: Question 3
   :class: hint

   What is the effect of returning ``TransitionCallbackReturn.FAILURE``
   from a transition callback?

   A. The node moves to **Finalized**.

   B. The node stays in the previous state and the transition can
      be retried.

   C. The node moves directly to **Active**.

   D. ROS 2 raises an exception and shuts down the executor.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The node stays in the previous state.

   ``FAILURE`` signals a recoverable problem in which nothing was
   half-allocated. The node remains in its prior state, so the
   operator can fix the issue and reissue the transition.


.. admonition:: Question 4
   :class: hint

   Why should publishers be created with
   ``create_lifecycle_publisher`` rather than ``create_publisher``
   inside a ``LifecycleNode``?

   A. ``create_publisher`` is deprecated in Jazzy.

   B. A lifecycle publisher silently discards messages when the
      node is not Active, preventing premature data from being
      sent.

   C. ``create_lifecycle_publisher`` is faster.

   D. Lifecycle publishers automatically subscribe to themselves
      for diagnostics.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Lifecycle publishers stay inactive until
   ``on_activate`` runs, so any message published before then is
   silently dropped instead of being delivered to subscribers
   prematurely.


.. admonition:: Question 5
   :class: hint

   Which service does every ``LifecycleNode`` automatically
   advertise so external clients (or the node itself) can request
   transitions?

   A. ``/<node_name>/get_state``

   B. ``/<node_name>/change_state``

   C. ``/lifecycle_manager``

   D. ``/<node_name>/transition``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``/<node_name>/change_state``.

   The service has type ``lifecycle_msgs/srv/ChangeState``. The
   ``ros2 lifecycle set`` CLI is just one client of this service;
   any node can call it programmatically with a service client.


.. admonition:: Question 6
   :class: hint

   Which ROS 2 bag storage backend is recommended for long
   navigation runs that include high-rate LiDAR data?

   A. SQLite3

   B. MCAP

   C. CSV

   D. ROS 1 ``.bag``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- **MCAP**.

   MCAP compresses sensor-heavy data better than SQLite3 and
   supports fast random-access seeks, which makes scrubbing through
   long bags in Foxglove Studio practical.


.. admonition:: Question 7
   :class: hint

   What does the ``--clock`` flag do when running ``ros2 bag play``?

   A. Replays the bag at real time only.

   B. Publishes a ``/clock`` topic so subscribers using sim time
      stay synchronized to the bag's timestamps.

   C. Prints elapsed time to the console.

   D. Replays only the messages within the last 60 seconds of the
      bag.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It publishes a ``/clock`` topic.

   Nodes configured with ``use_sim_time:=true`` will use this clock
   instead of wall-clock time, so timestamps in their callbacks
   match the bag's recording time.


.. admonition:: Question 8
   :class: hint

   Why must ``/tf_static`` be listed explicitly in
   ``ros2 bag record`` rather than relying on ``-a``?

   A. ``/tf_static`` is a private topic and is hidden from ``-a``.

   B. ``/tf_static`` is a latched topic with messages published
      only at startup, so a recorder started later will see no
      messages unless it is explicitly subscribed.

   C. The ``-a`` flag does not exist in Jazzy.

   D. ``/tf_static`` requires a special storage format.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``/tf_static`` is latched and published once.

   If the recorder is started after the static publisher, it may
   miss the message entirely. Including ``/tf_static`` explicitly
   triggers a transient-local subscription that fetches the latched
   message.


----


True / False
============

.. admonition:: Question 9
   :class: hint

   A lifecycle node can transition directly from **Unconfigured**
   to **Active** in a single ``activate`` command.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   Transitions follow the state machine strictly. The node must
   first ``configure`` (Unconfigured :math:`\to` Inactive) and then
   ``activate`` (Inactive :math:`\to` Active). Skipping
   ``configure`` causes ``ros2 lifecycle set`` to report
   **Transition failed**.


.. admonition:: Question 10
   :class: hint

   ``ros2 bag info`` requires the storage plugin used to record the
   bag to be installed locally before it can read the bag's
   metadata.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ``ros2 bag info`` reads the ``metadata.yaml`` file inside the
   bag directory. That file lists the storage plugin, topics,
   message counts, and time range, none of which require the
   plugin to be installed. Replaying the bag, however, *does*
   require the plugin.


.. admonition:: Question 11
   :class: hint

   In ``on_activate``, you should publish your first message
   *before* calling ``super().on_activate(state)``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ``super().on_activate(state)`` enables the lifecycle publisher.
   Messages published before that call are silently dropped.
   Always activate the base class first, then publish.


.. admonition:: Question 12
   :class: hint

   Foxglove Studio uploads any bag you open in the browser version
   to a remote server.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The browser version reads the file locally; nothing is
   uploaded. The browser is restricted to Chrome, Edge, or Firefox
   (no Safari).


----


Short Answer
============

.. admonition:: Question 13
   :class: hint

   Explain why timers should be created in ``on_activate`` and
   cancelled in ``on_deactivate`` rather than allocated in
   ``__init__``.

.. dropdown:: Answer
   :class-container: sd-border-success

   Timers fire callbacks that typically publish data or perform
   work. Allocating them in ``__init__`` would mean they start
   firing the moment the node is constructed -- before the
   operator has had a chance to ``configure`` and ``activate`` the
   node, and before any subscribers may be ready. Creating the
   timer in ``on_activate`` and cancelling it in ``on_deactivate``
   ties the work directly to the **Active** state and lets the
   operator pause and resume the node without restarting it.


.. admonition:: Question 14
   :class: hint

   Why does the self-cycling node use ``call_async`` instead of a
   blocking call to invoke its own ``change_state`` service?

.. dropdown:: Answer
   :class-container: sd-border-success

   The timer callback runs inside the same executor that must
   service the ``change_state`` response. A blocking ``call`` would
   wait for the response while preventing the executor from ever
   delivering it -- a classic single-threaded deadlock.
   ``call_async`` returns a future immediately and lets the
   executor process the response in its normal callback dispatch
   loop.


.. admonition:: Question 15
   :class: hint

   You recorded a navigation bag with ``/scan``, ``/tf``,
   ``/tf_static``, ``/odometry/filtered``, and ``/cmd_vel``, but
   when you replay it later in Foxglove the robot mesh is missing
   from the 3D panel even though laser scans appear correctly.
   Suggest a likely cause and a fix.

.. dropdown:: Answer
   :class-container: sd-border-success

   The robot mesh is published as a ``robot_description`` parameter
   (consumed by ``robot_state_publisher``), and the static joints /
   visual frames may also depend on ``/tf_static``. If
   ``/tf_static`` was empty (recorder started after the static
   publisher), Foxglove cannot place the visual frames relative to
   ``base_link``. A fix is to start ``ros2 bag record`` *before*
   the simulation/robot_state_publisher is launched, or to launch
   ``robot_state_publisher`` alongside the bag during replay so the
   description and static transforms are available.
