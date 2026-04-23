====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 12: Namespaces,
Remapping, Lifecycle Nodes, and Behavior Trees. Topics include
namespace isolation, node/topic/parameter remapping, the lifecycle
state machine and its callbacks, behavior tree composites (Sequence,
Selector), decorators, conditions, actions, and the tick mechanism.

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

   A ROS 2 node publishes on the topic ``image_raw`` (relative name).
   You launch it with ``--ros-args -r __ns:=/front``. What is the
   fully-qualified topic name?

   A. ``/image_raw``

   B. ``/front/image_raw``

   C. ``/front/camera_node/image_raw``

   D. ``image_raw``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``/front/image_raw``.

   A namespace prefixes all **relative** names. Since ``image_raw``
   does not start with ``/``, the namespace ``/front`` is prepended.
   Absolute names (starting with ``/``) are not affected.


.. admonition:: Question 2
   :class: hint

   What is the correct order of transitions to bring a lifecycle node
   from Unconfigured to Active?

   A. ``activate`` then ``configure``

   B. ``configure`` then ``activate``

   C. ``shutdown`` then ``activate``

   D. ``configure`` then ``cleanup`` then ``activate``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``configure`` then ``activate``.

   The lifecycle state machine requires Unconfigured -> Inactive
   (via ``configure``) -> Active (via ``activate``). Skipping
   ``configure`` causes a transition failure.


.. admonition:: Question 3
   :class: hint

   In a behavior tree, what does a **Sequence** node do when one of
   its children returns FAILURE?

   A. It continues ticking the remaining children.

   B. It immediately returns FAILURE without ticking remaining children.

   C. It retries the failed child.

   D. It returns RUNNING.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It immediately returns FAILURE.

   A Sequence node (logical AND) fails as soon as any child fails.
   It does not tick the remaining children.


.. admonition:: Question 4
   :class: hint

   In ``py_trees``, what is the difference between a **Selector** and
   a **Sequence**?

   A. A Selector ticks children in reverse order.

   B. A Selector succeeds on the first child SUCCESS; a Sequence
      succeeds only if all children succeed.

   C. A Selector always returns RUNNING.

   D. There is no difference; they are aliases.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A Selector (Fallback) succeeds on the first SUCCESS
   (logical OR). A Sequence succeeds only if **all** children succeed
   (logical AND).


.. admonition:: Question 5
   :class: hint

   What does a ``py_trees.decorators.Timeout`` decorator do?

   A. It makes the child node tick faster.

   B. It returns FAILURE if the child is still RUNNING after a set
      duration.

   C. It retries the child on FAILURE.

   D. It converts SUCCESS to RUNNING.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Returns FAILURE if the child is still RUNNING after the
   configured duration. This is used to detect when a navigation or
   driving action is taking too long.


.. admonition:: Question 6
   :class: hint

   In a lifecycle node, which method should you use to create a
   publisher that respects the node's active/inactive state?

   A. ``self.create_publisher()``

   B. ``self.create_lifecycle_publisher()``

   C. ``self.create_timer()``

   D. ``rclpy.create_publisher()``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``create_lifecycle_publisher()``.

   A lifecycle publisher silently discards messages when the node is
   Inactive. It is automatically enabled by ``super().on_activate()``
   and disabled by ``super().on_deactivate()``.


.. admonition:: Question 7
   :class: hint

   What does ``memory=False`` mean on a ``py_trees`` Sequence?

   A. The Sequence forgets which child was running and re-evaluates
      all children from the beginning on every tick.

   B. The Sequence caches the last result and never re-ticks children.

   C. The Sequence uses less RAM.

   D. The Sequence does not store any internal state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- With ``memory=False``, the Sequence is **reactive**: it
   starts from the first child on every tick. This means condition
   nodes are re-checked each tick, allowing the tree to react
   immediately to changes (e.g., goal reached, battery low).


.. admonition:: Question 8
   :class: hint

   You run the same executable twice in the same namespace without
   remapping the node name. What happens?

   A. Both nodes run normally.

   B. The second node fails to start because the name is already taken.

   C. Both nodes share the same publishers and subscribers.

   D. ROS 2 automatically assigns unique names.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The second node fails because every node in a ROS 2 system
   must have a unique name. Use ``--ros-args -r __node:=new_name`` or
   the ``name`` argument in a launch file to resolve this.


----


True/False
==========

.. admonition:: Question 9
   :class: hint

   A namespace affects **absolute** topic names (those starting with
   ``/``).

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Namespaces only affect **relative** names. Absolute
   names bypass the namespace entirely.


.. admonition:: Question 10
   :class: hint

   A condition node in a behavior tree should never return RUNNING.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- Condition nodes must give an instantaneous yes/no
   answer: SUCCESS or FAILURE. Only action nodes return RUNNING.


.. admonition:: Question 11
   :class: hint

   Calling ``super().on_activate(state)`` is optional in a lifecycle
   node's ``on_activate`` callback.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- ``super().on_activate(state)`` enables the lifecycle
   publisher. Without it, any messages published by the node are
   silently dropped.


.. admonition:: Question 12
   :class: hint

   A ``py_trees`` Selector with ``memory=True`` always starts from the
   first child on every tick.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- With ``memory=True``, the Selector remembers which
   child was last ticked. If a child returned FAILURE, the Selector
   resumes from the **next** child on the following tick, rather than
   starting over.


.. admonition:: Question 13
   :class: hint

   In a lifecycle node, ``on_deactivate`` can return FAILURE to prevent
   the node from leaving the Active state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Deactivation must always succeed. There is no FAILURE
   path for ``on_deactivate``. The node will end up Inactive
   regardless of what the callback returns.


----


Essay Questions
===============

.. admonition:: Question 14
   :class: hint

   Explain the difference between a **namespace** and **remapping** in
   ROS 2. When would you use one over the other?

.. dropdown:: Answer
   :class-container: sd-border-success

   A namespace is a **bulk** operation that prepends a prefix to all
   relative names (topics, services, parameters) associated with a
   node. It is used to isolate multiple instances of the same node
   (e.g., three cameras). Remapping is a **surgical** operation that
   changes one specific name (e.g., redirecting ``image_raw`` to
   ``/sensors/front/image``). Use namespaces first for isolation, then
   remapping to fine-tune individual names that the namespace alone
   does not handle correctly.


.. admonition:: Question 15
   :class: hint

   In the ``bt_demo`` behavior tree, the root Sequence uses
   ``memory=False`` while the Selector (DriveOrRecover) uses
   ``memory=True``. Explain why each choice is appropriate.

.. dropdown:: Answer
   :class-container: sd-border-success

   The root Sequence uses ``memory=False`` so that the
   ``GoalNotReached?`` condition is re-evaluated on **every tick**.
   This makes the tree reactive: the moment the robot reaches the
   goal, the condition returns FAILURE and the Sequence stops
   immediately. The Selector uses ``memory=True`` so that once
   DriveForward times out (FAILURE), the Selector stays on the Spin
   recovery child rather than retrying DriveForward immediately on the
   next tick. Spin runs until it reaches the target yaw (SUCCESS),
   then the Selector resets and gives DriveForward a fresh attempt.


.. admonition:: Question 16
   :class: hint

   Describe the four primary states of a ROS 2 lifecycle node and
   explain why resources (publishers, timers) are created in
   ``on_configure`` rather than in ``__init__``.

.. dropdown:: Answer
   :class-container: sd-border-success

   The four states are: **Unconfigured** (exists but holds no
   resources), **Inactive** (resources allocated but not processing),
   **Active** (fully operational), and **Finalized** (cleaned up,
   no further transitions). Resources are created in ``on_configure``
   rather than ``__init__`` because the lifecycle model demands
   explicit control over when resources are allocated. This prevents
   publishers from being created before the system is ready (e.g.,
   before a dependent node has configured), and allows resources to
   be released via ``on_cleanup`` and re-created by calling
   ``configure`` again -- something that would not be possible if
   resources were allocated in the constructor.
