from prompt_toolkit import prompt
from prompt_toolkit.completion.word_completer import WordCompleter
from app import my_team, fantasy_teams, master_dict, heir_dict, major_starting_slots

import pickle
players = pickle.load(open('AuctionDraft_Tool/app/all_players.sav', 'rb'))


def player_up(a_player: str):
    name = players[a_player]['name']
    pos = players[a_player]['position']
    espn_pre_draft = str(players[a_player]['espn_pre_draft$'])
    fpros_pre_draft = str(players[a_player]['fpros_pre_draft$'])
    #my_pre_draft = str(players[a_player]['my_pre_draft$'])
    economy = refresh_fraction_economy()

    print('-'*41)
    print('PLAYER UP: ', name)
    print('ESPN_PRE_DRAFT:  ', '$'+espn_pre_draft)
    print('FPROS_PRE_DRAFT: ', '$'+fpros_pre_draft)
    print('FRACTION OF $ REMAINING: ', economy)
    print('-'*41)

    competing_teams = []
    for fantasy_team in fantasy_teams:
        max_bid = master_dict[fantasy_team]['budget'] - ( (master_dict[fantasy_team]['empty_slots']-1) *1)
        if pos in ['QB', 'D/ST', 'K']:
            if not master_dict[fantasy_team]['slots'][pos]['Player']:
                competing_teams.append( (fantasy_team, max_bid, 1, 0) )

        if pos == 'TE':
            te_count = 0
            flx_count = 0
            if not master_dict[fantasy_team]['slots']['TE']['Player']:
                te_count = 1
            if not master_dict[fantasy_team]['slots']['FLX']['Player']:
                flx_count = 1
            if te_count or flx_count:
                competing_teams.append( (fantasy_team, max_bid, te_count, flx_count) )

        if pos == 'RB':
            rb_count = 0
            flx_count = 0
            for slot in ['RB1', 'RB2']:
                if not master_dict[fantasy_team]['slots'][slot]['Player']:
                    rb_count += 1
            if not master_dict[fantasy_team]['slots']['FLX']['Player']:
                flx_count = 1
            if rb_count or flx_count:
                competing_teams.append( (fantasy_team, max_bid, rb_count, flx_count) )

        if pos == 'WR':
            wr_count = 0
            flx_count = 0
            for slot in ['WR1', 'WR2']:
                if not master_dict[fantasy_team]['slots'][slot]['Player']:
                    wr_count += 1
            if not master_dict[fantasy_team]['slots']['FLX']['Player']:
                flx_count = 1
            if wr_count or flx_count:
                competing_teams.append( (fantasy_team, max_bid, wr_count, flx_count) )

    sorted_competing_teams = sorted(competing_teams, key = lambda x: (x[2], x[1], x[3]), reverse=True)
    pretty_display(sorted_competing_teams)


def player_bought(player: dict, fantasy_team: str, price_paid: int):
    #print('Begin player_bought...')
    #players.pop(player['name'])
    master_dict[fantasy_team]['budget'] -= price_paid
    master_dict[fantasy_team]['empty_slots'] -= 1
    economy = refresh_fraction_economy()
    #print('Begin insert_player...')
    insert_player(player, fantasy_team, price_paid)
    print('-'*41)
    print('FRACTION OF $ REMAINING: ', economy)
    print('-'*41)


def refresh_fraction_economy():
    starting_budget = len(fantasy_teams) * 200
    total_remaining = 0
    for team in fantasy_teams:
        total_remaining += master_dict[team]['budget']
    return round(total_remaining / starting_budget, 2)


def insert_player(player: dict, fantasy_team: str, price_paid: int):

    for slot in heir_dict[player['position']]:
        #print('looking at slot: ', slot)
        # Make sure that this player belongs in this spot, top-down
        if price_paid > master_dict[fantasy_team]['slots'][slot]['Price_Paid']:
            #print('Insert found, existing price: ', master_dict[fantasy_team]['slots'][slot]['Price_Paid'], ' price_paid: ', price_paid)
            # If this slot is already empty, insert it and do nothing
            if not master_dict[fantasy_team]['slots'][slot]['Player']:
                #print('Slot was found empty, inserting and breaking')
                master_dict[fantasy_team]['slots'][slot]['Player'] = player['name']
                master_dict[fantasy_team]['slots'][slot]['Position'] = player['position']
                master_dict[fantasy_team]['slots'][slot]['Price_Paid'] = price_paid
                break
            # Otherwise, copy what's in there to temp, insert it, and begin shift_down
            temp_player = master_dict[fantasy_team]['slots'][slot].copy()
            #print('Inserting, while temp_player: ', temp_player)
            master_dict[fantasy_team]['slots'][slot]['Player'] = player['name']
            master_dict[fantasy_team]['slots'][slot]['Position'] = player['position']
            master_dict[fantasy_team]['slots'][slot]['Price_Paid'] = price_paid

            #print('Enter shift_down')
            shift_the_rest_down(temp_player, heir_dict[player['position']], slot, fantasy_team, price_paid)
            # Once done with recursive shift_down, we're done
            break

def shift_the_rest_down(this_player, heir_list, last_slot, fantasy_team, price_paid):
    try:
        next_slot = heir_list[ heir_list.index(last_slot) + 1 ]
        #print('Shift: Next_slot: ', next_slot)

        # If a slot we're sliding into is empty, assign it then stop
        if not master_dict[fantasy_team]['slots'][next_slot]['Player']:
            #print('Shift: Empty Player found, inserting and returning')
            master_dict[fantasy_team]['slots'][next_slot] = this_player
            return

        # Otherwise, grab the temp, insert the last, and shift again
        temp_player = master_dict[fantasy_team]['slots'][next_slot].copy()
        #print('Shift: temp_player: ', temp_player, ' from ', next_slot)
        #print('Shift: inserting this_player: ', this_player, ' into ', next_slot)
        master_dict[fantasy_team]['slots'][next_slot] = this_player
        #print('Shift: Next shift_down')
        shift_the_rest_down(temp_player, heir_list, next_slot, fantasy_team, price_paid)

    except IndexError:
        print('Index Error, Done')
    except:
        print('Some other Error, something broke')


def pretty_display(teams_to_display):
    for competition in teams_to_display:
        total_empty_slots = count_all_starter_slots(competition[0])
        print(competition[0])
        print('\t\tMax bid: ',  '$'+str(competition[1]), \
              '\tPrimary slots: ', str(competition[2]), \
              '\tFlex slots:    ', str(competition[3]), \
              '\tTotal Starter Slots: ', total_empty_slots)

def on_the_block_prompt():
    PlayerCompleter = WordCompleter(list(players.keys()),
                                    ignore_case=True)
    on_the_block = prompt('Player nominated >> ',
                          completer=PlayerCompleter)
    try:
        assert on_the_block in list(players.keys())
        return on_the_block
    except:
        print('Invalid Player name, try again')
        return on_the_block_prompt()

def bought_by_prompt():
    bought_by = prompt('Bought By Fantasy Team >> ',
                       completer=TeamCompleter)
    try:
        assert bought_by in fantasy_teams
        return bought_by
    except:
        print('Invalid Team name, try again')
        return bought_by_prompt()

def cost_prompt():
    cost = prompt('For the Amount of >> ')
    try:
        int(cost)
        return cost
    except:
        print('Looking for an Integer, try again')
        return cost_prompt()

def count_all_starter_slots(fantasy_team):
    empty_count = 0
    for slot in major_starting_slots:
        if not master_dict[fantasy_team]['slots'][slot]['Player']:
            empty_count += 1
    return empty_count

def count_missing_starters(fantasy_team):
    missing_starters = {'QB': 0, 'RB': 0, 'WR': 0, 'TE': 0}
    for slot in ['QB']:
        if not master_dict[fantasy_team]['slots'][slot]['Player']:
            missing_starters['QB'] += 1
    for slot in ['RB1', 'RB2']:
        if not master_dict[fantasy_team]['slots'][slot]['Player']:
            missing_starters['RB'] += 1
    for slot in ['WR1', 'WR2']:
        if not master_dict[fantasy_team]['slots'][slot]['Player']:
            missing_starters['WR'] += 1
    for slot in ['TE']:
        if not master_dict[fantasy_team]['slots'][slot]['Player']:
            missing_starters['TE'] += 1
    return missing_starters

# WHERE THE ACTUAL PROGRAM GETS GOING !!!!! ----------------------------------------------------

TeamCompleter = WordCompleter(fantasy_teams,
                              ignore_case=True)

running = True
while running:
    on_the_block = on_the_block_prompt()

    player_up(on_the_block)

    bought_by = bought_by_prompt()
    cost = cost_prompt()

    player_block_dict = players[on_the_block]
    player_bought(player_block_dict, bought_by, int(cost))

    for team in fantasy_teams:
        missing_starters = count_missing_starters(team)
        # Sort by budget
        print(team)
        print(missing_starters, '\tTotal Budget: ', str(master_dict[team]['budget']), \
              '\tSlots Needed: ', str(master_dict[team]['empty_slots']) )
        print('-'*82)
