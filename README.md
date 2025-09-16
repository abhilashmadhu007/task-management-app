# Task Management Application with Completion Reports

## 📌 Project Overview
This is a **Task Management Application** built with **Python (Django + Django REST Framework)**.  
It allows Users, Admins, and SuperAdmins to manage tasks efficiently with the following features:
- Task assignment and status tracking
- Completion reports with worked hours
- Role-based access control (User, Admin, SuperAdmin)
- Secure authentication using **JWT (JSON Web Tokens)**

This project is designed for **company-level task management**, ensuring accountability and transparency.

---

## 🚀 Features

### 👤 User
- View assigned tasks
- Mark tasks as **Completed**
- Submit **Completion Report** & **Worked Hours**

### 👨‍💼 Admin
- Assign tasks to their users
- View & manage tasks assigned to their users
- View **Completion Reports** from their users
- Cannot manage user roles

### 🏆 SuperAdmin
- Manage all Admins and Users (create, update, delete, assign roles)
- Assign users to Admins
- View & manage all tasks across the system
- View all task completion reports

---

## 🛠️ Tech Stack
- **Backend:** Python, Django, Django REST Framework
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Frontend (Admin Panel):** Django Templates (HTML, CSS, Bootstrap)

---

## ⚙️ Installation & Setup 

```bash
# Clone repository
git clone https://github.com/yourusername/task-management-app.git
cd task-management-app

# Create virtual environment and activate
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Assign SuperAdmin role via shell
python manage.py shell
from app.models import User
user = User.objects.get(username="your_superuser_name")
user.role = "SuperAdmin"
user.save()

# Run server
python manage.py runserver
```
## 📡 API Endpoints

### 🔑 Authentication & Task Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/token/` | Obtain JWT access & refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh access token |
| `GET`  | `/api/tasks/` | Get all tasks for the logged-in user |
| `PUT`  | `/api/tasks/<id>/` | Update a task (mark as Completed with completion report & worked hours) |
| `GET`  | `/api/tasks/<id>/report/` | View completion report & worked hours (only for Completed tasks, accessible by Admin & SuperAdmin) |

---

**Example: Obtain Token**
```http
POST /api/token/
Content-Type: application/json
```
**Request Body:**
```http
{
  "username": "your_username",
  "password": "your_password"
}
```
Response:
```http
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```
⚡ Every protected request must include:
```http
Authorization: Bearer your_access_token
content-type: application/json
```



