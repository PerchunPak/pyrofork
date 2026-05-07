#  PyroFork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of PyroFork.
#
#  PyroFork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroFork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroFork.  If not, see <http://www.gnu.org/licenses/>.
import pyrogram
from pyrogram import raw, utils

from ..object import Object


class ChannelDifferenceTooLong(Object):
    """When fetching updates, Telegram may send ``ChannelDifferenceTooLong``
    event indicating that there are too many updates in one channel.

    Telegram recommends re-fetching the entire history of this channel in this
    case. See also https://core.telegram.org/constructor/updates.channelDifferenceTooLong

    Parameters:
        dialog (:obj:`~pyrogram.types.Dialog`):
            Dialog containing the latest state that can be used to reset the
            channel state.

        channel (:py:obj:`~pyrogram.types.Chat`):
            Channel to which this events applies.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client,
        dialog: pyrogram.types.Dialog,
        channel: pyrogram.types.Chat,
    ):
        super().__init__(client)

        self.dialog = dialog
        self.channel = channel

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        channel_difference: raw.types.updates.ChannelDifferenceTooLong,
        users: dict[int, raw.types.User],
        chats: dict[int, raw.types.Chat],
    ) -> "ChannelDifferenceTooLong":
        messages = {
            utils.get_raw_peer_id(msg.peer_id): msg
            for msg in channel_difference.messages
        }

        dialog = pyrogram.types.Dialog._parse(
            client, channel_difference.dialog, messages, users, chats
        )
        chat_id = utils.get_channel_id(dialog.chat.id)
        channel = pyrogram.types.Chat._parse_channel_chat(client, chats[chat_id])

        return ChannelDifferenceTooLong(
            client=client,
            dialog=dialog,
            channel=channel,
        )
