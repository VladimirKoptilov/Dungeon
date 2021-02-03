"""

• Dungeon-v1.5
• Author: Vladimir Koptilov
• Email: koptilovvova606@gmail.com

♦♦♦ THANK YOU, FOR BEING WITH US! ♦♦♦

"""

# Imports
from os import getlogin, makedirs as md
from random import randint as ri


# Getting username
user = getlogin()


# First start
def OS():

    try:
        records = open('./.Dangeon/.data/records.dungeon', 'a')
        records.close()

        config = open('./config.ini', 'a')
        config.close()
    except FileNotFoundError:
        md('./.Dangeon/.data')

        records_data = \
            'NAME: DIFFICULTY * COINS * KILLS\n\nSLAVIK:' \
            ' Easy * 300 * 30\nVOVA: Easy * 200 * 20\nDENIS: Easy * 100 * 10'
        records = open('./.Dangeon/.data/records.dungeon', 'w')
        records.write(records_data)
        records.close()

        config_cfg = '11:33: * DUNGEON * '
        config = open('./config.ini', 'w')
        config.write(config_cfg)
        config.close()


# Importing configs
config = open('./config.ini', 'r')
config_cfg = config.read()
cfg_list = config_cfg.split(':')


def logotype():
    # Designer greeting rug
    length = int(cfg_list[0])
    breadth = int(cfg_list[1])

    def out(n, string):
        for i in range(n):
            print("{}".format(string), end='')

    def print_out(hyphen_count, polka_count):
        out(hyphen_count, '-')
        out(polka_count, '.|.')
        out(hyphen_count, '-')
        print('')

    hyphen_count = (breadth - 3) // 2
    polka_count = 1
    for i in range(length):
        if i < (length // 2):
            print_out(hyphen_count, polka_count)
            hyphen_count = hyphen_count - 3
            polka_count = polka_count + 2
        elif i == (length // 2 + 1):
            out((breadth - 13)//2, '-')
            print(cfg_list[2], end='')
            out((breadth - 13)//2, '-')
            print('')
            hyphen_count = hyphen_count + 3
            polka_count = polka_count - 2
        elif (length // 2) < i < length:
            print_out(hyphen_count, polka_count)
            hyphen_count = hyphen_count + 3
            polka_count = polka_count - 2
    print_out(hyphen_count, polka_count)


# BASIC GAME CLASS

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

    # Game menu
    def menu(self):

        self.kills = 0

        # Importing resources
        records = open('./.Dangeon/.data/records.dungeon', 'r')
        records_data = records.read()
        records_list = records_data.split('\n')
        print()
        chs = input(
            f'{prfx} 1. Start the game • \n{prfx} '
            f'2. High score table • \n{prfx} 3. Quit the game • \n{log}'
        )

        if chs == '1':
            # Name
            print(tab)
            choise = input(
                f'{prfx} Your name is: \'{self.name}\' \n'
                f'Want to change? ( Y | N ) \n{log}'
            )

            if (
                choise == 'Y' or
                choise == 'y' or
                choise == 'Н' or
                choise == 'н'
            ):
                self.name = input(f'{prfx} Please, enter your name: \n{log}')
                print(tab)
                print(f'{prfx} Your name is: \'{self.name}\'')
            elif (
                choise == 'N' or
                choise == 'n' or
                choise == 'Т' or
                choise == 'т'
            ):
                print(tab)
                print(f'{prfx} Your name is: \'{self.name}\'')
            else:
                print(tab)
                print(
                    f'{prfx} There is no choice of \'{choise}\' ! \n'
                    f'Set default name: \'{self.name}\''
                )

            # Difficulty
            print(tab)
            diff = input(
                f'{prfx} Set the difficulty: \nE - Easy • \n'
                f'N - Normal • \nH - Hard • \n{log}')

            if diff == 'E' or diff == 'e' or diff == 'У' or diff == 'у':
                self.difficulty = 'Easy'
                print(tab)
                print(f'{prfx} Difficulty was set: \'{self.difficulty}\'')
            elif diff == 'N' or diff == 'n' or diff == 'Т' or diff == 'т':
                self.difficulty = 'Normal'
                print(tab)
                print(f'{prfx} Difficulty was set: \'{self.difficulty}\'')
            elif diff == 'H' or diff == 'h' or diff == 'Р' or diff == 'р':
                self.difficulty = 'Hard'
                print(tab)
                print(f'{prfx} Difficulty was set: \'{self.difficulty}\'')
            else:
                self.difficulty = 'Normal'
                print(tab)
                print(
                    f'{prfx} There is no choice of \'{diff}\' ! \n'
                    f'Default difficulty was set: \'{self.difficulty}\''
                )

            self.settings()
        elif chs == '2':
            print(tab)
            print('•••••••••••••••••••••••••')
            print('\n'.join(records_list))
            print('•••••••••••••••••••••••••')
            self.menu()
        elif chs == '3':
            input()
            quit()
        else:
            print(tab)
            print(f'{prfx} There is no choice of \'{chs}\' !')
            print(tab)
            self.menu()

# MAIN GAME CYCLE

    # Setting the values of the main variables depending on the difficulty
    def settings(self):

        difficulty = {
            'Easy': '20',
            'Normal': '15',
            'Hard': '10'
        }

        self.player_maxhealth = int(difficulty[self.difficulty])
        self.player_health = int(difficulty[self.difficulty])
        self.coins = 0

        print(tab)
        print('                   ***')
        print('******************* - *******************')
        print('***************  |START|  ***************')
        print('******************* - *******************')
        print('                   ***')
        self.start()

# MAIN FUNCTION - GAME LOGIK
    def start(self):

        while self.player_health > 0:
            print(tab)
            print(
                f'{self.name}: \n'
                f'[ {self.player_health}♥ ] *** [ {self.coins}$ ]'
            )
            print(tab)
            self.door = input(
                f'{prfx} Choose a door: \n1 - Door №1 • \n'
                f'2 - Door №2 • \n3 - Door №3 • \n{log}'
            )

            if self.door == '1' or self.door == '2' or self.door == '3':
                prize_list = [
                    'COINS',
                    'HEALTH',
                    'MONSTER'
                ]
                self.door = ri(0, 2)

                try:
                    self.prize = prize_list[int(self.door)]
                except TypeError:
                    print(tab)
                    print(f'There is no choice of \'{self.door}\' !')
                    self.start()

            else:
                print(tab)
                print(f'There is no choice of \'{self.door}\' !')
                self.start()

            self.surprize()

    # Door treatment
    def surprize(self):

        # COINS
        if self.prize == 'COINS':

            coins = {
                'Easy': '10',
                'Normal': '5',
                'Hard': '2'
            }

            self.coins += int(coins[self.difficulty])
            print(tab)
            print(f'{prfx} You got coins + {self.coins}$')

            self.start()
        # LIVES
        elif self.prize == 'HEALTH':

            lives = {
                'Easy': '3',
                'Normal': '2',
                'Hard': '1'
            }

            if (
                self.player_maxhealth - self.player_health >=
                int(lives[self.difficulty])
            ):
                self.player_health += int(lives[self.difficulty])
                print(tab)
                print(f'{prfx} You got + {int(lives[self.difficulty])}♥ lives')
            else:
                health = self.player_maxhealth - self.player_health
                self.player_health += health
                print(tab)

                if health != 0:
                    print(f'{prfx} You got + {health}♥ lives')
                else:
                    print(
                        f'{prfx} You didn\'t get a lives'
                        ' as their value is maximized...'
                    )

            self.start()
        # MONSTER
        elif self.prize == 'MONSTER':
            print(tab)
            monster = input(
                f'{prfx} You met a monster! \n1.Attack • \n2.Run • \n{log}')

            if monster == '1':

                coins = {
                    'Easy': '1',
                    'Normal': '2',
                    'Hard': '3'
                }
                self.coins += int(coins[self.difficulty])
                print(tab)
                print(
                    f'{self.name}: \nATTACK !!! \n{prfx} \'{self.name}\''
                    ' gets coins for courage: + '
                    f'{int(coins[self.difficulty])}$'
                )

                self.attack()
            elif monster == '2':

                damage = {
                    'Easy': f'{ri(0, 1)}',
                    'Normal': f'{ri(0, 2)}',
                    'Hard': f'{ri(1, 3)}'
                }

                if int(damage[self.difficulty]) != 0:
                    self.player_health -= int(damage[self.difficulty])

                    if self.player_health > 0:
                        print(tab)
                        print(
                            f'{self.name}: \nRUN !!! \n'
                            f'{prfx} Monster damages player '
                            f'\'{self.name}\' - '
                            f'{int(damage[self.difficulty])}♥'
                        )

                        if self.difficulty != 'Easy':
                            coins = {
                                'Normal': f'{ri(0, 2)}',
                                'Hard': f'{ri(1, 3)}'
                            }

                            if int(coins[self.difficulty]) != 0:
                                print(
                                    f'\'{self.name}\' louses coins - '
                                    f'{int(coins[self.difficulty])}$'
                                )
                    else:
                        self.game_over()

                self.start()
            else:
                print(tab)
                print(
                    f'{prfx} There is no choise of \'{monster}\' ! \n'
                    ' The default selection is made ...')

                coins = {
                    'Easy': '1',
                    'Normal': '2',
                    'Hard': '3'
                }
                self.coins += int(coins[self.difficulty])
                print(tab)
                print(
                    f'{self.name}: \nATTACK !!! \n{prfx} \'{self.name}\''
                    ' gets coins for courage: + '
                    f'{int(lives[self.difficulty])}$'
                )

                self.attack()

    # Battle with the monster
    def attack(self):
        # Who is first? Let it decide randomly xD
        fa = ri(0, 1)
        fa_list = [
            'PLAYER',
            'MONSTER'
        ]
        first_attack = fa_list[fa]

        monster_health = {
            'Easy': f'{ri(1, 2)}',
            'Normal': f'{ri(3, 5)}',
            'Hard': f'{ri(5, 7)}'
        }

        damage = {
            'Easy': f'{ri(1, 2)}',
            'Normal': f'{ri(2, 5)}',
            'Hard': f'{ri(3, 7)}'
        }

        self.monster_health = int(monster_health[self.difficulty])

        if first_attack == 'PLAYER':

            while (self.monster_health > 0) and (self.player_health > 0):
                self.player_damage = int(damage[self.difficulty])
                self.monster_damage = int(damage[self.difficulty])
                print(tab)
                print(
                    f'{self.name}: Lives [ {self.player_health}♥ ]'
                    f' | Coins [ {self.coins}$ ]'
                )
                print(f'Monster: Lives [ {self.monster_health}♥ ]')

                if self.player_health > 0:
                    self.monster_health -= self.player_damage
                    print(tab)
                    print(
                        f'{prfx} You attack: '
                        f'Monster takes damage - {self.player_damage}♥'
                    )
                    print(f'Monster: Lives [ {self.monster_health}♥ ]')

                if self.monster_health > 0:
                    self.player_health -= self.monster_damage
                    print(tab)
                    print(
                        f'{prfx} Monster attacks: \'{self.name}\''
                        f' takes damage - {self.monster_damage}♥'
                    )
                    print(
                        f'{self.name}: Lives [ {self.player_health}♥ ]'
                        f' | Coins [ {self.coins}$ ]'
                    )

            if self.monster_health <= 0:
                self.kills += 1
                win = ri(1, 10)
                print(tab)
                print(
                    f'{prfx} The monster has been killed!'
                    f' You get coins + {win}$'
                )
                self.start()
            elif self.player_health <= 0:
                self.game_over()

        elif first_attack == 'MONSTER':

            while self.monster_health > 0 and self.player_health > 0:
                self.player_damage = ri(1, 2)
                self.monster_damage = ri(1, 2)
                print(tab)
                print(
                    f'{self.name}: Lives [ {self.player_health}♥ ]'
                    f' | Coins [ {self.coins}$ ]'
                )
                print(f'Monster: Lives [ {self.monster_health}♥ ]')

                if self.monster_health > 0:
                    self.player_health -= self.monster_damage
                    print(tab)
                    print(
                        f'{prfx} Monster attacks: \'{self.name}\''
                        f' takes damage - {self.monster_damage}♥'
                    )
                    print(
                        f'{self.name}: Lives [ {self.player_health}♥ ]'
                        f' | Coins [ {self.coins}$ ]'
                    )

                if self.player_health > 0:
                    self.monster_health -= self.player_damage
                    print(tab)
                    print(
                        f'{prfx} You attack:'
                        f' Monster takes damage - {self.player_damage}♥'
                    )
                    print(f'Monster: Lives [ {self.monster_health}♥ ]')

            if self.monster_health <= 0:
                self.kills += 1
                win = ri(1, 10)
                print(tab)
                print(
                    f'{prfx} The monster has been killed!'
                    f' You get coins + {win}$'
                )
                self.start()
            elif self.player_health <= 0:
                self.game_over()

    # GAME OVER
    def game_over(self):
        print('                    *****')
        print('    ****************  -  ****************')
        print('***************  |GAME_OVER|  ***************')
        print('    ****************  -  ****************')
        print('                    *****')
        # Output and recording of results
        print(tab)
        record = input(
            f'{prfx} Results of player \'{self.name}\': \n'
            f'{prfx} COINS: [ {self.coins}$ ] | KILLS: [ {self.kills} ] \n'
            f'{prfx} Want to write the result to a table? ( Y | N )\n{log}'
        )

        if record == 'Y' or record == 'y' or record == 'Н' or record == 'н':
            records = open('./.Dangeon/.data/records.dungeon', 'a')
            records_data = (
                f'\n{self.name}: '
                f'{self.difficulty} * {self.coins} * {self.kills}'
            )
            records.write(records_data)
            records.close()
            print(tab)
            input(
                f'{prfx} Your results '
                'have been successfully written to the table ... \n'
                f' {prfx} Thank you for being with us!\n'
            )
            self.menu()
        elif record == 'N' or record == 'n' or record == 'Т' or record == 'т':
            input(f'{prfx} Thank you for being with us!')
            self.menu()
        else:
            print(tab)
            input(
                f'{prfx} There is no choice \'{record}\' !'
                ' By default, your results were not recorded ... \n'
                f' {prfx} Thank you for being with us!\n'
            )
            self.menu()


OS()
logotype()
game = Game()
game.menu()
