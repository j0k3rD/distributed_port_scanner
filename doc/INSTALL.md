<h3>Install</h3>

- 1 - Download or clone the repository to your local environment.
- 2 - **Celery:**
  - Install [Celery](https://pypi.org/project/celery/)
- 4 - Create a Discord Bot: [Create-Discord-App](https://discord.com/developers/applications)
  - Go to *Bot* and create new. (IMPORTANT: If the name of the application is already in use, you will have to change it to be able to create the bot.)
  - Go to the bot repository and create a new ".env" file with the format you found in the ".env-example" file.
  - Replace:
    - 'DATABASE_PATH': with the location of the repository on your pc. Example: "/home/user/Desktop/Bot_Courses_UM"
    - 'DISCORD_PREFIX': whatever prefix you want to use on Discord to communicate with the bot. Example: "!"
    - 'DISCORD_TOKEN': From the 'discord developers' page where you created the bot, copy your bot token. (IMPORTANT: do not share this token)
    - Save the changes made.
- Now on the 'discord developers' page, go to 'OAuth2' -> 'URL Generator' under 'Scopes' choose 'Bot' and under 'Bot Permissions' choose 'Administrator'.
Once this is done, copy the invitation link that will be generated at the bottom.
- Paste it into your browser and then choose the server you want to invite the bot to and click 'Continue'.
- 3 - Execute: ```
  sh install.sh```
- 4 - Execute: ```
  sh boot.sh```