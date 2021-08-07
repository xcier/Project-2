#! /usr/bin/env python

import argparse
from .savefile import App, ChallengeCat, Challenge, Config, DictAction

class AppBL2(App):
    """
    Our main application class for Borderlands 2
    """

    # Game name
    game_name = 'Borderlands 2'

    # Item export/import prefix
    item_prefix = 'BL2'

    # Max char level
    max_level = 80

    # The only difference here is that BLTPS has "laser"
    black_market_keys = (
        'rifle', 'pistol', 'launcher', 'shotgun', 'smg',
        'sniper', 'grenade', 'backpack', 'bank',
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
    }

    # B2 version is 7, TPS version is 10
    # "version" taken from what Gibbed calls it, not sure if that's
    # an appropriate descriptor or not.
    item_struct_version = 7

    # Available choices for --unlock option
    unlock_choices = ['slaughterdome', 'tvhm', 'uvhm', 'challenges', 'ammo']

    # Challenge categories
    challenge_cat_dlc4 = ChallengeCat("Hammerlock's Hunt", 4)
    challenge_cat_dlc3 = ChallengeCat("Campaign of Carnage", 3)
    challenge_cat_dlc9 = ChallengeCat("Dragon Keep", 9)
    challenge_cat_dlc1 = ChallengeCat("Pirate's Booty", 1)
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
    challenges = {}

    # Hammerlock DLC Challenges
    challenges[1752] = Challenge(305, 1752,
        "GD_Sage_Challenges.Challenges.Challenge_Sage_KillSavages",
        challenge_cat_dlc4,
        "Savage Bloody Savage",
        "Kill savages",
        (20, 50, 100, 250, 500))
    challenges[1750] = Challenge(303, 1750,
        "GD_Sage_Challenges.Challenges.Challenge_Sage_KillDrifters",
        challenge_cat_dlc4,
        "Harder They Fall",
        "Kill drifters",
        (5, 15, 30, 40, 50))
    challenges[1751] = Challenge(304, 1751,
        "GD_Sage_Challenges.Challenges.Challenge_Sage_KillFanBoats",
        challenge_cat_dlc4,
        "Fan Boy",
        "Kill Fan Boats",
        (5, 10, 15, 20, 30))
    challenges[1753] = Challenge(306, 1753,
        "GD_Sage_Challenges.Challenges.Challenge_Sage_RaidBossA",
        challenge_cat_dlc4,
        "Voracidous the Invincible",
        "Defeat Voracidous the Invincible",
        (1, 3, 5, 10, 15))
    challenges[1952] = Challenge(307, 1952,
        "GD_Sage_Challenges.Challenges.Challenge_Sage_KillBoroks",
        challenge_cat_dlc4,
        "Boroking Around",
        "kill boroks",
        (10, 20, 50, 80, 120))
    challenges[1953] = Challenge(308, 1953,
        "GD_Sage_Challenges.Challenges.Challenge_Sage_KillScaylions",
        challenge_cat_dlc4,
        "Stinging Sensation",
        "Kill scaylions",
        (10, 20, 50, 80, 120))

    # Torgue DLC Challenges
    challenges[1756] = Challenge(310, 1756,
        "GD_Iris_Challenges.Challenges.Challenge_Iris_KillMotorcycles",
        challenge_cat_dlc3,
        "Bikes Destroyed",
        "Destroy Bikes",
        (10, 20, 30, 50, 80))
    challenges[1757] = Challenge(311, 1757,
        "GD_Iris_Challenges.Challenges.Challenge_Iris_KillBikers",
        challenge_cat_dlc3,
        "Bikers Killed",
        "Bikers Killed",
        (50, 100, 150, 200, 250))
    challenges[1950] = Challenge(316, 1950,
        "GD_Iris_Challenges.Challenges.Challenge_Iris_TorgueTokens",
        challenge_cat_dlc3,
        "Torgue Tokens Acquired",
        "Acquire Torgue Tokens",
        (100, 250, 500, 750, 1000))
    challenges[1949] = Challenge(315, 1949,
        "GD_Iris_Challenges.Challenges.Challenge_Iris_BuyTorgueItems",
        challenge_cat_dlc3,
        "Torgue Items Purchased",
        "Purchase Torgue Items with Tokens",
        (2, 5, 8, 12, 15))
    challenges[1758] = Challenge(312, 1758,
        "GD_Iris_Challenges.Challenges.Challenge_Iris_CompleteBattles",
        challenge_cat_dlc3,
        "Battles Completed",
        "Complete All Battles",
        (1, 4, 8, 12))
    challenges[1759] = Challenge(313, 1759,
        "GD_Iris_Challenges.Challenges.Challenge_Iris_Raid1",
        challenge_cat_dlc3,
        "Pete The Invincible Defeated",
        "Defeat Pete the Invincible",
        (1, 3, 5, 10, 15))

    # Tiny Tina DLC Challenges
    challenges[1954] = Challenge(318, 1954,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillDwarves",
        challenge_cat_dlc9,
        "Scot-Free",
        "Kill dwarves",
        (50, 100, 150, 200, 250))
    challenges[1768] = Challenge(320, 1768,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillGolems",
        challenge_cat_dlc9,
        "Rock Out With Your Rock Out",
        "Kill golems",
        (10, 25, 50, 80, 120))
    challenges[1769] = Challenge(321, 1769,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillKnights",
        challenge_cat_dlc9,
        "Knighty Knight",
        "Kill knights",
        (10, 25, 75, 120, 175))
    challenges[1771] = Challenge(323, 1771,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillOrcs",
        challenge_cat_dlc9,
        "Orcs Should Perish",
        "Kill orcs",
        (50, 100, 150, 200, 250))
    challenges[1772] = Challenge(324, 1772,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillSkeletons",
        challenge_cat_dlc9,
        "Bone Breaker",
        "Kill skeletons",
        (50, 100, 150, 200, 250))
    challenges[1773] = Challenge(325, 1773,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillSpiders",
        challenge_cat_dlc9,
        "Ew Ew Ew Ew",
        "Kill spiders",
        (25, 50, 100, 150, 200))
    challenges[1774] = Challenge(326, 1774,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillTreants",
        challenge_cat_dlc9,
        "Cheerful Green Giants",
        "Kill treants",
        (10, 20, 50, 80, 120))
    challenges[1775] = Challenge(327, 1775,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillWizards",
        challenge_cat_dlc9,
        "Magical Massacre",
        "Kill wizards",
        (10, 20, 50, 80, 120))
    challenges[1754] = Challenge(317, 1754,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillDragons",
        challenge_cat_dlc9,
        "Fus Roh Die",
        "Kill dragons",
        (10, 20, 50, 80, 110))
    challenges[1770] = Challenge(322, 1770,
        "GD_Aster_Challenges.Challenges.Challenge_Aster_KillMimics",
        challenge_cat_dlc9,
        "Can't Fool Me",
        "Kill mimics",
        (5, 15, 30, 50, 75))

    # Captain Scarlett DLC Challenges
    challenges[1743] = Challenge(298, 1743,
        "GD_Orchid_Challenges.Challenges.Challenge_Orchid_Crystals",
        challenge_cat_dlc1,
        "In The Pink",
        "Collect Seraph Crystals",
        (80, 160, 240, 320, 400))
    challenges[1755] = Challenge(299, 1755,
        "GD_Orchid_Challenges.Challenges.Challenge_Orchid_Purchase",
        challenge_cat_dlc1,
        "Shady Dealings",
        "Purchase Items With Seraph Crystals",
        (1, 3, 5, 10, 15))
    challenges[1745] = Challenge(294, 1745,
        "GD_Orchid_Challenges.Challenges.Challenge_Orchid_KillWorms",
        challenge_cat_dlc1,
        "Worm Killer",
        "Kill Sand Worms",
        (10, 20, 30, 50, 80))
    challenges[1746] = Challenge(295, 1746,
        "GD_Orchid_Challenges.Challenges.Challenge_Orchid_KillBandits",
        challenge_cat_dlc1,
        "Land Lubber",
        "Kill Pirates",
        (50, 100, 150, 200, 250))
    challenges[1747] = Challenge(296, 1747,
        "GD_Orchid_Challenges.Challenges.Challenge_Orchid_KillHovercrafts",
        challenge_cat_dlc1,
        "Hovernator",
        "Destroy Pirate Hovercrafts",
        (5, 10, 15, 20, 30))
    challenges[1748] = Challenge(297, 1748,
        "GD_Orchid_Challenges.Challenges.Challenge_Orchid_PirateChests",
        challenge_cat_dlc1,
        "Pirate Booty",
        "Open Pirate Chests",
        (25, 75, 150, 250, 375))
    challenges[1742] = Challenge(292, 1742,
        "GD_Orchid_Challenges.Challenges.Challenge_Orchid_Raid1",
        challenge_cat_dlc1,
        "Hyperius the Not-So-Invincible",
        "Divide Hyperius by zero",
        (1, 3, 5, 10, 15))
    challenges[1744] = Challenge(293, 1744,
        "GD_Orchid_Challenges.Challenges.Challenge_Orchid_Raid3",
        challenge_cat_dlc1,
        "Master Worm Food",
        "Feed Master Gee to his worms",
        (1, 3, 5, 10, 15))

    # Enemies
    challenges[1632] = Challenge(24, 1632,
        "GD_Challenges.enemies.Enemies_KillSkags",
        challenge_cat_enemies,
        "Skags to Riches",
        "Kill skags",
        (10, 25, 75, 150, 300))
    challenges[1675] = Challenge(84, 1675,
        "GD_Challenges.enemies.Enemies_KillConstructors",
        challenge_cat_enemies,
        "Constructor Destructor",
        "Kill constructors",
        (5, 12, 20, 30, 50))
    challenges[1655] = Challenge(80, 1655,
        "GD_Challenges.enemies.Enemies_KillLoaders",
        challenge_cat_enemies,
        "Load and Lock",
        "Kill loaders",
        (20, 100, 500, 1000, 1500),
        bonus=3)
    challenges[1651] = Challenge(76, 1651,
        "GD_Challenges.enemies.Enemies_KillBullymongs",
        challenge_cat_enemies,
        "Bully the Bullies",
        "Kill bullymongs",
        (25, 50, 150, 300, 750))
    challenges[1652] = Challenge(77, 1652,
        "GD_Challenges.enemies.Enemies_KillCrystalisks",
        challenge_cat_enemies,
        "Crystals are a Girl's Best Friend",
        "Kill crystalisks",
        (10, 25, 50, 80, 120))
    challenges[1653] = Challenge(78, 1653,
        "GD_Challenges.enemies.Enemies_KillGoliaths",
        challenge_cat_enemies,
        "WHY SO MUCH HURT?!",
        "Kill goliaths",
        (10, 25, 50, 80, 120))
    challenges[1654] = Challenge(79, 1654,
        "GD_Challenges.enemies.Enemies_KillEngineers",
        challenge_cat_enemies,
        "Paingineering",
        "Kill Hyperion personnel",
        (10, 25, 75, 150, 300))
    challenges[1658] = Challenge(83, 1658,
        "GD_Challenges.enemies.Enemies_KillSurveyors",
        challenge_cat_enemies,
        "Just a Moment of Your Time...",
        "Kill surveyors",
        (10, 25, 75, 150, 300))
    challenges[1694] = Challenge(87, 1694,
        "GD_Challenges.enemies.Enemies_KillNomads",
        challenge_cat_enemies,
        "You (No)Mad, Bro?",
        "Kill nomads",
        (10, 25, 75, 150, 300))
    challenges[1695] = Challenge(88, 1695,
        "GD_Challenges.enemies.Enemies_KillPsychos",
        challenge_cat_enemies,
        "Mama's Boys",
        "Kill psychos",
        (50, 100, 150, 300, 500))
    challenges[1696] = Challenge(89, 1696,
        "GD_Challenges.enemies.Enemies_KillRats",
        challenge_cat_enemies,
        "You Dirty Rat",
        "Kill rats.  Yes, really.",
        (10, 25, 75, 150, 300))
    challenges[1791] = Challenge(93, 1791,
        "GD_Challenges.enemies.Enemies_KillSpiderants",
        challenge_cat_enemies,
        "Pest Control",
        "Kill spiderants",
        (10, 25, 75, 150, 300))
    challenges[1792] = Challenge(94, 1792,
        "GD_Challenges.enemies.Enemies_KillStalkers",
        challenge_cat_enemies,
        "You're One Ugly Mother...",
        "Kill stalkers",
        (10, 25, 75, 150, 300))
    challenges[1793] = Challenge(95, 1793,
        "GD_Challenges.enemies.Enemies_KillThreshers",
        challenge_cat_enemies,
        "Tentacle Obsession",
        "Kill threshers",
        (10, 25, 75, 150, 300))
    challenges[1693] = Challenge(86, 1693,
        "GD_Challenges.enemies.Enemies_KillMarauders",
        challenge_cat_enemies,
        "Marauder? I Hardly Know 'Er",
        "Kill marauders",
        (20, 100, 500, 1000, 1500),
        bonus=3)
    challenges[1794] = Challenge(96, 1794,
        "GD_Challenges.enemies.Enemies_KillVarkid",
        challenge_cat_enemies,
        "Another Bug Hunt",
        "Kill varkids",
        (10, 25, 75, 150, 300))
    challenges[1795] = Challenge(97, 1795,
        "GD_Challenges.enemies.Enemies_KillGyros",
        challenge_cat_enemies,
        "Die in the Friendly Skies",
        "Kill buzzards",
        (10, 25, 45, 70, 100))
    challenges[1796] = Challenge(98, 1796,
        "GD_Challenges.enemies.Enemies_KillMidgets",
        challenge_cat_enemies,
        "Little Person, Big Pain",
        "Kill midgets",
        (10, 25, 75, 150, 300))
    challenges[1895] = Challenge(249, 1895,
        "GD_Challenges.enemies.Enemies_ShootBullymongProjectiles",
        challenge_cat_enemies,
        "Hurly Burly",
        "Shoot bullymong-tossed projectiles out of midair",
        (10, 25, 50, 125, 250))
    challenges[1896] = Challenge(250, 1896,
        "GD_Challenges.enemies.Enemies_ReleaseChainedMidgets",
        challenge_cat_enemies,
        "Short-Chained",
        "Shoot chains to release midgets from shields",
        (1, 5, 15, 30, 50))
    challenges[1934] = Challenge(99, 1934,
        "GD_Challenges.enemies.Enemies_KillBruisers",
        challenge_cat_enemies,
        "Cruising for a Bruising",
        "Kill bruisers",
        (10, 25, 75, 150, 300))
    challenges[1732] = Challenge(91, 1732,
        "GD_Challenges.enemies.Enemies_KillVarkidPods",
        challenge_cat_enemies,
        "Pod Pew Pew",
        "Kill varkid pods before they hatch",
        (10, 25, 45, 70, 100))

    # Elemental
    challenges[1873] = Challenge(225, 1873,
        "GD_Challenges.elemental.Elemental_SetEnemiesOnFire",
        challenge_cat_elemental,
        "Cowering Inferno",
        "Ignite enemies",
        (25, 100, 400, 1000, 2000))
    challenges[1642] = Challenge(40, 1642,
        "GD_Challenges.elemental.Elemental_KillEnemiesCorrosive",
        challenge_cat_elemental,
        "Acid Trip",
        "Kill enemies with corrode damage",
        (20, 75, 250, 600, 1000))
    challenges[1645] = Challenge(43, 1645,
        "GD_Challenges.elemental.Elemental_KillEnemiesExplosive",
        challenge_cat_elemental,
        "Boom.",
        "Kill enemies with explosive damage",
        (20, 75, 250, 600, 1000),
        bonus=3)
    challenges[1877] = Challenge(229, 1877,
        "GD_Challenges.elemental.Elemental_DealFireDOTDamage",
        challenge_cat_elemental,
        "I Just Want to Set the World on Fire",
        "Deal burn damage",
        (2500, 20000, 100000, 500000, 1000000),
        bonus=5)
    challenges[1878] = Challenge(230, 1878,
        "GD_Challenges.elemental.Elemental_DealCorrosiveDOTDamage",
        challenge_cat_elemental,
        "Corroderate",
        "Deal corrode damage",
        (2500, 20000, 100000, 500000, 1000000))
    challenges[1879] = Challenge(231, 1879,
        "GD_Challenges.elemental.Elemental_DealShockDOTDamage",
        challenge_cat_elemental,
        'Say "Watt" Again',
        "Deal electrocute damage",
        (5000, 20000, 100000, 500000, 1000000))
    challenges[1880] = Challenge(232, 1880,
        "GD_Challenges.elemental.Elemental_DealBonusSlagDamage",
        challenge_cat_elemental,
        "Slag-Licked",
        "Deal bonus damage to Slagged enemies",
        (5000, 25000, 150000, 1000000, 5000000),
        bonus=3)

    # Loot
    challenges[1898] = Challenge(251, 1898,
        "GD_Challenges.Pickups.Inventory_PickupWhiteItems",
        challenge_cat_loot,
        "Another Man's Treasure",
        "Loot or purchase white items",
        (50, 125, 250, 400, 600))
    challenges[1899] = Challenge(252, 1899,
        "GD_Challenges.Pickups.Inventory_PickupGreenItems",
        challenge_cat_loot,
        "It's Not Easy Looting Green",
        "Loot or purchase green items",
        (20, 50, 75, 125, 200),
        bonus=3)
    challenges[1900] = Challenge(253, 1900,
        "GD_Challenges.Pickups.Inventory_PickupBlueItems",
        challenge_cat_loot,
        "I Like My Treasure Rare",
        "Loot or purchase blue items",
        (5, 12, 20, 30, 45))
    challenges[1901] = Challenge(254, 1901,
        "GD_Challenges.Pickups.Inventory_PickupPurpleItems",
        challenge_cat_loot,
        "Purple Reign",
        "Loot or purchase purple items",
        (2, 4, 7, 12, 20))
    challenges[1902] = Challenge(255, 1902,
        "GD_Challenges.Pickups.Inventory_PickupOrangeItems",
        challenge_cat_loot,
        "Nothing Rhymes with Orange",
        "Loot or purchase orange items",
        (1, 3, 6, 10, 15),
        bonus=5)
    challenges[1669] = Challenge(108, 1669,
        "GD_Challenges.Loot.Loot_OpenChests",
        challenge_cat_loot,
        "The Call of Booty",
        "Open treasure chests",
        (5, 25, 50, 125, 250))
    challenges[1670] = Challenge(109, 1670,
        "GD_Challenges.Loot.Loot_OpenLootables",
        challenge_cat_loot,
        "Open Pandora's Boxes",
        "Open lootable chests, lockers, and other objects",
        (50, 250, 750, 1500, 2500),
        bonus=3)
    challenges[1630] = Challenge(8, 1630,
        "GD_Challenges.Loot.Loot_PickUpWeapons",
        challenge_cat_loot,
        "Gun Runner",
        "Pick up or purchase weapons",
        (10, 25, 150, 300, 750))

    # Money
    challenges[1858] = Challenge(118, 1858,
        "GD_Challenges.Economy.Economy_MoneySaved",
        challenge_cat_money,
        "For the Hoard!",
        "Save a lot of money",
        (10000, 50000, 250000, 1000000, 3000000),
        bonus=3)
    challenges[1859] = Challenge(119, 1859,
        "GD_Challenges.Economy.General_MoneyFromCashDrops",
        challenge_cat_money,
        "Dolla Dolla Bills, Y'all",
        "Collect dollars from cash drops",
        (5000, 25000, 125000, 500000, 1000000))
    challenges[1678] = Challenge(112, 1678,
        "GD_Challenges.Economy.Economy_SellItems",
        challenge_cat_money,
        "Wholesale",
        "Sell items to vending machines",
        (10, 25, 150, 300, 750))
    challenges[1860] = Challenge(113, 1860,
        "GD_Challenges.Economy.Economy_PurchaseItemsOfTheDay",
        challenge_cat_money,
        "Limited-Time Offer",
        "Buy Items of the Day",
        (1, 5, 15, 30, 50))
    challenges[1810] = Challenge(111, 1810,
        "GD_Challenges.Economy.Economy_BuyItemsWithEridium",
        challenge_cat_money,
        "Whaddaya Buyin'?",
        "Purchase items with Eridium",
        (2, 5, 9, 14, 20),
        bonus=4)
    challenges[1805] = Challenge(214, 1805,
        "GD_Challenges.Economy.Trade_ItemsWithPlayers",
        challenge_cat_money,
        "Psst, Hey Buddy...",
        "Trade with other players",
        (1, 5, 15, 30, 50))

    # Vehicle
    challenges[1640] = Challenge(37, 1640,
        "GD_Challenges.Vehicles.Vehicles_KillByRamming",
        challenge_cat_vehicle,
        "Hit-and-Fun",
        "Kill enemies by ramming them with a vehicle",
        (5, 10, 50, 100, 200))
    challenges[1920] = Challenge(275, 1920,
        "GD_Challenges.Vehicles.Vehicles_KillByPowerSlide",
        challenge_cat_vehicle,
        "Blue Sparks",
        "Kill enemies by power-sliding over them in a vehicle",
        (5, 15, 30, 50, 75),
        bonus=3)
    challenges[1641] = Challenge(38, 1641,
        "GD_Challenges.Vehicles.Vehicles_KillsWithVehicleWeapon",
        challenge_cat_vehicle,
        "Turret Syndrome",
        "Kill enemies using a turret or vehicle-mounted weapon",
        (10, 25, 150, 300, 750))
    challenges[1922] = Challenge(277, 1922,
        "GD_Challenges.Vehicles.Vehicles_VehicleKillsVehicle",
        challenge_cat_vehicle,
        "...One Van Leaves",
        "Kill vehicles while in a vehicle",
        (5, 10, 50, 100, 200))
    challenges[1919] = Challenge(274, 1919,
        "GD_Challenges.Vehicles.Vehicles_KillsWhilePassenger",
        challenge_cat_vehicle,
        "Passive Aggressive",
        "Kill enemies while riding as a passenger (not a gunner) in a vehicle",
        (1, 10, 50, 100, 200))

    # Health
    challenges[1917] = Challenge(270, 1917,
        "GD_Challenges.Player.Player_PointsHealed",
        challenge_cat_health,
        "Heal Plz",
        "Recover health",
        (1000, 25000, 150000, 1000000, 5000000))
    challenges[1865] = Challenge(200, 1865,
        "GD_Challenges.Player.Player_SecondWind",
        challenge_cat_health,
        "I'll Just Help Myself",
        "Get Second Winds by killing an enemy",
        (5, 10, 50, 100, 200))
    challenges[1866] = Challenge(201, 1866,
        "GD_Challenges.Player.Player_SecondWindFromBadass",
        challenge_cat_health,
        "Badass Bingo",
        "Get Second Winds by killing a badass enemy",
        (1, 5, 15, 30, 50),
        bonus=5)
    challenges[1868] = Challenge(204, 1868,
        "GD_Challenges.Player.Player_CoopRevivesOfFriends",
        challenge_cat_health,
        "This is No Time for Lazy!",
        "Revive a co-op partner",
        (5, 10, 50, 100, 200),
        bonus=5)
    challenges[1834] = Challenge(198, 1834,
        "GD_Challenges.Player.Player_SecondWindFromFire",
        challenge_cat_health,
        "Death, Wind, and Fire",
        "Get Second Winds by killing enemies with a burn DoT (damage over time)",
        (1, 5, 15, 30, 50))
    challenges[1833] = Challenge(197, 1833,
        "GD_Challenges.Player.Player_SecondWindFromCorrosive",
        challenge_cat_health,
        "Green Meanie",
        "Get Second Winds by killing enemies with a corrosive DoT (damage over time)",
        (1, 5, 15, 30, 50))
    challenges[1835] = Challenge(199, 1835,
        "GD_Challenges.Player.Player_SecondWindFromShock",
        challenge_cat_health,
        "I'm Back! Shocked?",
        "Get Second Winds by killing enemies with an electrocute DoT (damage over time)",
        (1, 5, 15, 30, 50))

    # Grenades
    challenges[1639] = Challenge(31, 1639,
        "GD_Challenges.Grenades.Grenade_Kills",
        challenge_cat_grenades,
        "Pull the Pin",
        "Kill enemies with grenades",
        (10, 25, 150, 300, 750),
        bonus=3)
    challenges[1886] = Challenge(238, 1886,
        "GD_Challenges.Grenades.Grenade_KillsSingularityType",
        challenge_cat_grenades,
        "Singled Out",
        "Kill enemies with Singularity grenades",
        (10, 25, 75, 150, 300))
    challenges[1885] = Challenge(237, 1885,
        "GD_Challenges.Grenades.Grenade_KillsMirvType",
        challenge_cat_grenades,
        "EXPLOOOOOSIONS!",
        "Kill enemies with Mirv grenades",
        (10, 25, 75, 150, 300),
        bonus=3)
    challenges[1883] = Challenge(235, 1883,
        "GD_Challenges.Grenades.Grenade_KillsAoEoTType",
        challenge_cat_grenades,
        "Chemical Sprayer",
        "Kill enemies with Area-of-Effect grenades",
        (10, 25, 75, 150, 300))
    challenges[1884] = Challenge(236, 1884,
        "GD_Challenges.Grenades.Grenade_KillsBouncing",
        challenge_cat_grenades,
        "Whoa, Black Betty",
        "Kill enemies with Bouncing Betty grenades",
        (10, 25, 75, 150, 300))
    challenges[1918] = Challenge(239, 1918,
        "GD_Challenges.Grenades.Grenade_KillsTransfusionType",
        challenge_cat_grenades,
        "Health Vampire",
        "Kill enemies with Transfusion grenades",
        (10, 25, 75, 150, 300))

    # Shields
    challenges[1889] = Challenge(243, 1889,
        "GD_Challenges.Shields.Shields_KillsNova",
        challenge_cat_shields,
        "Super Novas",
        "Kill enemies with a Nova shield burst",
        (5, 10, 50, 100, 200),
        bonus=3)
    challenges[1890] = Challenge(244, 1890,
        "GD_Challenges.Shields.Shields_KillsRoid",
        challenge_cat_shields,
        "Roid Rage",
        'Kill enemies while buffed by a "Maylay" shield',
        (5, 10, 50, 100, 200))
    challenges[1891] = Challenge(245, 1891,
        "GD_Challenges.Shields.Shields_KillsSpikes",
        challenge_cat_shields,
        "Game of Thorns",
        "Kill enemies with reflected damage from a Spike shield",
        (5, 10, 50, 100, 200))
    challenges[1892] = Challenge(246, 1892,
        "GD_Challenges.Shields.Shields_KillsImpact",
        challenge_cat_shields,
        "Amp It Up",
        "Kill enemies while buffed by an Amplify shield",
        (5, 10, 50, 100, 200))
    challenges[1930] = Challenge(222, 1930,
        "GD_Challenges.Shields.Shields_AbsorbAmmo",
        challenge_cat_shields,
        "Ammo Eater",
        "Absorb enemy ammo with an Absorption shield",
        (20, 75, 250, 600, 1000),
        bonus=5)

    # Rocket Launchers
    challenges[1762] = Challenge(32, 1762,
        "GD_Challenges.Weapons.Launcher_Kills",
        challenge_cat_rockets,
        "Rocket and Roll",
        "Kill enemies with rocket launchers",
        (10, 50, 100, 250, 500),
        bonus=3)
    challenges[1828] = Challenge(192, 1828,
        "GD_Challenges.Weapons.Launcher_SecondWinds",
        challenge_cat_rockets,
        "Gone with the Second Wind",
        "Get Second Winds with rocket launchers",
        (2, 5, 15, 30, 50))
    challenges[1870] = Challenge(224, 1870,
        "GD_Challenges.Weapons.Launcher_KillsSplashDamage",
        challenge_cat_rockets,
        "Splish Splash",
        "Kill enemies with rocket launcher splash damage",
        (5, 10, 50, 100, 200))
    challenges[1869] = Challenge(223, 1869,
        "GD_Challenges.Weapons.Launcher_KillsDirectHit",
        challenge_cat_rockets,
        "Catch-a-Rocket!",
        "Kill enemies with direct hits from rocket launchers",
        (5, 10, 50, 100, 200),
        bonus=5)
    challenges[1871] = Challenge(54, 1871,
        "GD_Challenges.Weapons.Launcher_KillsFullShieldEnemy",
        challenge_cat_rockets,
        "Shield Basher",
        "Kill shielded enemies with one rocket each",
        (5, 15, 35, 75, 125))
    challenges[1808] = Challenge(52, 1808,
        "GD_Challenges.Weapons.Launcher_KillsLongRange",
        challenge_cat_rockets,
        "Sky Rockets in Flight...",
        "Kill enemies from long range with rocket launchers",
        (25, 100, 400, 1000, 2000))

    # Sniper Rifles
    challenges[1636] = Challenge(28, 1636,
        "GD_Challenges.Weapons.SniperRifle_Kills",
        challenge_cat_sniper,
        "Longshot",
        "Kill enemies with sniper rifles",
        (20, 100, 500, 2500, 5000),
        bonus=3)
    challenges[1666] = Challenge(178, 1666,
        "GD_Challenges.Weapons.Sniper_CriticalHits",
        challenge_cat_sniper,
        "Longshot Headshot",
        "Get critical hits with sniper rifles",
        (25, 100, 400, 1000, 2000))
    challenges[1824] = Challenge(188, 1824,
        "GD_Challenges.Weapons.Sniper_SecondWinds",
        challenge_cat_sniper,
        "Leaf on the Second Wind",
        "Get Second Winds with sniper rifles",
        (2, 5, 15, 30, 50))
    challenges[1844] = Challenge(59, 1844,
        "GD_Challenges.Weapons.Sniper_CriticalHitKills",
        challenge_cat_sniper,
        "Snipe Hunting",
        "Kill enemies with critical hits using sniper rifles",
        (10, 25, 75, 150, 300))
    challenges[1798] = Challenge(47, 1798,
        "GD_Challenges.Weapons.SniperRifle_KillsFromHip",
        challenge_cat_sniper,
        "No Scope, No Problem",
        "Kill enemies with sniper rifles without using ironsights",
        (5, 10, 50, 100, 200))
    challenges[1881] = Challenge(233, 1881,
        "GD_Challenges.Weapons.SniperRifle_KillsUnaware",
        challenge_cat_sniper,
        "Surprise!",
        "Kill unaware enemies with sniper rifles",
        (5, 10, 50, 100, 200))
    challenges[1872] = Challenge(55, 1872,
        "GD_Challenges.Weapons.SniperRifle_KillsFullShieldEnemy",
        challenge_cat_sniper,
        "Eviscerated",
        "Kill shielded enemies with one shot using sniper rifles",
        (5, 15, 35, 75, 125),
        bonus=5)

    # Assault Rifles
    challenges[1637] = Challenge(29, 1637,
        "GD_Challenges.Weapons.AssaultRifle_Kills",
        challenge_cat_ar,
        "Aggravated Assault",
        "Kill enemies with assault rifles",
        (25, 100, 400, 1000, 2000),
        bonus=3)
    challenges[1667] = Challenge(179, 1667,
        "GD_Challenges.Weapons.AssaultRifle_CriticalHits",
        challenge_cat_ar,
        "This Is My Rifle...",
        "Get critical hits with assault rifles",
        (25, 100, 400, 1000, 2000))
    challenges[1825] = Challenge(189, 1825,
        "GD_Challenges.Weapons.AssaultRifle_SecondWinds",
        challenge_cat_ar,
        "From My Cold, Dead Hands",
        "Get Second Winds with assault rifles",
        (5, 15, 30, 50, 75))
    challenges[1845] = Challenge(60, 1845,
        "GD_Challenges.Weapons.AssaultRifle_CriticalHitKills",
        challenge_cat_ar,
        "... This Is My Gun",
        "Kill enemies with critical hits using assault rifles",
        (10, 25, 75, 150, 300))
    challenges[1797] = Challenge(46, 1797,
        "GD_Challenges.Weapons.AssaultRifle_KillsCrouched",
        challenge_cat_ar,
        "Crouching Tiger, Hidden Assault Rifle",
        "Kill enemies with assault rifles while crouched",
        (25, 75, 400, 1600, 3200),
        bonus=5)

    # SMGs
    challenges[1635] = Challenge(27, 1635,
        "GD_Challenges.Weapons.SMG_Kills",
        challenge_cat_smg,
        "Hail of Bullets",
        "Kill enemies with SMGs",
        (25, 100, 400, 1000, 2000),
        bonus=3)
    challenges[1665] = Challenge(177, 1665,
        "GD_Challenges.Weapons.SMG_CriticalHits",
        challenge_cat_smg,
        "Constructive Criticism",
        "Get critical hits with SMGs",
        (25, 100, 400, 1000, 2000))
    challenges[1843] = Challenge(58, 1843,
        "GD_Challenges.Weapons.SMG_CriticalHitKills",
        challenge_cat_smg,
        "High Rate of Ire",
        "Kill enemies with critical hits using SMGs",
        (10, 25, 75, 150, 300))
    challenges[1823] = Challenge(187, 1823,
        "GD_Challenges.Weapons.SMG_SecondWinds",
        challenge_cat_smg,
        "More Like Submachine FUN",
        "Get Second Winds with SMGs",
        (2, 5, 15, 30, 50))

    # Shotguns
    challenges[1634] = Challenge(26, 1634,
        "GD_Challenges.Weapons.Shotgun_Kills",
        challenge_cat_shotgun,
        "Shotgun!",
        "Kill enemies with shotguns",
        (25, 100, 400, 1000, 2000),
        bonus=3)
    challenges[1664] = Challenge(176, 1664,
        "GD_Challenges.Weapons.Shotgun_CriticalHits",
        challenge_cat_shotgun,
        "Faceful of Buckshot",
        "Get critical hits with shotguns",
        (50, 250, 1000, 2500, 5000))
    challenges[1822] = Challenge(186, 1822,
        "GD_Challenges.Weapons.Shotgun_SecondWinds",
        challenge_cat_shotgun,
        "Lock, Stock, and...",
        "Get Second Winds with shotguns",
        (2, 5, 15, 30, 50))
    challenges[1806] = Challenge(50, 1806,
        "GD_Challenges.Weapons.Shotgun_KillsPointBlank",
        challenge_cat_shotgun,
        "Open Wide!",
        "Kill enemies from point-blank range with shotguns",
        (10, 25, 150, 300, 750))
    challenges[1807] = Challenge(51, 1807,
        "GD_Challenges.Weapons.Shotgun_KillsLongRange",
        challenge_cat_shotgun,
        "Shotgun Sniper",
        "Kill enemies from long range with shotguns",
        (10, 25, 75, 150, 300))
    challenges[1842] = Challenge(57, 1842,
        "GD_Challenges.Weapons.Shotgun_CriticalHitKills",
        challenge_cat_shotgun,
        "Shotgun Surgeon",
        "Kill enemies with critical hits using shotguns",
        (10, 50, 100, 250, 500))

    # Pistols
    challenges[1633] = Challenge(25, 1633,
        "GD_Challenges.Weapons.Pistol_Kills",
        challenge_cat_pistol,
        "The Killer",
        "Kill enemies with pistols",
        (25, 100, 400, 1000, 2000),
        bonus=3)
    challenges[1663] = Challenge(175, 1663,
        "GD_Challenges.Weapons.Pistol_CriticalHits",
        challenge_cat_pistol,
        "Deadeye",
        "Get critical hits with pistols",
        (25, 100, 400, 1000, 2000))
    challenges[1821] = Challenge(185, 1821,
        "GD_Challenges.Weapons.Pistol_SecondWinds",
        challenge_cat_pistol,
        "Hard Boiled",
        "Get Second Winds with pistols",
        (2, 5, 15, 30, 50))
    challenges[1841] = Challenge(56, 1841,
        "GD_Challenges.Weapons.Pistol_CriticalHitKills",
        challenge_cat_pistol,
        "Pistolero",
        "Kill enemies with critical hits using pistols",
        (10, 25, 75, 150, 300))
    challenges[1800] = Challenge(49, 1800,
        "GD_Challenges.Weapons.Pistol_KillsQuickshot",
        challenge_cat_pistol,
        "Quickdraw",
        "Kill enemies shortly after entering ironsights with a pistol",
        (10, 25, 150, 300, 750),
        bonus=5)

    # Melee
    challenges[1650] = Challenge(75, 1650,
        "GD_Challenges.Melee.Melee_Kills",
        challenge_cat_melee,
        "Fisticuffs!",
        "Kill enemies with melee attacks",
        (25, 100, 400, 1000, 2000),
        bonus=3)
    challenges[1893] = Challenge(247, 1893,
        "GD_Challenges.Melee.Melee_KillsBladed",
        challenge_cat_melee,
        "A Squall of Violence",
        "Kill enemies with melee attacks using bladed guns",
        (20, 75, 250, 600, 1000))

    # General Combat
    challenges[1621] = Challenge(0, 1621,
        "GD_Challenges.GeneralCombat.General_RoundsFired",
        challenge_cat_combat,
        "Knee-Deep in Brass",
        "Fire a lot of rounds",
        (1000, 5000, 10000, 25000, 50000),
        bonus=5)
    challenges[1702] = Challenge(90, 1702,
        "GD_Challenges.GeneralCombat.Player_KillsWithActionSkill",
        challenge_cat_combat,
        "...To Pay the Bills",
        "Kill enemies while using your Action Skill",
        (20, 75, 250, 600, 1000),
        bonus=5)
    challenges[1916] = Challenge(269, 1916,
        "GD_Challenges.GeneralCombat.Kills_AtNight",
        challenge_cat_combat,
        "...I Got to Boogie",
        "Kill enemies at night",
        (10, 25, 150, 300, 750))
    challenges[1915] = Challenge(268, 1915,
        "GD_Challenges.GeneralCombat.Kills_AtDay",
        challenge_cat_combat,
        "Afternoon Delight",
        "Kill enemies during the day",
        (50, 250, 1000, 2500, 5000))
    challenges[1908] = Challenge(261, 1908,
        "GD_Challenges.GeneralCombat.Tediore_KillWithReload",
        challenge_cat_combat,
        "Boomerbang",
        "Kill enemies with Tediore reloads",
        (5, 10, 50, 100, 200),
        bonus=5)
    challenges[1909] = Challenge(262, 1909,
        "GD_Challenges.GeneralCombat.Tediore_DamageFromReloads",
        challenge_cat_combat,
        "Gun Slinger",
        "Deal damage with Tediore reloads",
        (5000, 20000, 100000, 500000, 1000000))
    challenges[1912] = Challenge(265, 1912,
        "GD_Challenges.GeneralCombat.Barrels_KillEnemies",
        challenge_cat_combat,
        "Not Full of Monkeys",
        "Kill enemies with stationary barrels",
        (10, 25, 45, 70, 100),
        bonus=3)
    challenges[1646] = Challenge(44, 1646,
        "GD_Challenges.GeneralCombat.Kills_FromCrits",
        challenge_cat_combat,
        "Critical Acclaim",
        "Kill enemies with critical hits. And rainbows.",
        (20, 100, 500, 1000, 1500))

    # Miscellaneous
    challenges[1659] = Challenge(104, 1659,
        "GD_Challenges.Dueling.DuelsWon_HatersGonnaHate",
        challenge_cat_misc,
        "Haters Gonna Hate",
        "Win duels",
        (1, 5, 15, 30, 50))
    challenges[1804] = Challenge(211, 1804,
        "GD_Challenges.Miscellaneous.Missions_SideMissionsCompleted",
        challenge_cat_misc,
        "Sidejacked",
        "Complete side missions",
        (5, 15, 30, 55, 90))
    challenges[1803] = Challenge(210, 1803,
        "GD_Challenges.Miscellaneous.Missions_OptionalObjectivesCompleted",
        challenge_cat_misc,
        "Compl33tionist",
        "Complete optional mission objectives",
        (10, 25, 45, 70, 100))
    challenges[1698] = Challenge(173, 1698,
        "GD_Challenges.Miscellaneous.Misc_CompleteChallenges",
        challenge_cat_misc,
        "Yo Dawg I Herd You Like Challenges",
        "Complete many, many challenges",
        (5, 25, 50, 100, 200))
    challenges[1940] = Challenge(100, 1940,
        "GD_Challenges.Miscellaneous.Misc_JimmyJenkins",
        challenge_cat_misc,
        "JEEEEENKINSSSSSS!!!",
        "Find and eliminate Jimmy Jenkins",
        (1, 3, 6, 10, 15),
        bonus=5)

    def setup_currency_args(self, parser):
        """
        Adds the options we're using to control currency
        """

        parser.add_argument('--eridium',
                type=int,
                help='Eridium to set for character',
                )

        parser.add_argument('--seraph',
                type=int,
                help='Seraph crystals to set for character',
                )

        parser.add_argument('--torgue',
                type=int,
                help='Torgue tokens to set for character',
                )

    @staticmethod
    def oplevel(value):
        """
        Helper function for argparse which requires a valid Overpower level
        """
        try:
            intval = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError('OP Levels must be from 0 to 10')
        if intval < 0 or intval > 10:
            raise argparse.ArgumentTypeError('OP Levels must be from 0 to 10')
        return intval

    def setup_game_specific_args(self, parser):
        """
        Adds BL2-specific arguments
        """

        parser.add_argument('--oplevel',
                type=AppBL2.oplevel,
                help='OP Level to unlock (will also unlock TVHM/UVHM if not already unlocked)',
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
                    4: "unknown4",
                }),
            55: "stats_bonuses_disabled",
            56: "bank_size",
        }
