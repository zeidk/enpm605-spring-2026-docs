====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 13: Mapping and
Navigation with Nav2. Topics include map representations, occupancy
grids, the ``map`` frame and REP 105, SLAM with ``slam_toolbox``
(scan matching, pose graph, loop closure), localization with AMCL
(particle filters, predict/update/resample), costmaps (global vs.
local, layers, inflation, footprint), planners and controllers, the
behavior tree, and the ``NavigateToPose`` action API.

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

   In a ``nav_msgs/OccupancyGrid``, what does a cell value of
   ``-1`` mean?

   A. The cell is free space.

   B. The cell is occupied.

   C. The cell has not been observed yet (unknown).

   D. The cell is invalid and should be ignored.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The cell is **unknown**.

   ``OccupancyGrid`` uses ``0`` for free, ``100`` for occupied, and
   ``-1`` for unknown. RViz2 renders unknown cells in grey.


.. admonition:: Question 2
   :class: hint

   Which transform in the REP 105 chain is allowed to **jump**?

   A. ``base_link`` -> sensor frames

   B. ``odom`` -> ``base_link``

   C. ``map`` -> ``odom``

   D. ``world`` -> ``map``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``map`` -> ``odom``.

   The localization stack (SLAM or AMCL) corrects accumulated drift
   by adjusting this transform. The ``odom`` -> ``base_link``
   transform must remain smooth (no jumps); the ``map`` -> ``odom``
   transform absorbs the corrections.


.. admonition:: Question 3
   :class: hint

   In ``slam_toolbox``, what does **loop closure** add to the pose
   graph?

   A. A new node at the robot's current pose.

   B. An edge connecting two distant nodes that observed the same
      area.

   C. A new occupancy grid layer.

   D. A copy of every previous scan as a fresh node.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- An edge connecting two distant nodes.

   When the robot revisits an area, scan matching between the
   current scan and the stored scan creates a constraint between the
   two corresponding nodes. The graph optimizer then realigns all
   poses to satisfy this new constraint, correcting accumulated
   drift.


.. admonition:: Question 4
   :class: hint

   Why is AMCL called **adaptive**?

   A. It can run on any robot regardless of sensor configuration.

   B. It varies the number of particles based on how well-localized
      the robot is.

   C. It automatically chooses between a 2D and 3D map.

   D. It adapts the map resolution at runtime.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It varies the particle count.

   When the robot is lost, AMCL uses many particles to cover the
   uncertainty. When the cloud has converged, it shrinks the
   particle set to save CPU. Standard MCL uses a fixed count.


.. admonition:: Question 5
   :class: hint

   Which two costmaps does Nav2 maintain, and what is each used for?

   A. **Static** for the map; **dynamic** for the robot.

   B. **Global** (whole map, used by the planner) and **local**
      (rolling window, used by the controller).

   C. **Inflation** for safety; **obstacle** for path planning.

   D. **Sensor** and **plan**, both updated at 20 Hz.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Global and local.

   The global costmap covers the entire map and feeds the global
   planner. The local costmap is a rolling window around the robot
   updated at sensor rate; it feeds the local controller and handles
   dynamic obstacles.


.. admonition:: Question 6
   :class: hint

   In Nav2, which planner is best suited to a non-holonomic robot
   that must navigate tight spaces with kinematic constraints
   enforced from the start?

   A. NavFn (Dijkstra/A*)

   B. Smac Hybrid A*

   C. DWB

   D. Regulated Pure Pursuit

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Smac Hybrid A*.

   Smac Hybrid A* searches an SE(2) lattice that respects the
   robot's turning radius, so the resulting path is physically
   drivable. NavFn ignores kinematics, and DWB / RPP are
   *controllers*, not planners.


.. admonition:: Question 7
   :class: hint

   What is the role of the **inflation layer** in a Nav2 costmap?

   A. It increases the resolution of the costmap near obstacles.

   B. It expands lethal cells outward, creating a graded cost
      gradient that steers the robot away from walls.

   C. It removes obstacles that are far from the robot.

   D. It records which cells were inflated by past plans.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Expands lethal cells outward.

   The inflation layer turns a hard binary obstacle into a smooth
   cost gradient. The planner then prefers paths that stay away from
   walls without explicitly modelling the robot's footprint at every
   cell.


.. admonition:: Question 8
   :class: hint

   In the ``NavigateToPose`` action, what does **feedback** provide?

   A. The final outcome of the navigation task.

   B. A periodic stream containing the current pose, distance
      remaining, and recovery count while the goal is active.

   C. A copy of the goal pose echoed back to the client.

   D. The full planned path on every tick.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A periodic stream of progress information.

   Feedback includes ``current_pose``, ``navigation_time``,
   ``estimated_time_remaining``, ``distance_remaining``, and
   ``number_of_recoveries``. The **result** is sent only once when
   the goal terminates.


----


True/False
==========

.. admonition:: Question 9
   :class: hint

   Setting ``set_initial_pose: true`` in AMCL's parameters and
   providing ``initial_pose_x``, ``initial_pose_y``, and
   ``initial_pose_a`` is a valid alternative to clicking
   **2D Pose Estimate** in RViz2.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- Both methods deliver the same initial pose to AMCL.
   The parameter approach is reproducible and well suited to
   scripted tests; the RViz2 button is convenient interactively.


.. admonition:: Question 10
   :class: hint

   The robot's **circumscribed radius** is the radius of the largest
   circle that fits *inside* the footprint.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- That definition describes the **inscribed radius**.
   The circumscribed radius is the smallest circle that *encloses*
   the footprint.


.. admonition:: Question 11
   :class: hint

   ``slam_toolbox`` can be used to localize against a previously
   saved map without modifying it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- ``slam_toolbox`` has a localization mode that loads
   an existing serialized graph and runs scan matching against it
   without adding new nodes, similar in role to AMCL.


.. admonition:: Question 12
   :class: hint

   In Nav2, the global planner is called every control cycle to
   produce a fresh path.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- The planner is called once per goal request and
   replanned only when needed (e.g., the path becomes blocked or a
   new goal arrives). The **local controller** runs every control
   cycle, typically at 20 Hz.


.. admonition:: Question 13
   :class: hint

   When using ``BasicNavigator.followWaypoints(poses)``, you must
   manually create your own ``NavigateToPose`` action client.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- ``BasicNavigator`` wraps the underlying action
   clients. You only construct the list of ``PoseStamped`` waypoints
   and call ``followWaypoints``; the action plumbing is hidden.


----


Essay Questions
===============

.. admonition:: Question 14
   :class: hint

   Explain how scan matching, the pose graph, and loop closure work
   together in ``slam_toolbox`` to produce a globally consistent
   map. Why is loop closure essential after long traversals?

.. dropdown:: Answer
   :class-container: sd-border-success

   Scan matching aligns consecutive LiDAR scans to estimate the
   relative motion between two robot poses; each result becomes an
   edge in the pose graph. The pose graph stores these edges as
   constraints between nodes that represent successive robot poses
   along the trajectory. Sequential edges accumulate small errors
   over time, so without correction the map would shear and
   overlap. Loop closure detects when the robot revisits a
   previously seen area, runs scan matching between the current and
   stored scans, and adds a new edge connecting two distant nodes.
   The graph optimizer then adjusts every node simultaneously to
   minimize the total constraint error, redistributing accumulated
   drift across the entire trajectory and producing a globally
   consistent occupancy grid.


.. admonition:: Question 15
   :class: hint

   Describe the predict / update / resample cycle of AMCL's
   particle filter. What role does each step play in keeping the
   pose estimate accurate?

.. dropdown:: Answer
   :class-container: sd-border-success

   In **predict**, every particle is shifted by the robot's measured
   motion plus a small amount of noise drawn from the motion model.
   This propagates the estimate forward in time and spreads the
   particles slightly to reflect uncertainty in the motion. In
   **update**, each particle is scored by casting a virtual LiDAR
   from its pose into the map and comparing the predicted ranges to
   the actual sensor reading; particles that explain the data well
   gain weight. In **resample**, a new set of particles is drawn
   with replacement, with probability proportional to weight, so
   high-weight hypotheses are duplicated and low-weight ones are
   dropped. Repeated cycles concentrate the cloud around poses that
   consistently explain motion and observation, giving a converged
   pose estimate.


.. admonition:: Question 16
   :class: hint

   Compare the **global costmap** and the **local costmap** in
   Nav2. Why does Nav2 maintain two separate costmaps instead of one?

.. dropdown:: Answer
   :class-container: sd-border-success

   The global costmap covers the entire map and is used by the
   global planner; it is built primarily from the static map (and
   slow-changing obstacles), updated at a low rate, and supports
   long-range route planning. The local costmap is a rolling window
   centred on the robot, updated at sensor rate from live LiDAR /
   depth data, and is used by the local controller to react to
   dynamic obstacles such as a person stepping into a corridor.
   Splitting them means each costmap can be sized and tuned for its
   own role: the global one is large but cheap to update; the local
   one is small but high-frequency and aggressive about new
   obstacles. Trying to use a single costmap would force a bad
   tradeoff between coverage, latency, and CPU cost.


.. admonition:: Question 17
   :class: hint

   In the ``NavigateToPose`` action interface, distinguish **goal**,
   **feedback**, and **result**, and explain why this three-part
   structure is appropriate for navigation.

.. dropdown:: Answer
   :class-container: sd-border-success

   The **goal** is the target ``PoseStamped`` in the ``map`` frame,
   sent once when the client requests navigation. **Feedback** is
   published periodically while the task is running and contains
   live progress information -- current pose, distance remaining,
   time elapsed, and recovery count. The **result** is sent exactly
   once when the task terminates and conveys the final status code
   (SUCCEEDED, CANCELED, or FAILED). This three-part structure fits
   navigation because the task is long-running (so a one-shot
   service would either block or time out), the client typically
   wants progress updates without polling, and the client must be
   able to cancel the goal mid-execution if a higher-priority task
   arrives.
