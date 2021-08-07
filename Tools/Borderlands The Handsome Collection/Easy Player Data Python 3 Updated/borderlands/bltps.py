#! /usr/bin/env python

import argparse
from .savefile import App, ChallengeCat, Challenge, Config, DictAction

class AppTPS(App):
    """
    Our main application class for Borderlands: The Pre-Sequel
    """

    # Game name
    game_name = 'Borderlands: The Pre-Sequel'

    # Item export/import prefix
    item_prefix = 'BLOZ'

    # Max char level
    max_level = 70

    # The only difference here is that BLTPS has "laser"
    black_market_keys = (
        'rifle', 'pistol', 'launcher', 'shotgun', 'smg',
        'sniper', 'grenade', 'backpack', 'bank', 'laser',
    )

    # Dict to tell us which black market keys are ammo-related, and
    # what the max ammo is at each level.  Could be computed pretty
    # easily, but we may as well just store it.
    black_market_ammo = {
        'rifle':    [280, 420, 560, 700, 840,  980,  1120, 1260],
        'pistol':   [200, 300, 400, 500, 600,  700,  800,  900],
        'launcher': [12,  15,  18,  21,  24,   27,   30,   33],
        'shotgun':  [80,  100, 120, 140, 160,  180,  200,  220],
        'smg':      [360, 540, 720, 900, 1080, 1260, 1440, 1620],
        'sniper':   [48,  60,  72,  84,  96,   108,  120,  132],
        'grenade':  [3,   4,   5,   6,   7,    8,    9,    10],
        'laser':    [500, 620, 740, 860, 980,  1100, 1220, 1340],
    }

    # B2 version is 7, TPS version is 10
    # "version" taken from what Gibbed calls it, not sure if that's
    # an appropriate descriptor or not.
    item_struct_version = 10

    # Available choices for --unlock option
    unlock_choices = ['tvhm', 'uvhm', 'challenges', 'ammo']

    # Challenge categories
    challenge_cat_gravity = ChallengeCat("Low Gravity")
    challenge_cat_grinder = ChallengeCat("Grinder")
    challenge_cat_enemies = ChallengeCat("Enemies")
    challenge_cat_elemental = ChallengeCat("Elemental")
    challenge_cat_loot = ChallengeCat("Loot")
    challenge_cat_money = ChallengeCat("Money and Trading")
    challenge_cat_vehicle = ChallengeCat("Vehicle")
    challenge_cat_health = ChallengeCat("Health and Recovery")
    challenge_cat_grenades = ChallengeCat("Grenades")
    challenge_cat_shields = ChallengeCat("Shields")
    challenge_cat_rockets = ChallengeCat("Rocket Launcher")
    challenge_cat_sniper = ChallengeCat("Sniper Rifle")
    challenge_cat_ar = ChallengeCat("Assault Rifle")
    challenge_cat_laser = ChallengeCat("Laser")
    challenge_cat_smg = ChallengeCat("SMG")
    challenge_cat_shotgun = ChallengeCat("Shotgun")
    challenge_cat_pistol = ChallengeCat("Pistol")
    challenge_cat_melee = ChallengeCat("Melee")
    challenge_cat_combat = ChallengeCat("General Combat")
    challenge_cat_misc = ChallengeCat("Miscellaneous")

    # There are two possible ways of uniquely identifying challenges in this file:
    # via their numeric position in the list, or by what looks like an internal
    # ID (though that ID is constructed a little weirdly, so I'm not sure if it's
    # actually intended to be used that way or not).
    #
    # I did run some tests, and it looks like internally, B2 probably does use
    # that ID field to identify the challenges...  You can mess around with the
    # order in which they're saved to the file, but so long as the ID field
    # is still pointing to the challenge you want, it'll be read in properly
    # (and then when you save your game, they'll be written back out in the
    # original order).
    #
    # Given that, I decided to go ahead and use that probably-ID field as the
    # index on this dict, rather than the order.  That should be slightly more
    # flexible for anyone editing the JSON directly, and theoretically
    # shouldn't be a problem in the future since there won't be any new major
    # DLC for B2...
    #
    # New major DLC for TPS seems unlikely too, though time will tell.
    challenges = {}

    # Low Gravity
    challenges[2052] = Challenge(468, 2052,
        "GD_Challenges.LowGravity.LowGravity_CriticalsWhileAirborne",
        challenge_cat_gravity,
        "Eagle Eye",
        "Get critical hits while airborne",
        (50, 250, 500, 1500, 3000))

    challenges[2093] = Challenge(507, 2093,
        "GD_Challenges.LowGravity.LowGravity_DoubleJump",
        challenge_cat_gravity,
        "Boosted",
        "Perform air boosts",
        (50, 250, 1000, 2500, 5000))

    challenges[2051] = Challenge(467, 2051,
        "GD_Challenges.LowGravity.LowGravity_KillsWhileAirborne",
        challenge_cat_gravity,
        "Death from Above",
        "Kill enemies while in the air",
        (50, 250, 1000, 2500, 5000),
        bonus=5)

    challenges[2055] = Challenge(471, 2055,
        "GD_Challenges.LowGravity.LowGravity_KillsWithSlam",
        challenge_cat_gravity,
        "Slampage!",
        "Kill enemies with slam attacks",
        (5, 10, 50, 100, 200))

    challenges[2053] = Challenge(469, 2053,
        "GD_Challenges.LowGravity.LowGravity_MeleeWhileAirborne",
        challenge_cat_gravity,
        "Dragon Punch",
        "Deal melee damage while airborne",
        (5000, 10000, 25000, 75000, 200000))

    challenges[2054] = Challenge(470, 2054,
        "GD_Challenges.LowGravity.LowGravity_SlamDamage",
        challenge_cat_gravity,
        "Roger Slamjet",
        "Desc",
        (2000, 10000, 50000, 100000, 2500000))

    # Grinder
    challenges[2060] = Challenge(476, 2060,
        "GD_Challenges.Grinder.Grinder_GrinderRecipes",
        challenge_cat_grinder,
        "Master Chef",
        "Discover Grinder recipes",
        (2, 5, 10, 20, 34),
        bonus=3)

    challenges[2061] = Challenge(477, 2061,
        "GD_Challenges.Grinder.Grinder_MoonstoneAttachments",
        challenge_cat_grinder,
        "Greater Than the Sum of its Parts",
        "Obtain Luneshine weapons from the Grinder",
        (20, 50, 75, 125, 200))

    challenges[2059] = Challenge(475, 2059,
        "GD_Challenges.Grinder.Grinder_MoonstoneGrind",
        challenge_cat_grinder,
        "This Time for Sure",
        "Perform Moonstone grinds",
        (10, 25, 150, 300, 750))

    challenges[2058] = Challenge(474, 2058,
        "GD_Challenges.Grinder.Grinder_StandardGrind",
        challenge_cat_grinder,
        "The Daily Grind",
        "Perform standard grind",
        (50, 250, 750, 1500, 25000))

    # Enemies
    challenges[2035] = Challenge(452, 2035,
        "GD_Challenges.Enemies.Enemies_KillDahlBadasses",
        challenge_cat_enemies,
        "Kiss My Badass",
        "Kill Lost Legion badasses",
        (5, 10, 20, 30, 50))

    challenges[2028] = Challenge(445, 2028,
        "GD_Challenges.Enemies.Enemies_KillDahlFlyers",
        challenge_cat_enemies,
        "Crash & Burn",
        "Destroy Lost Legion jet fighters",
        (1, 3, 5, 10, 20),
        bonus=3)

    challenges[2027] = Challenge(444, 2027,
        "GD_Challenges.Enemies.Enemies_KillDahlInfantry",
        challenge_cat_enemies,
        "Get Some!",
        "Kill Lost Legion infantry",
        (50, 250, 500, 1000, 2000))

    challenges[2029] = Challenge(446, 2029,
        "GD_Challenges.Enemies.Enemies_KillDahlSuits",
        challenge_cat_enemies,
        "No Suit for You!",
        "Kill Lost Legion powersuits",
        (10, 25, 75, 150, 300))

    challenges[2043] = Challenge(460, 2043,
        "GD_Challenges.Enemies.Enemies_KillGuardianBosses",
        challenge_cat_enemies,
        "More Where That Came From",
        "Kill Eridian Guardian bosses",
        (2, 4, 6, 8, 10),
        bonus=3)

    challenges[2031] = Challenge(448, 2031,
        "GD_Challenges.Enemies.Enemies_KillGuardians",
        challenge_cat_enemies,
        "Not So Tough Now",
        "Kill Eridian Guardians",
        (25, 50, 100, 150, 250))

    challenges[2030] = Challenge(447, 2030,
        "GD_Challenges.Enemies.Enemies_KillHyperionInfantry",
        challenge_cat_enemies,
        "Dose of Death",
        "Kill enemies infected with space hurps",
        (10, 50, 125, 250, 500))

    challenges[2034] = Challenge(451, 2034,
        "GD_Challenges.Enemies.Enemies_KillKraggonBadasses",
        challenge_cat_enemies,
        "Slayer of Titans",
        "Kill kraggon badasses",
        (1, 3, 7, 15, 25),
        bonus=3)

    challenges[2032] = Challenge(449, 2032,
        "GD_Challenges.Enemies.Enemies_KillKraggons",
        challenge_cat_enemies,
        "Big Game Hunt",
        "Kill kraggons",
        (25, 50, 150, 300, 750))

    challenges[2039] = Challenge(456, 2039,
        "GD_Challenges.Enemies.Enemies_KillLunarLooters",
        challenge_cat_enemies,
        "Gift That Keeps Giving",
        "Kill swagmen",
        (1, 3, 5, 8, 12))

    challenges[1989] = Challenge(406, 1989,
        "GD_Challenges.Enemies.Enemies_KillRathyds",
        challenge_cat_enemies,
        "Exterminator",
        "Kill rathyds",
        (25, 50, 150, 300, 750))

    challenges[2038] = Challenge(455, 2038,
        "GD_Challenges.Enemies.Enemies_KillScavBadasses",
        challenge_cat_enemies,
        "The One That Says B.A.M.F.",
        "Kill scav badasses",
        (10, 25, 50, 100, 250))

    challenges[2037] = Challenge(454, 2037,
        "GD_Challenges.Enemies.Enemies_KillScavFlyers",
        challenge_cat_enemies,
        "It Wasn't Yours, Anyway",
        "Destroy scav jet fighters",
        (1, 3, 5, 10, 20))

    challenges[2036] = Challenge(453, 2036,
        "GD_Challenges.Enemies.Enemies_KillScavSpacemen",
        challenge_cat_enemies,
        "Space Dead",
        "Kill scav outlaws",
        (25, 50, 150, 300, 750),
        bonus=3)

    challenges[2033] = Challenge(450, 2033,
        "GD_Challenges.Enemies.Enemies_KillScavs",
        challenge_cat_enemies,
        "Die, Moon Jerks",
        "Kill scavs",
        (75, 250, 750, 2000, 5000))

    challenges[1988] = Challenge(405, 1988,
        "GD_Challenges.Enemies.Enemies_KillShugguraths",
        challenge_cat_enemies,
        "That Was Unpleasant",
        "Kill shugguraths",
        (25, 50, 150, 300, 750))

    challenges[2041] = Challenge(458, 2041,
        "GD_Challenges.Enemies.Enemies_KillTorkBadasses",
        challenge_cat_enemies,
        "Torkin' Out the Trash",
        "Kill tork badasses",
        (5, 10, 20, 30, 50))

    challenges[1974] = Challenge(391, 1974,
        "GD_Challenges.Enemies.Enemies_KillTorks",
        challenge_cat_enemies,
        "Pest Control",
        "Kill torks",
        (25, 75, 150, 500, 1000))

    # This challenge ID is odd, since it identifies itself as a level-specific
    # challenge, but lives up in the "Enemies" section along with everything
    # else.  Unlocking this challenge prematurely will correctly show the
    # challenge in the Enemies section, but will also cause an "Eleseer" entry
    # to be added to the location-specific area, and a single (undiscovered)
    # entry will be there.  TODO: I have yet to verify that that doesn't
    # cause problems when you do first enter Eleseer.  I assume it should be
    # fine, though I should doublecheck.
    challenges[2257] = Challenge(671, 2257,
        "GD_Challenges.Co_LevelChallenges.InnerCore_AintNobodyGotTime",
        challenge_cat_enemies,
        "Aim for the Little Ones",
        "Kill Opha's spawned Putti",
        (10, 25, 45, 70, 100))

    challenges[1728] = Challenge(331, 1728,
        "GD_Marigold_Challenges.Enemies.Enemies_KillCorruptions",
        challenge_cat_enemies,
        "Clean Sweep",
        "Kill corrupted enemies inside of Claptrap",
        (10, 25, 75, 150, 300))

    challenges[1727] = Challenge(330, 1727,
        "GD_Marigold_Challenges.Enemies.Enemies_KillInsecuityForces",
        challenge_cat_enemies,
        "Claptomaniac",
        "Kill insecurity forces",
        (5, 10, 25, 75, 200),
        bonus=3)

    challenges[1733] = Challenge(336, 1733,
        "GD_Marigold_Challenges.Enemies.Enemies_KillsFromBitBombs",
        challenge_cat_enemies,
        "Volakillity",
        "Kill enemies with Volatile Bits",
        (3, 8, 20, 50, 120))

    # Elemental
    challenges[1823] = Challenge(226, 1823,
        "GD_Challenges.elemental.Elemental_SetEnemiesOnFire",
        challenge_cat_elemental,
        "Way of the Enkindling",
        "Light enemies on fire",
        (25, 100, 400, 1000, 2000))

    challenges[1592] = Challenge(40, 1592,
        "GD_Challenges.elemental.Elemental_KillEnemiesCorrosive",
        challenge_cat_elemental,
        "Toxic Takedown",
        "Kill enemies with corrosive damage",
        (20, 75, 250, 600, 1000))

    challenges[1595] = Challenge(43, 1595,
        "GD_Challenges.elemental.Elemental_KillEnemiesExplosive",
        challenge_cat_elemental,
        "Out with a Bang",
        "Kill enemies with explosive damage",
        (20, 75, 250, 600, 1000))

    challenges[1827] = Challenge(230, 1827,
        "GD_Challenges.elemental.Elemental_DealFireDOTDamage",
        challenge_cat_elemental,
        "Some Like It Hot",
        "Deal damage with incindiary DoT (damage-over-time) effects",
        (2500, 20000, 100000, 500000, 1000000),
        bonus=5)

    challenges[1828] = Challenge(231, 1828,
        "GD_Challenges.elemental.Elemental_DealCorrosiveDOTDamage",
        challenge_cat_elemental,
        "Chemical Burn",
        "Deal damage with corrosive DoT (damage-over-time) effects",
        (2500, 20000, 100000, 500000, 1000000))

    challenges[1977] = Challenge(394, 1977,
        "GD_Challenges.elemental.Elemental_DealIceDOTDamage",
        challenge_cat_elemental,
        "Frost Bite",
        "Deal damage with cryo DoT (damage-over-time) effects",
        (2500, 20000, 100000, 500000, 1000000))

    challenges[1829] = Challenge(232, 1829,
        "GD_Challenges.elemental.Elemental_DealShockDOTDamage",
        challenge_cat_elemental,
        "Watt's Up?",
        "Deal damage with shock DoT (damage-over-time) effects",
        (5000, 20000, 100000, 500000, 1000000))

    # Loot
    challenges[1848] = Challenge(252, 1848,
        "GD_Challenges.Pickups.Inventory_PickupWhiteItems",
        challenge_cat_loot,
        "Junkyard Dog",
        "Loot or purchase white items",
        (50, 125, 250, 400, 600))

    challenges[1849] = Challenge(253, 1849,
        "GD_Challenges.Pickups.Inventory_PickupGreenItems",
        challenge_cat_loot,
        "A Chunk of Purest Green",
        "Loot or purchase green-rarity items",
        (25, 75, 125, 250, 500),
        bonus=3)

    challenges[1850] = Challenge(254, 1850,
        "GD_Challenges.Pickups.Inventory_PickupBlueItems",
        challenge_cat_loot,
        "Rare as Rocking Horse...",
        "Loot or purchase blue-rarity items",
        (5, 25, 50, 75, 100))

    challenges[1851] = Challenge(255, 1851,
        "GD_Challenges.Pickups.Inventory_PickupPurpleItems",
        challenge_cat_loot,
        "Purple Haze",
        "Loot or purchase purple-rarity items",
        (3, 7, 15, 30, 75))

    challenges[1852] = Challenge(256, 1852,
        "GD_Challenges.Pickups.Inventory_PickupOrangeItems",
        challenge_cat_loot,
        "The Happiest Color",
        "Loot or purchase legendary items",
        (1, 3, 6, 10, 15),
        bonus=5)

    challenges[1731] = Challenge(334, 1731,
        "GD_Marigold_Challenges.Loot.Loot_OpenGlitchedChests",
        challenge_cat_loot,
        "I Like Surprises...",
        "Open Glitched treasure chests",
        (1, 3, 5, 8, 12))

    challenges[1730] = Challenge(333, 1730,
        "GD_Marigold_Challenges.Loot.Loot_PickupGlitchedItems",
        challenge_cat_loot,
        "99 Problems and a Glitch Aint One",
        "Loot or purchase Glitched-rarity items",
        (1, 3, 6, 10, 15),
        bonus=5)

    challenges[1619] = Challenge(108, 1619,
        "GD_Challenges.Loot.Loot_OpenChests",
        challenge_cat_loot,
        "Aaaaaand OPEN!",
        "Open treasure chests",
        (10, 25, 75, 150, 300))

    challenges[1620] = Challenge(110, 1620,
        "GD_Challenges.Loot.Loot_OpenLootables",
        challenge_cat_loot,
        "Scrounging Around",
        "Open lootable crates, lockers, and other objects",
        (50, 300, 1000, 2000, 3000),
        bonus=3)

    challenges[1580] = Challenge(8, 1580,
        "GD_Challenges.Loot.Loot_PickUpWeapons",
        challenge_cat_loot,
        "One for Every Occasion",
        "Pick up or purchase weapons",
        (10, 25, 150, 300, 750))

    # Money
    challenges[1808] = Challenge(119, 1808,
        "GD_Challenges.Economy.Economy_MoneySaved",
        challenge_cat_money,
        "Mom Would Be Proud",
        "Save a lot of money",
        (10000, 50000, 250000, 1000000, 3000000))

    challenges[1809] = Challenge(120, 1809,
        "GD_Challenges.Economy.General_MoneyFromCashDrops",
        challenge_cat_money,
        "Mr. Money Pits",
        "Collect dollars from cash drops",
        (5000, 25000, 125000, 500000, 1000000))

    challenges[1628] = Challenge(113, 1628,
        "GD_Challenges.Economy.Economy_SellItems",
        challenge_cat_money,
        "Pawn Broker",
        "Sell items to vending machines",
        (50, 100, 250, 750, 2000))

    challenges[1810] = Challenge(114, 1810,
        "GD_Challenges.Economy.Economy_PurchaseItemsOfTheDay",
        challenge_cat_money,
        "Impulse Shopper",
        "Buy Items of the Day from vending machines",
        (1, 5, 15, 30, 50))

    challenges[1760] = Challenge(112, 1760,
        "GD_Challenges.Economy.Economy_BuyItemsWithMoonstone",
        challenge_cat_money,
        "Over the Moon",
        "Purchase items with Moonstones",
        (25, 50, 125, 250, 500),
        bonus=3)

    challenges[1755] = Challenge(215, 1755,
        "GD_Challenges.Economy.Trade_ItemsWithPlayers",
        challenge_cat_money,
        "Trade Negotiations",
        "Trade with other players",
        (1, 5, 15, 30, 50))

    # Vehicle
    challenges[1590] = Challenge(37, 1590,
        "GD_Challenges.Vehicles.Vehicles_KillByRamming",
        challenge_cat_vehicle,
        "Fender Bender",
        "Kill enemies by ramming them with a vehicle",
        (5, 10, 50, 100, 200))

    challenges[1870] = Challenge(276, 1870,
        "GD_Challenges.Vehicles.Vehicles_KillByPowerSlide",
        challenge_cat_vehicle,
        "Splat 'n' Slide",
        "Kill enemies by power-sliding over them in a vehicle",
        (1, 5, 10, 25, 50),
        bonus=3)

    challenges[1591] = Challenge(38, 1591,
        "GD_Challenges.Vehicles.Vehicles_KillsWithVehicleWeapon",
        challenge_cat_vehicle,
        "Improvise, Adapt, Overcome",
        "Kill enemies using a turret or vehicle-mounted weapon",
        (10, 25, 150, 300, 750))

    challenges[1872] = Challenge(278, 1872,
        "GD_Challenges.Vehicles.Vehicles_VehicleKillsVehicle",
        challenge_cat_vehicle,
        "Road Warrior",
        "Kill vehicles while in a vehicle",
        (5, 10, 20, 40, 75))

    challenges[2044] = Challenge(461, 2044,
        "GD_Challenges.Vehicles.Vehicles_KillByPancaking",
        challenge_cat_vehicle,
        "Pancakes For Breakfast",
        "Kill enemies with Stingray slams",
        (1, 5, 10, 25, 50))

    # Health
    challenges[1867] = Challenge(271, 1867,
        "GD_Challenges.Player.Player_PointsHealed",
        challenge_cat_health,
        "Doctor Feels Good",
        "Recover health",
        (1000, 25000, 150000, 1000000, 5000000))

    challenges[1815] = Challenge(201, 1815,
        "GD_Challenges.Player.Player_SecondWind",
        challenge_cat_health,
        "Better You Than Me",
        "Get Second Winds by killing an enemy",
        (10, 25, 75, 150, 300))

    challenges[1816] = Challenge(202, 1816,
        "GD_Challenges.Player.Player_SecondWindFromBadass",
        challenge_cat_health,
        "There Can Be Only... Me",
        "Get Second Winds by killing badass enemies",
        (1, 5, 15, 30, 50),
        bonus=5)

    challenges[1818] = Challenge(205, 1818,
        "GD_Challenges.Player.Player_CoopRevivesOfFriends",
        challenge_cat_health,
        "Up Unt at Zem",
        "Revive a co-op partner",
        (5, 10, 50, 100, 200),
        bonus=5)

    challenges[1784] = Challenge(199, 1784,
        "GD_Challenges.Player.Player_SecondWindFromFire",
        challenge_cat_health,
        "The Phoenix",
        "Get Second Winds by killing enemies with an incindiary DoT (damage over time)",
        (1, 5, 15, 30, 50))

    challenges[1783] = Challenge(198, 1783,
        "GD_Challenges.Player.Player_SecondWindFromCorrosive",
        challenge_cat_health,
        "Soup's Up!",
        "Get Second Winds by killing enemies with a corrosive DoT (damage over time)",
        (1, 5, 15, 30, 50))

    challenges[1785] = Challenge(200, 1785,
        "GD_Challenges.Player.Player_SecondWindFromShock",
        challenge_cat_health,
        "Had a Bit of a Shocker",
        "Get Second Winds by killing enemies with a shock DoT (damage over time)",
        (1, 5, 15, 30, 50))

    challenges[2057] = Challenge(473, 2057,
        "GD_Challenges.Player.Player_SecondWindFromShatter",
        challenge_cat_health,
        "Rollin' the Ice",
        "Get Second Winds by shattering frozen enemies",
        (1, 5, 15, 30, 50))

    # Grenades
    challenges[1589] = Challenge(31, 1589,
        "GD_Challenges.Grenades.Grenade_Kills",
        challenge_cat_grenades,
        "Home Nade Cookin'",
        "Kill enemies with grenades",
        (10, 25, 150, 300, 750),
        bonus=3)

    challenges[1836] = Challenge(239, 1836,
        "GD_Challenges.Grenades.Grenade_KillsSingularityType",
        challenge_cat_grenades,
        "See Ya on the Other Side",
        "Kill enemies with Singularity grenades",
        (10, 25, 75, 150, 300))

    challenges[1835] = Challenge(238, 1835,
        "GD_Challenges.Grenades.Grenade_KillsMirvType",
        challenge_cat_grenades,
        "Big MIRV",
        "Kill enemies with MIRV grenades",
        (10, 25, 75, 150, 300),
        bonus=3)

    challenges[1833] = Challenge(236, 1833,
        "GD_Challenges.Grenades.Grenade_KillsAoEoTType",
        challenge_cat_grenades,
        "Sprayowee",
        "Kill enemies with Area-of-Effect grenades",
        (25, 50, 125, 250, 500))

    challenges[1834] = Challenge(237, 1834,
        "GD_Challenges.Grenades.Grenade_KillsBouncing",
        challenge_cat_grenades,
        "Betty Boom",
        "Kill enemies with Bouncing Betty grenades",
        (10, 25, 75, 150, 300))

    challenges[1868] = Challenge(240, 1868,
        "GD_Challenges.Grenades.Grenade_KillsTransfusionType",
        challenge_cat_grenades,
        "Pass the Chianti",
        "Kill enemies with Transfusion grenades",
        (10, 25, 75, 150, 300))

    # Shields
    challenges[1839] = Challenge(244, 1839,
        "GD_Challenges.Shields.Shields_KillsNova",
        challenge_cat_shields,
        "Nova Say Die",
        "Kill enemies with a Nova shield burst",
        (5, 10, 50, 100, 200),
        bonus=3)

    challenges[1840] = Challenge(245, 1840,
        "GD_Challenges.Shields.Shields_KillsRoid",
        challenge_cat_shields,
        "Wet Work",
        "Kill enemies while buffed by a Maylay shield",
        (5, 10, 50, 100, 200))

    challenges[1841] = Challenge(246, 1841,
        "GD_Challenges.Shields.Shields_KillsSpikes",
        challenge_cat_shields,
        "That'll Learn Ya",
        "Kill enemies with reflected damage from a Spike shield",
        (5, 10, 50, 100, 200))

    challenges[1842] = Challenge(247, 1842,
        "GD_Challenges.Shields.Shields_KillsImpact",
        challenge_cat_shields,
        "Amplitude Killulation",
        "Kill enemies while buffed by an Amplify shield",
        (5, 10, 50, 100, 200))

    challenges[1880] = Challenge(223, 1880,
        "GD_Challenges.Shields.Shields_AbsorbAmmo",
        challenge_cat_shields,
        "Ammo Eater",
        "Absorb enemy ammo with an Absorption shield",
        (20, 75, 250, 600, 1000),
        bonus=5)

    # Rocket Launchers
    challenges[1712] = Challenge(32, 1712,
        "GD_Challenges.Weapons.Launcher_Kills",
        challenge_cat_rockets,
        "Get a Rocket up Ya",
        "Kill enemies with rocket launchers",
        (10, 50, 100, 250, 500),
        bonus=3)

    challenges[1778] = Challenge(193, 1778,
        "GD_Challenges.Weapons.Launcher_SecondWinds",
        challenge_cat_rockets,
        "Magic Missile",
        "Get Second Winds with rocket launchers",
        (2, 5, 15, 30, 50))
    
    challenges[1820] = Challenge(225, 1820,
        "GD_Challenges.Weapons.Launcher_KillsSplashDamage",
        challenge_cat_rockets,
        "Collateral Damage",
        "Kill enemies with rocket launcher splash damage",
        (5, 10, 50, 100, 200))

    challenges[1819] = Challenge(224, 1819,
        "GD_Challenges.Weapons.Launcher_KillsDirectHit",
        challenge_cat_rockets,
        "Missile Magnet",
        "Kill enemies with direct hits from rocket launchers",
        (5, 10, 50, 100, 200),
        bonus=5)

    challenges[1821] = Challenge(54, 1821,
        "GD_Challenges.Weapons.Launcher_KillsFullShieldEnemy",
        challenge_cat_rockets,
        "Punker Buster",
        "Kill shielded enemies with one rocket each",
        (5, 15, 35, 75, 125))

    challenges[1758] = Challenge(52, 1758,
        "GD_Challenges.Weapons.Launcher_KillsLongRange",
        challenge_cat_rockets,
        "Hand of God",
        "Kill enemies from long range with rocket launchers",
        (25, 100, 400, 1000, 2000))

    # Sniper Rifles
    challenges[1586] = Challenge(28, 1586,
        "GD_Challenges.Weapons.SniperRifle_Kills",
        challenge_cat_sniper,
        "Sharp Shooter",
        "Kill enemies with sniper rifles",
        (20, 100, 500, 2500, 5000),
        bonus=3)

    challenges[1616] = Challenge(179, 1616,
        "GD_Challenges.Weapons.Sniper_CriticalHits",
        challenge_cat_sniper,
        "Melon Splitter",
        "Get critical hits with sniper rifles",
        (25, 100, 400, 1000, 2000))

    challenges[1774] = Challenge(189, 1774,
        "GD_Challenges.Weapons.Sniper_SecondWinds",
        challenge_cat_sniper,
        "Windage Adjustment",
        "Get Second Winds with sniper rifles",
        (2, 5, 15, 30, 50))

    challenges[1794] = Challenge(59, 1794,
        "GD_Challenges.Weapons.Sniper_CriticalHitKills",
        challenge_cat_sniper,
        "Critical Reception",
        "Kill enemies with critical hits using sniper rifles",
        (10, 25, 75, 150, 300))

    challenges[1748] = Challenge(47, 1748,
        "GD_Challenges.Weapons.SniperRifle_KillsFromHip",
        challenge_cat_sniper,
        "Ol' Skool",
        "Kill enemies with sniper rifles without using the scope/ironsights",
        (5, 10, 50, 100, 200))

    challenges[1831] = Challenge(234, 1831,
        "GD_Challenges.Weapons.SniperRifle_KillsUnaware",
        challenge_cat_sniper,
        "Clean and Simple",
        "Kill unaware enemies with sniper rifles",
        (5, 10, 50, 100, 200))

    challenges[1822] = Challenge(55, 1822,
        "GD_Challenges.Weapons.SniperRifle_KillsFullShieldEnemy",
        challenge_cat_sniper,
        "Penetrating Wound",
        "Kill shielded enemies with one shot using sniper rifles",
        (5, 15, 35, 75, 125),
        bonus=5)

    # Assault Rifles
    challenges[1587] = Challenge(29, 1587,
        "GD_Challenges.Weapons.AssaultRifle_Kills",
        challenge_cat_ar,
        "Assault With a Deadly Weapon",
        "Kill enemies with assault rifles",
        (25, 100, 400, 1000, 2000),
        bonus=3)

    challenges[1617] = Challenge(180, 1617,
        "GD_Challenges.Weapons.AssaultRifle_CriticalHits",
        challenge_cat_ar,
        "Aim to Please",
        "Get critical hits with assault rifles",
        (25, 100, 400, 1000, 2000))

    challenges[1775] = Challenge(190, 1775,
        "GD_Challenges.Weapons.AssaultRifle_SecondWinds",
        challenge_cat_ar,
        "Assaulty Dog",
        "Get Second Winds with assault rifles",
        (5, 15, 30, 50, 75))

    challenges[1795] = Challenge(60, 1795,
        "GD_Challenges.Weapons.AssaultRifle_CriticalHitKills",
        challenge_cat_ar,
        "Hot Lead Injection",
        "Kill enemies with critical hits using assault rifles",
        (10, 25, 75, 150, 300))

    challenges[1747] = Challenge(46, 1747,
        "GD_Challenges.Weapons.AssaultRifle_KillsCrouched",
        challenge_cat_ar,
        "Crouch Potato",
        "Kill enemies with assault rifles while crouched",
        (25, 75, 400, 1600, 3200),
        bonus=5)

    # Laser
    challenges[1984] = Challenge(401, 1984,
        "GD_Challenges.Weapons.Laser_CriticalHitKills",
        challenge_cat_laser,
        "Light 'em Up",
        "Kill enemies with critical hits using laser weapons",
        (10, 25, 75, 150, 300))

    challenges[1982] = Challenge(399, 1982,
        "GD_Challenges.Weapons.Laser_CriticalHits",
        challenge_cat_laser,
        "Aggressive Lasik",
        "Get critical hits with lasers",
        (25, 100, 400, 1000, 2000))

    challenges[2045] = Challenge(462, 2045,
        "GD_Challenges.Weapons.Laser_FlyingKills",
        challenge_cat_laser,
        "Battle Star",
        "Kill flying enemies with laser weapons while airborne",
        (10, 25, 150, 300, 750),
        bonus=5)

    challenges[1981] = Challenge(398, 1981,
        "GD_Challenges.Weapons.Laser_Kills",
        challenge_cat_laser,
        "Pew Pew",
        "Kill enemies with laser weapons",
        (25, 100, 400, 1000, 2000),
        bonus=3)

    challenges[1983] = Challenge(400, 1983,
        "GD_Challenges.Weapons.Laser_SecondWinds",
        challenge_cat_laser,
        "I See the Light",
        "Get Second Winds with laser weapons",
        (2, 5, 15, 30, 50))

    # SMGs
    challenges[1585] = Challenge(27, 1585,
        "GD_Challenges.Weapons.SMG_Kills",
        challenge_cat_smg,
        "Nice Spray Job",
        "Kill enemies with SMGs",
        (25, 100, 400, 1000, 2000),
        bonus=3)

    challenges[1615] = Challenge(178, 1615,
        "GD_Challenges.Weapons.SMG_CriticalHits",
        challenge_cat_smg,
        "Bring the Pain",
        "Get critical hits with SMGs",
        (25, 100, 400, 1000, 2000))

    challenges[1793] = Challenge(58, 1793,
        "GD_Challenges.Weapons.SMG_CriticalHitKills",
        challenge_cat_smg,
        "Dinky Death Dealer",
        "Kill enemies with critical hits using SMGs",
        (10, 25, 75, 150, 300))

    challenges[1773] = Challenge(188, 1773,
        "GD_Challenges.Weapons.SMG_SecondWinds",
        challenge_cat_smg,
        "And Stay Down!",
        "Get Second Winds with SMGs",
        (2, 5, 15, 30, 50))

    # Shotguns
    challenges[1584] = Challenge(26, 1584,
        "GD_Challenges.Weapons.Shotgun_Kills",
        challenge_cat_shotgun,
        "Boomstick Boogie",
        "Kill enemies with shotguns",
        (25, 100, 400, 1000, 2000),
        bonus=3)

    challenges[1614] = Challenge(177, 1614,
        "GD_Challenges.Weapons.Shotgun_CriticalHits",
        challenge_cat_shotgun,
        "Hello Uncle Buckshot",
        "Get critical hits with shotguns",
        (50, 250, 1000, 2500, 5000))

    challenges[1772] = Challenge(187, 1772,
        "GD_Challenges.Weapons.Shotgun_SecondWinds",
        challenge_cat_shotgun,
        "Shotgunning the Breeze",
        "Get Second Winds with shotguns",
        (2, 5, 15, 30, 50))

    challenges[1756] = Challenge(50, 1756,
        "GD_Challenges.Weapons.Shotgun_KillsPointBlank",
        challenge_cat_shotgun,
        "Take It All!",
        "Kill enemies from point-blank range with shotguns",
        (10, 25, 150, 300, 750))

    challenges[1757] = Challenge(51, 1757,
        "GD_Challenges.Weapons.Shotgun_KillsLongRange",
        challenge_cat_shotgun,
        "Over Achiever",
        "Kill enemies from long range with shotguns",
        (10, 25, 75, 150, 300))

    challenges[1792] = Challenge(57, 1792,
        "GD_Challenges.Weapons.Shotgun_CriticalHitKills",
        challenge_cat_shotgun,
        "Shotty Workmanship",
        "Kill enemies with critical hits using shotguns",
        (10, 50, 100, 250, 500))

    # Pistols
    challenges[1583] = Challenge(25, 1583,
        "GD_Challenges.Weapons.Pistol_Kills",
        challenge_cat_pistol,
        "Trigger Happy",
        "Kill enemies with pistols",
        (25, 100, 400, 1000, 2000),
        bonus=3)

    challenges[1613] = Challenge(176, 1613,
        "GD_Challenges.Weapons.Pistol_CriticalHits",
        challenge_cat_pistol,
        "Pistoleer",
        "Get critical hits with pistols",
        (25, 100, 400, 1000, 2000))

    challenges[1771] = Challenge(186, 1771,
        "GD_Challenges.Weapons.Pistol_SecondWinds",
        challenge_cat_pistol,
        "Pistol Whipped",
        "Get Second Winds with pistols",
        (2, 5, 15, 30, 50))

    challenges[1791] = Challenge(56, 1791,
        "GD_Challenges.Weapons.Pistol_CriticalHitKills",
        challenge_cat_pistol,
        "Magnum Maestro",
        "Kill enemies with critical hits using pistols",
        (10, 25, 75, 150, 300))

    challenges[1750] = Challenge(49, 1750,
        "GD_Challenges.Weapons.Pistol_KillsQuickshot",
        challenge_cat_pistol,
        "Gunslinger",
        "Kill enemies shortly after aiming down the sights with a pistol",
        (10, 25, 150, 300, 750),
        bonus=5)

    # Melee
    challenges[1600] = Challenge(75, 1600,
        "GD_Challenges.Melee.Melee_Kills",
        challenge_cat_melee,
        "Martial Marhsal",
        "Kill enemies with melee attacks",
        (25, 100, 400, 1000, 2000),
        bonus=3)

    challenges[1843] = Challenge(248, 1843,
        "GD_Challenges.Melee.Melee_KillsBladed",
        challenge_cat_melee,
        "Captain Cutty",
        "Kill enemies with melee attacks using bladed guns",
        (20, 75, 250, 600, 1000))

    # General Combat
    challenges[1571] = Challenge(0, 1571,
        "GD_Challenges.GeneralCombat.General_RoundsFired",
        challenge_cat_combat,
        "Projectile Proliferation",
        "Fire a lot of rounds",
        (5000, 10000, 25000, 50000, 75000),
        bonus=5)

    challenges[1652] = Challenge(90, 1652,
        "GD_Challenges.GeneralCombat.Player_KillsWithActionSkill",
        challenge_cat_combat,
        "Action Hero",
        "Kill enemies while using your Action Skill",
        (20, 75, 250, 750, 1500))

    challenges[1866] = Challenge(270, 1866,
        "GD_Challenges.GeneralCombat.Kills_AtNight",
        challenge_cat_combat,
        "Dark Sider",
        "Kill enemies at night",
        (25, 100, 500, 1000, 1500))

    challenges[1865] = Challenge(269, 1865,
        "GD_Challenges.GeneralCombat.Kills_AtDay",
        challenge_cat_combat,
        "Day of the Dead",
        "Kill enemies during the day",
        (250, 1000, 2500, 5000, 7500))

    challenges[1858] = Challenge(262, 1858,
        "GD_Challenges.GeneralCombat.Tediore_KillWithReload",
        challenge_cat_combat,
        "Throw Me the Money!",
        "Kill enemies with Tediore reloads",
        (5, 10, 25, 75, 150),
        bonus=5)

    challenges[1859] = Challenge(263, 1859,
        "GD_Challenges.GeneralCombat.Tediore_DamageFromReloads",
        challenge_cat_combat,
        "One Man's Trash",
        "Deal damage with Tediore reloads",
        (5000, 20000, 100000, 500000, 1000000))

    challenges[1862] = Challenge(266, 1862,
        "GD_Challenges.GeneralCombat.Barrels_KillEnemies",
        challenge_cat_combat,
        "Barrel of Laughs",
        "Kill enemies with stationary barrels",
        (10, 25, 50, 100, 200),
        bonus=3)

    challenges[1596] = Challenge(44, 1596,
        "GD_Challenges.GeneralCombat.Kills_FromCrits",
        challenge_cat_combat,
        "Executioner",
        "Kill enemies with critical hits",
        (20, 100, 500, 1000, 1500))

    challenges[2046] = Challenge(463, 2046,
        "GD_Challenges.GeneralCombat.Break_Masks",
        challenge_cat_combat,
        "Having Trouble Breathing?",
        "Shatter enemy oxygen masks",
        (25, 100, 250, 500, 1000))

    challenges[2047] = Challenge(464, 2047,
        "GD_Challenges.GeneralCombat.Kills_Asphyxiation",
        challenge_cat_combat,
        "Last Gasp",
        "Kill enemies by asphyxiation",
        (10, 25, 150, 300, 750))

    challenges[2050] = Challenge(466, 2050,
        "GD_Challenges.GeneralCombat.Shatter_With_Falling",
        challenge_cat_combat,
        "Comet Crash",
        "Shatter frozen enemies with falling damage",
        (5, 10, 50, 100, 200),
        bonus=5)

    challenges[2049] = Challenge(465, 2049,
        "GD_Challenges.GeneralCombat.Shatter_With_Weapons",
        challenge_cat_combat,
        "Ice to Meet You",
        "Shatter frozen enemies with weapons",
        (20, 75, 250, 600, 1000))

    # Miscellaneous
    challenges[1609] = Challenge(105, 1609,
        "GD_Challenges.Dueling.DuelsWon_HatersGonnaHate",
        challenge_cat_misc,
        "The Duelist",
        "Win duels",
        (1, 5, 15, 30, 50))

    challenges[1754] = Challenge(212, 1754,
        "GD_Challenges.Miscellaneous.Missions_SideMissionsCompleted",
        challenge_cat_misc,
        "Little on the Side",
        "Complete side missions",
        (10, 25, 50, 75, 125))

    challenges[1753] = Challenge(211, 1753,
        "GD_Challenges.Miscellaneous.Missions_OptionalObjectivesCompleted",
        challenge_cat_misc,
        "OC/DC",
        "Complete optional mission objectives",
        (5, 10, 15, 20, 30))

    challenges[1648] = Challenge(174, 1648,
        "GD_Challenges.Miscellaneous.Misc_CompleteChallenges",
        challenge_cat_misc,
        "We Have a Contender",
        "Complete many, many challenges",
        (5, 25, 50, 100, 200))

    def setup_currency_args(self, parser):
        """
        Adds the options we're using to control currency
        """

        parser.add_argument('--moonstone',
                type=int,
                help='Moonstone to set for character',
                )

    def setup_save_structure(self):
        """
        Sets up our main save_structure var which controls how we read the file
        """

        self.save_structure = {
            1: "class",
            2: "level",
            3: "experience",
            4: "skill_points",
            6: ("currency", True, 0),
            7: "playthroughs_completed",
            8: ("skills", True, {
                    1: "name",
                    2: "level",
                    3: "unknown3",
                    4: "unknown4"
                }),
            11: ("resources", True, {
                    1: "resource",
                    2: "pool",
                    3: ("amount", False, (self.unwrap_float, self.wrap_float)),
                    4: "level"
                }),
            13: ("sizes", False, {
                    1: "inventory",
                    2: "weapon_slots",
                    3: "weapon_slots_shown"
                }),
            15: ("stats", False, (self.unwrap_challenges, self.wrap_challenges)),
            16: ("active_fast_travel", True, None),
            17: "last_fast_travel",
            18: ("missions", True, {
                    1: "playthrough",
                    2: "active",
                    3: ("data", True, {
                        1: "name",
                        2: "status",
                        3: "is_from_dlc",
                        4: "dlc_id",
                        5: ("unknown5", False, (self.unwrap_bytes, self.wrap_bytes)),
                        6: "unknown6",
                        7: ("unknown7", False, (self.unwrap_bytes, self.wrap_bytes)),
                        8: "unknown8",
                        9: "unknown9",
                        10: "unknown10",
                        11: "level",
                    }),
                }),
            19: ("appearance", False, {
                    1: "name",
                    2: ("color1", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
                    3: ("color2", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
                    4: ("color3", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
                }),
            20: "save_game_id",
            21: "mission_number",
            23: ("unlocks", False, (self.unwrap_bytes, self.wrap_bytes)),
            24: ("unlock_notifications", False, (self.unwrap_bytes, self.wrap_bytes)),
            25: "time_played",
            26: "save_timestamp",
            29: ("game_stages", True, {
                    1: "name",
                    2: "level",
                    3: "is_from_dlc",
                    4: "dlc_id",
                    5: "playthrough",
                }),
            30: ("areas", True, {
                    1: "name",
                    2: "unknown2"
                }),
            34: ("id", False, {
                    1: ("a", False, 5),
                    2: ("b", False, 5),
                    3: ("c", False, 5),
                    4: ("d", False, 5),
                }),
            35: ("wearing", True, None),
            36: ("black_market", False, (self.unwrap_black_market, self.wrap_black_market)),
            37: "active_mission",
            38: ("challenges", True, {
                    1: "name",
                    2: "is_from_dlc",
                    3: "dlc_id"
                }),
            41: ("bank", True, {
                    1: ("data", False, (self.unwrap_item_info, self.wrap_item_info)),
                }),
            43: ("lockouts", True, {
                    1: "name",
                    2: "time",
                    3: "is_from_dlc",
                    4: "dlc_id"
                }),
            46: ("explored_areas", True, None),
            49: "active_playthrough",
            53: ("items", True, {
                    1: ("data", False, (self.unwrap_item_info, self.wrap_item_info)),
                    2: "unknown2",
                    3: "is_equipped",
                    4: "star"
                }),
            54: ("weapons", True, {
                    1: ("data", False, (self.unwrap_item_info, self.wrap_item_info)),
                    2: "slot",
                    3: "star",
                }),
            55: "stats_bonuses_disabled",
            56: "bank_size",
        }
