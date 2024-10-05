import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

description = "Dice roller for 2d20 games. This was designed for Fallout, but should work for other 2d20 games"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", description=description, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("------")


@bot.command()
async def rolld20(ctx, num_d20: int = 2, tn: int = None, complication: int = 20, tagged_skill_level: int = 0):
    """
    Rolls 2d20 and returns the result, including the number of successes or complications

    :param ctx: The context
    :param num_d20: The number of d20s to be rolled. There can be more than 2d20
        if the user spends AP
    :param tn: The Target Number to roll under for a success. This isn't necessary.
        If not provided the method won"t return any information about the number
        of successes.
    :param complication: If the complication range is extended this allows
        for an accurate count of complications
    :param tagged_skill_level: If the skill rolling is tagged then it counts
        any successes as critical successes

    :return:
    """
    # Build initial message to return.
    message = f"Rolling {num_d20}d20 \n"
    if num_d20 > 5:
        message += "Wow, that's a lot of dice. Did you specify the number of dice to roll? \n"

    if tn:
        complication_range = "20" if complication == 20 else f"{complication}-20"
        tagged_skill = f"You are rolling a tagged skill at level {tagged_skill_level}" if tagged_skill_level else ""

        message += (f"The target number is {tn} \n"
                    f"The complication range is {complication_range} \n"
                    f"{tagged_skill} \n\n")

    # Actually make the roll and add it to the message
    rolls = [random.randint(1, 20) for _r in range(num_d20)]
    r = ", ".join(str(r) for r in sorted(rolls))
    message += f"Results: **{r}** \n"

    # Check for successes, complications, and crit successes
    num_complications = 0
    num_ones = rolls.count(1)
    total_successes = 0

    message += f"Crit success! \n" if num_ones else ""

    # Count the number of values in the complication range
    for r in range(int(complication), 21):
        num_complications += rolls.count(r)

    # Successes can only be counted if we know the target number
    if tn:
        tn = int(tn)
        for r in rolls:
            # A 1 or value under the level of a tagged skill returns an additional success
            if r == 1 or r <= tagged_skill_level:
                total_successes += 2
            elif tagged_skill_level < r <= tn:
                total_successes += 1

        if total_successes:
            message += f"Total successes: {total_successes} \n"

    # Add the complication info at the end of the message since it's the bad news
    if num_complications:
        complication_msg = "a complication" if num_complications == 1 else f"{num_complications} complications"
        message += f"You've rolled {complication_msg}."

    await ctx.send(message)


@bot.command()
async def hitd20(ctx, handy=False):
    """
    Rolls a 1d20 and returns the hit location.

    :param handy: If true we return information for a Mr. Handy
    """
    roll_result = random.randint(1, 20)
    locations_dict = {
        "1-2": "the **HEAD**", "3-8": "the **TORSO**", "9-11": "the **LEFT ARM**", "12-14": "the **RIGHT ARM**",
        "15-17": "the **LEFT LEG**", "18-20": "the **RIGHT LEG**"
    }
    if handy:
        locations_dict = {
            "1-2": "the **OPTICS**", "3-8": "the **MAIN BODY**", "9-11": "**ARM 1**", "12-14": "**ARM 2**",
            "15-17": "**ARM 3**", "18-20": "the **THRUSTERS** "
        }

    if roll_result < 3:
        await ctx.send(f"{roll_result}!, the hit location is {locations_dict['1-2']}")
    elif roll_result in range(3, 9):
        await ctx.send(f"{roll_result}!, the hit location is {locations_dict['3-8']}")
    elif roll_result in range(9, 12):
        await ctx.send(f"{roll_result}!, the hit location is {locations_dict['9-11']}")
    elif roll_result in range(12, 15):
        await ctx.send(f"{roll_result}!, the hit location is {locations_dict['12-14']}")
    elif roll_result in range(15, 18):
        await ctx.send(f"{roll_result}!, the hit location is {locations_dict['15-17']}")
    else:
        await ctx.send(f"{roll_result}!, the hit location is {locations_dict['18-20']}")


@bot.command()
async def effectsd6(ctx, num_dice: int = None):
    """
    Rolls a number of d6 and returns the number of hits and number of effect triggers.

    :param num_dice: The number of d6 to roll
    """
    if not num_dice:
        await ctx.send("You need to specify a number of d6 to roll, for example `/effectsd6 5` will roll 5d6.")

    rolls = [random.randint(1, 6) for _r in range(num_dice + 1)]
    results = {"num_successes": 0, "num_effects": 0}

    # A "2" adds additional successes, a 5 or 6 adds effect triggers
    for roll in rolls:
        if roll == 1:
            results["num_successes"] += 1
        elif roll == 2:
            results["num_successes"] += 2
        elif roll >= 5:
            results["num_successes"] += 1
            results["num_effects"] += 1

    result = ", ".join(str(r) for r in sorted(rolls))

    message = (f"You rolled {result}; dealing **{results['num_successes']}** hits "
               f"and **{results['num_effects']}** effect triggers")
    await ctx.send(message)


@bot.command()
async def helpd20(ctx, cmd=None):
    """
    Help command for the bot.
    :param cmd: If included, the bot will return the help message for the specified command
    """
    # Default message, summarizes all the commands.
    if not cmd:
        help_text = ("This bot allows you to make rolls for 2d20 games, these are the existing commands \n"
                     "* `/rolld20`: Rolls a number of d20 and returns the results. Optional arguments: "
                     "`num_d20` `tn` `complication` `skill_level`. \n"
                     "* `/hitd20`: rolls 1d20 and returns the hit location. Returns the location for a Mr. Handy "
                     "if you include 'handy' as an argument \n"
                     "* `/effectsd6 x`: rolls xd6 and returns the number of successes and effect triggers \n\n "
                     "For information about a specific command, like the arguments needed, use `/helpd20 <command>`"
                     )
        await ctx.send(help_text)

    elif "roll" in cmd.lower():
        help_text = ("This is the most complicated command, sorry! \n "
                     "For `/rolld20`, this command requires that if you use one argument then you must specify "
                     "the value of every argument before it. So you can't roll with a target number without specifying "
                     "that you're rolling 2 dice. If you don't it will roll your target number worth of d20s \n"
                     "The default roll is just /rolld20. It will assume normal parameters and return the result "
                     "of a 2d20 roll \n\n "
                     "* **Argument 1**: The number of dice to roll. If you're rolling additional d20s, you can "
                     "indicate the number here. The default value is 2. \n"
                     "* **Argument 2**: Your target number. This is the number you need to roll under to succeed. If "
                     "it isn't included the bot won't tell you how many successes you've rolled. You must include the "
                     "number of dice to roll as a prior argument. The default value is None. \n"
                     "* **Argument 3**: The complication range. If you have a larger complication range, you can "
                     "indicate the low number here. You must include the number of dice to roll and the target number "
                     "as prior arguments. The default value is 20.\n"
                     "* **Argument 4**: The level of the skill if it is a tagged skill. This will count values below "
                     "the skill level as two successes. You must include all of the arguments to use this. The default "
                     "value is 0, which means the bot will ignore then argument \n\n"
                     "__Examples__: \n"
                     "`/rolld20` will roll 2d20 and return the results. It will indicate if you have a critical "
                     "success or a complication \n"
                     "`/rolld20 12` will roll 12d20. You need to include the number of dice, even if it's 2. \n"
                     "`/rolld20 2 12` will roll 2d20 and tell you how many successes you have and any complications \n"
                     "`/rolld20 2 12 19` will roll 2d20, and tell you the number of successes and complications. It "
                     "will count a complication for each roll of 19 or 20 \n"
                     "`/rolld20 2 12 20 11` will roll 2d20 and tell you the number of successes and complications. It "
                     "will count any roll equal to or under 11 as two successes. It will also tell you if you have a "
                     "complication"
                     )
        await ctx.send(help_text)

    elif "hit" in cmd.lower() or "location" in cmd.lower():
        await ctx.send(
            "`/hitd20` rolls 1d20 and returns where the target was hit. If you include the argument 'handy' it will "
            "use the Mr. Handy table instead."
        )

    elif "effect" in cmd.lower() or "damage" in cmd.lower() or "combat" in cmd.lower():
        await ctx.send(
            "`/effectsd6` takes one argument- the number of dice (x) to roll. It rolls xd6 and counts the number of "
            "hits and effect triggers."
        )

    # If a command doesn't exist let the user know and list the existing commands
    else:
        bot_commands = ", ".join([x.name for x in bot.commands])
        await ctx.send(f"No command named `{cmd.lower()}`. Try one of these: {bot_commands}")


load_dotenv()
bot.run(os.getenv("DISCORD_2D20_TOKEN"))
