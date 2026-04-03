====================================================
Simulation
====================================================

Overview
--------

This page provides instructions for setting up the simulation
environment used in this course. The entire ROS 2 Jazzy + Gazebo
Harmonic stack runs inside a **Docker container**, which avoids
conflicts with other ROS 2 or Gazebo Classic installations on your host
machine.

The pre-built Docker image includes:

- **ROS 2 Jazzy** desktop installation
- **Gazebo Harmonic** simulator
- **Husarion ROSbot** simulation packages (robot model with LiDAR,
  camera, and IMU sensors)

.. note::

   These instructions are for **simulation only**. No physical robot
   hardware is required.

.. warning::

   **Why Docker?** Gazebo Harmonic and Gazebo Classic cannot coexist on
   the same system -- they share library names and the ``gazebo``
   command, leading to symbol collisions. If you need Gazebo Classic for
   another course, running Harmonic inside Docker keeps both
   installations isolated.


.. _simulation-docker:

Step 1: Install Docker Engine
====================================================


.. dropdown:: Install Docker Engine on Ubuntu
   :open:

   Follow the official guide:
   `Install Docker Engine on Ubuntu
   <https://docs.docker.com/engine/install/ubuntu/>`_

   After installation, add your user to the ``docker`` group so you can
   run containers without ``sudo``:

   .. code-block:: console

      sudo usermod -aG docker $USER

   - ``usermod -aG docker`` adds your user to the ``docker`` group.
   - Without this, every ``docker`` command would require ``sudo``.

   **Log out and log back in** for the group change to take effect.
   Verify with:

   .. code-block:: console

      docker run hello-world

   - This downloads a tiny test image and runs it.
   - You should see a "Hello from Docker!" message confirming Docker is
     working.


.. dropdown:: Install NVIDIA Container Toolkit (GPU acceleration)
   :open:

   GPU acceleration is strongly recommended -- without it, Gazebo will
   fall back to software rendering and be very slow.

   **Add the NVIDIA container toolkit repository and install:**

   .. code-block:: console

      curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
          | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
      curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
          | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
          | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
      sudo apt update
      sudo apt install -y nvidia-container-toolkit

   - The first two commands download NVIDIA's GPG key and add their
     package repository to your system.
   - ``nvidia-container-toolkit`` is the package that allows Docker
     containers to access your NVIDIA GPU.

   **Configure Docker to use the NVIDIA runtime:**

   .. code-block:: console

      sudo nvidia-ctk runtime configure --runtime=docker
      sudo systemctl restart docker

   - ``nvidia-ctk runtime configure`` registers the NVIDIA runtime with
     Docker so containers can use GPU hardware.
   - Restarting Docker applies the new configuration.

   **Verify GPU access inside Docker:**

   .. code-block:: console

      docker run --rm --gpus all nvidia/cuda:12.3.1-base-ubuntu22.04 nvidia-smi

   - ``--rm`` removes the container after it exits (this is just a
     test).
   - ``--gpus all`` passes all available GPUs into the container.
   - ``nvidia-smi`` prints GPU information. You should see your GPU
     listed in the output.

   .. note::

      If you do not have an NVIDIA GPU, skip this step entirely. The
      simulation will still work but will run more slowly using software
      rendering.


.. _simulation-pull:

Step 2: Pull the Docker Image
====================================================


.. dropdown:: Pull the pre-built image
   :open:

   The course Docker image is hosted on Docker Hub. Pull it with:

   .. code-block:: console

      docker pull zeidk/enpm605-sim:latest

   - ``docker pull`` downloads a pre-built image from Docker Hub to
     your machine.
   - ``zeidk/enpm605-sim:latest`` is the image name -- it contains
     ROS 2 Jazzy, Gazebo Harmonic, and the ROSbot simulation workspace
     already compiled.
   - The download is ~4--6 GB. No further compilation is needed.

   **Verify the image was downloaded:**

   .. code-block:: console

      docker images | grep enpm605-sim

   You should see a row showing ``zeidk/enpm605-sim`` with the
   ``latest`` tag.


.. _simulation-run:

Step 3: Run the Container
====================================================


.. dropdown:: Allow X11 Display Access
   :open:

   Before starting the container, allow Docker to access your display
   server so Gazebo and RViz windows appear on your screen:

   .. code-block:: console

      xhost +local:docker

   - ``xhost`` controls access to your X11 display server (the system
     that draws windows on your screen).
   - ``+local:docker`` grants display access to all local Docker
     containers.
   - You will see: ``non-network local connections being added to
     access control list``

   .. tip::

      Run this command **once per login session**. If you log out and
      back in, you need to run it again.


.. dropdown:: Start the Container (with NVIDIA GPU)
   :open:

   First, create a directory on your host machine where your course
   work will be saved:

   .. code-block:: console

      mkdir -p ~/enpm605_ws

   Then start the container:

   .. code-block:: console

      docker run -it \
          --name enpm605 \
          --gpus all \
          -e DISPLAY=$DISPLAY \
          -e QT_X11_NO_MITSHM=1 \
          -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
          -v ~/enpm605_ws:/home/user/enpm605_ws \
          --network host \
          zeidk/enpm605-sim:latest \
          bash

   Here is what each flag does:

   .. list-table::
      :widths: 40 60
      :class: compact-table

      * - ``docker run``
        - Create and start a new container from the image.
      * - ``-it``
        - Run interactively (``-i``) with a terminal (``-t``) so you
          get a bash prompt.
      * - ``--name enpm605``
        - Name the container ``enpm605`` so you can refer to it easily
          later (stop, start, attach).
      * - ``--gpus all``
        - Pass all NVIDIA GPUs into the container for hardware-
          accelerated rendering.
      * - ``-e DISPLAY=$DISPLAY``
        - Forward the ``DISPLAY`` environment variable so GUI
          applications (Gazebo, RViz) appear on your screen.
      * - ``-e QT_X11_NO_MITSHM=1``
        - Disable shared memory for Qt applications, which prevents
          rendering errors inside Docker.
      * - ``-v /tmp/.X11-unix:/tmp/.X11-unix:rw``
        - Mount the X11 socket so the container can communicate with
          your display server.
      * - ``-v ~/enpm605_ws:/home/user/enpm605_ws``
        - **Mount your work directory.** Files you create inside
          ``~/enpm605_ws`` in the container are saved to
          ``~/enpm605_ws`` on your host machine. Your code is preserved
          even if you delete the container.
      * - ``--network host``
        - Share the host's network so ROS 2 nodes inside and outside
          the container can discover each other.
      * - ``zeidk/enpm605-sim:latest``
        - The Docker image to use.
      * - ``bash``
        - The command to run inside the container (a bash shell).

   You are now inside the container with ROS 2 and Gazebo ready to use.


.. dropdown:: Start the Container (without NVIDIA GPU)
   :open:

   If you do **not** have an NVIDIA GPU, use this command instead:

   .. code-block:: console

      mkdir -p ~/enpm605_ws
      docker run -it \
          --name enpm605 \
          -e DISPLAY=$DISPLAY \
          -e QT_X11_NO_MITSHM=1 \
          -e LIBGL_ALWAYS_SOFTWARE=1 \
          -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
          -v ~/enpm605_ws:/home/user/enpm605_ws \
          --network host \
          zeidk/enpm605-sim:latest \
          bash

   The only differences from the GPU version:

   - ``--gpus all`` is removed (no GPU to pass through).
   - ``-e LIBGL_ALWAYS_SOFTWARE=1`` is added, which forces OpenGL to
     use software rendering instead of looking for GPU hardware.


.. dropdown:: Open Additional Terminals

   To open a second (or third, etc.) terminal in the **same running
   container**:

   .. code-block:: console

      docker exec -it enpm605 bash

   - ``docker exec`` runs a command inside an already-running container.
   - ``-it`` gives you an interactive terminal.
   - ``enpm605`` is the container name you set with ``--name``.
   - ``bash`` starts a new shell session.

   This is useful for running ``ros2 topic echo`` or
   ``teleop_twist_keyboard`` in a separate terminal while the
   simulation is running.


.. dropdown:: Stop and Restart the Container

   The container **persists** after you exit, so you can restart it
   later without losing any installed packages or configuration changes
   inside the container.

   **Stop the container** (when you are done working):

   .. code-block:: console

      docker stop enpm605

   - This gracefully shuts down the container. It is not deleted --
     all state inside the container is preserved.

   **Restart and reattach** (next time you want to work):

   .. code-block:: console

      xhost +local:docker
      docker start enpm605
      docker exec -it enpm605 bash

   - ``docker start`` restarts a previously stopped container with all
     its state intact.
   - ``docker exec`` attaches a new terminal to it.

   **Permanently remove the container** (if you want a fresh start):

   .. code-block:: console

      docker rm enpm605

   - This deletes the container and all state inside it.
   - Files in ``~/enpm605_ws`` on your host machine are **not**
     affected because they live on the host, not inside the container.
   - After removing, you can create a new container with ``docker run``
     again.


.. dropdown:: Connect with VS Code
   :open:

   VS Code can attach directly to the running container, giving you a
   full editor with IntelliSense, integrated terminal, and file
   browsing inside the Docker environment.

   **1. Install the Dev Containers extension**

   Open VS Code and install the **Dev Containers** extension
   (``ms-vscode-remote.remote-containers``):

   .. code-block:: console

      code --install-extension ms-vscode-remote.remote-containers

   - This extension allows VS Code to connect to Docker containers and
     use them as a full development environment.

   **2. Start the container** (if not already running)

   .. code-block:: console

      xhost +local:docker
      docker start enpm605

   If you have not created the container yet, run the ``docker run``
   command from the previous section first.

   **3. Attach VS Code to the container**

   - Open the VS Code **Command Palette** (``Ctrl+Shift+P``)
   - Type **Dev Containers: Attach to Running Container...**
   - Select **enpm605** from the list

   VS Code will open a new window connected to the container. The
   bottom-left corner will show **Container enpm605**.

   **4. Open a folder**

   Once attached, use **File > Open Folder** to navigate to a
   workspace inside the container:

   - ``/home/user/enpm605_ws/`` -- your work directory (mounted from
     host -- changes are saved on your machine)
   - ``/home/user/rosbot_ws/`` -- the pre-built ROSbot simulation
     workspace

   **5. Install extensions inside the container**

   Extensions run inside the container and need to be installed there
   separately from your host VS Code. VS Code will prompt you to
   install recommended extensions. You can also install them manually:

   - **Python** (``ms-python.python``)
   - **ROS** (``ms-iot.vscode-ros``)

   .. tip::

      Once attached to the container, you can open integrated terminals
      inside VS Code with ``Ctrl+``` ` -- these run inside the
      container and have full access to ROS 2 and Gazebo commands.


.. _simulation-launch:

Step 4: Launch the Simulation
====================================================


.. dropdown:: Launch Gazebo with ROSbot
   :open:

   Once inside the container (via terminal or VS Code), launch the
   simulation:

   .. code-block:: console

      ros2 launch rosbot_gazebo simulation.yaml

   - ``ros2 launch`` starts a launch file that brings up multiple nodes.
   - ``rosbot_gazebo`` is the package containing the simulation launch
     files.
   - ``simulation.yaml`` is the launch file that starts Gazebo with the
     ROSbot model and RViz.

   The Gazebo window and RViz should appear on your host display.

   To launch with the ROSbot XL model instead:

   .. code-block:: console

      ros2 launch rosbot_gazebo simulation.yaml robot_model:=rosbot_xl

   - ``robot_model:=rosbot_xl`` overrides the default robot model
     parameter.


.. dropdown:: Launch Arguments

   You can customize the simulation by passing arguments to the launch
   file using the ``argument:=value`` syntax.

   .. list-table::
      :widths: 22 50 28
      :header-rows: 1
      :class: compact-table

      * - Argument
        - Description
        - Default
      * - ``robot_model``
        - Robot model (``rosbot`` or ``rosbot_xl``)
        - ``rosbot``
      * - ``gz_gui``
        - GUI layout configuration file
        - ``teleop.config``
      * - ``gz_headless_mode``
        - Run Gazebo without the GUI
        - ``False``
      * - ``gz_log_level``
        - Console output verbosity (0--4)
        - ``1``
      * - ``gz_world``
        - Path to SDF world file
        - ``husarion_world.sdf``
      * - ``rviz``
        - Launch RViz alongside the simulation
        - ``True``
      * - ``x``, ``y``, ``z``
        - Initial robot position
        - ``0.0``, ``2.0``, ``0.0``
      * - ``roll``, ``pitch``, ``yaw``
        - Initial robot orientation
        - ``0.0``, ``0.0``, ``0.0``

   **Example:** launch without RViz and with the robot at position
   (1, 3, 0):

   .. code-block:: console

      ros2 launch rosbot_gazebo simulation.yaml rviz:=False x:=1.0 y:=3.0


.. _simulation-verify:

Step 5: Verify the Setup
====================================================


.. dropdown:: Quick Smoke Test
   :open:

   Open a second terminal in the container (``docker exec -it enpm605
   bash``) and verify the robot is publishing data:

   .. code-block:: console

      # List all active topics -- you should see /scan, /odom,
      # /camera/color/image_raw, etc.
      ros2 topic list

      # Print one LiDAR scan message and exit
      ros2 topic echo /scan --once

      # Measure the camera publishing rate (Ctrl+C to stop)
      ros2 topic hz /camera/color/image_raw

      # Print one odometry message and exit
      ros2 topic echo /odom --once

      # Generate a PDF of the TF tree (saved to frames.pdf)
      ros2 run tf2_tools view_frames

   You should see topics for the LiDAR (``/scan``), camera, IMU
   (``/imu_broadcaster/imu``), and odometry (``/odom``).

   **Drive the robot manually:**

   .. code-block:: console

      ros2 run teleop_twist_keyboard teleop_twist_keyboard

   - This node reads your keyboard input and publishes velocity
     commands on ``/cmd_vel``.
   - Use the keys shown on screen (``i`` = forward, ``j`` = turn left,
     ``l`` = turn right, ``k`` = stop, ``,`` = backward).


Troubleshooting
====================================================


.. dropdown:: ``cannot open display`` error

   The container cannot connect to your display server.

   - Ensure you ran ``xhost +local:docker`` on the host **before**
     starting the container.
   - Check that the ``DISPLAY`` variable is set inside the container:

     .. code-block:: console

        echo $DISPLAY

     It should show ``:0`` or ``:1``. If it is empty, the ``-e
     DISPLAY=$DISPLAY`` flag was not passed correctly.


.. dropdown:: Gazebo is extremely slow (no GPU)

   The simulator is likely using software rendering.

   - Run ``nvidia-smi`` inside the container. If it fails, the GPU is
     not being passed through.
   - Ensure ``--gpus all`` was included in your ``docker run`` command.
   - Ensure the NVIDIA Container Toolkit is installed on the host
     (see Step 1).
   - Restart Docker on the host: ``sudo systemctl restart docker``.


.. dropdown:: ``permission denied`` when running Docker commands

   Your user is not in the ``docker`` group.

   .. code-block:: console

      sudo usermod -aG docker $USER

   Then **log out and log back in**. Alternatively, run
   ``newgrp docker`` to apply the change in your current session only.


.. dropdown:: ``docker: Error response from daemon: Conflict``

   A container named ``enpm605`` already exists. Either restart it:

   .. code-block:: console

      docker start enpm605
      docker exec -it enpm605 bash

   Or remove it and create a new one:

   .. code-block:: console

      docker rm enpm605
      # Then run the docker run command again
