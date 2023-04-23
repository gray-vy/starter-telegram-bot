import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, executor



#Создание базы данных
conn = sqlite3.connect('tobacco_list.db')
#Создание объекта подключения
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS tobacco_list(
   name_tobacco TEXT,
   quantity INT);
""")
conn.commit()

# Выполняем SQL-запрос для выборки всех значений из таблицы tobacco_list
cur.execute("SELECT name_tobacco, quantity FROM tobacco_list")

# Получаем все результаты из выполненного запроса в виде списка кортежей
results = cur.fetchall()

# Создаем список строк, где каждая строка содержит имя и количество отдельного табака
tobacco_strings = [f"{row[0]} - {row[1]}" for row in results]

# Объединяем все строки в одну с помощью функции join() и переносов строк между ними
tobacco_message = "\n".join(tobacco_strings)


async def send_low_quantity_tobacco(bot: Bot, chat_id: int):
    # Выполняем SQL-запрос для выборки всех значений из таблицы tobacco_list
    cur.execute("SELECT name_tobacco, quantity FROM tobacco_list")

    # Получаем все результаты из выполненного запроса в виде списка кортежей
    results = cur.fetchall()

    # Создаем список строк, где каждая строка содержит имя и количество отдельного табака, у которого количество меньше 2
    tobacco_strings = [f"{row[0]} - {int(row[1])}" for row in results if int(row[1]) < 2]


    # Если есть табаки с низким количеством, отправляем сообщение с их перечислением
    if tobacco_strings:
        # Объединяем все строки в одну с помощью функции join() и переносов строк между ними
        tobacco_message = "\n".join(tobacco_strings)
        await bot.send_message(chat_id, f"Этот табак стоит заказать 🤔:\n{tobacco_message}")


####

###



    # Закрываем соединение с базой данных

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6198709957:AAHZ9mvFccb3LV-E3ZhgDe0MXCnkNQIe2SA")

dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Список табаков📋")
    keyboard.add(button_1)
    button_2 = types.KeyboardButton(text="Позиции к заявке🛒")
    keyboard.add(button_2)
    button_3 = types.KeyboardButton(text="Актуальный график работы")
    keyboard.add(button_3)
    await message.answer("Добро пожаловать в ревизионного телеграмм-бота!\nВоспользуйтесь клавиатурой для навигации\nДля изменения количества табака напишите: 'Изменить (название) (количество)'\nPowered by @grayvord", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Список табаков📋")
@dp.message_handler(lambda message: message.text == "Список табаков📋")
async def cmd_list(message: types.Message):
    # Выполняем SQL-запрос для выборки всех значений из таблицы tobacco_list
    cur.execute("SELECT name_tobacco, quantity FROM tobacco_list")

    # Получаем все результаты из выполненного запроса в виде списка кортежей
    results = cur.fetchall()

    # Создаем список строк, где каждая строка содержит имя и количество отдельного табака
    tobacco_strings = [f"{row[0]} - {row[1]}" for row in results]

    # Объединяем все строки в одну с помощью функции join() и переносов строк между ними
    tobacco_message = "\n".join(tobacco_strings)

    await message.reply(tobacco_message)


@dp.message_handler(lambda message: message.text == "Позиции к заявке🛒")
async def check_tobacco(message: types.Message):
    # Получаем идентификатор чата, куда нужно отправить сообщение
    chat_id = message.chat.id

    # Вызываем функцию для отправки сообщения с табаками, у которых количество меньше 2
    await send_low_quantity_tobacco(bot, chat_id)

@dp.message_handler(lambda message: message.text.startswith("Изменить"))
async def cmd_change_quantity(message: types.Message):
    # Получаем имя и новое количество табака из сообщения пользователя
    parts = message.text.split()
    name = " ".join(parts[1:-1])
    quantity = int(parts[-1])

    # Выполняем SQL-запрос для обновления количества табака в базе данных
    cur.execute("UPDATE tobacco_list SET quantity = ? WHERE name_tobacco = ?", (quantity, name))
    conn.commit()

    # Отправляем подтверждение пользователю
    await message.reply(f"Количество табака \"{name}\" изменено на {quantity} ✅")

@dp.message_handler(lambda message: message.text == 'Актуальный график работы')
async def cmd_raspisanie(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo='https://imgur.com/4FgWfNX')



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)