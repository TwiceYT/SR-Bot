import nextcord
from nextcord.ext import commands, application_checks
import os
import requests
from dotenv import load_dotenv, dotenv_values

# Database file
load_dotenv(dotenv_path='config\config.env')



intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)



def search_programs(query):
    url = f"https://api.sr.se/api/v2/search?q={query}&format=json"
    response = requests.get(url)
    data = response.json()
    return data['programs']

def get_episodes(program_id):
    url = f"https://api.sr.se/api/v2/programs/{program_id}/episodes?format=json"
    response = requests.get(url)
    data = response.json()
    return data['episodes']  # lista med avsnitt


class LiveRadio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    Guild_ID = 1246504726044999903

    SR_CHANNELS = {
    "P1": "https://sverigesradio.se/topsy/direkt/132-hi.mp3",
    "P2": "https://sverigesradio.se/topsy/direkt/163-hi.mp3",
    "P3": "https://sverigesradio.se/topsy/direkt/164-hi.mp3",
    "P4": "https://sverigesradio.se/topsy/direkt/179-hi.mp3",
}

    @nextcord.slash_command(name="live", description="Start a live radio stream", guild_ids=[Guild_ID])
    async def live(self, i: nextcord.Interaction, kanal: str):
        """Get the current live radio stream URL."""
        kanal = kanal.upper()
        if kanal not in self.SR_CHANNELS:
            await i.response.send_message(f"Invalid channel name: {kanal}. Available channels: {', '.join(self.SR_CHANNELS.keys())}", ephemeral=True)
            return
        
        if i.user.voice is None:
            await i.response.send_message("You must be in a voice channel to use this command.", ephemeral=True)
            return
        
        # Play the live radio stream
        if i.guild.voice_client:
            await i.guild.voice_client.disconnect()
        voice_channel = i.user.voice.channel
        vc = await voice_channel.connect()

        stream_url = self.SR_CHANNELS[kanal]
        if not stream_url:
            await i.response.send_message(f"No live stream available for {kanal}.", ephemeral=True)
            return
        
        vc.play(
            nextcord.FFmpegPCMAudio(stream_url), 
            after=lambda e: print(f"Finished playing: {e}")
            )
        
        await i.response.send_message(f"Now playing {kanal} live radio stream.", ephemeral=True)

        

    @nextcord.slash_command(name="stop", description="Stop the live radio stream")
    async def stop(self, i: nextcord.Interaction):
        """Stop the live radio stream."""
        await i.guild.voice_client.disconnect()
        await i.response.send_message("Stopped the live radio stream.", ephemeral=True)
        
    @nextcord.slash_command(name="radiochannels", description="Get a list of available radio channels", guild_ids=[Guild_ID])
    async def radiochannels(self, i: nextcord.Interaction):
        """Get a list of available radio channels."""
        channels_list = "\n".join([f"{name}: {url}" for name, url in self.SR_CHANNELS.items()])
        await i.response.send_message(f"Available radio channels:\n{channels_list}", ephemeral=True)

def setup(bot: commands.Bot):
    print("LiveRadio Cog Registered")
    bot.add_cog(LiveRadio(bot))