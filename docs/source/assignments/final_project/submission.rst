====================================================
Submission
====================================================


Pre-Submission Checklist
========================

Work through every item below before packaging your ZIP. Items that
fail at submission time typically also fail at grading time.

**Functionality**

- |box| Both packages are registered in
  ``final_project_meta/package.xml`` and the full stack builds:
  ``colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release --packages-up-to final_project_meta``
- |box| Both service interfaces are visible:
  ``ros2 interface show group<N>_final_interfaces/srv/DetectSurvivor``
  ``ros2 interface show group<N>_final_interfaces/srv/ReportSurvivor``
- |box| The full system launches:
  ``ros2 launch group<N>_final search_and_rescue.launch.py``
- |box| The robot visits all search zones sequentially.
- |box| Detection service is called at each zone.
- |box| Survivors are detected and TF frames are broadcast
  (verify with ``ros2 run tf2_ros tf2_echo map survivor_1``).
- |box| Report service is called for each found survivor.
- |box| After every zone is visited, the robot drives back to the
  base station.
- |box| Launch arguments work: ``--show-args`` and override.
- |box| Parameters load from ``mission_params.yaml``.
- |box| ``maps/final_project_map.pgm`` and
  ``maps/final_project_map.yaml`` (built with ``slam_toolbox``)
  are present inside ``group<N>_final/`` and Nav2 launches cleanly
  against them.
- |box| ``setup.py`` installs ``maps/``, ``config/``, and
  ``launch/`` via ``data_files`` -- verify with
  ``ls install/group<N>_final/share/group<N>_final/`` after a
  ``colcon build`` and confirm all three directories appear.
  Without this, ``get_package_share_directory()`` returns a path
  that does not contain your map / params / launch files at
  runtime.

**Documentation**

- |box| ``README.md`` lists each group member and their
  contributions.
- |box| ``README.md`` includes a brief BT design description
  (memory choices).

**Code Quality**

- |box| Type hints on all methods.
- |box| Google-style docstrings on all classes and methods.
- |box| Comments explain non-obvious logic.
- |box| No linting errors (Ruff).

**Packaging**

- |box| Removed ``__pycache__/``, ``*.pyc``, ``.ruff_cache/``, ``.vscode/``, etc 
- |box| ZIP file is named ``group<N>_final_project.zip``.
- |box| ZIP contains the ``final_project/`` folder with **both**
  ``group<N>_final_interfaces/`` and ``group<N>_final/`` inside it.

.. |box| unicode:: U+2610


How to Submit
=============

1. Zip the ``~/enpm605_ws/src/final_project/`` folder and submit it
   on Canvas, renamed to ``group<N>_final_project.zip`` (e.g.,
   ``group3_final_project.zip``). 

2. The ZIP must contain the ``final_project/`` folder, with **both**
   package folders inside it:
   ``final_project/group<N>_final_interfaces/`` and
   ``final_project/group<N>_final/``.

3. The ZIP must not contain ``build/``, ``install/``, ``log/``,
   ``__pycache__/``, ``.pyc``, ``.ruff_cache/``, and any other artifacts.

4. Only one submission per group.
