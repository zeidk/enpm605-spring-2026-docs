===================
Classes and Objects
===================

Classes
-------

**Definition:** A class is a **blueprint** or template for creating objects.


Components of a Class
~~~~~~~~~~~~~~~~~~~~~

**Attributes (Data Members)**
  Properties or characteristics that represent the object's state.
  
  - Example: ``color``, ``model``, ``is_running``
  - Typically ``private`` for encapsulation

**Methods (Member Functions)**
  Functions or actions that an object can perform.
  
  - Example: ``start_engine()``, ``stop_engine()``, ``drive()``
  - Typically ``public`` to provide interface

Class Definition Syntax
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // vehicle.hpp
   #include <string>

   namespace transportation {

   class Vehicle {
   private:
       // Attributes
       std::string color_;
       std::string model_;
       bool is_running_{false};
       int max_speed_;

   public:
       // Constructor
       Vehicle(const std::string& color, const std::string& model, 
               int max_speed);
       
       // Methods
       void start_engine();
       void stop_engine();
       void drive();
       
       // Accessors/Mutators
       [[nodiscard]] bool is_running() const noexcept;
       [[nodiscard]] const std::string& get_model() const noexcept;
   };  // class Vehicle - note the semicolon!

   }  // namespace transportation

Key Conventions
~~~~~~~~~~~~~~~

- **File naming:** ``snake_case`` (e.g., ``vehicle.hpp``)
- **Class naming:** ``PascalCase`` (e.g., ``Vehicle``)
- **Attribute naming:** ``snake_case`` with trailing underscore (e.g., ``color_``)
- **Method naming:** ``snake_case`` (e.g., ``start_engine()``)
- **Semicolon:** Required after class definition
- **End comment:** ``};  // class Vehicle``

Objects
-------

**Definition:** An object is a **concrete instance** of a class.


Characteristics of Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**State (Unique Attributes)**
  Each object has its own set of attribute values.

.. code-block:: cpp

   Vehicle blue_car{"blue", "Wraith", 131};
   Vehicle red_car{"red", "Wraith", 131};
   
   // blue_car.color_ = "blue"  (separate from red_car.color_)
   // red_car.color_ = "red"    (separate from blue_car.color_)

**Behavior (Shared Methods)**
  All objects share the same methods defined in the class.

.. code-block:: cpp

   blue_car.start_engine();  // Same method implementation
   red_car.start_engine();   // Same method implementation


Object Independence
~~~~~~~~~~~~~~~~~~~

Each object exists independently. Destroying one doesn't affect others.

.. code-block:: cpp

   {
       Vehicle car1{"blue", "Sedan", 120};
       Vehicle car2{"red", "SUV", 140};
   }  // car1 destroyed here, car2 remains valid

Instantiation
-------------

**Instantiation** is the process of creating a new object from a class blueprint.

Stack vs. Heap Allocation
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Stack Allocation (Automatic)**

.. code-block:: cpp

   Vehicle stack_car{"gray", "civic", 131};
   stack_car.start_engine();
   // Automatically destroyed when out of scope

**Heap Allocation (Dynamic)**

.. code-block:: cpp

   // Using smart pointers (modern C++)
   auto heap_car = std::make_unique<Vehicle>("gray", "civic", 131);
   heap_car->start_engine();
   // Automatically cleaned up when unique_ptr goes out of scope

.. important::

   Prefer stack allocation when possible. Use ``std::unique_ptr`` or ``std::shared_ptr`` for dynamic allocation instead of raw ``new``/``delete``.

Key Takeaways
-------------

- **Class** = Blueprint (defines structure)
- **Object** = Instance (actual data)
- Each object has its **own attributes** (state)
- All objects share the **same methods** (behavior)
- Objects are **independent** of each other