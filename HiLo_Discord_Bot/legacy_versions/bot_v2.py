import discord, aiohttp, math

TOKEN = "BOT_TOKEN"

print("Program Running!")

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

client = discord.Bot()

game_state = {}

async def show_mod_selection_screen(ctx, index_number):
    main_embed = discord.Embed(
        title = "Higher or Lower?",
        description = "Given below are two projects. Select the project which you think has more downloads. If both have an equal amount of downloads, you automatically get this question right.",
        color = discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )

    embed1 = discord.Embed(
        title = game_state[ctx.author.name]['projects'][index_number]['title'],
        description = game_state[ctx.author.name]['projects'][index_number]['description'],
        color = discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    embed1.set_thumbnail(url = game_state[ctx.author.name]['projects'][index_number]['icon_url'])

    embed2 = discord.Embed(
        title = game_state[ctx.author.name]['projects'][index_number + 1]['title'],
        description = game_state[ctx.author.name]['projects'][index_number + 1]['description'],
        color = discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    embed2.set_thumbnail(url = game_state[ctx.author.name]['projects'][index_number + 1]['icon_url'])

    await ctx.respond("", view=response_to_the_option_selection_menu(ctx), embeds = [main_embed, embed1, embed2])

class response_to_the_option_selection_menu(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx
        print(self.ctx)

    @discord.ui.button(label="Project 1", style=discord.ButtonStyle.primary)
    async def option_1_button_callback(self, button, interaction):
        global game_state
        
        if self.ctx.author == interaction.user:
            print(f"{interaction.user} pressed option 1")
            # self.disable_all_items()
            # await interaction.response.edit_message(content = "Loading...")
            # await interaction.response.defer()
            await interaction.message.edit(content = "Loading...", embed = None, view = None)

            if game_state[self.ctx.author.name]['projects'][0]['downloads'] >= game_state[self.ctx.author.name]['projects'][1]['downloads']:
                print("...which was correct!")
                embed = discord.Embed(
                    title="Correct answer!",
                    description=f"{game_state[self.ctx.author.name]['projects'][0]['title']} has **{shorten_number(game_state[self.ctx.author.name]['projects'][0]['downloads'])}** downloads, while {game_state[self.ctx.author.name]['projects'][1]['title']} has **{shorten_number(game_state[self.ctx.author.name]['projects'][1]['downloads'])}** downloads. Links to the mods have been given below for your reference.",
                    color=discord.Colour.green(), # Pycord provides a class with default colors you can choose from
                )
                embed.add_field(name = game_state[self.ctx.author.name]['projects'][0]['title'], value = f"https://www.modrinth.com/mod/{game_state[self.ctx.author.name]['projects'][0]['slug']}")
                embed.add_field(name = game_state[self.ctx.author.name]['projects'][1]['title'], value = f"https://www.modrinth.com/mod/{game_state[self.ctx.author.name]['projects'][1]['slug']}")
                embed.set_footer(text="Type \'/game\' to play again!")

                # msg = await interaction.original_response()
                # await msg.edit("", embed = embed)
                await interaction.message.edit(content = "", embed = embed, view = None)
            
            else:
                print("...which was wrong.")
                embed = discord.Embed(
                    title="Wrong answer...",
                    description=f"{game_state[self.ctx.author.name]['projects'][0]['title']} has **{shorten_number(game_state[self.ctx.author.name]['projects'][0]['downloads'])}** downloads, while {game_state[self.ctx.author.name]['projects'][1]['title']} has **{shorten_number(game_state[self.ctx.author.name]['projects'][1]['downloads'])}** downloads. Links to the mods have been given below for your reference.",
                    color=discord.Colour.red() , # Pycord provides a class with default colors you can choose from
                )
                embed.add_field(name = game_state[self.ctx.author.name]['projects'][0]['title'], value = f"https://www.modrinth.com/mod/{game_state[self.ctx.author.name]['projects'][0]['slug']}")
                embed.add_field(name = game_state[self.ctx.author.name]['projects'][1]['title'], value = f"https://www.modrinth.com/mod/{game_state[self.ctx.author.name]['projects'][1]['slug']}")
                embed.set_footer(text="Type \'/game\' to play again!")

                # msg = await interaction.original_response()
                # await msg.edit("", embed = embed)
                await interaction.message.edit(content = "", embed = embed, view = None)
            

            game_state[self.ctx.author.name]['playing'] = False
        else:
            print(f"blocked {interaction.user} from answering the question of {self.ctx.author}")
            await interaction.response.send_message("Hey! That question is not for you, so you cant answer that.", ephemeral=True)


    @discord.ui.button(label="Project 2", style=discord.ButtonStyle.primary)
    async def option_2_button_callback(self, button, interaction):
        global game_state

        if self.ctx.author == interaction.user:
            print(f"{interaction.user} pressed option 2")
            # self.disable_all_items()
            # await interaction.response.edit_message(view=self)
            await interaction.message.edit(content = "Loading...", embed = None, view = None)

            if game_state[self.ctx.author.name]['projects'][1]['downloads'] >= game_state[self.ctx.author.name]['projects'][0]['downloads']:
                print("...which was correct!")
                embed = discord.Embed(
                    title="Correct answer!",
                    description=f"{game_state[self.ctx.author.name]['projects'][1]['title']} has **{shorten_number(game_state[self.ctx.author.name]['projects'][1]['downloads'])}** downloads, while {game_state[self.ctx.author.name]['projects'][0]['title']} has **{shorten_number(game_state[self.ctx.author.name]['projects'][0]['downloads'])}** downloads. Links to the mods have been given below for your reference.",
                    color=discord.Colour.green(), # Pycord provides a class with default colors you can choose from
                )
                embed.add_field(name = game_state[self.ctx.author.name]['projects'][1]['title'], value = f"https://www.modrinth.com/mod/{game_state[self.ctx.author.name]['projects'][1]['slug']}")
                embed.add_field(name = game_state[self.ctx.author.name]['projects'][0]['title'], value = f"https://www.modrinth.com/mod/{game_state[self.ctx.author.name]['projects'][0]['slug']}")
                embed.set_footer(text="Type \'/game\' to play again!")

                await interaction.message.edit(content = "", embed = embed, view = None)
            
            else:
                print("...which was wrong.")
                embed = discord.Embed(
                    title="Wrong answer...",
                    description=f"{game_state[self.ctx.author.name]['projects'][1]['title']} has **{shorten_number(game_state[self.ctx.author.name]['projects'][1]['downloads'])}** downloads, while {game_state[self.ctx.author.name]['projects'][0]['title']} has **{shorten_number(game_state[self.ctx.author.name]['projects'][0]['downloads'])}** downloads. Links to the mods have been given below for your reference.",
                    color=discord.Colour.red(), # Pycord provides a class with default colors you can choose from
                )
                embed.add_field(name = game_state[self.ctx.author.name]['projects'][1]['title'], value = f"https://www.modrinth.com/mod/{game_state[self.ctx.author.name]['projects'][1]['slug']}")
                embed.add_field(name = game_state[self.ctx.author.name]['projects'][0]['title'], value = f"https://www.modrinth.com/mod/{game_state[self.ctx.author.name]['projects'][0]['slug']}")
                embed.set_footer(text="Type \'/game\' to play again!")

                await interaction.message.edit(content = "", embed = embed, view = None)

            game_state[self.ctx.author.name]['playing'] = False
        else:
            print(f"blocked {interaction.user} from answering the question of {self.ctx.author}")
            await interaction.response.send_message("Hey! That question is not for you, so you cant answer that.", ephemeral=True)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command(description = "Starts the game")
async def game(ctx):
    global game_state
    
    await ctx.defer()

    if (not game_state.get(ctx.author.name, False)) or (not game_state[ctx.author.name]['playing']):
        print(f"{ctx.author} started the game!")
        game_state.update({
            ctx.author.name: {
                'projects': [],
                'playing': True
            }
        })

        while True:
            response = await make_request("https://api.modrinth.com/v2/projects_random?count=10")
            game_state[ctx.author.name]['projects'] = response
            print(f"recieved {len(game_state[ctx.author.name]['projects'])} projects")


            if len(game_state[ctx.author.name]['projects']) >= 2:
                await show_mod_selection_screen(ctx, 0)
                break
            print(f"failed to get all 2 projects, only got {len(game_state[ctx.author.name]['projects'])}. Retrying...")
    
    else:
        await ctx.respond("You already have a game going on!", ephemeral=True)  
    
@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
client.run(TOKEN)
