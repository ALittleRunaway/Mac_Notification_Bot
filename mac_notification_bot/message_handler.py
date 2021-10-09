import subprocess

import telethon
from telethon.tl.types import Channel
from telethon.tl.types import User
from telethon.tl.types import UserStatusOnline
from telethon.tl.types import MessageMediaPhoto

from .settings import settings


class MessageHandler():
    def __init__(self, logger):
        self.chat = None
        self.sender = None
        self.me = None
        self.logger = logger

    async def get_message_info(self, event, client):
        self.chat = await event.get_chat()
        self.sender = await event.get_sender()
        self.me = await client.get_me()

    def validate_message(self, event):
        # something weird (usually channels)
        if self.chat is None or self.sender is None:
            return False
        # the channel's post
        if isinstance(self.chat, Channel) and isinstance(self.sender, Channel):
            return False
        # my message
        if isinstance(self.sender, User):
            if self.sender.is_self:
                return False
        # I'm already online
        if isinstance(self.me.status, UserStatusOnline):
            return False
        return True

    def prepare_data(self, event):
        # it's expected that the sender is always user
        if self.sender.last_name is not None:
            sender = f"{self.sender.first_name} {self.sender.last_name}"
        else:
            sender = self.sender.first_name

        if isinstance(self.chat, User):  # private chat
            dialog = sender
        else:   # group
            dialog = self.chat.title

        return dialog, sender

    def create_message(self, event, dialog, sender):
        if (msg := event.message.message) != "":   # simple text, emoji
            msg_text = msg
        else:
            if isinstance(event.message.media, MessageMediaPhoto):  # photo
                msg_text = "Photo"
            else:
                if event.message.media.document.mime_type == "audio/ogg":  # voice message
                    msg_text = "Voice message"
                elif event.message.media.document.mime_type == "image/webp":  # sticker
                    msg_text = f"Sticker {event.message.media.document.attributes[1].alt}"
                elif event.message.media.document.mime_type == "video/mp4":
                    if len(event.message.media.document.attributes) < 3:  # video
                        msg_text = "Video"
                    else:  # gif
                        msg_text = "GIF"
                elif "application" in event.message.media.document.mime_type:  # document
                    msg_text = "Document"
                else:  # something unexpected
                    msg_text = "Message"

        if dialog == sender:
            message = f"✈️ {dialog}: {msg_text}"
        else:
            message = f"✈️ [{dialog}] {sender}: {msg_text}"

        return message

    def send_message_to_imessages(self, message):
        bash_command = ['osascript', '-e', f'tell application "Messages" to send '
                                           f'"{message}" to buddy "{settings.email}"']
        process = subprocess.Popen(bash_command, stdout=subprocess.PIPE)
        output, error = process.communicate()

    async def handle_message(self, event, client):
        await self.get_message_info(event, client)
        if self.validate_message(event):
            self.send_message_to_imessages(self.create_message(event, *self.prepare_data(event)))
        self.__init__(self.logger)
