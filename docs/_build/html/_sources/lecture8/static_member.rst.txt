===============
Static Members
===============

Introduction
------------

In C++, **static members** belong to the **class itself** rather than to any individual object. This means:

- There is only **one copy** of a static member shared by all instances of the class
- Static members exist even if no objects of the class have been created
- They are useful for class-wide data (counters, constants) and utility functions

Static members come in two forms:

1. **Static attributes** (static data members)
2. **Static methods** (static member functions)

Static Attributes
-----------------

Definition
~~~~~~~~~~

A **static attribute** is a data member that belongs to the class itself, not to any individual object.

Key Characteristics
~~~~~~~~~~~~~~~~~~~

- **Shared by all instances:** Only one copy exists, regardless of how many objects are created
- **Exists independently:** The static attribute exists even if no objects are instantiated
- **Class-level scope:** Accessed through the class name (e.g., ``ClassName::static_member``)
- **Common uses:** Class-wide constants, counters, shared resources, configuration data

Syntax (C++17 and later)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Vehicle {
   private:
       inline static int vehicle_count_{0};  // C++17: inline static with initialization
       std::string model_;
       
   public:
       Vehicle(const std::string& model) : model_{model} {
           ++vehicle_count_;
       }
       
       ~Vehicle() {
           --vehicle_count_;
       }
   };

.. note::

   Starting with C++17, you can use ``inline static`` to both declare and initialize static members directly in the class definition, avoiding separate out-of-class definitions.

Syntax (C++14 and earlier)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
   private:
       static int vehicle_count_;  // Declaration only
       
   public:
       Vehicle();
   };
   
   // vehicle.cpp
   int Vehicle::vehicle_count_{0};  // Definition and initialization

Example: Tracking Object Count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   #include <iostream>
   #include <string>

   class Vehicle {
   private:
       inline static int vehicle_count_{0};
       std::string model_;

   public:
       Vehicle(const std::string& model) : model_{model} {
           ++vehicle_count_;
       }
       
       ~Vehicle() {
           --vehicle_count_;
       }

       [[nodiscard]] static int get_vehicle_count() noexcept {
           return vehicle_count_;
       }
   };

   int main() {
       std::cout << Vehicle::get_vehicle_count() << '\n';  // 0
       
       Vehicle car1("Sedan");
       std::cout << Vehicle::get_vehicle_count() << '\n';  // 1
       
       Vehicle car2("SUV");
       std::cout << Vehicle::get_vehicle_count() << '\n';  // 2
       
       {
           Vehicle car3("Truck");
           std::cout << Vehicle::get_vehicle_count() << '\n';  // 3
       }  // car3 goes out of scope, destructor called
       
       std::cout << Vehicle::get_vehicle_count() << '\n';  // 2
   }

Static Methods
--------------

Definition
~~~~~~~~~~

A **static method** is a member function that belongs to the class itself, not to any individual object.

Key Characteristics
~~~~~~~~~~~~~~~~~~~

- **No** ``this`` **pointer:** Static methods cannot access non-static members (attributes or methods)
- **Class-level access:** Can be called using the class name: ``ClassName::method()``
- **Can access static members only:** Only static attributes and other static methods are accessible
- **Can be called without an object:** No instance required
- **Common uses:** Utility functions, factory methods, accessors for static data

Why No this Pointer?
~~~~~~~~~~~~~~~~~~~~~

Static methods are not associated with any particular object. Since ``this`` points to a specific object instance, it doesn't make sense in a static context.

.. danger::

   **Compilation Error:**
   
   .. code-block:: cpp
   
      class Example {
      private:
          int value_;
          static int count_;
          
      public:
          static void static_method() {
              value_ = 42;  // ❌ ERROR: cannot access non-static member
              count_ = 10;  // ✓ OK: can access static member
          }
      };

Syntax
~~~~~~

.. code-block:: cpp

   class Vehicle {
   private:
       inline static int vehicle_count_{0};
       std::string model_;

   public:
       Vehicle(const std::string& model) : model_{model} {
           ++vehicle_count_;
       }

       // Static method - note: no 'this' pointer
       [[nodiscard]] static int get_vehicle_count() noexcept {
           return vehicle_count_;
       }
   };

   int main() {
       // Call via class name (preferred)
       std::cout << Vehicle::get_vehicle_count() << '\n';  // 0
       
       Vehicle car("Sedan");
       
       // Can also call via object (but less clear)
       std::cout << car.get_vehicle_count() << '\n';  // 1
   }

Complete Example
----------------

.. code-block:: cpp

   #include <iostream>
   #include <string>

   class Vehicle {
   private:
       inline static int vehicle_count_{0};  // Shared by all instances
       std::string model_;
       int id_;

   public:
       // Constructor
       Vehicle(const std::string& model) 
           : model_{model}, id_{++vehicle_count_} {
           std::cout << "Vehicle #" << id_ << " (" << model_ 
                     << ") created. Total: " << vehicle_count_ << '\n';
       }

       // Destructor
       ~Vehicle() {
           std::cout << "Vehicle #" << id_ << " (" << model_ 
                     << ") destroyed.\n";
           --vehicle_count_;
       }

       // Static method to access static data
       [[nodiscard]] static int get_vehicle_count() noexcept {
           return vehicle_count_;
       }

       // Regular (non-static) methods
       [[nodiscard]] const std::string& get_model() const noexcept {
           return model_;
       }
       
       [[nodiscard]] int get_id() const noexcept {
           return id_;
       }
   };

   int main() {
       std::cout << "Initial count: " 
                 << Vehicle::get_vehicle_count() << "\n\n";

       Vehicle car("Sedan");
       std::cout << "Count: " << Vehicle::get_vehicle_count() << "\n\n";

       {
           Vehicle truck("Pickup");
           Vehicle suv("SUV");
           std::cout << "Count: " << Vehicle::get_vehicle_count() << "\n\n";
       }  // truck and suv destroyed here

       std::cout << "Count after scope: " 
                 << Vehicle::get_vehicle_count() << "\n\n";
   }

**Output:**

.. code-block:: text

   Initial count: 0

   Vehicle #1 (Sedan) created. Total: 1
   Count: 1

   Vehicle #2 (Pickup) created. Total: 2
   Vehicle #3 (SUV) created. Total: 3
   Count: 3

   Vehicle #2 (Pickup) destroyed.
   Vehicle #3 (SUV) destroyed.
   Count after scope: 1

Common Use Cases
----------------

1. Tracking Object Count
~~~~~~~~~~~~~~~~~~~~~~~~~

As shown above, static members can track how many objects of a class exist.

2. Shared Configuration
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Database {
   private:
       inline static std::string connection_string_{"localhost:5432"};
       inline static int max_connections_{100};
       
   public:
       [[nodiscard]] static const std::string& get_connection_string() noexcept {
           return connection_string_;
       }
       
       static void set_max_connections(int max) {
           if (max > 0) {
               max_connections_ = max;
           }
       }
   };

3. Factory Methods
~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Color {
   private:
       int r_;
       int g_;
       int b_;
       
       Color(int r, int g, int b) : r_{r}, g_{g}, b_{b} {}
       
   public:
       [[nodiscard]] static Color red() noexcept {
           return Color(255, 0, 0);
       }
       
       [[nodiscard]] static Color green() noexcept {
           return Color(0, 255, 0);
       }
       
       [[nodiscard]] static Color blue() noexcept {
           return Color(0, 0, 255);
       }
   };

   int main() {
       Color red = Color::red();
       Color green = Color::green();
   }

4. Utility Functions
~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class MathUtils {
   public:
       [[nodiscard]] static int add(int a, int b) noexcept {
           return a + b;
       }
       
       [[nodiscard]] static double square(double x) noexcept {
           return x * x;
       }
       
       [[nodiscard]] static double distance(double x1, double y1, 
                                             double x2, double y2) noexcept {
           double dx = x2 - x1;
           double dy = y2 - y1;
           return std::sqrt(dx * dx + dy * dy);
       }
   };

   int main() {
       int result = MathUtils::add(5, 3);
       double sq = MathUtils::square(4.5);
       double dist = MathUtils::distance(0, 0, 3, 4);  // 5.0
   }

Accessing Static Members
-------------------------

Static members can be accessed in two ways:

1. Using Class Name (Preferred)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   int count = Vehicle::get_vehicle_count();  // ✓ Clear and explicit

This is the **preferred** approach because it makes it immediately clear that you're accessing class-level data, not instance-level data.

2. Using Object Instance
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   Vehicle car("Sedan");
   int count = car.get_vehicle_count();  // ✓ Works, but less clear

While this works, it's less clear that ``get_vehicle_count()`` is a static method.

.. tip::

   **Best Practice:** Always access static members using the class name (``ClassName::member``) to make it clear that you're accessing class-level data.

Static vs. Non-Static Comparison
---------------------------------

.. list-table::
   :widths: 30 35 35
   :header-rows: 1

   * - Aspect
     - Non-Static Member
     - Static Member
   * - **Belongs to**
     - Individual object
     - Class itself
   * - **Copies**
     - One per object
     - One shared copy
   * - **Access**
     - Requires object instance
     - Via class name or object
   * - ``this`` **pointer**
     - Available
     - Not available
   * - **Can access non-static members**
     - Yes
     - No
   * - **Can access static members**
     - Yes
     - Yes
   * - **Exists when**
     - Object exists
     - Always (once initialized)

Important Rules
---------------

.. warning::

   **Static methods CANNOT:**
   
   - Access non-static data members
   - Call non-static methods
   - Use the ``this`` pointer
   
   **Static methods CAN:**
   
   - Access static data members
   - Call other static methods
   - Access global functions and data

.. important::

   **Memory considerations:**
   
   - Static members are stored in the **data segment**, not on the stack or heap with objects
   - They exist for the entire program lifetime
   - Only one copy exists regardless of object count

Common Pitfalls
---------------

1. Forgetting to Define Static Members (Pre-C++17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // ❌ Wrong (C++14 and earlier)
   class Vehicle {
   private:
       static int count_{0};  // Declaration only—linker error!
   };
   
   // ✓ Correct (C++14 and earlier)
   // vehicle.hpp
   class Vehicle {
   private:
       static int count_;  // Declaration
   };
   
   // vehicle.cpp
   int Vehicle::count_{0};  // Definition

2. Trying to Access Non-Static Members
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Vehicle {
   private:
       std::string model_;
       static int count_;
       
   public:
       static void print_model() {
           std::cout << model_ << '\n';  // ❌ ERROR: no 'this' pointer!
       }
   };

3. Confusing Static and Non-Static
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Vehicle {
   private:
       inline static int count_{0};
       
   public:
       // ❌ Wrong: trying to make count_ non-static in constructor
       Vehicle() : count_{0} {}  // ERROR: cannot initialize static member here
       
       // ✓ Correct: increment the shared static member
       Vehicle() { ++count_; }
   };

Summary
-------

**Key Takeaways:**

- Static attributes belong to the class, with only one copy shared by all instances
- Static methods can only access static members and have no ``this`` pointer
- Use ``inline static`` (C++17+) for in-class initialization of static members
- Access static members via class name: ``ClassName::member()``
- Common uses: counters, shared configuration, factory methods, utility functions
- Static members exist for the entire program lifetime

**Best Practices:**

- Use ``[[nodiscard]]`` and ``noexcept`` on static getter methods when appropriate
- Always access static members using the class name for clarity
- Use static methods for functionality that doesn't depend on object state
- Be careful not to access non-static members from static methods

.. tip::

   **When to use static:**
   
   - Data that should be shared across all instances (counters, shared config)
   - Utility functions that don't need object state
   - Factory methods that create objects
   - Constants that belong to the class conceptually