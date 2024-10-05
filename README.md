# 2D20 Roller for Discord
This discord bot allows a user to make rolls for the 2d20 system, hopefully simplifying some of the need to look 
at charts for hit locations and damage rolls. It can be invited to a server using [this link](https://discord.com/oauth2/authorize?client_id=1289984227273867397)  

This was designed while I played Modiphius's Fallout game, values for things like hit locations may vary in other 
systems. If there's other rolls you want this to make, either make a pull request or create an issue. 

## Commands
* `/helpd20`: This command will print out the help statements. It takes the optional argument of the command name. For
  example, `/helpd20 rolld20` will show how to use the roller.
* `/rolld20`: This command will roll 2d20 and return the results of the roll. If a one or twenty is rolled it will 
  state that as well. This command takes additional arguments. However, if you include an argument, you must also 
  define each of the arguments to the left (or above it if you're using this list as a reference), even if they don't 
  change from the default value.
  * Number of Dice: Default value is 2. This tells the bot how many dice to roll, which can change. To change the 
    number of dice your command would look like `/rolld20 3`
  * Target Number: Default value is None. If a target number (TN) is provided, the roller will count the number of 
    successes you roll. For instance, if you have a TN of 11 the command would be `/rolld20 2 11`. If you roll '1, 11', 
    it will return that you have three successes. If you roll '11, 20', it will return that you rolled 1 success with 
    one complication. This information will be returned for each subsequent argument.
  * Complication Range: Default value is 20. The complication range can change for a variety of reasons. If the 
    range is 19-20 with a TN of 12, your command would be `/rolld20 2 12 19` The roller will return one complication 
    and no successes on a roll of '14, 19'.
  * Tagged Skill Level: Default value is None. If the skill you are rolling is a tagged skill, the bot will increase
    the number of successes appropriately. On a roll with a TN of 12, complication range of 20-20, and tagged skill
    level of 3, your command would be `/rolld20 2 12 20 3` the bot will return two successes on a roll of '2, 15'.
* `/hitd20`: This command rolls 1d20 and returns the hit location. It takes one optional argument of 'handy' (so
  `/hitd20 handy`) to return the hits on a Mr. Handy instead.
* `/effectsd6`: This command rolls a number of d6 and returns a count of hits as well as the number of effect triggers.
  for example if I use `/effectsd6 5` and get the results '1, 2, 3, 3, 5', it will return that you had four successes and
  one effect trigger.

## Package Management
This project uses Poetry for package management.
