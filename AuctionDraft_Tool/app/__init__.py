import os
from yaml import load
import pickle

# For slurping files
def slurp(fi):
    with open(fi, mode="r") as fh:
        return fh.read()

# For loading yaml configs
def config_loader(config_path):
    ''' Error catching for loading .yaml config files'''
    try:
        assert os.path.exists(config_path)
    except AssertionError:
        print('!!Config file of path: ', config_path, ' not found.')
        raise AssertionError()
    try:
        loaded = load(slurp(config_path))
    except Exception as ex:
        print('Exception: ', ex)
        print('!!Something broke during loading of yaml config file at path: ', config_path)
        raise Exception()
    try:
        assert isinstance(loaded, (dict, list))
    except AssertionError:
        print('!!Consumer config file not properly formatted as yaml, dictionary or list type not loaded')
        raise AssertionError()
    return loaded

players = pickle.load(open('AuctionDraft_Tool/app/all_players.sav', 'rb'))
for unknown in ['UNKNOWN QB', 'UNKNOWN RB', 'UNKNOWN WR', 'UNKNOWN TE', 'UNKNOWN DST', 'UNKNOWN K']:
    players[unknown] = {'name': 'UNKNOWN',
                        'position': unknown.split()[1],
                        'tier': None,
                        'fpros_pre_draft$': 0,
                        'espn_pre_draft$': 0,
                        'my_pre_draft$': 0}

project_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_dir, "config/fantasy_teams.yaml")
fantasy_teams = config_loader(config_path)

#initialize tiers
tiers_remaining = {'RB': {'tier_1': 0, 'tier_2': 0, 'tier_3': 0},
                   'WR': {'tier_1': 0, 'tier_2': 0, 'tier_3': 0, 'tier_4': 0},
                   'TE': {'tier_1': 0, 'tier_2': 0, 'tier_3': 0}}

for player in players:
    if players[player]['position'] in ['RB', 'WR', 'TE'] and players[player]['tier']:
        tiers_remaining[ players[player]['position'] ][ players[player]['tier'] ] += 1

# Currently, hardcoded for this format
slots = ['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'TE', 'FLX', 'DST', 'K',
         'BE1', 'BE2', 'BE3', 'BE4', 'BE5', 'BE6']

master_dict = {}
#intialize dicts
for fantasy_team in fantasy_teams:
    master_dict[fantasy_team] = {}
    master_dict[fantasy_team]['budget'] = 200
    master_dict[fantasy_team]['empty_slots'] = len(slots)
    master_dict[fantasy_team]['slots'] = {}
    for slot in slots:
        master_dict[fantasy_team]['slots'][slot] = {'Player': None,
                                                    'Position': None,
                                                    'Price_Paid': 0}
    master_dict[fantasy_team]['max_bid'] = master_dict[fantasy_team]['budget'] - (master_dict[fantasy_team]['empty_slots'] - 1)

bench_heir = ['BE1', 'BE2', 'BE3', 'BE4', 'BE5', 'BE6']
rb_heir    = ['RB1', 'RB2'] + bench_heir
wr_heir    = ['WR1', 'WR2'] + bench_heir
qb_heir    = ['QB']         + bench_heir
te_heir    = ['TE']         + bench_heir
k_heir     = ['K']          + bench_heir
dst_heir   = ['DST']       + bench_heir

heir_dict = {'RB': rb_heir, 'WR': wr_heir, 'QB': qb_heir, 'TE': te_heir, 'K': k_heir, 'DST': dst_heir}

major_starting_slots = ['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'TE', 'FLX']


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
    for slot in major_starting_slots:
        if not master_dict[fantasy_team]['slots'][slot]['Player']:
            empty_count += 1
    return empty_count
