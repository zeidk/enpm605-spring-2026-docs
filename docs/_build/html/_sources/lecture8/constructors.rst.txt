============
Constructors
============

A **constructor** is a special member function that initializes an object when it is created.

Key Characteristics
-------------------

- **Same name** as the class
- **No return type** (not even ``void``)
- **Automatically called** when object is instantiated
- **Used to initialize** object's attributes
- **Can be overloaded** (multiple constructors with different parameters)

.. code-block:: cpp

   class Vehicle {
   public:
       // Constructor
       Vehicle(const std::string& color, const std::string& model, int max_speed) {
           std::cout << "Vehicle constructed\n";
       }
   };
   
   Vehicle car{"red", "sedan", 120};  // Constructor called automatically

Default Constructor
-------------------

**Definition:** A constructor that takes **no arguments**.

Compiler-Generated Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't define **any** constructor, the compiler generates a default constructor that:

1. Leaves built-in types (``int``, ``double``, etc) **uninitialized** (garbage values)
2. Calls default constructor for user-defined type members (``std::string``, etc.)
3. Uses in-class initializers if provided

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;       // Default constructor → empty string
       std::string model_;       // Default constructor → empty string  
       bool is_running_{false};  // In-class initializer → false
       int max_speed_;           // UNINITIALIZED → garbage value!
   };
   
   Vehicle car;  // Compiler-generated default constructor called

.. danger::

   **Uninitialized primitives contain garbage values!** Always initialize or use in-class initializers.

User-Defined Default Constructor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;
       std::string model_;
       bool is_running_{false};
       int max_speed_;
       
   public:
       // User-defined default constructor
       Vehicle() {
           color_ = "White";
           model_ = "Unknown";
           max_speed_ = 0;
           std::cout << "Vehicle created with default values\n";
       }
   };
   
   transportation::Vehicle car;  // User-defined constructor called

.. note::

   Once you define **any** constructor (even parameterized), the compiler **will not** generate a default constructor unless you explicitly request it with ``= default``.

Parameterized Constructors
---------------------------

**Definition:** Constructors that accept one or more parameters to initialize attributes with specific values.

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;
       std::string model_;
       int max_speed_;
       
   public:
       // Parameterized constructor
       Vehicle(const std::string& color, const std::string& model, int max_speed) {
           color_ = color;
           model_ = model;
           max_speed_ = max_speed;
       }
       
       // Another parameterized constructor (overloading)
       Vehicle(int max_speed) {
           color_ = "Gray";
           model_ = "Standard";
           max_speed_ = max_speed;
       }
   };
   
   transportation::Vehicle car1{"red", "sedan", 120};  // Uses first constructor
   transportation::Vehicle car2{150};                   // Uses second constructor

.. warning::

   The above approach uses **assignment**, not initialization. This is inefficient!

Member Initializer List
------------------------

**Definition:** A more efficient way to initialize attributes **directly** before the constructor body executes.

Syntax
~~~~~~

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;
       std::string model_;
       bool is_running_;
       int max_speed_;
       
   public:
       // Constructor with member initializer list
       Vehicle(const std::string& color, const std::string& model, int max_speed)
           : color_{color}, model_{model}, is_running_{false}, max_speed_{max_speed} {
           // Body can be empty or contain additional logic
           std::cout << "Vehicle constructed\n";
       }
   };

Why Use Member Initializer Lists?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Direct Initialization**
  Attributes are initialized directly, avoiding default construction + assignment.

**2. Required for const and References**
  ``const`` and reference members **must** be initialized via initializer list.

.. code-block:: cpp

   class Vehicle {
   private:
       const std::string vin_;  // const member
       Engine& engine_;         // reference member
       
   public:
       // MUST use initializer list for const and references
       Vehicle(const std::string& vin, Engine& engine)
           : vin_{vin}, engine_{engine} {
           // vin_ = vin;      // ❌ Error: cannot assign to const
           // engine_ = engine; // ❌ Error: cannot reassign reference
       }
   };

**3. Efficiency**
  Avoids creating temporary objects that occur with assignment.

Inefficient vs. Efficient Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Inefficient (Assignment in Body):**

.. code-block:: cpp

   class Vehicle {
   private:
       std::string model_;
       
   public:
       Vehicle(const std::string& model) {
           model_ = model;  // 1. Default construct, 2. Assign
       }
   };

**Efficient (Member Initializer List):**

.. code-block:: cpp

   class Vehicle {
   private:
       std::string model_;
       
   public:
       Vehicle(const std::string& model)
           : model_{model} {  // Direct construction
       }
   };

Detailed Example: Two-Step Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class A {
   public:
       A() { std::cout << "default ctor A\n"; }
       A(int x) : x_{x} { std::cout << "param ctor A\n"; }
   private:
       int x_;
   };

   class B {
   public:
       // ❌ Inefficient: Two constructors called for A
       B() {
           std::cout << "default ctor B\n";
           a_ = A(2);  // Creates temporary, assigns, destroys
       }
   private:
       A a_;  // Default constructor called here first!
   };
   
   int main() {
       B b;
   }

**Output:**

.. code-block:: text

   default ctor A    ← a_ default constructed
   default ctor B    ← B constructor body starts
   param ctor A      ← Temporary A(2) created
                     ← Temporary assigned to a_, then destroyed

**Fixed with Member Initializer List:**

.. code-block:: cpp

   class B {
   public:
       // ✓ Efficient: Only one constructor called for A
       B() : a_{2} {
           std::cout << "default ctor B\n";
       }
   private:
       A a_;
   };
   
   int main() {
       B b;
   }

**Output:**

.. code-block:: text

   param ctor A      ← a_ constructed directly with A(2)
   default ctor B    ← B constructor body

C++ Object Construction Order
-----------------------------

When an object is created, C++ follows a strict initialization sequence:

1. **Base class constructors** — If the class inherits from a base class, the base class constructor(s) execute first (in declaration order for multiple inheritance).
2. **Member attribute constructors** — All member objects are constructed in the order they are *declared* in the class definition, regardless of the order in the member initializer list.
3. **Constructor body** — Finally, the statements in the constructor body execute.

.. important::

   The order in the member initializer list does **not** affect the initialization order. Members are always initialized in **declaration order**.

Constructor Initialization Order
---------------------------------

Members are **always initialized in declaration order**, not the order in the initializer list.

.. code-block:: cpp

   class Vehicle {
   private:
       int max_speed_;    // Initialized FIRST (declaration order)
       std::string model_; // Initialized SECOND
       
   public:
       // Order in list doesn't matter!
       Vehicle(const std::string& model, int speed)
           : model_{model}, max_speed_{speed} {  // List order ≠ init order
       }
   };

.. tip::

   Match initializer list order to declaration order for readability, even though it doesn't affect execution.

Declaration Order Matters
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Rectangle {
   private:
       double area_;   // 1. initialized FIRST
       double width_;  // 2. initialized SECOND
       double height_; // 3. initialized THIRD
       
   public:
       Rectangle(double w, double h)
           : width_{w}, height_{h}, area_{width_ * height_} {
           // ❌ PROBLEM: area_ is computed using uninitialized width_ and height_!
           // area_ initializes FIRST, but width_ and height_ haven't been set yet
       }
   };

   int main() {
       Rectangle rect(4, 10);  // area_ will have garbage value!
   }

**The Problem:** Even though ``width_{w}`` and ``height_{h}`` appear before ``area_{width_ * height_}`` in the initializer list, ``area_`` is initialized first (with uninitialized ``width_`` and ``height_``) because of declaration order.

**Solution:** Reorder the declarations:

.. code-block:: cpp

   class Rectangle {
   private:
       double width_;  // 1. initialized FIRST
       double height_; // 2. initialized SECOND
       double area_;   // 3. initialized THIRD
       
   public:
       Rectangle(double w, double h)
           : width_{w}, height_{h}, area_{width_ * height_} {
           // ✓ OK: width_ and height_ are initialized before area_
       }
   };

const Objects
-------------

Definition
~~~~~~~~~~

A **const object** is an instance of a class whose state cannot be modified after it is created.

.. code-block:: cpp

   const Vehicle car("White", "Camry", 113);
   car.start_engine();  // ❌ Error: cannot call non-const method on const object

Key Rules
~~~~~~~~~

When you declare an object as ``const``, all its non-``const`` methods become inaccessible—only methods marked as ``const`` can be called.

This enforces **read-only access** to the object's internal data and ensures **const-correctness**.

.. code-block:: cpp

   class Vehicle {
   private:
       std::string model_;
       bool is_running_{false};
       
   public:
       Vehicle(const std::string& model) : model_{model} {}
       
       // Non-const method
       void start_engine() {
           is_running_ = true;
       }
       
       // Const method
       [[nodiscard]] const std::string& get_model() const noexcept {
           return model_;
       }
       
       [[nodiscard]] bool is_running() const noexcept {
           return is_running_;
       }
   };

   int main() {
       const Vehicle car("Camry");
       
       // ✓ OK: calling const methods
       std::cout << car.get_model() << '\n';
       std::cout << car.is_running() << '\n';
       
       // ❌ Error: cannot call non-const method on const object
       car.start_engine();
   }

.. note::

   Non-``const`` objects can access both ``const`` and non-``const`` methods, but ``const`` objects can only access ``const`` methods.

Constructor Best Practices
---------------------------

.. important::

   **Always use member initializer lists:**

   - ✓ More efficient (direct initialization)
   - ✓ Required for ``const`` and references
   - ✓ Prevents two-step initialization
   - ✓ Industry standard practice

**Template:**

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;
       std::string model_;
       int max_speed_;
       bool is_running_{false};  // In-class initializer for defaults
       
   public:
       // Default constructor
       Vehicle()
           : color_{"White"}, model_{"Unknown"}, max_speed_{0} {
       }
       
       // Parameterized constructor
       Vehicle(const std::string& color, const std::string& model, int max_speed)
           : color_{color}, model_{model}, max_speed_{max_speed} {
           // Validation logic can go here
           if (max_speed_ < 0) {
               throw std::invalid_argument("Speed cannot be negative");
           }
       }
   };

Common Mistakes
---------------

.. warning::

   **Critical Errors:**

   ❌ Not using member initializer lists
   
   .. code-block:: cpp
   
      Vehicle(const std::string& model) {
          model_ = model;  // Inefficient! Use initializer list
      }

   ❌ Forgetting semicolon after class
   
   .. code-block:: cpp
   
      class Vehicle {
          // ...
      }  // ❌ Missing semicolon!

   ❌ Uninitialized primitives
   
   .. code-block:: cpp
   
      class Vehicle {
      private:
          int max_speed_;  // ❌ Uninitialized! Use {0} or initializer list
      };

   ❌ Wrong initialization order assumptions
   
   .. code-block:: cpp
   
      class Vehicle {
      private:
          int speed_;
          int max_speed_;
      public:
          // Members initialize in DECLARATION order (speed_, then max_speed_)
          // Not in initializer list order!
          Vehicle() : max_speed_{100}, speed_{max_speed_ / 2} {}  // ❌ Dangerous!
      };

Summary
-------

**Constructor Checklist:**

- ✓ Always use member initializer lists
- ✓ Initialize all members (especially primitives)
- ✓ Validate parameters in constructor body when needed
- ✓ Provide both default and parameterized constructors when appropriate
- ✓ Use ``const std::string&`` for string parameters
- ✓ Match initializer list order to declaration order (for readability)

.. tip::

   **Quick rule:** If you're assigning to members in the constructor body instead of using an initializer list, you're doing it wrong!

Example: Complete Constructor Implementation
---------------------------------------------

.. code-block:: cpp

   namespace transportation {

   class Vehicle {
   private:
       std::string color_;
       std::string model_;
       bool is_running_{false};
       int max_speed_;

   public:
       // Default constructor
       Vehicle()
           : color_{"White"}, model_{"Unknown"}, max_speed_{0} {
       }

       // Parameterized constructor with validation
       Vehicle(const std::string& color, const std::string& model, int max_speed)
           : color_{color}, model_{model}, max_speed_{max_speed} {
           if (max_speed_ < 0) {
               throw std::invalid_argument("Max speed cannot be negative");
           }
       }
   };

   }  // namespace transportation