from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
from services.gpt.proxy import set_proxy, clear_proxy


def generate_img():
    load_dotenv()

    set_proxy()
    client = genai.Client(api_key=getenv("GEMINI_API_KEY"))
    clear_proxy()

    prompt = (f"""
        Edit the hairstyle to extend the hair length to the desired measurement while preserving the person's face, pose, background, and overall appearance. Keep hair color, highlights, texture, and shine exactly as in the original. Extend the hair to [desired length] cm (or inches), with a natural blend at the roots and ends. Maintain the current volume distribution and movement, and keep the same parting. Do not alter skin, eyes, facial expression, or any other facial features, nor lighting or background.
        Keep the person exactly as in the original photo (same face, pose, clothes, colors).
        No new characters, no stylization. Photorealistic."""
    )

    print(prompt)

    img = Image.open(rf"input.jpg")  # можно .png/.jpg

    resp = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt, img],
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )

    for part in resp.candidates[0].content.parts:
        print("DEBUG PART:", part)
        if getattr(part, "inline_data", None):
            with open(rf"output.jpg", "wb") as f:
                f.write(part.inline_data.data)
                print('сгенерировано')

generate_img()