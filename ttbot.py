import discord
import SynergyBot


t = open("discordAPI.txt","r")
chid = open("channelId.txt", "r")

TOKEN = t.readline()
CHANNEL_ID = chid.readline()

intents = discord.Intents.default()
intents.members = True


client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!ttb'):
        
        copy = message.content
        if len(message.content.split()) > 1:
            if copy.split()[1] == 'leaderboards':
                await message.channel.send(SynergyBot.get_matches())
            elif (copy.split()[1] == 'help'):
                await message.channel.send("wip")
            elif (copy.split()[1] == 'ranks'):
                summName = ''
                for i in copy.split()[2:]:
                    summName += i + ' '
                summName = summName.strip(' ')
                try:
                    info = SynergyBot.get_ranked_stats(summName)[0]
                    
                    if(type(info) == str):
                        await message.channel.send("User with that name does not exist")
                    else:
                        winRate = (info['wins']/(info['wins'] + info['losses'])) * 100

                        await message.channel.send("```css\nUSER: {0}\nRANK: {1} {2}\nWIN RATE: {3:.2f}%```".format(info['summonerName'], info['tier'], info['rank'], winRate))
                except IndexError:
                    await message.channel.send("```css\nUSER: {0}\nRANK: UNRANKED\nWIN RATE: 0%```".format(info['summonerName']))

            elif (copy.split()[1] == 'cg' or copy.split()[1] == 'current_game'):
                summName = ''
                for i in copy.split()[2:]:
                    summName += i + ' '
                curGame = SynergyBot.get_current_match(summName)
                fin = ""
                counter = 0
                for player in curGame['participants']:
                    info = SynergyBot.get_ranked_stats(player['summonerName'])[0]
                    
                    
                    winRate = (info['wins']/(info['wins'] + info['losses'])) * 100
                    fin += "```css\nUSER: {0}\nRANK: {1} {2}\nWIN RATE: {3:.2f}%```".format(info['summonerName'], info['tier'], info['rank'], winRate)
                    counter += 1
                await message.channel.send(fin)

            else:
                await message.channel.send('Invalid Command. \nType \"!ttb help\" to get a list of commands.')
        else:
            await message.channel.send('Hello, I am TeaTimeBot!\nType \"!ttb help\" to get a list of commands.')

@client.event
async def on_member_join(member):
 
    print("A new member has joined the server")

    channel = client.get_channel(CHANNEL_ID)
    

@client.event
async def on_member_remove(member):

    print('A member has left the server')

client.run(TOKEN)