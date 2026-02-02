.. default-domain:: cpp
.. _final_project_micromouse_cpp:

=========================================================
Assignment 4
=========================================================

.. admonition:: Changelog
   :class: changelog
   
   - **v3.0 (11/12/2025)** — Added demo for the backtracking mechanism.
   - **v2.0 (11/12/2025)** — Updated figures.
   - **v1.0 (11/07/2025)** — Initial release of Assignment 4 instructions.

.. admonition:: Resources
   :class: resources


   - ⚙️ `Starter Code (rwa4_starter) <https://github.com/zeidk/enpm702-fall-2025/tree/main/rwa4_starter>`_
   - 🔗 `MicroMouse Simulator (main) <https://github.com/mackorone/mms>`_
   - 🔗 `MicroMouse Simulator (API) <https://github.com/mackorone/mms#mouse-api>`_
   - 🔗 `MicroMouse Simulator (maze files) <https://github.com/mackorone/mms#maze-files>`_

**MicroMouse Robot Maze Navigation**

.. list-table::
   :widths: 20 30
   :stub-columns: 1
   :class: compact-table

   * - **Version**
     - v3.0
   * - **Due Date**
     - 11/27/2025
   * - **Points**
     - 50 pts + 5 bonus pts
   * - **Work Mode**
     - Group assignment
   * - **Language**
     - C++17



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

You will develop a C++ program that implements a **MicroMouse Robot Navigation System** for maze exploration. You are developing control software for a MicroMouse robot competing in `autonomous maze navigation <https://youtu.be/ZMQbHMgK2rw?si=FH-yd7i0Rrf44S3q>`_. The robot must efficiently navigate through an unknown warehouse-like 16x16 maze to reach one of the four center goal cells using sophisticated pathfinding algorithms and sensor systems. 

Your robot can be configured for different scanning approaches (minimal detection or comprehensive sensing), demonstrating how different configurations produce different behaviors. Your system must demonstrate well-designed object-oriented architecture with clear separation between navigation logic and shared resources.

**Key System Features:**

- **Aggregation** — Shared resources (maze, algorithm)
- **Encapsulation** — Proper data hiding and access control
- **Modular Design** — Separate systems working together cohesively
- **Configuration-Based Behavior** — Single robot class with multiple operational modes
- **Random Goal Selection** — Algorithm randomly selects one of four center goals for navigation

---------------------------------------------------------
Simulator
---------------------------------------------------------

Your program is required to interface with a graphical user interface simulator (`mms <https://github.com/mackorone/mms>`_). The simulator makes it easy to write and test maze-solving code without a physical robot.

Installation
^^^^^^^^^^^^^

.. todo::

    1. Download the `Linux precompiled version of the simulator <https://github.com/mackorone/mms/releases/download/v1.2.0/linux.zip>`_
    2. Unzip the file, which generates the `linux` folder
    3. ``cd <path to linux folder>``
    4. ``chmod +x mms-x86_64.AppImage``
    5. ``./mms-x86_64.AppImage --appimage-extract`` :math:`\rightarrow` creates the folder `squashfs-root`
    6. ``cd squashfs-root``
    7. ``chmod +x mms``
    8. ``./mms``
    9. The simulator should start (we will refer to this window as the `mms` window)

.. only:: html

   .. raw:: html

      <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
        <img src="../_static/rwa4/simulator_start.png"
             alt="Simulator"
             class="only-light"
             style="width:100%; border-radius:8px;">
        <img src="../_static/rwa4/simulator_start.png"
             alt="Simulator"
             class="only-dark"
             style="width:100%; border-radius:8px;">
      </div>

Maze Files
^^^^^^^^^^^^

The simulator only provides the graphical user interface and functionalities to interact with your code. You will also need maze files. In order to use a maze in the simulator, it must be:

- Nonempty
- Rectangular
- Fully enclosed
- Also note that official Micromouse mazes have additional requirements:

  - No inaccessible locations
  - Exactly three starting walls
  - Only one entrance to the center
  - Has a hollow center, i.e., the center peg has no walls attached to it
  - Has walls attached to every peg except the center peg
  - Is unsolvable by a wall-following robot

.. todo::
 
    - Download maze files:
    
        - Follow `instructions <https://github.com/mackorone/mms?tab=readme-ov-file#maze-files>`_ to retrieve the maze files.
        - or ``git clone https://github.com/micromouseonline/mazefiles.git``
    
    - Load maze files in the simulator.

        - Click the 🗂️ icon from the `mms` window
        - Navigate to the maze folder you cloned earlier
        - Select any file from `mazefiles` :math:`\rightarrow` `classic`

Build and Run
^^^^^^^^^^^^^^

.. todo::
 
    - Click on the + symbol to configure the simulator :math:`\rightarrow` `Edit Mouse Algorithm` window.
    
        .. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/config_mms.png"
                    alt="Configuration"
                    class="only-light"
                    style="width:100%; border-radius:8px;">
                <img src="../_static/rwa4/config_mms.png"
                    alt="Configuration"
                    class="only-dark"
                    style="width:100%; border-radius:8px;">
            </div>
        
        - **Name:** Give a name to this configuration
        - **Directory:** Provide absolute path to your executable (inside the `build` folder)
        - **Build Command:** I suugest you leave this empty. We will build the project in Visual Studio Code. If you prefer to build the whole project from the simulator, you will need to enter the whole ``g++`` command.
        - **Run Command:** Name of the executable. The simulator will try to run it using the path provided in the **Directory** field.
        - Click OK
        - Write and build the project in Visual Studio Code
        - Click `Run` (`mms` window)

Simulator API Reference
^^^^^^^^^^^^^^^^^^^^^^^^^

The simulator provides an Application Programming Interface (API) that enables interaction between your code and the simulator.

The original API is available on GitHub:
`API.h <https://github.com/mackorone/mms-cpp/blob/master/API.h>`_.

For this assignment, the API has been modified to adhere to consistent class and attribute naming conventions, and it is encapsulated within the `micro_mouse` namespace.
The modified API interface is defined in `maze_api.hpp`, and its corresponding implementation resides in `maze_api.cpp`.

An overview of the provided API is summarized below:

.. code-block:: cpp
   :linenos:

    #pragma once
    #include <string>

    namespace micro_mouse {

    /**
    * @brief API for controlling and interacting with a maze environment
    *
    * This class provides methods to navigate through a maze, query maze
    * properties, manipulate walls, set colors and text, and handle reset events.
    */
    class MazeControlAPI {
    public:
    /**
    * @brief Get the width of the maze
    * @return The width of the maze in cells
    */
    static int get_maze_width();

    /**
    * @brief Get the height of the maze
    * @return The height of the maze in cells
    */
    static int get_maze_height();

    /**
    * @brief Check if there is a wall in front of the current position
    * @return true if there is a wall in front, false otherwise
    */
    static bool has_wall_front();

    /**
    * @brief Check if there is a wall to the right of the current position
    * @return true if there is a wall to the right, false otherwise
    */
    static bool has_wall_right();

    /**
    * @brief Check if there is a wall to the left of the current position
    * @return true if there is a wall to the left, false otherwise
    */
    static bool has_wall_left();

    /**
    * @brief Move forward in the maze
    * @param distance Number of cells to move forward (default: 1)
    */
    static void move_forward(int distance = 1);

    /**
    * @brief Turn right (clockwise) in the maze
    */
    static void turn_right();

    /**
    * @brief Turn left (counter-clockwise) in the maze
    */
    static void turn_left();

    /**
    * @brief Set a wall at the specified position and direction
    * @param x X coordinate of the cell
    * @param y Y coordinate of the cell
    * @param direction Direction of the wall ('n', 's', 'e', 'w' for north,
    * south, east, west)
    */
    static void set_wall(int x, int y, char direction);

    /**
    * @brief Clear a wall at the specified position and direction
    * @param x X coordinate of the cell
    * @param y Y coordinate of the cell
    * @param direction Direction of the wall ('n', 's', 'e', 'w' for north,
    * south, east, west)
    */
    static void clear_wall(int x, int y, char direction);

    /**
    * @brief Set the color of a cell in the maze
    * @param x X coordinate of the cell
    * @param y Y coordinate of the cell
    * @param color Color character identifier
    */
    static void set_color(int x, int y, char color);

    /**
    * @brief Clear the color of a cell in the maze
    * @param x X coordinate of the cell
    * @param y Y coordinate of the cell
    */
    static void clear_color(int x, int y);

    /**
    * @brief Clear all colors from the entire maze
    */
    static void clear_all_color();

    /**
    * @brief Set text at the specified cell in the maze
    * @param x X coordinate of the cell
    * @param y Y coordinate of the cell
    * @param text Text string to display at the cell
    */
    static void set_text(int x, int y, const std::string &text);

    /**
    * @brief Clear text from the specified cell in the maze
    * @param x X coordinate of the cell
    * @param y Y coordinate of the cell
    */
    static void clear_text(int x, int y);

    /**
    * @brief Clear all text from the entire maze
    */
    static void clear_all_text();

    /**
    * @brief Check if the maze was reset
    * @return true if the maze was reset, false otherwise
    */
    static bool was_reset();

    /**
    * @brief Acknowledge that the reset has been handled
    */
    static void ack_reset();

    /**
    * @brief Print a message in the simulator
    * To print anything in the simulator, use std::cerr
    * @param text
    */
    static void log(std::string_view text);

    }; // class MazeControlAPI

    } // namespace maze

.. warning::
   
   DO NOT MODIFY the provided API implementation. Your code should only call these static methods through the maze class wrapper methods. The API handles communication with the simulator through standard input/output streams.

.. note::

    Algorithms communicate with the simulator via stdin/stdout. To issue a command, simply print to stdout. To read a response, simply read from stdin. All valid commands are listed below. Invalid commands are simply ignored.

    - `std::cout` sends commands to the simulator
    - `std::cin` reads commands from the simulator
    - `std::cerr` prints in the simulator's main window

.. todo::
 
    The starter package provides a simple left-wall follower. This is just for demonstration purpose as the robot is not expected to reach the center of the maze (due to the nature of the mazes).

    .. code-block:: cpp
       :linenos:

        #include <iostream>
        #include <string>

        #include "maze_api.hpp"

        void log(const std::string& text) {
          std::cerr << text << std::endl;
        }

        using MMS = micro_mouse::MazeControlAPI;

        int main() {
          log("Running...");
          MMS::set_color(0, 0, 'G');
          MMS::set_text(0, 0, "S");
          
          MMS::set_text(7, 7, "(7,7)");
          MMS::set_text(7, 8, "(7,8)");
          MMS::set_text(8, 7, "(8,7)");
          MMS::set_text(8, 8, "(8,8)");
          MMS::set_color(7, 7, 'y');
          MMS::set_color(7, 8, 'y');
          MMS::set_color(8, 7, 'y');
          MMS::set_color(8, 8, 'y');
          while (true) {
            if (!MMS::has_wall_left()) {
              MMS::turn_left();
            }
            while (MMS::has_wall_front()) {
              MMS::turn_right();
            }
            MMS::move_forward();
          }
        }

---------------------------------------------------------
DFS Algorithm: Tree-Based Path Finding
---------------------------------------------------------

Maze pathfinding can be conceptualized as a tree traversal problem, where the starting position serves as the root node and the goal position represents a target leaf. Each cell in the maze corresponds to a node in the tree structure, with accessible adjacent cells forming the children of the current node.

This assignment focuses on implementing a depth-first search (DFS) algorithm for maze navigation. While DFS provides a systematic approach to exploring all possible paths, it does not guarantee optimal solutions and typically does not produce the shortest route to the destination.

Algorithm Behavior
^^^^^^^^^^^^^^^^^^^^

The DFS algorithm operates by starting at the root node and exploring each branch to its maximum depth before backtracking to explore alternative paths. This exhaustive exploration strategy ensures that all reachable nodes are eventually visited, though not necessarily in the most efficient order.

The key characteristic of DFS is its commitment to exploring as deeply as possible along each path before considering alternatives. When the algorithm encounters a dead end or reaches a previously visited node, it backtracks to the most recent node with unexplored neighbors and continues the search from there.

Goal Selection
^^^^^^^^^^^^^^^^

The maze contains four goal cells located at the center: (7,7), (7,8), (8,7), and (8,8). Before beginning navigation, the algorithm must randomly select one of these four cells as the target destination. This random selection ensures that different runs may have different objectives, adding variability to the navigation demonstration.

Search Order Protocol
^^^^^^^^^^^^^^^^^^^^^^^

To maintain consistency in maze traversal, the following directional priority sequence must be followed:

1. **North** (↑) — First priority direction
2. **East** (→) — Second priority direction
3. **South** (↓) — Third priority direction
4. **West** (←) — Fourth priority direction

This ordering ensures deterministic behavior across different implementations and makes debugging more predictable. The algorithm will always attempt to move North first when multiple directions are available.





Implementation Details
^^^^^^^^^^^^^^^^^^^^^^^^

DFS can be implemented using stacks with the last-in-first-out (LIFO) approach. The stack maintains the current exploration path and facilitates backtracking when dead ends are encountered. During traversal, nodes are pushed onto the stack when exploring new paths and popped during backtracking when no further progress is possible.

A list of visited nodes is essential to prevent infinite cycles and ensure each node is processed only once. Without this mechanism, the algorithm could become trapped in loops, especially in maze configurations with multiple paths between the same locations.

In C++, `std::stack <https://en.cppreference.com/w/cpp/container/stack>`_ provides the LIFO data structure for maintaining the exploration path, while `std::set <https://en.cppreference.com/w/cpp/container/set>`_ serves as the visited nodes collection. The algorithm begins at the start node and systematically explores all possible paths until it either reaches the goal node or exhausts all reachable nodes.

Performance Considerations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The choice of ``std::set`` over ``std::vector`` for tracking visited nodes is crucial for performance. The algorithm frequently performs two operations on the visited collection: checking if a node has been visited and marking a node as visited. The following table demonstrates the significant performance difference between these data structures.


.. list-table:: Performance comparison of container types for visited node tracking
   :widths: 30 35 35
   :stub-columns: 1
   :class: compact-table

   * - **Operation**
     - **std::vector**
     - **std::set**
   * - Lookup ("is visited?")
     - O(n) — linear search
     - O(log n) — tree search
   * - Insert ("mark visited")
     - O(1) — push_back
     - O(log n) — tree insertion
   * - **Overall Impact**
     - Gets slower as maze grows
     - Stays efficient

The critical operation "is this node already visited?" occurs frequently during maze traversal. With ``std::vector``, this requires searching through all previously visited nodes, creating a performance bottleneck that worsens as the maze size increases. In contrast, ``std::set`` provides logarithmic lookup time and automatically prevents duplicate entries, making it the optimal choice for this application. For large mazes containing thousands of nodes, this performance difference becomes substantial and can significantly impact the algorithm's execution time.

Pseudocode
^^^^^^^^^^^

The iterative implementation of DFS uses explicit stack management to simulate the recursive call stack. The following pseudocode presents the complete approach:

.. prf:algorithm:: Depth-First Search for Maze Solving
   :label: dfs-maze-search

   **Inputs:** 

   - :math:`s` (stack of nodes, initially empty)
   - :math:`v` (list of visited nodes, initially empty)
   - :math:`m_{maze}` (2D array representing the maze)
   - :math:`m_{goal}` (goal node coordinates)
   - :math:`m_{start}` (start node coordinates)
   
   **Output:** true if a path to goal is found, otherwise false

   1. :math:`s.\text{push}(m_{start})`
   
   2. **while** not :math:`s.\text{empty}()` **do**
   
      a. :math:`n \gets s.\text{top}()` (examine current node without removing it)
      
      b. **if** :math:`n = m_{goal}` **then** return **true** (goal found)
      
      c. **if** :math:`n \in v` **then** (node already explored)
      
         i. :math:`s.\text{pop}()` (backtrack: remove dead end)
         
         ii. **continue**
      
      d. :math:`v.\text{insert}(n)` (mark current node as visited)
      
      e. :math:`moved \gets \text{false}`
      
      f. **if** :math:`m_{maze}[n.x][n.y+1]` is valid and :math:`(n.x, n.y+1) \notin v` **then** (check North)
      
         i. :math:`neighbor.x \gets n.x, neighbor.y \gets n.y + 1`
         
         ii. :math:`s.\text{push}(neighbor), moved \gets \text{true}`
      
      g. **else if** :math:`m_{maze}[n.x+1][n.y]` is valid and :math:`(n.x+1, n.y) \notin v` **then** (check East)
      
         i. :math:`neighbor.x \gets n.x + 1, neighbor.y \gets n.y`
         
         ii. :math:`s.\text{push}(neighbor), moved \gets \text{true}`
      
      h. **else if** :math:`m_{maze}[n.x][n.y-1]` is valid and :math:`(n.x, n.y-1) \notin v` **then** (check South)
      
         i. :math:`neighbor.x \gets n.x, neighbor.y \gets n.y - 1`
         
         ii. :math:`s.\text{push}(neighbor), moved \gets \text{true}`
      
      i. **else if** :math:`m_{maze}[n.x-1][n.y]` is valid and :math:`(n.x-1, n.y) \notin v` **then** (check West)
      
         i. :math:`neighbor.x \gets n.x - 1, neighbor.y \gets n.y`
         
         ii. :math:`s.\text{push}(neighbor), moved \gets \text{true}`
      
      j. **if** not :math:`moved` **then** :math:`s.\text{pop}()` (backtrack)
   
   3. **return** false (all reachable nodes explored, goal not found)



Demonstration
"""""""""""""""

This section presents a visual example using a simple 4x4 maze. The depth-first search (DFS) algorithm begins at position (0, 0) and aims to reach the goal at position (2, 2). The exploration priority is defined as follows: (1) North, (2) East, (3) South, and (4) West. The algorithm has prior knowledge only of the maze's perimeter walls.

Iteration 1
~~~~~~~~~~~~~~

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/i1_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:40%; border-radius:8px;">
                <img src="../_static/rwa4/i1_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:40%; border-radius:8px;">
            </div>


.. admonition:: Demo
   :class: leftline

   - :math:`s=[(0,0)]`
   - :math:`n=(0,0)`
   - :math:`v=[(0,0)]`


Iteration 2
~~~~~~~~~~~~~~

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/i2_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:40%; border-radius:8px;">
                <img src="../_static/rwa4/i2_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:40%; border-radius:8px;">
            </div>


.. admonition:: Demo
   :class: leftline

   - :math:`s=[(0,1),(0,0)]`
   - :math:`n=(0,1)`
   - :math:`v=[(0,0),(0,1)]`

Iteration 4
~~~~~~~~~~~~~~

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/i4_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:40%; border-radius:8px;">
                <img src="../_static/rwa4/i4_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:40%; border-radius:8px;">
            </div>

.. admonition:: Demo
   :class: leftline

   - :math:`s=[(0,3),(0,2),(0,1),(0,0)]`
   - :math:`n=(0,3)`
   - :math:`v=[(0,0),(0,1),(0,2),(0,3)]`

Iteration 5
~~~~~~~~~~~~~~

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/i5_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:40%; border-radius:8px;">
                <img src="../_static/rwa4/i5_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:40%; border-radius:8px;">
            </div>

.. admonition:: Demo
   :class: leftline

   - :math:`s=[(1,3),(0,3),(0,2),(0,1),(0,0)]`
   - :math:`n=(1,3)`
   - :math:`v=[(0,0),(0,1),(0,2),(0,3),(1,3)]`

Iteration 13
~~~~~~~~~~~~~~

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/i13_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:40%; border-radius:8px;">
                <img src="../_static/rwa4/i13_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:40%; border-radius:8px;">
            </div>

.. admonition:: Demo
   :class: leftline

   - :math:`s=[(2,2),...,(3,3),(2,3),(1,3),(0,3),(0,2),(0,1),(0,0)]`
   - :math:`n=(2,2)`
   - :math:`v=[(0,0),(0,1),(0,2),(0,3),(1,3),(2,3),(3,3),...,(2,1)]`

Path Following
^^^^^^^^^^^^^^^^^

.. note::
   
   At the conclusion of the algorithm, the stack :math:`s` holds the sequence of nodes from the goal back to the start. To obtain the correct path from start to goal, this stack must be reversed.


.. prf:algorithm:: Path-Follow with Conditional Replan
   :label: follow-conditional-replan

   **Inputs:**
   
   - :math:`s` — stack representing the current path from start to goal
   - `maze_` — internal maze representation
   - `API` — simulator interface

   **Output:** Updated path :math:`s` and synchronized maze state

   1. **for each** cell :math:`c \in s` **do**
   
      a. Move robot to :math:`c`
      
      b. Sense walls :math:`D = \{\text{front}, \text{left}, \text{right}\}` :code:`// Use` :code:`has_wall_front()`, :code:`has_wall_right()`, :code:`has_wall_left()`

      
      c. **for each** direction :math:`d \in D` **where a wall is detected do**
         
         i. Update `maze_(c, d)` to mark a wall
         
         ii. Use the `API` to synchronize visualization :code:`// Use` :code:`set_wall(int x, int y, char direction)`
         
      d. Let :math:`E_{\text{new}}` be the set of edges blocked by any newly detected wall
      
      e. Let :math:`P_{\text{rem}}` be the set of edges on the remaining path in :math:`s` (from :math:`c` to goal)
      
      f. **if** :math:`E_{\text{new}} \cap P_{\text{rem}} \neq \varnothing` **then** :code:`// if a newly detected wall blocks part of the path we intended to follow`
         
         i. :math:`s \gets \text{DFS}(\text{current}=c, \text{goal}, maze\_)` :code:`// recompute path`
         
         ii. **if** :math:`s = \varnothing` **then** return **false**
   
   2. **return** **true**

Demonstration
"""""""""""""""


.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/iterations_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:100%; border-radius:8px;">
                <img src="../_static/rwa4/iterations_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:100%; border-radius:8px;">
            </div>



Backtracking Mechanism
^^^^^^^^^^^^^^^^^^^^^^^^

When the algorithm reaches a position where no unvisited adjacent cells are available, the backtracking process begins. The algorithm retraces its steps along the current path, returning to previously visited nodes to identify unexplored branches. This systematic retreat continues until either:

1. An unvisited node is discovered along the backtracked path
2. All possible paths from the current branch have been exhausted

The process ensures complete coverage of all accessible areas within the maze structure while maintaining the integrity of the search path. Backtracking is what allows DFS to explore all possible solutions systematically.


Demonstration
"""""""""""""""

DFS has reached a node requiring backtracking. The algorithm cannot move in any direction: North, East, and West are blocked by walls, while South leads to an already-visited node at :math:`(0,2) \in v`. DFS will backtrack to the previous node in the stack.


.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/backtracking1_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:30%; border-radius:8px;">
                <img src="../_static/rwa4/backtracking1_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:30%; border-radius:8px;">
            </div>


.. admonition:: Demo
   :class: leftline

   - :math:`s=[(0,3),(0,2),(0,1),(0,0)]`
   - :math:`n=(0,3)`
   - :math:`v=[(0,0),(0,1),(0,2),(0,3)]`
   - :math:`n \in v \rightarrow s.pop()`
   - new :math:`s[(0,2),(0,1),(0,0)]`

----

The algorithm cannot explore East or West due to walls, and cannot go North or South because these nodes have already been visited (:math:`(0,3) \in v` and :math:`(0,1) \in v`). DFS will backtrack to the previous node in the stack.

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/backtracking2_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:30%; border-radius:8px;">
                <img src="../_static/rwa4/backtracking2_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:30%; border-radius:8px;">
            </div>


.. admonition:: Demo
   :class: leftline

   - :math:`s=[(0,2),(0,1),(0,0)]`
   - :math:`n=(0,2)`
   - :math:`v=[(0,0),(0,1),(0,2),(0,3)]`
   - :math:`n \in v \rightarrow s.pop()`
   - new :math:`s[(0,1),(0,0)]`

----

The algorithm cannot explore East or West due to walls, and cannot go North or South because these nodes have already been visited (:math:`(0,2) \in v` and :math:`(0,0) \in v`). DFS will backtrack to the previous node in the stack.

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/backtracking3_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:30%; border-radius:8px;">
                <img src="../_static/rwa4/backtracking3_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:30%; border-radius:8px;">
            </div>


.. admonition:: Demo
   :class: leftline

   - :math:`s=[(0,1),(0,0)]`
   - :math:`n=(0,1)`
   - :math:`v=[(0,0),(0,1),(0,2),(0,3)]`
   - :math:`n \in v \rightarrow s.pop()`
   - new :math:`s[(0,0)]`

----

The East branch has not been explored (:math:`(1,0) \notin v`). DFS will continue with this branch.

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/rwa4/backtracking4_light.png"
                    alt="Demo"
                    class="only-light"
                    style="width:30%; border-radius:8px;">
                <img src="../_static/rwa4/backtracking4_dark.png"
                    alt="Demo"
                    class="only-dark"
                    style="width:30%; border-radius:8px;">
            </div>

----------------
Design Phase
----------------

Before writing any code, you must design the architecture of your MicroMouse robot navigation system. The **Design Phase** focuses on transforming functional requirements into an object-oriented structure that clearly demonstrates **abstraction**, **inheritance**, **composition**, and **aggregation**.

This phase ensures that your implementation is modular, extensible, and aligned with sound software engineering practices.

Objectives
^^^^^^^^^^^

- Model the system architecture using a **UML Class Diagram**.
- Depict runtime interactions using a **UML Sequence Diagram**.
- Demonstrate **inheritance**, **composition**, and **aggregation** explicitly in your design.
- Implement **polymorphism** through an abstract base class :code:`Algorithm`.

Class Diagram
^^^^^^^^^^^^^^^^^^^^^^

Create a UML **class diagram** that represents the key structural components of your system.

**Required Elements:**

1. **Abstract Base Class**
   
   - Define an abstract class :code:`Algorithm` that declares common behaviors for maze-solving algorithms.
   - It must include at least one pure virtual method (e.g., :code:`virtual void solve() = 0;`).
   - Derived classes should implement different algorithms (e.g., :code:`DFSAlgorithm`, :code:`BFSAlgorithm`, or :code:`RandomWalkAlgorithm`).

2. **Inheritance**
   
   - Use inheritance to extend the base class :code:`Algorithm`.
   - Ensure each derived algorithm shares a consistent interface but provides its own behavior.
   - Example: both :code:`DFSAlgorithm` overrides :code:`solve()`.

3. **Composition**
   
   - Composition represents a **has-a** relationship where the *contained object cannot exist independently* of the containing class.
   - Example:

     - The :code:`Robot` **has a** :code:`Maze` object that represents the robot's internal understanding of the maze.
     - If the :code:`Robot` object is destroyed, its :code:`Maze` should also be destroyed.
     
   - UML Notation: **filled diamond (◆)** next to the owning class.
  

4. **Aggregation**
   
   - Aggregation represents a **“uses” or “has access to”** relationship where the associated object can exist independently.
   - Example:

     - The :code:`Robot` **uses** an :code:`Algorithm` object to navigate.
     - The :code:`Algorithm` may be shared between multiple robots or swapped at runtime.

   - UML Notation: **hollow diamond (◇)** next to the aggregate class.


Sequence Diagram
^^^^^^^^^^^^^^^^^^^^^^

Create a **sequence diagram** showing how objects interact during maze navigation.  
The diagram should illustrate **dynamic behavior** — the sequence of messages exchanged between the main system components.

**Required Scenario:**

- The :code:`Robot` initiates maze exploration.
- The :code:`Algorithm` computes the next move based on sensory input.
- The :code:`Maze` updates its internal map through composition.
- The :code:`MazeControlAPI` (simulator interface) updates the visualization.

**Expected Message Flow:**

1. :code:`Robot` calls :code:`Algorithm.solve()`.
2. :code:`Algorithm` requests maze information from :code:`Maze`.
3. :code:`Algorithm` determines the next move and instructs the :code:`Robot`.
4. :code:`Robot` calls :code:`MazeControlAPI::move_forward()` or other relevant API functions.
5. The :code:`Maze` updates wall information via :code:`set_wall(x, y, d)`.

Your sequence diagram must clearly depict method calls and object lifetimes, highlighting polymorphism when the :code:`Algorithm` instance refers to a derived class.

Submission Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Include **two UML diagrams**:
  
  - :code:`design_class_diagram.png` — Class Diagram  
  - :code:`design_sequence_diagram.png` — Sequence Diagram

.. note::
   
   Diagrams must follow standard UML notation and be legible.

Evaluation Criteria
^^^^^^^^^^^^^^^^^^^^^^

- Correct use of UML symbols and relationships.
- Accurate and meaningful application of inheritance, composition, and aggregation.
- Clear demonstration of polymorphism through the :code:`Algorithm` abstraction.
- Logical, modular, and well-organized class structure.
- Completeness and clarity of both diagrams.

--------------------------------
Implementation Phase
--------------------------------

The **Implementation Phase** focuses on translating your design into a fully functional C++ program. In this stage, you will implement all classes defined in your class diagram and ensure that the system behavior aligns with your sequence diagram. Your implementation must demonstrate a strong understanding of object-oriented programming (OOP) principles, including **encapsulation**, **inheritance**, **composition**, **aggregation**, and **polymorphism**.

Objectives
^^^^^^^^^^^^

- Implement all classes, relationships, and behaviors outlined in the design phase.
- Ensure clean modular separation between components.
- Apply abstraction through an abstract class that defines the algorithm interface.
- Demonstrate inheritance and polymorphism through derived algorithm classes.
- Properly implement composition and aggregation relationships as modeled.
- Maintain encapsulation and const-correctness throughout your code.

Implementation Overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your project should be organized according to the responsibilities of each class. Each component must serve a distinct purpose and align with your UML diagrams:

- The **Algorithm** hierarchy defines the abstract interface for all maze-solving strategies.  
- The **Robot** serves as the main controller that interacts with the maze and delegates navigation to a selected algorithm.  
- The **Maze** class acts as an internal model of the environment, encapsulating all communication with the simulator.  
- The **MazeControlAPI** (provided) handles simulator-level interactions and must only be accessed through the Maze wrapper.  

This structure enforces modularity and prevents direct dependencies on simulator internals.

Abstract Class and Polymorphism
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Define an abstract class representing a general maze-solving algorithm. This class must specify the interface shared by all algorithm implementations. Derived classes should override the relevant methods to implement their specific navigation logic.

Polymorphism must be demonstrated by allowing the robot to hold a reference or pointer to the abstract base class and to invoke derived algorithm implementations at runtime. This enables flexible switching between algorithms without altering the robot's logic.

Composition
^^^^^^^^^^^^^^^^^^^^^^^^

Composition represents a strong ownership relationship. In your design:

- The **Robot** must *own* its **Maze** instance.  
- The maze should not exist independently of the robot.  
- When the robot is destroyed, its maze is also destroyed.  

This relationship emphasizes that the maze is a core internal component of the robot’s state. All maze-related functionality, including sensing, wall updates, and visualization synchronization, must occur through this composition relationship.

Aggregation
^^^^^^^^^^^^^^^^^^^^^^^^

Aggregation represents a weaker “uses-a” relationship. In your design:

- The **Robot** uses an **Algorithm** to perform navigation but does not own it.  
- The algorithm can be shared, replaced, or modified independently.  

This relationship allows the robot to switch between algorithms (e.g., DFS, BFS) without altering its internal composition. Aggregation must be clearly demonstrated both in your UML and in your implementation structure.

Encapsulation and Abstraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All data members must remain private or protected, accessible only through well-defined public methods.  
Avoid exposing raw internal states. Instead, provide accessors and mutators when necessary.  

.. code-block:: cpp
  :linenos:


    class Maze {
    private:
        int width_;
        int height_;
    public:
        [[nodiscard]] int get_width() const noexcept { return width_; }
    };

Abstraction should be maintained by hiding low-level simulator communication inside your **Maze** class, ensuring other classes remain simulator-agnostic.

Direct calls to the **MazeControlAPI** are strictly prohibited outside the Maze class.  
All simulator commands must go through the Maze wrapper methods to preserve abstraction and ensure that your logic remains decoupled from simulator implementation details.

.. code-block:: cpp
  :linenos:

  // maze.hpp
  class Maze {
  public:
      void set_wall(int x, int y, char direction) {
          micro_mouse::MazeControlAPI::set_wall(x, y, direction);
      }

      bool has_wall_left() const {
          return micro_mouse::MazeControlAPI::has_wall_left();
      }
  };

Implementation Notes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Follow your class and sequence diagrams faithfully.  
- Keep functions focused on single responsibilities.  
- Use modern C++ best practices, including uniform initialization, RAII, and const-correctness.  
- Do not use global variables or hard-coded constants.  
- Maintain consistent naming conventions as used in the starter package.  
- Verify successful compilation using the required build flags (:code:`-Wall -Wextra -Werror -pedantic-errors`).  
- Use appropriate logging via :code:`std::cerr` for simulator output.

Deliverables
^^^^^^^^^^^^^^^^^^^^^^^^

- Fully implemented source files corresponding to your class and sequence diagrams.  
- A working executable that interfaces correctly with the simulator.  
- Evidence of composition, aggregation, inheritance, and polymorphism in your implementation.  
- Updated documentation (comments and brief report) describing how your design was realized in code.

Evaluation Criteria
^^^^^^^^^^^^^^^^^^^^^^^^

- Correct and consistent translation of UML design into code.  
- Proper use of abstraction, inheritance, and polymorphism.  
- Correct implementation of composition and aggregation.  
- Adherence to encapsulation principles and avoidance of direct API access.  
- Code organization, readability, and compliance with modern C++ practices.  
- Successful integration and functional operation within the simulator environment.

.. warning::
   
   - Your code will be tested on different 16x16 mazes.
   - To help with visualization:
   
    - Use one color to visualize the path generated by the BFS algorithm.
    - Use a different color to highlight the robot's current cell as it follows the path.
    
---------------------------------------------------------
Submission
---------------------------------------------------------

Before submitting, carefully review your project to ensure all requirements have been met and that your implementation runs correctly within the simulator environment.  
Each group must submit **one zipped file** named according to the format below:

.. admonition:: File Naming Convention
   :class: leftline

   **Format:** :code:`groupX_rwa4.zip`  
   **Example:** :code:`group3_rwa4.zip`  

   Use your assigned group number. Submissions that do not follow this naming convention may receive a penalty.

Submission Checklist
^^^^^^^^^^^^^^^^^^^^^^^^

Use the checklist below to verify that your submission is complete and properly organized:

.. list-table::
   :widths: 10 90
   :class: compact-table

   * - [ ]
     - The file is named correctly as :code:`groupX_rwa4.zip`
   * - [ ]
     - All required source files and headers are included
   * - [ ]
     - UML class and sequence diagrams are provided in image format (PNG or SVG) and placed in the `diagram` folder in your project folder
   * - [ ]
     - Implementation follows the design diagrams faithfully
   * - [ ]
     - The project builds cleanly with :code:`-Wall -Wextra -Werror -pedantic-errors`
   * - [ ]
     - The program runs successfully within the simulator without modification
   * - [ ]
     - All simulator interactions occur through the Maze wrapper (no direct API calls)
   * - [ ]
     - Doxygen documentation is complete and generated successfully
   * - [ ]
     - Group members’ names and group number are included in a README file
   * - [ ]
     - The zipped file contains only the relevant project files (no build folders or binaries)

Pre-Submission Review
^^^^^^^^^^^^^^^^^^^^^^^^

.. important::
   Before submitting, all group members must review the **“Summary of Past Assignment Issues”** document posted on **Canvas**.  
   This document highlights common mistakes observed in previous assignments (such as missing files, incorrect naming conventions, or direct API usage).  
   Groups are expected to verify that these issues have been avoided in their current submission.

Submission Method
^^^^^^^^^^^^^^^^^^^^^^^^

- Submit your :code:`groupX_rwa4.zip` file through **Canvas** under the *Assignment 4* submission link.  
- Late submissions will follow the course's late policy.  
- Only one group member needs to upload the file, but all members must be listed in the README.


---------------------------------------------------------
Grading Rubric
---------------------------------------------------------


**Total:** 50 points (plus up to **5 bonus points** for BFS)

UML Diagrams: Class & Sequence (10 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 80
   :stub-columns: 1
   :class: compact-table

   * - **Points**
     - **Criteria**
   * - 9-10 pts
     - Class and sequence diagrams are complete, consistent, and readable; correctly model **inheritance**, **composition**, **aggregation**, and **polymorphism** via an abstract :code:`Algorithm`; correct UML notation (roles, multiplicities, access, lifelines, messages); sequence diagram matches a realistic navigation scenario.
   * - 6-8 pts
     - Diagrams mostly correct with minor UML or consistency issues; relationships are present but one is under-specified (e.g., missing multiplicity or abstract marker).
   * - 3-5 pts
     - Partial diagrams; some relationships incorrect or missing; sequence flow unclear; noticeable UML notation errors.
   * - 0-2 pts
     - Diagrams missing or unusable; relationships not conveyed.

Implementation Faithfulness to Design (8 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 80
   :stub-columns: 1
   :class: compact-table

   * - **Points**
     - **Criteria**
   * - 7-8 pts
     - Implementation closely follows the submitted diagrams (classes, responsibilities, relationships, method roles) with only minor, well-justified deviations.
   * - 4-6 pts
     - Mostly consistent; some classes or relationships diverge from the diagrams without clear rationale.
   * - 1-3 pts
     - Significant divergence from design; several elements reinterpreted or omitted.
   * - 0 pts
     - Implementation bears little relation to the diagrams.

Algorithm Correctness & Behavior (DFS + Path Following) (10 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 80
   :stub-columns: 1
   :class: compact-table

   * - **Points**
     - **Criteria**
   * - 9-10 pts
     - DFS adheres to specified priority (N, E, S, W); maintains visited set; produces a valid path; **conditional replan** triggers only when newly detected walls block the remaining path; correct goal selection behavior; stack/path reversal handled correctly.
   * - 6-8 pts
     - DFS mostly correct; minor mistakes (e.g., occasional priority violation or edge case in replan); path reversal or visited handling slightly flawed but recoverable.
   * - 3-5 pts
     - DFS present but frequently incorrect; inconsistent priority; improper visited handling; replan logic missing or largely ineffective.
   * - 0-2 pts
     - DFS non-functional or absent.

C++{} Core Guidelines & Best Practices (10 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 80
   :stub-columns: 1
   :class: compact-table

   * - **Points**
     - **Criteria**
   * - 9-10 pts
     - Strong adherence to C++ Core Guidelines and best practices (encapsulation, RAII, const-correctness, uniform initialization, clear ownership, error handling, naming consistency, no globals, warnings clean with :code:`-Wall -Wextra -Werror -pedantic-errors`).
   * - 6-8 pts
     - Generally good practices; a few inconsistencies (e.g., occasional non-const, mixed naming, minor warnings).
   * - 3-5 pts
     - Several guideline violations; unclear ownership or resource handling; frequent warnings.
   * - 0-2 pts
     - Poor practices; widespread guideline violations; unstable build.

Encapsulation, Composition & Aggregation Realization (5 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 80
   :stub-columns: 1
   :class: compact-table

   * - **Points**
     - **Criteria**
   * - 5 pts
     - **Composition**: Robot *owns* its Maze (lifecycle bound). **Aggregation**: Robot *uses* Algorithm without owning it (swappable). Encapsulation enforced; direct simulator API calls avoided outside the Maze wrapper.
   * - 3-4 pts
     - Relationships mostly realized; minor leakage of API or ownership ambiguity.
   * - 1-2 pts
     - Relationships partially realized or confused; some direct API bypass of wrapper.
   * - 0 pts
     - Relationships not implemented; direct API usage pervasive.

Documentation (Doxygen & Comments) (4 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 80
   :stub-columns: 1
   :class: compact-table

   * - **Points**
     - **Criteria**
   * - 4 pts
     - Complete Doxygen documentation; clear, helpful comments; well-documented interfaces; brief usage notes where appropriate.
   * - 2-3 pts
     - Basic documentation with some missing elements; adequate comment coverage.
   * - 1 pt
     - Minimal documentation; poor comment quality.
   * - 0 pts
     - Missing or completely inadequate code documentation.

Build & Simulator Integration (3 pts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 80
   :stub-columns: 1
   :class: compact-table

   * - **Points**
     - **Criteria**
   * - 3 pts
     - Project builds cleanly; runs in the simulator; correct interaction via the Maze wrapper; logging visible as required.
   * - 2 pts
     - Builds with minor warnings or setup friction; runs with occasional issues.
   * - 1 pt
     - Build/run problems requiring instructor intervention; fragile integration.
   * - 0 pts
     - Cannot build or run in the simulator.


.. note::
   
   Bonus (up to +5 pts): BFS Implementation
   
   - Implement a **Breadth-First Search (BFS)** variant as an additional algorithm (polymorphic with :code:`Algorithm`) and demonstrate it on the same simulator setup.
   - Provide a brief note comparing DFS vs. BFS characteristics in this maze context (e.g., completeness, optimality on unweighted grids, memory usage).
   - **Reference:** `Breadth-First Search (BFS) — Wikipedia <https://en.wikipedia.org/wiki/Breadth-first_search>`_
