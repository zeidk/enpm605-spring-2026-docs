References
==========


.. dropdown:: Lecture 13
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L13: Mapping and Navigation with Nav2**

        Covers map representations (metric, topological, semantic),
        occupancy grids (resolution, origin, free / occupied /
        unknown cell states, Bayesian / log-odds updates from LiDAR),
        the ``map`` frame and the REP 105 chain (``world``, ``map``,
        ``odom``, ``base_link``), SLAM with ``slam_toolbox`` (scan
        matching, pose graph, loop closure, key parameters,
        online-async mapping), map saving and loading
        (``map_saver_cli``, ``map_server``, ``.pgm`` / ``.yaml``
        format), localization with AMCL (particle filter,
        predict/update/resample, initial pose), Nav2 stack (global
        and local costmaps, layers, inflation, footprint, NavFn /
        Smac global planners, DWB / Regulated Pure Pursuit local
        controllers, behavior tree and recovery behaviors), and the
        ``NavigateToPose`` action API (goal / feedback / result,
        sending goals from RViz2, ``nav2_simple_commander`` /
        ``BasicNavigator`` Python API).


.. dropdown:: Mapping and SLAM
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: nav_msgs/OccupancyGrid
            :link: https://docs.ros.org/en/api/nav_msgs/html/msg/OccupancyGrid.html
            :class-card: sd-border-secondary

            **ROS Message Definition**

            The standard occupancy grid message used throughout ROS
            and Nav2: header, ``MapMetaData`` (resolution, width,
            height, origin), and the cell data array.

            +++

            - Cell encoding (free / occupied / unknown)
            - ``MapMetaData``
            - ``geometry_msgs/Pose`` origin

        .. grid-item-card:: REP 105: Coordinate Frames
            :link: https://www.ros.org/reps/rep-0105.html
            :class-card: sd-border-secondary

            **ROS Enhancement Proposal**

            Defines the standard coordinate frames for mobile
            platforms: ``world``, ``map``, ``odom``, ``base_link``,
            and ``base_footprint``, including jump vs. drift
            semantics.

            +++

            - Frame naming conventions
            - Parent-child relationships
            - ``map`` -> ``odom`` correction

        .. grid-item-card:: Nav2 + slam_toolbox Tutorial
            :link: https://docs.nav2.org/tutorials/docs/navigation2_with_slam.html
            :class-card: sd-border-secondary

            **Nav2 Documentation**

            Walk-through for using ``slam_toolbox`` to build a map
            and feed it into Nav2 for navigation.

            +++

            - Online async SLAM
            - Map saving
            - Switching to AMCL

        .. grid-item-card:: slam_toolbox Repository
            :link: https://github.com/SteveMacenski/slam_toolbox
            :class-card: sd-border-secondary

            **Steve Macenski's slam_toolbox**

            Source, parameter reference, and usage notes for the
            graph-based 2D SLAM library used in this lecture.

            +++

            - Pose graph
            - Loop closure
            - Online async mode

        .. grid-item-card:: slam_toolbox API
            :link: https://docs.ros.org/en/jazzy/p/slam_toolbox/
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: slam_toolbox**

            Auto-generated API and parameter reference for the
            ``slam_toolbox`` package as shipped with Jazzy.

            +++

            - Parameters
            - Topics
            - Services


.. dropdown:: Localization (AMCL)
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Nav2: Configuring AMCL
            :link: https://docs.nav2.org/configuration/packages/configuring-amcl.html
            :class-card: sd-border-secondary

            **Nav2 Documentation**

            Full parameter reference for ``nav2_amcl``, including
            motion model, sensor model, and adaptive resampling
            parameters.

            +++

            - ``min_particles`` / ``max_particles``
            - ``laser_max_range``
            - ``set_initial_pose``

        .. grid-item-card:: nav2_amcl
            :link: https://docs.ros.org/en/jazzy/p/nav2_amcl/
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: nav2_amcl**

            API reference for the AMCL implementation that ships
            with Nav2 on Jazzy.

            +++

            - Particle filter
            - Sensor models
            - Topic interface


.. dropdown:: Nav2 Stack
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Nav2 Documentation
            :link: https://docs.nav2.org/index.html
            :class-card: sd-border-secondary

            **Nav2: Top-level Docs**

            Entry point for the Nav2 navigation stack: getting
            started, configuration, behavior trees, plugins, and
            tutorials.

        .. grid-item-card:: Nav2 Concepts
            :link: https://docs.nav2.org/concepts/index.html
            :class-card: sd-border-secondary

            **Nav2: Concepts Overview**

            Conceptual overview of the navigation stack: planners,
            controllers, costmaps, recoveries, and the behavior
            tree navigator.

            +++

            - Costmap layers
            - Planner / controller plugins
            - Behavior tree

        .. grid-item-card:: Configuring Costmaps
            :link: https://docs.nav2.org/configuration/packages/configuring-costmaps.html
            :class-card: sd-border-secondary

            **Nav2 Configuration**

            Parameter reference for the global and local costmaps,
            including the static, obstacle, voxel, and inflation
            layers.

            +++

            - Layer plugins
            - ``inflation_radius``
            - ``cost_scaling_factor``

        .. grid-item-card:: NavFn Planner
            :link: https://docs.nav2.org/configuration/packages/configuring-navfn.html
            :class-card: sd-border-secondary

            **Nav2 Configuration**

            Configuration of the classical Dijkstra/A* grid planner.
            Fast and simple, ignores kinematic constraints.

        .. grid-item-card:: Smac Planner
            :link: https://docs.nav2.org/configuration/packages/configuring-smac-planner.html
            :class-card: sd-border-secondary

            **Nav2 Configuration**

            Configuration of the Smac family of planners (Hybrid
            A*, lattice, Theta*) for kinematically constrained
            planning.

        .. grid-item-card:: DWB Controller
            :link: https://docs.nav2.org/configuration/packages/configuring-dwb-controller.html
            :class-card: sd-border-secondary

            **Nav2 Configuration**

            Configuration of the Dynamic Window-based DWB local
            controller, including critic plugins and trajectory
            scoring.

        .. grid-item-card:: Regulated Pure Pursuit
            :link: https://docs.nav2.org/configuration/packages/configuring-regulated-pp.html
            :class-card: sd-border-secondary

            **Nav2 Configuration**

            Configuration of the Regulated Pure Pursuit controller,
            which slows the robot near obstacles and tight curves.

        .. grid-item-card:: Nav2 Behavior Trees
            :link: https://docs.nav2.org/behavior_trees/index.html
            :class-card: sd-border-secondary

            **Nav2 Documentation**

            Reference for the behavior tree XML files that
            orchestrate planning, control, and recovery in Nav2.

            +++

            - ``navigate_to_pose_w_replanning_and_recovery.xml``
            - Custom BT plugins
            - Recovery actions

        .. grid-item-card:: BehaviorTree.CPP
            :link: https://www.behaviortree.dev/
            :class-card: sd-border-secondary

            **Behavior Tree Library**

            Documentation for the C++ behavior tree engine that Nav2
            uses to execute its navigation BTs.


.. dropdown:: NavigateToPose API
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Simple Commander API
            :link: https://docs.nav2.org/commander_api/index.html
            :class-card: sd-border-secondary

            **Nav2: nav2_simple_commander**

            Python convenience API (``BasicNavigator``) wrapping
            ``NavigateToPose`` and the waypoint follower.

            +++

            - ``setInitialPose``
            - ``goToPose``
            - ``followWaypoints``

        .. grid-item-card:: nav2_simple_commander Source
            :link: https://github.com/ros-navigation/navigation2/tree/main/nav2_simple_commander
            :class-card: sd-border-secondary

            **GitHub Source**

            The source for ``BasicNavigator`` and friends, useful
            for understanding what the Python wrapper does under the
            hood.

        .. grid-item-card:: NavigateToPose Interface
            :link: https://docs.ros.org/en/jazzy/p/nav2_msgs/interfaces/action/NavigateToPose.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: nav2_msgs**

            The ``NavigateToPose`` action definition: goal pose,
            feedback fields (current pose, distance remaining,
            recoveries), and the empty result.


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Robotics, Vision and Control (Corke)
            :link: https://link.springer.com/book/10.1007/978-3-031-07262-8
            :class-card: sd-border-secondary

            **Textbook: Chapter 14**

            Comprehensive treatment of mobile robot localization
            and mapping, including occupancy grids, particle
            filters, and SLAM.

        .. grid-item-card:: Modern Robotics (Lynch & Park)
            :link: http://hades.mech.northwestern.edu/index.php/Modern_Robotics
            :class-card: sd-border-secondary

            **Textbook: Chapter 13**

            Open-access textbook chapter on wheeled mobile robots
            covering kinematics, odometry, and motion planning.
