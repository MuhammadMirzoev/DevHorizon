import requests

url = "http://127.0.0.1:5000/tasks"
data = {
    "title": "Разработка новой функции",
    "description": "Добавить поддержку REST API",
    "assigned_user_id": 1,
    "status": "в процессе",
    "deadline": "2024-12-20"
}

response = requests.post(url, json=data)
print(response.json())
