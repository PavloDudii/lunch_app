# test_task_inforce

## Clone the Repository

```bash
git clone https://github.com/...
cd your_project_folder
```
## Local Setup

Install PostgreSQL

Guide: https://www.postgresql.org/download/

Create and activate a virtual environment

```bash
python -m venv venv

# Linux / MacOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

## Install dependencies
```bash
pip install -r requirements.txt
pip install -r dev_requirements.txt
```

## Apply migrations
```bash 
python manage.py makemigrations
python manage.py migrate
```

## Run the server
```bash 
python manage.py runserver
```

## Run with Docker
```bash
docker-compose build
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py migrate"
docker-compose up
```

### Server will be available at http://localhost:8000

### Create superuser: 
```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```
### Run tests
```bash
docker-compose run --rm app sh -c pytest
```

### Use linting tool (flake8)
```bash
docker-compose run --rm app sh -c flake8
```

# API Endpoints

___

# /api/user/
 
### POST	 /register/	-> User registration
### POST	/login/	->  Obtain JWT tokens
### POST	/token/refresh -> Refresh access token
___

# /api/menus/

### GET	/ -> List all menus
### POST	/	-> Create a new menu (staff only)
### PUT	/id/	-> Update a menu
### DELETE	/id/	-> Delete a menu
### GET	/today_menu/ -> Get today's menu
### GET	/today_rating/ -> Get today's menu rating
### POST	/vote/	-> Vote for a menu
___

# /api/restaurants/

### GET	/ ->	List all restaurants
### POST	/ ->	Create a new restaurant
### GET	/id/ ->	Retrieve a specific restaurant
### PUT	/id/ ->	Update a restaurant
### DELETE	/id/ ->	Delete a restaurant

___
