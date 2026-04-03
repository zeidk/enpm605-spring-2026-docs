====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 10: Parameters, Custom
Interfaces, Services, and Actions. Topics include parameter declaration
and callbacks, YAML parameter files, custom ``.msg``/``.srv``/``.action``
definitions, service server/client patterns (synchronous vs.
asynchronous), action server/client patterns with feedback and
cancellation, and choosing the right communication mechanism.

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

   What must you do before calling ``self.get_parameter("speed")`` in a
   ROS 2 Python node?

   A. Import ``ParameterDescriptor`` from ``rcl_interfaces.msg``.

   B. Call ``self.declare_parameter("speed", <default>)`` to register
      the parameter.

   C. Start the node with ``--ros-args --params-file``.

   D. Create a service client to the parameter server.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``self.declare_parameter("speed", <default>)``.

   ROS 2 requires parameters to be declared before they can be read.
   Calling ``get_parameter()`` on an undeclared parameter raises
   ``ParameterNotDeclaredException``. The declaration registers the
   parameter name, default value, and type on the node. Importing
   ``ParameterDescriptor`` is optional and only needed for adding
   metadata. Starting with ``--params-file`` provides values but does
   not replace declaration.


.. admonition:: Question 2
   :class: hint

   In a YAML parameter file, what is the correct key under a node name
   to specify its parameters?

   A. ``parameters:``

   B. ``ros_parameters:``

   C. ``ros__parameters:``

   D. ``node_parameters:``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``ros__parameters:`` (with double underscores).

   The double-underscore convention is required by the ROS 2 parameter
   loading system. Using a single underscore or any other key name will
   cause the parameters to be silently ignored. The top-level key must
   match the fully qualified node name (e.g., ``/controller``).


.. admonition:: Question 3
   :class: hint

   Why must custom interface packages use ``ament_cmake`` instead of
   ``ament_python``?

   A. Python does not support message serialization.

   B. The ``rosidl`` code generators require CMake build infrastructure
      to produce language-specific bindings.

   C. Custom interfaces can only be used in C++ nodes.

   D. ``ament_python`` does not support ``package.xml``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The ``rosidl`` code generators require CMake.

   The ROS 2 interface generation pipeline (``rosidl``) compiles
   ``.msg``, ``.srv``, and ``.action`` files into Python classes and
   C++ headers using CMake macros (``rosidl_generate_interfaces``).
   This is a build-time requirement of the generator toolchain, not a
   limitation of Python itself. The generated Python classes can be
   imported and used in any ``ament_python`` package.


.. admonition:: Question 4
   :class: hint

   What separates the request and response sections in a ``.srv`` file?

   A. A blank line.

   B. The keyword ``response:``.

   C. Three dashes: ``---``

   D. The keyword ``return``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Three dashes: ``---``.

   The ``---`` separator is used in both ``.srv`` files (separating
   request from response) and ``.action`` files (separating goal,
   result, and feedback). This is a convention inherited from ROS 1
   and enforced by the ``rosidl`` parser.


.. admonition:: Question 5
   :class: hint

   What happens if you call ``self._client.call(request)``
   (synchronous) from the main executor thread in a single-threaded
   executor?

   A. The call succeeds but takes longer than usual.

   B. A ``TimeoutError`` is raised after 5 seconds.

   C. A **deadlock** occurs because the blocked thread cannot process
      the response callback.

   D. The executor automatically switches to multi-threaded mode.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- A deadlock occurs.

   The synchronous ``call()`` method blocks the calling thread until
   the response arrives. In a single-threaded executor, this is the
   same thread responsible for processing callbacks, including the
   response from the service server. Since the thread is blocked
   waiting for a response it can never process, the node hangs
   indefinitely. This is why ``call_async()`` is the recommended
   pattern.


.. admonition:: Question 6
   :class: hint

   In an action definition, how many sections are separated by ``---``?

   A. 2 -- request and response.

   B. 3 -- goal, result, and feedback.

   C. 3 -- goal, feedback, and status.

   D. 4 -- goal, acceptance, result, and feedback.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- 3 sections: goal, result, and feedback.

   An ``.action`` file is divided into three sections by two ``---``
   separators. The first section defines the goal (sent by the client),
   the second defines the result (returned when the action completes),
   and the third defines the feedback (published periodically during
   execution). This three-part structure distinguishes actions from
   services, which have only two sections.


.. admonition:: Question 7
   :class: hint

   Which method on a ``GoalHandle`` does the action server call to
   indicate the goal completed successfully?

   A. ``goal_handle.complete()``

   B. ``goal_handle.succeed()``

   C. ``goal_handle.finish(success=True)``

   D. ``goal_handle.set_result(result)``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``goal_handle.succeed()``.

   The ``GoalHandle`` provides terminal state methods: ``succeed()``,
   ``canceled()``, and ``abort()``. Calling ``succeed()`` sets the goal
   status to ``STATUS_SUCCEEDED`` before the execute callback returns
   the result object. The client receives this status along with the
   result when it calls ``get_result_async()``.


.. admonition:: Question 8
   :class: hint

   A parameter callback returns
   ``SetParametersResult(successful=False, reason="...")``. What
   happens?

   A. The parameter is set anyway but a warning is logged.

   B. The parameter change is rejected and the previous value is
      retained.

   C. The node shuts down with an error.

   D. The parameter is set to its default value.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The parameter change is rejected.

   When a parameter callback returns ``successful=False``, the
   parameter service returns an error to the caller (CLI, launch file,
   or another node) and the parameter retains its previous value. The
   ``reason`` string is included in the error response to explain why
   the change was rejected. This mechanism allows nodes to validate
   parameter changes at runtime.


----


True/False
==========

.. admonition:: Question 9
   :class: hint

   **True or False:** Parameters in ROS 2 are stored on a central
   parameter server shared by all nodes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Parameters are **node-local** in ROS 2. Each node maintains its own
   parameter store and exposes it through automatically created
   parameter services (``get_parameters``, ``set_parameters``, etc.).
   There is no central parameter server as in ROS 1. Two nodes can have
   parameters with the same name but completely independent values.


.. admonition:: Question 10
   :class: hint

   **True or False:** A ``.msg`` file can reference message types from
   other packages (e.g., ``std_msgs/Header``).

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Custom message definitions can include fields of any type from any
   package listed as a dependency in ``package.xml`` and passed to the
   ``DEPENDENCIES`` argument of ``rosidl_generate_interfaces`` in
   ``CMakeLists.txt``. ``std_msgs/Header`` and ``geometry_msgs/Pose``
   are common examples.


.. admonition:: Question 11
   :class: hint

   **True or False:** Action cancellation in ROS 2 is immediate -- as
   soon as the client calls ``cancel_goal_async()``, the server stops
   executing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Action cancellation is **cooperative**. The client sends a cancel
   request, and the server's ``cancel_callback`` decides whether to
   accept it. Even after acceptance, the execute callback must
   explicitly check ``goal_handle.is_cancel_requested`` and call
   ``goal_handle.canceled()`` to acknowledge the cancellation. The
   server is free to finish a critical operation before stopping.


.. admonition:: Question 12
   :class: hint

   **True or False:** ``ros2 param dump /node_name`` outputs YAML that
   can be directly reloaded with ``--params-file``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``ros2 param dump`` generates a YAML file in the correct format
   (node name as the top-level key, ``ros__parameters`` as the
   sub-key). This output can be saved to a file and loaded with
   ``--ros-args --params-file <file>``, making it a convenient way to
   snapshot and restore a node's configuration.


.. admonition:: Question 13
   :class: hint

   **True or False:** A service client using ``call_async()`` will
   deadlock in a single-threaded executor.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``call_async()`` is the asynchronous pattern that returns a
   ``Future`` immediately without blocking the executor thread. The
   executor remains free to process other callbacks, including the
   response when it arrives. It is the synchronous ``call()`` method
   that causes a deadlock in a single-threaded executor by blocking the
   thread that needs to process the response.


----


Essay Questions
===============

.. admonition:: Question 14
   :class: hint

   **Explain the difference between a ROS 2 service and a ROS 2
   action.** When would you choose one over the other? Give a concrete
   robotics example for each.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A **service** implements a synchronous request/response pattern
     suitable for short-duration operations. The client sends a request
     and blocks (or waits asynchronously) for a single response. There
     is no mechanism for progress updates or cancellation. Example:
     requesting a robot to compute inverse kinematics for a target pose.
   - An **action** extends the service model with feedback and
     cancellation for long-running tasks. The server publishes periodic
     feedback while executing and the client can cancel the goal at any
     time. Example: commanding a mobile robot to navigate to a
     waypoint, receiving distance-remaining updates, and canceling if
     an obstacle is detected.
   - Choose a service when the operation completes quickly (under ~1 s)
     and no progress tracking is needed. Choose an action when the
     operation takes noticeable time and the user or system needs
     visibility into progress or the ability to abort.


.. admonition:: Question 15
   :class: hint

   **Describe the purpose of a parameter callback in ROS 2.** What
   happens if the callback returns ``successful=False``? Why is this
   mechanism useful for robotic systems?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A parameter callback is invoked whenever a parameter value is
     changed at runtime (via CLI, service call, launch file, or another
     node). It receives the list of pending parameter changes and can
     inspect each one.
   - If the callback returns ``SetParametersResult(successful=False)``,
     the change is rejected and the parameter retains its previous
     value. The ``reason`` string is returned to the caller to explain
     the rejection.
   - This is critical for safety in robotic systems: a controller node
     can reject a proportional gain that is negative or dangerously
     high, preventing unstable behavior without requiring a node
     restart. It also enables logging all parameter changes for
     debugging and audit purposes.


.. admonition:: Question 16
   :class: hint

   **Why is it recommended to use ``call_async()`` instead of
   ``call()`` for ROS 2 service clients?** Explain the deadlock
   scenario that can occur with ``call()`` and describe one strategy
   to avoid it if synchronous behavior is required.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``call()`` blocks the calling thread until the response arrives.
     In a ``SingleThreadedExecutor``, this blocks the only thread
     responsible for processing callbacks. Since the response callback
     cannot be processed by the blocked thread, the node deadlocks
     permanently.
   - ``call_async()`` returns a ``Future`` immediately and allows the
     executor to continue processing other callbacks, including the
     eventual response. This is safe in all executor configurations.
   - If synchronous behavior is truly required, one strategy is to call
     the service from a callback assigned to a
     ``ReentrantCallbackGroup`` inside a ``MultiThreadedExecutor``. This
     ensures the blocking call runs on one thread while the response is
     processed on another. However, ``call_async()`` with
     ``add_done_callback()`` is almost always the cleaner solution.
