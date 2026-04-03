====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 11: Simulation with
Gazebo Harmonic and Mobile Robot Control, including the Gazebo
architecture, SDF files, ``ros_gz_bridge``, spawning models, TF2
coordinate frames, static and dynamic transforms, ``cmd_vel``/Twist
commands, differential drive control, and reading sensor data in
Python nodes.

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

   What is the role of ``ros_gz_bridge`` in a Gazebo Harmonic + ROS 2
   system?

   A. It replaces the Gazebo physics engine with a ROS 2
      implementation.

   B. It converts Gazebo Transport messages to ROS 2 messages (and
      vice versa) so that ROS 2 nodes can interact with the
      simulation.

   C. It is the GUI client that renders the 3D simulation viewport.

   D. It compiles SDF files into URDF for ROS 2 compatibility.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It converts Gazebo Transport messages to ROS 2 messages
   (and vice versa) so that ROS 2 nodes can interact with the
   simulation.

   Gazebo Harmonic uses its own transport layer (Gazebo Transport)
   based on Protobuf messages, which is completely independent of
   ROS 2. The ``ros_gz_bridge`` subscribes to Gazebo Transport topics
   and republishes them as ROS 2 messages, and vice versa. Without
   the bridge, ``ros2 topic list`` shows no Gazebo data, and ROS 2
   velocity commands cannot reach the simulated robot.


.. admonition:: Question 2
   :class: hint

   In the ``ros_gz_bridge`` topic mapping syntax, what does the
   following line mean?

   .. code-block:: text

      /cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist

   A. Data flows from Gazebo to ROS 2 on the ``/cmd_vel`` topic.

   B. Data flows from ROS 2 to Gazebo on the ``/cmd_vel`` topic.

   C. Data flows bidirectionally between ROS 2 and Gazebo.

   D. The bridge creates a new ``/cmd_vel`` topic in Gazebo only.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Data flows from ROS 2 to Gazebo on the ``/cmd_vel`` topic.

   The ``]`` bracket means data flows from the left side (ROS 2) into
   the right side (Gazebo). The ``[`` bracket means the opposite
   direction (Gazebo to ROS 2). For ``cmd_vel``, the direction is
   ROS 2 to Gazebo because ROS 2 nodes publish velocity commands
   that the simulated robot must receive.


.. admonition:: Question 3
   :class: hint

   Which of the following is NOT a required system plugin in a Gazebo
   Harmonic world file?

   A. ``gz::sim::systems::Physics``

   B. ``gz::sim::systems::SceneBroadcaster``

   C. ``gz::sim::systems::UserCommands``

   D. ``gz::sim::systems::RosBridge``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``gz::sim::systems::RosBridge``

   There is no built-in Gazebo system plugin called ``RosBridge``.
   The ROS 2 bridge is a separate ROS 2 node (``ros_gz_bridge``)
   that runs outside Gazebo. The three required system plugins are
   ``Physics`` (steps the simulation), ``SceneBroadcaster`` (sends
   scene data to the GUI), and ``UserCommands`` (allows runtime
   model spawning and manipulation). The ``Sensors`` plugin is also
   commonly needed for sensor data generation.


.. admonition:: Question 4
   :class: hint

   What does ``rclpy.time.Time()`` (time zero) mean when passed to
   ``tf_buffer.lookup_transform()``?

   A. It requests the transform at simulation time zero (the start
      of the simulation).

   B. It requests the transform at the Unix epoch (January 1, 1970).

   C. It requests the most recently available transform regardless
      of timestamp.

   D. It causes ``lookup_transform`` to block indefinitely until
      a transform is published.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It requests the most recently available transform
   regardless of timestamp.

   In TF2, passing a zero-valued ``Time`` object is a special
   convention meaning "give me the latest transform you have." This
   is the most common usage pattern because you typically want the
   current state of the robot, not a historical transform. To query
   a transform at a specific time, you pass a non-zero ``Time``
   message matching the desired timestamp.


.. admonition:: Question 5
   :class: hint

   For a differential-drive robot in ROS 2, which fields of the
   ``geometry_msgs/msg/Twist`` message are used?

   A. ``linear.x`` and ``linear.y``

   B. ``linear.x`` and ``angular.z``

   C. ``angular.x`` and ``angular.z``

   D. ``linear.x``, ``linear.y``, and ``angular.z``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``linear.x`` and ``angular.z``

   A differential-drive robot can only move forward/backward
   (``linear.x``) and rotate about the vertical axis
   (``angular.z``). It cannot move sideways (``linear.y`` is zero
   because it is a non-holonomic platform), and roll/pitch rates
   (``angular.x``, ``angular.y``) are always zero for a ground
   robot. All other fields of the ``Twist`` message must be set to
   ``0.0``.


.. admonition:: Question 6
   :class: hint

   Why must you bridge the ``/clock`` topic when running Gazebo with
   ROS 2 nodes?

   A. Because Gazebo does not have an internal clock and relies on
      ROS 2 for time.

   B. So that ROS 2 nodes use simulation time instead of wall clock
      time, ensuring consistent timestamps.

   C. Because ROS 2 cannot function without a ``/clock`` topic
      published at all times.

   D. To synchronize the Gazebo GUI refresh rate with ROS 2
      timer frequencies.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- So that ROS 2 nodes use simulation time instead of wall
   clock time, ensuring consistent timestamps.

   When ``use_sim_time`` is set to ``True`` on a ROS 2 node, the
   node's clock subscribes to ``/clock`` instead of using the system
   wall clock. This is essential for reproducibility: if Gazebo runs
   slower or faster than real time, all ROS 2 nodes stay synchronized
   with the simulation. Without bridging ``/clock``, sensor data
   timestamps and node clocks will be misaligned, causing TF lookup
   failures and incorrect behavior.


.. admonition:: Question 7
   :class: hint

   What is the difference between ``/tf`` and ``/tf_static`` in ROS 2?

   A. ``/tf`` uses ``BEST_EFFORT`` QoS and ``/tf_static`` uses
      ``RELIABLE`` QoS; otherwise they are identical.

   B. ``/tf`` carries transforms that change over time, while
      ``/tf_static`` carries transforms that are published once with
      ``TRANSIENT_LOCAL`` durability so late-joining subscribers
      still receive them.

   C. ``/tf`` is for robot frames and ``/tf_static`` is for world
      frames such as ``map``.

   D. ``/tf_static`` is deprecated in ROS 2 Jazzy; all transforms
      should use ``/tf``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``/tf`` carries transforms that change over time, while
   ``/tf_static`` carries transforms that are published once with
   ``TRANSIENT_LOCAL`` durability so late-joining subscribers still
   receive them.

   Dynamic transforms (e.g., ``odom`` -> ``base_link``) are published
   continuously on ``/tf`` and expire if not refreshed. Static
   transforms (e.g., ``base_link`` -> ``lidar_link``) never change,
   so they are published once on ``/tf_static`` with
   ``TRANSIENT_LOCAL`` durability. This means any node that starts
   after the static broadcaster automatically receives the cached
   static transforms without waiting for the next publish cycle.


.. admonition:: Question 8
   :class: hint

   A student launches Gazebo with a lidar-equipped robot but sees no
   data on the ``/lidar`` ROS 2 topic. Which of the following is the
   most likely cause?

   A. The lidar sensor is not defined in the SDF file.

   B. The ``ros_gz_bridge`` is not running or is missing the lidar
      topic mapping.

   C. The ``Sensors`` system plugin is missing from the world file.

   D. All of the above could cause this problem.

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- All of the above could cause this problem.

   Missing lidar data on the ROS 2 side can be caused by any link in
   the pipeline: (A) if the sensor is not defined in SDF, Gazebo
   generates no data; (B) if the bridge is not running or has the
   wrong topic name, Gazebo data is not forwarded to ROS 2; (C) if
   the ``Sensors`` system plugin is missing, Gazebo will not generate
   any sensor data even if the sensor is defined. Debugging requires
   checking all three: the SDF file, the bridge configuration, and
   the world's system plugins.


----


True / False
============

.. admonition:: Question 9
   :class: hint

   **True or False:** TF2 allows coordinate frames to form a general
   graph with cycles and multiple parents.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   TF2 organizes coordinate frames as a strict **tree** structure.
   Every frame has exactly one parent frame (except the root frame,
   which has none). There are no cycles, and no frame can have
   multiple parents. If you accidentally publish transforms that
   create a cycle or give a frame two parents, TF2 will report an
   error and the lookup will fail. This tree constraint ensures that
   the transform between any two frames is unique and unambiguous.


.. admonition:: Question 10
   :class: hint

   **True or False:** In Gazebo Harmonic, the ``DiffDrive`` system
   plugin subscribes directly to ROS 2 ``/cmd_vel`` messages without
   needing a bridge.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The ``DiffDrive`` plugin operates within Gazebo and subscribes to
   ``cmd_vel`` on **Gazebo Transport**, not on ROS 2. A
   ``ros_gz_bridge`` must be running to convert ROS 2
   ``geometry_msgs/msg/Twist`` messages into Gazebo
   ``gz.msgs.Twist`` messages. Without the bridge, ROS 2 velocity
   commands never reach the simulated robot.


.. admonition:: Question 11
   :class: hint

   **True or False:** A ``StaticTransformBroadcaster`` must publish
   its transforms continuously at a fixed rate, just like a dynamic
   ``TransformBroadcaster``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   A ``StaticTransformBroadcaster`` publishes to the ``/tf_static``
   topic with ``TRANSIENT_LOCAL`` durability. This means the transform
   is published **once** and cached by DDS. Any subscriber that
   connects later automatically receives the cached transform without
   the broadcaster needing to republish. In contrast, a dynamic
   ``TransformBroadcaster`` must publish continuously because
   ``/tf`` uses ``VOLATILE`` durability and transforms expire from
   the TF2 buffer after a timeout.


.. admonition:: Question 12
   :class: hint

   **True or False:** Setting ``max_step_size`` to ``0.01`` in the
   Gazebo physics configuration makes the simulation run faster
   but may cause objects to pass through each other.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A larger ``max_step_size`` means the physics engine advances
   more simulated time per step, so fewer steps are needed per
   second of simulation time, making it run faster. However, larger
   steps reduce the accuracy of collision detection and constraint
   solving. Fast-moving objects can "tunnel" through thin walls
   because the physics engine does not detect the contact between
   steps. For contact-heavy simulations, ``0.001`` seconds or
   smaller is recommended.


.. admonition:: Question 13
   :class: hint

   **True or False:** Publishing a single ``Twist`` message on
   ``/cmd_vel`` will cause a differential-drive robot to move at
   that velocity indefinitely.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Most differential-drive controllers implement a command timeout.
   If no new ``cmd_vel`` message arrives within the timeout period
   (typically 0.5-1.0 seconds), the controller sets the wheel
   velocities to zero as a safety measure. To maintain continuous
   motion, you must publish ``cmd_vel`` messages at a steady rate
   (typically 10-50 Hz). This is why ``teleop_twist_keyboard``
   publishes repeatedly while a key is held down, not just once per
   key press.


----


Essay Questions
===============

.. admonition:: Question 14
   :class: hint

   **Explain the complete data path for a lidar scan from Gazebo to
   a ROS 2 subscriber node.** Describe each component involved and
   the message format at each stage.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The ``Sensors`` system plugin in Gazebo generates lidar data
     each simulation step based on the sensor definition in the SDF
     file. The data is published as a ``gz.msgs.LaserScan`` Protobuf
     message on a Gazebo Transport topic (e.g., ``/lidar``).
   - The ``ros_gz_bridge`` subscribes to the Gazebo Transport topic,
     deserializes the Protobuf message, converts it to a
     ``sensor_msgs/msg/LaserScan`` ROS 2 message, and publishes it
     on the corresponding ROS 2 topic.
   - The ROS 2 subscriber node receives the
     ``sensor_msgs/msg/LaserScan`` message through DDS, which
     triggers its callback function. The callback processes the
     ``ranges`` array to extract distance measurements.
   - The pipeline requires three correctly configured components:
     the sensor in SDF, the bridge mapping, and the ROS 2 subscriber.
     A failure at any stage silently breaks the data flow.


.. admonition:: Question 15
   :class: hint

   **Describe the difference between static and dynamic transforms
   in TF2 and explain when you would use each.** Give a concrete
   example of each type in a mobile robot system.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **Static transforms** represent fixed geometric relationships
     that never change, such as the offset from ``base_link`` to a
     rigidly mounted sensor (``lidar_link``, ``camera_link``). They
     are published once on ``/tf_static`` with ``TRANSIENT_LOCAL``
     durability. Use a ``StaticTransformBroadcaster``.
   - **Dynamic transforms** represent relationships that change over
     time, such as ``odom`` -> ``base_link`` (updated as the robot
     moves) or ``map`` -> ``odom`` (updated by a localization
     algorithm). They are published continuously on ``/tf`` at a
     regular rate (e.g., 50 Hz). Use a ``TransformBroadcaster``.
   - The key design choice: if the relative pose between two frames
     is physically fixed (bolted, welded), use a static transform.
     If it changes during operation, use a dynamic transform.
   - Using a static transform for a fixed relationship avoids
     unnecessary network traffic and ensures late-joining nodes
     immediately receive the transform.


.. admonition:: Question 16
   :class: hint

   **Describe how the Gazebo DiffDrive plugin converts a Twist
   command into wheel velocities.** What parameters are needed and
   what outputs does the plugin produce?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The ``DiffDrive`` plugin receives a ``Twist`` command
     (``linear.x`` and ``angular.z``) and uses the differential drive
     kinematic equations to compute left and right wheel angular
     velocities. The two key parameters are ``wheel_separation`` (L)
     and ``wheel_radius`` (r).
   - The kinematic equations are:
     ``v_left = (linear.x - angular.z * L / 2) / r`` and
     ``v_right = (linear.x + angular.z * L / 2) / r``.
   - The plugin applies these velocities to the wheel joints in the
     physics simulation, causing the robot to move.
   - As output, the plugin computes and publishes odometry (position
     and velocity estimates based on wheel rotation) on the ``odom``
     topic and the ``odom`` -> ``base_link`` transform on the ``tf``
     topic.
