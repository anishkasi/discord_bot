import discord
import re
import numpy as np
from itertools import combinations

pattern = "\$cleps [0-9]"
TOKEN = "NzczODUxNjE2MzAyMzMzOTc2.X6PPeg.TSBPOf4_3LJN4FtouHh5WJ_N2sk"

n = ['anishkasi', 'Wolfinthehouse', 'pindabc', 'aprbhd', 'the_week', 'JakeSuli', 'gopuman', 'akshara', 'greybeard278', 'Dobby']
nicknames = {
        'anishkasi': set(['kasi','anishkasi']),
        'Wolfinthehouse': set(['neil','pratith','juice','Wolfinthehouse']),
        'pindabc': set(['pinds','yogesh','dips','pindabc']),
        'aprbhd' : set(['apar','jose','aprbhd']),
        'the_week' : set(['aveek','tupperware','shelly','the_week']),
        'JakeSuli' : set(['arvi','ssr','ronnie','jakesuli']),
        'gopuman': set(['gops','chilly','gopuman']),
        'akshara': set(['akshara','hak']),
        'greybeard278': set(['paro','greybeard278']), # gops add some funny nickname for me and paro  and others also if you can
        'Dobby': set(['dobby','kuneil']),
        }

weights = {
        'anishkasi': 2.3 + 0.81*3,
        'Wolfinthehouse': 3.5 + 0.86*3,
        'pindabc': 2.1 + 0.8*3,
        'aprbhd' : 2.3 + 0.78*3,
        'the_week' : 1 + 0.8*3,
        'JakeSuli' : 2 + 0.83*3,
        'gopuman': 2.25 + 0.85*3,
        'akshara': 1.3 + 0.78*3,
        'greybeard278': 1.5 + 0.77*3,
        'Dobby': 1.2 + 0.76*3,
        }

def return_names(split):
    names = []
    ss = set(split)
    for key,val in nicknames.items():
        if(len(val.intersection(ss)) >= 1):
            names.append(key)
    return names

def create_weighted_team(names,num_teams):
    tol = 2
    numppl = len(names)//num_teams
    if(num_teams == 2):
        combs = list(combinations(names,numppl))
        other_team = [[i for i in names if i not in s] for s in combs]
        team_scores = np.array([sum([weights[i] for i in s]) for s in combs])
        other_team_scores = np.array([sum([weights[i] for i in s]) for s in other_team])
        diff_in_scores = np.abs(team_scores - other_team_scores)
        inds = np.where(diff_in_scores < tol)[0]
        ttp = np.array(combs)
        ttp = ttp[inds]
        np.random.shuffle(ttp)
        final_team = list(ttp[0])
        final_other_team = [i for i in names if i not in final_team]
        return final_team,final_other_team

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

def filterOnlyOnlineMembers(member):
    return member.status != discord.Status.offline and not member.bot

def online_members(message):
    guild = message.guild 
    vc = guild.voice_channels
    mems = []
    for i in vc:
        members = i.members
        mems.extend(members)
    return [i.name for i in mems]
    
@client.event
async def on_message(message):
    z = re.findall(pattern,message.content)
    if(len(z) > 0):
        split_msg = message.content.split(" ")
        exclude = return_names(split_msg)
        names = online_members(message)
        names = [i for i in names if i not in exclude]
        print(names)
        if("-w" in split_msg):
            t1,t2 = create_weighted_team(names,2)
            msg = " ".join(t1)
            await message.channel.send(msg)
            msg = " ".join(t2)
            await message.channel.send(msg)
        #onlineMembersCount = len(onlineMembersInServer)
        else:
            numteams = int(z[0][-1])
            np.random.shuffle(names)
            if(numteams == 3):
                for i in range(3):
                    msg = names[i*3 : (i+1)*3]
                    msg = " ".join(msg)
                    await message.channel.send(msg)
            
            elif(numteams == 2):
                msg = names[:3]
                msg = " ".join(msg)
                await message.channel.send(msg)
                msg = names[3:]
                msg = " ".join(msg)
                await message.channel.send(msg)
                
            else:
                msg = " ".join(names)
                await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)