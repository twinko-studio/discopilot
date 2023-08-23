import os
import discord
from datetime import datetime, timedelta
from discopilot.configuration_loader import ConfigurationLoader
from discopilot.channel_mapper import ChannelMapper
from discopilot.utils import get_discord_details
from discopilot.ai.summarizer import summarize

# Read the configuration file
config = ConfigurationLoader.load_config()


# Extract Discord details
discord_details = get_discord_details(config)

intents = discord.Intents.default()  
intents.message_content = True
intents.reactions = True
discord_client = discord.Client(intents=intents)

cid_mapper = ChannelMapper(discord_details = discord_details)
report_file_dir = config['Settings']['REPORT_FILE_DIR']



def format_msg_embed(msg):   
    
    # Check if the message has any embeds
    if not msg.embeds:
        return ["The message does not contain any embeds."]
    
    # Create a list of formatted strings for each embed
    formatted_embeds = [
        f"[**{embed.title}**]({embed.url})\n{embed.description}\n\n_{embed.footer.text}_"
        if embed.footer and embed.footer.text else
        f"[**{embed.title}**]({embed.url})\n{embed.description}"
        for embed in msg.embeds
    ]

    # formatted_embeds = [f"**{embed.title}**\n{embed.description}\n{embed.url}" for embed in msg.embeds]

    # If there's only one embed, return its formatted string directly
    if len(formatted_embeds) == 1:
        return formatted_embeds[0]
    
    # If there are multiple embeds, join them with "\n\n" and return
    return "\n\n".join(formatted_embeds)



async def fetch_messages(channel_id, start_time=None, end_time=None, hours=None):
    if channel_id is None:
        print("No channel ID specified!")
        return

    print("start fetching channel", channel_id)
    channel = await discord_client.fetch_channel(channel_id)
    if channel is None:
        print("Channel not found!")
        return

    if hours:
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)

    print(channel_id, "Fetching messages from:", start_time, "to", end_time)

    if start_time and end_time:
        messages = [format_msg_embed(message) async for message in channel.history(after=start_time, before=end_time)]
        messages = "\n\n".join(messages)
    else:
        print("Invalid time range!")
        return
    return messages


def write_to_report(content, output_dir, report_type = "report"):
    if output_dir is None:
        print("No output directory specified!")
        return
    output_dir = os.path.expanduser(output_dir)
    # Ensure the output directory exists
    if not os.path.exists(output_dir):

        print("Creating output directory:", output_dir)
        os.makedirs(output_dir)
    

    # Create a filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if report_type == "report":
        output_file = os.path.join(output_dir, f"report_{timestamp}.md")
        print("Writing full report to file:", output_file)
    elif report_type == "summary":
        output_file = os.path.join(output_dir, f"summary_{timestamp}.md")
        print("Writing abstract to file:", output_file)
    else:
        print("Invalid report type!")
        return
    
    # Write the formatted content to a file
    with open(output_file, "w") as file:
            file.write(content)  

# Assuming you have the fetch_messages and write_to_report functions from before
async def generate_report(start_time=None, end_time=None, hours=24, output_dir = None):
    if output_dir is None:
        print("No output directory specified!")
        return
    output_dir = os.path.expanduser(output_dir)
    # Fetch messages from each channel in order and write to report
    report_content = ["# Table of Contents"]
    details = []
    abstract = []
    channels = dict(config["Report"])
    report_titles = dict(config['Report_Title'])
    
    for channel_name, should_fetch in channels.items():
        if should_fetch.lower() == 'true':
            cid = cid_mapper.get_id_from_name(channel_name)
            print("fetching messages from channel", channel_name, cid)
            msg = await fetch_messages(channel_id=cid, start_time=start_time, end_time = end_time, hours=hours)
            anchor_name = channel_name.lower().replace('_', '') 
            section_title = f"## {report_titles[channel_name]} <a name='{anchor_name}'></a>"
            details.append(section_title)
            if len(msg) > 0:    
                details.append(msg) 
                msg_abstract = summarize(msg)
                abstract.append(msg_abstract)   
                abstract.append("\n")
            else:
                details.append("No news found")

    # Add TOC links and details to the report content
    for idx, channel_name in enumerate(channels.keys()):
        toc_link_anchor = channel_name.lower().replace('_', '')
        toc_link = f"- [{report_titles[channel_name]}](#{toc_link_anchor})"
        report_content.insert(idx+1, toc_link)
    
    report_content.append("\n")
    report_content.extend(abstract)
    report_content.append("\n")
    report_content.extend(details)

    # Write to markdown report
    write_to_report("\n".join(report_content), output_dir = output_dir)
    write_to_report("\n".join(abstract), output_dir = output_dir, report_type = "summary")



@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user.name} (ID: {discord_client.user.id})')
    print('Connected to guild:', discord_client.guilds[0].name)
    await generate_report(hours=24, output_dir=report_file_dir)
    await discord_client.close()

discord_client.run(discord_details['dev_token'])
