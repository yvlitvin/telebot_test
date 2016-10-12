from telegram import TelegramObject, User, Location


class ChosenInlineResult(TelegramObject):
    """This object represents a Telegram ChosenInlineResult.
    Note:
        * In Python `from` is a reserved word, use `from_user` instead.
    Attributes:
        result_id (str):
        from_user (:class:`telegram.User`):
        query (str):
    Args:
        result_id (str):
        from_user (:class:`telegram.User`):
        query (str):
    """

    def __init__(self,
                 result_id,
                 from_user,
                 query,
                 location=None,
                 inline_message_id=None,
                 **kwargs):
        # Required
        self.result_id = result_id
        self.from_user = from_user
        self.query = query
        # Optionals
        self.location = location
        self.inline_message_id = inline_message_id

    @staticmethod
    def de_json(data, bot):
        """
        Args:
            data (dict):
            bot (telegram.Bot):
        Returns:
            telegram.ChosenInlineResult:
        """
        if not data:
            return None

        # Required
        data['from_user'] = User.de_json(data.pop('from'), bot)
        # Optionals
        data['location'] = Location.de_json(data.get('location'), bot)

        return ChosenInlineResult(**data)

    def to_dict(self):
        """
        Returns:
            dict:
        """
        data = super(ChosenInlineResult, self).to_dict()

        # Required
        data['from'] = data.pop('from_user', None)

        return data