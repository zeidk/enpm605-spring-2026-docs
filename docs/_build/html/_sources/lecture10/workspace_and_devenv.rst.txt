====================================================
Workspace
====================================================

ROS 2 Workspaces
----------------

A ROS 2 workspace is a directory that contains your source packages and the build artifacts.



.. grid:: 2
    :gutter: 3

    .. grid-item-card:: 📂 Directory Layout
        :class-card: sd-border-secondary

        .. code-block:: text

           ros2_ws/
             src/
               my_package/
               another_package/
             build/
             install/
             log/

    .. grid-item:: 
    
        **Key Directories:**

        * **src/**: Source code. This is where you clone/create packages.
        * **build/**: Temporary intermediate files. Rarely edited directly.
        * **install/**: Final artifacts and setup files. Source ``setup.bash`` here to use your code.

The colcon Build Tool
---------------------

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Workflow**
    
    1.  **Build:** Run from the workspace root.
    2.  **Source:** Extend the environment to find new packages.

    .. code-block:: bash
    
       cd ~/ros2_ws
       colcon build
       source ~/ros2_ws/install/setup.bash

Overlaying Workspaces
---------------------



.. tab-set::

    .. tab-item:: Concept

        ROS 2 supports an **overlay** mechanism:
        
        * **Underlay:** The base installation (e.g., ``/opt/ros/humble``).
        * **Overlay:** Your development workspace (e.g., ``~/ros2_ws``).
        
        This allows you to override system packages with your own forks while keeping the system intact.

    .. tab-item:: Sourcing Order

        ROS 2 searches the overlay first, then falls back to the underlay.

        .. code-block:: bash
        
           source /opt/ros/humble/setup.bash    # Underlay
           source ~/ros2_ws/install/setup.bash  # Overlay