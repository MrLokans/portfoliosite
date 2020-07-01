import operator

from telegram import Update

from apps.apartments_analyzer.models import UserSearchContact


def user_contact_description_from_update(update: Update) -> str:
    from_ = update.message.from_user
    username, first_name, last_name = operator.attrgetter('username', 'first_name', 'last_name')(from_)
    description = []
    if username:
        description = [f"@{username}"]
    else:
        if first_name:
            description.append(first_name)
        if last_name:
            description.append(last_name)
    if not description:
        description = ["Unknown data"]
    return " ".join(description)[:UserSearchContact.MAX_DESCRIPTION_LENGTH]