import numpy as np
import json
from modules.tournament import Tournament
from modules.greedy_scheduler import GreedyScheduler

def main(seed, iterations, rcl_length , greedy_constructor, do_ils, ils_iterations, progress_bar,
        max_value, violated_factor, critical_factor, equality_factor
        ):
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
    tourn = Tournament(teams=teams, locations=locations, stadiums=stadiums, timeslots=timeslots, rounds=22)

    scheduler = GreedyScheduler(tourn)

    schedule, obj = scheduler.grasp_heuristic(seed=seed, iterations = iterations, rcl_length = rcl_length,
                                                greedy_constructor=greedy_constructor, do_ils = do_ils,
                                                ils_iterations = ils_iterations, progress_bar = progress_bar,
                                                max_value = max_value, violated_factor = violated_factor,
                                                critical_factor = critical_factor, equality_factor=equality_factor 
                                            )
    tourn.fixture_matrix = schedule
    np.save('output/greedy1.npy', schedule)
    print("objective: ", obj)
    print("constraints violated: ", tourn.feasibility(schedule, debug=True))

if __name__ == '__main__':
    rcl_length = 10
    seed = 1234
    greedy_constructor = 'by_round'
    do_ils = False
    ils_iterations = 1000
    iterations = 1000
    progress_bar = False
    max_value,violated_factor,critical_factor,equality_factor = 2*(10**4),2*10**4,10**6,10**3
    main(seed,iterations, rcl_length, greedy_constructor, do_ils, ils_iterations, progress_bar,
        max_value,violated_factor,critical_factor,equality_factor
        )