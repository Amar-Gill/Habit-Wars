# Habit-Wars

Habit tracking with a competitive twist.

Deployed to Heroku at:

https://habitwars.herokuapp.com/


## How to play:

1) Register with username and password. 

2) Challenge a friend to a Habit War by selecting 'New Game' (friend must have a Habit Wars account).

3) Select up to three habits and the weekly frequency you want to commit to. Preferably this is agreed upon with the friend to make it a fair competition.

4) Over the course of each week (beginning Sunday midnight - first week is shorter if the game started mid-week) complete your habits and log your progress in the current game page. A RabbitMQ task runner is used to track the active round for each Habit War a user has active. A user can only ever log the completed habit for the presently active battle round.

5) Each time a habit is logged - you must upload a selfie as evidence. Your opponent needs to log in an verify that you completed the habit. A notification in the current game page will alert the user to perform the verification. If they forget, make sure to remind them. This is strictly a cheating prevention mechanism. Hold each other accountable! (AWS STORAGE IS DISABLED NO PHOTO STORAGE CAPABILITIES ARE PRESENTLY ACTIVE)

6) At end of each week, battle round can be played under battle history page for each active Habit War you have.

7) Depending on if you achieved your targets or not, a user can earn up to three dice rolls used to power up your fighter for the battle round.

8) By completing all of your habits, you are in a better position to win the battle round at the end of each week. This creates the incentive to stick with your habits.

## Battle Round

This is where the real fun is. Roll up to three dice to power up your stats.

Base Fighter Stats

### ATTACK = 10
{This is how much damage you hit for. Each power up point gives you +10 more attack.}

### HITPOINTS = 150
{How much damage your fighter can take before losing. Each power up point gives you +10 hitpoints.}

### LUCK = 5
{The percentage odds of doing a 'Deadly Strike' which is double the damage you normally do. Each power up point gives you +5 luck.}

## Rolling Initiative

Once a user has submitted their power ups for that week, there is one final roll to do which decides who will go first. A higher initiative roll will determine which fighter attacks first. This can turn the tide of battle when each fighter's stats are evenly matched.