import os
from datetime import datetime, timedelta
from discopilot.ai.summarizer import summarize

from discord import 
from discopilot.configuration_loader import ConfigurationLoader
from discopilot.channel_mapper import ChannelMapper
from discopilot.utils import get_discord_details

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

    # If there's only one embed, return its formatted string directly
    if len(formatted_embeds) == 1:
        return formatted_embeds[0]
    
    # If there are multiple embeds, join them with "\n\n" and return
    return "\n\n".join(formatted_embeds)



async def fetch_messages(discord_client, channel_id, start_time=None, end_time=None, hours=None):
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


def write_to_report(content, output_dir, prefix = "report"):
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

    output_file = os.path.join(output_dir, f"{prefix}_{timestamp}.md")
    print(f"Writing {prefix} to file:", output_file)

    
    # Write the formatted content to a file
    with open(output_file, "w") as file:
            file.write(content)  

# Assuming you have the fetch_messages and write_to_report functions from before
async def generate_report(config_file = None, start_time=None, end_time=None, 
                        hours=24, output_dir = None, summary = False):

    config = ConfigurationLoader.load_config(config_file = config_file)
    discord_details = get_discord_details(config)
    cid_mapper = ChannelMapper(discord_details = discord_details)

    if output_dir is None:
        print("parsing from config file")
        output_dir = config['Settings']['REPORT_FILE_DIR']
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
                if summary:
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
    
    if summary:
        report_content.append("\n")
        report_content.extend(abstract)

    report_content.append("\n")
    report_content.extend(details)

    # Write to markdown report
    write_to_report("\n".join(report_content), output_dir = output_dir)
    if summary:
        write_to_report("\n".join(abstract), output_dir = output_dir, prefix = "summary")

