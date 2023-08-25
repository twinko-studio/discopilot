import discord
from discopilot.configuration_loader import ConfigurationLoader
from discopilot.channel_mapper import ChannelMapper
from discopilot.utils import get_discord_details

def report():
    parser = argparse.ArgumentParser(description="My Python script.")
    parser.add_argument('--start_time', type=str, help="Start time of the report")
    parser.add_argument('--end_time', type=str, help="End time of the report")
    parser.add_argument('--hours', type=int, help="Number of hours to fetch", default = 24)
    parser.add_argument('--summary', action='store_true', help="Include to activate summary mode")
    parser.add_argument('--output_dir', type=str, requried = True, help="Output directory for the report")
    
    args = parser.parse_args()

    intents = discord.Intents.default()  
    intents.message_content = True
    intents.reactions = True
    discord_client = discord.Client(intents=intents)

    @discord_client.event
    async def on_ready():
        print(f'Logged in as {discord_client.user.name} (ID: {discord_client.user.id})')
        print('Connected to guild:', discord_client.guilds[0].name)
        await generate_report(hours=args.hours, output_dir=args.output_dir, summary=args.summary, 
                            start_time=args.start_time, end_time=args.end_time)
        await discord_client.close()

    discord_client.run(discord_details['dev_token'])

if __name__ == "__main__":
    report()


