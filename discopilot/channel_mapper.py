from discopilot.configuration_loader import ConfigurationLoader
from discopilot.utils import get_discord_details

class ChannelMapper:
    """
    Maps channel names to target filterd channel and target Chinese channel.
    """

    def __init__(self, discord_details):
        if discord_details is None:
             config = ConfigurationLoader.load_config()
             discord_details = get_discord_details(config)
             
        self.channel_ids = discord_details['channel_ids']
        self.channel_mapping = discord_details['channel_mapping']
        self.chinese_mapping = discord_details['chinese_mapping']

    def get_id_from_name(self, channel_name):
        """Given a channel name, returns its ID."""
        return self.channel_ids.get(channel_name)

    def get_name_from_id(self, channel_id):
        """Given a channel ID, returns its name."""
        for name, id_ in self.channel_ids.items():
            if id_ == str(channel_id):
                return name
        return None

    def get_target_channel_id(self, identifier):
        """Given a channel name or ID, returns the mapped target channel ID."""
        if isinstance(identifier, int):  # If an ID is passed
            identifier = self.get_name_from_id(identifier)
        mapped_name = self.channel_mapping.get(identifier)
        return self.channel_ids.get(mapped_name)

    def get_chinese_channel_id(self, identifier):
        """Given a channel name or ID, returns the mapped Chinese channel ID."""
        if isinstance(identifier, int):  # If an ID is passed
            identifier = self.get_name_from_id(identifier)
        mapped_name = self.chinese_mapping.get(identifier)
        return self.channel_ids.get(mapped_name)

    def get_all_raw_cid(self):
        """Returns the raw channel ID."""
        return list(self.channel_mapping.keys())

    def get_all_target_cid(self):
        """Returns the target channel ID."""
        return list(self.channel_mapping.values())

