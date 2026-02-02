=====================
Requirements Analysis
=====================

The **requirements analysis** defines **what** the system must do before designing **how** it will work.
It captures functional capabilities, quality attributes, constraints, and measurable success criteria
for the transportation domain supporting both autonomous robotaxis and traditional human-driven taxis
(Passenger, Vehicle, RoboTaxi, Taxi, Driver, Fleet, Route, Sensor, Location, Position).

------------------------
Functional Requirements
------------------------


.. list-table::
   :widths: 25 60 15
   :header-rows: 1
   :class: compact-table

   * - **ID**
     - **Requirement**
     - **Priority**
   * - FR-1
     - The system shall allow a Passenger to **request a ride** by specifying pickup and dropoff locations.
     - Must
   * - FR-2
     - The system shall allow a Fleet to **dispatch an available vehicle** to service a ride request, supporting both RoboTaxi and Taxi vehicles.
     - Must
   * - FR-3
     - The system shall support **polymorphic vehicle behavior**: Vehicle subclasses (RoboTaxi, Taxi) must implement type-specific driving operations.
     - Must
   * - FR-4
     - The system shall enforce that each RoboTaxi contains **one or more Sensors** for autonomous navigation and safety monitoring.
     - Must
   * - FR-5
     - The system shall allow a Vehicle to **follow an optional Route**; if a Route is assigned, the Vehicle shall navigate along the route waypoints.
     - Must
   * - FR-6
     - The system shall expose **status queries** (e.g., vehicle status, current location, driver information for Taxi).
     - Should
   * - FR-7
     - The system shall **log key lifecycle events** (ride requested, vehicle dispatched, route assigned, passenger boarded/exited, trip completed).
     - Should
   * - FR-8
     - The system shall **read sensor data continuously** during RoboTaxi operation for navigation and obstacle detection.
     - Must
   * - FR-9
     - The system shall allow **creating and optimizing Routes** with multiple waypoints at runtime.
     - Should
   * - FR-10
     - The system shall support **Fleet management operations** including adding/removing vehicles and querying available vehicles.
     - Must
   * - FR-11
     - The system shall support **driver management** for traditional Taxi vehicles, including assigning and removing drivers.
     - Must
   * - FR-12
     - The system shall support **passenger boarding and exiting** operations that update vehicle state and passenger count.
     - Must

----------------------------
Non-Functional Requirements
----------------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Attribute**
     - **Requirement**
   * - Performance
     - Sensor data reading shall complete within **50 ms** per sensor, and route optimization shall complete within **500 ms** for routes with up to 20 waypoints.
   * - Reliability
     - The system shall handle sensor failures gracefully with redundancy; mean time between failures **> 1000 hours** for autonomous operation.
   * - Safety
     - The system shall prevent unsafe operations (e.g., passenger boarding while vehicle is in motion) via validated state checks in the Vehicle.
   * - Availability
     - Fleet dispatch and vehicle status operations shall be available **99.9%** during operational hours.
   * - Observability
     - All ride requests, vehicle dispatches, route assignments, and passenger events shall be logged with timestamps, location data, and entity identifiers.
   * - Maintainability
     - The system shall separate concerns by layers and achieve **< 10%** cyclic dependency density in static analysis.
   * - Extensibility
     - Adding a new Vehicle subtype (e.g., RoboBus) shall require **no changes** to existing Fleet or Route management logic.

----------------------
Technical Constraints
----------------------

.. list-table::
   :widths: 28 72
   :header-rows: 1
   :class: compact-table

   * - **Constraint**
     - **Description**
   * - Namespace Organization
     - All domain classes (Vehicle, RoboTaxi, Taxi, Driver, Sensor, Fleet, Passenger, Route, Location, Position) shall be encapsulated within the ``transportation`` namespace to provide logical grouping and prevent naming conflicts.
   * - Encapsulation
     - External actors shall not access Sensors directly. All sensor operations are managed internally by RoboTaxi.
   * - Composition Rule
     - Each RoboTaxi contains one or more Sensors (composition). Sensor lifecycle is bound to RoboTaxi lifecycle. Each Sensor has a Position that defines its mounting location (composition).
   * - Aggregation Rule
     - Fleet aggregates Vehicles. Vehicles can exist independently of the Fleet and can be transferred between Fleets.
   * - Optional Route
     - Route association is optional at runtime. Vehicles can operate without a Route assigned (e.g., idle, charging).
   * - Driver Association
     - Taxi vehicles have an optional Driver association. Taxis can operate without an assigned driver during off-hours.
   * - Type Abstraction
     - Diagram types are language agnostic (e.g., ``String``, ``Integer``), and mapping to concrete types (e.g., ``std::string``, ``int``) is an implementation detail.
   * - Error Handling
     - Operations must return typed results or exceptions with machine-readable codes and human-readable messages.

------------------------
Implementation Guidance
------------------------

**C++ Specific Constraints:**

All domain entities in the C++ implementation shall adhere to the following conventions:

- All domain classes shall be declared within the ``transportation`` namespace
- Header files shall use ``#pragma once`` or include guards with the pattern ``TRANSPORTATION_CLASSNAME_HPP``
- Member variables shall use camelCase convention (e.g., ``vehicleId``, ``currentLocation``, ``maxPassengers``)
- Pass ``std::string`` parameters as ``const std::string&`` in constructors and methods to avoid unnecessary copies
- Use ``std::shared_ptr`` for aggregation relationships (Fleet–Vehicle) and association relationships (Vehicle–Route, Passenger–Vehicle, Taxi–Driver)
- Use composition for Sensor ownership within RoboTaxi (RoboTaxi directly contains Sensors)
- Use composition for Position within Sensor (Sensor directly contains Position)
- Abstract methods shall be marked with ``= 0`` pure virtual specifier
- Class and method documentation shall follow Doxygen format with ``@file``, ``@class``, ``@brief``, ``@param``, and ``@return`` tags
- Virtual destructors shall be provided for all polymorphic base classes

**Namespace Structure:**

.. code-block:: cpp

   namespace transportation {
       // Core domain entities
       class Vehicle;      // Abstract base class
       class RoboTaxi;     // Autonomous taxi vehicle
       class Taxi;         // Human-driven taxi vehicle
       class Driver;       // Human driver
       class Sensor;       // Navigation and safety sensor
       struct Position;    // 3D sensor mounting position
       class Fleet;        // Vehicle fleet management
       class Passenger;    // Passenger/customer
       class Route;        // Navigation route
       class Location;     // Geographic location
       
       // Enumerations
       enum class SensorType;
       enum class VehicleStatus;
   }

**Example Usage:**

.. code-block:: cpp

  int main() {
    using transportation::Driver;
    using transportation::Fleet;
    using transportation::Location;
    using transportation::Passenger;
    using transportation::RoboTaxi;
    using transportation::Route;
    using transportation::Taxi;
    using transportation::Vehicle;

    // Fleet is shared because Passenger holds a shared_ptr<Fleet>
    auto fleet = std::make_shared<Fleet>("Fleet-001", "RideShare Inc");

    // Vehicles (id, max_passengers)
    auto robotaxi = std::make_shared<RoboTaxi>("ROBOTAXI-001", 4);
    auto taxi     = std::make_shared<Taxi>("TAXI-001", 4);

    // Assign a driver to Taxi (id, name, license)
    auto driver = std::make_shared<Driver>("D-001", "John Smith", "DL-12345");
    taxi->assign_driver(driver);

    // Base route for RoboTaxi
    auto robo_route = std::make_shared<Route>("R-ROBO-001");
    robo_route->add_waypoint(Location{37.7749, -122.4194}); // San Francisco
    robo_route->add_waypoint(Location{37.7890, -122.4010}); // Financial District
    robo_route->add_waypoint(Location{37.7955, -122.3937}); // Embarcadero
    robo_route->optimize_route();
    robotaxi->set_route(robo_route);

    // Base route for Taxi
    auto taxi_route = std::make_shared<Route>("R-TAXI-001");
    taxi_route->add_waypoint(Location{37.7749, -122.4194}); // San Francisco
    taxi_route->add_waypoint(Location{37.7980, -122.3770}); // Bay Bridge (west)
    taxi_route->add_waypoint(Location{37.8044, -122.2712}); // Oakland
    taxi_route->optimize_route();
    taxi->set_route(taxi_route);

    // Register vehicles in the fleet
    fleet->add_vehicle(robotaxi);
    fleet->add_vehicle(taxi);

    // Passenger requires (id, name, phone, shared_ptr<Fleet>)
    auto passenger = std::make_shared<Passenger>("P-001", "Jane Doe", "555-1234", fleet);

    // Trip endpoints
    Location pickup{37.7749, -122.4194};   // San Francisco
    Location dropoff{37.8044, -122.2712};  // Oakland

    // Dispatch an available vehicle
    std::shared_ptr<Vehicle> dispatched = fleet->dispatch_vehicle(pickup, dropoff);

    // Trip-specific route: pickup -> dropoff
    auto trip_route = std::make_shared<Route>("TRIP-0001");
    trip_route->add_waypoint(pickup);
    trip_route->add_waypoint(dropoff);
    trip_route->optimize_route();
    dispatched->set_route(trip_route);

    // Execute trip
    dispatched->pickup_passenger(passenger);
    dispatched->dropoff_passenger(passenger);
  }


----------------
Success Criteria
----------------

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Criterion**
     - **Measurable Outcome**
   * - Ride Request and Dispatch
     - Passenger requests ride with pickup/dropoff locations; Fleet dispatches available vehicle (RoboTaxi or Taxi) within **500 ms** and logs the event with timestamps and location data.
   * - Polymorphic Vehicle Behavior
     - For RoboTaxi and Taxi, invoking type-specific methods (drive, sensor operations, driver management) produces correct behavior without code changes in Fleet management; verified by unit tests covering all subtypes (**> 95%** branch coverage).
   * - Sensor Data Collection
     - RoboTaxis continuously read sensor data with **< 50 ms** latency per sensor; sensor failures are detected and logged within **100 ms**.
   * - Route Navigation
     - Vehicle navigates successfully with and without a Route; when a Route is assigned, route optimization completes within **500 ms** for routes with up to 20 waypoints.
   * - Fleet Management
     - Fleet operations (add/remove vehicle, query available vehicles) complete within **100 ms**; fleet maintains accurate vehicle inventory including both RoboTaxi and Taxi vehicles in **100%** of test cases.
   * - Driver Management
     - Taxi driver assignment and removal operations complete successfully; driver information is accurately tracked in **100%** of test cases.
   * - Passenger Operations
     - Passenger boarding/exiting operations correctly update vehicle passenger count and state in **100%** of test cases.
   * - Separation of Concerns
     - Static analysis reports **0** direct dependencies from Presentation to Domain or Infrastructure; only Application mediates.
   * - Observability
     - Logs contain complete audit trails (ride requests, dispatches, passenger events, route navigation) with **no missing events** in end-to-end tests across **N ≥ 50** scripted scenarios.
   * - Namespace Compliance
     - All domain classes reside within ``transportation`` namespace; static analysis confirms zero global namespace pollution from domain entities.

-------------------------
Assumptions and Scope
-------------------------

- A RoboTaxi contains one or more Sensors for autonomous navigation and safety.
- Each Sensor has a Position that defines its 3D mounting location on the vehicle.
- A Taxi may have zero or one Driver; drivers can be assigned or removed dynamically.
- A Fleet may contain zero or more Vehicles of mixed types (RoboTaxi and Taxi); vehicles can be added or removed dynamically.
- A Passenger may ride in zero or one Vehicle at any given time.
- A Vehicle may follow **zero or one** current Route; Routes may be shared or reused across vehicles.
- Sensor readings are simulated; timings refer to software execution in the target environment.
- All domain entities are organized within the ``transportation`` namespace in the C++ implementation.
- Language-agnostic design allows implementation in multiple programming languages while maintaining conceptual integrity.
- The system focuses on core ride-hailing functionality; payment processing and user authentication are out of scope.

-----------------------
Verification Approach
-----------------------

- **Unit tests** for Vehicle state management, Sensor data reading, Driver assignment, Fleet operations, and subtype-specific behavior within the ``transportation`` namespace.
- **Integration tests** for Passenger-Fleet-Vehicle interactions, route navigation, passenger boarding/exiting, and driver management across namespace boundaries.
- **Contract tests** for repository and gateway adapters (Infrastructure) to ensure stable interfaces with domain entities.
- **Static analysis** for dependency direction, absence of forbidden couplings, proper namespace usage, and cyclic dependency metrics.
- **Namespace verification** to ensure all domain classes are properly encapsulated within ``transportation`` and no global namespace pollution occurs.
- **Performance tests** to validate sensor reading completes within 50 ms per sensor and route optimization within 500 ms under nominal load.
- **Safety tests** to verify invalid state transitions (e.g., boarding while moving) are properly rejected with appropriate error codes in 100% of negative test cases.
- **Code coverage analysis** ensuring > 95% branch coverage on polymorphic vehicle behavior across RoboTaxi and Taxi subtypes.
- **Reliability tests** for sensor failure handling and graceful degradation under fault conditions.
- **Driver management tests** to verify correct assignment, removal, and information retrieval for Taxi vehicles.