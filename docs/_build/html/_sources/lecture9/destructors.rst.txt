===========
Destructors
===========

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-md
    
    **Definition:** A destructor is a special member function that cleans up an object's resources when it goes out of scope or is explicitly deleted. The destructor is automatically called: you don't invoke it manually.

----

Key Characteristics
-------------------

.. grid:: 2 2 4 4
    :gutter: 3

    .. grid-item-card:: Naming
        :class-card: sd-border-info
        
        ``~ClassName()``
        
        (e.g., ``~Vehicle()``)

    .. grid-item-card:: Signature
        :class-card: sd-border-info
        
        No parameters, no return type
        
        Unlike constructors

    .. grid-item-card:: One Per Class
        :class-card: sd-border-info
        
        Cannot be overloaded
        
        Only one destructor

    .. grid-item-card:: Automatic
        :class-card: sd-border-info
        
        Called at scope exit
        
        or ``delete``

----

What Does a Destructor Do?
---------------------------

A destructor performs **cleanup operations** before an object is destroyed:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Memory Management
        :class-card: sd-border-info
        
        Release dynamically allocated memory
        
        ``delete``, ``delete[]``

    .. grid-item-card:: Close Resources
        :class-card: sd-border-info
        
        Close file handles, network connections, database connections

    .. grid-item-card:: Release Locks
        :class-card: sd-border-info
        
        Release mutexes or other synchronization primitives

    .. grid-item-card:: Reference Counting
        :class-card: sd-border-info
        
        Decrement reference counts in shared ownership schemes

**Example: RAII Pattern**

.. code-block:: cpp
   :caption: Automatic Resource Management
   :emphasize-lines: 7-11

   class FileHandler {
   private:
       FILE* file_;
   public:
       FileHandler(const char* filename) : file_(fopen(filename, "r")) {}
       
       ~FileHandler() {  // Destructor ensures file is closed
           if (file_) {
               fclose(file_);
           }
       }
   };
   // file_ is automatically closed when FileHandler goes out of scope

----

Destructor Execution Order
---------------------------

.. card::
    :class-card: sd-border-warning sd-border-2
    
    ⚠️ **Critical Concept**
    
    Destructors are called in the **reverse order** of constructor calls

.. tab-set::

    .. tab-item:: Example Code

        .. code-block:: cpp
           :caption: Inheritance Destruction Order

           class Base {
           public:
               Base() { std::cout << "Base constructor\n"; }
               ~Base() { std::cout << "Base destructor\n"; }
           };

           class Derived : public Base {
           public:
               Derived() { std::cout << "Derived constructor\n"; }
               ~Derived() { std::cout << "Derived destructor\n"; }
           };

           int main() {
               Derived d;
           }

    .. tab-item:: Output & Explanation

        **Output:**
        
        .. code-block:: text
        
           Base constructor
           Derived constructor
           Derived destructor    ← Reversed order
           Base destructor       ← Reversed order
        
        **Why This Matters:**
        
        1. Derived class resources are cleaned up first
        2. Base class resources are cleaned up last
        3. No dangling references during destruction

----

``virtual`` Destructors and Inheritance
----------------------------------------

.. card::
    :class-card: sd-border-warning sd-border-4
    
    ⚠️ **CRITICAL WARNING**
    
    When deleting through a base pointer, a ``virtual`` destructor ensures the derived class destructor runs first. Without it, only the base destructor runs, causing **resource leaks** and **undefined behavior**.

The Problem
~~~~~~~~~~~

.. dropdown:: ❌ Non-Virtual Destructor Bug
    :class-container: sd-border-danger
    :open:

    .. code-block:: cpp
       :caption: Memory Leak with Non-Virtual Destructor
       :emphasize-lines: 3

       class Base {
       public:
           ~Base() { std::cout << "~Base()\n"; }  // NOT virtual!
       };

       class Derived : public Base {
       private:
           int* data_;
       public:
           Derived() : data_(new int[1000]) {}
           
           ~Derived() { 
               delete[] data_; 
               std::cout << "~Derived()\n"; 
           }
       };

       Base* ptr = new Derived();
       delete ptr;  // UNDEFINED BEHAVIOR!
                    // Only ~Base() called, not ~Derived()
                    // Leaks memory from data_!

    .. warning::

       Without ``virtual``, the destructor is selected at compile time based on the pointer type (``Base*``), not the actual object type (``Derived``). The derived destructor never runs!

The Solution
~~~~~~~~~~~~

.. dropdown:: ✅ Virtual Destructor Solution
    :class-container: sd-border-success
    :open:

    .. code-block:: cpp
       :caption: Correct Behavior with Virtual Destructor
       :emphasize-lines: 3,13

       class Base {
       public:
           virtual ~Base() { std::cout << "~Base()\n"; }  // Virtual!
       };

       class Derived : public Base {
       private:
           int* data_;
       public:
           Derived() : data_(new int[1000]) {}
           
           ~Derived() override { 
               delete[] data_; 
               std::cout << "~Derived()\n"; 
           }
       };

       Base* ptr = new Derived();
       delete ptr;  // Correct behavior
                    // Calls ~Derived() first, then ~Base()
                    // No memory leak!

       // Output:
       // ~Derived()
       // ~Base()

    .. important::

       **Golden Rule:** Any class intended to be a polymorphic base class **must** have a virtual destructor.

When to Use Virtual Destructors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 2
    :gutter: 3

    .. grid-item-card:: ✅ Always Use Virtual Destructors
        :class-card: sd-border-success sd-border-2
        
        **When:**
        
        - The class has any virtual methods
        - The class is designed to be inherited from
        - Objects may be deleted through base class pointers
        - The class is part of a polymorphic hierarchy

    .. grid-item-card:: 🚫 Don't Need Virtual Destructors
        :class-card: sd-border-warning sd-border-2
        
        **When:**
        
        - The class is ``final`` (cannot be inherited)
        - The class is never used polymorphically
        - No derived instances deleted through base pointers

----

The ``= default`` Keyword
--------------------------

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-md
    
    **Definition:** The ``= default`` keyword requests the compiler generate the default implementation of a special member function (constructor, destructor, copy/move operations).

Why Use It?
~~~~~~~~~~~

.. grid:: 2 2 4 4
    :gutter: 2

    .. grid-item-card:: Explicit Intent
        :class-card: sd-border-info
        
        Shows you deliberately want default behavior

    .. grid-item-card:: Optimization
        :class-card: sd-border-info
        
        Compiler-generated code is often optimal

    .. grid-item-card:: Rule of Zero
        :class-card: sd-border-info
        
        Don't write what compiler can generate

    .. grid-item-card:: Special Rules
        :class-card: sd-border-info
        
        Enables trivial/constexpr functions

**Example:**

.. code-block:: cpp
   :caption: Using = default
   :emphasize-lines: 3-5

   class Vehicle {
   public:
       virtual ~Vehicle() = default;         // Compiler generates virtual destructor body
       Vehicle() = default;                  // Compiler generates default constructor
       Vehicle(const Vehicle&) = default;    // Compiler generates copy constructor
   };

.. note::

   ``= default`` is particularly important for ``virtual`` destructors in abstract base classes where you don't need custom cleanup logic but must ensure the destructor is ``virtual``.

When to Use ``= default``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

    .. tab-item:: Use = default

        **Use** ``= default`` **for destructors when:**
        
        - You need a virtual destructor but have no cleanup logic
        - You are following the Rule of Zero
        - You want to explicitly document default behavior
        
        .. code-block:: cpp
        
           class Shape {
           public:
               virtual ~Shape() = default;
               virtual void draw() = 0;
           };

    .. tab-item:: Write Custom Destructor

        **Write a custom destructor when:**
        
        - You need to release manually managed resources
        - You need to close file handles or network connections
        - You need to perform logging or side effects
        - You are managing RAII wrappers
        
        .. code-block:: cpp
        
           class Connection {
           private:
               int socket_fd_;
           public:
               ~Connection() {
                   close(socket_fd_);  // Custom cleanup
               }
           };

----

Common Patterns
---------------

.. tab-set::

    .. tab-item:: Pattern 1: Abstract Base

        .. code-block:: cpp
           :caption: Abstract Base with Virtual Destructor

           class Shape {
           public:
               virtual ~Shape() = default;           // Virtual destructor
               virtual double area() const = 0;      // Pure virtual
               virtual void draw() const = 0;        // Pure virtual
           };

           class Circle : public Shape {
           private:
               double radius_;
           public:
               ~Circle() override = default;         // No cleanup needed
               double area() const override { 
                   return 3.14159 * radius_ * radius_; 
               }
               void draw() const override { /* drawing code */ }
           };

    .. tab-item:: Pattern 2: RAII Class

        .. code-block:: cpp
           :caption: RAII Class with Custom Destructor

           class DatabaseConnection {
           private:
               void* connection_;  // Opaque handle
           public:
               DatabaseConnection(const char* host) {
                   connection_ = connect_to_database(host);
               }
               
               ~DatabaseConnection() {
                   if (connection_) {
                       close_connection(connection_);
                       connection_ = nullptr;
                   }
               }
               
               // Delete copy operations (connection is unique)
               DatabaseConnection(const DatabaseConnection&) = delete;
               DatabaseConnection& operator=(const DatabaseConnection&) = delete;
           };

    .. tab-item:: Pattern 3: Smart Pointers

        .. code-block:: cpp
           :caption: Inheritance with Resource Management

           class Vehicle {
           public:
               virtual ~Vehicle() = default;  // Virtual for polymorphism
               virtual void drive() = 0;
           };

           class RoboTaxi : public Vehicle {
           private:
               std::unique_ptr<SensorArray> sensors_;  // RAII wrapper
               std::unique_ptr<NavigationSystem> nav_; // RAII wrapper
           public:
               // Compiler-generated destructor automatically cleans up unique_ptrs
               ~RoboTaxi() override = default;
               
               void drive() override { /* ... */ }
           };

----

Common Pitfalls
---------------

.. dropdown:: ❌ Pitfall 1: Forgetting Virtual Destructor
    :class-container: sd-border-danger
    :open:

    .. code-block:: cpp

       class Base {
       public:
           virtual void foo() = 0;
           // Missing: virtual ~Base() = default;
       };

       std::unique_ptr<Base> ptr = std::make_unique<Derived>();
       // When ptr goes out of scope: UNDEFINED BEHAVIOR!

    **Fix:** Always add virtual destructor to polymorphic bases.

.. dropdown:: ❌ Pitfall 2: Calling Virtual Functions in Destructors
    :class-container: sd-border-danger

    .. code-block:: cpp

       class Base {
       public:
           virtual ~Base() {
               cleanup();  // Does NOT use derived version!
           }
           virtual void cleanup() { /* base cleanup */ }
       };

       class Derived : public Base {
       public:
           ~Derived() override { /* ... */ }
           void cleanup() override { /* derived cleanup */ }
       };

    .. warning::

       Virtual dispatch does NOT work in constructors or destructors. Only the current class's version is called.

.. dropdown:: ❌ Pitfall 3: Exception Safety
    :class-container: sd-border-danger

    .. code-block:: cpp

       class Resource {
       public:
           ~Resource() {
               // Never throw from destructors!
               // If this throws, std::terminate is called
               cleanup();  
           }
       };

    .. important::

       Destructors should be ``noexcept`` (they are by default). Never let exceptions escape from destructors.

----

Best Practices
--------------

.. grid:: 1 1 2 3
    :gutter: 3

    .. grid-item-card:: 1. Virtual in Base Classes
        :class-card: sd-border-success sd-border-2
        
        Always make base class destructors virtual
        
        .. dropdown:: Show Example
        
            .. code-block:: cpp
            
               class Base {
               public:
                   virtual ~Base() = default;
               };

    .. grid-item-card:: 2. Use = default
        :class-card: sd-border-success sd-border-2
        
        Use ``= default`` when no custom cleanup needed
        
        .. dropdown:: Show Example
        
            .. code-block:: cpp
            
               class Widget {
               public:
                   virtual ~Widget() = default;
               };

    .. grid-item-card:: 3. Rule of Zero
        :class-card: sd-border-success sd-border-2
        
        Let compiler generate destructors when possible
        
        - Use RAII wrappers
        - ``unique_ptr``, ``shared_ptr``
        - Only write custom when managing raw resources

    .. grid-item-card:: 4. Use override
        :class-card: sd-border-success sd-border-2
        
        Mark overridden destructors with ``override``
        
        .. dropdown:: Show Example
        
            .. code-block:: cpp
            
               class Derived : public Base {
               public:
                   ~Derived() override = default;
               };

    .. grid-item-card:: 5. Never Throw
        :class-card: sd-border-success sd-border-2
        
        Never throw from destructors
        
        - Implicitly ``noexcept``
        - Throwing calls ``std::terminate``

    .. grid-item-card:: 6. Reverse Order
        :class-card: sd-border-success sd-border-2
        
        Clean up in reverse order of construction
        
        - Compiler does automatically
        - Ensures no dangling references

----

Key Takeaways
=============

.. card::
    :class-card: sd-border-primary sd-border-3 sd-shadow-lg
    
    **Core Concepts:**
    
    • Destructors clean up resources automatically when objects are destroyed
    
    • Use ``virtual`` destructors in polymorphic base classes
    
    • Use ``= default`` for virtual destructors when no cleanup is needed
    
    • Never throw exceptions from destructors
    
    • Follow the Rule of Zero: prefer RAII wrappers over manual management
    
    • Always use ``override`` when overriding virtual destructors
    
    • Virtual dispatch doesn't work in constructors/destructors
    
    • Destructors execute in reverse order of construction

.. grid:: 1 2 2 4
    :gutter: 3
    :class-container: sd-text-center

    .. grid-item-card:: Automatic
        :class-card: sd-border-info
        
        Called automatically

    .. grid-item-card:: Reverse Order
        :class-card: sd-border-info
        
        Opposite of construction

    .. grid-item-card:: Virtual Required
        :class-card: sd-border-info
        
        For polymorphic bases

    .. grid-item-card:: RAII Pattern
        :class-card: sd-border-info
        
        Resource management