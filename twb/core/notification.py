import asyncio
from pathlib import Path

import telegram

from twb.core.exceptions import InvalidJSONException
from twb.core.filemanager import FileManager


class _Notification:
    bot = None
    enabled = False
    channel_id = None
    token = None

    def __init__(self) -> None:
        """
        Inicializa a classe de notificações e configura o bot do Telegram, se ativado.
        """
        self.get_config()

        if self.enabled:
            # Cria um novo loop de eventos para as notificações
            self.loop = asyncio.new_event_loop()
            self.bot = telegram.Bot(token=self.token)

    def get_config(self) -> None:
        """
        Carrega as configurações de notificações do arquivo config.json.
        """
        try:
            config = FileManager.load_json_file(f"{Path.cwd()}/config.json")
        except InvalidJSONException:
            # Configuração inválida, desabilita notificações
            config = None
            self.enabled = False
        if config:
            notification_config = config.get("notifications", {})
            self.enabled = notification_config.get("enabled", False)
            self.channel_id = notification_config.get("channel_id")
            self.token = notification_config.get("token")

    def send(self, message: str) -> None:
        """
        Envia uma mensagem de notificação, se as notificações estiverem habilitadas.
        """
        if not self.enabled or not self.bot:
            return

        # Cria e executa uma tarefa assíncrona para enviar a mensagem
        task = self.loop.create_task(self.send_async(message))
        self.loop.run_until_complete(task)

    async def send_async(self, message):
        """
        Envia uma mensagem de forma assíncrona usando o bot o Telegram.
        """
        await self.bot.send_message(chat_id=self.channel_id, text=message)


Notification = _Notification()
