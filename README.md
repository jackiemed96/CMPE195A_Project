# Smart Planter Flask App

#### Setup & Installation
1. Before beginning, clone repository via SSH or HTTPS at this link:
https://github.com/jackiemed96/CMPE195A_Project

2. Install Python3:
```sudo apt-get install python3```
3. Install Flask and Required Extensions:
```pip install Flask```
```pip install flask-wtf flask-sqlalchemy flask-login```
4. Install Dependencies for reading data from plant file:
```pip install xlrd openpyxl```

#### Creating Plant Database
1. Navigate to the ```smartplanter``` directory
2. Convert Plant information Excel file into SQLAlchemy database
```python3 seed_db.py```

#### Running Flask Application
1. In ```smartplanter``` directory, start Flask Application:
```python3 run.py```
2. Open web browser and go to:
```http://127.0.0.1:5000```
