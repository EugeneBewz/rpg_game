"""
Коли вони приходять

Надворі вересень. У місто Умань для святкування свого свята,
Рош-га-Шана, з усього світу приїжджають паломники — ортодоксальні
євреї, або хасиди. Утім, для місцевих це означає лише дві речі:
долари та підвищений рівень складності цієї гри.
Ви — уманець, якого послали відвідати паломницький район на вулиці Туристів, щоб
купити там сувенір і повернутися. Однак паломників багато, і крім них у тому районі мешкає
ще й інша фауна — блатні.
Ваша ціль — подолати три райони ("Уманчанка", Центр, вулиця Туристів), придбати сувенір
та повернутися з ним. Гра завершиться, якщо ви залишитесь без грошей або повернетеся
без сувеніра.

Євгеній Бевз, ПКН-1
"""

import game_tools

# * Preparations =======================================================================================================
# ! Items ========================================================
wallet = game_tools.Item("wallet", "A wallet lying on pavement with a bunch of money", 3)
shock = game_tools.Item("Electroshock", "A powerful tool against powerful enemies", 5)
laws = game_tools.Item("Laws", "Sometimes they're effective, sometimes they're not", 3)

souvenir = game_tools.Item("Souvenir", "Your mother asked to buy it, so you have no choice but to obey")

# ! NPCs =========================================================
# ? Hostile mobs =================================================
khasid = game_tools.Hostile("Abraham",
                            "One of the many, who came to Uman. Thinks he can do everything here")
gopnik = game_tools.Hostile("Kosyi",
                            "His only friend is brute force", 4)
angry_cop = game_tools.Hostile("Cln.Petrenko",
                               "Ha had a salary cut: now he catches everyone he can see", 5)


khasid.set_dialogue("Shalom! Would you like to trade?")
khasid.set_weakness("wallet")
khasid.set_resistance("laws")

gopnik.set_dialogue("Hey, you dumb! It's my district!")
gopnik.set_weakness("shock")
gopnik.set_resistance("wallet")

angry_cop.set_dialogue("Well-well-well, I see someone who seeks troubles.")
angry_cop.set_weakness("shock")
angry_cop.set_resistance("laws")
# ? Allies =======================================================
merchant = game_tools.Friendly("Ivan Klymko",
                               "A toy merchants, who managed to keep his shop safe from jewish pilgrims")
child = game_tools.Friendly("Myshko",
                            "Just a child with something in his hand")

buddy = game_tools.Friendly("Buddy",
                            "Your buddy from middle school, always was a man of force")

merchant.set_buff("heal")
merchant.set_dialogue("Hey! What a nice boy! Would you like taking a look at my store?")

child.set_buff("gift")
child.set_dialogue("If you ask, where did I get this, I just found it.")
child.set_npc_equipment(shock)

buddy.set_buff("weaken enemies")
buddy.set_dialogue("Yo, man! I missed you! Anyone dared to bother you?")

bargainer = game_tools.Bargainer("Moses", "A bargainer, who sells everything he can")
bargainer.set_dialogue("Hey! You want to trade? My prices are the best among everyone")

# ! Districts ===================================================
umanchanka = game_tools.District('"Umanchanka"')
centre = game_tools.District('City centre')
tourists_street = game_tools.District('Tourists street')
old_uman = game_tools.District("Old Uman")

# ! Districts description ========================================
umanchanka.set_description("This is where you live. This place is quite peaceful.")
centre.set_description("Always quiet, yet always busy. You never know who you might run across.")
tourists_street.set_description("This stree is always overcrowded in September because of the Jewish New Year.")
old_uman.set_description("A beautiful historical part of Uman, perhaps sometimes you can meet unpleasant people.")

# ! Building roads ==============================================
umanchanka.build_road_between_districts(centre, "west")
centre.build_road_between_districts(umanchanka, "east")

centre.build_road_between_districts(tourists_street, "south")
tourists_street.build_road_between_districts(centre, "north")

tourists_street.build_road_between_districts(old_uman, "west")
old_uman.build_road_between_districts(tourists_street, "east")

old_uman.build_road_between_districts(umanchanka, "north")
umanchanka.build_road_between_districts(old_uman, "south")

# ! Filling districts ============================================
umanchanka.set_local_friendly_npc(child)
umanchanka.set_local_item(wallet)

centre.set_local_hostile_npc(gopnik)
centre.set_local_item(laws)

tourists_street.set_local_hostile_npc(khasid)
tourists_street.set_local_friendly_npc(bargainer)

#  * Main cycle ========================================================================================================
# mc_lives = 3
mc_backpack = []
mc_renown = 0

current_district = umanchanka

alive = True
while alive:

    print("\n")
    current_district.get_district_info()

    hostile_npc_here = current_district.get_local_hostile_npc()
    friendly_npc_here = current_district.get_local_friendly_npc()

    command = input(">>> ")
    # Move between locations
    if command in ["north", "south", "west", "east"]:
        current_district = current_district.travel(command)
        current_district.visit_district()
        if current_district == tourists_street:
            print(f"Your goal is here: a bargainer offers souvenirs for everyone")
        elif all([
            (current_district == umanchanka) and (current_district.visits > 1) and (souvenir not in mc_backpack)
        ]):
            print("You came back without a souvenir. You made your mother sad. Pathetic!")
            alive = False
        elif all([
            (current_district == umanchanka) and (current_district.visits > 1) and (souvenir in mc_backpack)
        ]):
            print("What a good boy! You did as your mother said. Congratulations. $5 are all yours")
            alive = False
    # Try to talk with NPC
    elif command == "talk":

        print("Who do you want to talk to?")
        speak_with = input(">>> ")
        if hostile_npc_here:
            if speak_with == hostile_npc_here.npc_name:
                hostile_npc_here.talk()
        if friendly_npc_here:
            if speak_with == bargainer.npc_name:
                bargainer.talk()
                response_for_trade = input("(y/n) >>> ")
                if response_for_trade == 'y':
                    if bargainer.bargain(mc_renown) == 0:
                        print("I will give a souvenir for 3 items. Agree?")
                        offer_response = input("(y/n) >>> ")
                        if offer_response == 'y':
                            if len(mc_backpack) == 3:
                                mc_backpack.pop()
                                mc_backpack.pop()
                                mc_backpack.pop()
                                mc_backpack.append(souvenir)
                            else:
                                print("Sorry, but not enough...")
                        else:
                            print("Then next time")
                    elif bargainer.bargain(mc_renown) == 1:
                        print("I will give a souvenir for 2 items. Agree?")
                        offer_response = input("(y/n) >>> ")
                        if offer_response == 'y':
                            if len(mc_backpack) >= 2:
                                mc_backpack.pop()
                                mc_backpack.pop()
                                mc_backpack.append(souvenir)
                            else:
                                print("Sorry, but not enough...")
                        else:
                            print("Then next time")
                    elif bargainer.bargain(mc_renown) == 2:
                        print("I will give a souvenir for 1 items. Agree?")
                        offer_response = input("(y/n) >>> ")
                        if offer_response == 'y':
                            if len(mc_backpack) >= 1:
                                mc_backpack.pop()
                                mc_backpack.append(souvenir)
                            else:
                                print("Sorry, but not enough...")
                        else:
                            print("Then next time")
                    elif bargainer.bargain(mc_renown) == 3:
                        print("Take this souvenir, but don't beat me!")
                        mc_backpack.append(souvenir)
                elif response_for_trade == 'n':
                    print("Then see you later")
            else:
                if speak_with == friendly_npc_here.npc_name:
                    friendly_npc_here.talk()
                    if friendly_npc_here.give_buff() == 0:
                        print("They can give no buff...")
                    elif friendly_npc_here.give_buff() == 1:
                        print(f"You received an item - [{friendly_npc_here.npc_equipment.item_name}]")
                        mc_backpack.append(friendly_npc_here.npc_equipment)
                        friendly_npc_here.set_npc_equipment(None)
    # Try to fight with NPC
    elif command == "fight":
        if hostile_npc_here or friendly_npc_here:
            print("Who do you want to fight with? If you changed your mind, type No one")
            fight_with = input(">>> ")
            # If you fight a mob, get renown for each victory
            if hostile_npc_here:
                if fight_with == hostile_npc_here.npc_name:
                    fighting_tool = input(f"""What is your weapon of mass destruction and enemy humiliation?
You possess: {[item.item_name for item in mc_backpack]} >>> """)
                    for tool in mc_backpack:
                        if tool.item_name == fighting_tool:
                            if hostile_npc_here.fight(tool):
                                print("You pass victorious")
                                current_district.set_local_hostile_npc(None)
                                mc_renown += 1
                            else:
                                print("YOU DIED")
                                alive = False
                    # print(f"There is no {fighting_tool} in your backpack")
            # If you fight an ally, you'll be punished for cruelty
            if friendly_npc_here:
                if fight_with == friendly_npc_here.npc_name:
                    print(
                        "Why? Are you trying to prove yourself by fighting weak and helpless? You're too cruel to live!"
                    )
                    alive = False
            elif fight_with == 'No one':
                print("One more day without violence. What a pleasure!")
            else:
                print("Are you nuts? There is no such person here")
    elif command == "take":
        if current_district.local_item:
            mc_backpack.append(current_district.local_item)
            current_district.set_local_item(None)
