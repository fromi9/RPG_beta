from random import randint, choices

class Player:
    def __init__(self):
        self.hp = randint(100, 150)
        self.base_damage = randint(10, 20)
        self.inventory = {"Healing Potion": 0}
        self.gold = 0
        self.weapon = None
        self.weapons = []

    def get_damage(self):
        weapon_damage = self.weapon.bonus_damage if self.weapon else 0
        return self.base_damage + weapon_damage

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"Вы экипировали {weapon.name}, теперь у вас {self.get_damage()} урона.")

    def show_inventory(self):
        print("**Ваш инвентарь:**")
        print(f" Золото: {self.gold}")
        print(f" Зелья лечения: {self.inventory['Healing Potion']}")
        print("Оружие:")
        
        if self.weapons:
            for i, weapon in enumerate(self.weapons, 1):
                equipped = " (Экипировано)" if self.weapon == weapon else ""
                print(f"{i}. {weapon}{equipped}")
        else:
            print("У вас нет оружия.")

        while True:
            print("\n1) Выпить зелье")
            print("2) Экипировать оружие")
            print("9) Вернуться в меню")
            n = input("Что хотите сделать: ")

            if n == "1":
                if self.inventory["Healing Potion"] > 0:
                    heal = randint(10, 20)
                    self.hp = min(150, self.hp + heal)
                    self.inventory["Healing Potion"] -= 1
                    print(f"Вы выпили зелье и восстановили {heal} HP. Ваше здоровье теперь {self.hp}.")
                else:
                    print("У вас нет зелий!")

            elif n == "2":
                if not self.weapons:
                    print("У вас нет оружия для экипировки.")
                    continue

                print("Выберите оружие для экипировки:")
                for i, weapon in enumerate(self.weapons, 1):
                    print(f"{i}) {weapon}")

                try:
                    choice = int(input("Введите номер оружия (или 9 для выхода): ")) - 1
                    if 0 <= choice < len(self.weapons):
                        self.equip_weapon(self.weapons[choice])
                    elif choice == 9 :
                        break
                    else:
                        print("Неверный выбор.")
                except ValueError:
                    print("Некорректный ввод.")

            elif n == "9":
                break
            else:
                print("Неверный ввод! Попробуйте снова.")
                
class Weapon:
    def __init__(self, name, bonus_damage, price, drop_chance):
        self.name = name
        self.bonus_damage = bonus_damage
        self.price = price
        self.drop_chance = drop_chance 

    def __str__(self):
        return f"{self.name} (+{self.bonus_damage} урона, {self.price} золота)"

weapons_list = [
    Weapon("Кинжал", 3, 15, 50),  
    Weapon("Меч", 5, 30, 30),      
    Weapon("Боевой топор", 7, 50, 15),  
    Weapon("Длинный лук", 4, 40, 20),  
    Weapon("Легендарный меч", 10, 100, 5)  
]

def get_random_weapon():
    return choices(weapons_list, weights=[w.drop_chance for w in weapons_list], k=1)[0]
        
class Enemy:
    def __init__(self):
        self.hp = randint(70, 90)
        self.damage = randint(6, 10)
        self.gold = randint(15, 50)

def menu(player):
    while True:
        print("**Главное меню**")
        print("1) Сражаться")
        print("2) Статистика")
        print("3) Инвентарь")
        print("4) Магазин")
        print("9) Выйти")

        choice = input("Выберите действие: ")
        if choice == "1":
            menu_fight(player)
        elif choice == "2":
            print(f"ХП: {player.hp} | Урон: {player.get_damage()} | Золото: {player.gold}")
        elif choice == "3":
            player.show_inventory()
        elif choice == "4":
            menu_store(player)
        elif choice == "9":
            print("Вы вышли из игры.")
            exit()
        else:
            print("Неверный выбор.")

def menu_store(player):
    while True:
        print("**Магазин**")
        print("1) Купить зелье лечения (10 золота)")
        print("2) Купить оружие")
        print("3) Продать оружие")
        print("9) Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            if player.gold >= 10:
                player.gold -= 10
                player.inventory["Healing Potion"] += 2
                print(f"Вы купили зелье. Теперь у вас {player.inventory['Healing Potion']} зелий и {player.gold} золота.")
            else:
                print("Недостаточно золота.")

        elif choice == "2":
            print("**Доступное оружие:**")
            for i, weapon in enumerate(weapons_list, 1):
                print(f"{i}) {weapon}")
            
            try:
                n = int(input("Выберите оружие для покупки (9 - выйти): ")) - 1
                if 9 <= n < len(weapons_list):
                    weapon = weapons_list[n]
                    if player.gold >= weapon.price:
                        player.gold -= weapon.price
                        player.weapons.append(weapon)
                        print(f"Вы купили {weapon.name}! Теперь у вас {player.gold} золота.")
                    else:
                        print("Недостаточно золота.")
            except ValueError:
                print("Неверный ввод.")

        elif choice == "3":
            if not player.weapons:
                print("У вас нет оружия для продажи.")
                continue

            print("**Ваше оружие:**")
            for i, weapon in enumerate(player.weapons, 1):
                print(f"{i}) {weapon} (Продажа: {weapon.price // 2} золота)")

            try:
                n = int(input("Выберите оружие для продажи (9 - выйти): ")) - 1
                if 9 <= n < len(player.weapons):
                    weapon = player.weapons.pop(n)
                    player.gold += weapon.price // 2
                    print(f"Вы продали {weapon.name} за {weapon.price // 2} золота. Теперь у вас {player.gold} золота.")

                    if player.weapon == weapon:
                        player.weapon = None
                else:
                    print("Неверный выбор.")
            except ValueError:
                print("Неверный ввод.")

        elif choice == "9":
            break

        else:
            print("Неверный выбор.")

def menu_fight(player):
    enemy = Enemy()
    print("Вы встретили врага!")
    
    while player.hp > 0 and enemy.hp > 0:
        print(f"Ваша ХП: {player.hp} | Урон: {player.get_damage()}")
        print(f"ХП Врага: {enemy.hp} | Урон: {enemy.damage}")
        print("1) Ударить")
        print("2) Использовать зелье")

        n = input("Введите число: ")
        if n == "1":
            enemy.hp -= player.get_damage()
            print(f"Вы ударили врага, у него осталось {enemy.hp} ХП.")

            if enemy.hp <= 0:
                print("Вы победили!")
                player.gold += enemy.gold
                print(f"Вы получили {enemy.gold} золота. Теперь у вас {player.gold} золота.")
                if randint(1, 100) <= 30:
                    dropped_weapon = get_random_weapon()
                    print(f"Вы нашли {dropped_weapon.name} (+{dropped_weapon.bonus_damage} урона)!")
                    player.weapons.append(dropped_weapon)
                break

            player.hp -= enemy.damage
            print(f"Враг ударил вас, у вас осталось {player.hp} ХП.")

        elif n == "2":
            if player.inventory["Healing Potion"] > 0:
                heal = randint(10, 20)
                player.hp = min(150, player.hp + heal)
                player.inventory["Healing Potion"] -= 1
                print(f"Вы использовали зелье. Теперь у вас {player.hp} ХП.")
            else:
                print("У вас нет зелий!")
        
        if player.hp <= 0:
            print("Вы проиграли! Игра окончена.")
            exit()

player = Player()
menu(player)
