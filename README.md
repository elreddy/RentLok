# 📱 RentLok: Rental Management System

**RentLok** is a smart rental management solution designed to streamline the day-to-day operations of property managers. It enables easy tracking of rooms, bookings, payments, and tenant details through a modern Android mobile app backed by a robust data pipeline using PostgreSQL and Confluent Kafka.

This project demonstrates a real-time, event-driven architecture where property and room data is captured through a mobile app, stored in PostgreSQL, and processed asynchronously via Kafka. FastAPI serves as the middleware to connect the app with the database and Kafka topics.

---

## ✅ Features

### 📲 Mobile App for Property Owners to:
- Add and manage **room/property details**
- Log **inquiries** and monitor **room availability**
- Record **tenant bookings** and **payment history**

### 🛠️ PostgreSQL
- Acts as the **central transactional database**
- Stores all core rental and operational data

### 🔄 Confluent Kafka
- Enables **real-time messaging and event handling**
- Powers asynchronous data processing between services

### ⚡ FastAPI
- Serves as a **lightweight backend API**
- Ingests data from the mobile app and streams events to Kafka

---

Stay tuned for:
- 🔧 System Architecture Diagram
- 🚀 Setup & Deployment Instructions
- 📡 Kafka Stream/Table Definitions
- 📲 Android App Screenshots and Usage Guide
