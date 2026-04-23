References
==========


.. dropdown:: Lecture 12
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L12: Namespaces, Remapping, Lifecycle Nodes, and Behavior Trees**

        Covers namespaces (topic isolation, CLI ``__ns``, launch file
        ``namespace`` argument), remapping (node, topic, and parameter
        remapping via CLI and launch files), lifecycle nodes (state
        machine, primary states, transition commands, callbacks,
        ``LifecycleNode``, ``create_lifecycle_publisher``, programmatic
        state changes), and behavior trees (composites, conditions,
        actions, decorators, ``py_trees``, ``py_trees_ros``, tick
        mechanism, terminal debug output).


.. dropdown:: Namespaces and Remapping
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROS 2 Launch: Large Projects
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Launch Tutorial**

            Tutorial on organizing launch files for large projects,
            including namespace usage and node grouping.

        .. grid-item-card:: ROS 2 Design: Topic and Service Names
            :link: https://design.ros2.org/articles/topic_and_service_names.html
            :class-card: sd-border-secondary

            **ROS 2 Design Article**

            Specification of how topic and service names are resolved,
            including namespace prefixing and absolute vs. relative
            names.

        .. grid-item-card:: ROS 2: Node Name Remapping
            :link: https://docs.ros.org/en/jazzy/How-To-Guides/Node-name-remapping.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: How-To Guide**

            How to remap node names at runtime using ``--ros-args``.

        .. grid-item-card:: ROS 2: Node Arguments
            :link: https://docs.ros.org/en/jazzy/Guides/Node-arguments.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Guide**

            Comprehensive guide to all ``--ros-args`` options:
            remapping, parameters, logging configuration.


.. dropdown:: Lifecycle Nodes
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROS 2 Design: Managed Nodes
            :link: https://design.ros2.org/articles/node_lifecycle.html
            :class-card: sd-border-secondary

            **ROS 2 Design Article**

            The original design document for lifecycle (managed) nodes.
            Defines the state machine, transition commands, and error
            handling semantics.

            +++

            - State machine diagram
            - Transition callbacks
            - Error processing

        .. grid-item-card:: ROS 2: Managing a Robot
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Managing-A-Robot-Introduction.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Tutorial**

            Introduction to managing lifecycle nodes using the CLI
            tools ``ros2 lifecycle get`` and ``ros2 lifecycle set``.

            +++

            - CLI state transitions
            - ``ros2 lifecycle`` commands
            - Lifecycle manager concept


.. dropdown:: Behavior Trees
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: py_trees Documentation
            :link: https://py-trees.readthedocs.io/en/devel/
            :class-card: sd-border-secondary

            **py_trees: Behavior Trees in Python**

            Official documentation for the ``py_trees`` library.
            Covers composites, decorators, blackboard, and
            visualization tools.

            +++

            - ``Behaviour`` base class
            - Composites (Sequence, Selector)
            - Decorators (Timeout, Inverter, Retry)

        .. grid-item-card:: py_trees_ros Documentation
            :link: https://py-trees-ros.readthedocs.io/en/latest/
            :class-card: sd-border-secondary

            **py_trees_ros: ROS 2 Integration**

            Wraps ``py_trees`` trees in a ROS 2 node with timer-driven
            ticking, subscriber behaviors, and action client behaviors.

            +++

            - ``BehaviourTree`` class
            - ``tick_tock()`` method
            - Built-in subscriber behaviors

        .. grid-item-card:: Behavior Trees in Robotics and AI
            :link: https://arxiv.org/abs/1709.00084
            :class-card: sd-border-secondary

            **Colledanchise & Ogren (2017)**

            Survey paper covering the theory and practice of behavior
            trees in robotics. Covers composites, decorators, memory,
            reactivity, and comparisons with state machines.

            +++

            - Formal BT definition
            - Tick mechanism
            - BTs vs. FSMs
