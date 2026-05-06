#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.
import collections.abc as c
import typing as t

import pyrogram
from pyrogram.filters import Filter
from pyrogram.types import Message

HANDLER: t.TypeAlias = "c.Callable[[pyrogram.Client, Message], t.Any]"


class OnDeletedMessages:
    def on_deleted_messages(
        self: pyrogram.Client | Filter | None = None,
        filters: Filter | None = None,
        group: int = 0,
    ) -> c.Callable[[HANDLER], HANDLER]:
        """Decorator for handling deleted messages.

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.DeletedMessagesHandler`.

        Parameters:
            filters (:obj:`~pyrogram.filters`, *optional*):
                Pass one or more filters to allow only a subset of messages to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: HANDLER) -> HANDLER:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.DeletedMessagesHandler(func, filters), group
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.DeletedMessagesHandler(func, self),
                        group if filters is None else filters,
                    )
                )

            return func

        return decorator
