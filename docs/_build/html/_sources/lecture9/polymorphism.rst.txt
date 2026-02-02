============
Polymorphism
============

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-md sd-rounded-1
    
    **Definition:** Polymorphism (Greek: *poly* = many, *morph* = form) is a core OOP principle. Polymorphism allows objects of different classes to be treated uniformly through a common interface.

C++ supports two types of polymorphism:

.. grid:: 2
    :gutter: 3

    .. grid-item-card:: ⚡ Compile-Time Polymorphism
        :class-card: sd-border-info sd-border-2
        
        Resolved at compile time
        
        **Static polymorphism / Early binding**

    .. grid-item-card:: ⚡ Runtime Polymorphism
        :class-card: sd-border-success sd-border-2
        
        Resolved at runtime
        
        **Dynamic polymorphism / Late binding**

----

Compile-Time Polymorphism
--------------------------

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-md sd-rounded-1
    
    **Definition:** Compile-time polymorphism (also called *static polymorphism* or *early binding*) is resolved during compilation. The compiler determines which function to call based on the **static type** at compile time.

**Key Characteristics:**

.. grid:: 2 2 4 4
    :gutter: 2

    .. grid-item-card:: When
        
        Resolution at compile time

    .. grid-item-card:: Based On
        
        Declared type of variable

    .. grid-item-card:: Performance
        
        No runtime overhead

    .. grid-item-card:: Mechanisms
        
        Overloading & redefinition

.. note::

   The function resolution happens at compile time based on the declared type of the variable, not the actual object it contains.

Method Order Check
~~~~~~~~~~~~~~~~~~

When a method is called on a derived class object:

.. grid:: 3
    :gutter: 2

    .. grid-item-card:: 1. First
        :class-card: sd-border-primary
        
        Check derived class

    .. grid-item-card:: 2. Then
        :class-card: sd-border-info
        
        Search up inheritance hierarchy

    .. grid-item-card:: 3. Finally
        :class-card: sd-border-success
        
        Use first match found

.. code-block:: cpp
   :caption: Method Resolution Example

   class Base {
   public:
       void test() { 
           std::cout << "Base::test()\n"; 
       }
   };

   class Derived : public Base {
       // No test() method defined
   };

   int main() {
       Derived derived;
       derived.test();  // Calls Base::test()
   }

Method Redefinition
~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-md sd-rounded-1
    
    **Definition:** Method redefinition allows a derived class to provide its own implementation of a base class method when the base class version is too general or needs specialization.

.. code-block:: cpp
   :caption: Method Redefinition Example
   :emphasize-lines: 10-12

   class Base {
   public:
       void test() { 
           std::cout << "Base::test()\n"; 
       }
   };

   class Derived : public Base {
   public:
       void test() {  // Redefines Base::test()
           std::cout << "Derived::test()\n";
       }
   };

   int main() {
       Derived derived;
       derived.test();  // Calls Derived::test()
   }

.. note::

   Method redefinition is compile-time polymorphism because the method selection is based on the static type known at compile time.

----

Runtime Polymorphism
--------------------

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-md sd-rounded-1
    
    **Definition:** Runtime polymorphism (*dynamic polymorphism* or *late binding*) decides which ``virtual`` method implementation runs based on the *dynamic type* (actual object type) at runtime, not the static type of the pointer/reference.

**Key Requirements:**

.. grid:: 3
    :gutter: 3

    .. grid-item-card:: 1. Virtual Method
        :class-card: sd-border-primary
        
        A ``virtual`` method in base class

    .. grid-item-card:: 2. Base Handle
        :class-card: sd-border-primary
        
        Call through base reference/pointer

    .. grid-item-card:: 3. Dynamic Dispatch
        :class-card: sd-border-primary
        
        Method depends on actual object type

.. important::

   Runtime polymorphism in C++ requires a ``virtual`` method in a base class and a call through a base reference or base pointer to a derived object. The actual method called depends on the real object type at runtime.

The ``virtual`` Keyword
~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-md sd-rounded-1
    
    **Definition:** The ``virtual`` keyword tells the compiler to use **dynamic dispatch** for a method.

**What It Does:**

.. grid:: 3
    :gutter: 2

    .. grid-item-card:: ⏰ Runtime Resolution
        
        Method call resolved at runtime, not compile time

    .. grid-item-card:: 🎯 Actual Type
        
        Actual object type determines which method runs

    .. grid-item-card:: 📊 VTable
        
        Compiler creates virtual method table

.. tab-set::

    .. tab-item:: Virtual Declaration

        .. code-block:: cpp
           :caption: Virtual Method Declaration
           :emphasize-lines: 4,7

           class Vehicle {
           public:
               // virtual -> can be overridden in derived classes
               virtual void drive();
               
               // NOT virtual -> cannot be overridden (static binding)
               void update_location(const Location& location);
           };

    .. tab-item:: Usage Example

        .. code-block:: cpp
           :caption: Dynamic Dispatch in Action

           int main() {
               using transportation::Vehicle;
               using transportation::RoboTaxi;
               
               // Actual object: RoboTaxi
               // Pointer type: Vehicle
               std::unique_ptr<Vehicle> rt = 
                   std::make_unique<RoboTaxi>("ROBOTAXI-001", 4);
               
               rt->drive();              // Calls RoboTaxi::drive() - dynamic dispatch
               rt->update_location(loc); // Calls Vehicle::update_location() - static binding
           }

.. warning::

   - Without ``virtual``, C++ uses static binding based on the pointer type, not the actual object!
   - Note that we wrote: ``std::unique_ptr<Vehicle> rt = ...`` and not ``auto rt = ...`` which is equivalent to ``std::unique_ptr<RoboTaxi> rt``. Remember that we want a base class pointer (or reference) to a derived object for polymorphism to work.

The Problem Without Polymorphism
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-warning
    
    **Challenge:** You must drive different vehicle types uniformly (``RoboTaxi``, ``Taxi``, ...), yet each type performs the task differently.

.. dropdown:: ❌ Non-Polymorphic Solution (Not Scalable)
    :class-container: sd-border-danger
    :open:

    .. code-block:: cpp
       :caption: Overloads for Each Type

       // Overloads choose at compile time based on the static type
       void run_shift(transportation::RoboTaxi& v) { v.drive(); }
       void run_shift(transportation::Taxi& v)     { v.drive(); }

       int main() {
           transportation::RoboTaxi rt{"ROBOTAXI-001", 4};
           transportation::Taxi     tx{"TAXI-001", 4};
           
           run_shift(rt);  // Calls RoboTaxi version
           run_shift(tx);  // Calls Taxi version
       }

    .. warning::

       Overload resolution is a compile-time choice. Each new derived type requires another overload. Bodies tend to duplicate (*violates DRY principle*). Does not support heterogeneous collections.

.. dropdown:: ✅ Polymorphic Solution (Scalable)
    :class-container: sd-border-success
    :open:

    .. code-block:: cpp
       :caption: One Function for All Types

       // Base interface with virtual method
       class Vehicle {
       public:
           virtual ~Vehicle() = default;  // Essential for polymorphic bases
           virtual void drive();          // Virtual (can be overridden)
       };

       // One function works for ALL current and future derived vehicle types
       void run_shift(transportation::Vehicle& v) {
           v.drive();  // Runtime dispatch - calls the actual object's drive()
       }

       // Pointer variant (e.g., ownership with unique_ptr)
       void run_shift(std::unique_ptr<transportation::Vehicle> v) {
           v->drive();  // Runtime dispatch
       }

       int main() {
           auto rt = std::make_unique<transportation::RoboTaxi>("ROBOTAXI-001", 4);
           auto tx = std::make_unique<transportation::Taxi>("TAXI-001", 4);
           
           run_shift(*rt);             // Calls RoboTaxi::drive()
           run_shift(std::move(tx));   // Calls Taxi::drive()
       }

    .. important::

       Only one ``run_shift()`` is needed. The call *site* uses a base reference or pointer. The *target* method is determined at runtime based on the actual object type (the most-derived override).

----

When to Use ``auto`` vs. Explicit Base Type
--------------------------------------------

.. card::
    :class-card: sd-border-primary sd-border-2
    
    **Question:** When should you use ``auto`` versus an explicit base type?
    
    **Answer:** The choice depends on **where polymorphism needs to happen**.

.. tab-set::

    .. tab-item:: Explicit Base Type

        .. code-block:: cpp
           :caption: Base Type from Start

           std::unique_ptr<Vehicle> rt = std::make_unique<RoboTaxi>(...);
           
           // Polymorphic calls directly
           rt->drive();

        **Use when:**
        
        ✓ Multiple polymorphic calls needed locally
        
        ✓ Polymorphism happens at point of creation
        
        ✓ Building polymorphic collections

    .. tab-item:: Using auto

        .. code-block:: cpp
           :caption: Concrete Type Initially

           auto rt = std::make_unique<RoboTaxi>(...);
           
           // Direct calls to RoboTaxi
           rt->drive();
           
           // Pass to polymorphic function
           run_shift(std::move(rt));

        **Use when:**
        
        ✓ Concrete type needed initially
        
        ✓ Polymorphism delegated to function calls
        
        ✓ Need derived-specific methods before passing to functions

The Container Problem with ``auto``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 2
    :gutter: 3

    .. grid-item-card:: ✅ This WORKS
        :class-card: sd-border-success
        
        **Function parameter accepts conversion:**
        
        .. code-block:: cpp
        
           auto rt = std::make_unique<RoboTaxi>(...);
           run_shift(std::move(rt));  // ✓ Converts at call

    .. grid-item-card:: ❌ This FAILS
        :class-card: sd-border-danger
        
        **Container requires exact type match:**
        
        .. code-block:: cpp
        
           auto rt = std::make_unique<RoboTaxi>(...);
           std::vector<std::unique_ptr<Vehicle>> fleet;
           
           fleet.push_back(std::move(rt));  // ✗ Type mismatch!

.. warning::

   **Why?** Function parameters allow implicit conversions at the call site. Container storage requires **exact type matches**: ``unique_ptr<RoboTaxi>`` ≠ ``unique_ptr<Vehicle>``. This applies to **ALL** containers (``vector``, ``deque``, ``list``, ``set``, ``map``, etc.).

Complete Comparison Table
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 25 25
   :class: compact-table

   * - Operation
     - Explicit Base Type
     - Using ``auto``
   * - Pass to function with base parameter
     - ✓
     - ✓
   * - Store in ANY container of base pointers
     - ✓
     - ✗
   * - Use ``push_back``/``emplace_back``/``insert`` with variable
     - ✓
     - ✗
   * - Direct insertion: ``vec.push_back(make_unique<...>())``
     - ✓
     - N/A*
   * - Call derived-specific methods
     - ✗
     - ✓
   * - Polymorphic calls at point of use
     - ✓
     - ✗

*\* No auto variable involved — temporary converts at insertion point*

Why This Happens: Type System Rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

    .. tab-item:: Function Parameters ✓

        .. code-block:: cpp
           :caption: Conversions Work at Call Boundary

           void run_shift(std::unique_ptr<Vehicle> v);  // Accepts base type
           
           auto rt = std::make_unique<RoboTaxi>(...);   // unique_ptr<RoboTaxi>
           run_shift(std::move(rt));  // ✓ Compiler converts RoboTaxi* → Vehicle*
                                      //   Conversion happens at call boundary

    .. tab-item:: Container Storage ✗

        .. code-block:: cpp
           :caption: Template Types Don't Convert

           std::vector<std::unique_ptr<Vehicle>> fleet;  // Template parameter is FIXED
           
           auto rt = std::make_unique<RoboTaxi>(...);    // unique_ptr<RoboTaxi>
           fleet.push_back(std::move(rt));  // ✗ Template types don't convert!
                                            // unique_ptr<RoboTaxi> ≠ unique_ptr<Vehicle>

.. warning::

   **Key insight:** ``unique_ptr<Derived>`` is NOT a subtype of ``unique_ptr<Base>``, even though ``Derived*`` converts to ``Base*``. Template instantiations don't inherit type relationships!

Solutions for Polymorphic Collections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

    .. tab-item:: Option 1: Direct Construction ⭐

        .. code-block:: cpp
           :caption: Best Practice

           std::vector<std::unique_ptr<Vehicle>> fleet;
           fleet.push_back(std::make_unique<RoboTaxi>(...));  // ✓ Implicit conversion
           fleet.push_back(std::make_unique<Taxi>(...));      // ✓ Implicit conversion

    .. tab-item:: Option 2: Base Type from Start

        .. code-block:: cpp
           :caption: Clear Intent

           std::unique_ptr<Vehicle> rt = std::make_unique<RoboTaxi>(...);
           rt->drive();  // Polymorphic call
           fleet.push_back(std::move(rt));  // ✓ Types match exactly

    .. tab-item:: Option 3: Explicit Cast

        .. code-block:: cpp
           :caption: Avoid - Verbose and Error-Prone

           auto rt = std::make_unique<RoboTaxi>(...);
           fleet.push_back(std::unique_ptr<Vehicle>(std::move(rt)));  // ✓ But ugly

Decision Framework
~~~~~~~~~~~~~~~~~~

.. grid:: 2 2 2 2
    :gutter: 3

    .. grid-item-card:: Container Storage?
        :class-card: sd-border-primary
        
        → Use **explicit base type** OR **direct insertion**

    .. grid-item-card:: Polymorphic Calls at Use?
        :class-card: sd-border-primary
        
        → Use **explicit base type**

    .. grid-item-card:: Derived-Specific Methods First?
        :class-card: sd-border-primary
        
        → Use **auto**, then pass to functions

    .. grid-item-card:: Only Function Calls?
        :class-card: sd-border-primary
        
        → Either works; **auto** is more flexible

.. important::

   **Rule of thumb:** If you're building polymorphic collections, use explicit base type or direct insertion. If you're only calling functions, ``auto`` is fine.

----

The ``override`` Keyword
------------------------

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-md sd-rounded-1
    
    **Definition:** The ``override`` keyword is a **safety feature** that tells the compiler "I intend this method to override a base class virtual method".

**Benefits:**

.. grid:: 3
    :gutter: 3

    .. grid-item-card:: Catches Typos
        
        If signatures don't match, compilation fails

    .. grid-item-card:: Documents Intent
        
        Makes it clear this overrides a base method

    .. grid-item-card:: Prevents Hiding
        
        Detects when you think you're overriding but aren't

.. code-block:: cpp
   :caption: Using override for Safety
   :emphasize-lines: 8

   class Vehicle {
   public:
       virtual void drive();
   };

   class RoboTaxi : public Vehicle {
   public:
       void drive() override;        // OK - matches base signature
       // void drive(int) override;  // ERROR - no matching virtual in base
       // void driev() override;     // ERROR - typo caught!
   };

.. important::

   Always use ``override`` when overriding virtual methods. It's free safety!

----

Avoid Slicing & Embrace Polymorphic Collections
------------------------------------------------

.. code-block:: cpp
   :caption: Polymorphic Collection Example

   std::vector<std::unique_ptr<transportation::Vehicle>> fleet;
   fleet.emplace_back(std::make_unique<transportation::RoboTaxi>("ROBOTAXI-001", 4));
   fleet.emplace_back(std::make_unique<transportation::Taxi>("TAXI-001", 4));

   for (auto& v : fleet) {
       v->drive();   // Runtime dispatch for each element's actual type
   }

.. warning::

   Do not store derived objects by value in a ``std::vector<Vehicle>``. This causes *object slicing* where derived class data is lost and polymorphism doesn't work. Use owning pointers (``unique_ptr``, ``shared_ptr``), or non-owning pointers/references with external lifetime management.

Requirements for Runtime Polymorphism
--------------------------------------

.. grid:: 3
    :gutter: 3

    .. grid-item-card:: 1.Inheritance ✓
        :class-card: sd-border-primary sd-border-2
        
        Derived classes inherit from common base (``Vehicle``)

    .. grid-item-card:: 2. Base Handle ✓
        :class-card: sd-border-primary sd-border-2
        
        Use ``Vehicle&``, ``Vehicle*``, ``unique_ptr<Vehicle>``

    .. grid-item-card:: 3. Virtual Method ✓
        :class-card: sd-border-primary sd-border-2
        
        Mark interface ``virtual``; override in derived classes

.. note::

   The call target depends on the **dynamic type** of the object (what it actually is at runtime), not the **static type** of the handle (how the pointer/reference was declared). This is *late binding*.

----

Key Takeaways
=============

.. card::
    :class-card: sd-border-primary sd-border-3 sd-shadow-lg
    
    **Core Concepts:**
    
    • **Compile-time polymorphism:** Function/operator overloading, method redefinition
    
    • **Runtime polymorphism:** Virtual methods with dynamic dispatch
    
    • Use ``virtual`` in base classes for methods that derived classes will override
    
    • Always use ``override`` in derived classes for safety
    
    • Prefer explicit base type when building polymorphic collections
    
    • Use ``auto`` when you need concrete type initially, then pass to functions
    
    • Remember: ``unique_ptr<Derived>`` ≠ ``unique_ptr<Base>`` for containers
    
    • Direct insertion works best for polymorphic collections

.. grid:: 1 2 2 4
    :gutter: 3
    :class-container: sd-text-center

    .. grid-item-card:: Compile-Time
        :class-card: sd-border-info
        
        Static resolution

    .. grid-item-card:: Runtime
        :class-card: sd-border-info
        
        Dynamic dispatch

    .. grid-item-card:: Virtual
        :class-card: sd-border-info
        
        Enable polymorphism

    .. grid-item-card:: Override
        :class-card: sd-border-info
        
        Safety feature