import base64
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from io import BytesIO

#app = FastAPI()

class ImageBase64Request(BaseModel):
    image_base64: str

def decode_base64_to_image(base64_string: str) -> np.ndarray:
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data)).convert('L')  
        return np.array(image)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image format")

def encode_image_to_base64(image: np.ndarray) -> str:
    pil_image = Image.fromarray(image)
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def bradley_threshold(image: np.ndarray, S_div: int = 8, t: float = 0.15) -> np.ndarray:
    height, width = image.shape
    S = width // S_div
    s2 = S // 2

    integral_image = np.cumsum(np.cumsum(image, axis=0), axis=1).astype(np.float64)
    integral_image = np.pad(integral_image, ((1, 0), (1, 0)), mode='constant', constant_values=0)

    binary_image = np.zeros_like(image, dtype=np.uint8)

    for y in range(height):
        y1 = max(y - s2, 0)
        y2 = min(y + s2, height - 1)
        for x in range(width):
            x1 = max(x - s2, 0)
            x2 = min(x + s2, width - 1)

            count = (y2 - y1 + 1) * (x2 - x1 + 1)
            sum_region = (
                integral_image[y2 + 1, x2 + 1]
                - integral_image[y1, x2 + 1]
                - integral_image[y2 + 1, x1]
                + integral_image[y1, x1]
            )

            if int(image[y, x]) * count < sum_region * (1.0 - t):
                binary_image[y, x] = 0
            else:
                binary_image[y, x] = 255

    return binary_image


