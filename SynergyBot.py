from operator import truediv
from riotwatcher import LolWatcher, ApiError
import json
import os
REGION = 'na1'
f = open("riotAPI.txt", 'r')
lol_watcher = LolWatcher(f.readline())
f.close()

def get_matches(puuid):
    return lol_watcher.match_v5.matchlist_by_puuid('AMERICAS', puuid, 0, 10)

def get_ranked_stats(ign):
    # user_name = lol_watcher.summoner.by_name(REGION, ign)
    
    try:
        my_ranked_stats = ['this_is_probably_not_anyones_summoner_name_since_it_is_too_long']
        user_name = lol_watcher.summoner.by_name(REGION, ign)
        my_ranked_stats = lol_watcher.league.by_summoner(REGION, user_name['id'])
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that name does not exist')
        else:
            raise
    
    
    return my_ranked_stats

def get_current_match(ign):
    cur_game = {}
    try:
        user_name = lol_watcher.summoner.by_name(REGION, ign)
        #matches = lol_watcher.match_v5.matchlist_by_puuid('AMERICAS', user_name['puuid'])
        userStats = lol_watcher.league.by_summoner(REGION, user_name['id'])
        
        cur_game = lol_watcher.spectator.by_summoner(REGION, userStats[0]['summonerId'])
        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that name does not exist')
        else:
            raise
    except IndexError:
        print("This user does not have any ranked games played this season")
    return cur_game


def is_ARAM(matchInfo):
    if lol_watcher.match_v5.by_id('americas', 'matchID')['gameMode'] == 'ARAM':
        return True
    return False

def update_all():
    with open('users.json', 'r') as f:
        data = json.load(f)
    for puuid, val in data.items():
        aram_mmr_update(val['ign'])
        #print(val)
            
    # os.remove('users.json')
    # with open('users.json', 'w') as f:
    #     json.dump(data, f, indent=4)

def aram_mmr_update(ign):
    try:
        user_name = lol_watcher.summoner.by_name(REGION, ign)
        puuid = user_name['puuid']
    
        matchlist = lol_watcher.match_v5.matchlist_by_puuid('AMERICAS', user_name['puuid'],0,10)
        f = open('users.json')
        data = json.load(f)
        f.close()
        userData = data[user_name['puuid']]

        update = ""
        count = 0
        for matchID in matchlist:
            #exit loop if no new aram games have been played
            if matchID == userData['lastgame']:
                break
            count += 1
            matchInfo = lol_watcher.match_v5.by_id('americas', matchID)
            if matchInfo['info']['gameMode'] == 'ARAM':
                #updates the latest game
                if update == "":
                    
                    update = matchID
                    
                #check if user won that game
                for player in matchInfo['info']['participants']:
                    if player['puuid'] == puuid:
                        if player['win'] == True:
                            data[puuid]['elo'] += 50
                        else:
                            data[puuid]['elo'] -= 50
                        break
        
        if update != "" and count != 0:
            data[puuid]['lastgame'] = update
            data[puuid]['ign'] = user_name['name']
                        
            os.remove('users.json')
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=4)
            print("mmr has been updated")
        else:
            print("no changes in mmr")
        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that name does not exist')
        else:
            raise
    
    

#add feature to include last 10 aram games
#returns string of status
def add_user(ign):
    try:
        user_name = lol_watcher.summoner.by_name(REGION, ign)

        #matches = lol_watcher.match_v5.matchlist_by_puuid('AMERICAS', user_name['puuid'])
        with open('users.json', 'r') as f:
            data = json.load(f)
            

            if user_name['puuid'] in data:
                print("that user has already been added to teatimebot")
                return "That user has already been added to TeaTimeBot!"
            data[user_name['puuid']] = {"ign":user_name['name'],"elo":1000,"lastgame":None}

        os.remove('users.json')
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)

        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that name does not exist')
        else:
            raise
    


    
if __name__ == "__main__":
    #print(aram_mmr_update("Cat in a Box"))
    # t = open('matchinfo.txt', 'w')
    # t.write(str(lol_watcher.match_v5.by_id('americas', 'NA1_4209650530')))
    # t.close()
    #print(lol_watcher.match_v5.by_id('americas', 'NA1_4209650530'))
    #print(get_matches('j_Kv9DIGGnhWxmu58G37nYqQF_gHG5C4tvzZmSoFQtBSsOITG6pHfQ54MsQk00a1twQ5W0rLuiBnQw'))
    
  
    #print(lol_watcher.summoner.by_name(REGION, "McMango"))

    #add_user('Kim Hyunjinny')
    
    update_all()

# get_ranked_stats('Cat in a Box')
# print(get_ranked_stats('Cat in a Box'))
# example call
# matchlist = lol_watcher.match_v5.matchlist_by_puuid('AMERICAS', 'OO6tLnqYJc0MYJv_3az24FfU8lAO3qNv3Z23hrrQu_qrtksglC49eZ376pAfAXnuPchucXqrWgS1Pg')
# print(matchlist)
# print("works")