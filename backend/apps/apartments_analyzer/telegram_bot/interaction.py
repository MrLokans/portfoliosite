from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

from apps.apartments_analyzer.models import ContactType
from apps.apartments_analyzer.tasks import send_apartments_to_new_user
from apps.apartments_analyzer.telegram_bot.constants import MenuState, MenuTitle, END
from apps.apartments_analyzer.telegram_bot.utils import user_contact_description_from_update
from apps.apartments_analyzer.telegram_bot.repository import TelegramSearchRepository


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
        return MenuState.CHOOSING_OPTIONS

    def disable_search(self, update: Update, context: CallbackContext):
        self.repo.disable_for_user(update.message.from_user.id)
        update.message.reply_text(
            text="Оповещения о результат выключены, но их всегда можно включить обратно",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return MenuState.CHOOSING_OPTIONS

    def greet_user(self, update: Update, context: CallbackContext):
        user_id = str(update.message.from_user.id)
        is_created, search = self.repo.get_or_create_for_user(contact_id=user_id)
        if is_created:
            update.message.reply_text(
                text=(
                    "Добро пожаловать в помощник поиска жилья. "
                    "Введите интересующие вас значения и мы оповестим вас "
                    "как только появятся подходящие квартиры."
                ),
                reply_markup=self.main_menu_for_contact(update.message.from_user.id),
            )
            # Report in a minute to make sure user is with us and gets some results instantly
            send_apartments_to_new_user.send_with_options(args=(user_id,), delay=60_000)
        else:
            update.message.reply_text(
                text=f"Знакомые лица, ваши параметры:\n{search.as_displayed_to_user()}",
                reply_markup=self.main_menu_for_contact(update.message.from_user.id),
            )
        self.repo.set_contact_description(user_id, user_contact_description_from_update(update))
        return MenuState.CHOOSING_OPTIONS

    def show_settings(self, update: Update, context: CallbackContext):
        _, search = self.repo.get_or_create_for_user(update.message.from_user.id)
        update.message.reply_text(
            text=f"Знакомые лица, ваши параметры:\n{search.as_displayed_to_user()}",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return MenuState.CHOOSING_OPTIONS

    def change_price_settings(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            text="Введите минимальную сумму поиска в $ (0-10.000)"
        )
        return MenuState.MIN_PRICE

    def change_min_price(self, update: Update, context: CallbackContext):
        try:
            min_price = int(update.message.text)
            assert 0 <= min_price <= 10_000
            context.user_data["min_price"] = min_price
        except (ValueError, AssertionError):
            update.message.reply_text(
                text="Некорректное число, должно быть в диапазоне 0-10000"
            )
            return MenuState.MIN_PRICE
        update.message.reply_text(
            text=f"Теперь введите максимальное значение цены в $ ({min_price + 1}-{10_001})"
        )
        return MenuState.MAX_PRICE

    def change_max_price(self, update: Update, context: CallbackContext):
        min_price = int(context.user_data["min_price"])
        try:
            max_price = int(update.message.text)
            assert min_price < max_price <= 10_001
        except (ValueError, AssertionError):
            update.message.reply_text(
                text=f"Некорректное число, должно быть в диапазоне {min_price + 1}-10001"
            )
            return MenuState.MAX_PRICE
        self.repo.update_search_price_range(
            update.message.from_user.id, min_price, max_price
        )
        update.message.reply_text(
            text=f"Ваши новые параметры цены {min_price}-{max_price}$, спасибо",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return MenuState.CHOOSING_OPTIONS

    def change_room_settings(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            text=f"Введите минимальное количество комнат (0-8, 0 - ищем отдельную комнату)",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return MenuState.ROOM_COUNT

    def change_room_count(self, update: Update, context: CallbackContext):
        try:
            room_count = int(update.message.text)
            assert 0 <= room_count <= 8
        except (ValueError, AssertionError):
            update.message.reply_text(
                text=f"Некорректное число, должно быть в диапазоне 0-8, попробуйте еще раз"
            )
            return MenuState.ROOM_COUNT
        self.repo.update_min_room_count(
            update.message.from_user.id, min_room_count=room_count
        )
        update.message.reply_text(
            text=f"Настройки комнат обновлены, спасибо",
            reply_markup=self.main_menu_for_contact(update.message.from_user.id),
        )
        return MenuState.CHOOSING_OPTIONS

    def stop_conversation(self, update: Update, context: CallbackContext):
        """End Conversation by command."""
        update.message.reply_text("Хорошего дня!")
        return END

    def _init(self):
        updater = Updater(token=self.__access_token, use_context=True)
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler(self._START_COMMAND, self.greet_user)],
            states={
                MenuState.CHOOSING_OPTIONS: [
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
                MenuState.MIN_PRICE: [MessageHandler(Filters.text, self.change_min_price)],
                MenuState.MAX_PRICE: [MessageHandler(Filters.text, self.change_max_price)],
                MenuState.ROOM_COUNT: [MessageHandler(Filters.text, self.change_room_count)],
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