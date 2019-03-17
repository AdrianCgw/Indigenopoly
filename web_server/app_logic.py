# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 13:42:10 2019

@author: Sophia
"""

import flask
import requests
import json

app = flask.Flask(__name__)
app.secret_key = 'voicy'

param_players_len = 3
param_filename = 'indigenopoly.txt'
param_values = ['old_pos', 'new_pos', 'learns', 'res_score']
param_answer_value = 100
param_forest_value = 60
param_city_value = 120

# mapping score id to square type
# learn, forest, city = 0,1,2
param_square_type = [0,2,0,0,1,1,0,0,0,0]


# Functions ==============================================================

def get_command(name):
    ''' Returns the value of the <name> argument in the pages access string
    '''
    new_command = flask.request.args.get(name, None)
    return new_command

def detect_move(new,old):
    ''' Detects which player moved and to where
    '''
    for i in range(param_players_len):
        if new[i] != old[i]:
            return i, new[i]
    return -1,0  #returns player, new_position

def read_state():
    '''Reads the games state from file. In order of lines:
    old_position, new_position, learn events, resources_score
    '''
    game_state = {}
    with open(param_filename) as f:
        for value in param_values:
            game_state[value] = [int(elem) for elem in f.readline().strip().split(',')]
    return game_state

def state_to_lines(game_state):
    ''' Transforms the state into a list of lines containing comma separated values
    '''
    lines = []
    for value in param_values:
        lines.append(','.join([str(elem) for elem in game_state[value]]))
    return lines

def print_state(game_state):
    ''' Prints state as an html page
    '''
    raw_lines = state_to_lines(game_state)
    lines = []
    for value,line in zip(param_values,raw_lines):
        lines.append(value+': ' + line)
    return '<br>'.join(lines)

def write_state(game_state):
    ''' Writes the state back to file:
    '''
    lines = state_to_lines(game_state)
    with open(param_filename,'w') as f:
        for line in lines:
            f.write(line + '\n')

def reset_state():
    ''' Resets the game state to the start position
    '''
    game_state = {}
    position =[9 for i in range(param_players_len)]
    game_state['old_pos'] = position
    game_state['new_pos'] = position
    game_state['learns'] = [0 for i in range(param_players_len)]
    game_state['res_score'] = [0 for i in range(2 * param_players_len)]
    return game_state

@app.route('/indigenopoly', methods=['POST','GET'])
def indigenopoly():
    '''
    filename = 'indigenopoly.txt'
    filename_new = 'indigenopoly_new.txt'
    #Read the old and the new position
    with open(filename) as f:
        lines = f.readlines()
        old_pos =[x.strip() for x in lines]
    with open(filename_new) as f:
        lines = f.readlines()
        new_pos =[x.strip() for x in lines]
        '''
    game_state = read_state()
    mplayer, mposition = detect_move(game_state['new_pos'], game_state['old_pos'])

    #Check for each possible command:
    # 'new' will add a new position
    new_command = get_command('new')
    if new_command:
        positions = new_command.split(',')
        game_state['new_pos'] = positions
        '''
        with open(filename_new,'w') as f:
            #record the new position
            f.write('\n'.join(positions))
        return 'new position:'+','.join(positions)
        '''
        write_state(game_state)
        return 'New position<br>' + print_state(game_state)

    # 'move' returns the move
    new_command = get_command('move')
    if new_command:
        return str(mplayer) + ',' + str(param_square_type[mposition])

    # 'moved' acknowledge the new move and updates the old position
    new_command = get_command('moved')
    if new_command:
        ''''
        with open(filename,'w') as f:
            f.write('\n'.join(new_pos))
        '''
        game_state['old_pos'] = game_state['new_pos']
        write_state(game_state)
        return 'Moved<br>' + print_state(game_state)

    # 'reset' resets the game state to the starting state
    new_command = get_command('reset')
    if new_command:
        game_state = reset_state()
        write_state(game_state)
        return 'Reseted game<br>' + print_state(game_state)

    # 'learns' returns the number of learns for the player id
    new_command = get_command('learns')
    if new_command:
        return str(game_state['learns'][int(new_command)])

    # 'change_learns'=player,value modifies the number of learns for the player id by value
    new_command = get_command('change_learns')
    if new_command:
        player,value = [int(elem) for elem in new_command.split(',')]
        game_state['learns'][player] += value
        write_state(game_state)
        return 'Changed learns for ' + new_command + '<br>' + print_state(game_state)

    # 'score' returns the resources, points for the player id
    new_command = get_command('score')
    if new_command:
        return str(game_state['res_score'][2* int(new_command)]) + ',' +\
                str(game_state['res_score'][2 * int(new_command) +1])

    # 'answer' adds resources to the player id
    new_command = get_command('answer')
    if new_command:
        game_state['res_score'][2* int(new_command)] += param_answer_value
        write_state(game_state)
        return 'Answered for ' + new_command + '<br>' + print_state(game_state)

    # 'invest'=player_id,value trasforms resources into points for player id
    new_command = get_command('invest')
    if new_command:
        player, value = [int(elem) for elem in new_command.split(',')]
        game_state['res_score'][2* player] -= value
        game_state['res_score'][2* player +1] += value
        write_state(game_state)
        return 'Invested for ' + new_command + '<br>' + print_state(game_state)

    # 'chat' extracts reply from susi ai json
    new_command = get_command('chat')
    if new_command:
        #url = 'http://api.susi.ai/susi/chat.json?q='
        #r = requests.get(url + new_command)
        r_json = json.loads(new_command)
        select = r_json['answers'][0]['actions'][0]['expression']
        return select

    # by default we return the old positions, new positions
    # return '<br>'.join([','.join(old_pos), ','.join(new_pos)])
    return print_state(game_state)
