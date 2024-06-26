# Vendor Management System

This is a Django-based Vendor Management System that handles vendor profiles, tracks purchase orders, and calculates vendor performance metrics. 

## Features
- Vendor Profile Management
- Purchase Order Tracking
- Vendor Performance Evaluation
- Vendor Performance Metrics Calculation
- Vendor Performance Report Generation


## Setup

### Prerequisites

- Python 3.12
- Django 5.0.6
- Django REST Framework 3.15.1

### Installation

1. **Clone the repository**

    ```bash
    https://github.com/python-monster08/assignment.git
    cd vendor_management
    ```

2. **Set up a virtual environment**

    ```bash
    python -m venv env
    source env/bin/activate  # On MacOs and linux
    env\Scripts\activate     # On Windows
    ```

3. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**

    ```bash
    python manage.py createsuperuser

    username : admin
    password : 1234
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

2. **Create a `pytest.ini` file inside root directory**

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

For any inquiries, please contact [kamleshlovewanshi2000@gmail.com](mailto:kamleshlovewanshi2000@gmail.com).
