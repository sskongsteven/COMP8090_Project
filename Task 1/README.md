# Resource Booking System

## Overview
This project is an Object-Oriented Programming (OOP) application built in Python. This is a booking system where students can reserve rooms and equipment, and staff can manage the inventory and track student bookings. The application has a Graphical User Interface (GUI) built with Tkinter, and also a backup console-based version.

## Features
* **Role-Based Access:** Separate students and staff with different menu and functions.
* **Resource Management:** All users can view available and borrowed rooms/equipment.
* **Booking & Returning:** Students can make bookings, and staff can process returns.
* **Inventory Management:** Staff can add new rooms and equipment to the system.

## Project Structure
* `gui.py` - The main file to launch the Graphical User Interface.
* `bookingSystem.py` - The core backend logic with console version interface.
* `user.py` - Contains the `User` parent class and `Student`/`Staff` child classes.
* `resource.py` - Contains the `Resource` parent class and `Room`/`Equipment` child classes.
* `notification.py` - Handles generating booking receipts.
* `utils.py` - Handles time tracking for bookings.

## Prerequisites
* Python 3.x
* Tkinter

## How to Run the Application
1. Download or clone this repository to your local machine.
2. Ensure the `Data` folder is in the same directory with the other Python modules.
3. To run the GUI version, run the 'gui.py'
4. To run the console version, run the 'bookingSystem.py'

## Test Login Credentials
You can use the following credentials to test the system:

1. Student Account:

* User ID: S001

* Password: Spassword123


2. Staff Account:

* User ID: T001

* Password: Apassword123