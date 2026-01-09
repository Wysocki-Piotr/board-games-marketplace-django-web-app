##  How to Run Locally

Follow these steps to get the project up and running on your local machine.

### 1. Prerequisites
Ensure you have the following installed:
* [Python](https://www.python.org/downloads/) (version 3.8 or higher)
* [Git](https://git-scm.com/)

### 2. Clone the Repository
Open your terminal and run:

```bash
git clone https://github.com/Wysocki-Piotr/board-games-marketplace-django-web-app.git
cd boardgame-market
```

### 3. Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
For MacOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
python -m pip install django djangorestframework django-filter pillow
```

### 5. Apply database migrations
```bash
python manage.py migrate
```

### 5. Create administrator (optional)
```bash
python manage.py createsuperuser
```

### 5. Run server
```bash
python manage.py runserver
```

### You should see webpage at URL:
http://127.0.0.1:8000/

