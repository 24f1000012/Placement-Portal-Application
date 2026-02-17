# Placement Portal Application

## 📌 Project Overview
The Placement Portal Application is a web-based system designed to streamline and manage campus placement activities within an institute. It provides a centralized platform for the Institute Placement Cell (Admin), Companies, and Students to interact efficiently during the recruitment process.

The application eliminates manual processes such as spreadsheets and emails by offering role-based access, automated approval workflows, and complete placement history tracking.

---

## 🎯 Objectives
- To manage company registrations and placement drives efficiently
- To allow students to apply for placement drives in a structured manner
- To provide the placement cell with complete control and visibility over placement activities
- To maintain accurate application and placement history

---

## 👥 User Roles
### 1. Admin (Institute Placement Cell)
- Pre-existing superuser
- Approves/rejects company registrations
- Approves/rejects placement drives
- Manages students, companies, drives, and applications
- Views complete placement statistics and history

### 2. Company
- Registers and creates a company profile
- Creates placement drives after admin approval
- Views student applications
- Shortlists and updates application status

### 3. Student
- Registers and manages profile
- Views approved placement drives
- Applies for placement drives
- Tracks application status and placement history

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** Jinja2, HTML, CSS, Bootstrap
- **Database:** SQLite (programmatically created)
- **Authentication:** Flask-Login
- **Version Control:** Git & GitHub

---

## 🗄️ Database
- SQLite database created automatically using SQLAlchemy
- No manual database creation tools are used
- Core tables include:
  - Admin
  - Student
  - Company
  - Placement Drive
  - Application

---

## 🔐 Authentication & Security
- Role-based authentication system
- Admin account is pre-seeded in the database
- Secure password hashing using Werkzeug
- Restricted access based on user roles

---

## 🚀 How to Run the Project Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/24f1000012/Placement-Portal-Application.git
