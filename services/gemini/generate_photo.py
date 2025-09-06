from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
from services.gpt.proxy import set_proxy, clear_proxy


def generate_img(user_id, user_prompt):
    load_dotenv()

    set_proxy()
    client = genai.Client(api_key=getenv("GEMINI_API_KEY"))
    clear_proxy()

    prompt = (f"""
        {user_prompt}
        Keep the person exactly as in the original photo (same face, pose, clothes, colors).
        No new characters, no stylization. Photorealistic."""
    )

    print(prompt)

    img = Image.open(rf"static/{user_id}/input_img/input.jpg")  # можно .png/.jpg

    resp = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt, img],
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )

    for part in resp.candidates[0].content.parts:
        if getattr(part, "inline_data", None):
            with open(rf"static/{user_id}/output_img/output.jpg", "wb") as f:
                f.write(part.inline_data.data)
                print('сгенерировано')
