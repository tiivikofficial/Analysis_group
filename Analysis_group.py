# Telegram Bot Analyzer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from telethon import TelegramClient
from datetime import datetime
import asyncio

# Get these from my.telegram.org
api_id = '1231026'
api_hash = 'deeb4e706acf0ce2f11b7f3751ecf260'
phone = '+989021712197'

# Calculate bot likelihood score
def calculate_bot_score(user_data):
    score = 0
    
    # Check account age (newer accounts are more suspicious)
    if user_data['account_age_days'] < 30:
        score += 30
    elif user_data['account_age_days'] < 90:
        score += 15
    
    # Check number of messages (high message frequency is suspicious)
    if user_data['msgs_per_day'] > 100:
        score += 25
    elif user_data['msgs_per_day'] > 50:
        score += 15
    
    # Check time pattern regularity (very regular timing is suspicious)
    if user_data['time_regularity'] > 0.8:
        score += 20
    
    # Check content diversity (low diversity is suspicious)
    if user_data['content_diversity'] < 0.3:
        score += 20
    
    # Check profile completeness (incomplete profiles are suspicious)
    if not user_data['has_profile_pic']:
        score += 10
    if not user_data['has_bio']:
        score += 5
    
    return min(score, 100)  # Maximum 100

async def analyze_group(group_username):
    # Connect to Telegram
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone)
    print("Client created")
    
    # Get group info
    group_entity = await client.get_entity(group_username)
    
    # Get all group members
    participants = await client.get_participants(group_entity)
    print(f"Found {len(participants)} users")
    
    # Get recent messages
    messages = await client.get_messages(group_entity, limit=1000)
    
    # Group messages by user
    user_messages = {}
    for msg in messages:
        if msg.sender_id not in user_messages:
            user_messages[msg.sender_id] = []
        user_messages[msg.sender_id].append(msg)
    
    # Analyze users
    user_data = []
    for user in participants:
        user_id = user.id
        
        # Get user messages
        user_msgs = user_messages.get(user_id, [])
        
        # Calculate features
        # Fixed: User object doesn't have 'date' attribute, use a default value for account age
        # We'll try to get the first message date as an approximation
        first_message_date = None
        if user_msgs:
            message_dates = [msg.date for msg in user_msgs]
            if message_dates:
                first_message_date = min(message_dates)
        
        if first_message_date:
            account_age = datetime.now() - first_message_date.replace(tzinfo=None)
            account_age_days = account_age.days
        else:
            # Default to 365 days if we can't determine age
            account_age_days = 365
            
        msgs_count = len(user_msgs)
        
        # Calculate messages per day
        if account_age_days > 0:
            msgs_per_day = msgs_count / account_age_days
        else:
            msgs_per_day = msgs_count
        
        # Calculate time regularity
        time_regularity = 0
        if len(user_msgs) > 5:
            msg_times = [msg.date for msg in user_msgs]
            msg_times.sort()
            time_diffs = [(msg_times[i] - msg_times[i-1]).total_seconds() 
                         for i in range(1, len(msg_times))]
            if time_diffs:
                time_regularity = 1 - min(1, np.std(time_diffs) / (np.mean(time_diffs) + 0.001))
        
        # Calculate content diversity
        content_diversity = 0
        all_words = []
        for msg in user_msgs:
            if msg.text:
                all_words.extend(msg.text.lower().split())
        
        if all_words:
            content_diversity = len(set(all_words)) / len(all_words)
        
        # Profile completeness
        has_profile_pic = user.photo is not None
        has_bio = hasattr(user, 'about') and user.about is not None and user.about != ""
        
        # Store user data
        user_data.append({
            'user_id': user_id,
            'username': user.username or f"User_{user_id}",
            'account_age_days': account_age_days,
            'msgs_count': msgs_count,
            'msgs_per_day': msgs_per_day,
            'time_regularity': time_regularity,
            'content_diversity': content_diversity,
            'has_profile_pic': has_profile_pic,
            'has_bio': has_bio
        })
    
    # Calculate bot score
    for user in user_data:
        user['bot_score'] = calculate_bot_score(user)
    
    await client.disconnect()
    return user_data

def visualize_results(user_data):
    # Convert to DataFrame
    df = pd.DataFrame(user_data)
    
    # Sort by bot score
    df = df.sort_values('bot_score', ascending=False)
    
    # Limit to top 20 users for better visibility
    if len(df) > 20:
        print(f"Chart showing top 20 of {len(df)} users (all results in CSV file)")
        df_chart = df.head(20).copy()
    else:
        df_chart = df.copy()
    
    # Truncate long usernames
    df_chart['display_name'] = df_chart['username'].apply(lambda x: (x[:10] + '...') if len(x) > 10 else x)
    
    # Create chart
    plt.figure(figsize=(16, 10))
    
    # Plot bot scores
    colors = ['red' if score > 70 else 'orange' if score > 40 else 'green' for score in df_chart['bot_score']]
    bars = plt.bar(df_chart['display_name'], df_chart['bot_score'], color=colors)
    
    # Add the values on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    # Add horizontal lines for risk levels
    plt.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='High Risk')
    plt.axhline(y=40, color='orange', linestyle='--', alpha=0.7, label='Medium Risk')
    
    plt.title('Telegram Group Bot Analysis', fontsize=16)
    plt.xlabel('Users', fontsize=12)
    plt.ylabel('Bot Score (0-100)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.ylim(0, 105)  # Leave room for text above bars
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    # Save chart
    plt.savefig('telegram_bot_analysis.png', dpi=300)
    
    # For a larger version, just increase the DPI (removed the wrong figsize parameter)
    plt.savefig('telegram_bot_analysis_large.png', dpi=600)
    
    # Save detailed info
    df.to_csv('telegram_bot_analysis.csv', index=False)
    print(f"Results saved to telegram_bot_analysis.png and telegram_bot_analysis.csv")
    
    # Create a summary chart for bot risk levels
    plt.figure(figsize=(10, 6))
    risk_counts = [
        len(df[df['bot_score'] > 70]),    # High risk
        len(df[(df['bot_score'] > 40) & (df['bot_score'] <= 70)]),  # Medium risk
        len(df[df['bot_score'] <= 40])    # Low risk
    ]
    risk_labels = ['High Risk\n(Likely Bots)', 'Medium Risk', 'Low Risk\n(Likely Humans)']
    risk_colors = ['red', 'orange', 'green']
    
    plt.bar(risk_labels, risk_counts, color=risk_colors)
    plt.title('Bot Risk Distribution', fontsize=16)
    plt.ylabel('Number of Users', fontsize=12)
    
    # Add count labels on the bars
    for i, count in enumerate(risk_counts):
        plt.text(i, count + 0.5, str(count), ha='center', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('telegram_bot_risk_summary.png', dpi=300)
    print(f"Summary chart saved to telegram_bot_risk_summary.png")

# Main function
async def main():
    print("Starting Telegram bot analysis...")
    
    # Get group username from user
    group_username = input("Enter the Telegram group username (without @): ")
    
    # Add @ if not provided
    if not group_username.startswith('@'):
        group_username = '@' + group_username
    
    user_data = await analyze_group(group_username)
    
    # Show summary
    high_risk = len([u for u in user_data if u['bot_score'] > 70])
    medium_risk = len([u for u in user_data if 40 < u['bot_score'] <= 70])
    low_risk = len([u for u in user_data if u['bot_score'] <= 40])
    
    print(f"Analysis complete. Found {len(user_data)} users:")
    print(f" - High risk (likely bots): {high_risk}")
    print(f" - Medium risk: {medium_risk}")
    print(f" - Low risk (likely humans): {low_risk}")
    
    # Draw chart
    visualize_results(user_data)

# Run the program
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
