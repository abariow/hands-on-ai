import configparser
import asyncio
import csv
from pyrogram import Client

proxy = {
     "scheme": "http", 
     "hostname": "127.0.0.1",
     "port": 7890,
     "username": "",
     "password": ""
 }

class Telscraper:
    
    def __init__(self, telegram_confs) -> None:
        
        try:
            config = configparser.ConfigParser()
            config.read(telegram_confs)
            self.api_id = config.get('default', 'api_id')
            self.api_hash = config.get('default', 'api_hash')
            self.phone = config.get('default', 'phone')
        except Exception as e:
            print('Exit')
            print(e)
            exit(0)
        
        self.app = Client("my_account", self.api_id, self.api_hash, proxy=proxy)
        self.groups = dict()
        self.members_cache = list()
        self.group_members = dict()


    async def get_groups(self):
        group_types = ['ChatType.SUPERGROUP', 'ChatType.GROUP']
        async with self.app:
            async for dialog in self.app.get_dialogs():
                if str(dialog.chat.type) in group_types:
                    self.groups[dialog.chat.id] = dialog.chat.title
                    

    async def get_members(self, group_id):
        members = []
        async with self.app:
            async for member in self.app.get_chat_members(group_id):
                members.append({
                    'id': member.user.id,
                    'first_name': member.user.first_name,
                    'last_name': member.user.last_name,
                    'username': member.user.username,
                })
        return members
    
    
    async def members_to_csv(self, group_id):
        csv_file_name = f'G{group_id}_members.csv'
        with open(csv_file_name, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(
              csv_file, fieldnames=list(self.group_members[group_id][0].keys()))
            csv_writer.writeheader()
            csv_writer.writerows(self.group_members[group_id])
            print(f'Group(id={group_id}) members saved in {csv_file_name}')


    async def update_members(self, group_id, interval=30):
        while True:
            self.group_members[group_id] = await self.get_members(group_id)
            await self.members_to_csv(group_id)
            print(f'Group(id={group_id}) members updated successfuly')
            await asyncio.sleep(interval * 60)
        

    def run(self):
        self.app.run(self.get_groups())
        for group_id in self.groups:
            print(group_id, self.groups[group_id])
        
        group_id = input('Enter group id: ')
        self.app.run(self.update_members(group_id, interval=1))

if __name__ == '__main__':
  Telscraper('configs.ini').run()
