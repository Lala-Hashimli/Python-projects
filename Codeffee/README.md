# Codeffee

**Codeffee** is a console-based coffee shop ordering system developed in Python. It allows users to log in, view food and drink menus, manage their basket, and make payments — simulating a real coffee shop experience.

## Project Structure

Codeffee/
├── accounts/             # User account management (balance, password, etc.)
├── basket/               # Shopping basket functions
├── drinks/               # Drink menu & stock
├── foods/                # Food menu & stock
├── receipt/              # Receipt generator & purchase logging
├── private\_data/         # Contains users.json and basket\_db.json (gitignored)
├── main.py               # Application entry point
├── config.py             # App configuration and constants
├── README.md             # Project overview (this file)
├── .gitignore            # Files and folders ignored by Git

## Features

- 🔐 **User authentication** (Sign In / Log In)
- 🥤 **Drink Menu** (Hot, Cold, Frappuccino, etc.)
- 🍽️ **Food Menu** (Breakfast, Bakery, Lunch, etc.)
- 🛒 **Basket system** with add/remove logic
- 💳 **Payment system** with balance check
- 🧾 **Receipt generation** and order history
- 📊 Admin functions (view stats, manage menu)
