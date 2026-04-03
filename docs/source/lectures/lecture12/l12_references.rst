References
==========


.. dropdown:: Lecture 12
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L12: Nav2 and Lifecycle Nodes**

        Covers lifecycle (managed) nodes and the ROS 2 lifecycle state
        machine (Unconfigured, Inactive, Active, Finalized), transition
        callbacks (``on_configure``, ``on_activate``, ``on_deactivate``,
        ``on_cleanup``, ``on_shutdown``), lifecycle publishers, lifecycle
        CLI tools (``ros2 lifecycle``), bond connections, Nav2
        architecture (Planner Server, Controller Server, Behavior
        Server, BT Navigator, Map Server, AMCL, Costmap 2D), Nav2
        parameter configuration (planners, controllers, costmap layers,
        AMCL), launching Nav2 with ``nav2_bringup``, the
        ``BasicNavigator`` API (``goToPose``, ``followWaypoints``,
        ``waitUntilNav2Active``), and map creation with SLAM Toolbox.


.. dropdown:: Nav2 Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Nav2 Official Documentation
            :link: https://docs.nav2.org/
            :class-card: sd-border-secondary

            **docs.nav2.org**

            The official Navigation2 documentation hub.  Architecture
            overview, configuration guides, plugin descriptions, and
            tutorials.

            +++

            - Getting started guide
            - Configuration guide
            - Plugin descriptions

        .. grid-item-card:: Nav2 Tutorials
            :link: https://docs.nav2.org/tutorials/index.html
            :class-card: sd-border-secondary

            **Nav2 Tutorials**

            Step-by-step tutorials for setting up Nav2, navigating in
            simulation, and writing custom plugins.

            +++

            - First-time robot setup
            - Navigation in simulation
            - Custom plugin development

        .. grid-item-card:: nav2_simple_commander API
            :link: https://docs.nav2.org/commander_api/index.html
            :class-card: sd-border-secondary

            **BasicNavigator API**

            API reference for the ``BasicNavigator`` Python class used
            to send goals, follow waypoints, and manage navigation
            programmatically.

            +++

            - ``goToPose`` and ``goThroughPoses``
            - ``followWaypoints``
            - ``waitUntilNav2Active``

        .. grid-item-card:: Nav2 Configuration Guide
            :link: https://docs.nav2.org/configuration/index.html
            :class-card: sd-border-secondary

            **Configuration Reference**

            Complete reference for all Nav2 parameters organized by
            server and plugin.

            +++

            - Planner server parameters
            - Controller server parameters
            - Costmap layer parameters


.. dropdown:: Lifecycle Node Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROS 2 Managed Nodes Design
            :link: https://design.ros2.org/articles/node_lifecycle.html
            :class-card: sd-border-secondary

            **ROS 2 Design: Managed Nodes**

            The original design article describing the lifecycle node
            state machine, transition callbacks, and rationale for
            managed nodes in ROS 2.

            +++

            - State machine specification
            - Transition callback semantics
            - Design rationale

        .. grid-item-card:: rclpy Lifecycle API
            :link: https://docs.ros.org/en/jazzy/p/rclpy/rclpy.lifecycle.html
            :class-card: sd-border-secondary

            **rclpy.lifecycle**

            Python API reference for ``LifecycleNode``,
            ``LifecyclePublisher``, ``TransitionCallbackReturn``, and
            related classes.

            +++

            - ``LifecycleNode`` class
            - ``create_lifecycle_publisher``
            - Transition callbacks

        .. grid-item-card:: Lifecycle Node Tutorial
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Managing-Nodes-Lifecycle.html
            :class-card: sd-border-secondary

            **Managing Nodes with Lifecycle**

            Official ROS 2 tutorial on implementing and managing
            lifecycle nodes from the command line.

            +++

            - Implementing lifecycle callbacks
            - Using ``ros2 lifecycle`` CLI
            - Lifecycle manager patterns


.. dropdown:: SLAM and Mapping
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: SLAM Toolbox Documentation
            :link: https://github.com/SteveMacenski/slam_toolbox
            :class-card: sd-border-secondary

            **slam_toolbox**

            The primary SLAM package for ROS 2.  Supports online/offline
            synchronous and asynchronous SLAM modes.

            +++

            - Online async SLAM
            - Serialization and deserialization
            - Localization mode

        .. grid-item-card:: Nav2 Map Server
            :link: https://docs.nav2.org/configuration/packages/configuring-map-server.html
            :class-card: sd-border-secondary

            **Map Server Configuration**

            Configuration reference for the Nav2 map server, including
            map loading, saving, and YAML format specification.

            +++

            - ``map_saver_cli`` usage
            - Map YAML format
            - Map server parameters


.. dropdown:: External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Articulated Robotics: Nav2
            :link: https://articulatedrobotics.xyz/category/navigation/
            :class-card: sd-border-secondary

            **Articulated Robotics**

            Video tutorials covering Nav2 setup, SLAM mapping, and
            autonomous navigation with a simulated robot.

            +++

            - SLAM mapping walkthrough
            - Nav2 parameter tuning
            - Navigation in Gazebo

        .. grid-item-card:: The Construct: Nav2 Course
            :link: https://www.theconstructsim.com/
            :class-card: sd-border-secondary

            **The Construct**

            Browser-based ROS 2 environment with guided Nav2 courses
            from basic setup through advanced configuration.

            +++

            - Interactive Nav2 exercises
            - No local install required
            - Step-by-step guidance

        .. grid-item-card:: Robotics Backend: Nav2 Tutorials
            :link: https://roboticsbackend.com/
            :class-card: sd-border-secondary

            **Robotics Backend**

            Written tutorials on Nav2, lifecycle nodes, and ROS 2
            navigation concepts with practical examples.

            +++

            - Lifecycle node examples
            - Nav2 launch file walkthrough
            - Troubleshooting guides


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Steve Macenski et al.
            :class-card: sd-border-secondary

            **The Marathon 2: A Navigation System (IROS 2020)**

            The research paper describing the Nav2 architecture, design
            decisions, and performance evaluation.  Essential reading
            for understanding why Nav2 is structured the way it is.

        .. grid-item-card:: Anis Koubaa (Ed.)
            :class-card: sd-border-secondary

            **Robot Operating System (ROS): The Complete Reference
            (Vol. 1-7)**

            Multi-volume series covering ROS and ROS 2.  Relevant
            chapters cover navigation, SLAM, lifecycle management,
            and behavior trees.

        .. grid-item-card:: Sebastian Thrun et al.
            :class-card: sd-border-secondary

            **Probabilistic Robotics**

            The definitive reference for the probabilistic foundations
            underlying AMCL (particle filters), SLAM, and motion
            planning.  Chapters 4 (particle filters) and 7 (mobile
            robot localization) are directly relevant.

        .. grid-item-card:: Steven M. LaValle
            :class-card: sd-border-secondary

            **Planning Algorithms**

            Comprehensive reference for path planning algorithms
            including A*, Dijkstra, and sampling-based planners.
            Available free online at planning.cs.uiuc.edu.
