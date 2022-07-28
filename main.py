import asyncio

import aiohttp
from prettytable import PrettyTable

from fpl import FPL

teams = {
    "Arsenal": 1,
    "Aston Villa": 2,
    "Bournemouth": 3,
    "Brentford": 4,
    "Brighton": 5,
    "Chelsea": 6,
    "Crystal Palace": 7,
    "Everton": 8,
    "Fulham": 9,
    "Leicester": 10,
    "Leeds": 11,
    "Liverpool": 12,
    "Man City": 13,
    "Man Utd": 14,
    "New Castle": 15,
    "Nott'm Forest": 16,
    "Southampton": 17,
    "Spurs": 18,
    "West Ham": 19,
    "Wolves": 20,
}
roles = {
    "Goal Keeper": 1,
    "Defender": 2,
    "Midfielder": 3,
    "Forward": 4,
}

def get_role_by_code(code):
    for role in roles:
        if roles[role] == code:
            return role
    return None

def get_team_by_code(code):
    for team in teams:
        if teams[team] == code:
            return team
    return None

def print_table(top_performers, score_func, n):
    player_table = PrettyTable()
    player_table.field_names = ["Player", "£", "Team", "G", "A", "G + A","Status", "Total Points", "Minutes", "Score", "Role"]
    player_table.align["Player"] = "l"
    if n == 1:
        p = top_performers
        player_table.add_row([p.web_name, f"£{p.now_cost / 10}", get_team_by_code(p.team),
                            p.goals_scored, p.assists, p.goals_scored + p.assists, p.status, p.total_points, p.minutes, 0, p.element_type])

    else:
        for p in top_performers[:n]:
            goals = p.goals_scored
            assists = p.assists
            minutes = p.minutes
            team = get_team_by_code(p.team)
            score = score_func(p)
            player_table.add_row([p.web_name, f"£{p.now_cost / 10}", team,
                                goals, assists, goals + assists, p.status, p.total_points, minutes, score, p.element_type])

    return player_table
        
async def top_sub_10(players):
    players = [p for p in players if p.now_cost/10 < 10]
    calculation = lambda p: (((p.minutes)/90)*float((p.points_per_game)))/(p.now_cost/10)

    top_performers = sorted(
        players, key=calculation, reverse=True)

    table = print_table(top_performers, calculation, 10)
    print(("Top Players Below 10").center(100, "-"))
    print(table)

async def top_sub_5(players):
    players = [p for p in players if p.now_cost/10 < 5]
    calculation = lambda p: (((p.minutes)/90)*float((p.points_per_game)))/(p.now_cost/10)

    top_performers = sorted(
        players, key=calculation, reverse=True)

    table = print_table(top_performers, calculation, 10)
    print(("Top Players Below 5").center(100, "-"))
    print(table)

async def top_pointers(players):

    calculation = lambda p: (p.total_points/p.minutes)*float(p.points_per_game) if p.minutes > 2500 else 0
    top_performers = sorted(
        players, key=calculation, reverse=True)

    table = print_table(top_performers, calculation, 10)
    print(("Top Pointers").center(100, "-"))
    print(table)

async def top_above_10(players):
    players = [p for p in players if p.now_cost/10 > 10]

    calculation = lambda p: (((p.minutes)/90)*float((p.points_per_game)))/(p.now_cost/10)

    top_performers = sorted(
        players, key=calculation, reverse=True)

    table = print_table(top_performers, calculation, 10)

    print(("Top Players Above 10").center(100, "-"))
    print(table)

async def get_injured_players(players):
    injured_players = [p for p in players if p.status != "a"]
    table = print_table(injured_players, lambda p: p.total_points, 50)
    print(("Injured Players").center(100, "-"))
    print(table)

async def get_player_by_name(players, name):
    for p in players:
        if p.web_name == name:
            table = print_table(p, lambda p: p.total_points, 1)
            print(("Player").center(100, "-"))
            print(table)
            return
    print(f"Player {name} not found")


async def get_players():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()

    return players

if __name__ == "__main__":
    players = asyncio.run(get_players())

    asyncio.run(top_sub_10(players))
    asyncio.run(top_above_10(players))
    asyncio.run(top_pointers(players))
    asyncio.run(top_sub_5(players))
    asyncio.run(get_injured_players(players))
    