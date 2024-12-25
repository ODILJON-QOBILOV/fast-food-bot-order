from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
from app.database import get_user, start_db  # Make sure this function is available and working

class CustomI18nMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: tuple) -> str:
        start_db()
        """
        Determines the language of the user based on their database entry.
        Returns a language code such as 'ru', 'uz', or 'en'.
        """
        user = types.User.get_current()  # Get the current user
        language = "en"  # Default language (if no user or language is set)

        # Get user from the database by their user_id
        db_user = get_user(user.id)

        if db_user and db_user[3]:  # Assuming the 4th column contains the language
            language_map = {"Русский": "ru", "O'zbek": "uz", "English": "en"}
            language = language_map.get(db_user[3], "en")  # Default to 'en' if not found
        return language
