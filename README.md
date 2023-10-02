# Simplified community manager

## Description

The module makes and manages posts and unites them into communities.

| Technologies | Links |
| ---- | ---- |
| ![git_Django](https://github.com/pandenic/Foodgram_project/assets/114985447/87a6dd6e-127f-47e7-bbd4-a6c28fcddf76) | [Django](https://www.djangoproject.com/) |
| ![git_Unittest](https://github.com/pandenic/hw05_final/assets/114985447/43851cd6-d1ff-4aa3-8d81-3b7eaf88979c) | [Unittest](https://docs.python.org/3/library/unittest.html) |
| ![git_pytest](https://github.com/pandenic/hw05_final/assets/114985447/096e8e9f-e258-46fa-ae61-4e11107e2907) | [pytest](https://docs.pytest.org/en/7.4.x/) |

## Run instructions

Create a virtual environment:
```bash
python3.9 -m venv venv
```

Install requirements
```bash
pip install -r requirements.txt
```

Make migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

Execute the command in a folder with the manage.py file
```
python3 manage.py runserver
```
