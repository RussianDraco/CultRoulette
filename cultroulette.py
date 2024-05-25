import random
import time
import colorama
import winsound
from colorama import Fore, Style
colorama.init()

MAX_HEALTH = 10

playerHealth = MAX_HEALTH
enemyHealth = MAX_HEALTH

enemybullets = None
enemyblanks = None
enemyMemory = []

revolverSharded = False

playercannotitem = False
enemycannotitem = False

playeritems = []
enemyitems = []

bullets = [] #max : 8

def play_sound(name):
    winsound.PlaySound("sounds/" + name + ".wav", winsound.SND_FILENAME)
def colorprint(text, color):
    print(color + text + Style.RESET_ALL)
def display_stats():
    colorprint(f"Your health: {playerHealth}", Fore.LIGHTGREEN_EX)
    colorprint(f"Enemy health: {enemyHealth}", Fore.LIGHTRED_EX)

    if len(playeritems) == 0:
        colorprint("You have no items.", Fore.LIGHTGREEN_EX)
    else:
        pi = "Your items: "

        ia = []
        na = []
        for item in playeritems:
            if item in ia:
                na[ia.index(item)] += 1
            else:
                ia.append(item)
                na.append(1)
        for i in range(len(ia)):
            pi += ia[i] + (f" x {na[i]}" if na[i] > 1 else "") + ", "
        colorprint(pi[:-2], Fore.LIGHTGREEN_EX)

    if len(enemyitems) == 0:
        colorprint("The enemy has no items.", Fore.LIGHTRED_EX)
    else:
        ei = "Enemy items: "

        ia = []
        na = []
        for item in enemyitems:
            if item in ia:
                na[ia.index(item)] += 1
            else:
                ia.append(item)
                na.append(1)
        for i in range(len(ia)):
            ei += ia[i] + (f" x {na[i]}" if na[i] > 1 else "") + ", "
        colorprint(ei[:-2], Fore.LIGHTRED_EX)

def potion(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    if player:
        if playerHealth < MAX_HEALTH:
            playerHealth += 1
            print("You drink the healing potion and regain vigor.")
            playeritems.remove("potion")
        else:
            print("You are already at full health.")
    else:
        if enemyHealth < MAX_HEALTH:
            enemyHealth += 1
            print("Seth downs the healing potion and regains vigor.")
            enemyitems.remove("potion")
        else:
            print("Seth is already at full health.")
def poison_dart(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    if player:
        enemyHealth -= 1
        print("You blow a poison dart at Seth, it injects its venom.")
        playeritems.remove("poison dart")
    else:
        playerHealth -= 1
        print("Seth throws a poison dart at you, you are hurt.")
        enemyitems.remove("poison dart")
def fairy_dust(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    global bullets

    if player:
        print("You summon a fairy.")
        time.sleep(1)
        print("The fairy sneaks a look at the next bullet.")
        print("*the next bullet is... " + ("live." if bullets[0] else "a blank.") + "*")
        playeritems.remove("fairy dust")
    else:
        print("Seth summons a fairy.")
        enemyitems.remove("fairy dust")
        enemyMemory[0] = bullets[0]
def crystal_ball(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    global bullets

    if player:
        print("You look into the crystal ball.")
        time.sleep(1)
        n = random.randint(0, len(bullets) - 1)
        print("Bullet number " + str(n + 1) + " will be... " + ("live." if bullets[n] else "a blank."))
        playeritems.remove("crystal ball")
    else:
        print("Seth looks into the crystal ball.")
        enemyitems.remove("crystal ball")
        n = random.randint(0, len(bullets) - 1)
        enemyMemory[n] = bullets[n]
def cursed_spell(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    if player:
        print("You open the cursed tome.")
        print("Mmm...")
        time.sleep(1)
        print("You send curses after Seth, some of them affect you.")
        playerHealth -= 1
        enemyHealth -= 2
        playeritems.remove("cursed spell")
    else:
        print("Seth uses the cursed spell.")
        print("Mmm...")
        time.sleep(1)
        print("The curses catch you and the Seth.")
        playerHealth -= 2
        enemyHealth -= 1
        enemyitems.remove("cursed spell")
def suspicious_buff(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    if player:
        print("You take the suspicious buff.")
        time.sleep(1)
        if random.random() < 0.6:
            print("It was a healing buff. You regain 1 health.")
            playerHealth += 1
        else:
            print("It was a poison buff. You lose 1 health.")
            playerHealth -= 1
        playeritems.remove("suspicious buff")
    else:
        print("Seth takes the suspicious buff.")
        time.sleep(1)
        if random.random() < 0.6:
            print("It was a healing buff. The enemy regains 1 health.")
            enemyHealth += 1
        else:
            print("It was a poison buff. The enemy loses 1 health.")
            enemyHealth -= 1
        enemyitems.remove("suspicious buff")
def cool_ball(player):
    if player:
        print("You play with the cool ball.")
        playeritems.remove("cool ball")
    else:
        print("Seth plays with the cool ball.")
        enemyitems.remove("cool ball")
def goblins_hand(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    if player:
        print("You summon a goblin's hand.")
        time.sleep(1)
        print("The goblin's hand steals an item from Seth.")
        if len(enemyitems) > 0:
            item = random.choice(enemyitems)
            enemyitems.remove(item)
            playeritems.append(item)
            print("The goblin's hand brings you a " + item + ".")
            playeritems.remove("goblins hand")
        else:
            print("The goblin's hand cannot grip anything")
    else:
        print("Seth summons a goblin's hand.")
        time.sleep(1)
        print("The goblin's hand steals an item from you.")
        if len(playeritems) > 0:
            item = random.choice(playeritems)
            playeritems.remove(item)
            enemyitems.append(item)
            print("The goblin's hand brings Seth a " + item + ".")
            enemyitems.remove("goblins hand")
        else:
            print("The goblin's hand returns empty-handed.")
def hell_shard(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    global revolverSharded

    if revolverSharded:
        print("The revolver is already primed with a hell shard.")
    else:
        if player:
            print("You prime the revolver with the hell shard.")
            playeritems.remove("hell shard")
        else:
            print("Seth primes the revolver with the hell shard.")
            enemyitems.remove("hell shard")
        revolverSharded = True
def chaos_orb(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    global bullets

    if player:
        print("You use the chaos orb, summoning the God of Chaos.")
        playeritems.remove("chaos orb")
    else:
        print("Seth uses the chaos orb, summoning the God of Chaos.")
        enemyitems.remove("chaos orb")

    time.sleep(1)
    random.shuffle(bullets)
    global enemyMemory; enemyMemory = [None] * len(bullets)

    print("The God of Chaos shuffles the bullets.")
def heavens_horn(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    global summonAngels

    if player:
        print("You blow the Heaven's Horn.")
        playeritems.remove("heavens horn")
    else:
        print("Seth blows the Heaven's Horn.")
        enemyitems.remove("heavens horn")
    time.sleep(1)
    print("Heaven has summoned the angels.")
    play_sound("horn")
    summonAngels = True
def morph_key(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    if player:
        print("You use the morph key.")
        playeritems.remove("morph key")
    else:
        print("Seth uses the morph key.")
        enemyitems.remove("morph key")
    time.sleep(1)

    print("The God of Fate morphs all the items.")

    playeritems = random.choices(list(items.keys()), k=len(playeritems))
    enemyitems = random.choices(list(items.keys()), k=len(enemyitems))
def spirit_swap(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    global playerTurn

    if player:
        print("You use the spirit swap.")
        playeritems.remove("spirit swap")
    else:
        print("Seth uses the spirit swap.")
        enemyitems.remove("spirit swap")
    time.sleep(1)

    playeritems, enemyitems = enemyitems, playeritems

    print("The God of Fate swaps your items.")
def cursed_twine(player):
    global playerHealth
    global enemyHealth
    global playeritems
    global enemyitems

    global playercannotitem
    global enemycannotitem

    if player:
        print("You use the cursed twine.")
        playeritems.remove("cursed twine")
        time.sleep(1)
        print("The twine wraps around Seth, binding him.")
        enemycannotitem = True
    else:
        print("Seth uses the cursed twine.")
        enemyitems.remove("cursed twine")
        time.sleep(1)
        print("The twine wraps around you, binding you.")
        playercannotitem = True


items = {
    "potion": potion,
    "poison dart": poison_dart,
    "fairy dust": fairy_dust,
    "crystal ball": crystal_ball,
    "cursed spell": cursed_spell,
    "suspicious buff": suspicious_buff,
    "cool ball": cool_ball,
    "goblins hand": goblins_hand,
    "hell shard": hell_shard,
    "chaos orb": chaos_orb,
    "heavens horn": heavens_horn,
    "morph key": morph_key,
    "spirit swap": spirit_swap,
    "cursed twine": cursed_twine
}
itemdescriptions = {
    "potion": "Heals 1 health.",
    "poison dart": "Deals 1 damage.",
    "fairy dust": "Reveals the next bullet.",
    "crystal ball": "Reveals a random bullet.",
    "cursed spell": "Deals 2 damage to opponent and 1 damage to caster.",
    "suspicious buff": "Heals or deals 1 damage.",
    "cool ball": "Does nothing.",
    "goblins hand": "Steals an item from opponent.",
    "hell shard": "Amplifies the next shot.",
    "chaos orb": "Shuffles the bullets.",
    "heavens horn": "Calls the angels.",
    "morph key": "Morphs all items.",
    "spirit swap": "Swaps items with opponent.",
    "cursed twine": "Prevents opponent from using items."
}

playerTurn = random.choice([True, False])
lastturnskip = False
turn = -1
summonAngels = False
lastsummon = None

#play_sound("backgroundmusic") #stops everything from occuring until the sound is done playing
if True:
    print("You have finally found it, the cursed blade,")
    print("The last artifact for Seth's parade.")
    input("...")
    print('"The Order of the Black Sun will rise,"')
    print("Echoing through the cavernous skies.")
    input("...")
    print("You return to the cult's dark keep,")
    print("The blade in hand, secrets to reap.")
    input("...")
    print("The cultists chant in rhythmic trance,")
    print("Their voices rise, they start to dance.")
    input("...")
    print("You place the blade upon the crest,")
    print("The final piece, it joins the rest.")
    input("...")
    print("The ground splits open, the demon's here,")
    print("Seth emerges, casting fear.")
    input("...")
    print("You lunge to grab the cursed knife,")
    print("To keep it from his grasp, your life.")
    input("...")
    print("Seth roars with rage, the cultists flee,")
    print("The blade, his weakness, he now sees.")
    input("...")
    print("In desperation, Seth's spell is cast,")
    print("Calling to Fate, both fierce and vast.")
    input("...")
    print("The God of Fate, of light and might,")
    print("Appears to judge this final fight.")
    input("...")
    print("Fate takes you both to realms untold,")
    print("A place where time and space unfold.")
    input("...")
    print("The cursed blade now shifts its form,")
    print("A revolver, to weather the storm.")
    input("...")
    print("Fate runs the game, the world to decide,")
    print("In this final duel, there's nowhere to hide.")


while True:
    if playerHealth <= 0:
        # Seth's Victory Ending
        print("With a sinister grin, Seth takes his aim,")
        print("His dark magic fueling this deadly game.")
        input("...")
        print("The revolver's barrel points to you,")
        print("Your fate now sealed, in this final view.")
        input("...")
        print("He pulls the trigger, the chamber spins,")
        print("A shot rings out, the demon wins.")
        input("...")
        print("You stagger back, your strength departs,")
        print("The cursed blade's magic tears you apart.")
        input("...")
        print("Seth's roar of triumph fills the night,")
        print("His power unleashed, an endless blight.")
        input("...")
        print("The God of Fate, with a sorrowful nod, departs,")
        print("The world now doomed, by Seth's dark arts.")
        input("...")
        print("The cultists fear, their master supreme,")
        print("The world succumbs to Seth's dark dream.")
        input("...")
        print("With the cursed blade now in his hand,")
        print("Seth's reign of terror grips the land.")
        input("...")
        print("The world is lost, the light undone,")
        print("All bow before the demon's son.")
        break
    if enemyHealth <= 0:
        # Protagonist's Victory Ending
        print("With steely resolve, you take your aim,")
        print("Determined to end this deadly game.")
        input("...")
        print("The revolver's barrel points straight and true,")
        print("In this moment, it's all up to you.")
        input("...")
        print("You pull the trigger, the chamber spins,")
        print("A shot rings out, the hero wins.")
        input("...")
        print("Seth staggers back, his power fades,")
        print("The cursed blade's magic invades.")
        input("...")
        print("The demon lord's roar, a final cry,")
        print("As he is banished, back to the sky.")
        input("...")
        print("The God of Fate, with a nod, departs,")
        print("The world now safe, thanks to your heart.")
        input("...")
        print("You return to the cult's forsaken keep,")
        print("The cultists gone, their secrets deep.")
        input("...")
        print("With the cursed blade now purified,")
        print("You leave the shadows, to the light outside.")
        input("...")
        print("The world is safe, the dark undone,")
        print("Thanks to the hero, the chosen one.")
        break

    load = False
    turn += 1
    if bullets == []:
        bullets = random.choices([True, False], k=random.randint(1, 8))
        print("")
        print(f"Fate's ancient clock strikes {str(turn)}...")
        time.sleep(1)
        print("Fate's will loads the revolver...")
        time.sleep(1.5)
        print(f"The chamber is filled with {bullets.count(True)} bullets and {bullets.count(False)} blanks.")
        enemybullets = bullets.count(True)
        enemyblanks = bullets.count(False)
        time.sleep(1)
        load = True
    
    if load or summonAngels:
        print("The spirit angels come bearing gifts.")
        play_sound("angelic")
        time.sleep(1)
        t = "You are given a "
        for x in range(2):
            item = random.choice(list(items.keys()))
            t += item
            if x == 0:
                t += " and a "
            else:
                t += "."
            playeritems.append(item)
        print(t)
        time.sleep(1)

        t = "Seth is given a "
        for x in range(2):
            item = random.choice(list(items.keys()))
            t += item
            if x == 0:
                t += " and a "
            else:
                t += "."
            enemyitems.append(item)
        print(t)
        if summonAngels:
            lastsummon = turn
            summonAngels = False
    
    print("")
    print("")

    if playerTurn:
        colorprint("It is your turn.", Fore.GREEN)

        if playercannotitem:
            if random.random() > 0.6:
                print("The cursed twine loosens its grip.")
                playercannotitem = False

        if playercannotitem:
            print("You are bound by the cursed twine and cannot use items.")

        time.sleep(1)
        display_stats()
        while True:
            time.sleep(0.5)
            print("Would you like to shoot, skip, use item or read description? (shoot/skip/<item>/info <item>)")
            if lastturnskip:
                print("Seth skipped his turn. Fate makes you shoot.")
                action = input()
                while action != "shoot":
                    print("Invalid action.")
                    action = input()

                print("Chk-chk...")
                play_sound("reload")
                time.sleep(1) 
                if bullets.pop(0):
                    print("POW - The cursed bullet hits Seth in the chest as he roars in pain.")
                    play_sound("gunshot")
                    if revolverSharded:
                        print("The hell shard amplifies the shot.")
                        enemyHealth -= 1
                        revolverSharded = False
                    enemyHealth -= 1
                    enemybullets -= 1
                else:
                    print("Pft - The empty shell falls in your lap.")
                    play_sound("blank")
                    enemyblanks -= 1
                lastturnskip = False
                break

            action = input()
            if action == "shoot":
                print("Chk-chk...")
                play_sound("reload")
                time.sleep(1)
                if bullets.pop(0):
                    print("POW - The cursed bullet hits Seth in the chest as he roars in pain.")
                    play_sound("gunshot")
                    if revolverSharded:
                        print("The hell shard amplifies the shot.")
                        enemyHealth -= 1
                        revolverSharded = False
                    enemybullets -= 1
                    enemyHealth -= 1
                else:
                    print("Pft - The empty shell falls in your lap.")
                    play_sound("blank")
                    enemyblanks -= 1
                break
            elif action == "skip":
                print("You drop the revolver.")
                play_sound("gundrop")
                lastturnskip = True
                break
            elif action in playeritems:
                if playercannotitem:
                    print("You are bound by the cursed twine and cannot use items.")
                    continue

                time.sleep(0.5)
                items[action](True)
                time.sleep(1)
                display_stats()
            elif action.startswith("info "):
                item = action[5:]
                if item in items:
                    colorprint(f"{item}:" + itemdescriptions[item], Fore.MAGENTA)
                else:
                    print("Invalid item.")
            else:
                print("Invalid action.")
        playerTurn = False
    else:
        time.sleep(0.5)
        colorprint("It is the Seth's turn.", Fore.RED)
        play_sound("growl")

        if enemycannotitem:
            if random.random() > 0.6:
                print("Seth's cursed twine loosens its grip.")
                enemycannotitem = False

        if enemycannotitem:
            print("Seth is bound by the cursed twine and cannot use items.")

        time.sleep(1)
        display_stats()
        while True:
            print("Seth ponders...")
            time.sleep(1)
            
            action = None

            def get_inventory_quality(items):
                qualities = {
                    "potion": 1,
                    "poison dart": 1,
                    "fairy dust": 2,
                    "crystal ball": 1,
                    "cursed spell": 1,
                    "suspicious buff": 1,
                    "cool ball": 0,
                    "goblins hand": 2,
                    "hell shard": 2,
                    "chaos orb": 1,
                    "heavens horn": 1,
                    "morph key": 1,
                    "spirit swap": 2,
                    "cursed twine": 3
                }
                return sum([qualities[item] for item in items])
            def ai_logic():
                if len(enemyMemory) < enemybullets + enemyblanks:
                    for x in range(enemybullets + enemyblanks - len(enemyMemory)):
                        enemyMemory.append(None)
                if len(enemyMemory) > enemybullets + enemyblanks:
                    for x in range(len(enemyMemory) - enemybullets - enemyblanks):
                        enemyMemory.pop(0)

                #possible_actions = ["shoot", "skip", *enemyitems]
                #items: potion, poison dart, fairy dust, crystal ball, cursed spell, suspicious buff, cool ball, goblins hand, hell shard, chaos orb, heavens horn, morph key, spirit swap, cursed twine
                if "potion" in enemyitems and enemyHealth < MAX_HEALTH:
                    return "potion"
                if "poison dart" in enemyitems:
                    return "poison dart"
                if "fairy dust" in enemyitems:
                    if enemyMemory[0] == None:
                        return "fairy dust"
                if "crystal ball" in enemyitems:
                    return "crystal ball"
                if "cursed spell" in enemyitems:
                    if enemyHealth > 2 and enemyHealth > playerHealth:
                        return "cursed spell"
                if "suspicious buff" in enemyitems:
                    if enemyHealth > 1:
                        return "suspicious buff"
                if "goblins hand" in enemyitems and len(playeritems) > 0:
                    return "goblins hand"
                if "hell shard" in enemyitems:
                    if enemyMemory[0] or enemybullets > enemyblanks:
                        return "hell shard"
                if "chaos orb" in enemyitems:
                    if enemyMemory.count(None) == len(enemyMemory):
                        return "chaos orb"
                if "heavens horn" in enemyitems:
                    if len(playeritems) > len(enemyitems) or len(enemyitems) == 0:
                        return "heavens horn"
                if "morph key" in enemyitems:
                    if get_inventory_quality(playeritems) > get_inventory_quality(enemyitems):
                        return "morph key"
                if "spirit swap" in enemyitems:
                    if len(playeritems) > len(enemyitems):
                        return "spirit swap"
                if "cursed twine" in enemyitems:
                    if not playercannotitem and len(playeritems) > 0:
                        return "cursed twine"
                
                if enemyMemory[0] == True:
                    return "shoot"
                elif enemyMemory[0] == False:
                    return "skip"
                else:
                    if enemybullets >= enemyblanks:
                        return "shoot"
                    else:
                        return "skip"
                
            
            if lastturnskip:
                print("Fate makes Seth shoot.")
                action = "shoot"
            else:
                if enemycannotitem:
                    action = "shoot" if enemybullets >= enemyblanks else "skip"
                else:
                    action = ai_logic()

            if action == "shoot":
                print("Chk-chk...")
                play_sound("reload")
                time.sleep(1)
                if bullets.pop(0):
                    print("POW - Seth aims at you and fires a dark bullet straight at your heart. You feel pain.")
                    play_sound("gunshot")
                    if revolverSharded:
                        print("The hell shard amplifies the shot.")
                        playerHealth -= 1
                        revolverSharded = False
                    playerHealth -= 1
                    enemybullets -= 1
                else:
                    print("Pft - A blank falls out of the chamber.")
                    play_sound("blank")
                    enemyblanks -= 1
                lastturnskip = False
                break
            elif action == "skip":
                print("Seth laughs and tosses you the revolver.")
                play_sound("gundrop")
                lastturnskip = True
                break
            else:
                if enemycannotitem:
                    time.sleep(0.1)
                    continue

                items[action](False)

        playerTurn = True
