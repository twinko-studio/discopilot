import os
import discord
from datetime import datetime, timedelta
from discopilot.configuration_loader import ConfigurationLoader


# Read the configuration file
config = ConfigurationLoader.load_config()


# Extract Discord details
discord_details = {
    'token': config['Discord']['DISCORD_BOT_TOKEN'],
    'dev_token': config['Discord']['DISCORD_BOT_DEV_TOKEN'],
    'admin_id': config['Discord']['ADMIN_ID'],
    'emoji_id': config['Discord']['SPECIFIC_REACTION']
}

intents = discord.Intents.default()  
intents.message_content = True
intents.reactions = True
discord_client = discord.Client(intents=intents)

ai_cid = 1142141161373437953


def format_msg_embed(msg):   
    
    # Check if the message has any embeds
    if not msg.embeds:
        return ["The message does not contain any embeds."]
    
    # Create a list of formatted strings for each embed
    formatted_embeds = [f"**{embed.title}**\n{embed.description}\n{embed.url}" for embed in msg.embeds]

    # If there's only one embed, return its formatted string directly
    if len(formatted_embeds) == 1:
        return formatted_embeds[0]
    
    # If there are multiple embeds, join them with "\n\n" and return
    return "\n\n".join(formatted_embeds)

def write_to_report(content, output_dir = "~/reports/"):
    output_dir = os.path.expanduser(output_dir)
    # Ensure the output directory exists
    if not os.path.exists(output_dir):

        print("Creating output directory:", output_dir)
        os.makedirs(output_dir)
    

    # Create a filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"report_{timestamp}.md")
    print("Writing to file:", output_file)
    
    # Write the formatted content to a file
    with open(output_file, "w") as file:
            file.write(content)  

async def fetch_messages(channel_id, start_time=None, end_time=None, hours=None):
    channel = await discord_client.fetch_channel(channel_id)
    if channel is None:
        print("Channel not found!")
        return

    if hours:
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)

    print("Fetching messages from:", start_time, "to", end_time)

    if start_time and end_time:
        messages = [format_msg_embed(message) async for message in channel.history(after=start_time, before=end_time)]
        messages = "\n\n".join(messages)
    else:
        print("Invalid time range!")
        return


    return messages

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user.name} (ID: {discord_client.user.id})')
    print('Connected to guild:', discord_client.guilds[0].name)
    
    messages = await fetch_messages(channel_id = ai_cid, hours=24)
    print(messages)
    write_to_report(messages)  
    await discord_client.close()

discord_client.run(discord_details['dev_token'])
