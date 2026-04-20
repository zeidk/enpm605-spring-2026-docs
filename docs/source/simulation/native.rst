====================================================
Native Installation
====================================================

This page walks you through installing **Gazebo Harmonic** and building
the ROSbot simulation packages directly on your system -- no Docker
required.

.. warning::

   Gazebo Harmonic and Gazebo Classic **cannot coexist** on the same
   system. If you need Gazebo Classic for another course, use the
   :doc:`docker` method instead.

Prerequisites
-------------

- **Ubuntu 24.04** with **ROS 2 Jazzy** already installed
- ``colcon`` and ``vcs`` build tools:

  .. code-block:: console

     sudo apt install -y python3-colcon-common-extensions python3-vcstool


.. _native-step1:

Step 1: Install Gazebo Harmonic
====================================================

.. dropdown:: Install Gazebo Harmonic from packages
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

   **Add the Gazebo package repository:**

   .. code-block:: console

      sudo curl https://packages.osrfoundation.org/gazebo.gpg \
          --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg

   .. code-block:: console

      echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
          http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
          | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

   **Install Gazebo Harmonic:**

   .. code-block:: console

      sudo apt update
      sudo apt install -y gz-harmonic

   **Verify the installation:**

   .. code-block:: console

      gz sim --version

   You should see the Gazebo Harmonic version printed.

   **Install the ROS 2--Gazebo bridge packages:**

   .. code-block:: console

      sudo apt install -y ros-jazzy-ros-gz


.. _native-step2:

Step 2: Create and Build the Workspace
====================================================

.. dropdown:: Clone the course workspace
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

   The course repository already bundles the ROSbot simulation packages
   (``husarion_components_description``, ``husarion_controllers``,
   ``husarion_gz_worlds``, and ``rosbot_ros``) under ``lecture11/`` --
   there is no need to create a separate ``rosbot_ws`` or to pull them
   in manually with ``vcs import``.

   Clone the course repository into your workspace:

   .. code-block:: console

      mkdir -p ~/enpm605_ws
      cd ~/enpm605_ws
      git clone https://github.com/zeidk/enpm605-spring-2026-ros.git src


.. dropdown:: Install dependencies and build
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

   Install all required ROS 2 dependencies:

   .. code-block:: console

      source /opt/ros/jazzy/setup.bash
      rosdep update
      rosdep install --from-paths src --ignore-src -y --skip-keys "micro_ros_agent"

   .. warning::

      You **must** source ``/opt/ros/jazzy/setup.bash`` **before**
      building. If you skip this step, the workspace overlay will not
      be able to find system packages like ``ros_gz_bridge``, and the
      simulation launch will fail.

   Build the workspace up to the Lecture 11 meta-package (this pulls
   in every ROSbot simulation package and the lecture demos in the
   correct order):

   .. code-block:: console

      colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release --packages-up-to lecture11_meta

   - ``--symlink-install`` creates symbolic links instead of copying
     files, so changes to Python scripts and launch files take effect
     without rebuilding.
   - ``-DCMAKE_BUILD_TYPE=Release`` enables compiler optimizations.
   - ``--packages-up-to lecture11_meta`` builds ``lecture11_meta`` and
     all of its transitive dependencies (the husarion and rosbot
     packages, plus ``frame_demo`` and ``robot_control_demo``).

   The build may take several minutes on the first run.

   **Source the workspace:**

   .. code-block:: console

      source install/setup.bash

   .. tip::

      Add the following line to your ``~/.bashrc`` so the workspace is
      sourced automatically in every new terminal:

      .. code-block:: bash

         source ~/enpm605_ws/install/setup.bash


.. _native-step3:

Step 3: Launch the Simulation
====================================================

With the workspace sourced, launch the simulation using the shared
instructions on the :ref:`simulation-launch` page.


Troubleshooting
====================================================

.. card::

   .. dropdown:: ``gz sim`` command not found
      :color: warning
      :icon: cpu
      :animate: fade-in-slide-down

      Gazebo Harmonic is not installed or not on your ``PATH``.

      - Verify the installation with ``apt list --installed | grep gz-harmonic``.
      - Ensure the OSRF repository was added correctly (see Step 1).
      - Re-run ``sudo apt update && sudo apt install -y gz-harmonic``.


   .. dropdown:: ``rosdep install`` fails with missing keys
      :color: warning
      :icon: cpu
      :animate: fade-in-slide-down

      Some dependencies may not be available in the default rosdep
      sources.

      - Ensure you ran ``rosdep update`` before ``rosdep install``.
      - Try adding the ``--skip-keys`` flag for known missing keys:

      .. code-block:: console

         rosdep install --from-paths src --ignore-src -y --skip-keys "gz-harmonic micro_ros_agent"


   .. dropdown:: ``colcon build`` fails with CMake errors
      :color: warning
      :icon: cpu
      :animate: fade-in-slide-down

      - Make sure you sourced ROS 2 before building:

      .. code-block:: console

         source /opt/ros/jazzy/setup.bash

      - Ensure all dependencies were installed with ``rosdep install``.
      - Delete the ``build/``, ``install/``, and ``log/`` directories
        and rebuild:

      .. code-block:: console

         rm -rf build/ install/ log/
         colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release --packages-up-to lecture11_meta


   .. dropdown:: Gazebo crashes or shows a black screen
      :color: warning
      :icon: cpu
      :animate: fade-in-slide-down

      - Check if your GPU drivers are working:

      .. code-block:: console

         glxinfo | grep "OpenGL renderer"

      If the renderer shows ``llvmpipe`` or ``software``, your GPU
      drivers are not properly installed.
      - For NVIDIA GPUs, ensure the proprietary driver is installed:

      .. code-block:: console

         sudo ubuntu-drivers install

      - Try running Gazebo with software rendering as a workaround:

      .. code-block:: console

         export LIBGL_ALWAYS_SOFTWARE=1
         ros2 launch rosbot_gazebo simulation.yaml


   .. dropdown:: ``package 'rosbot_gazebo' not found``
      :color: warning
      :icon: cpu
      :animate: fade-in-slide-down

      The workspace is not sourced.

      - Run ``source ~/enpm605_ws/install/setup.bash`` in your terminal.
      - Verify the package exists:

      .. code-block:: console

         ros2 pkg prefix rosbot_gazebo
