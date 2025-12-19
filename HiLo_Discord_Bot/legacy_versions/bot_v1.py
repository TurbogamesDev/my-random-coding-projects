import discord, aiohttp, math

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

def shorten_number(num):
    if num < 1000:
        return num
    elif num < 10000:
        return str(math.floor(num / 10) / 100) + "K+" 
    elif num < 100000:
        return str(math.floor(num / 100) / 10) + "K+"
    elif num < 1000000:
        return str(math.floor(num / 1000)) + "K+"
    elif num < 10000000:
        return str(math.floor(num / 10000) / 100) + "M+"
    else:
        return str(math.floor(num / 100000) / 10) + "M+"
    

# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)
client = discord.Bot()
original_context = None

class response_to_the_option_selection_menu(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Project 1", style=discord.ButtonStyle.primary)
    async def option_1_button_callback(self, button, interaction):
        global original_context

        if original_context.author == interaction.user:
            print(f"{interaction.user} pressed option 1")
            self.disable_all_items()
            await interaction.response.edit_message(view=self)

            if projects[0]['downloads'] >= projects[1]['downloads']:
                print("...which was correct!")
                embed = discord.Embed(
                    title="Correct answer!",
                    description=f"{projects[0]['title']} has **{shorten_number(projects[0]['downloads'])}** downloads, while {projects[1]['title']} has **{shorten_number(projects[1]['downloads'])}** downloads. Links to the mods have been given below for your reference.",
                    color=discord.Colour.teal(), # Pycord provides a class with default colors you can choose from
                )
                embed.add_field(name = projects[0]['title'], value = f"https://www.modrinth.com/mod/{projects[0]['slug']}")
                embed.add_field(name = projects[1]['title'], value = f"https://www.modrinth.com/mod/{projects[1]['slug']}")
                embed.set_footer(text="Type \'/game\' to play again!")

                await interaction.followup.send("", embed = embed)
            
            else:
                print("...which was wrong.")
                embed = discord.Embed(
                    title="Wrong answer...",
                    description=f"{projects[0]['title']} has **{shorten_number(projects[0]['downloads'])}** downloads, while {projects[1]['title']} has **{shorten_number(projects[1]['downloads'])}** downloads. Links to the mods have been given below for your reference.",
                    color=discord.Colour.red() , # Pycord provides a class with default colors you can choose from
                )
                embed.add_field(name = projects[0]['title'], value = f"https://www.modrinth.com/mod/{projects[0]['slug']}")
                embed.add_field(name = projects[1]['title'], value = f"https://www.modrinth.com/mod/{projects[1]['slug']}")
                embed.set_footer(text="Type \'/game\' to play again!")

                await interaction.followup.send("", embed = embed)
        
        else:
            print(f"blocked {interaction.user} from answering the question of {original_context.author}")
            await interaction.response.send_message("Hey! That question is not for you, so you cant answer that.", ephemeral=True)


    @discord.ui.button(label="Project 2", style=discord.ButtonStyle.primary)
    async def option_2_button_callback(self, button, interaction):
        global original_context

        if original_context.author == interaction.user:
            print(f"{interaction.user} pressed option 1")
            self.disable_all_items()
            await interaction.response.edit_message(view=self)

            if projects[1]['downloads'] >= projects[0]['downloads']:
                print("...which was correct!")
                embed = discord.Embed(
                    title="Correct answer!",
                    description=f"{projects[1]['title']} has **{shorten_number(projects[1]['downloads'])}** downloads, while {projects[0]['title']} has **{shorten_number(projects[0]['downloads'])}** downloads. Links to the mods have been given below for your reference.",
                    color=discord.Colour.green(), # Pycord provides a class with default colors you can choose from
                )
                embed.add_field(name = projects[1]['title'], value = f"https://www.modrinth.com/mod/{projects[1]['slug']}")
                embed.add_field(name = projects[0]['title'], value = f"https://www.modrinth.com/mod/{projects[0]['slug']}")
                embed.set_footer(text="Type \'/game\' to play again!")

                await interaction.followup.send("", embed = embed)
            
            else:
                print("...which was wrong.")
                embed = discord.Embed(
                    title="Wrong answer...",
                    description=f"{projects[1]['title']} has **{shorten_number(projects[1]['downloads'])}** downloads, while {projects[0]['title']} has **{shorten_number(projects[0]['downloads'])}** downloads. Links to the mods have been given below for your reference.",
                    color=discord.Colour.red(), # Pycord provides a class with default colors you can choose from
                )
                embed.add_field(name = projects[1]['title'], value = f"https://www.modrinth.com/mod/{projects[1]['slug']}")
                embed.add_field(name = projects[0]['title'], value = f"https://www.modrinth.com/mod/{projects[0]['slug']}")
                embed.set_footer(text="Type \'/game\' to play again!")

                await interaction.followup.send("", embed = embed)
        
        else:
            print(f"blocked {interaction.user} from answering the question of {original_context.author}")
            await interaction.response.send_message("Hey! That question is not for you, so you cant answer that.", ephemeral=True)

projects = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command(description = "Starts the game")
async def game(ctx):
    global original_context
    global projects
    print(f"{ctx.author} started the game!")
    while True:
        response = await make_request("https://api.modrinth.com/v2/projects_random?count=4")
        projects = response
        print(f"recieved {len(projects)} projects")
        if len(projects) >= 2:
            main_embed = discord.Embed(
                title = "Higher or Lower?",
                description = "Given below are two projects. Select the project which you think has more downloads. If both have an equal amount of downloads, you automatically get this question right.",
                color = discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
            )

            embed1 = discord.Embed(
                title = projects[0]['title'],
                description = projects[0]['description'],
                color = discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
            )
            embed1.set_thumbnail(url = projects[0]['icon_url'])
            
            embed2 = discord.Embed(
                title = projects[1]['title'],
                description = projects[1]['description'],
                color = discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
            )
            embed2.set_thumbnail(url = projects[1]['icon_url'])
            
            original_context = ctx
            await ctx.respond("", view=response_to_the_option_selection_menu(), embeds = [main_embed, embed1, embed2])
            break
        
        print(f"failed to get all 2 projects, only got {len(projects)}. Retrying...")


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
client.run(TOKEN)