====================================================
Executors
====================================================

Why Executors Matter
--------------------

Robotic systems require concurrent tasks and coordination:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🔄 Concurrent Tasks
        :class-card: sd-border-primary
        
        - Process sensor data (cameras, lidar, IMU)
        - Update control commands at different rates
        - Monitor system health and safety
        - Handle user commands
        - Log data for analysis

    .. grid-item-card:: 🧩 Coordination Challenges
        :class-card: sd-border-warning
        
        - How do we handle multiple callbacks?
        - What if one callback blocks others?
        - Can we process sensors in parallel?
        - How do we prioritize critical tasks?
        - When should we use threads vs. sequential processing?

.. card::
    :class-card: sd-border-info

    **Executors** provide tools for managing concurrent tasks and their coordination.

Threads
-------

.. card::
    :class-card: sd-border-secondary sd-shadow-sm

    **Definition**
    
    A **thread of execution** is the smallest unit of instructions that can be scheduled and run independently by the operating system.

- A process may contain one or many threads.
- Each thread runs a sequence of instructions in parallel with others.
- Threads share the same memory space, which enables fast data access but requires synchronization to avoid conflicts.
- Threads allow programs to perform multiple tasks simultaneously, such as handling sensor input, control loops, and communication.

.. tip::
    **Example:** A robot may use separate threads for LiDAR processing, camera processing, and odometry updates (running concurrently but within the same process).

Single-Threaded Executors
-------------------------

.. card::
    :class-card: sd-border-info

    **Definition**
    
    A **single-threaded executor** ensures that all callbacks are executed sequentially in a single thread.

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: ✅ Benefits
        :class-card: sd-border-success
        
        - One callback at a time **in the order they are scheduled**
        - **No concurrency** issues
        - Easy to reason about and debug
        - Suitable for low computational demands
        - Deterministic execution

    .. grid-item-card:: ⚠️ Limitations
        :class-card: sd-border-warning
        
        - Not ideal for performance with many independent tasks
        - A slow callback blocks all others
        - May bottleneck under heavy load

rclcpp::spin() vs SingleThreadedExecutor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

They are essentially the same! ``rclcpp::spin(node)`` is a convenience wrapper.

.. tab-set::

    .. tab-item:: Using rclcpp::spin()

        .. code-block:: cpp
           :linenos:

           int main(int argc, char** argv) {
               rclcpp::init(argc, argv);
               
               auto node = std::make_shared<MyFirstNode>();
               
               // Simple spinning
               rclcpp::spin(node);
               rclcpp::shutdown();
           }

        - Creates a ``SingleThreadedExecutor``
        - Adds your node to it
        - Calls ``executor.spin()``
        - Blocks until shutdown

    .. tab-item:: Using Executor Explicitly

        .. code-block:: cpp
           :linenos:

           int main(int argc, char** argv) {
               rclcpp::init(argc, argv);
               
               auto node1 = std::make_shared<MyFirstNode>();
               auto node2 = std::make_shared<MySecondNode>();
               
               // Explicit executor
               rclcpp::executors::SingleThreadedExecutor executor;
               executor.add_node(node1);
               executor.add_node(node2);
               executor.spin();
               
               rclcpp::shutdown();
           }

        **More control over:**
        
        - Multiple nodes in one executor
        - Switching executor types easily
        - Custom spin behaviors

Multi-Threaded Executors
------------------------

.. card::
    :class-card: sd-border-info

    **Definition**
    
    A **multi-threaded executor** is a mechanism for managing and executing callbacks across multiple threads, allowing for concurrent processing of tasks.

Key Characteristics
^^^^^^^^^^^^^^^^^^^

- **Thread pool**: Creates a pool of threads (configurable). Each thread can independently process callbacks.
- **Callback scheduling**: When events occur (message arrival, timer firing, service request), the executor assigns pending callbacks to available threads. Multiple callbacks can run concurrently.
- **Spinning**: Calling ``executor.spin()`` starts an event loop that continuously checks for and dispatches work to the thread pool.

Benefits
^^^^^^^^

.. grid:: 1 3 3 3
    :gutter: 2

    .. grid-item-card:: ⚡ Performance
        :class-card: sd-border-success
        
        Ideal for applications with many independent tasks. Concurrent execution reduces latency and improves throughput.

    .. grid-item-card:: 📈 Scalability
        :class-card: sd-border-success
        
        Handles multiple nodes or high-frequency callbacks better than single-threaded executors.

    .. grid-item-card:: 🚨 Responsiveness
        :class-card: sd-border-success
        
        Critical tasks (like emergency stop) won't be delayed by slower, less urgent ones.

Challenges
^^^^^^^^^^

.. card::
    :class-card: sd-border-danger sd-border-3

    **Race Conditions**
    
    If callbacks access shared resources (e.g., a class attribute), you will need synchronization mechanisms like locks to prevent data corruption. Single-threaded executors avoid this issue entirely.

.. warning::
    Managing multiple threads introduces complexity and CPU overhead. If your application is lightweight, the extra threads might not be worth it.

Callback Groups
---------------

.. card::
    :class-card: sd-border-primary sd-shadow-sm

    **Definition**
    
    A **callback group** is a container within a node that holds callbacks (e.g., for subscriptions, timers, or services). Each group defines how its callbacks are handled in terms of execution and threading.

- By default, all callbacks belong to the node's implicit callback group (``rclcpp::CallbackGroupType::MutuallyExclusive``).
- You can create explicit callback groups to customize execution behavior.
- **Two types exist**: ``MutuallyExclusive`` and ``Reentrant``.
- The executor type determines whether callback groups can actually leverage concurrency.

Mutually Exclusive Callback Group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
    :class-card: sd-border-warning

    **Definition**
    
    Callbacks within a **mutually exclusive callback group** cannot run concurrently, even in a multi-threaded executor. They are executed sequentially, one after another.
    
    **Use case**: When callbacks share resources (e.g., modifying the same variable) and you want to avoid race conditions without explicit locks.

Reentrant Callback Group
^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
    :class-card: sd-border-success

    **Definition**
    
    Callbacks within a **reentrant callback group** can run concurrently with each other (and with callbacks in other reentrant groups), assuming the executor supports multiple threads.
    
    **Use case**: Independent tasks that don't interfere with each other, maximizing concurrency.

Callback Group Overview
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - Group Type
     - Behavior
     - Use Case
   * - ``MutuallyExclusive``
     - Sequential execution within group
     - Shared resources, avoid race conditions
   * - ``Reentrant``
     - Concurrent execution allowed
     - Independent tasks, maximize parallelism

Demonstrations
--------------

Two Mutex Callback Groups
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   mutex_group1_:
     - timer1_callback
     - timer2_callback

   mutex_group2_:
     - timer3_callback
     - timer4_callback

.. card::
    :class-card: sd-border-secondary

    .. code-block:: bash

       ros2 run executors_demo two_mutex

One Mutex + One Reentrant
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   mutex_group_:
     - timer3_callback
     - timer4_callback

   reentrant_group_:
     - timer1_callback
     - timer2_callback

.. card::
    :class-card: sd-border-secondary

    .. code-block:: bash

       ros2 run executors_demo mutex_reentrant