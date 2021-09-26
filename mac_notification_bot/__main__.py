import asyncio

from telethon import TelegramClient
from telethon import events

from .settings import settings
from .message_handler import MessageHandler


client = TelegramClient(settings.username, settings.api_id, settings.api_hash)
message_handler = MessageHandler()


@client.on(events.NewMessage)
async def my_event_handler(event):
    await message_handler.handle_message(event, client)


async def connect():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(settings.phone)
        try:
            await client.sign_in(settings.phone, input('Enter the code: '))
        except:
            await client.sign_in(password=input('Password: '))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(connect())
    loop.run_forever()
