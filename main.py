# A program designed to read every incoming message from all groups and channels
# that the account follows, look for specific keywords and forward them to a
# broadcast if they match. I SUCK AT PYTHON

import file_handler as f
import message_processor as process
import file_handler as file
from telethon import TelegramClient, events
from datetime import datetime

# Set API ID, API hash, chat ID
ids = file.get_ids()
api_id = ids[0]
api_hash = ids[1]
chat_id = int(ids[2])

# Load keywords
keywords = file.get_keywords()

# Set date and time variables for start of program
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%d/%m/%Y")

# Set client
client = TelegramClient('anon', api_id, api_hash)

# Print to console with date and time
f.log(f'Session launched at ' + current_date + ', ' + current_time)


@client.on(events.NewMessage)
async def my_event_handler(event):
    chat = await event.get_chat()           # chat entity
    sender = await event.get_sender()       # sender entity
    message_text = event.message.message    # message body
    message_media = event.message.media     # message media (image or video or whatever)

    counts = f.get_counts()                 # messages processed = index 0, matches processed = index 1
    messages_processed = int(counts[0])
    matches_processed = int(counts[1])
    messages_processed += 1

    # Try to get user's name
    try:
        full_name = str(sender.first_name) + ' ' + str(sender.last_name)
    except AttributeError:
        full_name = 'N/A'
        f.log(f'Couldn\'t concatenate first and last names.')

    # Message received
    f.log(f'Message received from user ' + full_name + ': ' + message_text)
    f.log(f'Chat ID to check against: ' + str(chat_id))
    f.log(f'Incoming chat ID: ' + str(chat.id))

    # Check if it's a command
    is_command = process.check_cmd(message_text)
    if chat.id == chat_id and is_command:
        command_success_text = process.process_command(message_text, keywords)
        await client.send_message(715258797, command_success_text)

    # Otherwise search for keywords
    else:
        # If keywords match, send it to the group
        if process.check_for_keywords(message_text, keywords):

            # Only works for channels, not chats with one person.
            try:
                channel_name = str(chat.title)
                f.log(f'Group: ' + channel_name)
            except AttributeError:
                f.log(f'No group name available')
                channel_name = 'N/A'

            # Send notification to monitoring chat
            await client.send_message(chat_id,
                                      '__Message received at ' + current_time + ' on ' + current_date + '\n' +
                                      'Channel name: ' + channel_name + '\n' +
                                      'Posted by: ' + full_name + '__\n\n'
                                      + message_text + '\n\n')

            # Send image or video along with message if there is one - prob a better way to do this
            try:
                await client.send_file(chat_id, message_media)
            except TypeError as error:
                f.log(f'No media sent. Error message: ' + str(error))

            matches_processed += 1

    f.save_counts(messages_processed, matches_processed)

    # line break for console
    f.log(f'---------------------------------------------')


# Start and loop until we disconnect
client.start()
client.run_until_disconnected()
