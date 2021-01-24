### Imports ###
from os import getlogin, makedirs as md
from random import randint as ri


### Getting username ###
user = getlogin()

### First start ###
try:
    records = open('./.Dangeon/.data/records.dungeon', 'a')
    records.close()

    config = open('./config.ini', 'a')
    config.close()
except FileNotFoundError:
    md('./.Dangeon/.data')

    records_data = 'NAME: DIFFICULTY * COINS * KILLS\n\nSLAVIK: Easy * 300 * 30\nVOVA: Easy * 200 * 20\nDENIS: Easy * 100 * 10'
    records = open('./.Dangeon/.data/records.dungeon', 'w')
    records.write(records_data)
    records.close()

    config_cfg = '11:33: * DUNGEON * '
    config = open('./config.ini', 'w')
    config.write(config_cfg)
    config.close()

### Importing configs ###
config = open('./config.ini', 'r')
config_cfg = config.read()
cfg_list = config_cfg.split(':')

### Designer greeting rug ###
length = int(cfg_list[0])
breadth = int(cfg_list[1])

def out(n,string):
    for i in range(n):
        print ("{}".format(string), end='')

def print_out(hyphen_count,polka_count):
    out(hyphen_count, '-')
    out(polka_count, '.|.')
    out(hyphen_count, '-')
    print ('')

hyphen_count = (breadth - 3) // 2
polka_count = 1
for i in range(length):
    if i < (length // 2):
        print_out(hyphen_count,polka_count)        
        hyphen_count = hyphen_count - 3
        polka_count = polka_count + 2
    elif i == (length // 2 + 1):
        out((breadth - 13)//2, '-')
        print (cfg_list[2], end='')
        out((breadth - 13)//2, '-')
        print ('')
        hyphen_count = hyphen_count + 3
        polka_count = polka_count - 2        
    elif (length // 2) < i < length:
        print_out(hyphen_count,polka_count)        
        hyphen_count = hyphen_count + 3
        polka_count = polka_count - 2 
print_out(hyphen_count,polka_count)

####### BASIC GAME CLASS #######

tab = '\n-------------------------\n'
prfx = '[ ♦ DUNGEON ♦ ]'
log = '>>> '


class Game:
    name = user
    player_health = 0
    player_maxhealth = 0
    monster_health = 0
    coins = 0
    player_damage = 0
    monster_damage = 0
    door = None
    prize = None
    kills = 0
    difficulty = None

    ### Game menu ###
    def menu(self):
        ### Importing resources ###
        records = open('./.Dangeon/.data/records.dungeon', 'r')
        records_data = records.read()
        records_list = records_data.split('\n')
        print()
        chs = input(f'{prfx} 1. Start the game • \n{prfx} 2. High score table • \n{prfx} 3. Quit the game • \n{log}')

        if chs == '1':
            ### Name ###
            print(tab)
            choise = input(f'{prfx} Your name is: \'{self.name}\' \nWant to change? ( Y | N ) \n{log}')

            if (choise == 'Y') or (choise == 'y') or (choise == 'Н') or (choise == 'н') :
                self.name = input(f'{prfx} Please, enter your name: \n{log}')
                print(tab)
                print(f'{prfx} Your name is: \'{self.name}\'')
            elif (choise == 'N') or (choise == 'n') or (choise == 'Т') or (choise == 'т') :
                print(tab)
                print(f'{prfx} Your name is: \'{self.name}\'')
            else:
                print(tab)
                print(f'{prfx} There is no choice of \'{choise}\' ! \nSet default name: \'{self.name}\'')

            ### Difficulty ###
            print(tab)
            diff = input(f'{prfx} Set the difficulty: \nE - Easy • \nN - Normal • \nH - Hard • \n{log}')

            if (diff == 'E') or (diff == 'e') or (diff == 'У') or (diff == 'у') :
                self.difficulty = 'Easy'
                print(tab)
                print(f'{prfx} Difficulty was set: \'{self.difficulty}\'')
            elif (diff == 'N') or (diff == 'n') or (diff == 'Т') or (diff == 'т'):
                self.difficulty = 'Normal'
                print(tab)
                print(f'{prfx} Difficulty was set: \'{self.difficulty}\'')
            elif (diff == 'H') or (diff == 'h') or (diff == 'Р') or (diff == 'р') :
                self.difficulty = 'Hard'
                print(tab)
                print(f'{prfx} Difficulty was set: \'{self.difficulty}\'')
            else:
                self.difficulty = 'Normal'
                print(tab)
                print(f'{prfx} There is no choice of \'{diff}\' ! \nDefault difficulty was set: \'{self.difficulty}\'')

            self.settings()       
        elif chs == '2' :
            print(tab)
            print('•••••••••••••••••••••••••')
            print('\n'.join(records_list))
            print('•••••••••••••••••••••••••')
            self.menu()
        elif chs == '3' :
            input()
            quit()
        else:
            print(tab)
            print(f'{prfx} There is no choice of \'{chs}\' !')
            print(tab)
            self.menu()

####### MAIN GAME CYCLE #######

    ### Setting the values of the main variables depending on the difficulty ###
    def settings(self):

        if self.difficulty == 'Easy':
            self.player_maxhealth = 20
            self.player_health = 20
            self.coins = 0
        elif self.difficulty == 'Normal':
            self.player_maxhealth = 15
            self.player_health = 15
            self.coins = 0
        elif self.difficulty == 'Hard':
            self.player_maxhealth = 10
            self.player_health = 10
            self.coins = 0
        
        print(tab)
        print('                   ***'                   )
        print('******************* - *******************')
        print('***************  |START|  ***************')
        print('******************* - *******************')
        print('                   ***'                   )
        self.start()

####### MAIN FUNCTION - GAME LOGIK #######
    def start(self):

        while self.player_health > 0:
            print(tab)
            print(f'{self.name}: \n[ {self.player_health}♥ ] *** [ {self.coins}$ ]')
            print(tab)
            self.door = input(f'{prfx} Choose a door: \n1 - Door №1 • \n2 - Door №2 • \n3 - Door №3 • \n{log}')

            if (self.door == '1') or (self.door == '2') or (self.door == '3') :
                prize_list = [
                    'COINS', 
                    'HEALTH', 
                    'MONSTER'
                ]
                self.door = ri(0, 2)

                try:
                    self.prize = prize_list[int(self.door)]
                except:
                    print(tab)
                    print(f'There is no choice of \'{self.door}\' !')
                    self.start()

            else:
                print(tab)
                print(f'There is no choice of \'{self.door}\' !')
                self.start()

            self.surprize()

    ### Door treatment ###
    def surprize(self):

        ### COINS ###
        if self.prize == 'COINS':

            if self.difficulty == 'Easy':
                self.coins += 10
                print(tab)
                print(f'{prfx} You got coins + 10$')
            elif self.difficulty == 'Normal':
                self.coins += 5
                print(tab)
                print(f'{prfx} You got coins + 5$')
            elif self.difficulty == 'Hard':
                self.coins += 2
                print(tab)
                print(f'{prfx} You got coins + 2$')

            self.start()
        ### LIVES ###
        elif self.prize == 'HEALTH':

            if self.difficulty == 'Easy':

                if  (self.player_maxhealth - self.player_health >= 3) :
                    self.player_health += 3
                    print(tab)
                    print(f'{prfx} You got + 3♥ lives')
                else:
                    health = self.player_maxhealth - self.player_health
                    self.player_health += health
                    print(tab)

                    if health != 0:
                        print(f'{prfx} You got + {health}♥ lives')
                    else:
                        print(f'{prfx} You didn\'t get a lives as their value is maximized...')

            elif self.difficulty == 'Normal':

                if  (self.player_maxhealth - self.player_health >= 2) :
                    self.player_health += 2
                    print(tab)
                    print(f'{prfx} You got + 2♥ lives')            
                else:
                    health = self.player_maxhealth - self.player_health
                    self.player_health += health
                    print(tab)

                    if health != 0:
                        print(f'{prfx} You got + {health}♥ lives')
                    else:
                        print(f'{prfx} You didn\'t get a lives as their value is maximized...')

            elif self.difficulty == 'Hard':

                if  (self.player_maxhealth - self.player_health >= 1) :
                    self.player_health += 1
                    print(tab)
                    print(f'{prfx} You got + 1♥ lives')
                else:
                    health = self.player_maxhealth - self.player_health
                    self.player_health += health
                    print(tab)
                    
                    if health != 0:
                        print(f'{prfx} You got + {health}♥ lives')
                    else:
                        print(f'{prfx} You didn\'t get a lives as their value is maximized...')

            self.start()
        ### MONSTER ###
        elif self.prize == 'MONSTER':
            print(tab)
            monster = input(f'{prfx} You met a monster! \n1.Attack • \n2.Run • \n{log}')

            if monster == '1':

                if self.difficulty == 'Easy':
                    self.coins += 1
                    print(tab)
                    print(f'{self.name}: \nATTACK !!! \n{prfx} \'{self.name}\' gets coins for courage: + 1$')
                elif self.difficulty == 'Normal':
                    self.coins += 2
                    print(tab)
                    print(f'{self.name}: \nATTACK !!! \n{prfx} \'{self.name}\' gets coins for courage: + 2$')
                elif self.difficulty == 'Hard':
                    self.coins += 3
                    print(tab)
                    print(f'{self.name}: \nATTACK !!! \n{prfx} \'{self.name}\' gets coins for courage: + 3$')
                
                self.attack()
            elif monster == '2':

                if self.difficulty == 'Easy':
                    damage = ri(0, 1)
                    self.player_health -= damage
                    print(tab)
                    print(f'{self.name}: \nRUN !!! \n{prfx} Monster damages player \'{self.name}\' - {damage}♥')
                elif self.difficulty == 'Normal':
                    damage = ri(0, 2)
                    coins = ri(1, 5)

                    if (self.coins - coins >= 0):
                        self.coins -= coins

                    self.player_health -= damage
                    print(tab)
                    print(f'{self.name}: \nRUN !!! \n{prfx} Monster damages player \'{self.name}\' - {damage}♥ and he loses coins - {coins}$')
                elif self.difficulty == 'Hard':
                    damage = ri(1, 3)
                    coins = ri(1, 5)

                    if (self.coins - coins >= 0):
                        self.coins -= coins
                    self.player_health -= damage
                    print(tab)
                    print(f'{self.name}: \nRUN !!! \n{prfx} Monster damages player \'{self.name}\' - {damage}♥ and he loses coins - {coins}$')

                self.start()
            else:
                print(tab)
                print(f'{prfx} There is no choise of \'{monster}\' ! \n The default selection is made ...')

                if self.difficulty == 'Easy':
                    self.coins += 1
                    print(tab)
                    print(f'{self.name}: \nATTACK !!! \n{prfx} \'{self.name}\' gets coins for courage: + 1$')
                elif self.difficulty == 'Normal':
                    self.coins += 2
                    print(tab)
                    print(f'{self.name}: \nATTACK !!! \n{prfx} \'{self.name}\' gets coins for courage: + 2$')
                elif self.difficulty == 'Hard':
                    self.coins += 3
                    print(tab)
                    print(f'{self.name}: \nATTACK !!! \n{prfx} \'{self.name}\' gets coins for courage: + 3$')
             
                self.attack()

    ### Battle with the monster ###
    def attack(self):
        ### Who is first? Let it decide randomly xD ###
        fa = ri(0, 1)
        fa_list = [
            'PLAYER', 
            'MONSTER'
        ]
        first_attack = fa_list[fa]

        if self.difficulty == 'Easy':
            self.monster_health = ri(1, 2)

            if first_attack == 'PLAYER':

                while (self.monster_health > 0) and (self.player_health > 0):
                    self.player_damage = ri(1, 2)
                    self.monster_damage = ri(1, 2)
                    print(tab)
                    print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')
                    print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.player_health > 0:
                        self.monster_health -= self.player_damage
                        print(tab)
                        print(f'{prfx} You attack: Monster takes damage - {self.player_damage}♥')
                        print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.monster_health > 0:
                        self.player_health -= self.monster_damage
                        print(tab)
                        print(f'{prfx} Monster attacks: \'{self.name}\' takes damage - {self.monster_damage}♥')
                        print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')

                if self.monster_health <= 0:
                    self.kills += 1
                    win = ri(1, 10)
                    print(tab)
                    print(f'{prfx} The monster has been killed! You get coins + {win}$')
                    self.start()
                elif self.player_health <= 0:
                    self.game_over()

            elif first_attack == 'MONSTER':

                while (self.monster_health > 0) and (self.player_health > 0):
                    self.player_damage = ri(1, 2)
                    self.monster_damage = ri(1, 2)
                    print(tab)
                    print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')
                    print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.monster_health > 0:
                        self.player_health -= self.monster_damage
                        print(tab)
                        print(f'{prfx} Monster attacks: \'{self.name}\' takes damage - {self.monster_damage}♥')
                        print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')
                    
                    if self.player_health > 0:
                        self.monster_health -= self.player_damage
                        print(tab)
                        print(f'{prfx} You attack: Monster takes damage - {self.player_damage}♥')
                        print(f'Monster: Lives [ {self.monster_health}♥ ]')

                if self.monster_health <= 0:
                    self.kills += 1
                    win = ri(1, 10)
                    print(tab)
                    print(f'{prfx} The monster has been killed! You get coins + {win}$')
                    self.start()
                elif self.player_health <= 0:
                    self.game_over()

        elif self.difficulty == 'Normal':           
            self.monster_health = ri(3, 5)

            if first_attack == 'PLAYER':

                while (self.monster_health > 0) and (self.player_health > 0):
                    self.player_damage = ri(2, 5)
                    self.monster_damage = ri(2, 5)
                    print(tab)
                    print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')
                    print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.player_health > 0:
                        self.monster_health -= self.player_damage
                        print(tab)
                        print(f'{prfx} You attack: Monster takes damage - {self.player_damage}♥')
                        print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.monster_health > 0:
                        self.player_health -= self.monster_damage
                        print(tab)
                        print(f'{prfx} Monster attacks: \'{self.name}\' takes damage - {self.monster_damage}♥')
                        print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')

                if self.monster_health <= 0:
                    self.kills += 1
                    win = ri(1, 5)
                    print(tab)
                    print(f'{prfx} The monster has been killed! You get coins + {win}$')
                    self.start()
                elif self.player_health <= 0:
                    self.game_over()

            elif first_attack == 'MONSTER':

                while (self.monster_health > 0) and (self.player_health > 0):
                    self.player_damage = ri(2, 5)
                    self.monster_damage = ri(2, 5)
                    print(tab)
                    print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')
                    print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.monster_health > 0:
                        self.player_health -= self.monster_damage
                        print(tab)
                        print(f'{prfx} Monster attacks: \'{self.name}\' takes damage - {self.monster_damage}♥')
                        print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')

                    if self.player_health > 0:
                        self.monster_health -= self.player_damage
                        print(tab)
                        print(f'{prfx} You attack: Monster takes damage - {self.player_damage}♥')
                        print(f'Monster: Lives [ {self.monster_health}♥ ]')

                if self.monster_health <= 0:
                    self.kills += 1
                    win = ri(1, 5)
                    print(tab)
                    print(f'{prfx} The monster has been killed! You get coins + {win}$')
                    self.start()
                elif self.player_health <= 0:
                    self.game_over() 

        elif self.difficulty == 'Hard':           
            self.monster_health = ri(5, 7)

            if first_attack == 'PLAYER':

                while (self.monster_health > 0) and (self.player_health > 0):
                    self.player_damage = ri(3, 7)
                    self.monster_damage = ri(3, 7)
                    print(tab)
                    print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')
                    print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.player_health > 0:
                        self.monster_health -= self.player_damage
                        print(tab)
                        print(f'{prfx} You attack: Monster takes damage - {self.player_damage}♥')
                        print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.monster_health > 0:
                        self.player_health -= self.monster_damage
                        print(tab)
                        print(f'{prfx} Monster attacks: \'{self.name}\' takes damage - {self.monster_damage}♥')
                        print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')

                if self.monster_health <= 0:
                    self.kills += 1
                    win = ri(1, 3)
                    print(tab)
                    print(f'{prfx} The monster has been killed! You get coins + {win}$')
                    self.start()
                elif self.player_health <= 0:
                    self.game_over()

            elif first_attack == 'MONSTER':

                while (self.monster_health > 0) and (self.player_health > 0):
                    self.player_damage = ri(3, 7)
                    self.monster_damage = ri(3, 7)
                    print(tab)
                    print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')
                    print(f'Monster: Lives [ {self.monster_health}♥ ]')

                    if self.monster_health > 0:
                        self.player_health -= self.monster_damage
                        print(tab)
                        print(f'{prfx} Monster attacks: \'{self.name}\' takes damage - {self.monster_damage}♥')
                        print(f'{self.name}: Lives [ {self.player_health}♥ ] | Coins [ {self.coins}$ ]')

                    if self.player_health > 0:
                        self.monster_health -= self.player_damage
                        print(tab)
                        print(f'{prfx} You attack: Monster takes damage - {self.player_damage}♥')
                        print(f'Monster: Lives [ {self.monster_health}♥ ]')

                if self.monster_health <= 0:
                    self.kills += 1
                    win = ri(1, 3)
                    print(tab)
                    print(f'{prfx} The monster has been killed! You get coins + {win}$')
                    self.start()
                elif self.player_health <= 0:
                    self.game_over()

    ### GAME OVER ###
    def game_over(self):
        print('                    *****'                    )
        print('    ****************  -  ****************'    )
        print('***************  |GAME_OVER|  ***************')
        print('    ****************  -  ****************'    )
        print('                    *****'                    )
        ### Output and recording of results ###
        print(tab)
        record = input(f'{prfx} Results of player \'{self.name}\': \n{prfx} COINS: [ {self.coins}$ ] | KILLS: [ {self.kills} ] \n{prfx} Want to write the result to a table? ( Y | N )\n{log}')

        if (record == 'Y') or (record == 'y') or (record == 'Н') or (record == 'н'):
            records = open('./.Dangeon/.data/records.dungeon', 'a')
            records_data = f'\n{self.name}: {self.difficulty} * {self.coins} * {self.kills}'
            records.write(records_data)
            records.close()
            print(tab)
            input(f'{prfx} Your results have been successfully written to the table ... \n {prfx} Thank you for being with us!\n')
            self.menu()
        elif (record == 'N') or (record == 'n') or (record == 'Т') or (record == 'т'):
            input()
            self.menu()
        else:
            print(tab)
            input(f'{prfx} There is no choice \'{record}\' ! By default, your results were not recorded ... \n {prfx} Thank you for being with us!\n')
            self.menu()


game = Game()
game.menu()