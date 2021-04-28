'''

Notes:
The espn_api lib requires python3.7 as of April 2021 due to the versions of numpy it uses.

py -3.7 -m pip install espn-api

baseball_scraper is also broken, so use my fixed version:
git clone git@github.com:NathanaelMathieu/baseball_scraper.git
cd baseball_scraper && py -3.7 setup.py install

Run with:
py -3.7 fangraphs-espn-pitcher-stat-aggregator.py -a="['xFIP', 'ERA', 'K/9', 'Start-IP', 'Relief-IP', 'GS', 'CG']"

'''
from espn_api.baseball import League
from baseball_scraper import pitching_stats
import argparse
import ast
import csv

def printStats(player_name, player_type, args, fg=None):
    if fg is not None:
        fg_player = fg.query('Name=="{}"'.format(player_name))
        stats = []
        for arg in args:
            try: stats.append(fg_player.iloc[0][arg])
            except: stats.append(0)
        args = stats

    column = "%10s | %20s |" % (player_type, player_name)
    for val in args:
        column = column + " %7s |" % (str(val))
    print(column)

    if fg is None:
        print('-' * len(column))

    with open('out/fangraphs-espn-pitcher-stats.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        new_line = [player_type, player_name, *args]
        writer.writerow(new_line)

def main():
    parser = argparse.ArgumentParser(description="Pull Fangraphs data on FA and your team's pitchers from ESPN")
    parser.add_argument('-a', '--args', type=ast.literal_eval, required=True, help='List of stats to pull. Required. Use form -a="[\'IP\']"')
    parser.add_argument('-s', '--season', type=int, default=2021, help='Year of stats to pull. Default=2021')
    parser.add_argument('-l', '--league-id', type=int, default=45839, help='ESPN league id. Must be public. Default=45839')
    parser.add_argument('-t', '--team-id', type=int, default=4, help='ESPN team ID. Default=4')
    parser.add_argument('-n', '--number-of-fa', type=int, default=100, help='Number free agents on ESPN to search. Default=100')
    args = parser.parse_args()
    
    arguments = args.args
    current_season = args.season
    league_id = args.league_id
    team_id = args.team_id
    size = args.number_of_fa

    league = League(league_id=league_id, year=current_season)

    my_roster = league.get_team_data(team_id).roster
    free_agent_pitchers = league.free_agents(size=size, position='P')

    fangraphs = pitching_stats(current_season, current_season)

    printStats("Player Name", "Roster", arguments)

    for fantasy_player in my_roster:
        if 'P' in fantasy_player.eligibleSlots:
            printStats(fantasy_player.name, "My Team", arguments, fangraphs)

    for fantasy_player in free_agent_pitchers:
        if 'P' in fantasy_player.eligibleSlots:
            printStats(fantasy_player.name, "Free Agent", arguments, fangraphs)

if __name__ == "__main__":
   main()
 
