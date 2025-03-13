# Telegram API credentials
# Replace with your own values from https://my.telegram.org
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'

# Session name (will be stored as this filename + .session)
SESSION_NAME = 'analyzer_session'

# Analysis settings
MAX_MESSAGES = 1000  # Maximum number of messages to retrieve per group
ANALYSIS_PERIOD_DAYS = 30  # How many days of history to analyze
DOWNLOAD_DELAY = 2  # Delay between message batches to avoid rate limits

# Bot detection thresholds
HIGH_RISK_THRESHOLD = 70  # Score above which users are classified as high risk
MEDIUM_RISK_THRESHOLD = 40  # Score above which users are classified as medium risk

# Scoring weights (adjust to prioritize different factors)
WEIGHTS = {
    'account_age': 1.0,
    'message_frequency': 1.0,
    'temporal_regularity': 1.0,
    'content_diversity': 1.0,
    'profile_completeness': 1.0
}

# Output settings
RESULTS_FOLDER = 'results'
SAVE_CHARTS = True
SAVE_CSV = True
CSV_FILENAME = 'analysis_results.csv'

# Logging
DEBUG_MODE = False  # Set to True for verbose logging
LOG_FILE = 'analysis.log'
