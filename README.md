# Workspace Management System (Django REST Framework)

## 📌 Overview

The **Workspace Management System** is a backend application built using **Django REST Framework (DRF)** that enables structured collaboration through a hierarchical model:

* **Workspace → Projects → Tasks**

It supports **role-based access control**, **JWT authentication**, and scalable API features such as filtering, pagination, and throttling.

---

## 🚀 Features

### 🏢 Hierarchical Structure

* **Workspace**

  * Top-level entity representing an organization or team space
* **Projects**

  * Created within a workspace
* **Tasks**

  * Managed within projects

---

### 🔐 Authentication

* JWT-based authentication using secure token handling
* Stateless and scalable authentication mechanism

---

### 👥 Role-Based Access Control (RBAC)

The system implements multi-level roles:

#### 1. Organization-Level Roles

* Define top-level authority across the system

#### 2. Workspace-Level Roles

* Control access and permissions within a workspace

#### 3. Project-Level Functional Roles

* Roles like:

  * Developer
  * Tester
  * QA
* Fine-grained control over project-specific actions

---

### 🛡️ Permissions System

* Custom permission classes implemented using DRF
* Permissions enforced based on:

  * User role
  * Resource ownership
  * Context (workspace/project/task)

---

### ⚙️ API Features

* **Pagination**: Efficient handling of large datasets
* **Filtering**: Query-based filtering for better data retrieval
* **Throttling**: Rate limiting to prevent abuse
* **Optimized Queries**: Use of `.select_related()` and `.only()` for performance

---

### 🔗 Model Relationships

* **Workspace ↔ Users** (Many-to-Many via WorkspaceUser)
* **Project ↔ Users** (Many-to-Many via ProjectUser)
* **Workspace → Projects → Tasks** (Hierarchical ForeignKey relationships)

---

## 🏗️ Tech Stack

* **Backend**: Django, Django REST Framework
* **Authentication**: JWT (JSON Web Tokens)
* **Database**: PostgreSQL / SQLite (configurable)
* **API Tools**:

  * DRF Serializers
  * Generic Views / APIViews
  * Custom Permissions

---

## 📂 Project Structure (Simplified)

```
company_app/
│── models/
│   ├── workspace.py
│   ├── project.py
│   ├── task.py
│   ├── workspace_user.py
│   ├── project_user.py
│
│── api/
│   ├── views/
│   ├── serializers/
│   ├── permissions/
│   ├── urls.py
│
│── services/
│── utils/
```

---

## ⚡ Key Functionalities

* Create and manage workspaces
* Assign users to workspaces and projects
* Role-based task assignment and control
* Secure API access using JWT
* Fine-grained permission validation across all endpoints

---

## 🧪 API Capabilities

* CRUD operations for:

  * Workspaces
  * Projects
  * Tasks
* User-role assignment APIs
* Permission-protected endpoints
* Query-based filtering and pagination support

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/06kunal/WorkspaceGovernance.git
cd WorkspaceGovernance
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Run the server

```bash
python manage.py runserver
```

---

## 🔑 Authentication Flow

1. User logs in → Receives JWT token
2. Token is passed in headers:

```
Authorization: Bearer <your_token>
```

3. Access is granted based on role + permissions

---

## 📈 Future Improvements

* Frontend integration (React / Next.js)
* Real-time notifications (WebSockets)
* Activity logs and audit trails
* File attachments in tasks
* Role management dashboard

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📬 Contact

For any queries or collaboration:

* GitHub: https://github.com/06kunal

---

## ⭐ Acknowledgment

This project demonstrates backend system design with:

* Scalable architecture
* Clean permission handling
* Real-world collaboration workflows

---
