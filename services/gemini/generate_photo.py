import google.genai as genai
from google.genai import types
from PIL import Image
from io import BytesIO
from os import getenv
from dotenv import load_dotenv
import base64

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение API ключа
api_key = getenv('GEMINI_API_KEY')

# Инициализация клиента с API ключом
client = genai.Client(api_key=api_key)

# Путь к изображению
image_path = "../../static/test.jpg"

# Чтение изображения
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# Преобразуем изображение в формат base64
image_base64 = base64.b64encode(image_data).decode('utf-8')

# Запрос к модели Gemini API для редактирования изображения
response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[
        "Remove the background from this image and replace it with a snowy mountain vista.",
        image_base64  # Передаем изображение как строку base64
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
    )
)

# Сохранение отредактированного изображения
for part in response.candidates[0].content.parts:
    if part.inline_data:
        edited_image = Image.open(BytesIO(part.inline_data.data))
        edited_image.save("edited_image.jpg")
