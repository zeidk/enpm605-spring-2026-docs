References
==========


.. dropdown:: Lecture 10
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L10: Parameters, Custom Interfaces, Services & Actions**

        Covers ROS 2 parameters (declaration, reading, descriptors with
        range constraints, runtime parameter callbacks, YAML parameter
        files, CLI tools), custom interface definitions (``.msg``,
        ``.srv``, ``.action`` files, CMake build configuration, interface
        verification), services (request/response model, server
        implementation, asynchronous and synchronous clients, deadlock
        avoidance), and actions (goal/feedback/result model, server with
        cancellation support, asynchronous client with feedback
        monitoring, CLI tools, and a decision guide for choosing the
        right communication pattern).


.. dropdown:: ROS 2 Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Using Parameters (Python)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Parameters**

            Tutorial for declaring, reading, and using parameters in a
            Python class-based node.

            +++

            - ``declare_parameter()``
            - ``get_parameter()``
            - Parameter callbacks

        .. grid-item-card:: About Parameters
            :link: https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html
            :class-card: sd-border-secondary

            **ROS 2 Parameter Concepts**

            Conceptual overview of parameters: types, descriptors,
            constraints, and the parameter service API.

            +++

            - Parameter types
            - Parameter descriptors
            - Node-local storage

        .. grid-item-card:: Writing a Service and Client (Python)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Services**

            Step-by-step tutorial for creating a service server and
            client in Python.

            +++

            - ``create_service()``
            - ``create_client()``
            - ``call_async()``

        .. grid-item-card:: Understanding Services
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html
            :class-card: sd-border-secondary

            **ROS 2 Service Concepts**

            CLI-based introduction to services, including listing,
            calling, and inspecting service types.

            +++

            - ``ros2 service list``
            - ``ros2 service call``
            - Service vs. topic comparison

        .. grid-item-card:: Writing an Action Server and Client (Python)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Actions**

            Complete tutorial covering action server implementation,
            client usage, feedback, and cancellation.

            +++

            - ``ActionServer``
            - ``ActionClient``
            - Goal handling and cancellation

        .. grid-item-card:: Understanding Actions
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html
            :class-card: sd-border-secondary

            **ROS 2 Action Concepts**

            CLI-based introduction to the action model, goal states,
            feedback topics, and introspection commands.

            +++

            - ``ros2 action send_goal``
            - ``ros2 action info``
            - Goal lifecycle

        .. grid-item-card:: Creating Custom Interfaces
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Custom Interfaces**

            Tutorial for creating ``.msg``, ``.srv``, and ``.action``
            files with CMake and ``rosidl_generate_interfaces``.

            +++

            - Interface package structure
            - ``rosidl_generate_interfaces``
            - ``ros2 interface show``

        .. grid-item-card:: Implementing Custom Interfaces
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Single-Package-Define-And-Use-Interface.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Using Custom Interfaces**

            Advanced guide for using custom interfaces defined in the
            same package or a separate package.

            +++

            - Cross-package interface dependencies
            - ``package.xml`` configuration
            - Import patterns


.. dropdown:: External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Articulated Robotics: ROS 2 Services
            :link: https://articulatedrobotics.xyz/category/ros2-tutorials/
            :class-card: sd-border-secondary

            **Articulated Robotics**

            Video tutorials covering ROS 2 services and actions with
            practical robot examples and demonstrations.

            +++

            - Service server/client walkthrough
            - Action server/client walkthrough
            - Real robot demos

        .. grid-item-card:: The Construct: ROS 2 Services & Actions
            :link: https://www.theconstructsim.com/ros2-for-beginners/
            :class-card: sd-border-secondary

            **The Construct**

            Browser-based interactive environment with guided
            exercises on services, actions, and custom interfaces.

            +++

            - Interactive service exercises
            - Action server/client labs
            - No local install required

        .. grid-item-card:: Robotics Back-End: ROS 2 Tutorials
            :link: https://roboticsbackend.com/category/ros2/
            :class-card: sd-border-secondary

            **Robotics Back-End**

            Practical blog posts with complete code examples for
            services, actions, parameters, and custom interfaces.

            +++

            - Parameter YAML files
            - Service patterns
            - Action patterns


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Anis Koubaa (Ed.)
            :class-card: sd-border-secondary

            **Robot Operating System (ROS): The Complete Reference
            (Vol. 1-7)**

            Relevant chapters cover ROS 2 services, actions, and the
            interface generation pipeline.

        .. grid-item-card:: Open Robotics
            :class-card: sd-border-secondary

            **Programming Robots with ROS 2**

            Chapters on services, actions, and custom interfaces
            provide applied coverage of this lecture's communication
            patterns.

        .. grid-item-card:: Joseph, Cacace
            :class-card: sd-border-secondary

            **Mastering ROS for Robotics Programming (3rd Edition)**

            Covers service/action design patterns, custom interface
            packages, and parameter management in production ROS 2
            systems.

        .. grid-item-card:: ROS 2 Design Articles
            :link: https://design.ros2.org/
            :class-card: sd-border-secondary

            **ROS 2 Design**

            Official design documents explaining the rationale behind
            the action protocol, parameter API, and interface
            definition language (IDL) used in ROS 2.

            +++

            - Action design article
            - Parameter design article
            - IDL mapping specification
