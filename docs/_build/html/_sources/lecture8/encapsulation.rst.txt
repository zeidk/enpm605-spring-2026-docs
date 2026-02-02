==============
Encapsulation
==============

Encapsulation (data hiding) is the practice of restricting direct access to an object's internal data, providing controlled access through public methods.

Why Encapsulation?
------------------

**Security**
  Protects data from unauthorized or accidental modification

**Flexibility**
  Allows internal changes without breaking external code

**Validation**
  Enforces business rules and maintains class invariants

**Maintainability**
  Centralizes data access logic

.. danger::

   **All class attributes MUST be encapsulated using** ``private`` **or** ``protected`` **access specifiers.**
   
   Failure to encapsulate attributes = **automatic 0** on assignments. This is non-negotiable.

Access Specifiers
-----------------

C++ provides three access specifiers to control member visibility:

``public``
~~~~~~~~~~

Members accessible from anywhere.

.. code-block:: cpp

   class Vehicle {
   public:
       void start_engine();  // Anyone can call this
   };

**Use for:** Methods that form the class's public interface.

``private``
~~~~~~~~~~~

Members accessible only within the class.

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;  // Only Vehicle methods can access
   };

**Use for:** Attributes and internal helper methods.

``protected``
~~~~~~~~~~~~~

Members accessible within the class and derived classes.

.. code-block:: cpp

   class Vehicle {
   protected:
       int max_speed_;  // Accessible in derived classes (Car, Truck)
   };

**Use for:** Attributes/methods shared with derived classes (*covered in Lecture 9*).

.. warning::

   If you don't specify an access specifier, C++ defaults to ``private`` for classes.

Encapsulation Example
---------------------

**Bad (No Encapsulation):**

.. code-block:: cpp

   class Vehicle {
   public:
       std::string color_;  // ❌ Direct access - anyone can modify!
       int max_speed_;      // ❌ No validation possible!
   };
   
   int main() {
       Vehicle car;
       car.max_speed_ = -100;  // ❌ Invalid but compiles!
   }

**Good (Proper Encapsulation):**

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;  // ✓ Protected
       int max_speed_;      // ✓ Protected
       
   public:
       // Controlled access
       [[nodiscard]] const std::string& get_color() const noexcept {
           return color_;
       }
       
       void set_max_speed(int speed) {
           if (speed < 0) {
               throw std::invalid_argument("Speed cannot be negative");
           }
           max_speed_ = speed;  // ✓ Validated!
       }
   };

Accessors (Getters)
-------------------

**Definition:** Public methods providing **read-only** access to private attributes.

Syntax and Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Vehicle {
   private:
       bool is_running_{false};
       std::string model_;
       
   public:
       // Return by value for small types
       [[nodiscard]] bool is_running() const noexcept {
           return is_running_;
       }
       
       // Return by const reference for large types
       [[nodiscard]] const std::string& get_model() const noexcept {
           return model_;
       }
   };

Key Points
~~~~~~~~~~

- **Return type:** Value for primitives, ``const&`` for large types
- **``const``:** Always mark accessors as ``const``
- **``[[nodiscard]]``:** Prevent accidentally ignoring return value
- **``noexcept``:** Use when accessor cannot throw
- **Never:** Return non-const reference (breaks encapsulation)

const-Correctness
~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // ✓ Correct: const guarantees no modification
   [[nodiscard]] bool is_running() const noexcept {
       // is_running_ = true;  // ❌ Compilation error!
       return is_running_;
   }
   
   // ❌ Wrong: missing const allows accidental modification
   [[nodiscard]] bool is_running() noexcept {
       is_running_ = true;  // ✓ Compiles but violates accessor contract!
       return is_running_;
   }

Why ``const`` Matters
~~~~~~~~~~~~~~~~~~~~~

1. **Compile-time guarantee:** Prevents accidental modification
2. **Self-documenting:** Clearly states intent
3. **Enables calling on const objects:**

.. code-block:: cpp

   void process(const Vehicle& car) {
       bool running = car.is_running();  // Only works if accessor is const
   }

Mutators (Setters)
------------------

**Definition:** Public methods providing **controlled modification** of private attributes.

Syntax and Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class Vehicle {
   private:
       std::string color_;
       int max_speed_;
       
   public:
       // Simple setter
       void set_color(const std::string& color) noexcept {
           color_ = color;
       }
       
       // Setter with validation
       void set_max_speed(int speed) {
           if (speed < 0) {
               throw std::invalid_argument("Max speed cannot be negative");
           }
           max_speed_ = speed;
       }
   };

Key Points
~~~~~~~~~~

- **Return type:** Typically ``void``
- **Parameters:** ``const&`` for large types, value for small types
- **Never ``const``:** Mutators modify state
- **Validation:** Enforce business rules and invariants
- **``noexcept``:** Only if validation doesn't throw

Why Mutators Cannot Be const
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // ✓ Correct: can modify member
   void set_is_running(bool running) noexcept {
       is_running_ = running;  // OK
   }
   
   // ❌ Wrong: const prevents modification
   void set_is_running(bool running) const noexcept {
       is_running_ = running;  // ❌ Compilation error!
   }

Mutators modify object state, so they must **not** be ``const``.

Validation Examples
~~~~~~~~~~~~~~~~~~~

**Range checking:**

.. code-block:: cpp

   void set_max_speed(int speed) {
       if (speed < 0 || speed > 500) {
           throw std::out_of_range("Speed must be 0-500 km/h");
       }
       max_speed_ = speed;
   }

**Non-empty validation:**

.. code-block:: cpp

   void set_model(const std::string& model) {
       if (model.empty()) {
           throw std::invalid_argument("Model cannot be empty");
       }
       model_ = model;
   }

**Business rule enforcement:**

.. code-block:: cpp

   void set_color(const std::string& color) {
       static const std::set<std::string> valid_colors{
           "red", "blue", "white", "black", "gray"
       };
       
       if (valid_colors.find(color) == valid_colors.end()) {
           throw std::invalid_argument("Invalid color");
       }
       color_ = color;
   }

Common Mistakes
---------------

.. warning::

   **Critical Errors:**

   ❌ Forgetting ``const`` on accessors
   
   .. code-block:: cpp
   
      bool is_running();  // Wrong! Should be const

   ❌ Returning non-const reference from accessor
   
   .. code-block:: cpp
   
      std::string& get_color();  // Wrong! Breaks encapsulation

   ❌ Making attributes ``public``
   
   .. code-block:: cpp
   
      public:
          std::string color_;  // Wrong! Direct access!

   ❌ Not validating in mutators
   
   .. code-block:: cpp
   
      void set_max_speed(int speed) {
          max_speed_ = speed;  // Wrong! No validation!
      }

Summary
-------

**Encapsulation Checklist:**

- ✓ All attributes are ``private`` or ``protected``
- ✓ Accessors marked ``const noexcept`` when appropriate
- ✓ Accessors use ``[[nodiscard]]`` attribute
- ✓ Mutators validate input
- ✓ Never return non-const references from accessors
- ✓ Use ``const std::string&`` for large types in parameters

.. tip::

   When in doubt about whether a method should be ``const``, ask: "Does this method modify any member variables?" If no, make it ``const``.