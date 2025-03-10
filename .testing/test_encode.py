import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Укажи путь к изображению
image_base64 = encode_image_to_base64(".testing/test_image.png")

# Сохраняем base64 в файл (для удобства копирования)
with open(".testing/image_base64.txt", "w") as f:
    f.write(image_base64)

print("✅ Base64-код сохранён в image_base64.txt")
