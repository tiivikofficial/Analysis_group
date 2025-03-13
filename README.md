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
2. git clone https://github.com/tiivik/Analysis.git cd Analysis
3. 3. Install dependencies:
   4. 4. Obtain Telegram API credentials:
- Visit [my.telegram.org](https://my.telegram.org)
- Log in with your phone number
- Go to 'API development tools'
- Create a new application
- Note your API ID and API Hash

## 💻 Usage

1. Edit the `config.py` file and enter your Telegram API credentials:
```python
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
Run the analyzer: python3 Analysis_group.py
