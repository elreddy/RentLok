<p align="center">
  <img src="Assets/Logo.png" alt="RentLok Logo" width="130"/>
</p>

# 📱 RentLok: Rental Management System (Version 1.0)

**RentLok** is a rental management solution designed to streamline the day-to-day operations of property managers. It enables easy tracking of rooms, bookings, payments, and tenant details through a modern Android mobile app backed by a robust data pipeline using PostgreSQL and Confluent Kafka.

This project demonstrates a real-time, event-driven architecture where property and room data is captured through a mobile app, stored in PostgreSQL, and processed asynchronously via Kafka. FastAPI serves as the middleware to connect the app with the database and Kafka topics.

---

## ✅ Features

### 📲 Mobile App (Android)
- Add/manage properties & rooms
- Track room availability & inquiries
- Record tenant bookings & payments
- View real-time operational metrics

### 🛠️ Backend Stack
| Component       | Role                                                                 |
|-----------------|----------------------------------------------------------------------|
| **PostgreSQL**  | Central transactional database for rental/operational data           |
| **Confluent Kafka** | Real-time event streaming for live updates (vacancies, inquiries, etc.) |
| **FastAPI**     | Middleware connecting app ↔ database ↔ Kafka   

---
## 🔧 System Architecture Diagram
<div align="center">
  <img src="Assets/DataFlow.JPG" width="550">
</div>


1. **Mobile App** → FastAPI (REST calls)
2. **FastAPI** → PostgreSQL (CRUD operations)
3. **PostgreSQL** → Kafka (publishing events)
4. **Kafka** → FastAPI (real-time stats)
5. **FastAPI** → Mobile App (real-time updates via consumer)

## 📱 Android App: Home Screen

The **RentLok** Android app provides a clean and intuitive user interface for property managers to efficiently navigate the system.

### Home Screen Overview
<table>
  <tr>
    <td><img src="Assets/SplashScreen.JPG" width="200"></td>
    <td style="padding-left;"><img src="Assets/HomeScreen.JPG" width="200"></td>
  </tr>
</table>

The **Home** screen acts as the central hub, offering quick access to the core modules of the RentLok system:

| Feature          | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| 🏢 **My Business** | Real-time dashboard showing vacancies and daily/monthly requests via Kafka |
| 🏠 **Properties**   | Manage property listings, add new properties, and view details             |
| 🚪 **Rooms**        | Add rooms to properties, set availability, and manage room metadata        |
| 💵 **Requests**     | View and handle incoming inquiries or service requests                     |
| 👥 **Tenants**      | Maintain tenant records and history                                        |
| 📅 **Bookings**     | Create, view, and manage tenant bookings and stay durations                |
| 💰 **Payments**     | Log and track rent payments, view history, and check dues                  |


## 1) Properties: 

Manage rental properties directly from the mobile app.
<table>
  <tr>
    <td><img src="Assets/PropertiesScreen.JPG" width="200"></td>
    <td style="padding-left;"><img src="Assets/PropertiesScreen(Add).JPG" width="200"></td>
  </tr>
</table>

### 📲 Screen

- **View Properties** – Displays all saved properties with basic details
- **Add Property** – Input property name, address, and number of rooms

### 🔧 CRUD Operations

- ✅ **Create** → Add new property  
- 📖 **Read** → View all properties  
- 📝 **Update** → Update property info  
- ❌ **Delete** → Mark property as inactive

## 2) Rooms:

Add and manage rooms under each property directly from the mobile app.
<table>
  <tr>
    <td><img src="Assets/RoomsScreen.JPG" width="200"></td>
    <td><img src="Assets/RoomsScreen(Add).JPG" width="200"></td>
  </tr>
</table>

### 📲 Screen

- **View Rooms** – Displays all rooms under a selected property
- **Add Room** – Input room number, monthly rent, and availability status

### 🔧 CRUD Operations

- ✅ **Create** → Add new room under a selected property  
- 📖 **Read** → View rooms for a selected property  
- 📝 **Update** → Update room details  
- ❌ **Delete** → Mark room as inactive

## 3) Requests:

Track and manage room rental inquiries for each property from the mobile app.

<table>
  <tr>
    <td><img src="Assets/RequestsScreen.JPG" width="200"></td>
    <td><img src="Assets/RequestsScreen(Add).JPG" width="200"></td>
  </tr>
</table>

### 📲 Screen

- **View Requests** – Displays rental inquiries submitted for a selected property
- **Add Request** – Capture name, contact, and inquiry notes from interested tenants

### 🔧 CRUD Operations

- ✅ **Create** → Submit a new room inquiry  
- 📖 **Read** → View all rental requests for a property  
- 📝 **Update** → (Planned) Update request status or details  
- ❌ **Delete** → (Planned) Remove closed or invalid requests

## 4) Tenants:

Manage tenant details directly within the mobile app.

<table>
  <tr>
    <td><img src="Assets/TenantsScreen.JPG" width="200"></td>
    <td><img src="Assets/TenantsScreen(Add).JPG" width="200"></td>
  </tr>
</table>

### 📲 Screen

- **View Tenants** – Displays all active tenants.
- **Add Tenant** – Input tenant name, contact info, room number, and check-in date

### 🔧 CRUD Operations

- ✅ **Create** → Add a new tenant to a room  
- 📖 **Read** → View tenant list for a property  
- 📝 **Update** → Update tenant details  
- ❌ **Delete** → Mark tenant as vacated or remove record

## 5) Bookings:

Track and manage room bookings for properties directly within the mobile app.

<table>
  <tr>
    <td><img src="Assets/BookingsScreen.JPG" width="200"></td>
    <td><img src="Assets/BookingsScreen(Add).JPG" width="200"></td>
  </tr>
</table>

### 📲 Screen

- **View Bookings** – Lists all current and past room bookings for a property
- **Add Booking** – Select room and enter tenant details along with check-in/check-out dates

### 🔧 CRUD Operations

- ✅ **Create** → Record a new booking for a room  
- 📖 **Read** → View all bookings under a property  
- 📝 **Update** → Modify booking dates or details  
- ❌ **Delete** → Cancel or archive a booking



The settings icon ⚙️ at the bottom-right provides access to configuration and future customization options.

This modular approach ensures each function is logically grouped, enabling a user-friendly experience for non-technical users like landlords and rental agents.

## ⚙️ Backend: FastAPI Services

The backend is built using **FastAPI**, serving as the core middleware for handling RESTful API requests between the Android app, PostgreSQL, and Kafka.

---

### 🧩 Service 1: Android App ↔ PostgreSQL

This FastAPI script handles all database interactions and core business logic:

- CRUD operations for properties, rooms, tenants, bookings, and payments  
- Data validation and serialization  
- Request/response schema handling using **Pydantic**  
- PostgreSQL connection management using **SQLAlchemy**

📄 **Script:** [app_postgres_service.py](Backend/app_postgres_service.py)  
This service ensures reliable data persistence for the rental system.

### 🔁 Service 2: Android App ↔ Kafka (Confluent Platform)

This FastAPI service connects the Android app to Confluent Kafka using **ksqlDB queries** to serve real-time operational metrics through REST APIs.

- Serves live stats like room vacancies and inquiry counts using ksqlDB queries  
- Powers the "My Business" dashboard in the Android app  
- Uses HTTP-based integration with **Confluent ksqlDB REST API**  
- Provides endpoints to fetch daily, monthly, and current metrics from Kafka streams

📄 **Script:** [app_kafka_metrics_service.py](Backend/app_kafka_metrics_service.py)  
This approach allows your app to consume Kafka stream data without needing a direct Kafka consumer — simplifying real-time integration using HTTP.

## 🗄️ Storage: PostgreSQL

The **PostgreSQL** database is the primary data store for RentLok, supporting persistent, consistent, and structured storage of all rental business operations. It manages properties, rooms, tenants, bookings, payments, and inquiry requests submitted through the Android app. Every change to the business is captured as a structured record in these normalized tables.

### 🧩 ERD Diagram

<div align="center">
  <img src="Assets/DataModel.png" width="650">
</div>

### 🗃️ Database Tables Overview

| Table Name     | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `properties`   | Stores property-level details like name, address, total rooms, and owner ID |
| `rooms`        | Lists rooms per property with floor info, type, rent, and status            |
| `tenants`      | Stores tenant details like name, phone number, and profile description      |
| `bookings`     | Tracks active room bookings by linking tenants, rooms, and properties       |
| `payments`     | Stores rent payment records, status, amount, and related booking info       |
| `requests`     | Captures property inquiry requests from new or prospective tenants          |


























## Stay Tuned still work in progress.




