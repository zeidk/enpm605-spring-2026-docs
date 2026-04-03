====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 13: Behavior Trees
and Project Integration, including BT fundamentals, node types,
the tick mechanism, the ``py_trees`` library, Blackboard communication,
ROS 2 integration with ``py_trees_ros``, lifecycle node management
from a BT, and debugging strategies.

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

   What are the three possible return statuses of a behavior tree node?

   A. ``PASS``, ``FAIL``, ``WAIT``

   B. ``SUCCESS``, ``FAILURE``, ``RUNNING``

   C. ``TRUE``, ``FALSE``, ``PENDING``

   D. ``DONE``, ``ERROR``, ``ACTIVE``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``SUCCESS``, ``FAILURE``, ``RUNNING``

   Every node in a behavior tree returns one of exactly three statuses
   on each tick: ``SUCCESS`` (the task completed), ``FAILURE`` (the
   task could not be completed), and ``RUNNING`` (the task is still
   in progress and needs to be ticked again). These statuses propagate
   up through the tree to determine overall behavior.


.. admonition:: Question 2
   :class: hint

   How does a **Sequence** node differ from a **Fallback** (Selector)
   node?

   A. A Sequence succeeds if any child succeeds; a Fallback succeeds
      if all children succeed.

   B. A Sequence succeeds if all children succeed; a Fallback succeeds
      if any child succeeds.

   C. Both succeed only when all children succeed, but they tick
      children in opposite order.

   D. A Sequence runs children in parallel; a Fallback runs them
      sequentially.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A Sequence succeeds if all children succeed; a Fallback
   succeeds if any child succeeds.

   A Sequence node ticks children left to right and returns ``SUCCESS``
   only when every child returns ``SUCCESS``. It returns ``FAILURE``
   immediately when any child fails (analogous to logical AND). A
   Fallback (Selector) node also ticks left to right but returns
   ``SUCCESS`` as soon as any child succeeds and returns ``FAILURE``
   only when all children fail (analogous to logical OR).


.. admonition:: Question 3
   :class: hint

   What is the primary advantage of behavior trees over finite state
   machines for complex robotic systems?

   A. BTs execute faster than FSMs because they have fewer nodes.

   B. BTs use less memory because they do not store state.

   C. BTs offer better modularity and scalability -- adding a new
      behavior requires inserting a subtree rather than rewiring
      transitions across the entire graph.

   D. BTs can only be used with ROS 2, making them more specialized.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- BTs offer better modularity and scalability -- adding a
   new behavior requires inserting a subtree rather than rewiring
   transitions across the entire graph.

   In an FSM, adding a new state potentially requires adding
   transitions to and from every existing state, leading to
   combinatorial complexity. In a behavior tree, a new behavior is
   a self-contained subtree that can be inserted at any point without
   modifying existing nodes. BTs also support natural priority
   ordering through their left-to-right tick evaluation and provide
   inherent reactivity through root-level re-evaluation on every tick.


.. admonition:: Question 4
   :class: hint

   What does the ``memory`` parameter control in a ``py_trees``
   Sequence?

   A. It determines how much RAM the Sequence uses.

   B. It controls whether the Sequence remembers which child was
      ``RUNNING`` and resumes from there, or restarts from the first
      child on every tick.

   C. It enables logging of past tick results for debugging.

   D. It stores the return status of all children for post-tick
      analysis.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It controls whether the Sequence remembers which child
   was ``RUNNING`` and resumes from there, or restarts from the first
   child on every tick.

   When ``memory=True``, a Sequence that was interrupted by a
   ``RUNNING`` child will resume from that child on the next tick,
   skipping previously successful children. When ``memory=False``,
   the Sequence restarts from the first child every tick, which means
   condition checks at the beginning are re-evaluated on every cycle.
   Use ``memory=False`` for reactive behavior where conditions may
   change between ticks.


.. admonition:: Question 5
   :class: hint

   What is the purpose of the Blackboard in ``py_trees``?

   A. It is a visualization tool for displaying the tree structure.

   B. It is a shared key-value store that allows behaviors to exchange
      data without direct coupling.

   C. It is a logging mechanism that records all tick results.

   D. It is a configuration file that defines the tree topology.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It is a shared key-value store that allows behaviors to
   exchange data without direct coupling.

   The Blackboard is a centralized data store accessed through client
   objects. Behaviors register keys with either ``READ`` or ``WRITE``
   access, then read or write values during their ``update()`` method.
   This allows a sensor behavior to write data that a condition
   behavior reads, without either behavior knowing about the other.
   Namespaces prevent key collisions in large trees.


.. admonition:: Question 6
   :class: hint

   In the ``py_trees.behaviour.Behaviour`` lifecycle, which method
   is called on every tick while the behavior is active?

   A. ``setup()``

   B. ``initialise()``

   C. ``update()``

   D. ``terminate()``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``update()``

   The behavior lifecycle is: ``setup()`` runs once during tree
   initialization; ``initialise()`` runs when the behavior transitions
   from idle to active (first tick or after reset); ``update()`` runs
   on every tick while the behavior is active and must return a
   ``Status``; ``terminate()`` runs when the behavior is interrupted
   or returns a terminal status. Only ``update()`` is called on every
   active tick.


.. admonition:: Question 7
   :class: hint

   Which ``py_trees`` decorator would you use to make a behavior
   tree branch succeed only when its child **fails**?

   A. ``Retry``

   B. ``Timeout``

   C. ``Inverter``

   D. ``Repeat``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``Inverter``

   The ``Inverter`` decorator flips ``SUCCESS`` to ``FAILURE`` and
   ``FAILURE`` to ``SUCCESS``. It passes ``RUNNING`` through
   unchanged. This is useful for negating condition checks -- for
   example, creating a "not at goal" condition by inverting an
   "at goal" condition, rather than writing a separate behavior.


.. admonition:: Question 8
   :class: hint

   How does ``py_trees_ros.subscribers.ToBlackboard`` make sensor
   data available to other behaviors in the tree?

   A. It passes the data directly to sibling behaviors through
      function calls.

   B. It publishes the data on a new ROS 2 topic that other behaviors
      subscribe to.

   C. It subscribes to a ROS 2 topic and writes the received data to
      the Blackboard, where other behaviors can read it.

   D. It stores the data in a ROS 2 parameter that other nodes can
      query.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It subscribes to a ROS 2 topic and writes the received
   data to the Blackboard, where other behaviors can read it.

   ``ToBlackboard`` is a pre-built behavior that creates a ROS 2
   subscription internally. On each tick, it checks for the latest
   message and writes it (or selected fields) to specified Blackboard
   keys. Other behaviors in the tree then read these keys through
   their own Blackboard clients, maintaining the decoupled
   communication pattern that makes behavior trees modular.


----


True / False
============

.. admonition:: Question 9
   :class: hint

   **True or False:** A condition node in a behavior tree should
   never return ``RUNNING``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Condition nodes are leaf nodes that check a state and return
   either ``SUCCESS`` or ``FAILURE`` immediately. They represent
   instantaneous checks (e.g., "is the battery above 20%?", "is
   the path clear?") and should never return ``RUNNING``. Only
   action nodes may return ``RUNNING`` to indicate ongoing work
   across multiple ticks.


.. admonition:: Question 10
   :class: hint

   **True or False:** In a behavior tree, the root node is ticked
   only once and then the tree runs autonomously.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The root node is ticked **repeatedly** at a fixed rate (e.g.,
   10 Hz). Each tick propagates through the tree from the root,
   evaluating conditions and executing actions. This continuous
   re-evaluation is what makes behavior trees reactive -- the tree
   can respond to changing conditions on every tick cycle.


.. admonition:: Question 11
   :class: hint

   **True or False:** Calling ``time.sleep()`` inside a behavior's
   ``update()`` method is an acceptable way to implement a timed
   action.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Calling ``time.sleep()`` in ``update()`` blocks the entire tree
   tick, preventing all other behaviors from executing during the
   sleep period. The correct approach is to track elapsed time and
   return ``RUNNING`` on each tick until the desired duration has
   passed, then return ``SUCCESS``. This allows the tree to continue
   ticking other branches concurrently.


.. admonition:: Question 12
   :class: hint

   **True or False:** A behavior tree can manage ROS 2 lifecycle
   node transitions by calling the ``change_state`` service from
   within a behavior's ``update()`` method.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A behavior can create a ROS 2 service client for the lifecycle
   node's ``change_state`` service and send transition requests
   (e.g., ``TRANSITION_CONFIGURE``, ``TRANSITION_ACTIVATE``)
   asynchronously. The behavior returns ``RUNNING`` while waiting
   for the service response and ``SUCCESS`` or ``FAILURE`` when
   the response arrives. This pattern allows the BT to orchestrate
   the startup and shutdown of managed nodes.


.. admonition:: Question 13
   :class: hint

   **True or False:** Two behaviors writing to the same Blackboard
   key without coordination is safe because the Blackboard handles
   concurrent access internally.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   While the Blackboard itself does not crash from concurrent
   writes, having two behaviors write to the same key without
   coordination creates a logical race condition. The value read
   by a third behavior depends on which writer was ticked last,
   leading to unpredictable results. Use namespaced keys or
   explicit design to ensure each Blackboard key has exactly one
   writer.


----


Essay Questions
===============

.. admonition:: Question 14
   :class: hint

   **Explain how a Parallel composite node works in ``py_trees``
   and give a concrete robotics example where you would use one.**
   Describe the difference between ``SuccessOnAll`` and
   ``SuccessOnOne`` policies.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A Parallel composite ticks all of its children on every tick,
     regardless of their return statuses. The ``policy`` parameter
     determines when the Parallel itself reports success.
   - ``SuccessOnAll`` returns ``SUCCESS`` only when every child
     returns ``SUCCESS``. Use this when multiple tasks must all
     complete (e.g., "navigate to goal AND monitor battery" --
     both must run to completion).
   - ``SuccessOnOne`` returns ``SUCCESS`` as soon as any child
     returns ``SUCCESS``. Use this when any one of several approaches
     is sufficient (e.g., "try visual localization OR try LIDAR
     localization").
   - A concrete example: monitoring sensors in parallel with
     navigation. A Parallel node with ``SuccessOnAll`` ticks both
     a sensor monitoring behavior and a navigation behavior. If the
     sensor monitor detects a critical failure, it returns ``FAILURE``,
     causing the Parallel (and thus navigation) to fail, triggering
     a safety response in a parent Fallback.


.. admonition:: Question 15
   :class: hint

   **Describe the role of the Blackboard in a behavior tree that
   integrates multiple ROS 2 subsystems.** How does data flow from
   a ROS 2 topic subscription through the Blackboard to an action
   behavior?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The Blackboard acts as the central data bus in an integrated
     system. It decouples data producers from data consumers within
     the tree.
   - Data flow example: a ``ToBlackboard`` subscriber behavior
     receives ``LaserScan`` messages from the ``/scan`` topic and
     writes the closest obstacle distance to the Blackboard key
     ``/sensors/min_distance``. A condition behavior reads this key
     and returns ``SUCCESS`` if the path is clear. An action behavior
     reads the key to adjust its velocity command.
   - This pattern means behaviors only depend on Blackboard keys,
     not on specific topics or other behaviors. A behavior can be
     tested in isolation by manually setting Blackboard values.
   - Namespaces (e.g., ``/sensors/``, ``/navigation/``) organize
     keys by subsystem and prevent accidental collisions.


.. admonition:: Question 16
   :class: hint

   **You are designing a behavior tree for a mobile robot that must
   patrol a set of waypoints, avoid obstacles, and return to a
   charging station when the battery is low.** Sketch the high-level
   tree structure (in text form) and explain why you chose each
   composite type (Sequence, Fallback, Parallel) at each level.

   *(4-6 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   A reasonable tree structure:

   .. code-block:: text

      [Fallback: Root]
        -> [Sequence: EmergencyStop]
        |    -> CheckEStop
        |    -> HaltRobot
        |
        -> [Sequence: LowBattery]
        |    -> CheckBatteryLow (Inverter on CheckBatteryOK)
        |    -> NavigateToCharger
        |    -> Dock
        |
        -> [Sequence: Patrol]
             -> [Parallel: PatrolWithMonitoring]
                  -> [Sequence: Navigate]
                  |    -> GetNextWaypoint
                  |    -> NavigateToWaypoint
                  -> MonitorObstacles

   - The **Root Fallback** ensures priority ordering: emergency stop
     is checked first, then battery, then normal patrol. Because it
     is a Fallback, the first child that succeeds (or is running)
     takes precedence.
   - Each priority level uses a **Sequence** because all steps must
     succeed in order (check condition, then act).
   - The patrol uses a **Parallel** to monitor obstacles while
     navigating. If the obstacle monitor fails (obstacle detected),
     the Parallel fails, which causes the patrol Sequence to fail,
     returning control to the Root Fallback where obstacle avoidance
     can be handled.
   - Using ``memory=False`` on the Root Fallback ensures higher-
     priority conditions (emergency, battery) are re-evaluated on
     every tick, even if the patrol is currently running.
