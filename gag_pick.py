from enum import Enum
from math import ceil

cogs_hp = [  6,  12,  20,  30,  42,  56,  72,  90, 110, 132,
           156, 196, 224, 254, 286, 320, 356, 394, 434, 476, float("inf")]
combinations = {i : [] for i in range(1, 21)}

# print(combinations)
def get_max_level(damage):
    global cogs_hp
    if damage < 6:
        return -1
    for lvl in range(1, 21):
        if damage >= cogs_hp[lvl-1] and damage < cogs_hp[lvl]:
            # return lvl
            if damage < cogs_hp[lvl-1]*1.15:
                return lvl
            else:
                return -1

class GagTrack(Enum):
    TRAP = "Trap"
    LURE = "Lure"
    SOUND = "Sound"
    THROW = "Throw"
    SQUIRT = "Squirt"
    DROP = "Drop"

simple_gags = [
        # (GagTrack.TRAP, "Banana Peel", 12),
        # (GagTrack.TRAP, "Rake", 20),
        # (GagTrack.TRAP, "Marbles", 35),
        # (GagTrack.TRAP, "Quicksand", 50),
        (GagTrack.TRAP, "Trapdoor", 85),
        (GagTrack.TRAP, "TNT", 180),
        (GagTrack.TRAP, "Railroad", 200),
        (GagTrack.LURE, "Lure", 0),
        # (GagTrack.SOUND, "Bike Horn", 4),
        # (GagTrack.SOUND, "Whistle", 7),
        # (GagTrack.SOUND, "Bugle", 11),
        (GagTrack.SOUND, "Aoogah", 16),
        (GagTrack.SOUND, "Elephant Trunk", 21),
        (GagTrack.SOUND, "Foghorn", 50),
        (GagTrack.SOUND, "Opera Singer", 90),
        # (GagTrack.THROW, "Cupcake", 6),
        # (GagTrack.THROW, "Fruit Pie Slice", 10),
        # (GagTrack.THROW, "Cream Pie Slice", 17),
        (GagTrack.THROW, "Whole Fruit Pie", 27),
        (GagTrack.THROW, "Whole Cream Pie", 40),
        (GagTrack.THROW, "Birthday Cake", 100),
        (GagTrack.THROW, "Wedding Cake", 120),
        # (GagTrack.SQUIRT, "Squirting Flower", 4),
        # (GagTrack.SQUIRT, "Glass of Water", 8),
        # (GagTrack.SQUIRT, "Squirt Gun", 12),
        (GagTrack.SQUIRT, "Seltzer Bottle", 21),
        (GagTrack.SQUIRT, "Fire Hose", 30),
        (GagTrack.SQUIRT, "Storm Cloud", 80),
        (GagTrack.SQUIRT, "Geyser", 105),
        # (GagTrack.DROP, "Flower Pot", 10),
        # (GagTrack.DROP, "Sandbag", 18),
        # (GagTrack.DROP, "Anvil", 30),
        # (GagTrack.DROP, "Big Weight", 45),
        (GagTrack.DROP, "Safe", 70),
        (GagTrack.DROP, "Grand Piano", 170),
        (GagTrack.DROP, "Toontanic", 180),
        ]

gags = []

for gag in simple_gags:
    type, name, damage = gag

    gags.append(gag)
    if type != GagTrack.LURE:
        gags.append((type, "Organic " + name, damage + max(1, damage//10)))

# for gag in gags:
#     print(gag)

def simulate_attack(gags_chosen, start_lured=False):
    damage = 0
    trap = None
    lured = start_lured

    gags_used = [i for i in gags_chosen if not i is None ]

    idx = 0
    while idx < len(gags_used):
        gag = gags_used[idx]

        if gag[0] == GagTrack.TRAP:
            trap = gag
        elif gag[0] == GagTrack.LURE:
            if trap:
                damage += trap[2]
                trap = None
                # lured = False
            else:
                lured = True
        else:
            curr_gag_track = gag[0]
            last = idx
            while last+1 < len(gags_used) and gags_used[last+1][0] == curr_gag_track:
                last += 1
            gag_damage = sum([g[2] for g in gags_used[idx:last+1]])

            # apply lure
            knockback = 0
            if lured:
                if curr_gag_track == GagTrack.SOUND:
                    lured = False
                elif curr_gag_track == GagTrack.DROP:
                    gag_damage = 0
                else:
                    knockback = ceil(gag_damage/2)
                    lured = False


            # apply group bonus
            group = 0
            if last > idx:
                group = ceil(gag_damage/5)

            damage += gag_damage + knockback + group

            idx = last

        idx += 1
    return damage

round = [None, None, None, None]

def format_round(round, damage):
    # print(round)
    names = [g[1] for g in round]

    r = ' + '.join(names)
    return (f"{r} for {damage} damage\n" )

lure_index = min([i for i in range(len(gags)) if gags[i][0] == GagTrack.LURE])
sound_index = min([i for i in range(len(gags)) if gags[i][0] == GagTrack.SOUND])
throw_index = min([i for i in range(len(gags)) if gags[i][0] == GagTrack.THROW])

print(lure_index)
print(sound_index)
print(throw_index)
# with trap
gags = gags + [None]

for trap in gags[:lure_index]:
    round[0] = trap
    round[1] = gags[lure_index]
    for idx, third in enumerate(gags[sound_index:]):
        round[2] = third
        for fourth in gags[sound_index+idx:]:
            round[3] = fourth
            damage = simulate_attack(round)
            lvl = get_max_level(damage)
            if lvl > 0:
                combinations[lvl].append((tuple([r for r in round if r is not None]), damage))

# lure
round[0] = gags[lure_index]
for idx2, second in enumerate(gags[throw_index:]): #ignoring sound
    round[1] = second
    for idx3, third in enumerate(gags[throw_index+idx2:]):
        round[2] = third
        for fourth in gags[throw_index+idx2+idx3:]:
            round[3] = fourth
            damage = simulate_attack(round)
            # print(round)
            lvl = get_max_level(damage)
            if lvl > 0:
                combinations[lvl].append((tuple([r for r in round if r is not None]), damage))

# no lure, not lured
for idx1, first in enumerate(gags[sound_index:]):
    round[0] = first
    for idx2, second in enumerate(gags[sound_index+idx1:]):
        round[1] = second
        for idx3, third in enumerate(gags[sound_index+idx1+idx2:]):
            round[2] = third
            for fourth in gags[sound_index+idx1+idx2+idx3:]:
                round[3] = fourth
                damage = simulate_attack(round)
                lvl = get_max_level(damage)
                if lvl > 0:
                    combinations[lvl].append((tuple([r for r in round if r is not None]), damage))

# no lure, lured
for idx1, first in enumerate(gags[throw_index:]):
    round[0] = first
    for idx2, second in enumerate(gags[throw_index+idx1:]):
        round[1] = second
        for idx3, third in enumerate(gags[throw_index+idx1+idx2:]):
            round[2] = third
            for fourth in gags[throw_index+idx1+idx2+idx3:]:
                round[3] = fourth
                damage = simulate_attack(round, True)
                lvl = get_max_level(damage)
                if lvl > 0:
                    combinations[lvl].append((tuple([(GagTrack.LURE, "(Lured)", 0)] + [r for r in round if r is not None]), damage))


# for r in combinations[3]:
    # format_round(r[0], r[1])


for i in range(1, 21):
    combinations[i].sort(key=lambda x: x[1])


# with open("test_common_gags", 'w') as f:
#     i = 8
#     for r in combinations[i]:
#         f.write(format_round(r[0], r[1]))
for i in range(1, 21):
    if i < 10:
        r = f'level0{i}.txt'
    else:
        r = f'level{i}.txt'
    with open(r, 'w') as f:
        for r in combinations[i]:
            f.write(format_round(r[0], r[1]))
