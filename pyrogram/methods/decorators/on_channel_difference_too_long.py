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
from pyrogram.types import ChannelDifferenceTooLong

HANDLER: t.TypeAlias = "c.Callable[[pyrogram.Client, ChannelDifferenceTooLong], t.Any]"


class OnChannelDifferenceTooLong:
    def on_channel_difference_too_long(
        self: pyrogram.Client | Filter | None = None,
        filters: Filter | None = None,
        group: int = 0,
    ) -> c.Callable[[HANDLER], HANDLER]:
        """Decorator for ``ChannelDifferenceTooLong`` event. This event is
        issued if during fetching updates from Telegram, there are too many
        updates to fetch them individually.

        Telegram recommends deleting the entire chat history, and refetching it
        using ``GetHistory``. In reality, since this is an advice for
        applications, they just fetch last 10-20 messages when user opens
        a chat. This doesn't really fit bots, and if you really want to keep
        the history, you should fetch last ~10000 messages.

        See also https://core.telegram.org/constructor/updates.channelDifferenceTooLong

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.ChannelDifferenceTooLong`.

        Parameters:
            filters (:obj:`~pyrogram.filters`, *optional*):
                Pass one or more filters to allow only a subset of updates to be passed in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Callback parameters:
            client (:obj:`~pyrogram.Client`):
                The Client itself, useful when you want to call other API methods inside the message handler.

            update (:obj:`~pyrogram.types.ChannelDifferenceTooLong`):
                The event that triggered this callback.
        """

        def decorator(func: HANDLER) -> HANDLER:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.ChannelDifferenceTooLongHandler(func, filters),
                    group,
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.ChannelDifferenceTooLongHandler(func, self),
                        group if filters is None else filters,
                    )
                )

            return func

        return decorator
