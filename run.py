import requests
import time
import json
import sys
from datetime import datetime
from pyfiglet import figlet_format

API_URL = "https://api1-pp.klokapp.ai/v1/chat"

# Menampilkan logo
print("\033[1;36m")  # Warna cyan
print("╔══════════════════════════════╗")
print("║      🤖  🆆 🅷 🆃 🅴 🅲 🅷  🤖     ║")
print("║  Join 📢 t.me/airdropkerti   ║")
print("╚══════════════════════════════╝")
print("\033[0m")  # Reset warna

# Load akun dari file account.txt
def load_accounts():
    with open("account.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# Load pesan dari file pesan.txt
def load_messages():
    with open("pesan.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# Memilih model AI sekali untuk semua akun
def choose_model():
    models = {
        "1": "llama-3.3-70b-instruct",
        "2": "deepseek-r1",
        "3": "gpt-4o-mini"
    }
    print("\nPilih Model AI:")
    for k, v in models.items():
        print(f"{k}. {v}")

    while True:
        choice = input("\nMasukkan nomor model yang dipilih: ")
        if choice in models:
            print(f"\n✅ Model yang dipilih: {models[choice]}\n")
            return models[choice]
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")

# Mengirim request dengan format yang sesuai
def send_request(messages, headers, model):
    payload = {
        "id": "auto-generated",
        "title": "**🤖 Automated Chat**",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "language": "english",
        "messages": messages,
        "model": model,
        "sources": []
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, stream=True)
        if response.status_code == 200:
            print("\n✅ AI Response:")
            sys.stdout.flush()

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    sys.stdout.write(decoded_line + " ")
                    sys.stdout.flush()
            print("\n✅ Chat Success\n")
            return True
        else:
            print(f"⚠️ API Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ Request Error: {e}")
        return False

# Menjalankan auto chat untuk satu akun
def run_auto_chat(session_token, model_choice, messages):
    headers = {
        "x-session-token": session_token,
        "Content-Type": "application/json"
    }
    
    print("\n🔑 Menggunakan akun baru...\n")
    print("🚀 Memulai auto chat...\n")

    conversation = []
    for i, message in enumerate(messages, 1):
        print(f"📩 Mengirim pesan {i}/{len(messages)}: {message}")

        conversation.append({"role": "user", "content": message})

        success = send_request(conversation, headers, model_choice)

        if not success:
            print("⏩ Melewati pesan ini...\n")
            continue

        # Countdown sebelum pesan berikutnya
        for j in range(15, 0, -1):
            sys.stdout.write(f"\r⏳ Menunggu {j} detik... ")
            sys.stdout.flush()
            time.sleep(1)
        print("\n")

# Menjalankan semua akun
def run_all():
    accounts = load_accounts()
    messages = load_messages()
    model_choice = choose_model()
    
    while True:
        for session_token in accounts:
            run_auto_chat(session_token, model_choice, messages)

        # Menunggu 24 jam sebelum menjalankan ulang
        print(figlet_format("WAITING 24 H TO RUNNING AGAIN", font="slant"))
        for remaining in range(86400, 0, -1):
            sys.stdout.write(f"\r⏳ Menunggu {remaining//3600} jam {remaining%3600//60} menit {remaining%60} detik...")
            sys.stdout.flush()
            time.sleep(1)
        print("\n🔄 Memulai ulang...\n")

if __name__ == "__main__":
    run_all()
