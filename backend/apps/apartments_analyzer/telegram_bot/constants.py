from telegram.ext import ConversationHandler


class MenuState:
    CHOOSING_OPTIONS = "0"
    SHOW_SETTINGS = "1"
    CHANGE_PRICE = "2"
    MIN_PRICE = "3"
    MAX_PRICE = "4"
    ROOM_COUNT = "5"

END = ConversationHandler.END



class MenuTitle:
    CHANGE_PRICE = "Изменить цену"
    SHOW_SETTINGS = "Показать настройки"
    ROOM_COUNT = "Количество комнат"
    ENABLE_SEARCH = "Включить поиск"
    DISABLE_SEARCH = "Выключить поиск"
