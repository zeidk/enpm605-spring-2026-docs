====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 11: Pose Representation,
Coordinate Frames, TF2, and Mobile Robot Control. Topics include
position and orientation (Euler angles, quaternions, gimbal lock),
coordinate frames (REP 105), the TF2 transform library (static and
dynamic broadcasters, listeners, ``Buffer``), differential drive
kinematics, odometry, and proportional controllers.

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

   Which of the following correctly describes a quaternion representing
   **no rotation** (the identity)?

   A. :math:`(w, x, y, z) = (0, 0, 0, 0)`

   B. :math:`(w, x, y, z) = (1, 0, 0, 0)`

   C. :math:`(w, x, y, z) = (0, 1, 0, 0)`

   D. :math:`(w, x, y, z) = (0.5, 0.5, 0.5, 0.5)`

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- :math:`(w, x, y, z) = (1, 0, 0, 0)`.

   In the axis-angle-to-quaternion formula, a rotation angle of
   :math:`\theta = 0` gives :math:`w = \cos(0) = 1` and
   :math:`(x, y, z) = \sin(0) \cdot \mathbf{u} = (0, 0, 0)`.
   Option A is not a valid quaternion (zero magnitude). Options C
   and D encode non-zero rotations.


.. admonition:: Question 2
   :class: hint

   What is the **gimbal lock** problem?

   A. A quaternion becomes invalid when its magnitude is not 1.

   B. Two rotation axes align at certain Euler angle values, causing
      one degree of freedom to be lost.

   C. The robot's wheels lock when the angular velocity is too high.

   D. TF2 cannot interpolate between two frames that share a parent.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Two rotation axes align, losing one degree of freedom.

   In the Tait-Bryan ZYX convention, when pitch
   (:math:`\theta`) reaches :math:`\pm 90°`, the yaw and roll axes
   align. The rotation matrix then depends only on the difference
   :math:`(\psi - \phi)`, not on :math:`\psi` and :math:`\phi`
   independently. This makes certain orientations unreachable through
   smooth Euler-angle interpolation and is the primary reason ROS 2
   uses quaternions instead.


.. admonition:: Question 3
   :class: hint

   In the standard ROS 2 frame hierarchy (REP 105), which frame is
   **locally consistent but drifts over time**?

   A. ``world``

   B. ``map``

   C. ``odom``

   D. ``base_link``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``odom``.

   The ``odom`` frame is computed from wheel odometry and/or IMU
   integration. It is locally smooth (never jumps) but accumulates
   drift over time. The ``map`` frame, in contrast, may jump when a
   localization correction occurs (e.g., loop closure) but is
   globally consistent. ``world`` is the fixed inertial frame, and
   ``base_link`` moves with the robot.


.. admonition:: Question 4
   :class: hint

   For a differential drive robot, which fields of
   ``geometry_msgs/msg/Twist`` carry meaningful values?

   A. ``linear.x`` and ``linear.y``

   B. ``linear.x`` and ``angular.z``

   C. ``angular.x`` and ``angular.z``

   D. ``linear.x``, ``linear.y``, and ``angular.z``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``linear.x`` and ``angular.z``.

   A differential drive robot can only move forward/backward
   (``linear.x``) and rotate about its vertical axis
   (``angular.z``). It cannot translate sideways
   (``linear.y = 0``) or rotate about the forward or lateral axes
   (``angular.x = angular.y = 0``). All other fields are set to
   zero.


.. admonition:: Question 5
   :class: hint

   What does ``tf_buffer.lookup_transform("odom", "camera_link",
   rclpy.time.Time())`` return?

   A. The transform that converts points from ``odom`` into
      ``camera_link``.

   B. The transform that converts points from ``camera_link`` into
      ``odom``.

   C. The inverse of the ``camera_link`` → ``odom`` transform.

   D. Both B and C.

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- Both B and C.

   ``lookup_transform(target, source, time)`` returns the transform
   that expresses the ``source`` frame in the ``target`` frame. This
   means it converts points from ``camera_link`` (source) into
   ``odom`` (target). This is equivalent to the inverse of the
   ``camera_link`` → ``odom`` transform, so B and C describe the
   same thing.


.. admonition:: Question 6
   :class: hint

   Which topic do **static** transforms publish on?

   A. ``/tf``

   B. ``/tf_static``

   C. ``/tf_tree``

   D. ``/transform_static``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``/tf_static``.

   Static transforms are published once on ``/tf_static`` and are
   latched (retained for late-joining subscribers). Dynamic
   transforms are published repeatedly on ``/tf``. TF2's ``Buffer``
   subscribes to both topics and treats them differently: static
   transforms never expire, while dynamic transforms have a
   configurable timeout.


.. admonition:: Question 7
   :class: hint

   In a proportional controller, what happens to the velocity command
   as the robot approaches the goal?

   A. It increases because the gain is constant.

   B. It remains constant until the robot enters the tolerance zone.

   C. It decreases because the error decreases.

   D. It oscillates between positive and negative values.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It decreases because the error decreases.

   The proportional control law is :math:`u = K_p \cdot e`. As the
   robot approaches the goal, the error :math:`e` (distance or
   heading difference) decreases, so the commanded velocity decreases
   proportionally. This natural deceleration is a key property of
   P-control. However, with very low gains, the robot may stop short
   of the goal (steady-state error).


.. admonition:: Question 8
   :class: hint

   Given wheel separation :math:`L` and wheel radius :math:`r`, if
   both wheels spin at the same speed (:math:`v_L = v_R = v_w`),
   what is the angular velocity :math:`\omega`?

   A. :math:`\omega = r \cdot v_w / L`

   B. :math:`\omega = 0`

   C. :math:`\omega = 2 r \cdot v_w / L`

   D. :math:`\omega = v_w / r`

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- :math:`\omega = 0`.

   From the differential drive kinematics:
   :math:`\omega = r(v_R - v_L) / L`. When both wheels spin at the
   same speed, :math:`v_R - v_L = 0`, so :math:`\omega = 0`. The
   robot moves in a straight line with linear velocity
   :math:`v = r(v_R + v_L) / 2 = r \cdot v_w`.


----


True/False
==========

.. admonition:: Question 9
   :class: hint

   **True or False:** Quaternions :math:`q` and :math:`-q` represent
   different rotations.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   This is the **double cover** property. Both :math:`q` and
   :math:`-q` map to the same 3D rotation. For example,
   :math:`(0.707, 0.707, 0, 0)` and :math:`(-0.707, -0.707, 0, 0)`
   both encode a :math:`90°` rotation about the :math:`x`-axis. This
   can cause sign-flip artifacts when interpolating or comparing
   quaternions.


.. admonition:: Question 10
   :class: hint

   **True or False:** A ``StaticTransformBroadcaster`` should be used
   for publishing the ``odom`` → ``base_link`` transform.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The ``odom`` → ``base_link`` transform changes continuously as the
   robot moves. It must be published repeatedly on ``/tf`` using a
   ``TransformBroadcaster``. A ``StaticTransformBroadcaster``
   publishes once on ``/tf_static`` and TF2 assumes the transform is
   permanent. Using it for a time-varying relationship would cause the
   robot to appear frozen in RViz and break all downstream consumers.


.. admonition:: Question 11
   :class: hint

   **True or False:** Quaternion multiplication is commutative.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Quaternion multiplication is **not commutative**:
   :math:`q_1 \otimes q_2 \neq q_2 \otimes q_1` in general.
   The order matters because it determines which rotation is applied
   first. In a world-frame rotation, the new rotation is
   pre-multiplied; in a body-frame rotation, it is post-multiplied.


.. admonition:: Question 12
   :class: hint

   **True or False:** The TF2 transform tree can contain cycles (a
   frame can have more than one parent).

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The TF2 transform tree is a strict **tree**: every frame has
   exactly one parent, and there is exactly one root frame (typically
   ``world``). Cycles are not allowed. If two broadcasters publish
   conflicting parent relationships for the same frame, TF2 will
   report an error. To find the transform between any two frames,
   TF2 traverses up to the common ancestor and back down.


.. admonition:: Question 13
   :class: hint

   **True or False:** Odometry provides a globally accurate estimate
   of the robot's position.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Odometry integrates small incremental motions over time, so it
   **drifts**. Small errors in each step (wheel slip, encoder
   resolution, uneven terrain) accumulate, causing the estimated pose
   to diverge from the true pose. This is why the ``odom`` frame is
   described as "locally consistent, drift-prone." Global accuracy
   requires an additional localization source (e.g., AMCL against a
   known map).


----


Essay Questions
===============

.. admonition:: Question 14
   :class: hint

   Explain why ROS 2 uses quaternions instead of Euler angles to
   represent orientations. In your answer, mention gimbal lock and at
   least one other advantage of quaternions.

.. dropdown:: Answer
   :class-container: sd-border-success

   ROS 2 uses quaternions because they are **singularity-free**: unlike
   Euler angles, which suffer from gimbal lock when two rotation axes
   align (e.g., pitch at :math:`\pm 90°`), quaternions can represent
   any orientation without losing a degree of freedom. Additionally,
   quaternions are efficient to **compose** (a single quaternion
   multiplication vs. three matrix multiplications for Euler angles),
   produce smooth **interpolation** (SLERP), and require only four
   numbers to store a rotation. The trade-off is reduced human
   intuition: reading ``(0.707, 0, 0, 0.707)`` is less intuitive
   than "yaw = 90°," which is why ``scipy`` or ``tf_transformations``
   conversion functions are commonly used.


.. admonition:: Question 15
   :class: hint

   Describe the difference between a **static** and a **dynamic**
   transform in TF2. Give one concrete example of each.

.. dropdown:: Answer
   :class-container: sd-border-success

   A **static transform** describes a fixed geometric relationship
   that never changes over time. It is published once on
   ``/tf_static`` and is latched so that late-joining subscribers
   receive it immediately. Example: the offset from ``base_link`` to
   a rigidly mounted LiDAR (``lidar_link``).

   A **dynamic transform** describes a relationship that changes over
   time and must be re-published continuously on ``/tf``. Example:
   the ``odom`` → ``base_link`` transform, which updates as the
   robot moves based on odometry data.

   Using a ``StaticTransformBroadcaster`` for a dynamic relationship
   is incorrect because TF2 treats static transforms as permanent
   and will not update or expire them.


.. admonition:: Question 16
   :class: hint

   A proportional controller drives a robot toward a goal 5 m away
   with gain :math:`K_p = 0.5\,\text{s}^{-1}`. Explain what happens
   to the velocity at each step and identify one limitation of using
   only a P controller for this task.

.. dropdown:: Answer
   :class-container: sd-border-success

   At each control step, the velocity command is
   :math:`v = K_p \cdot d = 0.5 \times d`, where :math:`d` is the
   remaining distance. Initially :math:`v = 0.5 \times 5 = 2.5`
   m/s; as the robot moves closer, :math:`d` decreases and so does
   :math:`v`. The robot decelerates smoothly as it approaches the
   goal.

   A key limitation is **steady-state error**: if external
   disturbances (wheel slip, friction) oppose the motion, the small
   velocity near the goal may not overcome them, causing the robot to
   stop slightly before the target. A PID controller adds an integral
   term to eliminate this residual error and a derivative term to
   reduce overshoot.
