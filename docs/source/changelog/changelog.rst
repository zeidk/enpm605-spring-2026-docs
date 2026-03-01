====================================================
Changelog
====================================================

All notable changes to the ENPM605 Spring 2026 course documentation are recorded here.


.. dropdown:: v1.1.0 -- RWA 2 Released (2026-03-01)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: RWA 2: Search and Rescue Mission Planner (new)

   **Assignment Overview**

   - New assignment covering Object-Oriented Programming (Lectures 6 and 7)
   - Two-phase structure: Phase 1 (Design) and Phase 2 (Implementation)
   - Use case: Disaster Response Operation with aerial drones and ground crawlers searching a disaster zone divided into sectors
   - Total: 50 points (Design: 6 pts, Implementation: 44 pts)
   - Due: March 25, 2026

   **Phase 1: Design Document (6 pts)**

   - Deliverable: single UML class diagram in PDF format (``design_document.pdf``)
   - Design phase intentionally lightened to allow students to focus on implementation
   - Sequence diagram removed from requirements to reduce design workload

   **Phase 2: Implementation (44 pts)**

   - 7 classes across 6 modules: ``SensorPayload``, ``Robot`` (abstract), ``AerialDrone``, ``GroundCrawler``, ``Sector``, ``Mission``, ``DisasterZone``
   - OOP concepts exercised: abstraction (``abc.ABC``), encapsulation (``@property``), inheritance (2 subclasses), polymorphism (``search()``/``can_search()`` overrides), composition (Robot owns SensorPayload), aggregation (DisasterZone manages robots/sectors), association (Mission links robot to sector)
   - Dunder methods required: ``__str__``, ``__repr__``, ``__eq__``, ``__lt__``, ``__len__``, ``__contains__``
   - Main program (9 pts) demonstrates polymorphism, sorting, ``__contains__``, and report generation

   **AI Policy**

   - Explicit policy added: AI tools (Copilot, ChatGPT, Claude, etc.) are NOT permitted for code or design
   - Students instructed to disable GitHub Copilot and other AI extensions in VS Code before starting
   - Exception: AI may be used to generate docstring documentation **after** code is written by the student

   **Other Details**

   - Project naming convention: ``firstname_lastname_rwa2/``
   - Suggested 3-week timeline included with day-by-day breakdown
   - All major sections wrapped in ``.. dropdown::`` directives for collapsible navigation
   - Use case separated into subsections using ``.. rubric::`` directives (Robots, Common Robot Characteristics, Sensor Payload, Sectors, Missions, Disaster Zone)


.. dropdown:: v1.0.0 -- Initial Release (2026-01-27)
   :icon: tag
   :class-container: sd-border-success

   Initial release of the ENPM605 Spring 2026 course documentation.

   .. rubric:: Course Structure

   - Lectures 1 through 6 published with lecture notes, exercises, quizzes, glossaries, and references
   - Each lecture organized as a self-contained folder with RST files following a consistent structure

   .. rubric:: RWA 1: Robot Fleet Monitor

   - First assignment covering Lectures 1 through 4 (variables, data types, control flow, functions)
   - 30 points, 6 parts across 5 Python modules
   - Due: February 25, 2026