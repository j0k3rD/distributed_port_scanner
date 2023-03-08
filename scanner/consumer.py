from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import tasks
from .models import Scan, Group
from time import sleep
from channels.db import database_sync_to_async
from django.core import serializers


class ScanConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('WEBSOCKET CONNECTED...')
        print("CHANNEL LAYER...", self.channel_layer)
        print("CHANNEL NAME...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print('GROUP NAME...', self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        print('DISCONNECT', close_code)
        print("CHANNEL LAYER...", self.channel_layer)
        print("CHANNEL NAME...", self.channel_name)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        print('RECEIVE', text_data)
        data = json.loads(text_data)
        # print('DATA', data)
        # message = data
        # print('MESSAGE', message)
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)

        if self.scope['user'].is_authenticated:
            # print('ESTA AUTENTICADO')
            scanner_type = data['scanner_type']
            ipv_type = data['ipv_type']
            ip = data['ip']
            port = data['port']
            if ip != '':
                # print('antes de crear el scan')
                scan = Scan(
                    scanner_type=scanner_type,
                    ipv_type=ipv_type,
                    ip=ip,
                    port=port,
                    group=group
                )
                # print('antes de guardar el scan', scan.id)

                await database_sync_to_async(scan.save)()
                
                # print('Se guarda el scan', scan.id)
                
                tasks.scan_task.delay(scan.id)
                
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'scan.message',
                        'message': {
                            'scan_id': scan.id,
                        }
                    }
                )
        else: 
            await self.send(text_data=json.dumps({
                'message': 'You are not authenticated'
            }))


    async def scan_message(self, event):
        #Serialize the data
        print('SCAN MESSAGE', event)
        message = event['message']
        # print('MESSAGE', message)
        scan = await database_sync_to_async(Scan.objects.get)(id=message['scan_id'])
        # print('SCAN', scan)
        serialized_scan = await database_sync_to_async(serializers.serialize)('json', [scan,])
        # print('SERIALIZED SCAN', serialized_scan)
        await self.send(text_data=json.dumps({
            'message': serialized_scan
        }))