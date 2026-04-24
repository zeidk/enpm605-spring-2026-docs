====================================================
Docker Installation
====================================================

This page walks you through running the simulation inside a
**Docker container**. This approach isolates Gazebo Harmonic from any
Gazebo Classic installation on your host machine.

The pre-built Docker image includes:

- **ROS 2 Jazzy** desktop installation
- **Gazebo Harmonic** simulator
- **Husarion ROSbot** simulation packages (robot model with LiDAR,
  camera, and IMU sensors)

.. card:: Terminology

   Throughout this guide, two terms are used to distinguish between
   your machine and the Docker container:

   - **Host** -- your physical Ubuntu machine (where Docker is installed
     and where you run ``docker`` commands).
   - **Container** (or **remote**) -- the isolated Docker environment
     where ROS 2, Gazebo, and the simulation packages run. When VS Code
     is attached to the container, it refers to it as a *remote*
     environment.


.. _docker-step1:

Step 1: Install Docker Engine
====================================================


.. dropdown:: Install Docker Engine on Ubuntu
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

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
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

   GPU acceleration is strongly recommended -- without it, Gazebo will
   fall back to software rendering and be very slow.

   .. note::

      If you do not have an NVIDIA GPU, skip this step entirely. The
      simulation will still work but will run more slowly using software
      rendering.

   **Add the NVIDIA container toolkit repository and install:**

   .. code-block:: console

      curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
          | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg


   .. code-block:: console

      curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
          | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
          | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

   .. code-block:: console

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


.. _docker-step2:

Step 2: Pull the Docker Image
====================================================


.. dropdown:: Pull the pre-built image
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

   The course Docker image is hosted on Docker Hub. Pull it with:

   .. code-block:: console

      docker pull zeidk/enpm605-sim:latest

   - ``docker pull`` downloads a pre-built image from Docker Hub to
     your machine.
   - ``zeidk/enpm605-sim:latest`` is the image name -- it contains
     ROS 2 Jazzy, Gazebo Harmonic, and the ROSbot simulation workspace
     already compiled.
   - The download is ~4--6 GB. No further compilation is needed (unless indicated)

   **Verify the image was downloaded:**

   .. code-block:: console

      docker images | grep enpm605-sim

   You should see a row showing ``zeidk/enpm605-sim`` with the
   ``latest`` tag.


.. _docker-step3:

Step 3: Create and Start the Container
====================================================


.. dropdown:: Allow X11 Display Access
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

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


.. dropdown:: Create the Container
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

   .. important::

      You only need to run ``docker run`` **once** to create the
      container. After that, use ``docker start`` / ``docker exec`` to
      restart it (see :ref:`docker-lifecycle`).

   .. tab-set::

      .. tab-item:: With NVIDIA GPU

         .. code-block:: console

            docker run -it \
                --name enpm605 \
                --gpus all \
                -e DISPLAY=$DISPLAY \
                -e QT_X11_NO_MITSHM=1 \
                -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
                -v ~/enpm605_ws:/home/zeid/enpm605_ws \
                --network host \
                zeidk/enpm605-sim:latest \
                bash

      .. tab-item:: Without NVIDIA GPU

         .. code-block:: console

            docker run -it \
                --name enpm605 \
                -e DISPLAY=$DISPLAY \
                -e QT_X11_NO_MITSHM=1 \
                -e LIBGL_ALWAYS_SOFTWARE=1 \
                -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
                -v ~/enpm605_ws:/home/zeid/enpm605_ws \
                --network host \
                zeidk/enpm605-sim:latest \
                bash

         The differences from the GPU version:

         - ``--gpus all`` is removed (no GPU to pass through).
         - ``-e LIBGL_ALWAYS_SOFTWARE=1`` is added, which forces OpenGL
           to use software rendering instead of looking for GPU hardware.

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
          accelerated rendering (GPU tab only).
      * - ``-e DISPLAY=$DISPLAY``
        - Forward the ``DISPLAY`` environment variable so GUI
          applications (Gazebo, RViz) appear on your screen.
      * - ``-e QT_X11_NO_MITSHM=1``
        - Disable shared memory for Qt applications, which prevents
          rendering errors inside Docker.
      * - ``-v /tmp/.X11-unix:/tmp/.X11-unix:rw``
        - Mount the X11 socket so the container can communicate with
          your display server.
      * - ``-v ~/enpm605_ws:/home/zeid/enpm605_ws``
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

   After running this command you will be dropped into a bash shell
   **inside the container**. Your working directory will be
   ``/home/zeid/``. You now have access to ROS 2 and Gazebo.


.. _docker-step4:

Step 4: Verify the Setup
====================================================

Once inside the container, verify that everything works by launching
a quick test simulation.

.. dropdown:: Quick Gazebo Test
   :color: primary
   :icon: pin
   :open:
   :animate: fade-in-slide-down

   From the container shell, run:

   .. code-block:: console

      ros2 launch rosbot_gazebo empty_world.launch.py

   This launches Gazebo Harmonic with the ROSbot in an empty world.
   You should see:

   - A **Gazebo** window opens on your screen showing an empty
     environment with the ROSbot model.
   - An **RViz** window opens showing the robot's sensor data.

   If both windows appear and the robot is visible, your setup is
   working correctly. Close both windows (``Ctrl+C`` in the terminal)
   before proceeding.

   .. note::

      If Gazebo does not open or you see a ``cannot open display``
      error, make sure you ran ``xhost +local:docker`` on the host
      **before** starting the container. See the
      :ref:`docker-troubleshooting` section below.


.. _docker-workspace:

Working Inside the Container
====================================================

.. card:: Key Directories

   When you are inside the container, your home directory is
   ``/home/zeid/``. The main workspace is:

   .. list-table::
      :widths: 40 60
      :class: compact-table

      * - ``~/enpm605_ws/``
        - **Your workspace** (mounted from the host at
          ``~/enpm605_ws/``). This directory contains both the pre-built
          ROSbot simulation packages (under ``src/rosbot_sim/``) and
          your own ROS 2 packages. Files persist on your host machine
          even if the container is deleted.
      * - ``~/enpm605_ws/src/rosbot_sim/``
        - The ROSbot simulation packages (robot model, Gazebo worlds,
          launch files). **Do not modify** these packages.
      * - ``~/enpm605_ws/src/``
        - Create your own ROS 2 packages here alongside
          ``rosbot_sim/``.


.. dropdown:: Open Additional Terminals
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

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


.. _docker-lifecycle:

Container Lifecycle
====================================================

.. dropdown:: Exiting the Container
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

   To leave a container terminal, type:

   .. code-block:: console

      exit

   - If this is the **only** terminal attached to the container (the
     one from ``docker run``), the container **stops**.
   - If this is an **additional** terminal (opened with
     ``docker exec``), only that shell closes -- the container keeps
     running.

   You can also press ``Ctrl+D`` to exit the shell.

   .. tip::

      If you want to detach from the container without stopping it,
      press ``Ctrl+P`` followed by ``Ctrl+Q``. This returns you to the
      host shell while the container continues running in the
      background.


.. dropdown:: Stopping and Restarting the Container
   :color: primary
   :icon: pin
   :animate: fade-in-slide-down

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

   - ``xhost +local:docker`` re-enables display access (needed once
     per login session).
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


.. _docker-vscode:

Connecting with VS Code
====================================================

VS Code can attach directly to the running container, giving you a
full editor with IntelliSense, integrated terminal, and file
browsing -- all running inside the Docker environment.

The following diagram shows the complete pipeline:

.. image:: vscode_docker_pipeline.svg
   :align: center
   :width: 100%
   :alt: Pipeline showing how to connect VS Code to the Docker container

|

.. dropdown:: Step-by-step instructions
   :color: primary
   :icon: pin
   :open:
   :animate: fade-in-slide-down

   .. important::

      The container **must be running** before VS Code can attach to
      it. Always start the container from a terminal first (using
      ``docker run`` or ``docker start``), then attach VS Code.

   **1. Install the Dev Containers extension**

   Open VS Code on your **host machine** and install the
   **Dev Containers** extension
   (``ms-vscode-remote.remote-containers``):

   .. code-block:: console

      code --install-extension ms-vscode-remote.remote-containers

   This extension allows VS Code to connect to Docker containers and
   use them as a full development environment.

   **2. Start the container** (if not already running)

   In a **host terminal** (not VS Code), run:

   .. code-block:: console

      xhost +local:docker
      docker start enpm605

   If you have not created the container yet, run the ``docker run``
   command from Step 3 first.

   **3. Attach VS Code to the container**

   - Open the VS Code **Command Palette** (``Ctrl+Shift+P``)
   - Type ``Dev Containers: Attach to Running Container...``
   - Select **enpm605** from the list

   VS Code will open a **new window** connected to the container. The
   bottom-left corner will show
   :bdg-primary:`Container enpm605`
   confirming you are working inside the container.

   **4. Open a folder**

   Once attached, use **File > Open Folder** and navigate to:

   - ``/home/zeid/enpm605_ws/`` -- your workspace (mounted from
     host -- changes are saved on your machine)

   **5. Install extensions inside the container**

   Extensions run inside the container and need to be installed there
   separately from your host VS Code. VS Code will prompt you to
   install recommended extensions. You can also install them manually:

   - **Python** (``ms-python.python``)
   - **ROS** (``ms-iot.vscode-ros``)

   **6. Use the integrated terminal**

   Open a terminal inside VS Code with ``Ctrl+``` ` -- this terminal
   runs **inside the container** and has full access to ROS 2 and
   Gazebo commands. You can open multiple terminals from within VS Code,
   eliminating the need to run ``docker exec`` from separate host
   terminals.


.. _docker-launch:

Launching the Simulation
====================================================

Once your environment is set up (and verified with the quick test in
Step 4), launch the full simulation using the shared instructions on
the :ref:`simulation-launch` page.


.. _docker-troubleshooting:

Troubleshooting
====================================================

.. card::

   .. dropdown:: ``package 'ros_gz_bridge' not found``
      :color: warning
      :icon: package
      :animate: fade-in-slide-down

      The ROS--Gazebo bridge packages are not installed in the container.
      Install them:

      .. code-block:: console

         sudo apt update
         sudo apt install -y ros-jazzy-ros-gz

      Then source the environment again:

      .. code-block:: console

         source /opt/ros/jazzy/setup.bash
         source ~/enpm605_ws/install/setup.bash


   .. dropdown:: ``cannot open display`` error
      :color: warning
      :icon: device-desktop
      :animate: fade-in-slide-down

      The container cannot connect to your display server.

      - Ensure you ran ``xhost +local:docker`` on the host **before**
        starting the container.
      - Check that the ``DISPLAY`` variable is set inside the container:

      .. code-block:: console

         echo $DISPLAY

      It should show ``:0`` or ``:1``. If it is empty, the ``-e
      DISPLAY=$DISPLAY`` flag was not passed correctly.


   .. dropdown:: Gazebo is extremely slow (no GPU)
      :color: warning
      :icon: cpu
      :animate: fade-in-slide-down

      The simulator is likely using software rendering.

      - Run ``nvidia-smi`` inside the container. If it fails, the GPU is
        not being passed through.
      - Ensure ``--gpus all`` was included in your ``docker run`` command.
      - Ensure the NVIDIA Container Toolkit is installed on the host
        (see Step 1).
      - Restart Docker on the host: ``sudo systemctl restart docker``.


   .. dropdown:: ``permission denied`` when running Docker commands
      :color: warning
      :icon: lock
      :animate: fade-in-slide-down

      Your user is not in the ``docker`` group.

      .. code-block:: console

         sudo usermod -aG docker $USER

      Then **log out and log back in**. Alternatively, run
      ``newgrp docker`` to apply the change in your current session only.


   .. dropdown:: ``docker: Error response from daemon: Conflict``
      :color: warning
      :icon: alert
      :animate: fade-in-slide-down

      A container named ``enpm605`` already exists. Either restart it:

      .. code-block:: console

         docker start enpm605
         docker exec -it enpm605 bash

      Or remove it and create a new one:

      .. code-block:: console

         docker rm enpm605
         # Then run the docker run command again
