# Vendor Management System

This is a Django-based Vendor Management System that handles vendor profiles, tracks purchase orders, and calculates vendor performance metrics. 

## Features
- User registration and profiles
- Vendor profiles and job posting capabilities
- Application tracking system
- Notifications and alerts
- Performance metrics: on-time delivery rate, quality rating average, average response time, and fulfillment rate.

## Setup

### Prerequisites

- Python 3.12 or later
- Django 5.0.6
- Virtual environment tool (optional but recommended)
- Node.js and npm (if using React for the frontend)

### Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/vendor_management.git
    cd vendor_management
    ```

2. **Set up a virtual environment**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**

    ```bash
    python manage.py runserver
    ```

## Running Tests

### Setting Up for Testing

1. **Install testing dependencies**

    Make sure you have `pytest` and `pytest-django` installed. You can install them via pip:

    ```bash
    pip install pytest pytest-django
    ```

2. **Create a `pytest.ini` file**

    Create a `pytest.ini` file in the root directory of the project:

    ```ini
    [pytest]
    DJANGO_SETTINGS_MODULE = vendor_management.settings
    python_files = tests.py test_*.py *_tests.py
    ```

3. **Ensure your test directory structure**

    Make sure your tests are structured properly within the `vendors` app:

    ```
    vendor_management/
        manage.py
        vendor_management/
            __init__.py
            settings.py
            urls.py
            wsgi.py
        vendors/
            __init__.py
            admin.py
            apps.py
            models.py
            serializers.py
            urls.py
            views.py
            tests/
                __init__.py
                test_models.py
                test_serializers.py
                test_views.py
    ```

4. **Running the tests**

    Run the tests using `pytest`:

    ```bash
    pytest
    ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [your email@example.com](mailto:your email@example.com).
