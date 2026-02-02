===========
Abstraction
===========

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-mg
    
    **Definition:** Abstraction exposes a *stable interface* and hides *implementation details*. Users depend on *what* the type does (the contract), not *how* it does it (the implementation).

----

Key Benefits
------------

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Simplicity
        :class-card: sd-border-primary
        
        Small public surface with clear semantics

    .. grid-item-card:: Modularity
        :class-card: sd-border-primary
        
        Independent evolution of internals without breaking clients

    .. grid-item-card:: Maintainability
        :class-card: sd-border-primary
        
        Fewer ripple effects across codebase

    .. grid-item-card:: Testability
        :class-card: sd-border-primary
        
        Mock the interface, validate behavior independently

    .. grid-item-card:: Flexibility
        :class-card: sd-border-primary
        
        Swap implementations without changing client code

----

When to Use Abstract Classes
-----------------------------

Create abstract classes when you want to:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Define a Contract
        :class-card: sd-border-info
        
        Multiple concrete types must follow the same interface

    .. grid-item-card:: Enable Polymorphism
        :class-card: sd-border-info

        
        Different implementations with common behavior

    .. grid-item-card:: Prevent Direct Instantiation
        :class-card: sd-border-info
        
        Incomplete or conceptual types shouldn't be created

    .. grid-item-card:: Share Common Behavior
        :class-card: sd-border-info

        
        Provide base functionality while requiring specialization

    .. grid-item-card:: Design Plugin Architectures
        :class-card: sd-border-info

        
        Clients provide their own implementations

    .. grid-item-card:: Create Frameworks
        :class-card: sd-border-info

        
        Define extension points for users

Example Scenarios
~~~~~~~~~~~~~~~~~

.. tab-set::

    .. tab-item:: Device Drivers

        .. code-block:: cpp
        
           class Device {
           public:
               virtual ~Device() = default;
               virtual void initialize() = 0;
               virtual void read(Buffer& buf) = 0;
               virtual void write(const Buffer& buf) = 0;
           };

    .. tab-item:: Geometric Shapes

        .. code-block:: cpp
        
           class Shape {
           public:
               virtual ~Shape() = default;
               virtual double area() const = 0;
               virtual double perimeter() const = 0;
               virtual void draw() const = 0;
           };

    .. tab-item:: Data Sources

        .. code-block:: cpp
        
           class DataSource {
           public:
               virtual ~DataSource() = default;
               virtual bool open() = 0;
               virtual Data read() = 0;
               virtual bool write(const Data& d) = 0;
               virtual void close() = 0;
           };

    .. tab-item:: UI Widgets

        .. code-block:: cpp
        
           class Widget {
           public:
               virtual ~Widget() = default;
               virtual void render() = 0;
               virtual void handle_event(const Event& e) = 0;
               virtual void resize(int w, int h) = 0;
           };

----

How is Abstraction Implemented in C++?
---------------------------------------

.. grid:: 3
    :gutter: 3

    .. grid-item-card:: Abstract Classes
        :class-card: sd-border-primary
        
        Define behavior as a contract using pure ``virtual`` methods

    .. grid-item-card:: Pure Virtual Methods
        :class-card: sd-border-primary
        
        Enforce implementation in derived types (``= 0``)

    .. grid-item-card:: Encapsulation
        :class-card: sd-border-primary
        
        Keep data private/protected; expose intent through methods

**Example:**

.. code-block:: cpp
   :caption: Abstract Vehicle Class
   :emphasize-lines: 6,9

   class Vehicle {
   public:
       virtual ~Vehicle() = default;
       
       // Pure virtual - MUST be implemented in derived classes
       virtual void drive() = 0;
       
       // Pure virtual - MUST be implemented in derived classes
       virtual void update_location(const Location& location) = 0;
   };

----

Pure ``virtual`` Methods (``= 0``)
-----------------------------------

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-mg
    
    **Definition:** A **pure** ``virtual`` **method** is declared with ``= 0`` and:
    
    • **Makes the class abstract** — cannot be instantiated
    
    • **Requires derived classes to implement** the method
    
    • **Defines a contract** that concrete classes must fulfill
    
    • Can optionally provide a default implementation (rare)

Basic Example
~~~~~~~~~~~~~

.. code-block:: cpp
   :caption: Pure Virtual Method Declaration
   :emphasize-lines: 4

   class Vehicle {
   public:
       virtual ~Vehicle() = default;
       virtual void drive() = 0;  // Pure virtual method
   };

.. code-block:: cpp
   
    int main(){
        // transportation::Vehicle v;  // ERROR: cannot instantiate abstract class
    }


.. code-block:: cpp
   :caption: Mandatory base class method overriding
   :emphasize-lines: 3

   class RoboTaxi : public Vehicle {
   public:
       void drive() override;
       
       /* robo_taxi.cpp
       { 
         // logic
       }
       */
   };

.. code-block:: cpp

    int main(){
        RoboTaxi rt;  // OK - RoboTaxi has overridden drive()
    }

.. note::

   A caller invokes ``vehicle->drive()`` without knowledge of internal details. Any conforming concrete type satisfies the same contract.

Abstract Class Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-warning
    
    A class is **abstract** if it has at least one pure ``virtual`` method. An abstract class:
    
    ✓ **Cannot be instantiated** directly
    
    ✓ **Can have constructors** (for derived classes to call)
    
    ✓ **Can have data members** (typically ``protected``)
    
    ✓ **Can mix pure and regular virtual methods**
    
    ✓ **Can have non-virtual methods**

.. code-block:: cpp
   :caption: Abstract Class with Mixed Members
   :emphasize-lines: 10-11,14,21

   class Shape {
   protected:
       Point center_;  // Data member
       
   public:
       // Constructor (for derived classes)
       Shape(const Point& center) : center_{center} {}
       
       // Pure virtual - must override
       virtual double area() const = 0;
       virtual void draw() const = 0;
       
       // Regular virtual - can override
       virtual void move(const Vector& offset);
       /* shape.cpp
       {
           center_ = center_ + offset;
       }*/
       
       // Non-virtual - cannot override
       [[nodiscard]] Point get_center() const noexcept{ return center_; }
       
       // Virtual destructor
       virtual ~Shape() = default;
   };

Pure Virtual with Default Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. dropdown:: 💡 Advanced Pattern: Pure Virtual with Implementation
    :class-container: sd-border-info

    A pure ``virtual`` method can optionally provide a default implementation that derived classes can call explicitly:

    .. code-block:: cpp
       :emphasize-lines: 5-8

       class Logger {
       public:
           virtual ~Logger() = default;
           
           // Pure virtual with implementation
           virtual void log(const std::string& message) = 0 {
               // Default implementation
               std::cout << "[LOG] " << message << '\n';
           }
       };

       class FileLogger : public Logger {
       public:
           void log(const std::string& message) override; 
           /* file_logger.cpp
           {
               // Can call base implementation
               Logger::log(message);
               // Add file-specific behavior
               write_to_file(message);
           }*/
       };

    .. note::

       This pattern is rare but useful when you want to enforce implementation while providing a fallback.

----

Concrete Classes
----------------

.. card::
    :class-card: sd-border-secondary sd-border-5 sd-shadow-mg
    
    **Definition:** A concrete class is a class that can be instantiated. It provides complete implementations for all inherited pure ``virtual`` methods.

Key Characteristics
~~~~~~~~~~~~~~~~~~~

.. grid:: 2 2 4 4
    :gutter: 2

    .. grid-item-card:: Fully Defined
        :class-card: sd-border-primary sd-border-2

        
        Implements all inherited pure ``virtual`` methods

    .. grid-item-card:: Instantiable
        :class-card: sd-border-primary sd-border-2

        
        Can create objects directly

    .. grid-item-card:: Observable
        :class-card: sd-border-primary sd-border-2

        
        Provides complete, working functionality

    .. grid-item-card:: Safe to Use
        :class-card: sd-border-primary sd-border-2

        
        All methods have defined behavior

Example: Complete Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

    .. tab-item:: ✅ Correct Implementation

        .. code-block:: cpp
           :caption: Fully Concrete Class

           // Abstract base - defines interface contract
           class Vehicle {
           public:
               virtual ~Vehicle() = default;
               virtual void drive() = 0;
               virtual void stop() = 0;
           };

           // Concrete derived class - implements all pure virtuals
           class RoboTaxi : public Vehicle {
           public:
               ~RoboTaxi() override = default;
               
               void drive() override;
               /* robo_taxi.cpp
               { 
                   // RoboTaxi-specific driving logic  
               }*/
               
               void stop() override;
               /* robo_taxi.cpp
               { 
                   // RoboTaxi-specific stopping logic
               }*/
           };

        .. code-block:: cpp

            int main(){
                RoboTaxi robo_taxi{"ROBOT001", 6};  // OK - fully concrete
                robo_taxi.drive();  // OK
           }
           

    .. tab-item:: ❌ Incomplete Implementation

        .. code-block:: cpp
           :caption: Still Abstract - Missing Implementation

           // Abstract base
           class Vehicle {
           public:
               virtual ~Vehicle() = default;
               virtual void drive() = 0;
               virtual void stop() = 0;
           };

           // Still abstract - missing stop() implementation
           class Taxi : public Vehicle {
           public:
               ~Taxi() override = default;
               void drive() override; 
               /* taxi.cpp
               { 
                // Taxi-specific driving logic 
               }*/

               // Missing: void stop() override { }
           };

        .. code-block:: cpp

            int main(){
                // ERROR: cannot instantiate abstract class
                // Taxi taxi{"TAXI001", 6};
           }

        .. warning::

           A derived class must implement **ALL** pure ``virtual`` methods from the base class to become concrete. We forgot to implement ``stop()`` and therefore, ``Taxi`` is still an abstract class.

----

Design Patterns with Abstraction
---------------------------------

.. tab-set::

    .. tab-item:: 📋 Strategy Pattern

        .. code-block:: cpp
           :caption: Interchangeable Algorithms

           // Abstract strategy interface
           class SortStrategy {
           public:
               virtual ~SortStrategy() = default;
               virtual void sort(std::vector<int>& data) = 0;
           };

           // Concrete strategies
           class QuickSort : public SortStrategy {
           public:
               void sort(std::vector<int>& data) override;
               /* quick_sort.cpp
               {
                   // QuickSort implementation
               }*/
           };

           class MergeSort : public SortStrategy {
           public:
               void sort(std::vector<int>& data) override;
               /* merge_sort.cpp
               {
                   // MergeSort implementation
               }*/
           };

           // Client uses abstraction
           class DataProcessor {
           private:
               std::unique_ptr<SortStrategy> strategy_;
           public:
               void set_strategy(std::unique_ptr<SortStrategy> strategy) {
                   strategy_ = std::move(strategy);
               }
               
               void process(std::vector<int>& data);
               /* data_processor.cpp 
               {
                   strategy_->sort(data);  // Uses abstract interface
               }*/
           };

    .. tab-item:: 🏭 Factory Pattern

        .. code-block:: cpp
           :caption: Object Creation Abstraction

           // Abstract product
           class Document {
           public:
               virtual ~Document() = default;
               virtual void open() = 0;
               virtual void save() = 0;
           };

           // Concrete products
           class PDFDocument : public Document {
           public:
               void open() override;
               /* pdf_document.cpp
               { 
                 // PDF opening logic  
               */}

               void save() override;
               /* pdf_document.cpp
               { 
                 // PDF saving logic 
               }*/
           };

           class WordDocument : public Document {
           public:
               void open() override;
               /* word_document.cpp
               { 
                 // Word opening logic 
               }*/

               void save() override;
               /*  word_document.cpp
               { 
                 // Word saving logic 
               }*/
           };

           // Factory creates objects polymorphically
           class DocumentFactory {
           public:
               static std::unique_ptr<Document> create(const std::string& type) {
                   if (type == "pdf") {
                       return std::make_unique<PDFDocument>();
                   } else if (type == "word") {
                       return std::make_unique<WordDocument>();
                   }
                   return nullptr;
               }
           };

    .. tab-item:: 👁️ Observer Pattern

        .. code-block:: cpp
           :caption: Event Notification System

           // Abstract observer interface
           class Observer {
           public:
               virtual ~Observer() = default;
               virtual void update(const std::string& event) = 0;
           };

           // Concrete observers
           class EmailNotifier : public Observer {
           public:
               void update(const std::string& event) override;
               /*  email_notifier.cpp
               { 
                 send_email("Event occurred: " + event);
               }*/
           };

           class LoggerObserver : public Observer {
           public:
               void update(const std::string& event) override;
               /*  logger_observer.cpp
               { 
                 // log_to_file("Event occurred: " + event);
               }*/
           };

           // Subject maintains list of observers
           class EventManager {
           private:
               std::vector<Observer*> observers_;
           public:
               void attach(Observer* obs);
               /*  event_manager.cpp
               { 
                 observers_.push_back(obs);
               }*/
               
               
               void notify(const std::string& event);
               /*  event_manager.cpp
               { 
                 for (auto* obs : observers_) {
                       obs->update(event);  // Polymorphic call
                   }
               }*/
           };

----

Best Practices
--------------

.. grid:: 1 1 2 3
    :gutter: 3

    .. grid-item-card:: 1. Minimal Interfaces
        :class-card: sd-border-success sd-border-2
        
        Keep interfaces minimal and focused
        
        .. dropdown:: Show Example
        
            .. code-block:: cpp
            
               // Good - focused interface
               class Drawable {
               public:
                   virtual ~Drawable() = default;
                   virtual void draw() const = 0;
               };
               
               // Avoid - interface too broad
               class GraphicsObject {
               public:
                   virtual void draw() const = 0;
                   virtual void rotate(double angle) = 0;
                   virtual void scale(double factor) = 0;
                   virtual void translate(const Vector& offset) = 0;
                   virtual void set_color(const Color& color) = 0;
                   // Too many responsibilities!
               };

    .. grid-item-card:: 2. Contracts, Not Implementation
        :class-card: sd-border-success sd-border-2
        
        Use abstract classes for contracts, not implementation sharing
        
        - If you need shared implementation, consider composition
        - Abstract classes define "what", not "how"

    .. grid-item-card:: 3. Prefer Pure Virtual
        :class-card: sd-border-success sd-border-2
        
        Prefer pure virtual over virtual with defaults
        
        - Forces derived classes to think about implementation
        - Avoids silent bugs from forgotten overrides

    .. grid-item-card:: 4. Virtual Destructors
        :class-card: sd-border-success sd-border-2
        
        Always make destructors virtual
        
        .. dropdown:: Show Example
        
            .. code-block:: cpp
            
               class AbstractBase {
               public:
                   virtual ~AbstractBase() = default;  // Essential!
                   virtual void do_something() = 0;
               };

    .. grid-item-card:: 5. Interface Segregation
        :class-card: sd-border-success sd-border-2
        
        Many small interfaces beat one large interface (ISP)
        
        - Clients shouldn't depend on methods they don't use

    .. grid-item-card:: 6. Document Contracts
        :class-card: sd-border-success sd-border-2
        
        Document the contract clearly
        
        .. dropdown:: Show Example
        
            .. code-block:: cpp
            
               class DataSource {
               public:
                   virtual ~DataSource() = default;
                   
                   /**
                    * Reads data from the source.
                    * 
                    * @return Data buffer, or empty on error
                    * @throws std::runtime_error if source is not open
                    */
                   virtual std::vector<uint8_t> read() = 0;
               };

----

Common Pitfalls
---------------

.. dropdown:: ❌ Pitfall 1: Too Many Pure Virtuals
    :class-container: sd-border-danger
    :open:

    .. code-block:: cpp

       // Avoid - forces too much implementation
       class Vehicle {
       public:
           virtual void start_engine() = 0;
           virtual void stop_engine() = 0;
           virtual void open_door() = 0;
           virtual void close_door() = 0;
           virtual void honk_horn() = 0;
           virtual void turn_lights_on() = 0;
           virtual void turn_lights_off() = 0;
           // ... 50 more methods
       };

    **Fix:** Break into smaller, focused interfaces (Interface Segregation Principle).

.. dropdown:: ❌ Pitfall 2: Abstract Class with Data Members
    :class-container: sd-border-danger

    .. code-block:: cpp

       // Questionable - mixes interface and implementation
       class Shape {
       private:
           Color color_;  // Implementation detail in abstract class?
       public:
           virtual double area() const = 0;
       };

    **Better:** Keep abstract classes focused on interface, use composition for shared data.

.. dropdown:: ❌ Pitfall 3: Forgetting Virtual Destructor
    :class-container: sd-border-danger

    .. code-block:: cpp

       class Base {
       public:
           // Missing: virtual ~Base() = default;
           virtual void foo() = 0;
       };

    **Always** add virtual destructor to abstract base classes to prevent resource leaks.

----

Key Takeaways
=============

.. card::
    :class-card: sd-border-primary sd-border-3 sd-shadow-lg
    
    **Core Concepts:**
    
    • **Abstraction** exposes interface, hides implementation
    
    • **Abstract classes** define contracts using pure ``virtual`` methods
    
    • **Pure virtual methods** (``= 0``) must be implemented by derived classes
    
    • **Concrete classes** implement all inherited pure virtuals
    
    • Always provide **virtual destructors** in abstract base classes
    
    • Keep interfaces **minimal and focused**
    
    • Use abstraction for **polymorphic behavior** and **dependency inversion**
    
    • Abstract classes **cannot be instantiated** directly
    
    • Derived classes remain abstract until **all** pure virtuals are implemented

.. grid:: 1 2 2 3
    :gutter: 3
    :class-container: sd-text-center

    .. grid-item-card:: Contract
        :class-card: sd-border-primary
        
        Define what, not how

    .. grid-item-card:: Polymorphism
        :class-card: sd-border-primary
        
        Enable flexible designs

    .. grid-item-card:: Encapsulation
        :class-card: sd-border-primary
        
        Hide implementation details