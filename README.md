# Analysis

An effective tool for identifying automated accounts (bots) in Telegram groups by analyzing user behavior patterns.

*Written by researcher tiivik*

## 📋 Overview

This Python-based tool analyzes user behavior in Telegram groups to estimate the likelihood of users being bots. It assigns a "bot score" to each user based on multiple factors including account age, message frequency, activity patterns, content diversity, and profile completeness.

## ✨ Features

- Comprehensive user behavior analysis using multiple detection criteria
- Visual representation of results through charts
- Data export to CSV for further analysis
- User classification into High, Medium, and Low risk categories
- Simple interface for entering group information

## 🛠️ Technical Requirements

- Python 3.6+
- Telethon (Telegram client library)
- Matplotlib (for visualization)
- NumPy (for numerical calculations)
- Pandas (for data management)

## 📥 Installation

1. Clone this repository:
2. git clone https://github.com/tiivikofficial/Analysis_group.git
3. 3. Install dependencies:
   4. 4. Obtain Telegram API credentials:
- Visit [my.telegram.org](https://my.telegram.org)
- Log in with your phone number
- Go to 'API development tools'
- Create a new application
- Note your API ID and API Hash
- 

    Enter the target Telegram group username when prompted.

    View the results in the generated charts and check the output CSV file.

📊 How It Works

The tool calculates a bot score (0-100) for each user based on these factors:

    Account Age: New accounts (< 30 days): 30 points, 30-90 days: 15 points
    Message Frequency: > 100 msgs/day: 25 points, > 50 msgs/day: 15 points
    Temporal Regularity: Regularity > 0.8: 20 points
    Content Diversity: Diversity < 0.3: 20 points
    Profile Completeness: No profile picture: 10 points, No bio: 5 points

Risk categories:

    High Risk (Likely bot): Score > 70
    Medium Risk: Score 40-70
    Low Risk (Likely human): Score < 40

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
