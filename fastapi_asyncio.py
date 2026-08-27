import asyncio  # Модуль для работы с асинхронным циклом событий
import httpx     # Асинхронный HTTP-клиент

async def fetch_url(url: str):
    # Создаём клиент HTTPX внутри контекстного менеджера,
    # чтобы соединение автоматически закрывалось после выполнения запроса
    async with httpx.AsyncClient() as client:
        # Отправляем GET-запрос и ждём ответа
        response = await client.get(url)
        # Возвращаем код ответа и обрезанный до 50 символов текст
        return response.status_code, response.text[:50]

async def main():
    # Список URL, к которым будем делать запросы
    urls = [
        "https://postman-echo.com/delay/1", # Этот URL задержит ответ на 1 секунду
        "https://postman-echo.com/delay/2"  # Этот URL задержит ответ на 2 секунды
    ]

    # Запуск всех запросов параллельно с помощью asyncio.gather
    # Генератор создаёт корутины fetch_url(url) для каждого URL из списка
    results = await asyncio.gather(*(fetch_url(url) for url in urls))

    # Обработка результатов
    for status, text in results:
        # Печатаем HTTP-статус и первые 50 символов текста ответа
        print(f"Статус ответа: {status}, начало текста: {text}")

if __name__ == "__main__":
    # Запускаем основную корутину main() в асинхронном цикле событий
    asyncio.run(main())
