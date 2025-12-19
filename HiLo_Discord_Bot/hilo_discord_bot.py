import discord, aiohttp, math

from discord.ui.item import Item

TOKEN = "INSERT_BOT_TOKEN_HERE"

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
    
activity = discord.Activity(name='/game', type=discord.ActivityType.listening)
client = discord.Bot(activity=activity)

game_state = {}

async def show_next_screen_for_correct_answer(ctx):
    print("...which was correct!")
                
    game_state[ctx.author.name]['index_number'] += 1
    if game_state[ctx.author.name]['index_number'] + 1 < len(game_state[ctx.author.name]['projects']):
        pass

    else:
        while True:
            response = await make_request("https://api.modrinth.com/v2/projects_random?count=10")
            game_state[ctx.author.name]['projects'].extend(response)
            print(f"recieved {len(game_state[ctx.author.name]['projects'])} projects")
            if game_state[ctx.author.name]['index_number'] + 1 < len(game_state[ctx.author.name]['projects'][game_state[ctx.author.name]['index_number']]):
                break
    
    await show_mod_selection_screen(ctx, game_state[ctx.author.name]['index_number'], ctx)
    # print(game_state[ctx.author.name]['index_number'], game_state[ctx.author.name]['projects'])

async def show_next_screen_for_wrong_answer(ctx):
    print("...which was wrong, or the person ended the game.")

    embed = discord.Embed(
        title="Game Over...",
        description=f"**\'{game_state[ctx.author.name]['projects'][game_state[ctx.author.name]['index_number'] + 1]['title']}\'** has **{shorten_number(game_state[ctx.author.name]['projects'][game_state[ctx.author.name]['index_number'] + 1]['downloads'])}** downloads. Links to the mods have been given below.",
        color=discord.Colour.red(), # Pycord provides a class with default colors you can choose from
    )

    for m in (game_state[ctx.author.name]['projects'][0 : game_state[ctx.author.name]['index_number'] + 2]):
        embed.add_field(name = m['title'], value = f"https://www.modrinth.com/mod/{m['slug']}")

    embed.set_footer(text="Type \'/game\' or press the \'Play Again\' button to play again!")

    await ctx.respond("", view=view_for_game_over_screen(ctx=ctx), embed = embed)

async def show_mod_selection_screen(ctx, index_number, reply_ctx):

    main_embed = discord.Embed(
        title = "Higher or Lower?",
        description = f"**\'{game_state[ctx.author.name]['projects'][index_number]['title']}\'** has **{shorten_number(game_state[ctx.author.name]['projects'][index_number]['downloads'])}** downloads. Select whether you think **\'{game_state[ctx.author.name]['projects'][index_number + 1]['title']}\'** has a **higher** or **lower** amount of downloads. If both have an equal amount of downloads, you automatically get this question right.",
        color = discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    main_embed.set_author(name = f"Level {index_number + 1}")

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

    await reply_ctx.respond("", view=response_to_the_option_selection_menu(ctx), embeds = [main_embed, embed1, embed2])

async def start_game(ctx):
    global game_state

    if (not game_state.get(ctx.author.name, False)) or (not game_state[ctx.author.name]['playing']):

        print(f"{ctx.author} started the game!")
        game_state.update({
            ctx.author.name: {
                'projects': [],
                'playing': True,
                'index_number': 0
            }
        })

        while True:
            response = await make_request("https://api.modrinth.com/v2/projects_random?count=10")
            game_state[ctx.author.name]['projects'] = response
            print(f"recieved {len(game_state[ctx.author.name]['projects'])} projects")


            if len(game_state[ctx.author.name]['projects']) >= 2:

                await show_mod_selection_screen(ctx, 0, ctx)
                break

            print(f"failed to get all 2 projects, only got {len(game_state[ctx.author.name]['projects'])}. Retrying...")
    
    else:

        await ctx.respond("You already have a game going on! Do you want to end it?", view=view_for_end_game_confirmation(ctx), ephemeral=True)

class view_for_game_over_screen(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    @discord.ui.button(label="Play Again", style=discord.ButtonStyle.success)
    async def play_again_button_callback(self, button, interaction):
        global game_state

        if self.ctx.author == interaction.user:
            print(f"{interaction.user} started a new game")
            button.disabled = True
            
            await interaction.response.defer()

            await start_game(self.ctx)  

            try:
                await interaction.respond()
            except:
                print("empty message failed to send, as intended")

        else:
            print(f"blocked {interaction.user} from playing again of {self.ctx.author}")
            await interaction.response.send_message("Hey! That is meant for the person whose game got over. You can start a new game using /game.", ephemeral=True)

class view_for_end_game_confirmation(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx
    
    @discord.ui.button(label="Yes, End Game", style=discord.ButtonStyle.danger)
    async def confirmed_button_callback(self, button, interaction):
        global game_state

        print(f"{interaction.user} confirmed ending game")
        button.disabled = True

        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Hey! You cant end another person\'s game.", ephemeral=True)

        await interaction.response.defer()

        if (not game_state.get(self.ctx.author.name, False)) or (not game_state[self.ctx.author.name]['playing']):
            print("try end game when no game")
            try:
                await interaction.respond()
            except:
                print("empty message failed to send, as intended")
        else:
            print("try end game when game")
            await show_next_screen_for_wrong_answer(self.ctx)

            game_state[self.ctx.author.name]['playing'] = False

        

class response_to_the_option_selection_menu(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

    @discord.ui.button(label="Higher", style=discord.ButtonStyle.primary, emoji="⬆️")
    async def option_1_button_callback(self, button, interaction):
        global game_state

        if self.ctx.author == interaction.user:
            print(f"{interaction.user} pressed option 1")
            self.disable_all_items()
            await interaction.response.edit_message(view=self)
            # await interaction.message.edit(content = "Loading...", embed = None, view = None)
            
            if game_state[self.ctx.author.name]['projects'][game_state[self.ctx.author.name]['index_number']]['downloads'] <= game_state[self.ctx.author.name]['projects'][game_state[self.ctx.author.name]['index_number'] + 1]['downloads']:
                await show_next_screen_for_correct_answer(self.ctx)

            else:
                await show_next_screen_for_wrong_answer(self.ctx)

            game_state[self.ctx.author.name]['playing'] = False

        else:
            print(f"blocked {interaction.user} from answering the question of {self.ctx.author}")
            await interaction.response.send_message("Hey! That question is not for you, so you cant answer that.", ephemeral=True)    

    @discord.ui.button(label="Lower", style=discord.ButtonStyle.primary, emoji="⬇️")
    async def option_2_button_callback(self, button, interaction):
        global game_state
        
        if self.ctx.author == interaction.user:
            print(f"{interaction.user} pressed option 2")
            self.disable_all_items()
            await interaction.response.edit_message(view = self)

            if game_state[self.ctx.author.name]['projects'][game_state[self.ctx.author.name]['index_number']]['downloads'] >= game_state[self.ctx.author.name]['projects'][game_state[self.ctx.author.name]['index_number'] + 1]['downloads']:
                await show_next_screen_for_correct_answer(self.ctx)

            else:
                await show_next_screen_for_wrong_answer(self.ctx)

            game_state[self.ctx.author.name]['playing'] = False
        else:
            print(f"blocked {interaction.user} from answering the question of {self.ctx.author}")
            await interaction.response.send_message("Hey! That question is not for you, so you cant answer that.", ephemeral=True)

    @discord.ui.button(label="End Game", style=discord.ButtonStyle.danger)
    async def end_game_button_callback(self, button, interaction):
        if self.ctx.author == interaction.user:
            print(f"{interaction.user} requested to end game, awaiting confirmation")
            await interaction.response.send_message("Are you sure you want to end the current game? Your progress will not be saved.", view=view_for_end_game_confirmation(self.ctx), ephemeral=True)   

        else:
            print(f"blocked {interaction.user} from ending the game of {self.ctx.author}")
            await interaction.response.send_message("Hey! You can\'t end another person\'s game.", ephemeral=True)   

        

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command(description = "Starts the game")
async def game(ctx):    
    await ctx.defer()

    await start_game(ctx=ctx)
    
@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
client.run(TOKEN)
