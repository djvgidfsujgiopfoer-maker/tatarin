import asyncio, logging, json, sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
f
        web_app=WebAppInfo(url="https://maksim-theta.vercel.app/")
    )
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

    await message.answer(
        f" {username}!\n"
        "добро пожаловать! ёбаная бедность 💰\n"
        "Хочешь разбогатеть потыкай пузико максончика? 😎\n"
        "Жми «Играть» и покажи всем, кто настоящая ёбаная бедность!",
        reply_markup=keyboard
    )

# --- Получение данных из WebApp ---
@dp.message()
async def webapp_data_handler(message: types.Message):
    if message.web_app_data:  # данные пришли из игры
        try:
            data = json.loads(message.web_app_data.data)
            tg_id = message.from_user.id
            score = int(data.get("score", 0))

            cursor.execute("UPDATE leaderboard SET score = ? WHERE tg_id = ?", (score, tg_id))
            conn.commit()
            await message.answer(f"✅ Очки обновлены: {score} 🐷")
        except Exception as e:
            await message.answer("Ошибка при обработке данных ⚠️")
            print("Error:", e)

# --- Команда /top ---
@dp.message(Command("top"))
async def top_cmd(message: types.Message):
    rows = cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 10").fetchall()
    if not rows:
        await message.answer("Пока никто не играл 💤")
        return
    text = "🏆 Топ игроков:\n\n"
    for i, (name, score) in enumerate(rows, start=1):
        text += f"{i}. {name} — {score} 🐷\n"
    await message.answer(text)

async def main():
    print("✅ Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
