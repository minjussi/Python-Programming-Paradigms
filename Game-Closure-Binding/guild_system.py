import json
import random
from datetime import datetime

def load_data(file, default):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

# save as json   
def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# 0. Initial Screen
def initial_screen():
    print("=== Adventurer's Guild ===")
    print("[1] Register [2] Login [0] Exit")
    return input("Select: ").strip()

# 1. Register (parameter binding)
def register(username, password, *, pin, **kwargs):
    error_value = []
    # username must be unique
    for userid, user_info in users.items():
        usernames = user_info.get('username')
        if usernames == username:
            error_value.append("Username is already used.")
    # password length
    if len(password) < 8:
        error_value.append("Password must be at least 8 characters.")
    upper = False
    special = False
    for i in password:
        if i in "!@#$%^&*()":
            special = True
        if i.isupper():
            upper = True
    # at least one upper letter
    if upper == False:
        error_value.append("Password must contain at least 1 uppercase letter.")
    # at least one special letter
    if special == False:
        error_value.append("Password must contain at least 1 special letter.")

    if len(pin) != 4:
        error_value.append("PIN must be exactly 4 digits.")
    if not pin.isdigit():
        error_value.append("PIN must be digits.")
    
    if error_value:
        error_message = "\n".join(error_value)
        raise ValueError(error_message)
    else: # success : radnom 5-digit ID
        userid = random.randint(10000, 99999)
        for key, value in kwargs.items():
            if value:
                print("Additional information is entered.")
        return userid

# 2. Login
def login(username, password):
    login_userid = 0
    for userid, user_info in users.items():
        usernames = user_info.get('username')
        if usernames == username:
            if user_info.get("password") == password:
                login_userid = userid
            else:
                raise ValueError("Invalid Password")
    
    if not login_userid:
        raise ValueError("Invalid User")  
    else:
        return login_userid

# 3. Main Screen
def main_screen(user_info):
    print("=== Main ===")
    print(f"User:{user_info['username']} ID:{user_info['userid']} Rank:{user_info['rank']} Stamina:{user_info['stamina']}")
    if user_info.get('skills'):
        print(f"Skills:{user_info.get('skills')}", end=' ')
    else:
        print("Skills:(empty)", end=' ')
    if user_info.get('inventory'):
        print(f"Inventory:{user_info.get('inventory')}")
    else:
        print("Inventory:(empty)")

    print("[1] History [2] Accept Quest [3] Submit Quest [4] Train Skill [9] Logout")
    return input("Select: ").strip()

# XP (user-defined overloaded operators)
class XP:
    def __init__(self, xp = 0):
        self.value = int(xp)
    def __add__(self, amount):
        return XP(self.value + amount)
    def __ge__(self, amount):
        return self.value >= amount

# LootBag Management (user-defined overloaded operators)
class Loot:
    def __init__(self, items):
        self.items = items
    def __add__(self, loots):
        items_copy = self.items.copy() # current inventory items
        for loot, count in loots.items.items():
            items_copy[loot] = items_copy.get(loot, 0) + count
        return Loot(items_copy)
    def __sub__(self, loots):
        items_copy = self.items.copy() # current inventory items
        for loot, count in loots.items.items():
            if items_copy.get(loot, 0) < count:
                raise ValueError(f"There is no items; Necessary items:{loots.items}")
            items_copy[loot] -= count
            if items_copy[loot] == 0:
                del items_copy[loot]
        return Loot(items_copy)

# 4. History
def history(user_info):
    history = user_info.get('history')
    print("--- History (latest first) ---")
    if not history:
        print("There is no history")
        return
    for i in reversed(history):
        if i['action'] == "Accept":
            print(f"[{i['time']}] {i['action']} qid:{i['questid']}")
        elif i['action'] == "Submit":
            print(f"[{i['time']}] {i['action']} qid:{i['questid']} result:{i['result']} {i['reward']}")
        else:
            print(f"[{i['time']}] {i['action']} {i['skill_gain']} {i['minutes']}")
    return

# 5. Accept Quest
def accept_quest(user_info, users, quests):
    print("=== Quest Board ===")
    for questid, quest_info in quests.items():
        print(f"{questid} \"{quest_info.get('title')}\" D:{quest_info.get('difficulty')}", end=' ')
        print("Req:", end= '')
        for skill, minutes in quest_info.get('required').items():
            print(f"\"{skill}\" ≥ {minutes}", end = ' ')
        print(f"Due:{quest_info.get('due')}")

    quest_input = input("Quest ID to accept: ").strip()
    # quest existence
    if quest_input not in quests:
        raise ValueError("Invalid Quest ID.")
    # quest accpetance
    for quest in user_info['accepted']:
        if quest['questid'] == quest_input:
            raise ValueError("Already accepted quest.")

    quest_info = quests[quest_input]
    # skill requirement
    for skill, level in quest_info.get('required').items():
        user_skills = user_info['skills']
        # if there is no skill -> set level as 0
        user_level = user_skills.get(skill, 0)
        if user_level < level:
            raise ValueError("Lack of skill level; train skill")  
    # past due
    due_date = quest_info['due']
    due_date = datetime.strptime(due_date, "%Y-%m-%d")
    if datetime.now().date() > due_date.date():
        raise ValueError("Due date is passed.")
    
    pin_input = input("PIN: ").strip()
    if pin_input != user_info['pin']:
        raise ValueError("Invalid PIN")
    
    # Accept Success
    user_info['accepted'].append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                  "questid": quest_input, "title": quest_info['title'], "difficulty": quest_info['difficulty']})
    user_info['history'].append({"action": "Accept", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                  "questid": quest_input, "title": quest_info['title'], "difficulty": quest_info['difficulty']})
    save_data("user.json", users)
    print(f"✓ Accepted {quest_input}")
    

# 6. Submit Quest
def submit_quest(user_info, users, quest_input, quests, accepted_quest, *proof_items):
    def log(error):
        print(error)
        user_info['history'].append({"action": "Submit", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                  "questid": quest_input, "result": "Fail", "reward": ""})
        save_data("user.json", users)  
    quest_info = quests[quest_input]
    # wrong pin
    pin_input = input("PIN: ").strip()
    if pin_input != user_info['pin']:
        log("Invalid PIN.")
        return
    # insufficient stamina
    if user_info['stamina'] < 10:
        log("Lack of Stamina.")
        return
    
    # check proof items
    items_list = list(proof_items)
    items_dict = {}
    for item in items_list:
        if item in items_dict:
            items_dict[item] += 1
        else:
            items_dict[item] = 1
    try: 
        user_inventory = Loot(user_info.get('inventory', {}))
        req_inventory = Loot(quest_info.get('proof'))
        user_inventory = user_inventory - req_inventory

        rewards = quest_info.get('rewards')
        reward_xp = rewards.get('xp')
        user_info['xp'] = (XP(user_info['xp']) + reward_xp).value
        reward_fame = rewards.get('fame')
        user_info['fame'] += reward_fame
        reward_loot = rewards.get('loots', {})
        reward_inventory = Loot(reward_loot)
        user_inventory = user_inventory + reward_inventory
        user_info['inventory'] = user_inventory.items
    except ValueError as e:
        log(e)
        return
    
    # Success
    user_info['stamina'] -= 10
    # completed quest add
    user_info['completed'].append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                  "questid": quest_info['questid'], "result": "Success", 
                                  "reward": f"XP: {reward_xp}, Fame: {reward_fame}, Loot: {reward_loot}"})
    # accepted quest delete
    user_info['accepted'].remove(accepted_quest)
    # update rank
    if XP(user_info['xp']) >= 100 and user_info['rank'] == "BRONZE":
        user_info['rank'] = "SILVER"
        print("You have been promoted to SILVER rank!")
    elif XP(user_info['xp']) >= 300 and user_info['rank'] == "SILVER":
        user_info['rank'] = "GOLD"
        print("You have been promoted to GOLD rank!")

    user_info['history'].append({"action": "Submit", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                  "questid": quest_info['questid'], "result": "Success", 
                                  "reward": f"XP: {reward_xp}, Fame: {reward_fame}, Loot: {reward_loot}"})
    save_data("user.json", users)
    print(f"✓ Submit OK. +XP {reward_xp}, +Fame {reward_fame}, Loot: {reward_loot}")
    return

# Training Policy (Closure with diminishing returns)
def training_policy(divider):
    current_divider = divider
    def train(minutes):
        nonlocal current_divider
        level = int(minutes / current_divider)
        current_divider += 1
        return level
    return train

TRAINING_POLICIES = {
    "hunting": training_policy(10),
    "herbology": training_policy(10),
    "cooking": training_policy(10),
    "swimming": training_policy(10),
    "fishing": training_policy(10)
}

# 7. Train Skill (closure)
def train_skill(user_info, users):
    skill_input = input("Skill to train (e.g., herbology, hunting, cooking, fishing, swimming): ").strip()
    if skill_input not in TRAINING_POLICIES:
        raise ValueError("Skill name is incorrect.")

    minutes_input = input("Minutes [default 30]: ").strip()
    if not minutes_input:
        minutes_input = "30"
    if not minutes_input.isdigit():
        raise ValueError("Input correct minutes.")

    pin_input = input("PIN: ").strip()
    if pin_input != user_info['pin']:
        raise ValueError("Invalid PIN")
    
    if user_info['stamina'] < 5:
        raise ValueError("Lack of stamina.")
    
    policy = TRAINING_POLICIES[skill_input]
    level = policy(int(minutes_input))

    user_info['stamina'] -= 5
    current_skill = user_info['skills'].get(skill_input, 0)
    user_info['skills'][skill_input] = current_skill + level
    gain = {skill_input:level}

    # Train success
    user_info['history'].append({"action": "Train", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                 "skill": skill_input, "minutes": minutes_input, "skill_gain": gain})
    save_data("user.json", users)
    print(f"✓ Trained {skill_input} +{level} (Stamina -5)")
    return

def guild_rpg(users, quests):
    current_userid = None

    while True:
        if current_userid is None: # 로그인 된 유저가 없는 상태
            select = initial_screen()

            if select == '1':
                print("--- Register ---")
                username = input("Username: ").strip()
                password = input("Password ( >= 8, 1 uppercase, 1 special): ").strip()
                pin = input("PIN (4 digits): ").strip()
                additional_info = input("Put any information to add[Default nothing]: ").strip()
                try:
                    userid = register(username, password, pin=pin, additional_info = additional_info)
                    user_info = {
                        "userid": userid,
                        "username": username,
                        "password": password,
                        "pin": pin,
                        "stamina": 100,
                        "xp": 0,
                        "rank": "BRONZE",
                        "fame":0,
                        "inventory": {},
                        "skills": {},
                        "accepted":[],
                        "completed":[],
                        "history": [],
                        "additional_option":{}
                    }
                    users[userid] = user_info
                    save_data("user.json", users)
                except ValueError as e:
                    print(e)
                except TypeError as e: 
                    print(f"Binding Error: {e}")

            elif select == '2':
                print("--- Login ---")
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                try:
                    current_userid = login(username, password)
                except ValueError as e:
                    print(e)

            elif select == '0':
                break
            else:
                print("")
        
        else: # 로그인이 되어 있는 상태 -> main screen
            current_user_info = users.get(current_userid)
            print()
            select = main_screen(current_user_info)

            # 각 함수 안에서 json 파일에 쓰기
            if select == '1':
                history(current_user_info)
            elif select == '2':
                try:
                    accept_quest(current_user_info, users, quests)
                except ValueError as e:
                    print(e)
            elif select == '3':
                quest_input = input("Quest ID to submit: ").strip()
                def log(error):
                    print(error)
                    current_user_info['history'].append({"action": "Submit", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                                 "questid": quest_input, "result": "Fail", "reward": ""})
                    save_data("user.json", users)
                if quest_input not in quests:
                    print("Invalid Quest ID.")
                    continue
                # accepted quest?
                accepted_quest = None
                for quest in current_user_info['accepted']:
                    if quest['questid'] == quest_input:
                        accepted_quest = quest
                        break
                if not accepted_quest:
                    log("The quest is not accepted.")
                    continue
                # check due date
                due_date = quests[quest_input]['due']
                due_date = datetime.strptime(due_date, "%Y-%m-%d")
                if datetime.now().date() > due_date.date():
                    log("Due date passed.")
                    continue
                items = input("Provide proof items: ").strip()
                proof_items = []
                proof_items.append(items)
                while True:
                    proof_item = input("Add proof item (blank to stop): ").strip()
                    if not proof_item:
                        break
                    proof_items.append(proof_item)
                submit_quest(current_user_info, users, quest_input, quests, accepted_quest, *proof_items)
            elif select == '4':
                try:
                    train_skill(current_user_info, users)
                except ValueError as e:
                    print(e)
            elif select == '9':
                current_userid = None
                print("Logged out.")
            else:
                print("")

users = load_data("user.json", {})
quests = load_data("quest.json", {})

guild_rpg(users, quests)
