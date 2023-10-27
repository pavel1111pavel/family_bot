from database import SessionLocal, UserResponse, Task, Category

# Создаем сессию для работы с базой данных
db = SessionLocal()

# Выполняем запрос к таблице UserResponse
responses = db.query(Task).all()
responses2 = db.query(Category).all()
print(responses2)
for i in responses2:
    print(i.name, i.id)
# Теперь переменная responses содержит все записи из таблицы
for response in responses:
    print(f"User ID: {response.user_id}{response.id}, Response: {response.task_text}, Created At: {response.category_id}")

# Закрываем сессию
db.close()






# Создаем сессию для работы с базой данных
# db = SessionLocal()
#
# # Пример выполнения SQL-запроса
# sql_query = "SELECT * FROM user_responses WHERE user_id = :user_id"
# params = {"user_id": 123}
#
# result = db.execute(sql_query, params)
#
# # Получаем результаты запроса
# for row in result:
#     print(f"User ID: {row.user_id}, Response: {row.response_text}, Created At: {row.created_at}")
#
# # Закрываем сессию
# db.close()