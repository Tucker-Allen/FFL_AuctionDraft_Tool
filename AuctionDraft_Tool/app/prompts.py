from prompt_toolkit import prompt
from prompt_toolkit.completion.word_completer import WordCompleter
from app import players, fantasy_teams

TeamCompleter = WordCompleter(fantasy_teams,
                              ignore_case=True)

def welcome_screen_prompt():
    print('Welcome to the Fantasy Auction draft Tool Kit! ~by Tucker Allen (https://github.com/Tucker-Allen)')
    prompt('Press any key to continue')

def on_the_block_prompt():
    PlayerCompleter = WordCompleter(list(players),
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
