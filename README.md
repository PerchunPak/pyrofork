<p align="center">
    <a href="https://github.com/Mayuri-Chan/pyrofok">
        <img src="https://docs.pyrogram.org/_static/pyrogram.png" alt="Pyrofork" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://github.com/Mayuri-Chan">
        Homepage
    </a>
    •
    <a href="https://pyrofork.wulan17.dev">
        Documentation
    </a>
    •
    <a href="https://github.com/Mayuri-Chan/pyrofork/issues">
        Issues
    </a>
    •
    <a href="https://t.me/MayuriChan_Chat">
        Support Chat
    </a>
    •
    <a href="https://t.me/Pyrofork_CH">
        News/Releases
    </a>
</p>

## Pyrofork

> [!CAUTION]
> This is a fork of https://github.com/Mayuri-Chan/pyrofork with my personal patches.
> See [Changes](#changes) for a list of what is different.

> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots

``` python
from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Pyrofork!")


app.run()
```

**Pyrofork** is a modern, elegant and asynchronous [MTProto API](https://pyrofork.wulan17.dev/main/topics/mtproto-vs-botapi)
framework. It enables you to easily interact with the main Telegram API through a user account (custom client) or a bot
identity (bot API alternative) using Python.

### Key Features

- **Ready**: Install Pyrofork with pip and start building your applications right away.
- **Easy**: Makes the Telegram API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by [TgCrypto](https://github.com/pyrogram/tgcrypto), a high-performance cryptography library written in C.
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Telegram's API to execute any official client action and more.

### Installing

``` bash
pip install git+https://github.com/PerchunPak/pyrofork
```

### Changes

This is the list of changes compared to upstream:

- A lot of additional type annotations
- Added `unread_count` to `types.user_and_chats.Chat`
- `Client` can now accept argument `extra`, which is a dict specifically for
  user's information, that is useful to pass around using the `client` object.
- `reply_to` now passes true raw types, instead of pyrofork's types.

  This avoids crashes when you run with debug logs enabled.
- These decorators are now typed:
  - `client.on_callback_query`
  - `client.on_deleted_messages`
  - `client.on_edited_messages`
  - `client.on_message_reaction_count_updated`
  - `client.on_message_reaction_updated`
  - `client.on_message`
- There is now uv.lock with dependencies up to 2025-12-11 (last commit from upstream)
- Added `@client.on_channel_difference_too_long` decorator, that gets called when
  we couldn't fetch all chat updates. See https://core.telegram.org/constructor/updates.channelDifferenceTooLong
- If there were more than ~100 updates for a single channel, the first batch is no longer dropped.
- `pyrogram.storage.Storage` is now properly annotated, with overloads.
- `FloodWait` errors are now handled gracefully with a global backoff per query type.
- `pyrogram.raw.base`, `pyrogram.raw.types` and `pyrogram.raw.functions` now include `__all__`.

### Resources

- Check out the docs at https://pyrofork.wulan17.dev to learn more about Pyrofork, get started right
away and discover more in-depth material for building your client applications.
- Join the official group at https://t.me/MayuriChan_Chat and stay tuned for news, updates and announcements.
