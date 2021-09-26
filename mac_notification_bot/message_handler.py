import subprocess

import telethon

from .settings import settings

class MessageHandler():
    def __init__(self):
        self.chat = None
        self.chat_name = None
        self.sender = None
        self.sender_name = None
        self.message = None
        self.me = None

    async def get_message_info(self, event, client):
        self.chat = await event.get_chat()
        self.sender = await event.get_sender()
        self.me = await client.get_me()

        try:
            if self.chat.last_name is not None:
                self.chat_name = f"{self.chat.first_name} {self.chat.last_name}"
            else:
                self.chat_name = self.chat.first_name

            if self.sender.last_name is not None:
                self.sender_name = f"{self.sender.first_name} {self.sender.last_name}"
            else:
                self.sender_name = self.sender.first_name
        except:
            self.chat_name = "Some chat"
            self.sender_name = self.sender.first_name

    def create_message(self, event):
        if self.sender.is_self or isinstance(self.me.status, telethon.tl.types.UserStatusOnline):
            return False

        if event.message.message == "":
            msg_text = "Voice message"
        else:
            msg_text = event.message.message

        if self.chat.id == self.sender.id:
            self.message = f"✈️ {self.sender_name}: {msg_text}"
        else:
            self.message = f"✈️ [{self.chat_name}] {self.sender_name}: {msg_text}"

        return True

    def send_message_to_imessages(self):
        bash_command = ['osascript', '-e', f'tell application "Messages" to send '
                                           f'"{self.message}" to buddy "{settings.email}"']
        process = subprocess.Popen(bash_command, stdout=subprocess.PIPE)
        output, error = process.communicate()

    async def handle_message(self, event, client):
        await self.get_message_info(event, client)
        if self.create_message(event):
            self.send_message_to_imessages()
        self.__init__()
