import asyncio
from multiprocessing.connection import wait

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
    "GK": 1,
    "D": 2,
    "M": 3,
    "F": 4,
    "All": 5,
}
calculations = {
    "Points Per Game" : lambda p: ((p.minutes/90)/float(p.points_per_game)/(p.now_cost/10)) if float(p.points_per_game) > 0 else 0,
    "Top Points" : lambda p: p.total_points / (p.now_cost/10),

}
def get_role_by_code(code):
    for role in roles:
        if roles[role] == code and type(code) == int:
            return role
        elif role == code and type(code) == str:
            return roles[role]
    return None

def get_team_by_code(code):
    for team in teams:
        if teams[team] == code:
            return team
        elif team == code:
            return teams[team]
    return None

def print_table(top_performers, score_func, n, fixtures):
    player_table = PrettyTable()
    player_table.field_names = ["Player", "£", "Team", "Against", "G", "A", "G + A","Status", "Total Points", "Minutes", "Influence", "Score", "Role"]
    player_table.align["Player"] = "l"
    if n == 1:
        p = top_performers
        get_next_fixture(fixtures, p.team_code)
        player_table.add_row([players.web_name, f"£{players.now_cost / 10}", get_team_by_code(players.team),
                            players.goals_scored, players.assists, players.goals_scored + players.assists, players.status,
                            players.total_points, players.minutes,players.influence , 0, get_role_by_code(players.element_type)])

    else:
        for p in top_performers[:n]:
            goals = p.goals_scored
            assists = p.assists
            minutes = p.minutes
            team = get_team_by_code(p.team)
            against = get_next_fixture(fixtures, p.team)
            score = score_func(p)
            player_table.add_row([p.web_name, f"£{p.now_cost / 10}", team, against,
                                goals, assists, goals + assists, p.status, p.total_points, minutes, p.influence, round(score, 2), get_role_by_code(p.element_type)])

    return player_table

async def get_injured_players(players):
    injured_players = [p for p in players if players.status != "a"]
    table = print_table(injured_players, lambda p: players.total_points, 50)
    print(("Injured Players").center(100, "-"))
    print(table)

async def get_player_by_name(players, name):
    for p in players:
        if players.web_name == name:
            table = print_table(p, lambda p: players.total_points, 1)
            print(("Player").center(100, "-"))
            print(table)
            return
    print(f"Player {name} not found")

def get_next_fixture(fixtures, team):
    for team_fixture in fixtures:
        if team_fixture.event == 1:
            if team_fixture.team_h == team:
                return get_team_by_code(team_fixture.team_a)
            elif team_fixture.team_a == team:
                return get_team_by_code(team_fixture.team_h)
async def get_influence_per_team(players, team):
    calc = lambda p: float(p.influence)/(p.now_cost/10)

    players = [p for p in players if p.team == get_team_by_code(team)]
    top_performers = sorted(players, key=calc, reverse=True)
    table = print_table(top_performers, calc, 15, fixtures)
    print((f"Top Influencers - {team}").center(100, "-"))
    print(table)

async def get_players():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()

    return players

async def get_fixtures():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        fixtures = await fpl.get_fixtures()

    return fixtures

async def get_stats(players, fixtures, calculation, n, line, role, low_price, high_price):
    if role == "All":
        for i in range(4):
            await get_stats(players, fixtures, calculation, n, line, get_role_by_code(i+1), low_price, high_price)
        return
    calculation = calculations[calculation]
    players = [p for p in players if p.now_cost/10 > low_price and p.now_cost/10 < high_price]
    players = [p for p in players if p.element_type == get_role_by_code(role)]
    top_performers = sorted(
        players, key=calculation, reverse=True)

    table = print_table(top_performers, calculation, n, fixtures)
    print((f"Top Players {line} - {role} - {low_price}<{high_price}").center(100, "-"))
    print(table)

if __name__ == "__main__":
    players = asyncio.run(get_players())
    fixtures = asyncio.run(get_fixtures())

    # # top players above 10 pounds
    #asyncio.run(get_stats(players, "top_points", 10, "Above 10", "All", 10, 15))
    # top players below 5 pounds
    #asyncio.run(get_stats(players, "top_points", 10, "Below 5","All", 0, 5))
    # # top players below 10 pounds
    # asyncio.run(get_stats(players, "top_points", "Top Below 10", "All", 5, 10))
    # # top players below 15 pounds
    # asyncio.run(get_stats(players, "top_points", "Top Below 15", "All", 0, 15))
    # # top forwards
    #asyncio.run(get_stats(players, "Top Points", 10, "Forwards", "F", 3, 15))
    # # top midfielders
    #asyncio.run(get_stats(players, "Top Points", 10, "Midfielders", "M", 3, 7))
    # # top defenders
    #asyncio.run(get_stats(players, fixtures, "Top Points", 10, "Defenders", "D", 3, 15))
    # # top goalkeepers
    #asyncio.run(get_stats(players, "Top Points", 10, "Goalkeepers", "GK", 3, 15))
    # influencers
    asyncio.run(get_influence_per_team(players, "Man City"))
    #asyncio.run(get_injured_players(players))
    