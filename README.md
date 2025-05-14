# 📱 RentLok: Rental Management System

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
  <img src="DataFlow.JPG" width="550">
</div>


1. **Mobile App** → FastAPI (REST calls)
2. **FastAPI** → PostgreSQL (CRUD operations)
3. **FastAPI** → Kafka (publishing events)
4. **Kafka** → Mobile App (real-time updates via consumer)


Stay tuned for:
- 🚀 Setup & Deployment Instructions
- 📡 Kafka Stream/Table Definitions
- 📲 Android App Screenshots and Usage Guide


