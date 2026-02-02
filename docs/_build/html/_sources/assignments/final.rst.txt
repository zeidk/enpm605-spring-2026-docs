.. default-domain:: cpp
.. _final_project_micromouse_ros2:

=========================================================
Final Project
=========================================================

.. admonition:: Changelog
   :class: changelog
   
   - **v1.0 (12/03/2025)** — Initial release of ROS2 MicroMouse assignment.

.. admonition:: Resources
   :class: resources

   - ⚙️ `Starter Code <https://github.com/zeidk/enpm702-fall-2025-ROS/tree/main/final_starter/micromouse_cpp>`_
   - 🎥 `Demo Video <https://drive.google.com/file/d/1HK9yq_aKyOCe_Via429ekpd6PcMsQt5u/view?usp=sharing>`_
   - 📖 Slides for Lecture 12 (v2.0) - Canvas or `Google Drive <https://drive.google.com/file/d/1KoLZ5owrVZy_j06yUbwYXtujeIE2fdg_/view?usp=sharing>`_ 
   - 🔗 `MicroMouse Simulator (main) <https://github.com/mackorone/mms>`_
   - 🔗 `MicroMouse Simulator (API) <https://github.com/mackorone/mms#mouse-api>`_
   - 🔗 `MicroMouse Simulator (maze files) <https://github.com/mackorone/mms#maze-files>`_

**MicroMouse Robot Maze Navigation with ROS2**

.. list-table::
   :widths: 20 30
   :stub-columns: 1
   :class: compact-table

   * - **Due Date**
     - 12/12/2025
   * - **Points**
     - 100 pts
   * - **Work Mode**
     - Group assignment
   * - **Language**
     - C++17 / ROS2 Humble/Jazzy

---------------------------------------------------------
Guidelines
---------------------------------------------------------

This assignment is to be completed in **groups**, and all instructions must be followed carefully. Not adhering to these guidelines may result in a zero for the assignment.

.. important::
   
   - Each group member must contribute significantly to the project.
   - Keep your work private; do not share your files or code with other groups.
   - Any GitHub repository used for development must be private.
   - Submit your completed work as a zipped file via Canvas.
   - Feel free to discuss general concepts with other groups, but sharing specific implementation details is strictly forbidden.
   - The use of AI-generated code (e.g., ChatGPT, Copilot) for core logic is not permitted, though it may be used for documentation.

---------------------------------------------------------
Overview
---------------------------------------------------------

You will implement ROS2 communication patterns for a **MicroMouse Robot Navigation System**. The robot uses Depth-First Search (DFS) to navigate through an unknown 16x16 maze in the MMS simulator.

.. important::

   **Why is the DFS algorithm provided?**
   
   The navigation algorithm (DFS with dynamic replanning) is **fully provided** in this assignment. This design choice allows you to:
   
   1. **Focus on ROS2 concepts** — Topics, Services, Actions, and Parameters are the learning objectives
   2. **Level the playing field** — Students who may not have completed the previous DFS assignment are not penalized
   3. **Learn by example** — The provided code demonstrates proper C++ practices and algorithm implementation
   
   Your task is to implement the **ROS2 communication layer** that allows external nodes to interact with the robot.

.. important::

   **Your code must work in both execution modes:**
   
   - ``standalone_mode: true`` — Robot navigates immediately using goal set in `params.yaml`
   - ``standalone_mode: false`` — Robot waits for action client to send goal
   
   The grading will test both modes. Ensure your implementations handle both cases correctly.

**Learning Objectives:**

After completing this assignment, you will understand:

- **Parameters**: Loading configuration from YAML files
- **Topics**: Publishing continuous robot position data
- **Services**: Request/response pattern for querying robot status
- **Actions**: Long-running navigation tasks with feedback and cancellation (Ctrl+C)

**Key System Features:**

- **Custom Interfaces** — Define action and service message types with constants
- **Topic Publisher** — Broadcast robot position in real-time using ``geometry_msgs::msg::Point``
- **Service Server** — Respond to status queries (PROVIDED)
- **Service Client** — Query robot status as a standalone node
- **Action Server** — Handle navigation goals with feedback
- **Action Client** — Send goals, monitor progress, and cancel with Ctrl+C

System Communication
^^^^^^^^^^^^^^^^^^^^^

The following diagram illustrates the communication flow between all ROS2 components. The sequence diagram shows initialization, standalone mode, action mode, service queries, and topic monitoring.

.. only:: html

   .. figure:: ../_static/final/final_sequence_diagram_light.png
      :alt: MicroMouse ROS2 Communication Sequence Diagram
      :align: center
      :width: 90%
      :class: only-light

   .. figure:: ../_static/final/final_sequence_diagram_dark.png
      :alt: MicroMouse ROS2 Communication Sequence Diagram
      :align: center
      :width: 90%
      :class: only-dark


---------------------------------------------------------
Simulator
---------------------------------------------------------

Your program interfaces with the MMS graphical simulator (`mms <https://github.com/mackorone/mms>`_). The simulator enables testing maze-solving code without a physical robot.

Installation
^^^^^^^^^^^^^

.. todo::

    1. Download the `Linux precompiled version of the simulator <https://github.com/mackorone/mms/releases/download/v1.2.0/linux.zip>`_
    2. Unzip the file, which generates the ``linux`` folder
    3. ``cd <path to linux folder>``
    4. ``chmod +x mms-x86_64.AppImage``
    5. ``./mms-x86_64.AppImage --appimage-extract`` → creates the folder ``squashfs-root``
    6. ``cd squashfs-root``
    7. ``chmod +x mms``
    8. ``./mms``
    9. The simulator should start (we will refer to this window as the ``mms`` window)

Maze Files
^^^^^^^^^^^^

.. todo::
 
    - Download maze files:
    
        - Follow `instructions <https://github.com/mackorone/mms?tab=readme-ov-file#maze-files>`_ to retrieve the maze files.
        - or ``git clone https://github.com/micromouseonline/mazefiles.git``
    
    - Load maze files in the simulator:

        - Click the 🗂️ icon from the ``mms`` window
        - Navigate to the maze folder you cloned earlier
        - Select any file from ``mazefiles`` → ``classic``

Build and Run with ROS2
^^^^^^^^^^^^^^^^^^^^^^^^

.. todo::
 
    1. Build your ROS2 workspace:
    
       .. code-block:: bash
       
           cd ~/ros2_ws
           colcon build --packages-select micromouse_interfaces micromouse_cpp
           source install/setup.bash
    
    2. Configure MMS to run your node:
    
        - Click on the + symbol → ``New Mouse Algorithm`` window
        - **Name:** MicroMouse ROS2
        - **Directory:** ``.`` (a single dot — the field cannot be empty)
        - **Build Command:** Leave empty (build separately in terminal)
        - **Run Command:** 
        
          .. code-block:: bash
          
              ros2 run micromouse_cpp micromouse_node --ros-args \
                  -p standalone_mode:=true \
                  --params-file <absolute path to params.yaml>
          
          .. note::
          
              Change ``standalone_mode:=true`` to ``standalone_mode:=false`` when testing action mode.
              The command-line parameter overrides the value in ``params.yaml``.
        
        - Click OK
    
    3. Click ``Run`` in the MMS window

---------------------------------------------------------
Provided DFS Algorithm
---------------------------------------------------------

.. note::
   
   This section is only for your information as you are not expected to modify the algorithm

The Depth-First Search algorithm with dynamic replanning is **fully provided**. This section explains the algorithm so you understand how the robot navigates.

Algorithm Overview
^^^^^^^^^^^^^^^^^^^

The provided DFS implementation includes several improvements over the basic algorithm from previous assignments:

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Improvement
     - Description
   * - **Sense Before Move**
     - Robot senses walls *before* moving, not after. This prevents moving into walls.
   * - **Bidirectional Wall Marking**
     - When a wall is detected, it's marked on *both* sides (current cell and neighbor). This ensures consistency.
   * - **Dynamic Replanning**
     - When a wall blocks the planned path, the robot replans from its current position instead of failing.
   * - **MMS ACK Handling**
     - All movement commands wait for acknowledgment from the simulator to ensure synchronization.
   * - **Perimeter Walls**
     - Maze boundary walls are initialized at startup, preventing edge-case errors.

Planning with Wall Consideration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A key improvement in this implementation is how DFS plans paths using **known wall information**.

**Previous Assignment (Basic DFS):**

In the previous assignment, the DFS algorithm performed *blind exploration*. The robot would:

1. Push neighbors onto the stack without checking for walls
2. Discover walls only when attempting to move
3. Backtrack immediately upon hitting a wall
4. Have no memory of walls between planning iterations

This approach meant the robot would repeatedly attempt to visit cells it couldn't reach, leading to inefficient navigation and excessive backtracking.

**This Assignment (Wall-Aware DFS):**

The provided implementation maintains a **persistent wall map** that is consulted during path planning:

1. **Wall Array**: A 3D array ``walls[x][y][direction]`` stores all discovered walls
2. **Planning Uses Walls**: The ``DFS_PLAN`` function only considers neighbors where ``walls[x][y][dir] == false``
3. **Bidirectional Updates**: When a wall is sensed, both sides are marked (e.g., wall to the North of (2,3) also means wall to the South of (2,4))
4. **Accumulated Knowledge**: Wall information persists across replanning cycles, so the robot never "forgets" discovered walls

.. code-block:: cpp

    // Wall-aware neighbor check in DFS_PLAN
    for (Dir dir : {NORTH, EAST, SOUTH, WEST}) {
        if (!walls_[current.x][current.y][dir]) {  // Only if no wall
            Cell neighbor = get_neighbor(current, dir);
            if (in_bounds(neighbor) && visited.find(neighbor) == visited.end()) {
                stack.push(neighbor);
                parent[neighbor] = current;
            }
        }
    }

This wall-aware planning means:

- **Fewer wasted moves**: The robot plans around known walls instead of discovering them mid-path
- **Efficient replanning**: When a new wall is discovered, the replan immediately incorporates all known walls
- **Guaranteed progress**: Each replan produces a valid path through known-open cells

Pseudocode
^^^^^^^^^^^

The navigation system uses two algorithms: (1) the main navigation loop with dynamic replanning, and (2) the DFS path planning function.

.. prf:algorithm:: DFS Navigation with Dynamic Replanning
   :label: dfs-navigation-replanning

   **Inputs:** 

   - :math:`m_{start}` (start cell coordinates, typically (0,0))
   - :math:`m_{goal}` (goal cell coordinates)
   - :math:`w` (3D wall array: walls[x][y][direction])
   - :math:`r` (robot state: position and facing direction)
   
   **Output:** true if goal is reached, false otherwise

   1. Initialize maze dimensions from simulator: :math:`width \gets \text{mazeWidth}()`, :math:`height \gets \text{mazeHeight}()`
   
   2. Initialize wall storage: :math:`w[x][y][d] \gets \text{false}` for all cells and directions
   
   3. Set perimeter walls (maze boundaries)
   
   4. Set :math:`r.position \gets m_{start}`, :math:`r.facing \gets \text{NORTH}`
   
   5. Sense initial walls at :math:`m_{start}` and update :math:`w`
   
   6. :math:`path \gets \text{DFS_PLAN}(r.position, m_{goal}, w)`
   
   7. **if** :math:`path` is empty **then** return **false**
   
   8. Visualize :math:`path` in simulator
   
   9. :math:`idx \gets 1` (path index, skip start cell)
   
   10. **while** :math:`r.position \neq m_{goal}` **do**
   
       a. **if** :math:`idx \geq |path|` **then** (need to replan)
       
          i. :math:`path \gets \text{DFS_PLAN}(r.position, m_{goal}, w)`
          
          ii. **if** :math:`path` is empty **then** return **false**
          
          iii. :math:`idx \gets 1`
       
       b. :math:`next \gets path[idx]`
       
       c. :math:`dir \gets` direction from :math:`r.position` to :math:`next`
       
       d. Turn robot to face :math:`dir`
       
       e. Sense walls at :math:`r.position` and update :math:`w` (sense BEFORE moving)
       
       f. **if** wall detected in front **then** (path blocked)
       
          i. :math:`path \gets \text{DFS_PLAN}(r.position, m_{goal}, w)`
          
          ii. **if** :math:`path` is empty **then** return **false**
          
          iii. :math:`idx \gets 1`
          
          iv. **continue**
       
       g. Move forward: send ``moveForward``, wait for ACK, update :math:`r.position`
       
       h. Sense walls at new position and update :math:`w`
       
       i. Publish :math:`r.position` to ``/robot_position`` topic
       
       j. **if** not in standalone mode **then** publish feedback
       
       k. **if** :math:`r.position = next` **then** :math:`idx \gets idx + 1`
   
   11. **return** true (goal reached)

.. prf:algorithm:: Depth-First Search Path Planning
   :label: dfs-path-planning

   **Inputs:** 

   - :math:`s` (stack of cells, initially empty)
   - :math:`v` (set of visited cells, initially empty)
   - :math:`p` (parent map for path reconstruction)
   - :math:`w` (wall array: walls[x][y][direction])
   - :math:`m_{start}` (start cell coordinates)
   - :math:`m_{goal}` (goal cell coordinates)
   
   **Output:** path from start to goal as list of cells, or empty if no path

   1. **if** :math:`m_{start} = m_{goal}` **then** return :math:`[m_{start}]`
   
   2. :math:`s.\text{push}(m_{start})`
   
   3. :math:`p[m_{start}] \gets m_{start}`
   
   4. **while** not :math:`s.\text{empty}()` **do**
   
      a. :math:`n \gets s.\text{pop}()`
      
      b. **if** :math:`n \in v` **then** **continue**
      
      c. :math:`v.\text{insert}(n)`
      
      d. **if** :math:`n = m_{goal}` **then** (goal found, reconstruct path)
      
         i. :math:`path \gets []`
         
         ii. :math:`cell \gets m_{goal}`
         
         iii. **while** :math:`cell \neq m_{start}` **do**
         
              - :math:`path.\text{prepend}(cell)`
              
              - :math:`cell \gets p[cell]`
         
         iv. :math:`path.\text{prepend}(m_{start})`
         
         v. **return** :math:`path`
      
      e. **for** :math:`dir` **in** [NORTH, EAST, SOUTH, WEST] **do** (priority order)
      
         i. **if** :math:`w[n.x][n.y][dir] = \text{false}` **then** (no wall)
         
            - :math:`neighbor \gets` cell in direction :math:`dir` from :math:`n`
            
            - **if** :math:`neighbor` in bounds **and** :math:`neighbor \notin v` **then**
            
              - **if** :math:`neighbor \notin p` **then** :math:`p[neighbor] \gets n`
              
              - :math:`s.\text{push}(neighbor)`
   
   5. **return** :math:`[]` (no path found)

Key Implementation Details
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Wall Sensing and Marking:**

.. code-block:: cpp

    // Sense walls BEFORE moving
    void sense_and_update(const Cell& pos, Dir facing) {
        if (MazeControlAPI::has_wall_front()) {
            mark_wall(pos, facing);  // Mark on both sides
        }
        if (MazeControlAPI::has_wall_right()) {
            mark_wall(pos, right_of(facing));
        }
        if (MazeControlAPI::has_wall_left()) {
            mark_wall(pos, left_of(facing));
        }
    }
    
    // Mark wall bidirectionally
    void mark_wall(const Cell& c, Dir d) {
        walls_[c.x][c.y][d] = true;
        Cell neighbor = {c.x + dx(d), c.y + dy(d)};
        if (in_bounds(neighbor)) {
            walls_[neighbor.x][neighbor.y][opposite(d)] = true;
        }
    }

**Movement with ACK:**

.. code-block:: cpp

    // MMS requires acknowledgment for movement commands
    void MazeControlAPI::move_forward() {
        std::cout << "moveForward" << std::endl;
        std::string response;
        std::cin >> response;  // Wait for "ack"
        if (response != "ack") {
            std::cerr << "moveForward error: " << response << std::endl;
        }
    }

---------------------------------------------------------
Package Structure
---------------------------------------------------------

You will work with two ROS2 packages:

.. code-block:: text

    ros2_ws/src/
    ├── micromouse_interfaces/     # TODO: CREATE THIS
    │   ├── action/
    │   │   └── NavigateToGoal.action
    │   ├── srv/
    │   │   └── GetRobotStatus.srv
    │   ├── CMakeLists.txt
    │   └── package.xml
    │
    └── micromouse_cpp/            # PROVIDED (with TODOs)
        ├── include/micromouse_cpp/
        │   ├── maze_control_api.hpp      # PROVIDED
        │   ├── navigate_action_client.hpp # PROVIDED
        │   └── get_status_client.hpp     # PROVIDED
        ├── src/
        │   ├── maze_control_api.cpp      # PROVIDED
        │   ├── micromouse_node.cpp       # TODO: Topic Publisher, Action Server
        │   │                             # PROVIDED: Service Server, DFS Algorithm
        │   ├── navigate_action_client.cpp # TODO: Implement callbacks
        │   └── get_status_client.cpp     # TODO: Implement callbacks
        ├── config/
        │   └── params.yaml               # TODO: Implement
        ├── CMakeLists.txt                # PROVIDED
        └── package.xml                   # PROVIDED

.. note::

   The ``micromouse_cpp`` package already lists ``micromouse_interfaces`` as a dependency in its ``package.xml`` and ``CMakeLists.txt``. You only need to create the ``micromouse_interfaces`` package with the correct interface definitions.

---------------------------------------------------------
Tasks
---------------------------------------------------------

Task 1: Create ``micromouse_interfaces`` Package (25 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new ROS2 package that defines custom action and service interfaces. This package is already configured as a dependency in ``micromouse_cpp``.

.. code-block:: bash

    cd ~/ros2_ws/src
    ros2 pkg create micromouse_interfaces --dependencies std_msgs
    cd micromouse_interfaces
    mkdir action srv

NavigateToGoal.action
""""""""""""""""""""""

Create ``action/NavigateToGoal.action`` with the following content:

.. code-block:: text

    # =============================================================================
    # NavigateToGoal.action
    # Action for navigating the MicroMouse robot to a goal cell in the maze
    # =============================================================================

    # ---- CONSTANTS for Direction ----
    # These constants define the robot's facing direction
    uint8 DIRECTION_NORTH = 0
    uint8 DIRECTION_EAST = 1
    uint8 DIRECTION_SOUTH = 2
    uint8 DIRECTION_WEST = 3

    # ---- GOAL ----
    # The target cell coordinates in the maze (0-indexed)
    int32 goal_x    # X coordinate of target cell (column, 0 = leftmost)
    int32 goal_y    # Y coordinate of target cell (row, 0 = bottom)
    ---
    # ---- RESULT ----
    # Final outcome of the navigation attempt
    bool success        # True if goal was reached, False otherwise
    int32 total_steps   # Total number of cells traversed during navigation
    float64 total_time  # Total elapsed time in seconds
    string message      # Human-readable status message (e.g., "Goal reached!", "No path found")
    ---
    # ---- FEEDBACK ----
    # Real-time updates during navigation (published after each move)
    int32 current_x         # Robot's current X coordinate
    int32 current_y         # Robot's current Y coordinate
    uint8 direction         # Robot's facing direction (use DIRECTION_* constants)
    float64 elapsed_seconds # Time elapsed since navigation started

**Field Descriptions:**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1
   :class: compact-table

   * - Field
     - Section
     - Purpose
   * - ``goal_x``, ``goal_y``
     - Goal
     - Target cell coordinates. The maze is 16x16, so valid values are 0-15. The center goal cells are typically (7,7), (7,8), (8,7), or (8,8).
   * - ``success``
     - Result
     - Indicates whether the robot successfully reached the goal cell.
   * - ``total_steps``
     - Result
     - Count of forward movements made. Useful for evaluating path efficiency.
   * - ``total_time``
     - Result
     - Navigation duration in seconds from goal acceptance to completion.
   * - ``message``
     - Result
     - Descriptive status: "Goal reached!", "No path found", or "Navigation cancelled".
   * - ``current_x``, ``current_y``
     - Feedback
     - Robot's position after each move. Allows real-time tracking.
   * - ``direction``
     - Feedback
     - Robot's facing direction using the defined constants (NORTH=0, EAST=1, SOUTH=2, WEST=3).
   * - ``elapsed_seconds``
     - Feedback
     - Running time since navigation started. Useful for monitoring progress.

**Using Constants in C++:**

.. code-block:: cpp

    #include "micromouse_interfaces/action/navigate_to_goal.hpp"
    
    using NavigateToGoal = micromouse_interfaces::action::NavigateToGoal;
    
    // Access constants
    uint8_t north = NavigateToGoal::Goal::DIRECTION_NORTH;  // 0
    uint8_t east = NavigateToGoal::Goal::DIRECTION_EAST;    // 1

GetRobotStatus.srv
"""""""""""""""""""

Create ``srv/GetRobotStatus.srv`` with the following content:

.. code-block:: text

    # =============================================================================
    # GetRobotStatus.srv
    # Service for querying the current state of the MicroMouse robot
    # =============================================================================

    # ---- CONSTANTS for Direction ----
    # String representations of robot facing direction
    string DIRECTION_NORTH = "NORTH"
    string DIRECTION_EAST = "EAST"
    string DIRECTION_SOUTH = "SOUTH"
    string DIRECTION_WEST = "WEST"

    # ---- REQUEST ----
    # No request parameters needed - this is a status query
    ---
    # ---- RESPONSE ----
    # Complete snapshot of robot state at the time of the request
    int32 position_x            # Current X coordinate (column)
    int32 position_y            # Current Y coordinate (row)
    string direction            # Facing direction (use DIRECTION_* constants)
    int32 steps_taken           # Number of moves made so far
    int32 steps_to_goal_estimate # Manhattan distance to goal (|dx| + |dy|)
    float64 elapsed_seconds     # Time since navigation started
    bool is_running             # True if navigation is in progress
    bool success                # True if goal has been reached
    string message              # Status message or error description

**Field Descriptions:**

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Field
     - Purpose
   * - ``position_x``, ``position_y``
     - Robot's current cell coordinates in the maze grid.
   * - ``direction``
     - Robot's facing direction as a string ("NORTH", "EAST", "SOUTH", "WEST"). Use the defined constants for consistency.
   * - ``steps_taken``
     - Total number of forward movements executed since navigation began.
   * - ``steps_to_goal_estimate``
     - Manhattan distance from current position to goal: ``|goal_x - position_x| + |goal_y - position_y|``. This is an optimistic estimate (actual path may be longer due to walls).
   * - ``elapsed_seconds``
     - Time in seconds since the navigation started.
   * - ``is_running``
     - ``true`` if the robot is actively navigating, ``false`` if idle or finished.
   * - ``success``
     - ``true`` if the robot has successfully reached the goal, ``false`` otherwise.
   * - ``message``
     - Human-readable status such as "Navigating...", "Goal reached!", or "Waiting for goal".

**Using Constants in C++:**

.. code-block:: cpp

    #include "micromouse_interfaces/srv/get_robot_status.hpp"
    
    using GetRobotStatus = micromouse_interfaces::srv::GetRobotStatus;
    
    // In service callback
    response->direction = GetRobotStatus::Response::DIRECTION_NORTH;

CMakeLists.txt for micromouse_interfaces
"""""""""""""""""""""""""""""""""""""""""

.. todo::
 
    Update the content (refer to lecture slides)



package.xml for micromouse_interfaces
""""""""""""""""""""""""""""""""""""""

.. todo::
 
    Update the content (refer to lecture slides)

**Verification:**

.. code-block:: bash

    colcon build --packages-select micromouse_interfaces
    source install/setup.bash
    ros2 interface show micromouse_interfaces/action/NavigateToGoal
    ros2 interface show micromouse_interfaces/srv/GetRobotStatus

Task 2: Create ``params.yaml`` (10 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. todo::
 
    Create ``config/params.yaml`` in the ``micromouse_cpp`` package with the following parameters:


.. list-table::
   :widths: 25 15 60
   :header-rows: 1
   :class: compact-table

   * - Parameter
     - Type
     - Description
   * - ``goal_x``
     - int
     - Target cell X coordinate (default: 7). Used in standalone mode.
   * - ``goal_y``
     - int
     - Target cell Y coordinate (default: 7). Used in standalone mode.
   * - ``path_color``
     - string
     - MMS color code for path visualization.
   * - ``goal_color``
     - string
     - MMS color code for goal cell. 
   * - ``standalone_mode``
     - bool
     - Execution mode. Can be overridden via command line.

**Available MMS Colors:** ``r`` (red), ``g`` (green), ``b`` (blue), ``c`` (cyan), ``y`` (yellow), ``o`` (orange), ``G`` (dark green), ``B`` (dark blue)

Task 3: Implement Topic Publisher (5 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``micromouse_node.cpp``, implement the robot position publisher using ``geometry_msgs::msg::Point``.

**In constructor:**

- Create a publisher for topic ``/robot_position``
- Message type: ``geometry_msgs::msg::Point``
- QoS: 10

**In** ``publish_position()``:

- Create a ``Point`` message
- Set ``x`` = robot x position (cast to double)
- Set ``y`` = robot y position (cast to double)
- Set ``z`` = facing direction (cast to double, encodes N=0, E=1, S=2, W=3)
- Publish the message

.. note::

   We use ``geometry_msgs::msg::Point`` for simplicity. The ``z`` field is repurposed to encode the robot's facing direction since ``Point`` only has x, y, z fields.

**Verification:**

.. code-block:: bash

    # In a separate terminal while navigation is running:
    ros2 topic echo /robot_position

Task 4: Implement Action Server Callbacks (25 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``micromouse_node.cpp``, implement the navigation action server.

**In constructor:**

- Create an action server for ``/navigate_to_goal``
- Action type: ``NavigateToGoal``
- Callbacks: ``handle_goal``, ``handle_cancel``, ``handle_accepted``

**Implement callbacks:**

- ``handle_goal()``: Log the goal coordinates, return ``ACCEPT_AND_EXECUTE``
- ``handle_cancel()``: Log cancellation request, return ``ACCEPT``
- ``handle_accepted()``: Start ``execute_action`` in a detached thread

**In feedback publishing (already in provided code):**

- Use the action constants for direction (e.g., ``NavigateToGoal::Goal::DIRECTION_NORTH``)

.. hint::

    .. code-block:: cpp
    
        action_server_ = rclcpp_action::create_server<NavigateToGoal>(
            this,
            "/navigate_to_goal",
            std::bind(&MicroMouseNode::handle_goal, this, _1, _2),
            std::bind(&MicroMouseNode::handle_cancel, this, _1),
            std::bind(&MicroMouseNode::handle_accepted, this, _1));

**Verification (using CLI):**

.. code-block:: bash

    # With MMS running in action mode (standalone_mode:=false):
    ros2 action send_goal /navigate_to_goal micromouse_interfaces/action/NavigateToGoal \
        "{goal_x: 7, goal_y: 7}" --feedback

Task 5: Implement Action Client (20 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``navigate_action_client.cpp``, implement the action client callbacks.

**Implement** ``send_goal()``:

1. Wait for action server (10s timeout)
2. Create goal message from parameters
3. Set up ``SendGoalOptions`` with callbacks
4. Call ``async_send_goal``

**Implement callbacks:**

- ``goal_response_callback()``: Check if goal accepted, store goal handle, log result
- ``feedback_callback()``: Log position, direction (use constants), elapsed time
- ``result_callback()``: Clear goal handle, log result code and details, shutdown node

.. note::

   **Ctrl+C Cancellation (PROVIDED)**
   
   The signal handler for Ctrl+C cancellation is **fully provided** in the starter code. This includes:
   
   - ``signal_handler()`` — Catches SIGINT (Ctrl+C) and forwards to ``cancel_goal()``
   - ``cancel_goal()`` — Sends cancel request to the action server
   - ``goal_handle_`` member — Stores the goal handle for cancellation support
   
   You must still implement ``goal_response_callback()`` to **store the goal handle** in ``goal_handle_``, and ``result_callback()`` to **clear the goal handle** (set to ``nullptr``). Without these, cancellation will not work.

**Verification:**

.. code-block:: bash

    # Terminal 1: Start MMS with standalone_mode:=false
    
    # Terminal 2: Run the action client
    ros2 run micromouse_cpp navigate_action_client --ros-args -p goal_x:=7 -p goal_y:=7

**Testing Cancellation:**

To verify that Ctrl+C cancellation works correctly:

.. code-block:: bash

    # Terminal 1: Start MMS with standalone_mode:=false
    
    # Terminal 2: Send a goal to a distant location
    ros2 run micromouse_cpp navigate_action_client --ros-args -p goal_x:=15 -p goal_y:=15
    
    # While robot is navigating, press Ctrl+C in Terminal 2

**Expected behavior when pressing Ctrl+C:**

1. Action client logs: ``"Cancelling goal..."``
2. Action client logs: ``"=== NAVIGATION CANCELED ==="``
3. Result shows ``success: false`` and ``message: "Navigation cancelled"``
4. Robot stops navigating in MMS
5. Node shuts down gracefully

.. warning::

   If pressing Ctrl+C causes the client to exit immediately **without** sending a cancel request (robot keeps moving), check that:
   
   - ``goal_handle_`` is stored in ``goal_response_callback()``
   - ``goal_handle_`` is cleared in ``result_callback()``

Task 6: Implement Service Client (15 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``get_status_client.cpp``, implement the service client as a standalone ROS2 node.

**In constructor:**

- Create a service client for ``/get_robot_status``
- Service type: ``GetRobotStatus``

**Implement** ``send_request()``:

1. Wait for service to be available (5s timeout)
2. If not available, log warning and return
3. Create a request (empty for this service)
4. Call ``async_send_request`` with callback

**Implement** ``response_callback()``:

- Get the response from the future
- Log all response fields
- Call ``rclcpp::shutdown()`` to end the node

**Verification:**

.. code-block:: bash

    # While navigation is running in MMS:
    ros2 run micromouse_cpp get_status_client

---------------------------------------------------------
Execution Modes
---------------------------------------------------------

The system supports two execution modes controlled by the ``standalone_mode`` parameter:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Mode
     - ``standalone_mode``
     - Behavior
   * - Standalone
     - ``true``
     - Robot navigates immediately using ``goal_x``/``goal_y`` from `params.yaml`
   * - Action
     - ``false``
     - Robot waits for action client to send goal; provides feedback during navigation

.. warning::

   **Both modes must work correctly!** Your implementation will be tested in both standalone and action modes. Ensure that:
   
   - In standalone mode: Robot navigates using parameter values, topic publishes position
   - In action mode: Robot waits for goal, publishes feedback, returns result

---------------------------------------------------------
Running the System
---------------------------------------------------------

Building the Packages
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    cd ~/ros2_ws
    colcon build --packages-select micromouse_interfaces micromouse_cpp
    source install/setup.bash

Standalone Mode (Immediate Navigation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Configure MMS Run Command with ``standalone_mode:=true``:

   .. code-block:: bash
   
       ros2 run micromouse_cpp micromouse_node --ros-args \
           -p standalone_mode:=true \
           --params-file /absolute/path/to/params.yaml

2. Start MMS → Robot navigates immediately

3. Monitor in separate terminals:

   .. code-block:: bash
   
       # Terminal 2: Watch robot position
       ros2 topic echo /robot_position
       
       # Terminal 3: Query robot status
       ros2 run micromouse_cpp get_status_client
       
  
Action Mode (Client-Triggered Navigation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Configure MMS Run Command with ``standalone_mode:=false``:

   .. code-block:: bash
   
       ros2 run micromouse_cpp micromouse_node --ros-args \
           -p standalone_mode:=false \
           --params-file /absolute/path/to/params.yaml

2. Start MMS → Robot waits for goal

3. Send goal using action client:

   .. code-block:: bash
   
       # Using the action client node:
       ros2 run micromouse_cpp navigate_action_client --ros-args \
           -p goal_x:=7 -p goal_y:=7

4. Monitor in separate terminals:

   .. code-block:: bash
   
       # Terminal 2: Watch robot position
       ros2 topic echo /robot_position
       
       # Terminal 3: Query robot status
       ros2 run micromouse_cpp get_status_client

5. Test cancellation (press Ctrl+C in the action client terminal):

   .. code-block:: bash
   
       # While robot is navigating, press Ctrl+C
       # Expected output:
       # [INFO] Cancelling goal...
       # [WARN] === NAVIGATION CANCELED ===
       # [INFO] Result:
       # [INFO]   Success: false
       # [INFO]   Message: Navigation cancelled

---------------------------------------------------------
Demo Video
---------------------------------------------------------

Watch the demonstration video to see the expected behavior:

🎥 `MicroMouse ROS2 Demo Video <https://drive.google.com/file/d/1HK9yq_aKyOCe_Via429ekpd6PcMsQt5u/view?usp=sharing>`_

The video demonstrates:

1. Building the packages
2. Configuring MMS with the run command
3. Running in standalone mode
4. Running in action mode (with feedback)
5. Monitoring topic
6. Using the service client to query status
7. Cancelling navigation with Ctrl+C

---------------------------------------------------------
Provided Code
---------------------------------------------------------

The following components are **provided** and should **not be modified**:

- ``maze_control_api.hpp/cpp`` — MMS communication via stdin/stdout
- ``execute_with_replanning()`` — DFS navigation algorithm with replanning
- ``dfs_plan()`` — Path planning using Depth-First Search
- Wall sensing and movement functions
- **Service server** — ``/get_robot_status`` service is fully implemented
- **Signal handler** — Ctrl+C cancellation in action client (``signal_handler()``, ``cancel_goal()``)
- Main function structure
- Header files for action client and service client

---------------------------------------------------------
Submission
---------------------------------------------------------

Submit Format
^^^^^^^^^^^^^

Submit a single zipped file named:

.. code-block:: text

    groupX_micromouse_ros2.zip

Where ``X`` is your group number.

Submission Checklist
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 10 90
   :class: compact-table

   * - [ ]
     - File named correctly as ``groupX_micromouse_ros2.zip``
   * - [ ]
     - ``micromouse_interfaces`` package with action and service definitions (with constants)
   * - [ ]
     - ``params.yaml`` with all required parameters
   * - [ ]
     - Topic publisher implemented and working
   * - [ ]
     - Action server callbacks implemented with feedback using constants
   * - [ ]
     - Action client implemented and receiving feedback
   * - [ ]
     - Action client Ctrl+C cancellation works (robot stops, result shows CANCELED)
   * - [ ]
     - Service client implemented and receiving response
   * - [ ]
     - Project builds cleanly with ``colcon build``
   * - [ ]
     - Navigation works in **both** standalone and action modes
   * - [ ]
     - Code follows C++ best practices and ROS2 conventions
   * - [ ]
     - Group members' names in both `package.xml` (remove my name)

---------------------------------------------------------
Grading Rubric
---------------------------------------------------------

**Total:** 100 points

.. list-table::
   :widths: 50 15 35
   :header-rows: 1
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - ``micromouse_interfaces`` Package
     - 25 pts
     - Action and service definitions with constants; builds successfully; ``ros2 interface show`` works
   * - ``params.yaml``
     - 10 pts
     - All parameters defined with correct types; YAML syntax correct; node loads parameters
   * - Topic Publisher
     - 5 pts
     - Publisher created correctly; ``publish_position()`` implemented; data visible on topic
   * - Action Server Callbacks
     - 25 pts
     - All three callbacks implemented; goal acceptance works; feedback uses constants; result sent
   * - Action Client
     - 20 pts
     - All callbacks implemented; goal sent successfully; feedback logged with constants; Ctrl+C cancellation works; result handled
   * - Service Client
     - 15 pts
     - Client created; request sent; response logged correctly; runs as standalone node

**Point Deductions:**

- Build errors: Up to -20 pts
- Runtime errors/crashes: Up to -15 pts
- Not using constants from interfaces: -5 pts
- Only works in one mode (standalone or action): -15 pts
- Poor code style/documentation: Up to -10 pts
- Late submission: Per course policy

---------------------------------------------------------
Command Reference
---------------------------------------------------------

Building
^^^^^^^^^

.. code-block:: bash

    cd ~/ros2_ws
    colcon build --packages-select micromouse_interfaces micromouse_cpp
    source install/setup.bash

Checking Interfaces
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    ros2 interface show micromouse_interfaces/action/NavigateToGoal
    ros2 interface show micromouse_interfaces/srv/GetRobotStatus

Running Nodes
^^^^^^^^^^^^^^

.. code-block:: bash

    # Main node - standalone mode (via MMS)
    ros2 run micromouse_cpp micromouse_node --ros-args \
        -p standalone_mode:=true \
        --params-file /path/to/params.yaml
    
    # Main node - action mode (via MMS)
    ros2 run micromouse_cpp micromouse_node --ros-args \
        -p standalone_mode:=false \
        --params-file /path/to/params.yaml
    
    # Action client (press Ctrl+C to cancel navigation)
    ros2 run micromouse_cpp navigate_action_client --ros-args \
        -p goal_x:=7 -p goal_y:=7
    
    # Service client
    ros2 run micromouse_cpp get_status_client

Topic Commands
^^^^^^^^^^^^^^^

.. code-block:: bash

    ros2 topic list
    ros2 topic echo /robot_position

Service Commands
^^^^^^^^^^^^^^^^^

.. code-block:: bash

    ros2 service list
    ros2 service call /get_robot_status micromouse_interfaces/srv/GetRobotStatus "{}"

Action Commands
^^^^^^^^^^^^^^^^

.. code-block:: bash

    ros2 action list
    ros2 action info /navigate_to_goal
    ros2 action send_goal /navigate_to_goal \
        micromouse_interfaces/action/NavigateToGoal \
        "{goal_x: 7, goal_y: 7}" --feedback

Node Inspection
^^^^^^^^^^^^^^^^

.. code-block:: bash

    ros2 node list
    ros2 node info /micromouse_node

---------------------------------------------------------
Resources
---------------------------------------------------------

- `ROS2 Parameters Tutorial <https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters.html>`_
- `ROS2 Topics Tutorial <https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics.html>`_
- `ROS2 Services Tutorial <https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services.html>`_
- `ROS2 Actions Tutorial <https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Cpp.html>`_
- `Creating Custom Interfaces <https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html>`_
- `Interface Definition <https://docs.ros.org/en/humble/Concepts/About-ROS-Interfaces.html>`_