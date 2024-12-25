from aiogram import Bot, executor
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from app.database import update_language, update_city, get_user, add_user, start_db, update_name, update_phone, \
    get_user_language
from app.buttons import language_kb, city_kb_rus, city_kb_uzb, city_kb_eng, main_menu_kb_en, main_menu_kb_ru, \
    main_menu_kb_uz, settings_kb_ru, settings_kb_uz, settings_kb_en, back_kb_uz, back_kb_ru, back_kb_en, \
    get_feedback_keyboard_uzb, get_feedback_keyboard_ru, \
    get_feedback_keyboard_en, back_to_main_uz, back_to_main_ru, back_to_main_en
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os

BOT_TOKEN = "7718263976:AAFE04mgDSXu6ic1aaUiJvis-ahmOTeARgg"

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    waiting_for_number = State()
    waiting_for_city = State()
    waiting_for_language = State()
    waiting_for_comment = State()

class ChangeNameState(StatesGroup):
    waiting_for_name = State()



# Set up i18n
class CustomI18nMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: tuple) -> str:
        start_db()
        user = types.User.get_current()
        language = "en"  # Default language
        db_user = get_user(user.id)
        if db_user and db_user[3]:  # Assuming column 3 is language
            language_map = {"Русский": "ru", "O'zbek": "uz", "English": "en"}
            language = language_map.get(db_user[3], "en")
        print(f"User locale: {language}")  # Debugging line
        return language


i18n = CustomI18nMiddleware("mybot", os.path.join(os.path.dirname(__file__), 'locales'))
dp.middleware.setup(i18n)

_ = i18n.gettext

# Handle start command
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    user = get_user(message.from_user.id)

    if not user:
        add_user(username=message.from_user.username, user_id=message.from_user.id)
        await message.reply(
            _("Здравствуйте! Давайте для начала выберем язык обслуживания! Keling, avvaliga xizmat ko’rsatish tilini tanlab olaylik. Hi! Let's first choose the language of service!"),
            reply_markup=language_kb
        )
    else:
        language = user[3]
        city = user[4]

        if language and city:
            menu = {
                "Русский": main_menu_kb_ru,
                "O'zbek": main_menu_kb_uz,
                "English": main_menu_kb_en
            }.get(language, main_menu_kb_en)
            greeting_message = _("Welcome back! Choose an option from the menu below:")

            if language == "Русский":
                greeting_message = _("Добро пожаловать! Выберите опцию из меню ниже:")
            if language == "O'zbek":
                greeting_message = _("Xush kelibsiz")

            await message.reply(greeting_message, reply_markup=menu)
        else:
            if not language:
                await message.reply(_("Please choose your language:"), reply_markup=language_kb)
            elif not city:
                city_kb = {
                    "Русский": city_kb_rus,
                    "O'zbek": city_kb_uzb,
                    "English": city_kb_eng
                }.get(language, city_kb_eng)
                await message.reply(_("Please select your city:"), reply_markup=city_kb)

# Handle language selection
@dp.message_handler(lambda message: message.text in ["Русский", "O'zbek", "English"])
async def language_selection(message: types.Message):
    update_language(message.from_user.id, message.text)

    # Debugging line to check language update
    print(f"Language updated to: {message.text}")

    city_kb = {
        "Русский": city_kb_rus,
        "O'zbek": city_kb_uzb,
        "English": city_kb_eng
    }.get(message.text, city_kb_eng)

    if message.text == "Русский":
        response_message = _("Пожалуйста, выберите ваш город:")
    if message.text == "English":
        response_message = _("Please, choose you city:")
    if message.text == "O'zbek":
        response_message = _("Iltimos, shaxaringizni tanlang:")

    await message.reply(response_message, reply_markup=city_kb)


# Handle city selection
@dp.message_handler(
    lambda message: message.text in ["Ташкент", "Самарканд", "Андижон", "Toshkent", "Samarqand", "Andijon", "Tashkent",
                                     "Samarkand", "Andijan"])
async def city_selection(message: types.Message):
    update_city(message.from_user.id, message.text)

    # Debugging line to check city update
    print(f"City updated to: {message.text}")

    language = get_user(message.from_user.id)[3]
    menu = {
        "Русский": main_menu_kb_ru,
        "O'zbek": main_menu_kb_uz,
        "English": main_menu_kb_en
    }.get(language, main_menu_kb_en)

    if language == "Русский":
        confirmation_message = _("Вы успешно зарегистрированы! Выберите опцию из меню ниже:")
    elif language == "O'zbek":
        confirmation_message = _("Siz muvaffaqiyatli ro'yxatdan o'tdingiz! Quyidagi menyudan tanlov qiling:")
    elif language == "English":
        confirmation_message = _("You are registered successfully, You can go to the menu:")

    await message.reply(confirmation_message, reply_markup=menu)


# fikrlar
@dp.message_handler(lambda message: message.text in ["✍️ Fikr qoldirish", "✍️ Оставить отзыв", "✍️ Give a Feedback"])
async def prompt_feedback(message: types.Message):
    # Get the user's language preference
    language = get_user_language(message.from_user.id)

    # Send the feedback prompt based on the user's language
    if language == "O'zbek":
        await message.reply("Iltimos, xizmatimizni baholang:", reply_markup=get_feedback_keyboard_uzb())
    elif language == "Русский":
        await message.reply("Пожалуйста, оцените нашу работу:", reply_markup=get_feedback_keyboard_ru())
    else:
        await message.reply("Please rate our service:", reply_markup=get_feedback_keyboard_en())

@dp.message_handler(lambda message: message.text in
                                    ["⭐️⭐️⭐️⭐️⭐️ Yaxshi", "⭐️⭐️⭐️⭐️ Nima noto'g'ri?", "⭐️⭐️⭐️ Juda noto'g'ri",
                                     "⭐️⭐️ Yomon", "⭐️ Juda yomon",
                                     "⭐️⭐️⭐️⭐️⭐️ Хорошо", "⭐️⭐️⭐️⭐️ Что-то не так", "⭐️⭐️⭐️ Очень плохо",
                                     "⭐️⭐️ Плохо", "⭐️ Очень плохо",
                                     "⭐️⭐️⭐️⭐️⭐️ Good", "⭐️⭐️⭐️⭐️ Something is wrong", "⭐️⭐️⭐️ Very wrong",
                                     "⭐️⭐️ Bad", "⭐️ Very bad"])
async def handle_rating(message: types.Message):
    # Handle rating selection and process feedback
    user_id = message.from_user.id
    rating = 0
    feedback = ""

    # Determine rating based on the text
    if message.text in ["⭐️⭐️⭐️⭐️⭐️ Yaxshi", "⭐️⭐️⭐️⭐️⭐️ Хорошо", "⭐️⭐️⭐️⭐️⭐️ Good"]:
        rating = 5
        feedback = "Great service!"
    elif message.text in ["⭐️⭐️⭐️⭐️ Nima noto'g'ri?", "⭐️⭐️⭐️⭐️ Что-то не так", "⭐️⭐️⭐️⭐️ Something is wrong"]:
        rating = 4
        feedback = "Something was wrong."
    elif message.text in ["⭐️⭐️⭐️ Juda noto'g'ri", "⭐️⭐️⭐️ Очень плохо", "⭐️⭐️⭐️ Very wrong"]:
        rating = 3
        feedback = "Very wrong."
    elif message.text in ["⭐️⭐️ Yomon", "⭐️⭐️ Плохо", "⭐️⭐️ Bad"]:
        rating = 2
        feedback = "Bad service."
    elif message.text in ["⭐️ Juda yomon", "⭐️ Очень плохо", "⭐️ Very bad"]:
        rating = 1
        feedback = "Very bad."

    # Acknowledge the rating
    await message.reply(f"Thank you for your feedback! You rated us {rating} stars. {feedback}")

    # If the rating is less than 5, ask for additional feedback
    if rating < 5:
        # Request additional feedback based on the language
        language = get_user_language(user_id)
        if language == "O'zbek":
            await message.reply("Nima yoqtirmadingiz? Xizmatimizni yaxshilash uchun fikrlaringizni qoldiring.")
        elif language == "Русский":
            await message.reply(
                "Что вам не понравилось? Пожалуйста, оставьте ваш отзыв, чтобы мы могли улучшить наш сервис.")
        else:
            await message.reply("What did you dislike? Please leave your feedback so we can improve our service.")


# info
@dp.message_handler(lambda message: message.text == "ℹ️ Информация" or message.text == "ℹ️ Info" or message.text == "ℹ️ Info")
async def info_handler(message: types.Message):
    # Get the user's language from the database
    language = get_user_language(message.from_user.id)

    if language == "O'zbek":
        await message.reply("Hozircha ma'lumot mavjud emas.", reply_markup=back_to_main_uz)
    elif language == "Русский":
        await message.reply("На данный момент информации нет.", reply_markup=back_to_main_ru)
    else:
        await message.reply("Currently, no information is available.", reply_markup=back_to_main_en)



@dp.message_handler(lambda message: message.text in ["⚙ Settings", "⚙ Настройки", "⚙ Sozlamalar"])
async def settings_command(message: types.Message):
    language = get_user(message.from_user.id)[3]

    menu = {
        "Русский": settings_kb_ru,
        "O'zbek": settings_kb_uz,
        "English": settings_kb_en
    }.get(language, settings_kb_en)

    if language == "Русский":
        await message.reply(_("Выберите действие:"), reply_markup=menu)
    elif language == "O'zbek":
        await message.reply(_("Harakat tanlang:"), reply_markup=menu)
    elif language == "English":
        await message.reply(_("Choose an option:"), reply_markup=menu)


# Handle name, phone, and city changes
@dp.message_handler(lambda message: message.text in ["📝 Change Name", "📝 Изменить имя", "📝 Ismni o'zgartirish"])
async def change_name(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]
    user_id = message.from_user.id

    # Prompt the user to send their new name
    if language == "O'zbek":
        await message.reply("Yangi ismingizni kiriting:", reply_markup=back_kb_uz)
    elif language == "Русский":
        await message.reply("Введите Ф.И.О:", reply_markup=back_kb_ru)
    elif language == "English":
        await message.reply("Please send your new name:", reply_markup=back_kb_en)

    # Set the state to wait for the new name
    await ChangeNameState.waiting_for_name.set()
    # Store the user ID in the state
    await state.update_data(user_id=user_id, language=language)


@dp.message_handler(state=ChangeNameState.waiting_for_name)
async def save_new_name(message: types.Message, state: FSMContext):
    # Retrieve the stored data
    data = await state.get_data()
    user_id = data.get("user_id")
    language = data.get("language")

    # Update the user's name in the database
    new_name = message.text
    update_name(user_id, new_name)

    # Respond with a confirmation message
    if language == "O'zbek":
        await message.reply("✅ Qilindi", reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply("✅ Cделано", reply_markup=settings_kb_ru)
    elif language == "English":
        await message.reply("✅ Done", reply_markup=settings_kb_en)

    # Finish the state
    await state.finish()


@dp.message_handler(lambda message: message.text in ["🔙 Back", "🔙 Назад", "🔙 Orqaga"])
async def go_back(message: types.Message):
    language = get_user(message.from_user.id)[3]

    if language == "O'zbek":
        await message.reply(_("Siz hozirda sozlamalardasiz. Iltimos, kerakli variantni tanlang:"), reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply(_("Вы сейчас в настройках. Пожалуйста, выберите нужный вариант:"), reply_markup=settings_kb_ru)
    elif language == "English":
        await message.reply(_("You are currently in settings. Please choose an option:"), reply_markup=settings_kb_en)

# Handle "Change Number"

@dp.message_handler(lambda message: message.text in ["📱 Change Number", "📱 Изменить номер", "📱 Raqamni o'zgartirish"] or message.sticker, state="*")
async def change_number(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]
    user_id = message.from_user.id

    # Start the state machine for the user
    await state.set_state(UserState.waiting_for_number)

    if language == "O'zbek":
        await message.reply(_("Iltimos, yangi telefon raqamingizni kiriting:"), reply_markup=back_kb_uz)
    elif language == "Русский":
        await message.reply(_("Пожалуйста, введите ваш новый номер телефона:"), reply_markup=back_kb_ru)
    elif language == "English":
        await message.reply(_("Please send your new phone number:"), reply_markup=back_kb_en)

@dp.message_handler(state=UserState.waiting_for_number)
async def save_new_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_number = message.text
    language = get_user(message.from_user.id)[3]

    # Save the phone number in the database
    update_phone(user_id, new_number)

    # Send response in the user's language
    if language == "O'zbek":
        await message.reply(_("Sizning telefon raqamingiz yangilandi!"), reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply(_("Ваш номер телефона был обновлен!"), reply_markup=settings_kb_ru)
    else:
        await message.reply(_("Your phone number has been updated!"), reply_markup=settings_kb_en)

    # Reset state after updating phone number
    await state.finish()

# Handle the back button press to go back to the settings menu
@dp.message_handler(lambda message: message.text == _("🔙 Back"), state="*")
async def go_back(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]

    if language == "O'zbek":
        await message.reply(_("Siz hozir sozlamalar bo'limidasiz. Iltimos, kerakli variantni tanlang:"), reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply(_("Вы находитесь в разделе настроек. Пожалуйста, выберите необходимую опцию:"), reply_markup=settings_kb_ru)
    else:
        await message.reply(_("You are in the settings section. Please select the desired option:"), reply_markup=settings_kb_en)

    # Reset state after going back
    await state.finish()

# Handle "Change City"
@dp.message_handler(lambda message: message.text in ["🏙️ Change City", "🏙️ Изменить город", "🏙️ Shahrni o'zgartirish"] or message.sticker, state="*")
async def change_city(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]
    user_id = message.from_user.id

    # Start the state machine for the user
    await state.set_state(UserState.waiting_for_city)

    if language == "O'zbek":
        await message.reply(_("Iltimos, yangi shahringizni tanlang:"), reply_markup=city_kb_uzb)
    elif language == "Русский":
        await message.reply(_("Пожалуйста, выберите ваш новый город:"), reply_markup=city_kb_rus)
    elif language == "English":
        await message.reply(_("Please select your new city:"), reply_markup=city_kb_eng)

# Handle saving the city
@dp.message_handler(state=UserState.waiting_for_city)
async def save_new_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_city = message.text
    language = get_user(message.from_user.id)[3]

    # Save the city in the database
    update_city(user_id, new_city)

    # Send response in the user's language
    if language == "O'zbek":
        await message.reply(_("Sizning shaharingiz yangilandi!"), reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply(_("Ваш город был обновлен!"), reply_markup=settings_kb_ru)
    else:
        await message.reply(_("Your city has been updated!"), reply_markup=settings_kb_en)

    # Reset state after updating city
    await state.finish()

# Handle back button
@dp.message_handler(lambda message: message.text == _("🔙 Back"), state="*")
async def go_back(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]

    if language == "O'zbek":
        await message.reply(_("Siz hozir sozlamalar bo'limidasiz. Iltimos, kerakli variantni tanlang:"), reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply(_("Вы находитесь в разделе настроек. Пожалуйста, выберите необходимую опцию:"), reply_markup=settings_kb_ru)
    else:
        await message.reply(_("You are in the settings section. Please select the desired option:"), reply_markup=settings_kb_en)

    # Reset state after going back
    await state.finish()

@dp.message_handler(lambda message: message.text in ["🏙️ Change City", "🏙️ Изменить город", "🏙️ Shahrni o'zgartirish"] or message.sticker, state="*")
async def change_city(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]  # Get user's language from the database
    user_id = message.from_user.id

    # Start the state machine for the user
    await state.set_state(UserState.waiting_for_city)

    # Send messages based on the user's language
    if language == "O'zbek":
        await message.reply(_("Iltimos, yangi shahringizni tanlang:"), reply_markup=city_kb_uzb)
    elif language == "Русский":
        await message.reply(_("Пожалуйста, выберите ваш новый город:"), reply_markup=city_kb_rus)
    elif language == "English":
        await message.reply(_("Please select your new city:"), reply_markup=city_kb_eng)

# Handle saving the city
@dp.message_handler(state=UserState.waiting_for_city)
async def save_new_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_city = message.text
    language = get_user(message.from_user.id)[3]  # Get user's language again for the response

    # Save the city in the database
    update_city(user_id, new_city)

    # Send response in the user's language
    if language == "O'zbek":
        await message.reply(_("Sizning shaharingiz yangilandi!"), reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply(_("Ваш город был обновлен!"), reply_markup=settings_kb_ru)
    else:
        await message.reply(_("Your city has been updated!"), reply_markup=settings_kb_en)

    # Reset state after updating city
    await state.finish()

# Handle back button to go back to settings menu
@dp.message_handler(lambda message: message.text == _("🔙 Back"), state="*")
async def go_back(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]  # Get user's language for the back message

    # Send a message based on the user's language
    if language == "O'zbek":
        await message.reply(_("Siz hozir sozlamalar bo'limidasiz. Iltimos, kerakli variantni tanlang:"), reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply(_("Вы находитесь в разделе настроек. Пожалуйста, выберите необходимую опцию:"), reply_markup=settings_kb_ru)
    else:
        await message.reply(_("You are in the settings section. Please select the desired option:"), reply_markup=settings_kb_en)

    # Reset state after going back
    await state.finish()

@dp.message_handler(lambda message: message.text in ["🌐 Change Language", "🌐 Изменить язык", "🌐 Tilni o'zgartirish"] or message.sticker, state="*")
async def change_language(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]  # Get user's current language from the database
    user_id = message.from_user.id

    # Start the state machine for changing the language
    await state.set_state(UserState.waiting_for_language)

    # Send messages asking to choose the new language
    if language == "O'zbek":
        await message.reply(_("Iltimos, yangi tilni tanlang:"), reply_markup=language_kb)
    elif language == "Русский":
        await message.reply(_("Пожалуйста, выберите новый язык:"), reply_markup=language_kb)
    elif language == "English":
        await message.reply(_("Please select your new language:"), reply_markup=language_kb)

# Handle saving the selected language
@dp.message_handler(state=UserState.waiting_for_language)
async def save_new_language(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_language = message.text
    language = get_user(message.from_user.id)[3]  # Get user's language again for response

    # Update language in the database
    update_language(user_id, new_language)

    # Send response in the user's language
    if new_language == "O'zbek":
        await message.reply(_("Sizning tilingiz yangilandi!"), reply_markup=settings_kb_uz)
    elif new_language == "Русский":
        await message.reply(_("Ваш язык был обновлен!"), reply_markup=settings_kb_ru)
    elif new_language == "English":
        await message.reply(_("Your language has been updated!"), reply_markup=settings_kb_en)

    # Reset state after updating language
    await state.finish()

# Handle back button to go back to settings menu
@dp.message_handler(lambda message: message.text == _("🔙 Back"), state="*")
async def go_back(message: types.Message, state: FSMContext):
    language = get_user(message.from_user.id)[3]

    # Send a message based on the user's language
    if language == "O'zbek":
        await message.reply(_("Siz hozir sozlamalar bo'limidasiz. Iltimos, kerakli variantni tanlang:"), reply_markup=settings_kb_uz)
    elif language == "Русский":
        await message.reply(_("Вы находитесь в разделе настроек. Пожалуйста, выберите необходимую опцию:"), reply_markup=settings_kb_ru)
    else:
        await message.reply(_("You are in the settings section. Please select the desired option:"), reply_markup=settings_kb_en)

    # Reset state after going back
    await state.finish()


@dp.message_handler(lambda message: message.text)
async def back_from_settings(message: types.Message, state: FSMContext):
    # Get the user's language
    language = get_user(message.from_user.id)[3]

    if language == "O'zbek" and message.text == "🔙 Orqaga qaytish":
        await message.reply("Asosiy menyuga qaytish:", reply_markup=main_menu_kb_uz)
    elif language == "Русский" and message.text == "🔙 Вернуться в меню":
        await message.reply("Возвращение в главное меню:", reply_markup=main_menu_kb_ru)
    elif language == "English" and message.text == "🔙 Back to menu":
        await message.reply("Returning to the main menu:", reply_markup=main_menu_kb_en)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)