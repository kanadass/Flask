import requests

# user
response = requests.post(
    "http://127.0.0.1:5000/user",
    json={
        "name": "Bob",
        "password": "12aedgf345",
        }
)
print(response.status_code)
print(response.json())




# response = requests.get(
#     'http://127.0.0.1:5000/user/2',
# )
# print(response.status_code)
# print(response.json())
#
#
#
#
#
# response = requests.patch(
#     'http://127.0.0.1:5000/user/1',
#     json={"name": "Shara"},
# )
# print(response.status_code)
# print(response.json())
#
#
#
#
#
# response = requests.delete(
#     "http://127.0.0.1:5000/user/1",
# )
# print(response.status_code)
# print(response.json())




# Advertisement

# # Создание объявления
# response = requests.post(
#     "http://127.0.0.1:5000/ad/",
#     json={
#     "title": "New Advertisement 1",
#     "description": "Description of the new ad 1",
#     "owner_id": 2
#     }
# )
# print(response.status_code)
# print(response.json())

# # Получение информации об объявлении
# response = requests.get("http://127.0.0.1:5000/ad/5")
# print(response.status_code)
# print(response.json())
#
# # Редактирование информации об объявлении
# response = requests.patch(
#     "http://127.0.0.1:5000/ad/5",
#     json={
#     "title": "Updated Ad",
#     "description": "Updated description"
#     }
# )
# print(response.status_code)
# print(response.json())
#
# # Удаление объявления
# response = requests.delete("http://127.0.0.1:5000/ad/5")
# print(response.status_code)
# print(response.json())
