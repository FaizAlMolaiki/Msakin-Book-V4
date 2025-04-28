# Msakin Real Estate Platform

Msakin is a comprehensive real estate management platform built with Django, supporting real-time user interaction.

## Main Features
- Property management: add, edit, delete, view, and upload multiple images.
- Advanced comments and likes system (including nested comments).
- Real-time chat between users (WebSocket support).
- Instant notifications on all user interactions.
- Social follow system between users.
- User account and profile management.
- REST API endpoints for some services.

## Project Structure
```
src/
├── accounts         # User management and profiles
├── chat             # Real-time chat between users
├── home             # Main website pages
├── msakin           # Project settings and routing
├── notifications    # Notification system
├── properties       # Property management, comments, images
├── static           # Static files (CSS, JS)
├── media            # User-uploaded files and images
├── templates        # HTML templates
├── manage.py        # Project management script
├── requirements.txt # Project dependencies
```

---

## Workflow Diagram (User Journey)
Below is a simplified workflow showing how users interact with the main features:

```mermaid
flowchart TD
    A[User Registration/Login] --> B[Browse/Add Properties]
    B --> C[View Property Details]
    C --> D[Like/Comment on Property]
    C --> E[Start Chat with Owner]
    D --> F[Receive Notifications]
    E --> F
    F --> G[Real-time Updates via WebSocket]
    B --> H[Submit Property Request]
    A --> I[Follow Other Users]
    D --> F
```

---

## Project Analysis
Msakin consists of several Django apps:
- **accounts:** User management and profiles
- **properties:** Real estate listings, images, comments, likes, and requests
- **chat:** Real-time messaging between users (WebSocket)
- **notifications:** Real-time notifications for user activities
- **home:** Main website and landing pages
- **media/static/templates:** File storage, static assets, and HTML templates
- **Django Admin:** Admin dashboard for all data management

All apps interact through the Django backend, with users accessing the system via browser (HTTP/REST and WebSocket). Data and files are stored in the database and file storage, and the admin panel provides full management capabilities.

---

## Project Overview Diagram
Below is a high-level diagram showing how all core components interact:

```mermaid
flowchart TD
    User --> Browser
    Browser -->|HTTP/REST| API
    Browser -->|WebSocket| WS
    API --> accounts
    API --> properties
    API --> chat
    API --> notifications
    API --> home
    API --> Admin
    accounts --> DB
    properties --> DB
    properties --> Media
    properties --> Images
    chat --> DB
    notifications --> DB
    home --> Templates
    API --> Static
    API --> Templates
    API --> DB
    API --> Media
    WS --> chat
    WS --> notifications
    Admin --> DB
    Admin --> Media
    Images --> Media
    Static --> static_dir
    Templates --> templates_dir
```

---

## System Architecture Diagram
This diagram shows the high-level architecture and how the main components interact:

```mermaid
flowchart LR
    U1[User Browser] -- HTTP/REST --> ASGI[ASGI Server (Django + Channels)]
    U1 -- WebSocket --> ASGI
    ASGI -- ORM --> DB[(Database)]
    ASGI -- File Upload/Download --> FS[(File Storage)]
```

## Requirements
- Python 3.10+
- Django 4+
- Django Channels
- Pillow
- Django REST Framework

## خطوات التشغيل
1. تثبيت المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```
2. ترحيل قاعدة البيانات:
   ```bash
   python manage.py migrate
   ```
3. إنشاء مستخدم مدير:
   ```bash
   python manage.py createsuperuser
   ```
4. تشغيل السيرفر:
   ```bash
   python manage.py runserver
   ```

## Technical Notes
- The system supports WebSockets for chat and notifications.
- Users and properties can have multiple images.
- The project structure makes it easy to add new features or apps.

## Contributions
To contribute or report issues, please open an issue or pull request.

---

Msakin Real Estate Platform - All rights reserved © 2025
