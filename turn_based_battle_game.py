import random

class Character:
    def __init__(self, name, hp, attack, defense, speed, stamina=100, actions=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.is_defending = False
        self.speed = speed
        self.stamina = stamina
        self.max_stamina = stamina
        self.actions = actions if actions else []


    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def recover_stamina(self, amount):
        self.stamina = min(self.stamina + amount, self.max_stamina)

def calculate_damage(attacker, defender, multiplier=1):
    damage = int(max((attacker.attack - defender.defense) * multiplier, 1))
    is_critical = False
    if random.random() < 0.12:
        damage *= 2
        is_critical = True
    if defender.is_defending:
        damage //= 2
    return damage, is_critical

class Action:
    name = "Unnamed Action"
    def execute(self, attacker, defender, engine):
        raise NotImplementedError("Subclasses must implement execute!")

class AttackAction(Action):
    name = "Attack"
    def execute(self, attacker, defender, engine):
        damage, is_critical = calculate_damage(attacker, defender)
        defender.take_damage(damage)
        engine.events.append(f"{attacker.name} attacks {defender.name} for {damage} damage!")
        if is_critical:
            engine.events.append(f"{attacker.name} lands a Critical Hit!")

class PowerAttackAction(Action):
    name = "Power Attack"
    COST = 30
    MULTIPLIER = 1.5

    def execute(self, attacker, defender, engine):
        if attacker.stamina < self.COST:
            engine.events.append(f"{attacker.name} tried Power Attack but doesn't have enough stamina!")
            return
        attacker.stamina -= self.COST
        if random.random() < 0.25:
            engine.events.append(f"{attacker.name} tries a Power Attack but misses!")
            return
        damage, is_critical = calculate_damage(attacker, defender, multiplier=self.MULTIPLIER)
        defender.take_damage(damage)
        engine.events.append(f"{attacker.name} uses Power Attack on {defender.name} for {damage}!")
        if is_critical:
            engine.events.append(f"{attacker.name} lands a Critical Hit with Power Attack!")

class DefendAction(Action):
    name = "Defend"
    def execute(self, attacker, defender, engine):
        attacker.is_defending = True
        engine.events.append(f"{attacker.name} is defending!")

class HesitateAction(Action):
    def execute(self, attacker, defender, engine):
        engine.events.append(f"{attacker.name} hesitates!")

class BattleEngine:
    STAMINA_RECOVERY = 10

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 1
        self.events = []

    def next_turn(self):
        self.reset_defend()
        first, second = (self.player, self.enemy) if self.player.speed >= self.enemy.speed else (self.enemy, self.player)

        for attacker, defender in [(first, second), (second, first)]:
            if not self.player.is_alive() or not self.enemy.is_alive():
                break
            self.resolve_action(attacker, defender)

        self.player.recover_stamina(self.STAMINA_RECOVERY)
        self.enemy.recover_stamina(self.STAMINA_RECOVERY)
        self.turn += 1

    def reset_defend(self):
        self.player.is_defending = False
        self.enemy.is_defending = False

    def resolve_action(self, attacker, defender):
        action = self.decide_action(attacker, defender)
        action.execute(attacker, defender, self)

    def decide_action(self, character, opponent):
        if character == self.player:
            return self.player_input()
        else:
            return self.enemy_decide(character, opponent)

    def player_input(self):
        while True:
            print(f"\nYour stamina: {self.player.stamina}/{self.player.max_stamina}")
            print("\nChoose your action:")

            for i, action in enumerate(self.player.actions, 1):
                print(f"{i}: {action.name}")

            choice = input("Enter number: ")

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.player.actions):
                    return self.player.actions[index]

            print("Invalid choice, try again.")

    def enemy_decide(self, enemy, player):
        possible_actions = []

        for action in enemy.actions:

            if isinstance(action, PowerAttackAction):
                if enemy.stamina >= PowerAttackAction.COST:
                    possible_actions.append(action)
            else:
                possible_actions.append(action)

        return random.choice(possible_actions)

player = Character("Knight", 100, 15, 5, 6,
                   actions=[AttackAction(), DefendAction(), PowerAttackAction()])
enemy = Character("Goblin", 60, 10, 3, 4.2,
                  actions=[AttackAction(), DefendAction(), PowerAttackAction(), HesitateAction()])

engine = BattleEngine(player, enemy)

while player.is_alive() and enemy.is_alive():
    engine.next_turn()
    print(f"\n--- Turn {engine.turn - 1} ---")
    for event in engine.events:
        print(event)
    print(f"{player.name}: {player.hp}/{player.max_hp}, Stamina: {player.stamina}/{player.max_stamina}")
    print(f"{enemy.name}: {enemy.hp}/{enemy.max_hp}, Stamina: {enemy.stamina}/{enemy.max_stamina}")
    engine.events.clear()

print("\nBattle finished!")
if player.is_alive():
    print("Player wins!")
else:
    print("Enemy wins!")


