====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 9: Launch Files,
Parameters, and Executors, including Python launch file structure,
advanced launch features (includes, conditionals, grouping, arguments),
the ROS 2 parameter lifecycle (declaration, retrieval, setting, and
callbacks), single-threaded and multi-threaded executors, and callback
groups (mutually exclusive and reentrant). The GIL and its implications
for Python parallelism are also covered.

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

   What is the name of the function that **must** be defined in a
   Python ROS 2 launch file?

   A. ``main()``

   B. ``launch()``

   C. ``generate_launch_description()``

   D. ``create_launch_description()``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``generate_launch_description()``.

   ROS 2 discovers a Python launch file by calling the
   ``generate_launch_description()`` function. The function must return
   a ``LaunchDescription`` object containing all the actions (nodes,
   arguments, includes, etc.) to execute. If this function is absent or
   misnamed, ``ros2 launch`` will raise an error.


.. admonition:: Question 2
   :class: hint

   Which class is used to locate the installed share directory of a
   ROS 2 package inside a launch file at runtime?

   A. ``PathJoinSubstitution``

   B. ``FindPackageShare``

   C. ``IncludeLaunchDescription``

   D. ``PackageShareDirectory``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``FindPackageShare``.

   ``FindPackageShare("pkg_name")`` resolves to the share directory of
   a package in the install tree at launch time, without hardcoding
   absolute paths. It is typically combined with
   ``PathJoinSubstitution`` to construct the full path to a file inside
   that directory.


.. admonition:: Question 3
   :class: hint

   A parameter is declared with ``self.declare_parameter("rate", 10)``
   but no descriptor. What is the inferred parameter type?

   A. ``double``

   B. ``string``

   C. ``integer``

   D. ``byte[]``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``integer``.

   ROS 2 infers the parameter type from the Python type of the default
   value. The literal ``10`` is a Python ``int``, so the parameter type
   is ``integer``. If the default value were ``10.0``, the type would
   be ``double``. Use ``ParameterDescriptor`` to add constraints and
   documentation.


.. admonition:: Question 4
   :class: hint

   After calling ``ros2 param set /camera_demo camera_name 'new_name'``,
   a node still logs the old name. What is the most likely cause?

   A. The parameter file overrides the CLI value.

   B. The node did not register an on-set-parameters callback and
      therefore never updated its stored attribute.

   C. ``ros2 param set`` only works with integer and double types.

   D. The node must be rebuilt before parameter changes take effect.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The node did not register an on-set-parameters callback.

   ``ros2 param set`` updates the parameter value in the ROS 2 parameter
   server for that node. However, the node's Python attribute
   (``self._camera_name``) is only set during initialization. Without a
   registered callback via ``add_on_set_parameters_callback()``, the
   attribute is never updated after startup.


.. admonition:: Question 5
   :class: hint

   What is the correct accessor to retrieve an integer parameter value
   from a ``Parameter`` object returned by ``get_parameter()``?

   A. ``.value``

   B. ``.get_parameter_value().integer_value``

   C. ``.data``

   D. ``.get_value().as_int()``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``.get_parameter_value().integer_value``.

   ``get_parameter("name")`` returns a ``Parameter`` object. Calling
   ``.get_parameter_value()`` returns a ``ParameterValue`` message.
   Access the appropriate typed field: ``.integer_value``,
   ``.double_value``, ``.string_value``, ``.bool_value``, etc. The
   field must match the declared parameter type.


.. admonition:: Question 6
   :class: hint

   Which executor type is implicitly created by ``rclpy.spin(node)``?

   A. ``MultiThreadedExecutor``

   B. ``ReentrantExecutor``

   C. ``SingleThreadedExecutor``

   D. ``DefaultExecutor``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``SingleThreadedExecutor``.

   ``rclpy.spin(node)`` is a convenience wrapper. Internally it creates
   a ``SingleThreadedExecutor``, adds the node to it, and calls
   ``executor.spin()``. It is identical in behavior to creating the
   executor explicitly. The explicit form is preferred when managing
   multiple nodes or switching executor types.


.. admonition:: Question 7
   :class: hint

   Node A has three timers all assigned to the same
   ``MutuallyExclusiveCallbackGroup`` and runs under a
   ``MultiThreadedExecutor(num_threads=8)``. How many callbacks can
   execute simultaneously?

   A. Up to 8 -- one per thread.

   B. Up to 3 -- one per timer.

   C. Exactly 1 -- the mutex group serializes all three regardless of
      thread count.

   D. Exactly 2 -- threads are shared between groups.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Exactly 1.

   A ``MutuallyExclusiveCallbackGroup`` enforces serialization among
   all callbacks registered to it. The executor withholds a queued
   callback from the group until the currently running one returns.
   Thread count has no effect on this constraint -- the extra 7 threads
   remain idle for this group.


.. admonition:: Question 8
   :class: hint

   A ``ReentrantCallbackGroup`` callback has a period of 200 ms and an
   execution time of 350 ms. What happens at t=200 ms?

   A. The executor skips the second firing because the first has not
      finished.

   B. The executor waits until the first instance finishes (at 350 ms),
      then starts the second.

   C. The executor starts a second instance on a free thread
      regardless of the first instance still running.

   D. The node raises a ``RuntimeError`` due to overlapping callbacks.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The executor starts a second instance on a free thread.

   A ``ReentrantCallbackGroup`` places no serialization constraint.
   When a timer fires, the executor assigns it to any available thread
   immediately, even if a previous instance is still executing. This is
   the defining behavior of the reentrant group -- multiple instances
   can run concurrently. Use ``MutuallyExclusiveCallbackGroup`` if
   overlapping instances are undesirable.


.. admonition:: Question 9
   :class: hint

   Why does adding more threads to a ``MultiThreadedExecutor`` via
   ``num_threads`` not increase parallelism for pure Python callbacks?

   A. ROS 2 only allows one thread per node by design.

   B. CPython's GIL allows only one thread to execute Python bytecode
      at a time, regardless of thread count.

   C. ``MultiThreadedExecutor`` creates threads but never starts them.

   D. Python threads cannot be scheduled on separate CPU cores.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- CPython's Global Interpreter Lock (GIL).

   The GIL is a mutex inside the CPython interpreter that allows only
   one thread to run Python bytecode at any instant. Even with 16
   threads on a 16-core machine, pure Python code is serialized back
   onto one core. True parallelism is only achieved when a callback
   releases the GIL -- during ``time.sleep()``, I/O, or calls into
   native libraries such as NumPy or OpenCV.


.. admonition:: Question 10
   :class: hint

   You must modify a timer's firing period at runtime after a parameter
   change. Which approach is correct?

   A. Call ``self._timer.set_period(new_period)`` directly.

   B. Cancel the existing timer and create a new one with the updated
      period.

   C. Change the parameter value; the timer period updates automatically.

   D. Restart the node with the new parameter value.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Cancel the existing timer and create a new one.

   ROS 2 timers do not expose a ``set_period()`` method. The correct
   pattern is to cancel the existing timer with
   ``self._timer.cancel()`` and then call
   ``self.create_timer(new_period, callback)`` to create a replacement.
   This must be done inside the on-set-parameters callback so it
   triggers automatically when the parameter is updated.


----


True/False
==========

.. admonition:: Question 11
   :class: hint

   **True or False:** The ``--symlink-install`` flag means you never
   need to rebuild after adding a new launch file to an existing
   package.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``--symlink-install`` creates symlinks for Python source files and
   data files that are already registered in ``setup.py``. If you add a
   new ``glob()`` pattern or data directory entry to ``setup.py``,
   you must run ``colcon build`` again to register the new symlinks.
   Once registered, edits to the launch file itself take effect without
   rebuilding.


.. admonition:: Question 12
   :class: hint

   **True or False:** A parameter declared in a node's ``__init__``
   without a ``ParameterDescriptor`` cannot have constraints applied
   to it later.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Constraints and metadata are attached to a parameter at declaration
   time via ``ParameterDescriptor``. Once a parameter is declared
   without a descriptor (or with an empty descriptor), its constraints
   cannot be changed at runtime. Plan your parameter metadata during
   node design.


.. admonition:: Question 13
   :class: hint

   **True or False:** A YAML parameter file can configure parameters
   for multiple nodes in a single file.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A YAML parameter file maps node names to their ``ros__parameters``
   blocks at the top level. Multiple node blocks can appear in the same
   file. Each ``Node`` action in the launch file that loads the file
   will only apply the parameters belonging to its own node name.


.. admonition:: Question 14
   :class: hint

   **True or False:** A ``SingleThreadedExecutor`` can manage callbacks
   from more than one node simultaneously.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   An executor is not limited to a single node. You can add multiple
   nodes to the same ``SingleThreadedExecutor`` via
   ``executor.add_node()``. All callbacks from all nodes are queued and
   processed sequentially on the single thread.


.. admonition:: Question 15
   :class: hint

   **True or False:** The Python GIL is released during
   ``time.sleep()``, enabling true parallelism between two threads
   sleeping simultaneously.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``time.sleep()`` is a system call that suspends the calling thread
   and releases the GIL for the duration. While one thread sleeps,
   another thread can execute Python bytecode on the same core -- or
   run simultaneously on a separate core. This is why the timelines for
   reentrant callbacks in the demos show genuine overlap during sleep
   calls.


.. admonition:: Question 16
   :class: hint

   **True or False:** A ``ReentrantCallbackGroup`` is always safer than
   a ``MutuallyExclusiveCallbackGroup`` because it avoids blocking.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Safety depends on whether callbacks share mutable state.
   ``ReentrantCallbackGroup`` allows multiple concurrent instances,
   which can cause race conditions if any shared attribute is read and
   written without a lock. ``MutuallyExclusiveCallbackGroup`` prevents
   concurrent access by serializing all callbacks in the group. Neither
   is universally safer -- choose based on whether shared state is
   involved.


.. admonition:: Question 17
   :class: hint

   **True or False:** Passing ``condition=IfCondition(...)`` to a
   ``Node`` action means the node is started but immediately paused if
   the condition is false.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``IfCondition`` prevents the node from being launched at all. If the
   condition evaluates to false at launch time, the ``Node`` action is
   skipped entirely -- no process is created. It is not started and
   then paused; it simply does not start.


.. admonition:: Question 18
   :class: hint

   **True or False:** ``ros2 param set`` permanently changes the
   parameter default value so it persists after the node is restarted.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``ros2 param set`` updates the in-memory parameter value for a
   running node. When the node is stopped and restarted, it reverts to
   the default declared in the source code (or the value from a YAML
   file or CLI argument if provided). To make changes permanent,
   update the YAML file or the default value in the code.


.. admonition:: Question 19
   :class: hint

   **True or False:** ``GroupAction`` in a launch file allows applying
   a single ``IfCondition`` to an entire set of nodes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``GroupAction`` accepts a ``condition`` argument that applies to all
   actions in the group. If the condition is false, none of the nodes
   in the group are started. This is cleaner than adding the same
   condition to each individual ``Node`` action.


.. admonition:: Question 20
   :class: hint

   **True or False:** A ``MutuallyExclusiveCallbackGroup`` with
   ``MultiThreadedExecutor(num_threads=4)`` executes callbacks faster
   than the same group with ``num_threads=1``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The mutex constraint serializes all callbacks in the group
   regardless of how many threads are available. Extra threads remain
   idle for that group. Callback execution timing is identical for any
   ``num_threads >= 1`` when only a single mutex group is involved.
   More threads only provide benefit when multiple groups or nodes can
   run concurrently.


----


Essay Questions
===============

.. admonition:: Question 21
   :class: hint

   **Explain the ROS 2 parameter lifecycle.** Starting from declaration,
   describe each stage a parameter goes through and what can happen at
   each stage.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **Declaration**: the node calls ``declare_parameter()`` in
     ``__init__``, establishing the parameter name, type (inferred
     from the default value), default value, and optional descriptor.
     Accessing an undeclared parameter raises an error.
   - **Retrieval**: the node calls ``get_parameter().get_parameter_value()``
     to read the current value into a Python attribute. This is
     typically done once during initialization.
   - **Setting**: the value can be overridden via the CLI (``--ros-args
     -p``), a launch file, a YAML file, programmatically with
     ``set_parameters()``, or at runtime with ``ros2 param set``.
   - **Callback notification**: if ``add_on_set_parameters_callback()``
     is registered, the callback fires whenever a set operation is
     attempted. The callback validates the new values, updates stored
     attributes, and returns ``SetParametersResult(successful=...)``
     to accept or reject the change.


.. admonition:: Question 22
   :class: hint

   **Describe the difference between a single-threaded executor and a
   multi-threaded executor in ROS 2.** When would you choose one over
   the other?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A ``SingleThreadedExecutor`` processes all callbacks sequentially
     on one OS thread. No two callbacks ever overlap. It is simple,
     race-condition-free by construction, and appropriate for
     lightweight nodes or when deterministic execution order is
     required.
   - A ``MultiThreadedExecutor`` maintains a pool of OS threads and
     can dispatch multiple callbacks simultaneously, subject to the
     constraints of their callback groups. It is appropriate when
     independent tasks need to run concurrently to reduce latency.
   - Choice depends on whether callbacks share state (favor mutex
     groups or single-threaded), whether tasks are truly independent
     (favor reentrant), and the nature of the callbacks (I/O-bound
     tasks benefit most from multi-threading due to GIL release).


.. admonition:: Question 23
   :class: hint

   **Explain what the Python GIL is and how it limits parallelism in
   ROS 2 Python nodes.** Under what conditions can true parallelism be
   achieved?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The Global Interpreter Lock (GIL) is a mutex inside CPython that
     allows only one thread to execute Python bytecode at a time,
     regardless of how many CPU cores are available. It exists to
     protect CPython's internal memory management from concurrent
     access.
   - In ROS 2 Python nodes, a ``MultiThreadedExecutor`` with a
     ``ReentrantCallbackGroup`` allows multiple callback instances to
     be in progress simultaneously, but they still take turns on one
     core for pure Python code.
   - True parallelism is achieved when a callback releases the GIL:
     during ``time.sleep()``, blocking I/O, or calls into native
     extension libraries (NumPy, OpenCV, sensor drivers). AV
     perception callbacks are a practical example where the GIL is
     released during matrix operations.


.. admonition:: Question 24
   :class: hint

   **Compare ``MutuallyExclusiveCallbackGroup`` and
   ``ReentrantCallbackGroup``.** Give a concrete robotic example where
   each would be the appropriate choice.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``MutuallyExclusiveCallbackGroup`` serializes all callbacks in the
     group: only one can execute at a time, even in a multi-threaded
     executor. Example: a motor controller node where a timer callback
     and a subscriber callback both write to ``self._target_velocity``
     -- serialization prevents the race condition without an explicit
     lock.
   - ``ReentrantCallbackGroup`` allows multiple concurrent instances.
     Example: a logging node that subscribes to five different sensor
     topics and writes each message to an independent log file. Each
     callback is self-contained, does not share state, and benefits
     from concurrent execution when all five messages arrive
     simultaneously.
   - Start with ``MutuallyExclusive`` and switch to ``Reentrant`` only
     after confirming callbacks are stateless or properly locked.
