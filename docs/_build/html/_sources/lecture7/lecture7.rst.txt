L7 - Move Semantics and Smart Pointers
===============================================

This site accompanies *ENPM702 - Lecture 7: Move Semantics & Smart Pointers*. It organizes the lecture into concise, browsable pages with examples, short exercises, and instructor notes.

.. note::
   `Lecture 7 slides (v3.0) <https://drive.google.com/file/d/1asdrtcfj3Uyv_oq7InnKbaNOAPAg2e5i/view?usp=sharing>`_.


Learning Outcomes
-----------------

By the end of this session, you will be able to:

- Explain **move semantics** and distinguish between **lvalues**, **prvalues**, and **xvalues** in \CC.
- Use **rvalue references** and **std::move** to efficiently transfer ownership of resources.
- Implement and manage **smart pointers** from ``<memory>`` to ensure safe and automatic resource cleanup.
- Create and use **std::unique_ptr** with proper initialization, exclusive ownership, and member methods (``get()``, ``release()``, ``reset()``, ``swap()``).
- Apply **move semantics** when passing or returning ``std::unique_ptr`` to convey ownership transfer clearly.
- Use **std::shared_ptr** to manage shared ownership, explain its **control block structure**, and utilize methods like ``use_count()`` and ``unique()``.
- Pass and return **std::shared_ptr** correctly using **copy semantics** and understand **reference counting** and **Return Value Optimization (RVO)**.
- Use **std::weak_ptr** for non-owning observation, employ ``lock()`` and ``expired()`` safely, and explain how it breaks **circular dependencies**.
- Choose the appropriate **smart pointer type** (``unique_ptr``, ``shared_ptr``, or ``weak_ptr``) for various ownership and lifetime management scenarios.

.. tip::
   Compile examples with ``-std=c++17 -Wall -Wextra -pedantic-errors -Werror`` for strong diagnostics.

Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   lecture
   exercises
   references