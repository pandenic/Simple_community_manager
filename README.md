# Simplified community manager

## Description

The module makes and manages posts and unites them into communities.

| Technologies | Links |
| ---- | ---- |
| ![git_Django](https://github.com/pandenic/Foodgram_project/assets/114985447/87a6dd6e-127f-47e7-bbd4-a6c28fcddf76) | [Django](https://www.djangoproject.com/) |
| ![git_Unittest](https://github.com/pandenic/Simple_community_manager/assets/114985447/3598ffcc-d8a1-46ad-9145-81bb26c3d54d) | [Unittest](https://docs.python.org/3/library/unittest.html) |
| ![git_pytest](https://github.com/pandenic/Simple_community_manager/assets/114985447/515734be-8016-4575-8f14-37b9ec430fb3) | [pytest](https://docs.pytest.org/en/7.4.x/) |

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
