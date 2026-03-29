====================================================
Exercises
====================================================

This page contains two take-home exercises that reinforce the concepts
from Lecture 9. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your
``~/enpm605_ws/src/executor_demo/`` workspace package.


.. dropdown:: Exercise 1 -- Mutex vs Single-Threaded Comparison
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Observe the behavior difference between a
    ``SingleThreadedExecutor`` and a ``MultiThreadedExecutor`` with a
    ``MutuallyExclusiveCallbackGroup`` containing a slow callback.


    .. raw:: html

       <hr>


    **Specification**

    Create the file ``executors_demo/slow_callback_demo.py`` that
    implements the following.

    1. **``SlowCallbackDemo(Node)``** class:

       - ``__init__(self)``: calls ``super().__init__("slow_cb_demo")``,
         creates a ``MutuallyExclusiveCallbackGroup`` stored as
         ``_group``, and creates three timers:

         - ``_fast_timer``: 2 Hz, 50 ms execution (simulated with
           ``time.sleep(0.05)``), assigned to ``_group``.
         - ``_slow_timer``: 1 Hz, 600 ms execution
           (``time.sleep(0.60)``), assigned to ``_group``.
         - ``_monitor_timer``: 5 Hz, negligible execution, assigned to
           ``_group``. Logs ``"monitor tick"`` without sleeping.

    2. Three callbacks each logging their name and the current wall
       time at entry and exit.

    3. **Two entry points** in ``scripts/``:

       - ``run_single_threaded.py``: uses ``rclpy.spin(node)``
         (implicitly single-threaded).
       - ``run_multi_threaded.py``: uses
         ``MultiThreadedExecutor(num_threads=4)``.

    4. Register both in ``setup.py``.

    **Observation questions (answer as comments at the top of each
    entry point file)**

    - In the single-threaded case, what happens to ``_fast_timer`` and
      ``_monitor_timer`` while ``_slow_timer`` is executing?
    - In the multi-threaded case with a mutex group, is there any
      difference in behavior? Why or why not?

    **Verification**

    .. code-block:: console

       ros2 run executors_demo single_threaded_slow
       ros2 run executors_demo multi_threaded_slow


.. dropdown:: Exercise 2 -- Reentrant Pipeline
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build a node with two independent callback pipelines using a
    ``ReentrantCallbackGroup``, observe that they overlap correctly,
    and introduce a deliberate race condition to see what goes wrong.


    .. raw:: html

       <hr>


    **Specification**

    Create ``executors_demo/reentrant_pipeline.py``.

    1. **``ReentrantPipeline(Node)``** class with one
       ``ReentrantCallbackGroup``:

       - ``_camera_cb``: fires at 5 Hz, takes 80 ms
         (``time.sleep(0.08)``). Appends a timestamped entry to a
         shared list ``self._log``.
       - ``_lidar_cb``: fires at 5 Hz, takes 80 ms
         (``time.sleep(0.08)``). Appends a timestamped entry to the
         same ``self._log``.
       - ``_report_cb``: fires at 1 Hz, prints the length and last
         three entries of ``self._log``.

    2. Entry point ``scripts/run_reentrant_pipeline.py`` using
       ``MultiThreadedExecutor(num_threads=4)``.

    3. Register in ``setup.py``.

    **Part B -- Introduce and fix a race condition**

    Both ``_camera_cb`` and ``_lidar_cb`` append to the same list
    without a lock. Run the node for several seconds and note whether
    you ever observe a corrupted log (duplicated or missing entries).
    Then:

    - Protect ``self._log`` with a ``threading.Lock``.
    - Verify that the log is now consistent.

    **Written reflection (include as a comment block at the top of the
    file)**

    - Did you observe a race condition without the lock? Why is list
      ``append`` generally safe in CPython but not guaranteed across all
      Python implementations?
    - What would happen if you switched the group to
      ``MutuallyExclusiveCallbackGroup``? Would the race condition
      disappear? At what cost?
