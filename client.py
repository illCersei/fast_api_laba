import requests
import asyncio
import websockets
import json
import base64
import os

BASE_URL = "http://localhost:8000"

def login():
    email = input("Email: ")
    password = input("Password: ")
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    if response.status_code == 200:
        data = response.json()
        print("Успешный вход")
        return data["access_token"], data["id"]
    else:
        print("Ошибка входа:", response.text)
        return None, None

async def listen_websocket(user_id, token):
    url = f"ws://localhost:8000/ws/{user_id}?token={token}"
    async with websockets.connect(url) as websocket:
        print("WebSocket-соединение установлено")
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data.get("status") == "STARTED":
                print(f"[STARTED] Задача {data['task_id']} началась. Алгоритм: {data['algorithm']}")
            elif data.get("status") == "PROGRESS":
                print(f"[PROGRESS] Задача {data['task_id']}: {data['progress']}%")
            elif data.get("status") == "COMPLETED":
                print(f"[COMPLETED] Задача {data['task_id']} завершена. Изображение (base64): {data['binarized_image']}...")
            else:
                print("Неизвестное сообщение:", message)

def upload_image(token, user_id, path, algorithm="bradley"):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        response = requests.post(
            f"{BASE_URL}/binary/image/async",
            json={"image_base64": encoded_string, "user_id": str(user_id), "algorithm": algorithm},
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"Ответ сервера: {response.status_code} {response.text}")

def main():
    token, user_id = login()
    if not token:
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(listen_websocket(user_id, token))

    print("Введите команду (upload путь/к/файлу.png --algo=bradley | exit):")
    try:
        loop.run_until_complete(console_input_loop(token, user_id))
    except KeyboardInterrupt:
        print("\nВыход")

def parse_upload_command(cmd):
    parts = cmd.split()
    if len(parts) >= 2:
        path = parts[1]
        algo = "bradley"
        for part in parts:
            if part.startswith("--algo="):
                algo = part.split("=", 1)[1]
        return path, algo
    return None, None

async def console_input_loop(token, user_id):
    while True:
        cmd = await asyncio.to_thread(input, "> ")
        cmd = cmd.strip()
        if cmd == "exit":
            break
        elif cmd.startswith("upload"):
            path, algo = parse_upload_command(cmd)
            if path:
                upload_image(token, user_id, path, algo)
            else:
                print("Неверный формат. Пример: upload path/to/file.png --algo=bradley")

if __name__ == "__main__":
    main()
