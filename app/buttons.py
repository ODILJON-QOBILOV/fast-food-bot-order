from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define the feedback rating keyboard
def get_feedback_keyboard_uzb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("⭐️⭐️⭐️⭐️⭐️ Yaxshi"))
    keyboard.add(KeyboardButton("⭐️⭐️⭐️⭐️ Normalno"))
    keyboard.add(KeyboardButton("⭐️⭐️⭐️ Juda noto'g'ri"))
    keyboard.add(KeyboardButton("⭐️⭐️ Yomon"))
    keyboard.add(KeyboardButton("⭐️ Juda yomon"))
    return keyboard

# Keyboard for Feedback in Russian
def get_feedback_keyboard_ru():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("⭐️⭐️⭐️⭐️⭐️ Хорошо"))
    keyboard.add(KeyboardButton("⭐️⭐️⭐️⭐️ Что-то не так"))
    keyboard.add(KeyboardButton("⭐️⭐️⭐️ Очень плохо"))
    keyboard.add(KeyboardButton("⭐️⭐️ Плохо"))
    keyboard.add(KeyboardButton("⭐️ Очень плохо"))
    return keyboard

# Keyboard for Feedback in English
def get_feedback_keyboard_en():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("⭐️⭐️⭐️⭐️⭐️ Good"))
    keyboard.add(KeyboardButton("⭐️⭐️⭐️⭐️ Something is wrong"))
    keyboard.add(KeyboardButton("⭐️⭐️⭐️ Very wrong"))
    keyboard.add(KeyboardButton("⭐️⭐️ Bad"))
    keyboard.add(KeyboardButton("⭐️ Very bad"))
    return keyboard

# Define keyboards for language selection
language_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Русский"),
    KeyboardButton("O'zbek"),
    KeyboardButton("English")
)

# Define city keyboards for each language
city_kb_rus = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Ташкент"), KeyboardButton("Самарканд"), KeyboardButton("Андижон")
)
city_kb_uzb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Toshkent"), KeyboardButton("Samarqand"), KeyboardButton("Andijon")
)
city_kb_eng = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Tashkent"), KeyboardButton("Samarkand"), KeyboardButton("Andijan")
)

main_menu_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🛍️ Menu")  # First button in its own row
).row(
    KeyboardButton("📦 My Orders"), KeyboardButton("ℹ️ Info")
).row(
    KeyboardButton("📝 Feedbacks"), KeyboardButton("✍️ Give a Feedback")
).add(
    KeyboardButton("⚙ Settings")
)

# Russian Menu
main_menu_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🛍️ Меню")
).row(
    KeyboardButton("📦 Мои заказы"), KeyboardButton("ℹ️ Информация")
).row(
    KeyboardButton("📝 Отзывы"), KeyboardButton("✍️ Оставить отзыв")
).add(
    KeyboardButton("⚙ Настройки")
)


main_menu_kb_uz = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🛍️ Menyu")
).row(
    KeyboardButton("📦 Mening buyurtmalarim"), KeyboardButton("ℹ️ Ma'lumotlar")
).row(
    KeyboardButton("📝 Fikrlar"), KeyboardButton("✍️ Fikr qoldirish")
).add(
    KeyboardButton("⚙ Sozlamalar")
)

settings_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton("📝 Change Name"), KeyboardButton("📱 Change Number")
).row(
    KeyboardButton("🌐 Change Language"), KeyboardButton("🏙️ Change City")
).add(
    KeyboardButton("🔙 Back to menu")
)

settings_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton("📝 Изменить имя"), KeyboardButton("📱 Изменить номер")
).row(
    KeyboardButton("🌐 Изменить язык"), KeyboardButton("🏙️ Изменить город")
).add(
    KeyboardButton("🔙 Вернуться в меню")
)

settings_kb_uz = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton("📝 Ismni o'zgartirish"), KeyboardButton("📱 Raqamni o'zgartirish")
).row(
    KeyboardButton("🌐 Tilni o'zgartirish"), KeyboardButton("🏙️ Shaharni o'zgartirish")
).add(
    KeyboardButton("🔙 Orqaga qaytish")
)

back_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🔙 Back")
)

back_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🔙 Hазад")
)

back_kb_uz = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🔙 Orqaga")
)

back_to_main_ru = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🔙 Вернуться в меню")
)

back_to_main_uz = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🔙 Menyuga qaytish")
)

back_to_main_en = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("🔙 Back to menu")
)

