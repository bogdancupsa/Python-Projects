from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MonitoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connect")
        await self.channel_layer.group_add(
            "alert_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f"WebSocket disconnect; close_code: {close_code}")
        await self.channel_layer.group_discard(
            "alert_group",
            self.channel_name
        )

    async def send_alert(self, event):   
        print("MA bate vantul in fata")   
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'device_id': event['device_id']
        }))