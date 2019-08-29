import os
import pickle
from yaml import load

# For slurping files (supports config_loader only)
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

def return_starters_list(starters_dict):
    starters_list = []
    for pos in starters_dict:
        if starters_dict[pos] == 1:
            starters_list.append(pos)
        if starters_dict[pos] > 1:
            for i in range(starters_dict[pos]):
                starters_list.append(pos + str(i+1))
    return starters_list

def return_bench_list(bench_dict):
    bench_list = []
    if bench_dict['BE'] == 1:
        bench_list.append('BE')
    if bench_dict['BE'] > 1:
        for i in range(bench_dict['BE']):
            bench_list.append('BE' + str(i+1))
    return bench_list

# --------------------- END OF FUNCTIONS -------------------------

# Load the fantasy config and vars
project_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_dir, "config/fantasy_config.yaml")
fantasy_config = config_loader(config_path)

starting_budget = fantasy_config['starting_budget']
fantasy_teams = fantasy_config['fantasy_teams']
starting_slots = return_starters_list(fantasy_config['num_slots']['starters'])
bench_slots = return_bench_list(fantasy_config['num_slots']['bench'])
all_slots = starting_slots + bench_slots
tier_min_dict = fantasy_config['tier_minimums']

# Import full players dict
players_pre_tier = {}
with open('AuctionDraftTool/config/edit_my_pre_draft_dollars.txt', 'r') as f:
    for line in f.readlines():
        players_pre_tier[ eval(line)['name'] ] = eval(line)

# Initialize tiers
for player in players_pre_tier:
    for pos in tier_min_dict:
        if players_pre_tier[player]['position'] == pos:
            if players_pre_tier[player]['espn_pre_draft$'] >= tier_min_dict[pos]['tier_4']:
                players_pre_tier[player]['tier'] = 'tier_4'
            if players_pre_tier[player]['espn_pre_draft$'] >= tier_min_dict[pos]['tier_3']:
                players_pre_tier[player]['tier'] = 'tier_3'
            if players_pre_tier[player]['espn_pre_draft$'] >= tier_min_dict[pos]['tier_2']:
                players_pre_tier[player]['tier'] = 'tier_2'
            if players_pre_tier[player]['espn_pre_draft$'] >= tier_min_dict[pos]['tier_1']:
                players_pre_tier[player]['tier'] = 'tier_1'

players = players_pre_tier.copy()

#initialize tiers
tiers_remaining = {'QB':  {'tier_1': 0, 'tier_2': 0, 'tier_3': 0, 'tier_4': 0},
                   'RB':  {'tier_1': 0, 'tier_2': 0, 'tier_3': 0, 'tier_4': 0},
                   'WR':  {'tier_1': 0, 'tier_2': 0, 'tier_3': 0, 'tier_4': 0},
                   'TE':  {'tier_1': 0, 'tier_2': 0, 'tier_3': 0, 'tier_4': 0},
                   'K':   {'tier_1': 0, 'tier_2': 0, 'tier_3': 0, 'tier_4': 0},
                   'DST': {'tier_1': 0, 'tier_2': 0, 'tier_3': 0, 'tier_4': 0}
                   }
# WILL NEED ALL TIERS PROVIDED
for player in players:
    tiers_remaining[ players[player]['position'] ][ players[player]['tier'] ] += 1

# Add UNKOWN players for dexterity
for unknown in ['UNKNOWN QB', 'UNKNOWN RB', 'UNKNOWN WR', 'UNKNOWN TE', 'UNKNOWN DST', 'UNKNOWN K']:
    players[unknown] = {'name': 'UNKNOWN',
                        'position': unknown.split()[1],
                        'tier': 'tier_4',
                        'fpros_pre_draft$': 0,
                        'espn_pre_draft$': 0,
                        'my_pre_draft$': 0
                        }

master_dict = {}
#intialize dicts
for fantasy_team in fantasy_teams:
    master_dict[fantasy_team] = {}
    master_dict[fantasy_team]['budget'] = starting_budget
    master_dict[fantasy_team]['empty_slots'] = len(all_slots)
    master_dict[fantasy_team]['slots'] = {}
    for slot in all_slots:
        master_dict[fantasy_team]['slots'][slot] = {'Player': None,
                                                    'Position': None,
                                                    'Price_Paid': 0}
    master_dict[fantasy_team]['max_bid'] = master_dict[fantasy_team]['budget'] - (master_dict[fantasy_team]['empty_slots'] - 1)

rb_heir  = [pos for pos in starting_slots if pos.startswith('RB')]  + bench_slots
wr_heir  = [pos for pos in starting_slots if pos.startswith('WR')]  + bench_slots
qb_heir  = [pos for pos in starting_slots if pos.startswith('QB')]  + bench_slots
te_heir  = [pos for pos in starting_slots if pos.startswith('TE')]  + bench_slots
k_heir   = [pos for pos in starting_slots if pos.startswith('K')]   + bench_slots
dst_heir = [pos for pos in starting_slots if pos.startswith('DST')] + bench_slots

heir_dict = {'QB': qb_heir, 'RB': rb_heir, 'WR': wr_heir,
             'TE': te_heir, 'K': k_heir, 'DST': dst_heir}
