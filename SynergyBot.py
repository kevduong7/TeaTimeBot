from riotwatcher import LolWatcher, ApiError

REGION = 'na1'
f = open("riotAPI.txt", 'r')
lol_watcher = LolWatcher(f.readline())
f.close()

def get_matches():
    return lol_watcher.match_v5.matchlist_by_puuid('AMERICAS', 'OO6tLnqYJc0MYJv_3az24FfU8lAO3qNv3Z23hrrQu_qrtksglC49eZ376pAfAXnuPchucXqrWgS1Pg')

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
    
if __name__ == "__main__":
    print(get_current_match("MAMMOTHMAN65"))

# get_ranked_stats('Cat in a Box')
# print(get_ranked_stats('Cat in a Box'))
# example call
# matchlist = lol_watcher.match_v5.matchlist_by_puuid('AMERICAS', 'OO6tLnqYJc0MYJv_3az24FfU8lAO3qNv3Z23hrrQu_qrtksglC49eZ376pAfAXnuPchucXqrWgS1Pg')
# print(matchlist)
# print("works")