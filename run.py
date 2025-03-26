import requests
import json
import time
import uuid
import os
import random
from datetime import datetime

# 🎨 Menampilkan logo
def print_logo():
    print("\033[1;36m")  # Warna cyan
    print("╔══════════════════════════════╗")
    print("║      🤖  🆆 🅷 🆃 🅴 🅲 🅷  🤖     ║")
    print("║  Join 📢 t.me/airdropkerti   ║")
    print("╚══════════════════════════════╝")
    print("\033[0m")  # Reset warna

# 🔹 Baca user ID dan session token dari account.txt
def get_credentials():
    if not os.path.exists("account.txt"):
        print("❌ Error: File 'account.txt' tidak ditemukan!")
        exit()

    with open("account.txt", "r") as file:
        data = file.read().strip().split("|")
        if len(data) != 2:
            print("❌ Error: Format 'account.txt' tidak valid! (Gunakan format: user_id|session_token)")
            exit()
        return data[0], data[1]  # user_id, session_token

# 🔹 Baca daftar pesan dari pesan.txt (setiap baris = 1 pesan)
def get_messages():
    if not os.path.exists("pesan.txt"):
        print("❌ Error: File 'pesan.txt' tidak ditemukan!")
        exit()

    with open("pesan.txt", "r", encoding="utf-8") as file:
        messages = [line.strip() for line in file.readlines() if line.strip()]
    
    if not messages:
        print("❌ Error: File 'pesan.txt' kosong!")
        exit()
    
    return messages

# 🔹 Kirim request ke API
def send_request(message, user_id, session_token):
    url = "https://api1-pp.klokapp.ai/v1/chat"

    headers = {
        "Content-Type": "application/json",
        "x-session-token": session_token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    payload = {
        "id": str(uuid.uuid4()),  # UUID baru untuk setiap request
        "language": "english",
        "user": user_id,  # User ID dimasukkan ke payload
        "messages": [{"role": "user", "content": message}],
        "model": "llama-3.3-70b-instruct",
        "sources": []
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"🔍 Debug: Status Code = {response.status_code}")

        if response.status_code == 200:
            try:
                json_response = response.json()
                print(f"✅ Response: {json.dumps(json_response, indent=2)}\n")
            except json.JSONDecodeError:
                print(f"⚠️  Respon: {response.text}\n")
        else:
            print(f"⚠️ Respon Error {response.status_code}: {response.text}\n")

    except Exception as e:
        print(f"❌ Request failed: {e}\n")

# 🔹 Jalankan auto-chat setiap hari
def run_auto_chat():
    print_logo()  # Tampilkan logo
    user_id, session_token = get_credentials()
    messages = get_messages()

    while True:  # Loop terus-menerus agar jalan setiap hari
        print("\n📅 Hari baru dimulai! Mengirim 10 pesan...\n")

        # Pilih 10 pesan secara random setiap hari
        selected_messages = random.sample(messages, min(10, len(messages)))

        for i, message in enumerate(selected_messages, start=1):
            print(f"📩 Mengirim pesan {i}/10: {message}")
            send_request(message, user_id, session_token)

            if i < len(selected_messages):
                print("⏳ Menunggu 1 menit sebelum mengirim pesan berikutnya...\n")
                time.sleep(60)  # Jeda 1 menit antar pesan

        print("⏳ Menunggu 24 jam sebelum mengirim pesan lagi...\n")
        time.sleep(86400)  # Jeda 24 jam sebelum hari berikutnya

# 🔹 Jalankan skrip
if __name__ == "__main__":
    run_auto_chat()
