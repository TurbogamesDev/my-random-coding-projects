import discord, aiohttp, string

TOKEN = "BOT_TOKEN"

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def make_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                return js

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
    if msg.content[:1] == "?":
        command = msg.content.split(' ', 1)[0][1:]
        print(f"command sent by user: {command}")
        if command == "help":
            await msg.channel.send("List of commands:\nKey: (required_parameter) [optional_parameter]\n\n?help - shows this page\n?search (query) - search for mods on the modrinth website and returns the first 15 results\n?game - if you're seeing this ask turbogames to add the description")
        elif command == "search":
            if len(msg.content.split(' ', 1)) == 1:
                await msg.channel.send("please provide a search query")
            elif msg.content.split(' ', 1)[1]:
                response = await make_request(f"https://api.modrinth.com/v2/search?query={msg.content.split(' ', 1)[1]}&facets=[[\"project_type:mod\"]]&limit=15")
                if response['hits']:  
                    message_to_send = f"{len(response['hits'])} result{"s" if len(response['hits']) > 1 else ""} found:\n"
                    for hit in response['hits']:
                        message_to_send += f"\n{hit['title']}:\n{hit['description']}\n"
                    await msg.channel.send(message_to_send)
                else:
                    await msg.channel.send("no results found")
            else:
                await msg.channel.send("invalid usage of command \'search\'")
        elif command == "game":
            await msg.channel.send("cheese")
        else:
            await msg.channel.send("unknown command, type ?help for a list of commands")

    print("sent msg")

client.run(TOKEN)