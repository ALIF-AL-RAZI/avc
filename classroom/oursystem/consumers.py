import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # import pdb
        # pdb.set_trace()
        self.room_group_name = 'Test-Room'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        receive_data_json = json.loads(text_data)
        message = receive_data_json["message"]
        action = receive_data_json["action"]
        if action == 'new-answer' or action == 'new-offer':
            receiver_channel_name = receive_data_json['message']['receiver_channel_name']
            receive_data_json['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'receive_data_json': receive_data_json
                }
            )

        receive_data_json['message']['receiver_channel_name'] = self.channel_name
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'receive_data_json': receive_data_json
            }
        )

    async def send_sdp(self, event):
        receive_data_json = event['receive_data_json']
        await self.send(text_data=json.dumps(receive_data_json))

