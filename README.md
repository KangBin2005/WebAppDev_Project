# 🏥 PWID Support & Integrated Management System
> **A dual-sided Flask Web Application empowering Persons with Intellectual Disabilities (PWID) and streamlining social service operations.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap-purple.svg)
![Shelve](https://img.shields.io/badge/Database-Shelve-orange.svg)

## 🌟 Project Overview
This platform addresses the gap in community support for PWID and their caregivers. It features a simplified **Public/Participant Portal** for service engagement and a robust **Staff Management Suite** for data-driven administration.

---

## ✨ Core Features

### 👥 Participant & Public Portal (`PWID&Public_directory.py`)
* **Activity Discovery:** Browse and register for activities with specialized **Accessibility Needs** tracking.
* **Integrated Enquiry System:** Submit support tickets (Public or Member) and track real-time resolution status.
* **Secure Account Management:** Role-specific access (PWID, Caregiver, Member) with profile editing and password recovery.
* **Inactivity Protection:** 10-minute session timeout (`PERMANENT_SESSION_LIFETIME`) to protect sensitive user information.

### 🏢 Staff Administrative Portal (`Staff_directory.py`)
* **Centralized Dashboard:** Management of accounts, public activities, and participant workshops.
* **Financial Tracking:** A dedicated **Transaction System** to log sales and services with multi-payment support (Debit, Credit, Digital).
* **Enquiry Management:** Staff-side interface to review, reply to, and archive community feedback.
* **Sync ID Protocol:** Custom logic to synchronize auto-incrementing IDs across multiple `.db` files, ensuring data consistency.
* **Data Analytics Dashboard:** Real-time visualization using **Chart.js** to track activity participation (Bar Charts) and categorize enquiry trends (Pie Charts) for both Public and Registered users.

---

## 🛠️ Technical Architecture

### Tech Stack
* **Backend:** Python / Flask
* **Frontend:** Jinja2 Templates, Bootstrap 5, HTML, CSS, Chart.JS
* **Persistence:** `shelve` (Object-oriented persistent storage)
* **Form Logic:** WTForms with advanced validation (Email, length constraints, and custom error messages)

### Persistence Layer
The system uses a modular storage approach. Each module (Accounts, Enquiries, Transactions) is stored in its own `.db` file within the `storage/` directory, managed via the `shelve` module with `writeback=True` for reliable updates.

---

## 🌟 Project Overview
This platform addresses the gap in community support for PWID and their caregivers. It features a simplified **Public/Participant Portal** for service engagement and a robust **Staff Management Suite** for data-driven administration and operational tracking.

---

## ✨ Core Features

### 👥 Participant & Public Portal (`PWID&Public_directory.py`)
* **Activity Discovery:** Browse and register for workshops with specialized **Accessibility Needs** tracking.
* **Unified Enquiry System:** Submit support tickets (Public or Member) and track real-time resolution status.
* **Secure Account Management:** Role-specific access (PWID, Caregiver, Member) with profile management and password recovery.
* **Inactivity Protection:** 10-minute session timeout (`PERMANENT_SESSION_LIFETIME`) to ensure the privacy of vulnerable users.

### 🏢 Staff Administrative Suite (`Staff_directory.py`)
* **Operations Dashboard:** Manage user accounts, public activities, and internal participant workshops.
* **Transaction System:** Track product sales and service logs with multi-payment support (Debit, Credit, Apple Pay, etc.).
* **Enquiry Lifecycle:** Review, reply to, and archive community feedback through a centralized staff interface.
* **Sync ID Protocol:** Custom synchronization logic that prevents ID collisions by fetching the highest existing ID across multiple `.db` storage files.

---

## 🛠️ Technical Architecture

### Tech Stack
* **Backend:** Python / Flask
* **Frontend:** Jinja2 Templates, Bootstrap 5, CSS3
* **Persistence:** `shelve` (Object-oriented persistent storage)
* **Form Logic:** WTForms with advanced data validation (Email, Length, and Required Fields).

### Database Strategy
The system uses a modular storage approach. Each data type is isolated in its own `.db` file within the `storage/` directory, utilizing the `writeback=True` protocol for reliable object updates and data persistence.

---
## 🚀 Installation & Setup

### 1. Prerequisites
* Python 3.8+
* `pip` (Python package manager)

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/yourusername/pwid-support-system.git](https://github.com/yourusername/pwid-support-system.git)
cd pwid-support-system

# Install dependencies
pip install flask wtforms wtforms[email]

# Ensure the storage directory exists
mkdir storage

```
---

### 🏃 3. Running the Application
Every time you work on the project, ensure you follow these steps to start the correct portal.

### Main Portal (Port 5000)
This handles public activity sign-ups and participant accounts.

```bash
# Activate virtual environment
# Windows: venv\Scripts\activate.bat 
# Mac/Linux: source venv/bin/activate

# Run the Public/Participant portal
python "PWID&Public_directory.py"
```
---

## 📂 Project Structure
| File / Directory | Role |
| :--- | :--- |
| `PWID&Public_directory.py` | Main entry point for the Public and Registered Members portal. |
| `Staff_directory.py` | Main entry point for Administrative and Staff Dashboard functions. |
| `Forms.py` | Unified WTForm definitions for Activities, Enquiries, and Transactions. |
| `Account.py` | Class model for User profiles, roles, and ID management. |
| `Transaction.py` | Logic for processing and storing payment/sale data. |
| `Product.py` | Class model for managing inventory and items. |
| `Participant_Activity.py` | Class for defining workshop and activity parameters. |
| `Activity_public.py` | Class model for community-wide public events. |
| `Participant_Enquiry.py` | Logic for handling registered member support tickets. |
| `Public_Enquiry.py` | Logic for handling non-member support tickets. |
| `storage/` | Local directory for persistent `.db` files (Shelve persistence). |

---

## 🔒 Testing Credentials
Use these pre-configured accounts to test the different access levels of the system:

### 🏢 Staff Accounts (Dashboard Access)
* **Bob:** `password`
* **Mary:** `password123`

### 👥 Participant Accounts (Portal Access)
* **Amy:** `password`
* **Karl:** `karl123`
* **Julie:** `password123`

---
