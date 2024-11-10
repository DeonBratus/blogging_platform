from fastapi import FastAPI
from blog_api.api import app as blog_api  # Предполагается, что ваш роутер API экспортирован как api_router
from blog_front.app import app as blog_app  # Импортируем экземпляр FastAPI из blog_app
from users.user_api import app as user_app

app = FastAPI()

# Включаем роуты для API
app.include_router(blog_api, prefix="/api")
app.include_router(user_app, prefix="/api")
app.mount("/", blog_app)  # Привязываем приложение к корневому пути

# Запуск приложения с uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
