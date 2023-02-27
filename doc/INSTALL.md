<h3>Install</h3>

- 1 - Download or clone the repository to your local environment.
- 2 - **Celery:**
  - Install [Celery](https://pypi.org/project/celery/)
- 3 - **Redis:**
  - Install [Redis](https://redis.io/docs/getting-started/installation/)
- 3 - **Django:**
  - Install [Django](https://docs.djangoproject.com/en/4.1/topics/install/)
- 4 - Create a Discord Bot: [Create-Discord-App](https://discord.com/developers/applications)
  - Go to *Bot* and create new. (IMPORTANT: If the name of the application is already in use, you will have to change it to be able to create the bot.)
  - Go to the bot repository and create a new ".env" file with the format you found in the ".env-example" file.
  - Replace:
    - 'DATABASE_PATH': with the location of the repository on your pc. Example: "/home/user/Desktop/Bot_Courses_UM"
    - 'DISCORD_PREFIX': whatever prefix you want to use on Discord to communicate with the bot. Example: "!"
    - 'DISCORD_TOKEN': From the 'discord developers' page where you created the bot, copy your bot token. (IMPORTANT: do not share this token)
    - Save the changes made.
- 3 - Execute: ```
  sh install.sh```
- 4 - Execute: ```
  sh boot.sh```
