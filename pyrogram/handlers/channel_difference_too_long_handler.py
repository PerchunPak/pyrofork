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

from .handler import Handler


class ChannelDifferenceTooLongHandler(Handler):
    """Handler for ``ChannelDifferenceTooLong`` event. This event is issued if
    during fetching updates from Telegram, there are too many updates to fetch
    them individually.

    Telegram recommends deleting the entire chat history, and refetching it
    using ``GetHistory``. In reality, since this is an advice for applications,
    they just fetch last 10-20 messages when user opens a chat. This doesn't
    really fit bots, and if you really want to keep the history, you should
    fetch last ~10000 messages.

    See also https://core.telegram.org/constructor/updates.channelDifferenceTooLong

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_channel_difference_too_long` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when channel difference is too long.
            It takes *(client, channel)* as positional arguments (look at the section
            above for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of messages to be passed
            in your callback function.

    Callback parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        update (:obj:`~pyrogram.types.ChannelDifferenceTooLong`):
            The event that triggered this callback.
    """

    def __init__(
        self,
        callback: c.Callable[
            [pyrogram.Client, pyrogram.types.ChannelDifferenceTooLong],
            t.Any,
        ],
        filters: Filter | None = None,
    ):
        super().__init__(callback, filters)
