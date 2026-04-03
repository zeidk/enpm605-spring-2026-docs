References
==========


.. dropdown:: Lecture 11
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L11: Simulation and Mobile Robot Control**

        Covers Gazebo Harmonic architecture and installation, SDF world
        and model files (world structure, links, joints, sensors, physics
        settings), ``ros_gz_bridge`` configuration and common topic
        mappings, spawning robots with ``ros_gz_sim create``, TF2
        fundamentals (coordinate frames, static and dynamic transforms,
        transform broadcasters and listeners), mobile robot control
        (``cmd_vel`` and ``Twist`` messages, differential drive plugin,
        teleop, reading lidar/camera/IMU data), and launching a complete
        simulation pipeline.


.. dropdown:: Gazebo Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Gazebo Harmonic Documentation
            :link: https://gazebosim.org/docs/harmonic
            :class-card: sd-border-secondary

            **gazebosim.org**

            Official documentation for Gazebo Harmonic, the LTS release
            paired with ROS 2 Jazzy.

            +++

            - Installation guide
            - Tutorials and examples
            - SDF specification reference

        .. grid-item-card:: SDF Format Specification
            :link: http://sdformat.org/spec
            :class-card: sd-border-secondary

            **sdformat.org**

            The Simulation Description Format specification. Reference
            for all SDF elements: world, model, link, joint, sensor,
            physics, and plugin tags.

            +++

            - Element reference
            - Version changelog
            - Schema validation

        .. grid-item-card:: Gazebo Fuel Models
            :link: https://app.gazebosim.org/fuel/models
            :class-card: sd-border-secondary

            **Gazebo Fuel**

            Online repository of pre-built Gazebo models. Include models
            directly in your SDF world files by URI.

            +++

            - Robot models
            - Environment models
            - Sensor models

        .. grid-item-card:: Gazebo Sim API Reference
            :link: https://gazebosim.org/api/sim/8/
            :class-card: sd-border-secondary

            **API Reference**

            C++ API documentation for Gazebo Sim system plugins and
            components.

            +++

            - System plugin interface
            - ECS components
            - Event handling


.. dropdown:: ROS 2 + Gazebo Integration
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ros_gz GitHub Repository
            :link: https://github.com/gazebosim/ros_gz
            :class-card: sd-border-secondary

            **ros_gz**

            Source code and documentation for the ROS 2 + Gazebo
            integration packages: ``ros_gz_bridge``, ``ros_gz_sim``,
            ``ros_gz_image``.

            +++

            - Bridge configuration
            - Spawn examples
            - Image transport bridge

        .. grid-item-card:: ROS 2 Jazzy + Gazebo Integration Guide
            :link: https://docs.ros.org/en/jazzy/Tutorials/Advanced/Simulators/Gazebo/Gazebo.html
            :class-card: sd-border-secondary

            **docs.ros.org**

            Official ROS 2 tutorial for setting up and using Gazebo
            Harmonic with ROS 2 Jazzy.

            +++

            - Installation
            - Launch file integration
            - Bridge configuration

        .. grid-item-card:: ros_gz_bridge Message Pairs
            :link: https://github.com/gazebosim/ros_gz/blob/ros2/ros_gz_bridge/README.md
            :class-card: sd-border-secondary

            **Supported Message Pairs**

            Complete list of supported Gazebo-to-ROS 2 message type
            mappings for the bridge.

            +++

            - Sensor messages
            - Geometry messages
            - Navigation messages

        .. grid-item-card:: Gazebo + ROS 2 Launch Examples
            :link: https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_sim_demos
            :class-card: sd-border-secondary

            **ros_gz_sim_demos**

            Example launch files and configurations for common Gazebo +
            ROS 2 use cases.

            +++

            - Diff drive robot
            - Sensor bridges
            - Multi-robot simulation


.. dropdown:: TF2 Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: TF2 Tutorials
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy TF2 Tutorials**

            Step-by-step tutorials covering static broadcasters,
            dynamic broadcasters, listeners, and debugging TF2 trees.

            +++

            - Writing a static broadcaster
            - Writing a dynamic broadcaster
            - Writing a listener
            - Debugging with ``tf2_echo`` and ``view_frames``

        .. grid-item-card:: tf2_ros API Reference
            :link: https://docs.ros.org/en/jazzy/p/tf2_ros/
            :class-card: sd-border-secondary

            **tf2_ros**

            Python and C++ API reference for the TF2 ROS 2 client
            library.

            +++

            - ``Buffer`` and ``TransformListener``
            - ``TransformBroadcaster``
            - ``StaticTransformBroadcaster``

        .. grid-item-card:: REP 105: Coordinate Frames
            :link: https://www.ros.org/reps/rep-0105.html
            :class-card: sd-border-secondary

            **REP 105**

            Standard naming conventions for coordinate frames in
            mobile robots: ``map``, ``odom``, ``base_link``,
            ``base_footprint``.

            +++

            - Frame naming conventions
            - ``map`` vs ``odom`` semantics
            - ``base_link`` orientation

        .. grid-item-card:: REP 103: Units and Coordinate Conventions
            :link: https://www.ros.org/reps/rep-0103.html
            :class-card: sd-border-secondary

            **REP 103**

            Standard units (meters, radians, seconds) and coordinate
            axis conventions (right-hand rule, x-forward, z-up) for
            ROS 2.

            +++

            - SI units
            - Right-hand coordinate frame
            - Quaternion conventions


.. dropdown:: External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Articulated Robotics: Gazebo Sim
            :link: https://articulatedrobotics.xyz/category/ros2-tutorials/
            :class-card: sd-border-secondary

            **Articulated Robotics**

            Video tutorials covering Gazebo simulation setup, robot
            models, and ROS 2 integration from scratch.

            +++

            - Building a robot in Gazebo
            - Sensor simulation
            - Control and navigation

        .. grid-item-card:: The Construct: Gazebo Tutorials
            :link: https://www.theconstructsim.com/
            :class-card: sd-border-secondary

            **The Construct**

            Browser-based simulation environment with structured
            Gazebo + ROS 2 courses.

            +++

            - Interactive exercises
            - No local install required
            - Gazebo-focused curriculum

        .. grid-item-card:: Automatic Addison: TF2 Tutorials
            :link: https://automaticaddison.com/how-to-use-tf2-with-ros-2/
            :class-card: sd-border-secondary

            **Automatic Addison**

            Practical walkthroughs for TF2 in ROS 2, including
            broadcasters, listeners, and visualization.

            +++

            - TF2 broadcaster examples
            - TF2 listener examples
            - RViz visualization


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Anis Koubaa (Ed.)
            :class-card: sd-border-secondary

            **Robot Operating System (ROS): The Complete Reference
            (Vol. 1-7)**

            Relevant chapters cover simulation environments, Gazebo
            integration, and coordinate frame management in ROS and
            ROS 2 applications.

        .. grid-item-card:: Open Robotics
            :class-card: sd-border-secondary

            **Programming Robots with ROS 2**

            Chapters on simulation, TF2, and mobile robot control
            provide detailed background for the concepts in this
            lecture.

        .. grid-item-card:: Siegwart, Nourbakhsh, and Scaramuzza
            :class-card: sd-border-secondary

            **Introduction to Autonomous Mobile Robots (2nd Edition)**

            Chapters 3 and 5 cover mobile robot kinematics (including
            differential drive), coordinate transformations, and
            sensor-based navigation -- the theoretical foundations
            behind the ROS 2 tools used in this lecture.

        .. grid-item-card:: Corke, Peter
            :class-card: sd-border-secondary

            **Robotics, Vision and Control (3rd Edition)**

            Chapter 2 (Representing Position and Orientation) and
            Chapter 4 (Mobile Robot Vehicles) provide the mathematical
            background for transforms, quaternions, and differential
            drive kinematics.
