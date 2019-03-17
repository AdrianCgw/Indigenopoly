import serial
from time import sleep
from urllib.request import urlopen
from timeit import default_timer as timer

ser = serial.Serial('COM5', 9600, timeout=5)
param_web_server = 'http://voicecar.pythonanywhere.com/indigenopoly'

p_players = 3  # number of players
p_money, old_pos, new_pos = [],[], [] # money and position of players
for i in range(p_players):
    p_money.append(0)
    old_pos.append(9)
    new_pos.append(9)

def detect_move(new,old):
    ''' Detects which player moved and to where
    '''    
    for i in range(p_players):
        if new[i] != old[i]:
            return i, new[i]
    return -1,0  #returns player, new_position

while True:
    '''
    key = getch()
    okey = ord(key)
    if okey == 27:  # 27 is escape
        break
    # Special keys (arrows, f keys, ins, del, etc.) generate two codes:
    # first = 224, second = call getch() again to read it
    # only print printable characters
    if okey >= 32 and okey <=126:
        print("from okey: ",key, okey)
        # ser.write(key)
        #ser.write(bytes([okey]))
    '''
    line = ser.readline()
    if len(line):
        for i in range(p_players):
            new_pos[i] = line[i] - 48
        #print('Move: %s to %s' % (mplayer, mlocation))
        print(new_pos)
        urlopen(param_web_server + '?new=' + ','.join([str(x) for x in new_pos]))
    sleep(0.1)  # do not overload the serial with commands!

# %%
    
'''
response = urlopen(param_web_server)
for line in response:
    positions = line.decode('utf-8').strip().split(',')
print(positions)
'''         