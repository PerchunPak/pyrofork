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

import base64
import datetime as dt
import struct
import typing as t
from abc import ABC, abstractmethod

from pyrogram.raw.types.input_peer_channel import InputPeerChannel
from pyrogram.raw.types.input_peer_chat import InputPeerChat
from pyrogram.raw.types.input_peer_user import InputPeerUser

InputPeer: t.TypeAlias = InputPeerUser | InputPeerChat | InputPeerChannel


class Storage(ABC):
    SESSION_STRING_FORMAT = ">BI?256sQ?"
    USERNAME_TTL = dt.timedelta(days=1).total_seconds()

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def open(self) -> None:
        """Open connection."""

    @abstractmethod
    async def save(self) -> None:
        """Save current data.

        Should update columns ``date`` in ``sessions`` table.
        """

    @abstractmethod
    async def close(self) -> None:
        """Close connection."""

    @abstractmethod
    async def delete(self) -> None:
        """Delete all data."""

    @abstractmethod
    async def update_peers(self, peers: list[tuple[int, int, str, str, str]]) -> None:
        """Update peers.

        Parameters:
            peers: A tuple containing the following items:
                - id (signed 64 bit): The pyrogram ID of the entity.
                - access_hash (signed 64 bit): The telegram access hash.
                - type (str): Peer type.
                - username (str): Peer username.
                - phone_number (str): Peer phone_number.
        """

    @abstractmethod
    async def update_usernames(self, usernames: list[tuple[int, str]]) -> None:
        """Update peer usernames.

        Parameters:
            usernames: A list with tuples containing the following items:
                - peer_id (signed 64 bit): The pyrogram ID of the peer.
                - username (str): Peer username.
        """

    @t.overload
    async def update_state(
        self, update_state: tuple[int, int, int | None, int, int | None], /
    ) -> None: ...
    @t.overload
    async def update_state(
        self, update_state: None = None, /
    ) -> list[tuple[int, int, int | None, int, int | None]]: ...

    @abstractmethod
    async def update_state(
        self,
        update_state: tuple[int, int, int | None, int, int | None] | None = None,
        /,
    ) -> list[tuple[int, int, int | None, int, int | None]] | None:
        """Get or set the update state of the current session.

        Parameters:
            update_state:
                A tuple or None. If user provided tuple - update the data,
                otherwise return ``update_state`` from storage.
                Tuple contains the following items:
                - id (signed 64 bit): The pyrogram ID of the entity.
                - pts (unsigned 32 bit): The telegram PTS value.
                - qts (int | None): The telegram QTS value, currently not implemented.
                - date (unsigned 32 bit): UNIX timestamp.
                - seq (int | None): Sequence number, currently not implemented.
        """

    @abstractmethod
    async def remove_state(self, chat_id: int) -> None:
        """Remove ``update_state`` by ID.

        Parameters:
            chat_id: signed 64 bit integer.
        """

    @abstractmethod
    async def get_peer_by_id(self, peer_id: int) -> InputPeer:
        """Get peer by ID.

        Should raise ``KeyError`` if not found.

        Parameters:
            peer_id: signed 64 bit integer.
        """

    @abstractmethod
    async def get_peer_by_username(self, username: str) -> InputPeer:
        """Get peer by username.

        Should raise ``KeyError`` if not found.

        Parameters:
            peer_id: signed 64 bit integer.
        """

    @abstractmethod
    async def get_peer_by_phone_number(self, phone_number: str) -> InputPeer:
        """Get peer by phone number.

        Should raise ``KeyError`` if not found.

        Parameters:
            peer_id: signed 64 bit integer.
        """

    @t.overload
    async def dc_id(self, value: None = None, /) -> int: ...
    @t.overload
    async def dc_id(self, value: int, /) -> None: ...

    @abstractmethod
    async def dc_id(self, value: int | None = None, /) -> int | None:
        """Set or return ``dc_id`` from ``sessions`` table.

        Type: signed 32 bit integer.
        """

    @t.overload
    async def api_id(self, value: None = None, /) -> int: ...
    @t.overload
    async def api_id(self, value: int, /) -> None: ...

    @abstractmethod
    async def api_id(self, value: int | None = None, /) -> int | None:
        """Set or return ``api_id`` from ``sessions`` table.

        Type: signed 32 bit integer.
        """

    @t.overload
    async def test_mode(self, value: None = None, /) -> bool: ...
    @t.overload
    async def test_mode(self, value: bool, /) -> None: ...

    @abstractmethod
    async def test_mode(self, value: bool | None = None, /) -> bool | None:
        """Set or return ``test_mode`` from ``sessions`` table."""

    @t.overload
    async def auth_key(self, value: None = None, /) -> bytes: ...
    @t.overload
    async def auth_key(self, value: bytes, /) -> None: ...

    @abstractmethod
    async def auth_key(self, value: bytes | None = None, /) -> bytes | None:
        """Set or return ``auth_key`` from ``sessions`` table."""

    @t.overload
    async def date(self, value: None = None, /) -> int: ...
    @t.overload
    async def date(self, value: int, /) -> None: ...

    @abstractmethod
    async def date(self, value: int | None = None, /) -> int | None:
        """Set or return ``date`` from ``sessions`` table.

        Type: unsigned 32 bit integer, UNIX timestamp.
        """

    @t.overload
    async def user_id(self, value: None = None, /) -> int: ...
    @t.overload
    async def user_id(self, value: int, /) -> None: ...

    @abstractmethod
    async def user_id(self, value: int | None = None, /) -> int | None:
        """Set or return ``user_id`` from ``sessions`` table.

        Type: signed 64 bit integer.
        """

    @t.overload
    async def is_bot(self, value: None = None, /) -> bool: ...
    @t.overload
    async def is_bot(self, value: bool, /) -> None: ...

    @abstractmethod
    async def is_bot(self, value: bool | None = None, /) -> bool | None:
        """Set or return ``is_bot`` from ``sessions`` table."""

    async def export_session_string(self) -> str:
        packed = struct.pack(
            self.SESSION_STRING_FORMAT,
            await self.dc_id(),
            await self.api_id(),
            await self.test_mode(),
            await self.auth_key(),
            await self.user_id(),
            await self.is_bot(),
        )

        return base64.urlsafe_b64encode(packed).decode().rstrip("=")
