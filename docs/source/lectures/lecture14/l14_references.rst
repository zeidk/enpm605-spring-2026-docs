References
==========


.. dropdown:: Lecture 14
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L14: Lifecycle Nodes & ROS 2 Bags**

        Covers lifecycle nodes (state machine: Unconfigured /
        Inactive / Active / Finalized, transition commands and
        callbacks, ``LifecycleNode``,
        ``create_lifecycle_publisher``, ``TransitionCallbackReturn``
        with ``SUCCESS`` / ``FAILURE`` / ``ERROR``, CLI-driven
        transitions via ``ros2 lifecycle set``, programmatic
        transitions through the ``change_state`` service), ROS 2
        bags (storage backends -- SQLite3 vs.\ MCAP, recording with
        ``ros2 bag record``, useful flags, recording a Nav2
        navigation run, inspecting bags with ``ros2 bag info``,
        replaying with ``ros2 bag play`` and useful flags such as
        ``--rate``, ``--loop``, ``--remap``, ``--clock``), and
        Foxglove Studio (multi-panel layouts -- 3D, Plot, Raw
        Messages -- and importing / exporting layout files).


.. dropdown:: Lifecycle Nodes
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROS 2 Design: Managed Nodes
            :link: https://design.ros2.org/articles/node_lifecycle.html
            :class-card: sd-border-secondary

            **ROS 2 Design Article**

            Authoritative design document describing the lifecycle
            (managed) node concept, primary states, transitions,
            and the rationale for separating construction from
            activation.

            +++

            - Primary states
            - Transition commands
            - Service interfaces

        .. grid-item-card:: rclpy Lifecycle Examples
            :link: https://github.com/ros2/rclpy/tree/jazzy/rclpy
            :class-card: sd-border-secondary

            **rclpy Source (Jazzy)**

            Source for ``rclpy_lifecycle``, including
            ``LifecycleNode``, lifecycle publishers, and example
            patterns for transition callbacks.

            +++

            - ``LifecycleNode``
            - ``create_lifecycle_publisher``
            - ``TransitionCallbackReturn``

        .. grid-item-card:: lifecycle_msgs
            :link: https://docs.ros.org/en/jazzy/p/lifecycle_msgs/
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: lifecycle_msgs**

            Message and service definitions used to drive lifecycle
            transitions: ``State``, ``Transition``,
            ``ChangeState``, ``GetState``.

            +++

            - ``ChangeState`` service
            - ``Transition`` message
            - ``State`` message

        .. grid-item-card:: Nav2 Lifecycle Manager
            :link: https://docs.nav2.org/configuration/packages/configuring-lifecycle.html
            :class-card: sd-border-secondary

            **Nav2 Documentation**

            Reference for the Nav2 ``lifecycle_manager`` that
            sequences ``map_server``, ``amcl``, planners,
            controllers, and ``bt_navigator`` through their
            transitions.

            +++

            - Bringup ordering
            - Bond timeout
            - Auto-start


.. dropdown:: ROS 2 Bags
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Recording and Playing Back Data
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Tutorial**

            Step-by-step walk-through for ``ros2 bag record``,
            ``ros2 bag play``, and ``ros2 bag info``, including
            common flags.

            +++

            - Recording specific topics
            - Replaying bags
            - Inspecting metadata

        .. grid-item-card:: rosbag2 on GitHub
            :link: https://github.com/ros2/rosbag2
            :class-card: sd-border-secondary

            **rosbag2 Source**

            Source repository for ``rosbag2``: storage backends,
            CLI plugins, and the C++ / Python APIs for reading and
            writing bags programmatically.

            +++

            - Storage plugins
            - ``rosbag2_py`` API
            - CLI extensions

        .. grid-item-card:: MCAP File Format
            :link: https://mcap.dev/
            :class-card: sd-border-secondary

            **MCAP Documentation**

            Specification, design rationale, and tooling for the
            MCAP file format used by the recommended ROS 2 storage
            backend.

            +++

            - Format specification
            - ``mcap`` CLI
            - Language libraries

        .. grid-item-card:: rosbag2 Storage MCAP Plugin
            :link: https://github.com/ros2/rosbag2/tree/jazzy/rosbag2_storage_mcap
            :class-card: sd-border-secondary

            **rosbag2_storage_mcap (Jazzy)**

            Source for the MCAP storage plugin that ships in the
            ``ros-jazzy-rosbag2-storage-mcap`` Debian package.


.. dropdown:: Foxglove Studio
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Foxglove Website
            :link: https://foxglove.dev/
            :class-card: sd-border-secondary

            **Foxglove**

            Project home page for Foxglove Studio: features,
            downloads, and learning resources.

        .. grid-item-card:: Foxglove Documentation
            :link: https://docs.foxglove.dev/docs
            :class-card: sd-border-secondary

            **Foxglove Docs**

            Top-level documentation: getting started, panels,
            layouts, message types, and the WebSocket bridge.

            +++

            - Panels
            - Layouts
            - Live connection

        .. grid-item-card:: Panel Reference
            :link: https://docs.foxglove.dev/docs/visualization/panels/introduction
            :class-card: sd-border-secondary

            **Foxglove: Panels**

            Reference for every panel (3D, Plot, Image, Raw
            Messages, Diagnostics, Teleop, ...) and the message
            types each one consumes.

        .. grid-item-card:: Foxglove Desktop Downloads
            :link: https://foxglove.dev/download
            :class-card: sd-border-secondary

            **Foxglove**

            Desktop installers for Linux (Debian / AppImage),
            macOS, and Windows.

        .. grid-item-card:: Foxglove Web App
            :link: https://app.foxglove.dev/
            :class-card: sd-border-secondary

            **Foxglove**

            Browser version of Studio. Bag files chosen here are
            read locally; nothing is uploaded.

        .. grid-item-card:: Pricing and Academic Access
            :link: https://foxglove.dev/pricing
            :class-card: sd-border-secondary

            **Foxglove**

            Pricing tiers and information about free academic /
            open-source access.

