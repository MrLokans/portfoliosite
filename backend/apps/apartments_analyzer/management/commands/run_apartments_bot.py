import logging
from typing import Tuple

from django.conf import settings as django_settings
from django.core.management.base import BaseCommand
from telegram import ReplyKeyboardMarkup, Update

from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    ConversationHandler,
    CallbackContext,
)

from apps.apartments_analyzer.models import ContactType, UserSearchContact, UserSearch

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

END = ConversationHandler.END

CHOOSING_OPTIONS = "0"
SHOW_SETTINGS, CHANGE_PRICE = "1", "2"
MIN_PRICE, MAX_PRICE = "3", "4"
ROOM_COUNT = "5"


class MenuTitle:
    CHANGE_PRICE = "Изменить цену"
    SHOW_SETTINGS = "Показать настройки"
    ROOM_COUNT = "Количество комнат"
    ENABLE_SEARCH = "Включить поиск"
    DISABLE_SEARCH = "Выключить поиск"


class TelegramSearchRepository:
    def __qs_for_contact_id(self, contact_id: str):
        return UserSearch.objects.filter(
            contacts__contact_type=ContactType.TELEGRAM,
            contacts__contact_identifier=contact_id,
        )

    def get_or_create_for_user(self, contact_id: str) -> Tuple[bool, UserSearch]:
        existing_conversation, created = UserSearchContact.objects.get_or_create(
            contact_type=ContactType.TELEGRAM, contact_identifier=contact_id
        )
        existing_search = existing_conversation.get_existing_search()
        if not existing_search:
            existing_search = UserSearch()
            existing_search.save()
            existing_search.contacts.add(existing_conversation)
        return created, existing_search

    def update_search_price_range(
        self, contact_id: str, min_price: int, max_price: int
    ):
        self.__qs_for_contact_id(contact_id).update(
            min_price=min_price, max_price=max_price,
        )

    def update_min_room_count(self, contact_id: str, min_room_count: int):
        assert min_room_count >= 0
        self.__qs_for_contact_id(contact_id).update(min_rooms=min_room_count,)

    def enable_for_user(self, contact_id: str):
        self.__qs_for_contact_id(contact_id).update(is_active=True)

    def disable_for_user(self, contact_id: str):
        self.__qs_for_contact_id(contact_id).update(is_active=False)


class ApartmentReporterBot:

    _CONTACT_TYPE = ContactType.TELEGRAM
    _START_COMMAND = "start"
    _STOP_COMMAND = "stop"

    def __init__(self, logger, repo: TelegramSearchRepository, access_token: str):
        self.logger = logger
        self.repo = repo
        self.__access_token = access_token

    def keyboard_for_contact(self, contact_id: str):
        _, search = self.repo.get_or_create_for_user(contact_id)
        if search.is_active:
            return [
                [MenuTitle.SHOW_SETTINGS, MenuTitle.CHANGE_PRICE],
                [MenuTitle.ROOM_COUNT, MenuTitle.DISABLE_SEARCH],
            ]
        return [[MenuTitle.ENABLE_SEARCH,]]

    def main_menu_for_contact(self, contact_id):
        return ReplyKeyboardMarkup(
            keyboard=self.keyboard_for_contact(contact_id),
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    def error(self, update: Update, context: CallbackContext):
        """Log Errors caused by Updates."""
        self.logger.error(f'Update "{update}" caused error "{context.error}"')

    def enable_search(self, update: Update, context: CallbackContext):
        self.repo.enable_for_user(update.message.from_user.id)
        update.message.reply_text(
            text="Оповещения о результат включены",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return CHOOSING_OPTIONS

    def disable_search(self, update: Update, context: CallbackContext):
        self.repo.disable_for_user(update.message.from_user.id)
        update.message.reply_text(
            text="Оповещения о результат выключены, но их всегда можно включить обратно",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return CHOOSING_OPTIONS

    def greet_user(self, update: Update, context: CallbackContext):
        user_id = str(update.message.from_user.id)
        is_created, search = self.repo.get_or_create_for_user(contact_id=user_id)
        if is_created:
            update.message.reply_text(
                text="Добро пожаловать в помощник поиска жилья.",
                reply_markup=self.main_menu_for_contact(update.message.from_user.id),
            )
        else:
            update.message.reply_text(
                text=f"Знакомые лица, ваши параметры:\n{search.as_displayed_to_user()}",
                reply_markup=self.main_menu_for_contact(update.message.from_user.id),
            )
        return CHOOSING_OPTIONS

    def show_settings(self, update: Update, context: CallbackContext):
        _, search = self.repo.get_or_create_for_user(update.message.from_user.id)
        update.message.reply_text(
            text=f"Знакомые лица, ваши параметры:\n{search.as_displayed_to_user()}",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return CHOOSING_OPTIONS

    def change_price_settings(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            text="Введите минимальную сумму поиска в $ (0-10.000)"
        )
        return MIN_PRICE

    def change_min_price(self, update: Update, context: CallbackContext):
        try:
            min_price = int(update.message.text)
            assert 0 <= min_price <= 10_000
            context.user_data["min_price"] = min_price
        except (ValueError, AssertionError):
            update.message.reply_text(
                text="Некорректное число, должно быть в диапазоне 0-10000"
            )
            return MIN_PRICE
        update.message.reply_text(
            text=f"Теперь введите максимальное значение цены в $ ({min_price + 1}-{10_001})"
        )
        return MAX_PRICE

    def change_max_price(self, update: Update, context: CallbackContext):
        min_price = int(context.user_data["min_price"])
        try:
            max_price = int(update.message.text)
            assert min_price < max_price <= 10_001
        except (ValueError, AssertionError):
            update.message.reply_text(
                text=f"Некорректное число, должно быть в диапазоне {min_price + 1}-10001"
            )
            return MAX_PRICE
        self.repo.update_search_price_range(
            update.message.from_user.id, min_price, max_price
        )
        update.message.reply_text(
            text=f"Ваши новые параметры цены {min_price}-{max_price}$, спасибо",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return CHOOSING_OPTIONS

    def change_room_settings(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            text=f"Введите минимальное количество комнат (0-8, 0 - ищем отдельную комнату)",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return ROOM_COUNT

    def change_room_count(self, update: Update, context: CallbackContext):
        try:
            room_count = int(update.message.text)
            assert 0 <= room_count <= 8
        except (ValueError, AssertionError):
            update.message.reply_text(
                text=f"Некорректное число, должно быть в диапазоне 0-8, попробуйте еще раз"
            )
            return ROOM_COUNT
        self.repo.update_min_room_count(
            update.message.from_user.id, min_room_count=room_count
        )
        update.message.reply_text(
            text=f"Настройки комнат обновлены, спасибо",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return CHOOSING_OPTIONS

    def stop_conversation(self, update: Update, context: CallbackContext):
        """End Conversation by command."""
        update.message.reply_text("Хорошего дня!")
        return END

    def _init(self):
        updater = Updater(token=self.__access_token, use_context=True)
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler(self._START_COMMAND, self.greet_user)],
            states={
                CHOOSING_OPTIONS: [
                    MessageHandler(
                        Filters.regex(f"^{MenuTitle.CHANGE_PRICE}$"),
                        self.change_price_settings,
                    ),
                    MessageHandler(
                        Filters.regex(f"^{MenuTitle.SHOW_SETTINGS}$"),
                        self.show_settings,
                    ),
                    MessageHandler(
                        Filters.regex(f"^{MenuTitle.ROOM_COUNT}$"),
                        self.change_room_settings,
                    ),
                    MessageHandler(
                        Filters.regex(f"^{MenuTitle.DISABLE_SEARCH}$"),
                        self.disable_search,
                    ),
                    MessageHandler(
                        Filters.regex(f"^{MenuTitle.ENABLE_SEARCH}$"),
                        self.enable_search,
                    ),
                ],
                MIN_PRICE: [MessageHandler(Filters.text, self.change_min_price)],
                MAX_PRICE: [MessageHandler(Filters.text, self.change_max_price)],
                ROOM_COUNT: [MessageHandler(Filters.text, self.change_room_count)],
            },
            fallbacks=[CommandHandler("stop", self.stop_conversation)],
        )
        updater.dispatcher.add_handler(conversation_handler)
        updater.dispatcher.add_error_handler(self.error)
        return updater

    def run(self):
        self.logger.info("Initing routes")
        bot = self._init()
        self.logger.info("Starting polling")
        bot.start_polling()
        bot.idle()


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = ApartmentReporterBot(
            logger=logger,
            repo=TelegramSearchRepository(),
            access_token=django_settings.TELEGRAM_ACCESS_TOKEN,
        )
        bot.run()
