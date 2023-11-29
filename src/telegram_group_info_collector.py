from telethon.sync import TelegramClient
import json
import csv

# Replace these values with your own API ID, API hash, and phone number
api_id = "YOUR_API_ID" # Your Telegram API ID
api_hash = "YOUR_API_HASH" # Your Telegram API hash
phone_number = "YOUR_PHONE_NUMBER" # Your phone number associated with Telegram account

# Create a Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def collect_group_info():
    # Connect to Telegram
    await client.connect()

    # Check if the user is already authorized, otherwise prompt the user to authorize the client
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Enter the code: '))

    # Replace the value below with the username or ID of the group you want to collect information from
    group_entity = await client.get_entity("GROUP_USERNAME_OR_ID") # if use GROUP_ID with this format (-100{ID}) and if use GROUP_USERNAME with this format ("USERNAME")

    # Get and print group information
    group_info = await client.get_entity(group_entity)
    print("Group Name:", group_info.title)
    print("Group Info:", group_info.stringify())

    # Get and print group members
    group_participants = await client.get_participants(group_entity)
    print("\nGroup Members:")
    for participant in group_participants:
        print(participant.stringify())

    # Get and print messages from the group
    messages = []
    # Create an empty list to store message data
    all_messages_data = []

    async for message in client.iter_messages(group_entity, limit=None):
        messages.append(message)
        print(message.stringify())

        # Append message data to the list
        message_data = {
            "Message ID": message.id,
            "Sender ID": message.sender_id,
            "Message Text": message.text,
            "Date": message.date,
            "Media Type": message.media,
            "Reply To": message.reply_to_msg_id,
            "Forwarded From": message.fwd_from,
            "Views": message.views,
            "Forwards": message.forwards,
            "Replies": message.replies.replies if message.replies else None,
            # Add more fields as needed
        }
        all_messages_data.append(message_data)

    # Save collected information to a JSON file
    data = {
        "group_name": group_info.title,
        "group_info": group_info.stringify(),
        "group_members": [participant.stringify() for participant in group_participants],
        "all_messages": [message.stringify() for message in messages]
    }

    with open("group_info.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


    # Save collected information to a CSV file
    csv_file_path = "all_messages.csv"
    with open(csv_file_path, "w", encoding="utf-8-sig", newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=all_messages_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(all_messages_data)


# Run the collection function
with client:
    client.loop.run_until_complete(collect_group_info())