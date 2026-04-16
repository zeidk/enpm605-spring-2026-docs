====================================================
Submission
====================================================


Pre-Submission Checklist
========================

Work through every item below before packaging your ZIP. Items that
fail at submission time typically also fail at grading time.

**Functionality**

- |box| Both packages are registered in
  ``gp2_meta/package.xml`` and the full stack builds:
  ``colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release --packages-up-to gp2_meta``
- |box| The action interface is visible:
  ``ros2 interface show group<N>_gp2_interfaces/action/NavigateToGoal``
- |box| The full system launches:
  ``ros2 launch group<N>_gp2 gp2.launch.py``
- |box| The robot drives to all three goals sequentially.
- |box| Feedback (``current_pose``, ``distance_remaining``) is
  published during execution.
- |box| Each result (``success``, ``total_distance``,
  ``elapsed_time``) is logged by the client.
- |box| **Cancellation is demonstrated**: follow the procedure in
  :doc:`outputs` and capture a terminal log (or screenshot) of the
  server handling a cancel request. Include the log in the
  ``gp2/`` folder as ``cancel_demo.txt`` (or ``cancel_demo.png``).
- |box| Launch arguments work: ``--show-args`` and override.
- |box| Parameters load from ``goals.yaml``.

**Documentation**

- |box| ``README.md`` lists each group member and their
  contributions.

**Code Quality**

- |box| Type hints on all methods.
- |box| Google-style docstrings on all classes and methods.
- |box| Comments explain the two-phase controller and feedback
  logic.
- |box| No linting errors (Ruff).

**Packaging**

- |box| Removed ``__pycache__/``, ``*.pyc``, ``.ruff_cache/``.
- |box| ZIP file is named ``group<N>_gp2.zip``.
- |box| ZIP contains the ``gp2/`` folder with **both**
  ``group<N>_gp2_interfaces/`` and ``group<N>_gp2/`` inside it.
- |box| ``cancel_demo.txt`` (or ``cancel_demo.png``) is present
  inside the ``gp2/`` folder.

.. |box| unicode:: U+2610


How to Submit
=============

1. Zip the ``~/enpm605_ws/src/gp2/`` folder itself and submit it
   on Canvas, renamed to ``group<N>_gp2.zip`` (e.g.,
   ``group3_gp2.zip``). For example:

   .. code-block:: console

      cd ~/enpm605_ws/src
      zip -r group3_gp2.zip gp2 \
          -x "*/build/*" "*/install/*" "*/log/*" \
             "*/__pycache__/*" "*.pyc" "*/.ruff_cache/*"

2. The ZIP must contain the ``gp2/`` folder, with **both** package
   folders inside it:
   ``gp2/group<N>_gp2_interfaces/`` and ``gp2/group<N>_gp2/``.

3. The ZIP must not contain ``build/``, ``install/``, ``log/``,
   ``__pycache__/``, ``.pyc``, or ``*/.ruff_cache/*`` files.

4. Only one submission per group.
