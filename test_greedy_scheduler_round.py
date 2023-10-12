import numpy as np
import json
from modules.tournament import Tournament
from modules.greedy_round_scheduler import GreedyByRoundScheduler

np.random.seed(1234)

with open('teams.json', 'r') as f:
    teams = json.load(f)

with open('locations.json', 'r') as f:
    locations = json.load(f)

stadiums = {}
for loc in locations:
    snames = []
    for s in locations[loc]['stadiums']:
        snames.append(s)
        stadiums[s] = {
            'location': loc,
            'size': locations[loc]['stadiums'][s]['size'] 
        }
    
    locations[loc]['stadiums'] = snames

timeslot_values = [10, 13, 6, 7, 11, 5, 4]  # Change later according to attendances
timeslot_names = ['Thursday Night', 'Friday Night', 'Saturday Afternoon', 'Saturday Evening',
                  'Saturday Night', 'Sunday Afternoon', 'Sunday Evening']

timeslots = [{'value': v, 'name': n} for (n, v) in zip(timeslot_names, timeslot_values)]
tourn = Tournament(teams = teams, locations = locations, stadiums=stadiums, timeslots = timeslots, rounds = 22)

gr = GreedyByRoundScheduler(tourn)
arr = tourn.weight_matrix
fixture = gr.construct_greedy_schedule_random(arr, rounds = 22, timeslots = 7, n_games=9, rcl_length=10, print_games=True)
print("objective: ", tourn.fixture_attractiveness(fixture=fixture))
print("constraints violated: ", tourn.feasibility(fixture, debug=True))