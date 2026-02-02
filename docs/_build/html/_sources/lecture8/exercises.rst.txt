Exercises
=========

1. Basic Class Implementation with Encapsulation
-------------------------------------------------

Create a complete ``BankAccount`` class demonstrating proper encapsulation and member initialization.

**Requirements:**

- Define a class ``BankAccount`` in the ``banking`` namespace with private attributes:
  
  - ``account_number_`` (``std::string``)
  - ``balance_`` (``double``)
  - ``is_active_`` (``bool``, default ``true``)

- Implement:
  
  - Default constructor: account number "UNKNOWN", balance 0.0
  - Parameterized constructor: takes account number and initial balance
  - Use **member initializer lists** for both constructors

- Provide accessors (all ``const noexcept`` with ``[[nodiscard]]``):
  
  - ``get_account_number()`` returns ``const std::string&``
  - ``get_balance()`` returns ``double``
  - ``is_active()`` returns ``bool``

- Provide mutators:
  
  - ``deposit(double amount)`` — validate ``amount > 0``, throw ``std::invalid_argument`` if not
  - ``withdraw(double amount)`` — validate sufficient balance and ``amount > 0``
  - ``deactivate()`` — sets ``is_active_`` to ``false`` (``noexcept``)

**Tasks:**

- Create a project with ``include/bank_account.hpp`` and ``src/bank_account.cpp``
- Write ``main.cpp`` demonstrating all operations
- Add Doxygen comments to all public members
- Compile with ``-Wall -Wextra -pedantic-errors -Werror``
- **Verify:** Attempting to access private members directly fails to compile


2. Using ``std::optional`` for Safe Search Operations
------------------------------------------------------

Implement search functions that return ``std::optional`` instead of magic values.

**Requirements:**

- Implement ``std::optional<size_t> find_first_vowel(std::string_view text)`` that:
  
  - Returns the index of the first vowel (a, e, i, o, u, case-insensitive)
  - Returns ``std::nullopt`` if no vowel found
  - Mark as ``[[nodiscard]] noexcept``

- Implement ``std::optional<int> parse_int(std::string_view str)`` that:
  
  - Safely converts a string to ``int``
  - Returns ``std::nullopt`` for invalid input (non-numeric, overflow)
  - Use ``std::stoi`` in a try-catch block

- Implement ``std::optional<double> safe_divide(double numerator, double denominator)`` that:
  
  - Returns ``std::nullopt`` if ``denominator == 0.0``
  - Otherwise returns the result
  - Mark as ``[[nodiscard]] noexcept``

**Tasks:**

- Create test cases demonstrating all three functions
- Show three different ways to check for values (``if (opt)``, ``has_value()``, ``!= nullopt``)
- Demonstrate all three access methods (``*opt``, ``value()``, ``value_or()``)
- Write a function that chains optionals: parse a string to int, then divide by another parsed int


3. Constructor Best Practices: Avoiding Two-Step Initialization
----------------------------------------------------------------

Refactor poorly written classes to use member initializer lists correctly.

**Given this inefficient code:**

.. code-block:: cpp

   class Engine {
   private:
       int horsepower_;
       std::string fuel_type_;
       std::vector<std::string> components_;
       
   public:
       Engine() {
           horsepower_ = 0;
           fuel_type_ = "Unknown";
           components_ = {"Pistons", "Crankshaft", "Valves"};
       }
       
       Engine(int hp, std::string fuel) {
           horsepower_ = hp;
           fuel_type_ = fuel;
           components_ = {"Pistons", "Crankshaft", "Valves"};
       }
   };

**Tasks:**

- Rewrite both constructors using member initializer lists
- Add a third constructor taking ``hp``, ``fuel``, and ``components`` vector
- Measure performance difference (create 100,000 objects in a loop, time both versions)
- Explain why the original version is inefficient (hint: count constructor calls for ``std::vector``)
- Add ``const std::string serial_number_`` member and show why it **requires** initializer list
- Bonus: Add a reference member ``const Engine& base_model_`` and initialize it properly


4. ``std::string_view`` vs. ``const std::string&`` Performance
---------------------------------------------------------------

Compare the performance and flexibility of different string parameter types.

**Requirements:**

- Implement three versions of ``count_spaces``:

  .. code-block:: cpp
  
     // Version 1
     size_t count_spaces_ref(const std::string& text);
     
     // Version 2  
     size_t count_spaces_view(std::string_view text);
     
     // Version 3 (substring version)
     size_t count_spaces_substr(std::string_view text, size_t start, size_t length);

**Tasks:**

- Test all versions with:
  
  - ``std::string`` objects
  - String literals
  - ``const char*`` pointers
  - Substrings (using ``substr()`` for Version 1, ``substr()`` for Version 2)

- Time each version processing a large file (1 MB text, 1000 iterations)
- Show that Version 2 accepts all inputs without conversion overhead
- Demonstrate that Version 3 can extract substrings without allocation
- **Anti-pattern:** Show why using ``string_view`` in a constructor that stores ``std::string`` is wrong:

  .. code-block:: cpp
  
     // ❌ Wrong
     class Document {
         std::string title_;
     public:
         Document(std::string_view title) : title_{title} {}  // Still copies!
     };
     
     // ✓ Correct
     class Document {
         std::string title_;
     public:
         Document(const std::string& title) : title_{title} {}
     };


5. Complete Vehicle System Implementation
------------------------------------------

Design and implement a complete class following all lecture best practices.

**Requirements:**

Implement a ``Bicycle`` class in the ``transportation`` namespace with:

**Attributes (all private):**

- ``brand_`` (``std::string``)
- ``gear_count_`` (``int``)
- ``current_gear_`` (``int``, default 1)
- ``is_locked_`` (``bool``, default ``true``)

**Constructors:**

- Default: brand="Generic", gear_count=1
- Parameterized: takes brand and gear_count, validates ``gear_count > 0``
- Use member initializer lists for both

**Methods:**

- ``shift_up()`` — increases gear if ``current_gear_ < gear_count_`` and not locked
- ``shift_down()`` — decreases gear if ``current_gear_ > 1`` and not locked
- ``lock()`` / ``unlock()`` — toggle lock state (``noexcept``)
- ``get_current_gear()`` — accessor (``[[nodiscard]] const noexcept``)

**Advanced:**

- ``get_gear_ratio()`` — returns ``std::optional<double>`` calculating ratio based on current gear
  
  - Returns ``std::nullopt`` if locked
  - Formula: ``2.0 + (current_gear_ - 1) * 0.5``

**Tasks:**

- Create complete project structure: ``include/``, ``src/``, ``CMakeLists.txt``
- Add full Doxygen documentation
- Write ``main.cpp`` with comprehensive test cases:
  
  - Create bicycles with stack and heap allocation
  - Test all methods including error cases
  - Demonstrate ``optional`` usage with ``value_or()``

- **Validation tests:**
  
  - Verify shifting when locked returns ``false``
  - Verify cannot shift beyond gear limits
  - Verify ``get_gear_ratio()`` returns ``nullopt`` when locked

- Create a simple UML class diagram showing:
  
  - Class name (``Bicycle``)
  - All attributes with types and visibility
  - All methods with return types and visibility
  - Mark ``const`` methods appropriately


6. Scoped Enums (``enum class``) for Type-Safe Presets
--------------------------------------------------------

Replace fragile string fields with **strongly typed** scoped enums and provide conversion utilities.

Requirements
~~~~~~~~~~~~

- In namespace ``transportation``, define:

  .. code-block:: cpp

     enum class Color { Red, Blue, Green, Black, White, Silver, Unknown };
     enum class Model { Sedan, SUV, Truck, Coupe, Hatchback, Unknown };

- Refactor a class ``Vehicle`` to use these enums:

  .. code-block:: cpp

     class Vehicle {
     private:
         Color color_{Color::Unknown};
         Model model_{Model::Unknown};
         bool  is_running_{false};
         int   max_speed_{0};

     public:
         Vehicle(Color color, Model model, int max_speed);
         void start_engine();
         void stop_engine();
         void drive();
         [[nodiscard]] Color color() const noexcept;
         [[nodiscard]] Model model() const noexcept;
         [[nodiscard]] int   max_speed() const noexcept;
     };

  - Implement the constructor with a member initializer list and validate ``max_speed > 0`` (throw ``std::invalid_argument`` otherwise).
  - All accessors must be ``[[nodiscard]]`` and ``noexcept``.

- Provide readable conversions:

  .. code-block:: cpp

     std::string to_string(Color c);
     std::string to_string(Model m);

  - Implement via ``switch`` with **no default** and an explicit ``return`` for each enumerator.
  - Optionally add a ``default:`` returning ``"Unknown"`` if your compiler warns for missing cases.

- Provide parsing helpers that **do not throw**:

  .. code-block:: cpp

     std::optional<Color> parse_color(std::string_view s) noexcept;
     std::optional<Model> parse_model(std::string_view s) noexcept;

  - Accept case-insensitive inputs such as ``"red"``, ``"RED"``, or ``"Red"``.
  - Return ``std::nullopt`` for unknown tokens.

- Overload stream insertion for quick debugging:

  .. code-block:: cpp

     inline std::ostream& operator<<(std::ostream& os, Color c) { return os << to_string(c); }
     inline std::ostream& operator<<(std::ostream& os, Model m) { return os << to_string(m); }

Tasks
~~~~~

- **Header/Source split:**
  
  - Place enum declarations and conversions in ``include/transportation/types.hpp`` and their definitions in ``src/types.cpp``.
  - Implement ``Vehicle`` in ``include/vehicle.hpp`` and ``src/vehicle.cpp``.

- **Factory function:**

  .. code-block:: cpp

     std::optional<Vehicle> make_vehicle(std::string_view color,
                                         std::string_view model,
                                         int max_speed) noexcept;

  - Use ``parse_color`` and ``parse_model``.
  - Return ``std::nullopt`` if parsing fails or ``max_speed <= 0``.

- **Compile-time checks:**

  - Add ``static_assert(std::is_enum_v<Color> && std::is_enum_v<Model>);``
  - Optionally fix the underlying type:

    .. code-block:: cpp

       enum class Color : std::uint8_t { ... };
       enum class Model : std::uint8_t { ... };

- **Demonstration program (``main.cpp``):**
  
  - Construct vehicles using both enums directly and via ``make_vehicle("Red", "SUV", 180)``.
  - Print them using ``operator<<``.
  - Show behavior for invalid input (e.g., ``"Purple"`` or ``"Spaceship"``) and handle ``std::nullopt`` using ``value_or`` or conditional checks.
  - Verify that accidental assignments like ``color_ = "Red";`` no longer compile.

- **Doxygen:**
  
  - Document each enumerator and all conversion functions.
  - Mark non-throwing functions as ``noexcept`` and add ``\\warning`` on parsing about accepted spellings and case-insensitivity.

Validation Criteria
~~~~~~~~~~~~~~~~~~~~

- Assigning a string literal to ``color_`` or ``model_`` **does not compile**.
- ``to_string`` covers all enumerators; missing cases trigger warnings under ``-Wall -Wextra -Werror``.
- ``parse_color`` and ``parse_model`` return ``std::nullopt`` for unknown tokens and never throw.
- ``make_vehicle`` returns a disengaged ``std::optional`` for invalid input.
- All public methods and conversion helpers are documented and pass basic unit tests.

Bonus
~~~~~

- **Serialization:**
  
  Implement ``to_json`` / ``from_json`` adapters for ``nlohmann::json`` mapping enums to strings via your conversion helpers.

- **Hashing:**
  
  Provide a hasher for use in unordered containers:

  .. code-block:: cpp

     struct ColorHash {
         std::size_t operator()(Color c) const noexcept {
             return static_cast<std::size_t>(c);
         }
     };

- **Underlying type control:**
  
  Use ``enum class Color : std::uint8_t`` and ``enum class Model : std::uint8_t`` to reduce footprint, and explain trade-offs in your report.
