Modeling Phase
================

Introduction
------------

The **Modeling Phase** focuses on defining *how* a system is structured and behaves to satisfy
its requirements. It bridges the gap between the problem domain and the implementation domain,
providing visual representations that make complex designs easier to understand, communicate,
and maintain.

During this phase, several diagrams are used to represent different perspectives of the system:

- **Class Diagrams** – Depict the static structure of the system, including its classes,
  attributes, methods, and relationships.
- **Sequence Diagrams** – Illustrate the dynamic flow of interactions between objects over time.


Each diagram contributes to a comprehensive understanding of both the **structural** and
**behavioral** aspects of the system.


.. note::

   The naming conventions for **classes**, **attributes**, and **methods** used in these diagrams
   are **language-agnostic**.  
   The same applies to data types (for example, ``String`` is used instead of ``std::string`` or
   ``string``). This abstraction ensures that the design can be applied across multiple programming
   languages and paradigms without being tied to a specific implementation syntax.


Class Diagram
---------------

.. only:: html

   .. figure:: /_static/lecture8/design/class_diagram_light.png
      :alt: Class Diagram
      :align: center
      :width: 100%
      :class: only-light

   .. figure:: /_static/lecture8/design/class_diagram_dark.png
      :alt: Class Diagram
      :align: center
      :width: 100%
      :class: only-dark

This class diagram represents a **transportation system** that includes both autonomous robotaxis
and traditional human-driven taxis. It shows how various entities interact and relate to each other
through inheritance, composition, aggregation, and association. The model captures the structural
organization of a ride-hailing service supporting both autonomous and human-operated vehicles.

.. note::

   All classes in the domain layer are organized within the ``transportation`` namespace, providing
   logical grouping and preventing naming conflicts with other system components.

.. tip::

  UML and modeling tools use diverse notations to express specific characteristics of classes, methods, and attributes. Understanding these conventions ensures that diagrams convey both **structure** and **semantics** accurately.

  - **Abstract Classes:**  
    In PlantUML, an abstract class is represented by the letter *A* inside a circle. Other modeling tools may use different notations; for instance, Mermaid uses the ``<<abstract>>`` stereotype (see `Mermaid class diagrams <https://mermaid.js.org/syntax/classDiagram.html>`_).  
    Regardless of the notation style, abstract classes must always be explicitly indicated in class diagrams to distinguish them from concrete classes. Example of an abstract class in PlantUML:

    .. code-block:: java

       abstract class Dummy {
         ...
       }

  - **Abstract Methods:**  
    Abstract methods (called *pure virtual functions* in C++) are typically displayed in *italics* or annotated with the ``{abstract}`` label. In PlantUML, abstract methods are explicitly marked with ``{abstract}`` preceding the method name. These methods have no implementation in the abstract class and must be overridden by concrete subclasses. Example of an abstract method in PlantUML:

    .. code-block:: java

       class Dummy {
         + {abstract} method(): void
       }

  - **Virtual Methods:**  
    Virtual methods (those that can be overridden by derived classes) may not have distinct notations in every tool. They are often documented textually or marked with a stereotype. In C++, these correspond to methods declared with the ``virtual`` keyword that have a base implementation but may be redefined by subclasses.

    .. code-block:: java

       class Dummy {
         + {virtual} method(): void
       }

  - **Static Attributes:**  
    Static (class-level) attributes shared by all instances are shown **underlined** in standard UML notation. In PlantUML, the same can be expressed using the ``{static}`` modifier or underlining the attribute name. Static attributes belong to the class itself, not to any individual instance. Example of a static attribute in PlantUML:

    .. code-block:: java

       class Dummy {
         + {static} id: String
       }

  - **Static Methods:**  
    Static methods—class-level operations that do not require an instance—are also shown **underlined** in UML. In PlantUML, they can be denoted with ``{static}`` or by underlining the method name. Static methods can be invoked directly from the class.

    .. code-block:: java

       class Dummy {
         + {static} method(): void
       }

  - **Constant Attributes:**  
    Constants or read-only attributes are frequently marked with ``{readOnly}`` or written in uppercase (e.g., ``MAX_PASSENGERS``). In C++, these correspond to ``const`` or ``static const`` members that cannot be modified after initialization.

    .. code-block:: java

       class Dummy {
         + {readOnly} max_passengers: Integer
       }

  - **Visibility Modifiers:**  
    UML applies standardized symbols to denote access levels:
    
    - ``+`` → **Public** (accessible from anywhere)  
    - ``-`` → **Private** (accessible only within the class)  
    - ``#`` → **Protected** (accessible within the class and its subclasses)  


  These conventions ensure that class diagrams communicate not only the *structure* of a design but also the *intended behavior* and *scope* of its members: clarifying which methods can be invoked, which attributes are shared, and how access is controlled across classes.

~~~~~~~~~~~~~~~~
Key Components
~~~~~~~~~~~~~~~~

**Vehicle (Abstract Class)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Purpose:** Defines the general structure and behavior common to all vehicle types in the transportation system.
- **Namespace:** ``transportation``
- **Attributes:**

  - ``id : String`` - Unique vehicle identifier for tracking and fleet management
  - ``currentLocation : Location`` - Current geographic position of the vehicle
  - ``status : VehicleStatus`` - Current operational state (IDLE, IN_SERVICE, EN_ROUTE, CHARGING, MAINTENANCE, OUT_OF_SERVICE)
  - ``route : Route`` - Navigation route the vehicle is currently following (optional)
  - ``maxPassengers : Integer`` - Maximum number of passengers the vehicle can accommodate
  - ``currentPassengerCount : Integer`` - Number of passengers currently in the vehicle

- **Operations:**

  - ``{abstract} drive() : void`` — Executes vehicle movement; must be implemented by subclasses to define type-specific driving behavior
  - ``updateLocation(location : Location) : void`` — Updates the vehicle's current geographic position
  - ``getStatus() : VehicleStatus`` — Returns the current operational status of the vehicle
  - ``setRoute(route : Route) : void`` — Assigns a navigation route to the vehicle
  - ``getRoute() : Route`` — Retrieves the currently assigned route
  - ``pickupPassenger(passenger : Passenger) : void`` — Adds a passenger to the vehicle and updates passenger count
  - ``dropoffPassenger(passenger : Passenger) : void`` — Removes a passenger from the vehicle and updates passenger count

.. note::
    
    - The ``Vehicle`` class is abstract, meaning it cannot be instantiated directly. It provides a consistent interface for all concrete vehicle types and manages core operations like passenger handling and route following.



**Concrete Vehicle Types**
^^^^^^^^^^^^^^^^^^^^^^^^^^

All concrete vehicle types reside in the ``transportation`` namespace and inherit from ``Vehicle``.

1. **RoboTaxi**

   - **Purpose:** Represents an autonomous, self-driving taxi that uses sensors for navigation and operation.
   
   - **Additional Attributes:** 
     
     - ``sensors : List<Sensor>`` – Collection of sensors for autonomous navigation and safety (composition)
   
   - **Operations:**
     
     - ``drive() : void`` – Implements autonomous driving behavior using sensor data
     - ``addSensor(sensor : Sensor) : void`` – Adds a sensor to the robotaxi's sensor array

   The RoboTaxi specializes the ``Vehicle`` class by adding autonomous capabilities through
   integrated sensor systems. It manages its own navigation without human intervention.

2. **Taxi**

   - **Purpose:** Represents a traditional human-operated taxi with a driver.
   
   - **Additional Attributes:** 
     
     - ``driver : Driver`` – The human driver operating this taxi
   
   - **Operations:**
     
     - ``drive() : void`` – Implements human-driven operation behavior
     - ``assignDriver(driver : Driver) : void`` – Assigns a driver to this taxi
     - ``removeDriver() : void`` – Removes the current driver from this taxi
     - ``getDriver() : Driver`` – Returns the driver currently assigned to this taxi

   The Taxi specializes the ``Vehicle`` class by adding driver management capabilities.
   It requires a human driver for operation.

**Driver**
^^^^^^^^^^

- **Namespace:** ``transportation``
- **Purpose:** Represents a human driver who operates traditional Taxi vehicles.
- **Attributes:** 
  
  - ``id : String`` – Unique driver identifier
  - ``name : String`` – Driver's full name
  - ``licenseNumber : String`` – Driver's license number
  - ``rating : Float`` – Driver's performance rating

- **Operations:** 
  
  - ``getId() : String`` – Returns the unique driver identifier
  - ``getName() : String`` – Returns the driver's name
  - ``getLicenseNumber() : String`` – Returns the driver's license number
  - ``getRating() : Float`` – Returns the driver's rating

- **Relationship:** Association (``-->``) with ``Taxi``.
  A Taxi is operated by a Driver. The relationship indicates that a Taxi may have 0 or 1 Driver
  at any given time, supporting scenarios where taxis are temporarily unassigned.

**Sensor**
^^^^^^^^^^

- **Namespace:** ``transportation``
- **Attributes:** 
  
  - ``sensorId : String`` – Unique sensor identifier
  - ``sensorType : SensorType`` – Type of sensor (LIDAR, CAMERA, RADAR, GPS, IMU)
  - ``positionOnVehicle : Position`` – Physical mounting position on the vehicle (composition)

- **Operations:** 
  
  - ``readData() : SensorData`` – Reads current sensor data for navigation and obstacle detection
  - ``calibrate() : void`` – Performs sensor calibration procedure
  - ``getType() : SensorType`` – Returns the type of sensor
  - ``getSensorId() : String`` – Returns the unique sensor identifier

- **Relationship:** Composition (``*--``) with ``RoboTaxi``.
  A robotaxi contains one or more sensors; if the robotaxi is destroyed,
  the sensors are destroyed as well. This enforces that autonomous vehicles have
  integrated sensor systems for navigation and safety.
- **Purpose:** Represents sensor hardware for autonomous navigation, obstacle detection,
  and situational awareness in robotaxis.

.. important::
   **Encapsulation Rule:** External actors cannot interact directly with
   Sensors. All sensor operations are managed internally by the RoboTaxi, which
   processes sensor data for navigation decisions.

**Position (Struct)**
^^^^^^^^^^^^^^^^^^^^^

- **Namespace:** ``transportation``
- **Attributes:**

  - ``x : Double`` – X-coordinate of the sensor mounting position on the vehicle
  - ``y : Double`` – Y-coordinate of the sensor mounting position on the vehicle
  - ``z : Double`` – Z-coordinate of the sensor mounting position on the vehicle

- **Relationship:** Composition (``*--``) with ``Sensor``.
  Each sensor has a position that defines where it is mounted on the vehicle.
- **Purpose:** Represents the 3D mounting location of sensors on the vehicle body for
  precise sensor fusion and calibration.

**Fleet**
^^^^^^^^^

- **Namespace:** ``transportation``
- **Attributes:**

  - ``id : String`` – Unique fleet identifier
  - ``operatorName : String`` – Name of the fleet operating company
  - ``serviceArea : List<Location>`` – Geographic regions where fleet operates
  - ``vehicles : List<Vehicle>`` – Collection of vehicles managed by the fleet (both RoboTaxi and Taxi)

- **Operations:**

  - ``addVehicle(vehicle : Vehicle) : void`` — Adds a vehicle to the fleet inventory
  - ``removeVehicle(vehicle : Vehicle) : void`` — Removes a vehicle from the fleet
  - ``getAvailableVehicles() : List<Vehicle>`` — Returns all idle vehicles ready for dispatch
  - ``dispatchVehicle(pickup : Location, dropoff : Location) : Vehicle`` — Assigns an available vehicle to service a ride request
  - ``getId() : String`` — Returns the unique fleet identifier
  - ``getOperatorName() : String`` — Returns the name of the fleet operator

- **Relationship:** Aggregation (``o--``) with ``Vehicle``.
  The fleet manages vehicles but does not own them; vehicles exist independently
  and can be transferred between fleets or operate independently. This applies to
  both autonomous RoboTaxis and human-driven Taxis.

**Passenger**
^^^^^^^^^^^^^

- **Namespace:** ``transportation``
- **Attributes:**

  - ``id : String`` – Unique passenger identifier
  - ``name : String`` – Passenger's name
  - ``phoneNumber : String`` – Contact phone number
  - ``currentVehicle : Vehicle`` – The vehicle the passenger is currently riding in (if any)

- **Operations:**

  - ``requestRide(pickup : Location, dropoff : Location) : void`` — Requests a ride from the fleet specifying pickup and dropoff locations
  - ``getId() : String`` — Returns the unique passenger identifier
  - ``getName() : String`` — Returns the passenger's name

- **Relationship:** Association (``-->``) with ``Vehicle`` and ``Fleet``.
  A passenger rides in zero or one vehicle at any given time (temporary relationship).
  A passenger requests rides from a fleet (zero or more passengers can make requests).

**Route**
^^^^^^^^^

- **Namespace:** ``transportation``
- **Attributes:**

  - ``id : String`` – Unique route identifier
  - ``waypoints : List<Location>`` – Ordered list of locations defining the navigation path

- **Operations:** 
  
  - ``addWaypoint(location : Location) : void`` – Adds a waypoint to the route
  - ``optimizeRoute() : void`` – Optimizes the route for efficiency
  - ``getDistance() : Double`` – Calculates and returns total route distance
  - ``getId() : String`` – Returns the unique route identifier
  - ``getWaypointCount() : Integer`` – Returns the number of waypoints in the route

- **Relationship:** Composition (``*--``) with ``Location`` for waypoints.
  A route consists of one or more waypoints; waypoints are integral to the route definition.
  Association (``-->``) with ``Vehicle`` – a vehicle may follow zero or one route at any time.
- **Purpose:** Defines navigation paths for vehicles, supporting both single trips and multi-stop routes.

**Location**
^^^^^^^^^^^^

- **Namespace:** ``transportation``
- **Attributes:**

  - ``latitude : Double`` – Geographic latitude coordinate
  - ``longitude : Double`` – Geographic longitude coordinate

- **Operations:** 
  
  - ``distanceTo(other : Location) : Double`` – Calculates distance to another location
  - ``getLatitude() : Double`` – Returns the latitude coordinate
  - ``getLongitude() : Double`` – Returns the longitude coordinate

- **Relationship:** Used by Route (waypoints), Vehicle (currentLocation), and Fleet (serviceArea).
- **Purpose:** Represents geographic coordinates for navigation, service boundaries, and positioning.

**Enumerations**
^^^^^^^^^^^^^^^^

1. **SensorType**

   - **Values:** LIDAR, CAMERA, RADAR, GPS, IMU
   - **Purpose:** Defines the types of sensors that can be installed on a RoboTaxi
   - **Relationship:** Each Sensor has a SensorType that determines its data format and capabilities

2. **VehicleStatus**

   - **Values:** IDLE, IN_SERVICE, EN_ROUTE, CHARGING, MAINTENANCE, OUT_OF_SERVICE
   - **Purpose:** Defines the operational states a vehicle can be in
   - **Relationship:** Each Vehicle has a VehicleStatus that determines its availability and current operation

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Conceptual Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Dual Vehicle Types:**  
  The design supports both autonomous (RoboTaxi) and human-operated (Taxi) vehicles through
  a common ``Vehicle`` abstraction. This enables mixed fleets and flexible deployment strategies.

- **Encapsulation of Behavior:**  
  The ``RoboTaxi`` encapsulates sensor management internally. External actors (Passenger, Fleet) only
  interact with the ``Vehicle`` interface, never with ``Sensors`` directly. This promotes abstraction
  and separation of concerns, and enforces the technical constraint that sensors cannot be accessed directly.

- **Polymorphism:**  
  Concrete vehicles (RoboTaxi, Taxi) provide type-specific implementations of ``drive()``
  and specialized operations, enabling dynamic behavior depending on the vehicle type at runtime.
  The Fleet can manage both vehicle types uniformly through the Vehicle interface.

- **Optional Relationships:**  
  The ``Route`` association is optional; a vehicle can operate without being assigned a route
  (e.g., idle, charging). Similarly, a ``Passenger`` may or may not be riding in a vehicle at a given time. For instance, a ``Passenger`` waiting for the vehicle to arrive is not currently riding the vehicle.
  A ``Taxi`` may not have a ``Driver`` during off-hours or between shifts.

- **Ownership Hierarchy:**  

  - ``RoboTaxi`` **owns** ``Sensors`` — composition (sensors are integral parts of the autonomous vehicle).  
  - ``Sensor`` **owns** ``Position`` — composition (position is an integral property of sensor placement).
  - ``Route`` **owns** ``Waypoints`` (Locations) — composition (waypoints define the route).
  - ``Fleet`` **manages** ``Vehicles`` — aggregation (vehicles can exist independently of fleet).  
  - ``Vehicle`` **follows** ``Route`` — association (optional relationship).
  - ``Passenger`` **rides in** ``Vehicle`` — association (temporary relationship).
  - ``Taxi`` **operated by** ``Driver`` — association (driver can be assigned/unassigned).

- **Fleet Management:**
  The ``Fleet`` provides centralized management of all vehicle types, including dispatch logic, availability
  tracking, and service area management. This separates vehicle lifecycle from ride operations and enables
  unified management of heterogeneous vehicle types.

~~~~~~~~~~~~~~~~~~~~~~~~~~
Performance Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   **Performance Constraints:**
   
   - Sensor ``readData()`` operations complete within **50 ms per sensor**
   - Route ``optimizeRoute()`` completes within **500 ms for routes with up to 20 waypoints**
   - Fleet dispatch operations complete within **100 ms**
   - Fleet maintains **99.9% availability** during operational hours
   - All ride events (requests, dispatches, passenger boarding/exiting) are logged with timestamps and location data

~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~

This class diagram demonstrates several key object-oriented principles:

- **Abstraction** through the abstract ``Vehicle`` class supporting multiple vehicle types.  
- **Inheritance** and **polymorphism** in specialized vehicle types (RoboTaxi, Taxi).  
- **Encapsulation** of functionality within cohesive classes.  
- **Composition** for sensors that are integral parts of robotaxis and for sensor positions.
- **Aggregation** for fleet management where vehicles maintain independent lifecycles.
- **Association** for optional relationships (routes, passengers, drivers).
- **Clear separation of concerns** between passengers, fleet management, vehicle operations,
  driver management, navigation, and sensing.
- **Support for hybrid fleets** containing both autonomous and human-driven vehicles.

Overall, the design offers modularity, flexibility for extension to new vehicle types, and
a realistic mapping between software classes and transportation entities, while satisfying
both functional and non-functional requirements.

Sequence Diagram
-----------------

The **Sequence Diagram** captures the dynamic interaction between objects over time.
It illustrates how messages are passed, which operations are invoked, and how control
flows through the system to accomplish a specific ride request and completion.

.. only:: html

   .. figure:: /_static/lecture8/design/sequence_diagram_light.png
      :alt: Sequence Diagram
      :align: center
      :width: 100%
      :class: only-light

   .. figure:: /_static/lecture8/design/sequence_diagram_dark.png
      :alt: Sequence Diagram
      :align: center
      :width: 100%
      :class: only-dark

~~~~~~~~~~~~~~~~~~~~~~
Participants
~~~~~~~~~~~~~~~~~~~~~~

All participants belong to the ``transportation`` namespace in the implementation:

- **Passenger** – Customer requesting and using ride services; initiates ride requests.
- **Fleet** – Manages vehicle inventory and dispatches vehicles to service ride requests.
- **RoboTaxi** (Vehicle) – Autonomous vehicle that navigates routes and transports passengers.
- **Route** – Provides navigation path with waypoints for vehicle to follow.
- **Sensor** – Continuously provides data for navigation and obstacle detection.
- **Location** – Represents geographic coordinates (pickupLoc, dropoffLoc) for pickup, dropoff, and navigation waypoints.

~~~~~~~~~~~~~~~~~~~~~~
Message Flow
~~~~~~~~~~~~~~~~~~~~~~

1. **Passenger requests a ride** from the Fleet. 

   - Passenger calls ``dispatchVehicle(pickupLoc, dropoffLoc)`` on the Fleet.
   - Fleet queries available vehicles by calling ``getAvailableVehicles()`` on itself.
   - Fleet checks vehicle status by calling ``getStatus()`` on the RoboTaxi.
   - RoboTaxi returns its status (IDLE), indicating availability.

2. **Fleet creates and assigns a route**.  

   - Fleet creates a new Route object with a unique route ID.
   - Fleet adds the pickup location as a waypoint: ``addWaypoint(pickupLoc)``.
   - Fleet adds the dropoff location as a waypoint: ``addWaypoint(dropoffLoc)``.
   - Fleet optimizes the route by calling ``optimizeRoute()``.
   - Route calculates distances using ``distanceTo()`` method on Location objects.
   - Fleet assigns the optimized route to the RoboTaxi via ``setRoute(route)``.
   - Fleet returns the dispatched taxi to the Passenger.

3. **RoboTaxi navigates to pickup location**.  

   - While en route to pickup (loop construct):
     
     - RoboTaxi continuously reads sensor data by calling ``readData()`` on each Sensor.
     - Sensor returns SensorData for navigation and obstacle detection.
     - RoboTaxi updates its current location by calling ``updateLocation(newLocation)`` on itself.
     - RoboTaxi executes driving behavior by calling ``drive()`` on itself.
   
   - Loop continues until RoboTaxi arrives at pickup location.
   - RoboTaxi notifies Passenger of arrival.

4. **Passenger boards the vehicle**.  

   - Passenger physically boards the vehicle (actor action).
   - RoboTaxi calls ``pickupPassenger(Passenger)`` on itself to update its state.
   - Vehicle status updates to IN_SERVICE and passenger count increments.
   - RoboTaxi confirms readiness to Passenger.

5. **RoboTaxi navigates to dropoff location**.  

   - While en route to dropoff (loop construct):
     
     - RoboTaxi continues reading sensor data via ``readData()``.
     - Sensor returns SensorData for continued safe navigation.
     - RoboTaxi updates its location via ``updateLocation(newLocation)``.
     - RoboTaxi executes driving behavior via ``drive()``.
     - RoboTaxi queries route distance via ``getDistance()`` to monitor progress.
     - Route returns the distance value.
   
   - Loop continues until RoboTaxi arrives at dropoff location.
   - RoboTaxi notifies Passenger of arrival at destination.

6. **Passenger exits and trip completes**.  

   - Passenger physically exits the vehicle (actor action).
   - RoboTaxi calls ``dropoffPassenger(Passenger)`` on itself to update its state.
   - Passenger count decrements and vehicle prepares for next assignment.
   - RoboTaxi confirms trip completion to Passenger.
   - RoboTaxi notifies Fleet that trip is completed.
   - Fleet updates vehicle status to IDLE by calling ``setStatus(IDLE)`` on the RoboTaxi.

~~~~~~~~~~~~~~~~~~~~~~
Control Constructs
~~~~~~~~~~~~~~~~~~~~~~

- **loop [While en route to pickup]**: RoboTaxi continuously reads sensor data and updates location until it reaches the pickup point.
- **loop [While en route to dropoff]**: RoboTaxi navigates to the destination, reading sensors, updating location, and monitoring route progress.
- **object creation**: Route object is created dynamically during the ride request process.
- **activation boxes**: Show when objects are actively processing operations (fleet dispatch, route optimization, sensor reading, vehicle navigation).

~~~~~~~~~~~~~~~~~~~~~~
Key Interactions
~~~~~~~~~~~~~~~~~~~~~~

The sequence diagram highlights several important interactions:

- **Synchronous communication**: Most operations are synchronous with immediate return values (getStatus, setRoute, addWaypoint).
- **Continuous monitoring**: Sensor reading and location updates occur continuously in loops during navigation.
- **State transitions**: Vehicle status changes from IDLE → EN_ROUTE → IN_SERVICE → IDLE throughout the trip lifecycle.
- **Self-collaboration**: RoboTaxi frequently calls methods on itself (updateLocation, drive, pickupPassenger, dropoffPassenger) to manage its internal state.
- **Distance calculation**: Route optimization uses Location's ``distanceTo()`` method to calculate optimal paths.
- **Passenger-initiated actions**: Boarding and exiting are physical actions by the Passenger that trigger state updates in the RoboTaxi.

~~~~~~~~~~~~~~~~~~~~~~
Observability
~~~~~~~~~~~~~~~~~~~~~~

All key lifecycle events are logged with structured information:

- Ride requests (passenger ID, pickup/dropoff locations, timestamp)
- Vehicle dispatches (fleet ID, vehicle ID, route ID, timestamp)
- Route creation and optimization (route ID, waypoint count, optimization time)
- Passenger boarding/exiting (passenger ID, vehicle ID, location, timestamp)
- Sensor readings (vehicle ID, sensor type, timestamp, data quality metrics)
- Trip completion (vehicle ID, route ID, total distance, duration)

~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~

The sequence diagram complements the class diagram by showing the **runtime collaboration**
of objects during a complete ride lifecycle. It clarifies the responsibilities of each component:

- The **Passenger** initiates ride requests and physically boards/exits vehicles.
- The **Fleet** manages vehicle dispatch, route creation, optimization, and post-trip status updates.
- The **RoboTaxi** (Vehicle) executes autonomous navigation using sensor data, follows assigned routes, and manages passenger state transitions.
- The **Sensor** provides continuous data for safe autonomous navigation.
- The **Route** defines the navigation path through waypoints and supports distance calculations.
- The **Location** represents geographic coordinates for all spatial operations.

The interaction pattern demonstrates proper encapsulation (sensors only accessed by RoboTaxi),
clear separation of concerns (fleet management vs. vehicle operations), and realistic
autonomous vehicle behavior patterns. Together, the class and sequence diagrams provide a complete behavioral
and structural model of the transportation system that satisfies both functional requirements
and non-functional requirements (performance, safety, observability).