:orphan:

..
   Local-only autodoc page for the group0_final reference implementation.

   This file is built only when Sphinx runs on the maintainer's machine
   (where group0_final is available on sys.path). The render-api script
   then extracts the article body from the resulting
   _code_source.html and writes it to _code_api.html, which code.rst
   embeds via ``.. raw:: html``. RTD never builds this file -- conf.py
   adds it to exclude_patterns when the READTHEDOCS env var is set.

   The :orphan: directive above suppresses the "document isn't included
   in any toctree" warning.

Reference Implementation API
============================

Mission State
-------------

.. automodule:: group0_final.zone_manager
   :members:
   :undoc-members:
   :show-inheritance:


Behavior Tree Leaves
--------------------

Actions
~~~~~~~

.. automodule:: group0_final.bt_nodes.actions
   :members:
   :private-members: _NavigateToPoseAction, _yaw_to_quaternion, _make_pose_stamped
   :undoc-members:
   :show-inheritance:

Conditions
~~~~~~~~~~

.. automodule:: group0_final.bt_nodes.conditions
   :members:
   :undoc-members:
   :show-inheritance:


Service Servers
---------------

.. automodule:: group0_final.service_servers.detect_survivor_server
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: group0_final.service_servers.report_survivor_server
   :members:
   :undoc-members:
   :show-inheritance:


Entry Point
-----------

.. automodule:: group0_final.scripts.main_search_and_rescue
   :members:
   :undoc-members:
   :show-inheritance:
