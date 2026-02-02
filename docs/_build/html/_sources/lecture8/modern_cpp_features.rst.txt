======================
Modern C++ Features
======================

This lecture integrates contemporary C++ idioms directly into OOP class design. These features help write professional, efficient, and safe code.

Overview
--------

Modern C++ (C++11 and beyond) provides powerful features that improve code quality:

- Type safety
- Performance optimization
- Clear intent
- Compile-time guarantees

Features Covered
----------------

- ``std::string_view`` — Lightweight string references
- ``std::optional`` — Type-safe optional values
- ``[[nodiscard]]`` — Prevent value discards
- ``noexcept`` — Exception specifications

std::string_view
----------------

**Header:** ``<string_view>`` (C++17)

**Definition:** A lightweight, non-owning view into a string. Essentially a pointer + size.

Structure
~~~~~~~~~

.. code-block:: cpp

   // Simplified concept
   class string_view {
   private:
       const char* data_;  // Pointer to string data
       size_t size_;       // Length of view
   };

Characteristics
~~~~~~~~~~~~~~~

- **Non-owning:** Doesn't manage memory
- **Lightweight:** Typically 16 bytes (pointer + size)
- **Read-only:** Provides ``const`` access
- **Efficient:** No copying or allocation
- **View:** Underlying string must remain valid

The Problem
~~~~~~~~~~~

Traditional ``const std::string&`` is less flexible:

.. code-block:: cpp

   void process_name(const std::string& name) { /* ... */ }

   int main() {
       std::string john{"John Smith"};
       const char* jane{"Jane Doe"};
       
       process_name(john);                  // OK
       process_name(jane);                  // ❌ Creates temporary std::string
       process_name("Bob Johnson");         // ❌ Creates temporary std::string
       process_name(john.substr(0, 4));     // ❌ Allocates for "John"
   }

The Solution
~~~~~~~~~~~~

``std::string_view`` accepts any string-like type without conversion:

.. code-block:: cpp

   void process_name(std::string_view name) { /* ... */ }

   int main() {
       std::string john{"John Smith"};
       const char* jane{"Jane Doe"};
       
       process_name(john);                  // ✓ No conversion
       process_name(jane);                  // ✓ No conversion
       process_name("Bob Johnson");         // ✓ No conversion
       
       // Substrings are free (just adjusts pointer and size)
       std::string_view first_name = john.substr(0, 4);  // No allocation!
   }

When to Use
~~~~~~~~~~~

**Use ``std::string_view`` for:**

- Function parameters that only **read** string data
- Accepting any string-like input (``std::string``, ``const char*``, literals)
- Performance-critical code
- Frequent substring operations

**Do NOT use ``std::string_view`` for:**

- Storing as class members (lifetime issues)
- Constructor parameters when storing as ``std::string`` (forces copy anyway)
- When you need ``std::string`` specific methods (e.g., ``+=``)

.. danger::

   **Lifetime Warning:**
   
   .. code-block:: cpp
   
      std::string_view dangerous() {
          std::string temp{"temporary"};
          return temp;  // ❌ DANGER: view to destroyed object!
      }
      
      std::string_view safe() {
          return "permanent";  // ✓ OK: string literal has static storage
      }

Constructor Parameters
~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   **Do NOT use** ``std::string_view`` **for constructor parameters when storing as** ``std::string`` **members:**

   ❌ **Wrong:**
   
   .. code-block:: cpp
   
      class Vehicle {
      private:
          std::string model_;
      public:
          Vehicle(std::string_view model) : model_{model} {}
          // Forces copy anyway, no benefit!
      };

   ✓ **Correct:**
   
   .. code-block:: cpp
   
      class Vehicle {
      private:
          std::string model_;
      public:
          Vehicle(const std::string& model) : model_{model} {}
          // Or use pass-by-value + move for flexibility
      };

Summary
~~~~~~~

- ✓ Use for read-only function parameters
- ✓ More flexible than ``const std::string&``
- ✓ Zero-cost substring views
- ❌ Don't use for storage or constructors
- ❌ Watch out for lifetime issues

std::optional
-------------

**Header:** ``<optional>`` (C++17)

**Definition:** Represents a value that may or may not exist. Provides type-safe way to handle operations that might fail.

The Problem
~~~~~~~~~~~

Traditional approaches are error-prone:

.. code-block:: cpp

   // Magic values
   int find_index(const std::vector<int>& vec, int target) {
       for (size_t i = 0; i < vec.size(); ++i) {
           if (vec[i] == target) return static_cast<int>(i);
       }
       return -1;  // ❌ -1 as "not found" — easy to misuse
   }
   
   // What if -1 is a valid index in other contexts?
   // Caller might forget to check for -1

The Solution
~~~~~~~~~~~~

``std::optional`` makes the absence of a value explicit:

.. code-block:: cpp

   [[nodiscard]] std::optional<int> find_index(
       const std::vector<int>& vec, int target) noexcept {
       for (size_t i{0}; i < vec.size(); ++i) {
           if (vec[i] == target) {
               return static_cast<int>(i);
           }
       }
       return std::nullopt;  // Explicitly "no value"
   }

   int main() {
       std::vector<int> numbers{10, 20, 30, 40};
       
       auto index = find_index(numbers, 30);
       if (index) {  // Check if value exists
           std::cout << "Found at: " << *index << '\n';  // Output: 2
       } else {
           std::cout << "Not found\n";
       }
   }

Creating std::optional
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Empty optional
   std::optional<int> opt1;
   std::optional<int> opt2{std::nullopt};
   
   // With value
   std::optional<int> opt3{42};
   std::optional<int> opt4 = 42;
   
   // Using make_optional
   auto opt5 = std::make_optional(42);
   auto opt6 = std::make_optional<std::string>("Hello");

Checking for Value
~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::optional<int> result = find_index(numbers, 30);
   
   // Method 1: Implicit bool conversion
   if (result) { /* has value */ }
   
   // Method 2: Explicit check
   if (result.has_value()) { /* has value */ }
   
   // Method 3: Compare with nullopt
   if (result != std::nullopt) { /* has value */ }

Accessing Value
~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::optional<int> opt{42};
   
   // Method 1: Dereference (no checking)
   std::cout << *opt << '\n';  // 42
   
   // Method 2: .value() (throws if empty)
   std::cout << opt.value() << '\n';  // 42, throws std::bad_optional_access if empty
   
   // Method 3: .value_or() (provides default)
   std::cout << opt.value_or(-1) << '\n';  // 42 if has value, -1 if empty

.. important::

   ``std::optional`` is **not a pointer**. The ``*`` operator is overloaded to provide pointer-like syntax for convenience.

value() vs. Dereference
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::optional<int> empty;
   
   // Using * (undefined behavior if empty)
   int x = *empty;  // ❌ Undefined behavior!
   
   // Using .value() (throws exception if empty)
   try {
       int y = empty.value();  // ✓ Throws std::bad_optional_access
   } catch (const std::bad_optional_access& e) {
       std::cout << "Empty optional!\n";
   }

value_or() for Defaults
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::optional<int> config_port = read_config("server_port");
   int port = config_port.value_or(8080);  // Use 8080 if not configured
   
   std::optional<std::string> username = get_user_input();
   std::string name = username.value_or("Guest");  // Default to "Guest"

.. danger::

   **Always check before accessing:**
   
   .. code-block:: cpp
   
      std::optional<int> x{std::nullopt};
      
      // ❌ Unsafe
      std::cout << x.value() << '\n';  // Throws!
      
      // ✓ Safe
      if (x) {
          std::cout << *x << '\n';
      }
      
      // ✓ Safe with default
      std::cout << x.value_or(-1) << '\n';

When to Use
~~~~~~~~~~~

Use ``std::optional`` for:

- Functions that might fail (parsing, searching)
- Configuration values that are truly optional
- Database queries (may return no results)
- Operations with no valid sentinel value

**Benefits:**

- Type-safe (compiler forces handling)
- Expressive (code shows intent)
- No magic values
- Exception safety via ``value_or()``

[[nodiscard]]
-------------

**Attribute:** ``[[nodiscard]]`` (C++17)

**Purpose:** Warns if function return value is discarded, preventing accidental programming errors.

The Problem
~~~~~~~~~~~

.. code-block:: cpp

   bool is_running() const { return is_running_; }
   
   int main() {
       Vehicle car;
       car.is_running();  // ❌ Result ignored! Probably a bug
       
       // Intended:
       if (car.is_running()) { /* ... */ }
   }

The Solution
~~~~~~~~~~~~

.. code-block:: cpp

   [[nodiscard]] bool is_running() const noexcept {
       return is_running_;
   }
   
   int main() {
       Vehicle car;
       car.is_running();  // ⚠️ Compiler warning: unused return value
   }

When to Use
~~~~~~~~~~~

Use ``[[nodiscard]]`` on functions where ignoring the return value is almost certainly a bug:

- Accessors (getters)