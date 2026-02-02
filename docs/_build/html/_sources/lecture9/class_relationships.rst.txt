====================
Class Relationships
====================

Class relationships describe how classes interact and depend on each other. They represent real-world connections between objects and define the structure of your program. They are how you model the real world and, more importantly, how you create code that is reusable, maintainable, and flexible.

.. grid:: 1 2 2 4
    :gutter: 3
    :class-container: sd-text-center

    .. grid-item-card:: Association
        :link: association
        :link-type: ref
        :class-card: sd-border-info icon-uml
        
        "uses-a"
        
        Independent objects
        
    .. grid-item-card:: Aggregation
        :link: aggregation
        :link-type: ref
        :class-card: sd-border-info icon-uml
        
        "has-a"
        
        Weak ownership
        
    .. grid-item-card:: Composition
        :link: composition
        :link-type: ref
        :class-card: sd-border-info icon-uml
        
        "part-of"
        
        Strong ownership
        
    .. grid-item-card:: Inheritance
        :link: inheritance
        :link-type: ref
        :class-card: sd-border-info icon-uml
        
        "is-a"
        
        Code reuse

----


.. _association:

Association
===========

.. card::
    :class-card: sd-border-secondary sd-border-3 sd-shadow-md sd-rounded-1

    **Definition:** Association is a loose relationship where objects exist independently. One object uses or interacts with another, but neither owns the other. If one object is destroyed, the other can continue existing.

.. grid:: 2
    :gutter: 2

    .. grid-item::
        :columns: 5
        
        **Key Characteristics:**

        ✓ Objects exist independently
        
        ✓ Neither object owns the other
        
        ✓ Relationship is typically "uses-a"
        
        ✓ Both objects can survive independently

    .. grid-item::
        :columns: 7
        
        **Real-World Example**
        
        A **Teacher** and a **Student** have an association. If the teacher leaves, students still exist. If a student graduates, the teacher remains.

UML Representation
------------------

In UML diagrams, association is shown with a simple line connecting two classes. Multiplicity can be indicated at each end:

.. tab-set::

    .. tab-item:: Multiplicity Notations

        .. list-table::
           :header-rows: 1
           :widths: 20 80

           * - Notation
             - Meaning
           * - ``n``
             - exactly n
           * - ``0..1``
             - zero or one
           * - ``*`` or ``0..*``
             - zero or more
           * - ``1..*``
             - one or more

    .. tab-item:: Visual Examples

        .. code-block:: text

            Teacher ─────────── Student
                   1..*      1..*

            Teacher ───────────> Student
                   1..*      1..*

                      teaches
            Teacher ───────────> Student
                   1..*      1..*

----

.. _aggregation:

Aggregation
===========

.. card::
    :class-card: sd-border-secondary sd-border-3 sd-shadow-md sd-rounded-1

    **Definition:** Aggregation is a type of association and represents a "has-a" relationship where the container has a weak ownership of the contained objects. The contained objects can exist independently of the container. When the container is destroyed, the contained objects continue to exist.

.. grid:: 2
    :gutter: 3

    .. grid-item-card:: 🔑 Key Characteristics
        
        ◇ Represents a "has-a" relationship
        
        ◇ Weak ownership (hollow diamond in UML)
        
        ◇ Contained objects can exist independently
        
        ◇ Container destruction doesn't destroy contained objects

    .. grid-item-card:: 🚗 Example Scenario
        
        A **Fleet** "contains" **Vehicles**. If the fleet is dissolved, the vehicles still exist and can be transferred to another fleet or operate independently.

Code Example
------------

.. code-block:: cpp
   :caption: Aggregation Implementation
   :emphasize-lines: 11

   class Vehicle {
   private:
       std::string id_;
   public:
       Vehicle(const std::string& id) : id_{id} {}
       // Vehicle can exist independently
   };

   class Fleet {
   private:
       std::vector<Vehicle*> vehicles_;  // Non-owning pointers
   public:
       void add_vehicle(Vehicle* v) {
           vehicles_.push_back(v);
       }
       // Vehicles are NOT destroyed when Fleet is destroyed
   };

.. important::

   Notice the use of **raw pointers** (``Vehicle*``) - the Fleet doesn't own the vehicles, it just references them.

----

.. _composition:

Composition
===========

.. card::
    :class-card: sd-border-secondary sd-border-3 sd-shadow-md sd-rounded-1

    **Definition:** Composition is a strong "has-a" relationship with exclusive ownership. The contained object is an integral part of the container and cannot exist independently. When the container is destroyed, all its parts are destroyed as well.

.. grid:: 2
    :gutter: 3

    .. grid-item-card:: 🔑 Key Characteristics
        
        ◆ Strong ownership (filled diamond in UML)
        
        ◆ Contained objects cannot exist independently
        
        ◆ Container destruction destroys all parts
        
        ◆ Represents "part-of" relationship

    .. grid-item-card:: 📡 Example Scenario
        
        A **Vehicle** has **Sensors**. The sensors are integral parts of the vehicle. If the vehicle is destroyed (scrapped), its sensors are destroyed with it.

Code Example
------------

.. code-block:: cpp
   :caption: Composition Implementation
   :emphasize-lines: 14,15

   class Sensor {
   private:
       std::string type_;
       double reading_{0.0};
   public:
       Sensor(const std::string& type) : type_{type} {}
   };

   class Vehicle {
   private:
       std::vector<Sensor> sensors_;  // Owns sensors by value
   public:
       Vehicle() {
           sensors_.emplace_back("lidar");
           sensors_.emplace_back("radar");
       }
       // Sensors are automatically destroyed with Vehicle
   };

.. tip::

   Notice the sensors are stored **by value** - the Vehicle owns them completely. When the Vehicle is destroyed, the sensors go with it.

----

Comparison: Aggregation vs Composition
=======================================

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Aggregation (Weak)
        :class-card: sd-border-info icon-aggregation
        
        .. code-block:: cpp
        
           std::vector<Vehicle*> vehicles_;
           // Non-owning pointers
        
        Hollow diamond in UML
        
        ✓ Parts survive independently

    .. grid-item-card:: Composition (Strong)
        :class-card: sd-border-warning icon-composition
        
        .. code-block:: cpp
        
           std::vector<Sensor> sensors_;
           // Owned by value
        
        Filled diamond in UML
        
        ✗ Parts destroyed with container


----

.. _inheritance:

Inheritance
===========

.. card::
    :class-card: sd-border-secondary sd-border-3 sd-shadow-md sd-rounded-1

    **Definition:** Inheritance represents an "is-a" relationship where a derived class inherits attributes and behaviors from a base class. The derived class specializes or extends the base class, providing specific implementations while maintaining the common interface.

.. grid:: 2
    :gutter: 3

    .. grid-item-card:: 🔑 Key Characteristics
        
        ▲ Represents an "is-a" relationship
        
        ▲ Derived class inherits from base class
        
        ▲ Enables code reuse and polymorphism
        
        ▲ Supports specialization and extension

    .. grid-item-card:: 🚕 Example Scenario
        
        **RoboTaxi** "is-a" Vehicle. **Taxi** "is-a" Vehicle. Both inherit common vehicle behavior but add their own specific features.

Types of Inheritance
--------------------

.. tab-set::

    .. tab-item:: Single Inheritance

        A class inherits from exactly one base class.

        .. code-block:: cpp

           class Animal {
           protected:
               std::string name_;
               int age_;
           public:
               Animal(const std::string& name, int age) 
                   : name_{name}, age_{age} {}
           };

           class Bird : public Animal {
           private:
               double wingspan_;
           public:
               Bird(const std::string& name, int age, double wingspan)
                   : Animal(name, age), wingspan_{wingspan} {}
           };

           class Elephant : public Animal {
           private:
               double trunk_length_;
           public:
               Elephant(const std::string& name, int age, double trunk_length)
                   : Animal(name, age), trunk_length_{trunk_length} {}
           };

        .. note::

           - ``Bird`` and ``Elephant`` inherit ``Animal``'s ``public`` and ``protected`` members
           - UML diagrams typically don't show inherited members

    .. tab-item:: Multiple Inheritance

        Multiple inheritance occurs when a class inherits from more than one base class. The derived class gains access to all ``public`` and ``protected`` members from all parent classes.

        .. code-block:: cpp

           class Animal {
           protected:
               std::string species_;
           public:
               Animal(const std::string& species) : species_{species} {}
           };

           class Human {
           protected:
               std::string language_;
           public:
               Human(const std::string& language) : language_{language} {}
           };

           class MythicalCreature : public Animal, public Human {
           public:
               MythicalCreature(const std::string& species, 
                               const std::string& language)
                   : Animal(species), Human(language) {}
           };

        .. important::

           We focus exclusively on **single inheritance** in this course. For assignments and projects, you are welcome to use any inheritance approach.

Generalization and Specialization
----------------------------------

.. grid:: 2
    :gutter: 3

    .. grid-item-card:: 🔼 Generalization (Bottom-Up)
        :class-card: sd-border-success
        
        Bottom-up approach which should be used every time classes have specific differences and common similarities.
        
        **Process:**

        1. Identify common attributes and methods across multiple classes
        2. Extract commonalities into a base class
        3. Keep differences in specialized subclasses

    .. grid-item-card:: 🔽 Specialization (Top-Down)
        :class-card: sd-border-success
        
        Top-down approach which creates new classes from an existing class.
        
        **Process:**

        1. Start with a general base class
        2. Create derived classes for specific variants
        3. Add specialized attributes and methods to derived classes

UML Representation
------------------

The ``protected`` specifier is denoted with a ``#`` symbol in UML diagrams.

.. only:: html

        .. raw:: html

            <div style="display:flex; justify-content:center; align-items:center; gap:1rem;">
                <img src="../_static/lecture9/protected_light.png"
                    alt="Protected member"
                    class="only-light"
                    style="width:60%; border-radius:8px;">
                <img src="../_static/lecture9/protected_dark.png"
                    alt="Protected member"
                    class="only-dark"
                    style="width:60%; border-radius:8px;">
            </div>


Inheritance Access Types
-------------------------

The access specifier used during inheritance determines how base class members are accessible in the derived class:

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25
   :class: compact-table

   * - Base Class Member
     - public inheritance
     - protected inheritance
     - private inheritance
   * - ``public``
     - ``public``
     - ``protected``
     - ``private``
   * - ``protected``
     - ``protected``
     - ``protected``
     - ``private``
   * - ``private``
     - not accessible (hidden)
     - not accessible (hidden)
     - not accessible (hidden)

.. note::

   - ``private`` members are inherited but hidden from derived classes
   - Default inheritance in C++ is ``private``
   - Always explicitly specify ``public`` inheritance for is-a relationships

**Best Practice Example:**

.. code-block:: cpp

   class Base {
   public:
       void public_method();
   protected:
       void protected_method();
   private:
       void private_method();
   };

   // Use public inheritance for is-a relationships
   class Derived : public Base {
       // public_method() is public
       // protected_method() is protected
       // private_method() is not accessible
   };

Constructors in Inheritance
----------------------------

.. card::
    :class-card: sd-border-warning sd-border-3 sd-shadow-md sd-rounded-1
    
    **Critical Rule**
    
    The constructors of a class must address the attributes specific to that class.

**Problem:** How do we initialize base class attributes when constructing a derived object?

.. dropdown:: Wrong Approach #1: Initialize base class members in derived class initializer list
    :class-container: sd-border-danger

    .. code-block:: cpp

       class Base {
       protected:
           int base_member_;
       public:
           Base(int base_value = 50) : base_member_{base_value} {}
       };

       class Derived : public Base {
       private:
           double derived_member_;
       public:
           // ERROR: Cannot initialize inherited members
           Derived(double derived_value, int base_value)
               : derived_member_{derived_value}, base_member_{base_value} {}
       };

.. dropdown:: Wrong Approach #2: Assign base class members in constructor body
    :class-container: sd-border-danger

    .. code-block:: cpp

       class Derived : public Base {
       private:
           double derived_member_;
       public:
           Derived(double derived_value, int base_value)
               : derived_member_{derived_value} { 
               base_member_ = base_value;  // Works, but not ideal
           }
       };

    .. warning::

       This approach works but is performed in two steps and will not work if the attribute is a ``const`` or a reference.

.. dropdown:: Correct Approach: Explicitly call the base class constructor
    :class-container: sd-border-success
    :open:

    .. code-block:: cpp

       class Base {
       protected:
           int base_member_;
       public:
           Base(int base_value = 50) : base_member_{base_value} {}
       };

       class Derived : public Base {
       private:
           double derived_member_;
       public:
           Derived(double derived_value, int base_value)
               : Base(base_value),  // Call base constructor FIRST
                 derived_member_{derived_value} { 
               // Empty body
           }
       };

    .. code-block:: cpp

       int main() {
           Derived derived(20.5, 10);
           // Execution order:
           // 1. Base(10) is called -> base_member_ = 10
           // 2. Derived(20.5, 10) is called -> derived_member_ = 20.5
           // 3. Control returns to main()
       }

.. card::
    :class-card: sd-border-success

    
    ✅ **Best Practice**
    
    - Add parameters for base class attributes in the derived class constructor
    - Explicitly call the base class constructor in the member initializer list
    - Each constructor worries only about its own attributes

----

Key Takeaways
=============

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Association
        :class-card: sd-border-info
        
        **"uses-a"**
        
        Independent objects that interact

    .. grid-item-card:: Aggregation
        :class-card: sd-border-info
        
        **"has-a"**
        
        Weak ownership, parts can survive independently

    .. grid-item-card:: Composition
        :class-card: sd-border-info
        
        **"has-a"**
        
        Strong ownership, parts destroyed with whole

    .. grid-item-card:: Inheritance
        :class-card: sd-border-info
        
        **"is-a"**
        
        Derived class extends base class

.. card::
    :class-card: sd-border-primary sd-border-3 sd-shadow-md sd-rounded-1
    
    **Additional Guidelines:**
    
    - Always use ``public`` inheritance for is-a relationships
    - Call base class constructors explicitly in derived class initializer lists
    - Focus on single inheritance for clarity and maintainability