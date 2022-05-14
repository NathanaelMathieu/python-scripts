'''

Notes:

First time setup: Run `. setup.sh && initialVenvSetup` to install everything and enter the venv
After that run `. setup.sh && activate` to enter the venv

Run with:
python fangraphs-espn-pitcher-stat-aggregator.py -a="['xFIP', 'ERA', 'K/9', 'Start-IP', 'Relief-IP', 'GS', 'CG']"

'''
from espn_api.baseball import League
from baseball_scraper import pitching_stats
from datetime import date
import argparse
import ast
import csv

def printLine(player_name, player_type, args, doPrint, fg=None):
    if fg is not None:
        fg_player = fg.query('Name=="{}"'.format(player_name))
        stats = []
        for arg in args:
            try: stats.append(fg_player.iloc[0][arg])
            except: stats.append(0)
        args = stats

    if(doPrint):
        column = "%10s | %20s |" % (player_type, player_name)
        for val in args:
            column = column + " %7s |" % (str(val))
        print(column)

        if fg is None:
            print('-' * len(column))

    with open('out/fangraphs-espn-pitcher-stats-{}.csv'.format(date.today()), 'a', newline='') as csvfile:
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
    parser.add_argument('-p', '--print', type=bool, default=False, help='Print the stats to the terminal. Default=False')
    args = parser.parse_args()
    
    arguments = args.args
    current_season = args.season
    league_id = args.league_id
    team_id = args.team_id
    size = args.number_of_fa
    doPrint = args.print

    print('Fetching ESPN Data...')
    league = League(league_id=league_id, year=current_season)
    my_roster = league.get_team_data(team_id).roster
    free_agent_pitchers = league.free_agents(size=size, position='P')

    print('Fetching Fangraphs Data...')
    fangraphs = pitching_stats(current_season, current_season)

    print('Aggregating stats...')
    printLine("Player Name", "Roster", arguments, doPrint)
    for fantasy_player in my_roster:
        if 'P' in fantasy_player.eligibleSlots:
            printLine(fantasy_player.name, "My Team", arguments, doPrint, fangraphs)

    for fantasy_player in free_agent_pitchers:
        if 'P' in fantasy_player.eligibleSlots:
            printLine(fantasy_player.name, "Free Agent", arguments, doPrint, fangraphs)
    print('Done.')

if __name__ == "__main__":
   main()
 
