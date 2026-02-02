====================
Core OOP Principles
====================

Object-Oriented Programming is built around a set of fundamental principles that shape how code is structured, organized, and maintained. These concepts help developers build modular, scalable, and maintainable systems.

Overview
--------

OOP organizes software around **objects** — digital models of real-world things that hold data and perform actions. This approach helps make code more understandable, reusable, and easier to manage.

The Four Pillars of OOP
------------------------

Encapsulation
~~~~~~~~~~~~~

**Definition:** Groups data and the methods that operate on it into objects, shielding internal details from external access.

**Key Concepts:**

- Data hiding: private attributes protected from direct access
- Controlled access: public methods (accessors/mutators) manage data interaction
- Implementation details hidden from users

**Benefits:**

- Prevents unauthorized or accidental modification of data
- Allows internal changes without affecting external code
- Enforces class invariants and business rules

**Example:**

.. code-block:: cpp

   class BankAccount {
   private:
       double balance_;  // Hidden from direct access
       
   public:
       void deposit(double amount) {
           if (amount > 0) {
               balance_ += amount;  // Controlled modification
           }
       }
       
       [[nodiscard]] double get_balance() const noexcept {
           return balance_;  // Read-only access
       }
   };

Abstraction
~~~~~~~~~~~

**Definition:** Simplifies complexity by exposing only essential features while hiding the underlying implementation.

**Key Concepts:**

- Focus on "what" an object does, not "how" it does it
- Simplifies interfaces for users
- Reduces cognitive load

**Benefits:**

- Makes complex systems manageable
- Allows implementation changes without affecting users
- Promotes modular design

**Example:**

.. code-block:: cpp

   class Vehicle {
   public:
       void start_engine();  // User doesn't need to know HOW
       void drive();         // Implementation details hidden
       
   private:
       void ignite_spark_plugs();     // Hidden complexity
       void engage_fuel_injection();  // Hidden complexity
       void activate_drivetrain();    // Hidden complexity
   };

Inheritance
~~~~~~~~~~~

**Definition:** Enables new classes to reuse and extend the functionality of existing ones, fostering code reuse and hierarchy.

**Key Concepts:**

- "Is-a" relationship (Car *is a* Vehicle)
- Base