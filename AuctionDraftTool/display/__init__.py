from AuctionDraftTool import starting_budget, fantasy_teams, master_dict
from AuctionDraftTool import starting_slots, bench_slots, tiers_remaining

def starting_display():
    print('League Settings')
    print('\tAuction Budget:', starting_budget)
    print('\tStarting Slots:', starting_slots)
    print('\tBench Slots:', bench_slots)
    print('\tLeague Size:', len(fantasy_teams))
    print('\tAll Teams:')
    for team in fantasy_teams:
        print('\t\t', team)
    print('\tYour Tier Breakdown:')
    for pos in tiers_remaining:
        print('\t\t', pos, tiers_remaining[pos])

def pretty_display(teams_to_display):
    for competition in teams_to_display:
        total_empty_slots = count_all_starter_slots(competition[0])
        print(competition[0])
        print('\t\tMax bid: ',  '$'+str(competition[1]), \
              '\tPrimary slots: ', str(competition[2]), \
              '\tFlex slots:    ', str(competition[3]), \
              '\tTotal Starter Slots: ', total_empty_slots)

def count_all_starter_slots(fantasy_team):
    empty_count = 0
    for slot in starting_slots:
        if not master_dict[fantasy_team]['slots'][slot]['Player']:
            empty_count += 1
    return empty_count
