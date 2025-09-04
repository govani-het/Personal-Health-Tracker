<div align="center">

# HealthHub: Your Personal Health & Fitness Tracker ⚕️

<p>
  <strong>A web-based health management system built with Python (Django), JavaScript, and PostgreSQL ORM.
This project helps users track their nutrition, workouts, and reminders in a simple and structured way.</strong>
</p>

<!-- Badges -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-4.2%2B-darkgreen.svg?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-14-blue.svg?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JavaScript-ES6%2B-yellow.svg?logo=javascript&logoColor=white" alt="JavaScript">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

</div>

<!-- Project Demo GIF/Image -->
<div align="center">
  <!-- ⚠️ IMPORTANT: Replace this with a GIF or screenshot of your project -->
  <img src="https://via.placeholder.com/800x450.png?text=HealthHub+Project+Demo+GIF" alt="Project Demo" style="border-radius: 8px;">
</div>

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [💡 Future Improvements](#-future-improvements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📧 Contact](#-contact)

---

## 📸 Project Showcase

Here's a glimpse of HealthHub in action.

<div align="center">
<table>
  <tr>
    <td align="center">
      <img width="400"  alt="Screenshot 2025-09-04 171003" src="https://github.com/user-attachments/assets/7ca7dc4a-2c52-4310-97c0-b3262ff3267d" />
      <br>
      <b>Dashboard Overview</b>
    </td>
    <td align="center">
      <img width="400" alt="Screenshot 2025-09-04 171012" src="https://github.com/user-attachments/assets/07b69332-5e8b-48a9-8e92-8778f89b5bd3" />
      <br>
      <b>Meal Logging</b>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img width="400" alt="Screenshot 2025-09-04 171032" src="https://github.com/user-attachments/assets/69f51c80-277b-4d40-ac48-05ee0b779a7b" />
      <br>
      <b>Setting Page</b>
    </td>
    <td align="center">
      <img width="400" alt="Screenshot 2025-09-04 171159" src="https://github.com/user-attachments/assets/7d12c2e4-517a-4139-bd23-8caaef59b901" />
      <br>
      <b>Personalized Profile Setup</b>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img width="400" alt="Screenshot 2025-09-04 111438" src="https://github.com/user-attachments/assets/0e0f8b97-1ff2-4181-855e-4708ea521228" />
      <br>
      <b>Email Reminders</b>
    </td>
    <td align="center">
      <img width="400" alt="Screenshot 2025-09-04 111552" src="https://github.com/user-attachments/assets/f36b5694-06b2-4ab7-8619-da2e82bf03be" />
      <br>
      <b>Secure Login & Registration</b>
    </td>
  </tr>
</table>
</div>

---

## 📖 About The Project

In today's fast-paced world, keeping track of personal health can be a challenge. **HealthHub** is a web-based solution designed to simplify this process. It provides a user-friendly platform for individuals to monitor their daily caloric intake, track their exercise routines, and set important health-related reminders.

This project is a full-stack application that demonstrates proficiency in backend development with **Django**, database management with **PostgreSQL**, and frontend interactions with **JavaScript**. It features a secure authentication system, a personalized user experience, and a clean, intuitive dashboard.

---

## ✨ Key Features

-   🔐 **Secure User Authentication:** Users can register, log in, and securely reset their passwords using an OTP (One-Time Password) system sent via email.
-   👤 **Personalized User Profiles:** On first login, users are guided through a profile setup to enter personal metrics like age, weight, height, and health goals, which are used to personalize their experience.
-   📊 **Interactive Dashboard:** A central hub that provides a quick overview of the user's daily progress, including calories consumed and burned.
-   🥗 **Meal Tracking:** Easily add meals (breakfast, lunch, dinner, snacks) and instantly see a breakdown of calories, protein, carbohydrates, and fat consumed.
-   🏋️ **Exercise Logging:** Log various physical activities to track the number of calories burned, helping users stay on top of their fitness goals.
-   📧 **Email Reminders:** Set custom reminders for workouts, meals, or water intake, and receive timely notifications directly in your email inbox.

---

## 🛠️ Tech Stack

This project is built using a modern and robust tech stack:

| Technology | Description |
| :--- | :--- |
| **Backend** | `Python`, `Django`, `Django ORM` |
| **Database** | `PostgreSQL` |
| **Frontend** | `HTML5`, `CSS3`, `JavaScript` |
| **Authentication** | `JWT Token`, `Custom OTP System` |
| **Email** | `SMTP (Simple Mail Transfer Protocol)` |

---

## 📁 Project Structure

The repository is organized following Django's standard project layout to ensure maintainability and scalability.

```
djnagoProject/
├── djangoProject/            # Main Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py             # Celery configuration for async tasks
│   ├── settings.py           # Project settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py
├── exercise/                 # Django app for managing exercises
├── nutrition/                # Django app for tracking meals
├── reminder/                 # Django app for handling reminders
├── user/                     # Django app for user authentication & profiles
├── suggestion/               # Django app for health suggestions
├── static/                   # Global static files (CSS, JS, Images)
├── templates/                # Global HTML templates
├── .env                      # Environment variables (not committed)
├── .gitignore                # Git ignore file
├── manage.py                 # Django's command-line utility
└── requirements.txt          # Python dependencies
```

---

## 🚀 Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

Make sure you have the following installed on your system:
-   Python 3.10+
-   Git
-   PostgreSQL Server

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/govani-het/Personal-Health-Tracker.git
    cd Personal-Health-Tracker
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up the PostgreSQL Database:**
    -   Create a new database in PostgreSQL (e.g., `healthhub_db`).
    -   Create a new user with a password and grant it permissions to the new database.

5.  **Configure Environment Variables:**
    -   Create a `.env` file in the root directory of the project.
    -   Copy the contents of a `.env.example` file (if provided) or add the following variables:
    ```env
    SECRET_KEY='your-django-secret-key'
    DEBUG=True

    DB_NAME='healthhub_db'
    DB_USER='your_db_user'
    DB_PASSWORD='your_db_password'
    DB_HOST='localhost'
    DB_PORT='5432'

    EMAIL_HOST='smtp.gmail.com'
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER='your-email@gmail.com'
    EMAIL_HOST_PASSWORD='your-app-password' # Use a Google App Password
    ```
    *Note: You may need to generate an "App Password" for Gmail if you have 2FA enabled.*

6.  **Apply database migrations:**
    ```sh
    python manage.py migrate
    ```

7.  **Create a superuser to access the admin panel:**
    ```sh
    python manage.py createsuperuser
    ```

8.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

---

## 💡 Future Improvements

HealthHub is an ongoing project with many potential enhancements. Here are some ideas for the future:

-   [ ] **Data Visualization:** Implement charts and graphs (using Chart.js or D3.js) to visualize user progress over time.
-   [ ] **API Development:** Build a RESTful API using Django Rest Framework to allow for a mobile application.
-   [ ] **Social Features:** Add a friend system to share progress and achievements.
-   [ ] **Third-Party Integrations:** Integrate with fitness trackers like Fitbit or Google Fit to automatically sync data.
-   [ ] **Advanced Reporting:** Generate weekly/monthly health reports for users.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

To contribute:
1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📧 Contact

Het Govani - [LinkedIn](www.linkedin.com/in/het-govani-a58381339) - govanihet09@gmail.com

Project Link: [https://github.com/govani-het/Personal-Health-Tracker](https://github.com/govani-het/Personal-Health-Tracker)
