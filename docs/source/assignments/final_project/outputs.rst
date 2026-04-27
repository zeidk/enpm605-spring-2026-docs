====================================================
Expected Output
====================================================

.. |rarr| unicode:: U+2192


Nominal Run (Full Mission)
==========================

The following shows an example of the expected log output when the
full system is running correctly. The robot visits all four zones,
detects survivors in zones A and C, broadcasts TF frames, reports
findings, and completes the mission. Timestamps are abbreviated.
Exact numeric values will vary.

.. code-block:: text

   [INFO] [search_and_rescue]: Loaded 4 search zones from parameters.
   [INFO] [search_and_rescue]: Base station at (0.00, 0.00, yaw=0.00).
   [INFO] [detect_survivor_server]: DetectSurvivor service ready.
   [INFO] [report_survivor_server]: ReportSurvivor service ready.

   [INFO] [search_and_rescue]: --- Zone 1/4: zone_a (-3.00, 3.00) ---
   [INFO] [search_and_rescue]: Navigating to zone_a...
   [INFO] [search_and_rescue]: Reached zone_a.
   [INFO] [search_and_rescue]: Calling detect_survivor for zone_a...
   [INFO] [detect_survivor_server]: Detection request for zone_a: FOUND at (-2.50, 3.20)
   [INFO] [search_and_rescue]: Survivor detected at zone_a!
   [INFO] [search_and_rescue]: Broadcasting TF frame: survivor_1 at (-2.50, 3.20) in map frame.
   [INFO] [search_and_rescue]: Reporting survivor_1 to base...
   [INFO] [report_survivor_server]: Report received: survivor_1 at (-2.50, 3.20). Acknowledged.
   [INFO] [search_and_rescue]: Base acknowledged survivor_1.

   [INFO] [search_and_rescue]: --- Zone 2/4: zone_b (3.50, 3.00) ---
   [INFO] [search_and_rescue]: Navigating to zone_b...
   [INFO] [search_and_rescue]: Reached zone_b.
   [INFO] [search_and_rescue]: Calling detect_survivor for zone_b...
   [INFO] [detect_survivor_server]: Detection request for zone_b: NOT FOUND
   [INFO] [search_and_rescue]: No survivor found at zone_b.

   [INFO] [search_and_rescue]: --- Zone 3/4: zone_c (4.00, -3.00) ---
   [INFO] [search_and_rescue]: Navigating to zone_c...
   [INFO] [search_and_rescue]: Reached zone_c.
   [INFO] [search_and_rescue]: Calling detect_survivor for zone_c...
   [INFO] [detect_survivor_server]: Detection request for zone_c: FOUND at (4.10, -2.50)
   [INFO] [search_and_rescue]: Survivor detected at zone_c!
   [INFO] [search_and_rescue]: Broadcasting TF frame: survivor_2 at (4.10, -2.50) in map frame.
   [INFO] [search_and_rescue]: Reporting survivor_2 to base...
   [INFO] [report_survivor_server]: Report received: survivor_2 at (4.10, -2.50). Acknowledged.
   [INFO] [search_and_rescue]: Base acknowledged survivor_2.

   [INFO] [search_and_rescue]: --- Zone 4/4: zone_d (-3.50, -3.00) ---
   [INFO] [search_and_rescue]: Navigating to zone_d...
   [INFO] [search_and_rescue]: Reached zone_d.
   [INFO] [search_and_rescue]: Calling detect_survivor for zone_d...
   [INFO] [detect_survivor_server]: Detection request for zone_d: NOT FOUND
   [INFO] [search_and_rescue]: No survivor found at zone_d.

   [INFO] [search_and_rescue]: All zones visited. Returning to base.
   [INFO] [search_and_rescue]: Navigating to base station...
   [INFO] [search_and_rescue]: Reached base station. Mission complete.


Verification Commands
=====================

Use these commands to test individual components.

.. code-block:: console

   # 1. Launch simulation + Nav2 (separate terminals). The map file
   # is the one you built with slam_toolbox and saved under
   # group<N>_final/maps/.
   ros2 launch rosbot_gazebo final_project_world.launch.py
   ros2 launch rosbot_gazebo navigation.launch.py \
       map:=/path/to/group<N>_final/maps/final_project_world.yaml

   # 2. Launch the mission
   ros2 launch group<N>_final search_and_rescue.launch.py

   # 3. Check TF frames for discovered survivors
   ros2 run tf2_ros tf2_echo map survivor_1
   ros2 run tf2_ros tf2_echo map survivor_2

   # 4. List all static transforms
   ros2 topic echo /tf_static --once

   # 5. List available services
   ros2 service list | grep -E "detect|report"

   # 6. Test detection service manually
   ros2 service call /detect_survivor \
       group<N>_final_interfaces/srv/DetectSurvivor \
       "{zone_id: 'zone_a'}"

   # 7. Show launch arguments
   ros2 launch group<N>_final search_and_rescue.launch.py --show-args
