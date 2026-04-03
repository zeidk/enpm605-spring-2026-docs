References
==========


.. dropdown:: Lecture 13
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L13: Behavior Trees and Project Integration**

        Covers behavior tree fundamentals (tick mechanism, control flow
        vs. execution nodes, BT vs. FSM comparison), core node types
        (Sequence, Fallback/Selector, Decorator, Condition, Action),
        the ``py_trees`` Python library (composites, custom behaviours,
        status values, memory semantics), Blackboard shared data
        storage (read/write access, namespaces, inter-behavior
        communication), ROS 2 integration with ``py_trees_ros``
        (topic subscribers, publishers, action clients, service
        clients), a complete integration demo (lifecycle node
        management, Nav2 goal dispatch, sensor monitoring), and
        BT debugging (visualization, logging, common pitfalls).


.. dropdown:: py_trees Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: py_trees Documentation
            :link: https://py-trees.readthedocs.io/
            :class-card: sd-border-secondary

            **py-trees.readthedocs.io**

            Official documentation for the ``py_trees`` Python
            behavior tree library. Covers composites, behaviours,
            decorators, blackboard, and visualization.

            +++

            - API reference
            - Tutorials and demos
            - Blackboard usage

        .. grid-item-card:: py_trees GitHub Repository
            :link: https://github.com/splintered-reality/py_trees
            :class-card: sd-border-secondary

            **splintered-reality/py_trees**

            Source code, issue tracker, and example programs for
            the ``py_trees`` library.

            +++

            - Source code
            - Examples directory
            - Release notes

        .. grid-item-card:: py_trees_ros Documentation
            :link: https://py-trees-ros.readthedocs.io/
            :class-card: sd-border-secondary

            **py-trees-ros.readthedocs.io**

            Official documentation for the ROS 2 integration layer.
            Covers ROS 2 behavior wrappers, tree manager, and
            visualization tools.

            +++

            - ROS 2 behavior wrappers
            - Tree manager setup
            - ``py-trees-tree-watcher``

        .. grid-item-card:: py_trees_ros GitHub Repository
            :link: https://github.com/splintered-reality/py_trees_ros
            :class-card: sd-border-secondary

            **splintered-reality/py_trees_ros**

            Source code and examples for ``py_trees_ros``, including
            ROS 2 subscriber, publisher, action, and service behaviors.

            +++

            - Source code
            - Launch file examples
            - Integration demos


.. dropdown:: Behavior Tree Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Behavior Trees in Robotics and AI
            :link: https://arxiv.org/abs/1709.00084
            :class-card: sd-border-secondary

            **Colledanchise & Ogren (2018)**

            The foundational textbook on behavior trees for robotics.
            Covers formal definitions, analysis, extensions, and
            comparisons with FSMs.

            +++

            - Formal BT definition
            - BT vs. FSM analysis
            - Safety and liveness proofs

        .. grid-item-card:: A Survey of Behavior Trees in Robotics
            :link: https://doi.org/10.1016/j.robot.2022.104096
            :class-card: sd-border-secondary

            **Iovino et al. (2022)**

            Comprehensive survey covering BT implementations,
            extensions, learning-based BTs, and industry applications.

            +++

            - Implementation patterns
            - Learning and adaptation
            - Industrial use cases

        .. grid-item-card:: BehaviorTree.CPP
            :link: https://www.behaviortree.dev/
            :class-card: sd-border-secondary

            **behaviortree.dev**

            The C++ behavior tree library used by Nav2. Understanding
            its design helps when debugging Nav2 BT configurations.

            +++

            - XML-based tree definitions
            - BT node types
            - Nav2 integration


.. dropdown:: Nav2 BT Integration
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Nav2 Behavior Trees
            :link: https://docs.nav2.org/behavior_trees/index.html
            :class-card: sd-border-secondary

            **docs.nav2.org**

            How Nav2 uses behavior trees to coordinate planning,
            control, and recovery behaviors.

            +++

            - Default BT XML files
            - BT node plugins
            - Custom BT integration

        .. grid-item-card:: Nav2 BT Navigator
            :link: https://docs.nav2.org/configuration/packages/configuring-bt-navigator.html
            :class-card: sd-border-secondary

            **BT Navigator Configuration**

            Configuring the BT Navigator server, loading custom BT
            XML files, and setting tick rates.

            +++

            - BT XML file path
            - Plugin loading
            - Tick rate configuration

        .. grid-item-card:: Writing a New BT Plugin for Nav2
            :link: https://docs.nav2.org/plugin_tutorials/docs/writing_new_bt_plugin.html
            :class-card: sd-border-secondary

            **Nav2 Plugin Tutorial**

            Step-by-step guide to creating custom BT action and
            condition nodes for use in Nav2.

            +++

            - BT plugin interface
            - Registration and loading
            - Testing plugins

        .. grid-item-card:: Nav2 Lifecycle Management
            :link: https://docs.nav2.org/configuration/packages/configuring-lifecycle.html
            :class-card: sd-border-secondary

            **Lifecycle Manager Configuration**

            How Nav2 manages lifecycle transitions for its component
            nodes, and how to integrate with custom lifecycle nodes.

            +++

            - Managed node list
            - Transition sequencing
            - Bond connections


.. dropdown:: External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Articulated Robotics: Behavior Trees
            :link: https://articulatedrobotics.xyz/
            :class-card: sd-border-secondary

            **Articulated Robotics**

            Practical video and written tutorials covering behavior
            trees for ROS 2 robotic applications.

            +++

            - BT fundamentals
            - py_trees integration
            - Navigation examples

        .. grid-item-card:: The Construct: ROS 2 Advanced
            :link: https://www.theconstructsim.com/
            :class-card: sd-border-secondary

            **The Construct**

            Browser-based ROS 2 environment with advanced courses
            covering behavior trees and Nav2 integration.

            +++

            - Interactive exercises
            - Nav2 BT tutorials
            - Integration projects

        .. grid-item-card:: ROS 2 Lifecycle Nodes Tutorial
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Managing-Nodes-Lifecycle.html
            :class-card: sd-border-secondary

            **Managing Nodes with Lifecycles**

            Official ROS 2 tutorial on lifecycle (managed) nodes,
            essential background for BT-driven lifecycle management.

            +++

            - Lifecycle states and transitions
            - Service interfaces
            - Launch integration


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Colledanchise & Ogren
            :class-card: sd-border-secondary

            **Behavior Trees in Robotics and AI: An Introduction**

            The definitive textbook on behavior trees. Covers formal
            semantics, design patterns, safety analysis, and
            comparisons with FSMs, HTNs, and decision trees.

        .. grid-item-card:: Anis Koubaa (Ed.)
            :class-card: sd-border-secondary

            **Robot Operating System (ROS): The Complete Reference
            (Vol. 1-7)**

            Multi-volume series covering ROS and ROS 2 from
            fundamentals through advanced applications. Later volumes
            include chapters on behavior trees and Nav2.

        .. grid-item-card:: Steve Macenski et al.
            :class-card: sd-border-secondary

            **The Marathon 2: A Navigation System**

            Paper describing the Nav2 architecture, including its
            use of behavior trees for navigation coordination,
            recovery behaviors, and task planning.

        .. grid-item-card:: Daniel Faconti
            :class-card: sd-border-secondary

            **BehaviorTree.CPP: A C++ Behavior Tree Library**

            Documentation and design rationale for the C++ BT library
            used in Nav2. Understanding the C++ side helps debug
            Nav2 BT XML configurations and write custom plugins.
