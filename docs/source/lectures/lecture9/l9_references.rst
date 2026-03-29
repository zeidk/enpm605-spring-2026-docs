References
==========


.. dropdown:: Lecture 9
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM605 -- L9: Launch Files & Executors**

        Covers Python launch files (anatomy, ``generate_launch_description``,
        two configuration patterns), advanced launch features (including
        other launch files, conditional launching with ``IfCondition``,
        node grouping with ``GroupAction``, and parameterized launch
        arguments), executors (single-threaded vs. multi-threaded, the
        concurrency-vs-parallelism distinction, the Python GIL and its
        impact on ROS 2), and callback groups
        (``MutuallyExclusiveCallbackGroup`` and
        ``ReentrantCallbackGroup`` with execution timelines and
        comparison table).


.. dropdown:: ROS 2 Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Launch Files Tutorials
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Launch**

            Complete tutorial series for Python launch files, from
            basic node startup through substitutions and events.

            +++

            - Creating launch files
            - Passing arguments
            - Using substitutions

        .. grid-item-card:: About Executors
            :link: https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html
            :class-card: sd-border-secondary

            **ROS 2 Executors Concept**

            In-depth conceptual explanation of how executors manage
            thread pools and dispatch callbacks.

            +++

            - Single-threaded executor
            - Multi-threaded executor
            - Callback scheduling model

        .. grid-item-card:: Using Callback Groups
            :link: https://docs.ros.org/en/jazzy/How-To-Guides/Using-callback-groups.html
            :class-card: sd-border-secondary

            **Callback Groups How-To**

            Practical guide to creating and assigning callback groups,
            with examples for both group types.

            +++

            - ``MutuallyExclusiveCallbackGroup``
            - ``ReentrantCallbackGroup``
            - When to use each


.. dropdown:: Launch File API
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: launch Python API
            :link: https://docs.ros.org/en/jazzy/p/launch/
            :class-card: sd-border-secondary

            **launch package reference**

            Full API documentation for ``LaunchDescription``,
            ``DeclareLaunchArgument``, ``IncludeLaunchDescription``,
            ``GroupAction``, and substitution classes.

            +++

            - Actions reference
            - Substitutions reference
            - Conditions reference

        .. grid-item-card:: launch_ros Python API
            :link: https://docs.ros.org/en/jazzy/p/launch_ros/
            :class-card: sd-border-secondary

            **launch_ros package reference**

            API for ``Node``, ``FindPackageShare``, and
            ``PushRosNamespace`` used in ROS 2 launch files.

            +++

            - ``Node`` action
            - ``FindPackageShare`` substitution
            - Namespace management

        .. grid-item-card:: Launch File Formats
            :link: https://docs.ros.org/en/jazzy/How-To-Guides/Launch-file-different-formats.html
            :class-card: sd-border-secondary

            **XML, YAML, and Python**

            Comparison of all three launch file formats with equivalent
            examples, useful as a reference when reading third-party
            packages that use XML or YAML launch files.

            +++

            - Format equivalence table
            - When to use each format
            - Migration notes


.. dropdown:: Python Threading and the GIL
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Python threading module
            :link: https://docs.python.org/3/library/threading.html
            :class-card: sd-border-secondary

            **Python Standard Library: threading**

            Reference for ``Thread``, ``Lock``, ``RLock``, ``Event``,
            and ``Condition`` -- the synchronization primitives used
            when callbacks share mutable state.

            +++

            - ``threading.Lock``
            - Thread lifecycle
            - ``thread.daemon``

        .. grid-item-card:: Python GIL Explained
            :link: https://realpython.com/python-gil/
            :class-card: sd-border-secondary

            **Real Python: The Python GIL**

            Practical explanation of what the GIL is, why it exists,
            and when it is and is not released.

            +++

            - GIL history and rationale
            - Impact on multi-threaded code
            - When GIL is released (I/O, C extensions)

        .. grid-item-card:: Python multiprocessing module
            :link: https://docs.python.org/3/library/multiprocessing.html
            :class-card: sd-border-secondary

            **Python Standard Library: multiprocessing**

            For cases where true Python parallelism is required,
            ``multiprocessing`` bypasses the GIL by using separate
            OS processes instead of threads.

            +++

            - Process vs Thread
            - ``Pool`` for parallel work
            - Shared memory options


.. dropdown:: External Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Articulated Robotics: Launch Files
            :link: https://articulatedrobotics.xyz/category/ros2-tutorials/
            :class-card: sd-border-secondary

            **Articulated Robotics**

            Video and written tutorials for ROS 2 launch files and
            executors with practical robot examples.

            +++

            - Launch file deep dives
            - Executor comparisons

        .. grid-item-card:: The Construct: ROS 2 Executors
            :link: https://www.theconstructsim.com/ros2-for-beginners/
            :class-card: sd-border-secondary

            **The Construct**

            Browser-based interactive environment with guided
            exercises on executors and callback groups.

            +++

            - Interactive executor exercises
            - Callback group demos
            - No local install required


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Anis Koubaa (Ed.)
            :class-card: sd-border-secondary

            **Robot Operating System (ROS): The Complete Reference
            (Vol. 1-7)**

            Relevant chapters cover ROS 2 launch systems and the
            executor concurrency model.

        .. grid-item-card:: Open Robotics
            :class-card: sd-border-secondary

            **Programming Robots with ROS 2**

            Chapters on launch files and the threading model provide
            applied coverage of this lecture's topics.

        .. grid-item-card:: Silberschatz, Galvin, and Gagne
            :class-card: sd-border-secondary

            **Operating System Concepts (10th Edition)**

            Chapter 4 (Threads) provides the OS-level background for
            understanding the multi-threaded executor, thread pools,
            scheduling, and the synchronization primitives that prevent
            race conditions.

        .. grid-item-card:: David Beazley
            :class-card: sd-border-secondary

            **Python Concurrency from the Ground Up (PyCon Talk)**

            Classic conference talk (available on YouTube) explaining
            the GIL, threads, asyncio, and multiprocessing in CPython
            with clear timing diagrams that map directly to the
            executor timelines covered in this lecture.
