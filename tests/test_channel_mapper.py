
import os
from discopilot.channel_mapper import ChannelMapper
from discopilot.configuration_loader import ConfigurationLoader

def test_channel_mapper():

    config_file_path = os.path.join(os.path.dirname(__file__), 'data', 'discopilot_config_template.ini')
    config = ConfigurationLoader.load_config(config_file_path)

    discord_details = {
        'token': config['Discord']['DISCORD_BOT_TOKEN'],
        'guild_id': config['Discord']['TS_GUILD_ID'],
        'admin_id': config['Discord']['ADMIN_ID'],
        'emoji_id': config['Discord']['SPECIFIC_REACTION'],
        'command_prefix': config['Discord']['COMMAND_PREFIX'],
        'channel_ids' : config['Discord_CID'],
        'channel_mapping': config['Channel_Mapping'],
        'chinese_mapping': config['Chinese_Mapping']
    }

    mapper = ChannelMapper(discord_details = discord_details)
    assert mapper.get_target_channel_id("RAW_AI_CID") == "411613"
    assert mapper.get_target_channel_id(895094) == "411613"
    assert mapper.get_chinese_channel_id("RAW_AI_CID") == "784524"
    assert mapper.get_chinese_channel_id(895094) == "784524"
    assert mapper.get_id_from_name("RAW_AI_CID") == "895094"
    assert mapper.get_name_from_id(895094) == "RAW_AI_CID"
    assert mapper.get_raw_cid() == ['RAW_AI_CID', 'RAW_DT_CID', 'RAW_WEB3_CID', 'RAW_ROBOTICS_CID', 'RAW_AIDD_CID', 'RAW_RESPONSIBLE_AI_CID']

