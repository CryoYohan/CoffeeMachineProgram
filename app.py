from os import system
from main import *

quarters:float = 0
dimes:float = 0
nickels:float = 0
pennies:float = 0
coffee:str = ""
coffee_machine_money:float = 0
coffee_machine_on:bool = True

# TODO 1: Prompt user to decide which type of drink to dispense
def prompt_coffee()->None:
    global coffee
    coffee = input('What would you like my nigga? (espresso/latte/cappuccino): ').lower()
# TODO 2: Prompt user number of quarters, dimes, nickels, pennies
def insert_coins()->None:
    global quarters, dimes, nickels, pennies
    print('Please insert coins.')
    quarters,dimes,nickels,pennies = float(input("how many quarters?: ")),float(input("how many dimes?: ")),float(input("how many nickels?: ")),float(input("how many pennies?: "))

# TODO 3: Calculate total of coins and check if it meets the price of the picked drink
def calculate_coins(num_quarters, num_dimes,num_nickels,num_pennies)->float:
    total_coins:float = 0
    total_coins += (num_quarters*0.25) + (num_dimes * 0.10) + (num_nickels * 0.05) + (num_pennies * 0.01)
    return total_coins

def dispense_coffee(coffee_type:str)->None:
    coffee_price:float = MENU[coffee_type]['cost']
    money:float = calculate_coins(quarters, dimes, nickels, pennies)
    print("Sorry that's not enough money. Money refunded.") if money < coffee_price else print(get_change(coffee_price=coffee_price, money=money))

def brew_coffee()->bool:
    global coffee
    ingredients = list(resources.keys())
    if not coffee == 'espresso':
        for i in range(0, len(ingredients)-1):
            if not resources[ingredients[i]] < MENU[coffee]['ingredients'][ingredients[i]]:
                resources[ingredients[i]] -= MENU[coffee]['ingredients'][ingredients[i]]
                return True
            else:
                print(f'Coffee Machine has run out of {ingredients[i]}')
                return False

    else:
        if not resources['water'] < MENU[coffee]['ingredients']['water'] or resources['coffee'] < MENU[coffee]['ingredients']['coffee']:
            resources['water'] -= MENU[coffee]['ingredients']['water']
            resources['coffee'] -= MENU[coffee]['ingredients']['coffee']
            return True
        else:
            if resources['water'] < MENU[coffee]['ingredients']['water']:
                print(f'Coffee Machine has run out of water.')
                return False
            elif resources['coffee'] <MENU[coffee]['ingredients']['coffee']:
                print(f'Coffee Machine has run out of coffee.')
                return False

def get_change(money, coffee_price)->str:
    global coffee_machine_money, coffee
    money -= coffee_price
    if brew_coffee():
        coffee_machine_money+= coffee_price
        return f"Here is ${money:.2f} in change\nHere is your {coffee} ☕️. Enjoy!" if not money == 0 else f"You paid the exact amount of ${coffee_price}"
    else:
        return 'Sorry, your money is refunded.'

# TODO 4: Print report when admin type 'report', to check the current resources
def print_report()->None:
    unit: list = ['ml', 'ml', 'g']
    i: int = 0
    for ingredient, amount in resources.items():
        print(f"{ingredient.title()} : {amount}{unit[i]}")
        i += 1
    print(f"Money : ${coffee_machine_money:.2f}")

def coffee_machine()->None:
    global coffee
    while coffee_machine_on:
        try:
            prompt_coffee()
            if coffee == 'off':
                turn_off()
            elif coffee == 'report':
                print_report()
            else:
                if coffee == 'espresso' or coffee =='latte' or coffee =='cappuccino':
                    insert_coins()
                    dispense_coffee(coffee)
                else:
                    raise ValueError

        except ValueError:
            print('Sorry, we only offer these coffee flavors. (espresso/latte/cappuccino)')

# TODO 6: Has a secret 'off' command for admins to turn off or stop the coffee machine program.
def turn_off()->None:
    global coffee_machine_on
    coffee_machine_on = False

if __name__ == "__main__":
    coffee_machine()