*🚆 Railway Reservation Management System*

**A full-stack web-based Railway Reservation System built using Flask and SQLite, allowing users to view trains, book tickets, manage bookings, and generate digital tickets.**

📌 Project Overview

This project simulates a real-world railway booking platform where users can:

Register and log in securely

View available trains with arrival & departure timings

Book tickets

View booking history

Cancel tickets

Generate digital ticket receipts

The system demonstrates backend logic, database integration, and dynamic frontend rendering.

✨ Features

🔐 User Authentication (Signup/Login)

🚆 Train Listing with Arrival & Destination Timing

🎫 Ticket Booking & Cancellation

📜 Booking History Section

🧾 Dynamic Ticket Generation

💾 SQLite Database Integration

🎨 Responsive UI using HTML & CSS

🛠️ Tech Stack

Backend: Python, Flask

Frontend: HTML, CSS

Database: SQLite

Authentication: Werkzeug (Password Hashing)

Hosting: PythonAnywhere

🗄️ Database Structure

**Users Table**

id

username

email

password (hashed)

**Trains Table**

id

train_name

source

destination

arrival_time

departure_time

**Bookings Table**

id

user_id

train_id

booking_date

ticket_number
