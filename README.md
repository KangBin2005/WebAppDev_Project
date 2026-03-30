🏥 PWID Support & Integrated Management System

> **A dual-sided Flask Web Application empowering Persons with Intellectual Disabilities (PWID) and streamlining social service operations.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap-purple.svg)
![Chart.js](https://img.shields.io/badge/Charts-Chart.js-green.svg)
![Shelve](https://img.shields.io/badge/Database-Shelve-orange.svg)

## 🌟 Project Overview

This platform was developed for **SG Enable**, an agency in Singapore that supports Persons with Intellectual Disabilities (PWIDs) through skills training, job coaching, and community services. The web application bridges the gap in community support by offering:

- A simplified **Public/Participant Portal** for service engagement.
- A robust **Staff Management Suite** for data‑driven administration.

The solution centralises activities, enquiries, transactions, and analytics, making it easier for PWIDs, caregivers, and staff to connect and manage services efficiently.

---

## ✨ Core Features

### 👥 Participant & Public Portal (`PWID&Public_directory.py`)
- **Activity Discovery** – Browse and register for workshops/activities with **Accessibility Needs** tracking.
- **Integrated Enquiry System** – Submit support tickets (as public or registered member) and track real‑time resolution status.
- **Secure Account Management** – Role‑specific access (PWID, Caregiver, Member) with profile editing, password recovery, and secure login.
- **Inactivity Protection** – 10‑minute session timeout (`PERMANENT_SESSION_LIFETIME`) to protect sensitive user information.

### 🏢 Staff Administrative Portal (`Staff_directory.py`)
- **Centralized Dashboard** – Manage user accounts, public activities, and participant workshops.
- **Financial Tracking** – Transaction system to log sales and services with multi‑payment support (Debit, Credit, Digital, Apple Pay).
- **Enquiry Management** – Review, reply, and archive community feedback through a centralised interface.
- **Sync ID Protocol** – Custom logic that synchronises auto‑incrementing IDs across multiple `.db` files, ensuring data consistency.
- **Data Analytics Dashboard** – Real‑time visualisation using **Chart.js** to track activity participation (bar charts) and categorise enquiry trends (pie charts) for both public and registered users.
---

## 🛠️ Technical Architecture

### Tech Stack
* **Backend:** Python / Flask
* **Frontend:** Jinja2 Templates, Bootstrap 5, CSS3
* **Persistence:** `shelve` (Object-oriented persistent storage)
* **Form Logic:** WTForms with advanced data validation (Email, Length, and Required Fields).

### Persistence Layer
The system uses a modular storage approach. Each module (Accounts, Enquiries, Transactions) is stored in its own `.db` file within the `storage/` directory. The `shelve` module is used with `writeback=True` for reliable updates

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
# Run the Public/Participant portal
python "PWID&Public_directory.py"
```

# Staff portal (Port 5001)
This handle administrative functions for staffs.
```bash
# Run the Staff portal
python "Staff_directory.py"
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
