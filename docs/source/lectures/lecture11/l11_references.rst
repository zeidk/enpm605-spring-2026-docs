References
==========


.. dropdown:: Lecture 11
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L11: Coordinate Frames, TF2, and Mobile Robot Control**

        Covers pose representation (position as a 3D vector, orientation
        via Euler angles and quaternions, gimbal lock, axis-angle
        conversion, quaternion composition and multiplication order),
        mobile robot control (Gazebo Harmonic simulation, RViz2
        visualization, differential drive kinematics, ``cmd_vel`` and
        ``TwistStamped``, odometry, proportional controllers for
        position and heading), coordinate frames (REP 105 standard
        frames, transforms, chaining), and TF2 (the transform tree,
        static and dynamic broadcasters, transform listeners, CLI
        tools, KDL frame composition).


.. dropdown:: Orientation and Quaternions
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Robotics, Vision and Control (Corke)
            :link: https://link.springer.com/book/10.1007/978-3-031-07262-8
            :class-card: sd-border-secondary

            **Textbook: Pose and Orientation**

            Comprehensive coverage of spatial math for robotics:
            rotation matrices, Euler angles, quaternions, and
            homogeneous transforms.

        .. grid-item-card:: Modern Robotics (Lynch & Park)
            :link: http://hades.mech.northwestern.edu/index.php/Modern_Robotics
            :class-card: sd-border-secondary

            **Textbook: Kinematics and Dynamics**

            Open-access textbook covering rigid body motion,
            forward and inverse kinematics, and velocity kinematics.


.. dropdown:: TF2 and Coordinate Frames
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: About TF2
            :link: https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Tf2.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: TF2 Concepts**

            Conceptual overview of the transform library: frames,
            transforms, buffers, and the tree structure.

            +++

            - Transform tree
            - Static vs. dynamic transforms
            - Buffer and listener

        .. grid-item-card:: Introduction to TF2
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: TF2 Tutorial**

            Hands-on introduction to TF2 with turtlesim, covering
            broadcasters, listeners, and frame inspection tools.

            +++

            - ``view_frames``
            - ``tf2_echo``
            - ``TransformListener``

        .. grid-item-card:: Writing a Static Broadcaster (Python)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Static TF**

            Tutorial for publishing a fixed transform between two
            frames using ``StaticTransformBroadcaster``.

            +++

            - ``StaticTransformBroadcaster``
            - ``/tf_static``
            - ``TransformStamped``

        .. grid-item-card:: Writing a TF2 Broadcaster (Python)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Dynamic TF**

            Tutorial for publishing a time-varying transform using
            ``TransformBroadcaster``.

            +++

            - ``TransformBroadcaster``
            - ``/tf``
            - Timer-based broadcasting

        .. grid-item-card:: Writing a TF2 Listener (Python)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: TF Listener**

            Tutorial for looking up transforms between frames using
            ``Buffer`` and ``TransformListener``.

            +++

            - ``Buffer``
            - ``TransformListener``
            - ``lookup_transform()``

        .. grid-item-card:: REP 105: Coordinate Frames
            :link: https://www.ros.org/reps/rep-0105.html
            :class-card: sd-border-secondary

            **ROS Enhancement Proposal**

            Defines the standard coordinate frames for mobile
            platforms: ``world``, ``map``, ``odom``,
            ``base_link``, and ``base_footprint``.

            +++

            - Frame naming conventions
            - Parent-child relationships
            - Drift vs. jump semantics


.. dropdown:: Mobile Robot Control
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROSbot ROS Repository
            :link: https://github.com/husarion/rosbot_ros
            :class-card: sd-border-secondary

            **Husarion ROSbot ROS 2 Driver**

            The ROS 2 driver for both ROSbot 3 and ROSbot XL,
            including Gazebo simulation, URDF models, and
            hardware interfaces.

        .. grid-item-card:: Gazebo Harmonic
            :link: https://gazebosim.org/docs/harmonic
            :class-card: sd-border-secondary

            **Gazebo Sim Documentation**

            Official documentation for Gazebo Harmonic, the simulator
            paired with ROS 2 Jazzy.
