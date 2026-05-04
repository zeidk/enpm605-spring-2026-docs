====================================================
L14: Lifecycle Nodes & ROS 2 Bags
====================================================

Overview
--------

This lecture covers two ROS 2 capabilities essential for building,
debugging, and analyzing real robotic systems. **Lifecycle nodes**
follow a standardized state machine (Unconfigured, Inactive, Active,
Finalized) that gives the system precise control over initialization
order, resource allocation, and shutdown. Publishers, timers, and
other resources are allocated in transition callbacks
(``on_configure``, ``on_activate``) rather than ``__init__``, and
external commands or programmatic service calls drive the node
between states. **ROS 2 bags** record the messages published on a set
of topics, with their timestamps, so a run can be replayed offline
exactly as it happened. We compare the SQLite3 and MCAP storage
backends, record a full Nav2 navigation run, inspect and replay it
from the CLI, and finally visualize the recording in **Foxglove
Studio** using a multi-panel layout (3D, Plot, Raw Messages). All
hands-on examples use the ``lifecycle_demo`` and ``bag_demo``
packages.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Describe the four primary states of a lifecycle node and the
     transitions that connect them.
   - Explain why publishers and timers are allocated in
     ``on_configure`` and ``on_activate`` rather than ``__init__``.
   - Distinguish ``SUCCESS``, ``FAILURE``, and ``ERROR`` return
     values from a transition callback and predict the resulting
     state.
   - Implement a Python lifecycle node by extending ``LifecycleNode``
     and overriding the four transition callbacks.
   - Drive lifecycle transitions externally with
     ``ros2 lifecycle set`` and programmatically via the
     ``change_state`` service.
   - Record and replay topics with ``ros2 bag record`` and
     ``ros2 bag play``, and choose between SQLite3 and MCAP storage.
   - Inspect a bag's contents with ``ros2 bag info`` and identify the
     topics needed to reconstruct a navigation run offline.
   - Visualize an MCAP bag in Foxglove Studio using multi-panel
     layouts (3D, Plot, Raw Messages).


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:


   l14_lecture
   l14_exercises
   l14_quiz
   l14_references


Next Steps
----------

- This is the final regular lecture of the semester. The remaining
  class meetings are dedicated to **final project status checks** and
  office hours.
- Complete the exercises from this lecture whenever you have some time.
- Continue working on your final project deliverables.
