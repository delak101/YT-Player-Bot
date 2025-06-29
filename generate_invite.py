#!/usr/bin/env python3
"""
Bot Invite Link Generator
This script helps you generate the correct invite link for your Discord bot.
"""

def generate_invite_link():
    print("🤖 Discord Bot Invite Link Generator")
    print("=" * 40)
    
    print("\nFirst, you need your bot's Client ID from the Discord Developer Portal:")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Select your application")
    print("3. Go to 'General Information'")
    print("4. Copy the 'Application ID' (also called Client ID)")
    
    client_id = input("\nEnter your bot's Client ID: ").strip()
    
    if not client_id or not client_id.isdigit():
        print("❌ Invalid Client ID. Please enter a valid numeric ID.")
        return
    
    # Required permissions for the music bot
    permissions = {
        'View Channels': 1024,
        'Send Messages': 2048,
        'Embed Links': 16384,
        'Attach Files': 32768,
        'Read Message History': 65536,
        'Use External Emojis': 262144,
        'Connect': 1048576,
        'Speak': 2097152,
        'Use Voice Activity': 33554432,
    }
    
    # Calculate total permissions value
    total_permissions = sum(permissions.values())
    
    # Generate invite link
    base_url = "https://discord.com/api/oauth2/authorize"
    invite_link = f"{base_url}?client_id={client_id}&permissions={total_permissions}&scope=bot"
    
    print(f"\n✅ Your bot invite link:")
    print(f"🔗 {invite_link}")
    
    print(f"\n📋 Permissions included:")
    for perm_name in permissions.keys():
        print(f"   ✅ {perm_name}")
    
    print(f"\n🚀 How to use this link:")
    print(f"1. Copy the link above")
    print(f"2. Paste it in your browser")
    print(f"3. Select the Discord server you want to add the bot to")
    print(f"4. Click 'Authorize'")
    print(f"5. Your bot will be added to the server!")
    
    # Save to file for easy access
    try:
        with open("bot_invite_link.txt", "w") as f:
            f.write(f"Discord Bot Invite Link\n")
            f.write(f"=" * 25 + "\n")
            f.write(f"Client ID: {client_id}\n")
            f.write(f"Invite Link: {invite_link}\n")
            f.write(f"\nPermissions:\n")
            for perm_name in permissions.keys():
                f.write(f"- {perm_name}\n")
        
        print(f"\n💾 Invite link saved to 'bot_invite_link.txt'")
        
    except Exception as e:
        print(f"\n⚠️  Could not save to file: {e}")

if __name__ == "__main__":
    generate_invite_link()
