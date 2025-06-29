# How to Add Your Discord Bot to a Server

## Step 1: Create a Discord Application & Bot

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Sign in with your Discord account

2. **Create New Application**
   - Click "New Application" button
   - Give your bot a name (e.g., "YouTube Music Bot")
   - Click "Create"

3. **Create the Bot**
   - In the left sidebar, click "Bot"
   - Click "Add Bot" button
   - Confirm by clicking "Yes, do it!"

4. **Configure Bot Settings**
   - **Username**: Change if desired
   - **Icon**: Upload a profile picture (optional)
   - **Public Bot**: Toggle OFF if you only want to add it to your servers
   - **Requires OAuth2 Code Grant**: Keep this OFF
   - **Privileged Gateway Intents**:
     - ✅ Enable "Message Content Intent" (REQUIRED for commands to work)
     - ✅ Enable "Server Members Intent" (optional)
     - ✅ Enable "Presence Intent" (optional)

5. **Copy Bot Token**
   - Under "Token" section, click "Copy"
   - **IMPORTANT**: Keep this token secret! Never share it publicly.

## Step 2: Generate Bot Invite Link

1. **Go to OAuth2 → URL Generator**
   - In the left sidebar, click "OAuth2"
   - Then click "URL Generator"

2. **Select Scopes**
   - ✅ Check "bot"
   - ✅ Check "applications.commands" (for slash commands, if you want them later)

3. **Select Bot Permissions**
   Required permissions for your music bot:
   - ✅ **General Permissions**:
     - Read Messages/View Channels
     - Send Messages
     - Send Messages in Threads
     - Embed Links
     - Attach Files
     - Read Message History
     - Use External Emojis
   
   - ✅ **Voice Permissions**:
     - Connect
     - Speak
     - Use Voice Activity
     - Priority Speaker (optional)

4. **Copy Generated URL**
   - Copy the generated URL at the bottom
   - This is your bot invite link!

## Step 3: Invite Bot to Your Server

1. **Open the Invite Link**
   - Paste the copied URL in your browser
   - Or click the link if you have it

2. **Select Server**
   - Choose the server you want to add the bot to
   - You must have "Manage Server" permission

3. **Authorize Bot**
   - Review the permissions
   - Click "Authorize"
   - Complete any CAPTCHA if prompted

## Step 4: Set Up Bot Token

**Windows PowerShell:**
```powershell
$env:DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
```

**Windows Command Prompt:**
```cmd
set DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

**For Permanent Setup:**
1. Right-click "This PC" → Properties
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `DISCORD_BOT_TOKEN`
6. Variable value: Your bot token
7. Click OK

## Step 5: Run Your Bot

1. **Navigate to bot directory:**
   ```powershell
   cd "C:\Users\Administrator\Desktop\discord bot"
   ```

2. **Run the bot:**
   ```powershell
   "C:/Users/Administrator/Desktop/discord bot/.venv/Scripts/python.exe" bot.py
   ```
   
   Or double-click `run_bot.bat`

3. **Verify bot is online:**
   - You should see: "Bot has connected to Discord!"
   - The bot should appear online in your Discord server

## Step 6: Test the Bot

In your Discord server, try these commands:

1. **Join a voice channel** first
2. **Test basic commands:**
   ```
   !help
   !join
   !play Never Gonna Give You Up
   !pause
   !resume
   !volume 50
   !stop
   !leave
   ```

## Troubleshooting

### Bot appears offline:
- Check if the bot token is correct
- Ensure the bot is running (terminal should show connection message)
- Verify internet connection

### Commands not working:
- Make sure "Message Content Intent" is enabled in Discord Developer Portal
- Check if bot has proper permissions in the channel
- Verify the command prefix is `!`

### Audio not playing:
- Install FFmpeg and add to PATH
- Join a voice channel before using `!play`
- Check if bot has voice permissions

### Permission errors:
- Re-invite the bot with correct permissions
- Check channel-specific permissions
- Ensure bot role is high enough in server hierarchy

## Security Notes

- ⚠️ **Never share your bot token publicly**
- ⚠️ **Don't commit tokens to Git repositories**
- ⚠️ **Regenerate token if accidentally exposed**
- ✅ **Use environment variables for tokens**
- ✅ **Keep your bot code secure**

## Next Steps

Once your bot is working:
- Customize the command prefix if desired
- Add more features like music queues
- Set up logging for debugging
- Consider hosting on a VPS for 24/7 uptime
