import asyncio
import random
from telethon import TelegramClient
from telethon.tl.types import UserStatusRecently
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import UserAlreadyParticipantError
from telethon.errors import FloodWaitError
from config import API_ID, API_HASH, Sessions
from db import init_db, is_invited, mark_invited,init_group_db


async def get_group_id(session_name):
    async with TelegramClient(session_name, API_ID, API_HASH) as client:
        dialogs = await client.get_dialogs() 
        groups={}
        for d in dialogs: 
            if d.is_group or d.is_channel:
                print(d.name, d.id)
                groups[d.name]=d.id
        return groups
                
async def get_admin_ids(client, group):
    admins = await client.get_participants(
        group,
        filter=ChannelParticipantsAdmins
    )
    return {u.id for u in admins}
  
async def fetch_member(session_name,target_group, my_group):
    init_db()
    count=0
    
    async with TelegramClient(session_name, API_ID, API_HASH) as client:
        admin_id=await get_admin_ids(client,target_group)
        async for user in client.iter_participants(target_group):
            user_id=user.id
            
            if user_id in admin_id:
                continue
            
            if not isinstance(user.status, UserStatusRecently):
                continue

            if user.bot or user.deleted:
                continue
            
            if is_invited(user_id):
                print(f"{user} already invited, skip")
                continue

            try:
                await client(InviteToChannelRequest(my_group, [user_id]))
                
                print(f"invited {user}")
                
                count+=1
                if count>2:
                    break
                
                mark_invited(user_id, None)

                await asyncio.sleep(random.randint(40, 70)) 
                
            except UserAlreadyParticipantError:
                print(f"{user_id} already in group")
                mark_invited(user_id, "already_in_group")
                continue
            except FloodWaitError as e:
                print(f"Flood wait {e.seconds}s")
                await asyncio.sleep(e.seconds)
                break
            
            except Exception as e:
                print(f"fail {user}: {e}")

async def main():
    for session_name,group in Sessions.items():
        
        my_group=group["my_group"]
        print(f"=== {session_name} ===")
        
        groups=await get_group_id(session_name)
        if not groups:
            print(f"{session_name} 沒有群組，跳過")
            continue
        
        init_group_db()
        
        target_group_list = list(groups.values()) 
        
        for i in target_group_list:
            await fetch_member(session_name, i, my_group)
        
        
if __name__ == "__main__":
    asyncio.run(main())
