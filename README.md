

# eLearning Platform Project

## Project Overview

This eLearning platform is designed to provide a comprehensive environment for both students and teachers to engage in educational activities online. It features course listings, user authentication, profile management, and more, all built with Django.

## Key Features

- **User Authentication**: Support for user registration, login, and logout.
- **Profile Management**: Users can view and edit their profiles, including changing passwords and uploading avatars.
- **Course Management**: Teachers can create and manage courses, while students can browse the course listings and enroll in courses of their interest.
- **Dynamic Home Page**: Displays available courses and user-specific information based on their role (student or teacher).
- **Modern UI**: A clean and responsive user interface with Bootstrap integration for a seamless experience across devices.

## Tech Stack

- **Backend**: Django 5.0.2
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Database**: SQLite (development), adaptable to PostgreSQL or MySQL for production
- **Deployment**: (This section can be updated based on where and how you plan to deploy, e.g., Heroku, AWS, etc.)

## Setup and Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourgithubusername/eLearning-platform.git
cd eLearning-platform
```

2. **Create and Activate Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Run the Development Server**

```bash
python manage.py runserver
```

## Usage

- Visit `http://127.0.0.1:8000/` in your browser to view the home page.
- Access the admin panel at `http://127.0.0.1:8000/admin` with superuser credentials.
- Register as a new user or login with existing credentials to explore user-specific features.

## Development Progress

- [x] User authentication system implemented with custom user model.
- [x] Dynamic home page showing courses based on user status (enrolled/not enrolled).
- [x] Profile management including avatar upload and password change.
- [ ] Course creation and enrollment functionality (in progress).
- [ ] Implement advanced features like quizzes, forums, and progress tracking (planned).

## Contributing

We welcome contributions! Please follow the [GitHub flow](https://guides.github.com/introduction/flow/) for submitting pull requests to this project.

## License

This project is licensed under the [MIT License](LICENSE.txt) - see the LICENSE file for details.

