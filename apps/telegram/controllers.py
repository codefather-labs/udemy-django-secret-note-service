import asyncio
import ssl
import certifi
import requests

from aiohttp.client import ClientSession
from pyrogram import Client


class AsyncTelegramController:
    def __init__(self, django_server_url: str):
        self.django_server_url = django_server_url
        self.config_url = f"{django_server_url}api/v1/get_last_active_app_config/"
        self.create_message_url = f"{django_server_url}api/v1/create_message"
        self.get_message_url = f"{django_server_url}api/v1/get_message/"

        self.loop = asyncio.get_event_loop()
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())

        self.config = None
        self.session_name = None
        self.api_id = None
        self.api_hash = None
        self.is_bot = None
        self.bot_token = None
        self.is_active = None

        self.client_session = None

    async def gen_session(self):
        return ClientSession(loop=self.loop)

    async def get_config(self):
        session = await self.gen_session()
        response = await session.get(self.config_url, ssl=self.ssl_context)
        await session.close()
        return await response.json()

    async def start_session(self):
        if self.client_session:
            self.client_session.start()

    async def create_client_session(self):
        self.config = await self.get_config()

        self.session_name = self.config['session_name']
        self.api_id = self.config['api_id']
        self.api_hash = self.config['api_hash']
        self.is_bot = self.config['is_bot']
        self.bot_token = self.config['bot_token']
        self.is_active = self.config['is_active']

        self.client_session = Client(
            self.session_name,
            api_id=int(self.api_id),
            api_hash=str(self.api_hash),
            bot_token=str(self.bot_token),
            workers=2,
            workdir='apps/telegram/sessions/'
        )

        def parse_message(message, client_session):
            if message['chat']['type'] == 'private':
                try:
                    # username is required. that's why i'm use try/except
                    # not all users got username. sometimes they don't

                    sender_username = str(message['from_user']['username'])
                    text = str(message['text'])

                    key = text.split(":")[0]
                    value = text.split(':')[1]

                    # incoming message should be like (new:your text)
                    # or (message_id:access_token)

                    if key == 'new':
                        response = requests.post(
                            self.create_message_url,
                            data={
                                "text": str(value)
                            }
                        ).json()

                        msg = f"{response['id']}:{response['access_token']}"
                        client_session.send_message(sender_username, msg)
                    else:
                        value += f":{text.split(':')[2]}"

                        url = f"{self.get_message_url}{key}/{value}/"
                        print(url)
                        response = requests.get(url)

                        # you can customize response anyway you want
                        # inline buttons, inline keyboard - anything

                        if response.status_code == 204:
                            client_session.send_message(sender_username, 'status:object not found')

                        elif response.status_code == 200:
                            msg = response.json()['text']
                            client_session.send_message(sender_username, msg)

                        else:
                            client_session.send_message(sender_username, 'status:bad request')

                except:
                    pass

        @self.client_session.on_message()
        def message_handler(self, message):
            parse_message(message, client_session=self)

        @self.client_session.on_disconnect()
        def disconnect_handler(self, message=None):
            print(message)

        self.client_session.add_handler(message_handler)
        self.client_session.add_handler(disconnect_handler)
