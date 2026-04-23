====================================================
Exercises
====================================================

This page contains four take-home exercises that reinforce the concepts
from Lecture 12. Each exercise asks you to **write code from scratch**
based on a specification -- no starter code is provided.

All files should be created inside your ``~/enpm605_ws/src/`` workspace
in the appropriate packages (``namespace_demo``, ``remapping_demo``,
``lifecycle_demo``, or ``bt_demo``).


.. dropdown:: Exercise 1 -- Multi-Camera Namespace Launch
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a launch file that starts **three** instances of the same
    camera node, each in a different namespace, and verify they are
    fully isolated.


    .. raw:: html

       <hr>


    **Specification**

    Create a launch file at
    ``namespace_demo/launch/three_cameras.launch.py`` that:

    1. Starts three ``camera_demo_exe`` nodes under namespaces
       ``/front``, ``/left``, and ``/right``.
    2. Each node must use ``output="screen"`` and ``emulate_tty=True``.

    **Verification:**

    .. code-block:: console

       ros2 launch namespace_demo three_cameras.launch.py

    In a second terminal:

    .. code-block:: console

       ros2 node list
       # Expected: /front/camera_node, /left/camera_node, /right/camera_node

       ros2 topic list
       # Expected: /front/image_raw, /left/image_raw, /right/image_raw

       rqt_graph
       # Three isolated publisher nodes, no cross-talk


.. dropdown:: Exercise 2 -- Lifecycle Node with on_shutdown
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Extend the ``SensorPublisher`` lifecycle node to implement the
    ``on_shutdown`` callback and test the full lifecycle including
    shutdown.


    .. raw:: html

       <hr>


    **Specification**

    Modify ``lifecycle_demo/lifecycle_demo/sensor_publisher.py`` to add:

    1. An ``on_shutdown(self, state)`` callback that:

       - Cancels the timer if it exists.
       - Sets the publisher to ``None``.
       - Logs ``"Shutting down from: {state.label}"``.
       - Returns ``TransitionCallbackReturn.SUCCESS``.

    **Verification:**

    .. code-block:: console

       # T1:
       ros2 run lifecycle_demo sensor_pub_exe
       # T2:
       ros2 lifecycle set /sensor_publisher configure
       ros2 lifecycle set /sensor_publisher activate
       ros2 lifecycle set /sensor_publisher shutdown
       ros2 lifecycle get /sensor_publisher
       # Expected: finalized

    Test ``shutdown`` from different states:

    - From Unconfigured (immediately after starting the node).
    - From Inactive (after configure but before activate).
    - From Active (after activate).

    In all cases, the node should reach **Finalized** and log the
    shutdown message.


.. dropdown:: Exercise 3 -- Add a New Condition Node to the BT
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Add a ``MaxDistanceTraveled`` condition node to the behavior tree
    that stops the robot after it has traveled a configurable maximum
    distance.


    .. raw:: html

       <hr>


    **Specification**

    Create ``bt_demo/bt_demo/max_distance.py`` that implements:

    1. A ``MaxDistanceTraveled`` class inheriting from
       ``py_trees.behaviour.Behaviour``.
    2. Constructor takes ``name`` and ``max_distance`` (float, meters).
    3. In ``setup()``, subscribe to ``/odometry/filtered``.
    4. Track the cumulative distance traveled by computing the
       Euclidean distance between consecutive odometry readings.
    5. In ``update()``:

       - Return ``SUCCESS`` if the total distance is below
         ``max_distance`` (robot can keep going).
       - Return ``FAILURE`` if the total distance exceeds
         ``max_distance`` (robot should stop).

    6. Add this condition to the root Sequence in
       ``main_drive_to_goal.py``, **before** the ``GoalNotReached?``
       condition:

    .. code-block:: text

       Sequence (DriveToGoal, memory=False)
       |-- MaxDistanceTraveled?    [NEW]
       |-- GoalNotReached?
       |-- Selector (DriveOrRecover, memory=True)
           |-- ...

    **Verification:**

    .. code-block:: console

       ros2 launch bt_demo drive_to_goal.py goal_x:=100.0 max_distance:=3.0

    The robot should stop after approximately 3 meters, even though the
    goal is 100 meters away.


.. dropdown:: Exercise 4 -- Topic Remapping with Multiple Subscribers
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a launch file that connects two camera publishers to a
    single image processor subscriber using topic remapping.


    .. raw:: html

       <hr>


    **Specification**

    Create ``remapping_demo/launch/multi_remap.launch.py`` that:

    1. Starts two ``camera_demo_exe`` nodes with names ``front_camera``
       and ``rear_camera``.
    2. Remaps their topics:

       - ``front_camera``: ``image_raw`` -> ``/sensors/front/image``
       - ``rear_camera``: ``image_raw`` -> ``/sensors/rear/image``

    3. Starts two ``image_processor_exe`` nodes with names
       ``front_processor`` and ``rear_processor``.
    4. Remaps their subscriptions:

       - ``front_processor``: ``camera/image`` -> ``/sensors/front/image``
       - ``rear_processor``: ``camera/image`` -> ``/sensors/rear/image``

    **Verification:**

    .. code-block:: console

       ros2 launch remapping_demo multi_remap.launch.py

    In a second terminal:

    .. code-block:: console

       ros2 topic list
       # Expected: /sensors/front/image and /sensors/rear/image

       rqt_graph
       # front_camera -> /sensors/front/image -> front_processor
       # rear_camera  -> /sensors/rear/image  -> rear_processor
