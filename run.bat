@echo off
echo creating virtual environment
python -m venv venv
call venv\Scripts\activate.bat

echo installing requirements
python -m pip install -r requirements.txt

echo starting app
python -m src username_example125259 -1
