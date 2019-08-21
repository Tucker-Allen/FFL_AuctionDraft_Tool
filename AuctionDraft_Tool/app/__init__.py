players = {'DeSean Jackson, WAS':   {'name': 'DeSean Jackson, WAS',     'position': 'WR', 'pre_draft$': 13},
           'Tom Brady, NEP':        {'name': 'Tom Brady, NEP',          'position': 'QB', 'pre_draft$': 15},
           'Jimmy Graham, GNB':     {'name': 'Jimmy Graham, GNB',       'position': 'TE', 'pre_draft$': 10},
           'Jamison Crowder, WAS':  {'name': 'Jamison Crowder, WAS',    'position': 'WR', 'pre_draft$': 12},
           'LeVeon Bell, NYJ':      {'name': 'LeVeon Bell, NYJ',        'position': 'RB', 'pre_draft$': 50},
           'Mark Ingram, BAL':      {'name': 'Mark Ingram, BAL',        'position': 'RB', 'pre_draft$': 35},
           'Odell Beckham, CLE':    {'name': 'Odell Beckham, CLE',      'position': 'WR', 'pre_draft$': 65},
           'Joe Mixon, CIN':        {'name': 'Joe Mixon, CIN',          'position': 'RB', 'pre_draft$': 30},
           'James Conner, PIT':     {'name': 'James Conner, PIT',       'position': 'RB', 'pre_draft$': 15},
           'Lou FakeGuy, XYZ':      {'name': 'Lou FakeGuy, XYZ',        'position': 'RB', 'pre_draft$': 80},
           'UNKNOWN PLAYER, QB':    {'name': 'UNKNOWN PLAYER, QB',      'position': 'QB', 'pre_draft$': 0},
           'UNKNOWN PLAYER, RB':    {'name': 'UNKNOWN PLAYER, RB',      'position': 'RB', 'pre_draft$': 0},
           'UNKNOWN PLAYER, WR':    {'name': 'UNKNOWN PLAYER, WR',      'position': 'WR', 'pre_draft$': 0},
           'UNKNOWN PLAYER, TE':    {'name': 'UNKNOWN PLAYER, TE',      'position': 'TE', 'pre_draft$': 0},
           'UNKNOWN PLAYER, D/ST':  {'name': 'UNKNOWN PLAYER, D/ST',    'position': 'D/ST', 'pre_draft$': 0},
           'UNKNOWN PLAYER, K':     {'name': 'UNKNOWN PLAYER, K',       'position': 'K', 'pre_draft$': 0},}

# Adjust these as needed
my_team = 'Local Florida Man'
fantasy_teams = ['Local Florida Man', 'Bob Loblaw', 'Team 33', 'Nelson Studs', 'Belichick This', 'Brett Favres Next Team',
                 'New Yawk Mongos', 'Fear the Beard', 'David S. Pumpkins', 'Part Deux', 'K Factor', 'Mustangs',
                 'oh leh dew it', 'Revenge With a Fifth']

# Currently, hardcoded for this format
slots = ['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'TE', 'FLX', 'D/ST', 'K',
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

bench_heir = ['BE1', 'BE2', 'BE3', 'BE4', 'BE5', 'BE6']
rb_heir    = ['RB1', 'RB2'] + bench_heir
wr_heir    = ['WR1', 'WR2'] + bench_heir
qb_heir    = ['QB']         + bench_heir
te_heir    = ['TE']         + bench_heir
k_heir     = ['K']          + bench_heir
dst_heir   = ['D/ST']       + bench_heir

heir_dict = {'RB': rb_heir, 'WR': wr_heir, 'QB': qb_heir, 'TE': te_heir, 'K': k_heir, 'D/ST': dst_heir}
