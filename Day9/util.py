import re
import math
import os
import requests

# ==========================================================
# 🔐 Secure API Configuration (Environment Variable Based)
# ==========================================================

ABUSEIPDB_API_KEY = os.getenv("9888e5426bd7d97d5faef78841386b45b0aaaf68ace3cae77619c596fbdd4e68969febf68f6642d4")
ABUSE_SCORE_THRESHOLD = 50


def check_ip_reputation(ip_address):
    """Check IP reputation using AbuseIPDB API"""
    if not ABUSEIPDB_API_KEY:
        return False

    try:
        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {
            "Key": ABUSEIPDB_API_KEY,
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip_address,
            "maxAgeInDays": 90
        }

        response = requests.get(url, headers=headers, params=params, timeout=5)

        if response.status_code == 200:
            data = response.json()
            score = data["data"]["abuseConfidenceScore"]
            return score >= ABUSE_SCORE_THRESHOLD

    except Exception:
        return False

    return False


# ==========================================================
# 📧 Email Pattern Configuration
# ==========================================================

MAX_LENGTH = 30
MIN_LENGTH = 4
MAX_SPECIAL_CHARS = 3
HIGH_ENTROPY_THRESHOLD = 3.5
MAX_DIGIT_RATIO = 0.3
MAX_CONSECUTIVE_DIGITS = 4
MAX_SUBDOMAIN_DEPTH = 2

SUSPICIOUS_TLDS = {
    "xyz", "icu", "top", "loan", "win", "bid",
    "click", "monster", "tk", "ga", "ml", "cf", "gq"
}

KNOWN_SPAM_EMAILS = {
    "scammer123@gmail.com",
    "spam.bot@malicious.com",
    "prize.winner@suspicious.net"
}

DISPOSABLE_EMAIL_DOMAINS = [
    "tempmail.com", "mailinator.com", "10minutemail.com",
    "trashmail.com", "yopmail.com", "guerrillamail.com"
]

LOOKALIKE_DOMAINS = {
    "gmail.com": ["gmai1.com", "gmall.com", "gnail.com"],
    "paypal.com": ["paypa1.com", "paypaI.com"],
    "amazon.com": ["amaz0n.com", "arnazon.com"],
}

COMMON_KEYBOARD_PATTERNS = [
    "qwerty", "asdfgh", "zxcvbn",
    "12345", "123456", "abcdef",
    "aaaaaa", "111111"
]

SPAM_KEYWORDS = [
    "free", "winner", "prize", "urgent", "bitcoin", "crypto",
    "cash", "money", "lottery", "gift card", "claim",
    "verify", "account locked", "password reset",
    "invoice", "payment", "refund", "bonus",
    "earn daily", "work from home", "income",
    "congratulations", "limited offer", "offer",
    "discount", "deal", "gift", "giveaway", "iphone",
    "android", "samsung", "reward", "click here",
    "act now", "selected", "lucky", "jackpot",
    "won", "inheritance", "nigerian", "prince",
    "beneficiary", "unclaimed", "wire transfer",
    # Phishing / Social Engineering keywords
    "hacked", "security", "suspended", "deactivated",
    "deletion", "blocked", "unauthorized", "login now",
    "secure your", "confirm your", "update your",
    "restore", "recover", "unusual activity",
    "earn", "weekly", "daily income"
]

FINANCIAL_SCAM_PATTERNS = [
    r"earn.*daily",
    r"money.*home",
    r"get.*rich.*quick",
    r"\$[0-9]{3,}",
    r"investment.*scheme",
    r"tax.*refund",
    r"lottery.*winner"
]

URGENCY_PHRASES = [
    "act now",
    "within 24 hours",
    "final warning",
    "limited time",
    "immediately",
    "urgent response",
    "login now",
    "permanent deletion",
    "before permanent",
    "will be deleted",
    "will be suspended",
    "account will be",
    "secure your account",
    "verify your account"
]

SHORTENED_URL_DOMAINS = [
    "bit.ly", "tinyurl.com", "t.co",
    "goo.gl", "is.gd", "buff.ly"
]


# ==========================================================
# 🔎 Email Feature Checks
# ==========================================================

def check_syntax(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return 0 if re.match(regex, email) else 1


def check_length(email):
    try:
        local = email.split('@')[0]
        return 1 if len(local) < MIN_LENGTH or len(local) > MAX_LENGTH else 0
    except:
        return 0


def check_special_chars(email):
    try:
        local = email.split('@')[0]
        if re.search(r'[\._-]{2,}', local):
            return 1
        if len(re.findall(r'[^a-zA-Z0-9]', local)) > MAX_SPECIAL_CHARS:
            return 1
    except:
        pass
    return 0


def check_entropy(email):
    try:
        local = email.split('@')[0]
        if not local:
            return 0
        prob = [float(local.count(c)) / len(local) for c in set(local)]
        entropy = -sum([p * math.log(p, 2) for p in prob])
        return 1 if entropy > HIGH_ENTROPY_THRESHOLD else 0
    except:
        return 0


def check_digit_ratio(email):
    try:
        local = email.split('@')[0]
        digit_count = sum(c.isdigit() for c in local)
        return 1 if (digit_count / len(local)) > MAX_DIGIT_RATIO else 0
    except:
        return 0


def check_consecutive_digits(email):
    try:
        local = email.split('@')[0]
        return 1 if re.search(r'\d{' + str(MAX_CONSECUTIVE_DIGITS) + r',}', local) else 0
    except:
        return 0


def check_known_spam(email):
    return 1 if email in KNOWN_SPAM_EMAILS else 0


def check_disposable(email):
    try:
        domain = email.split('@')[1].lower()
        return 1 if domain in DISPOSABLE_EMAIL_DOMAINS else 0
    except:
        return 0


def check_lookalike(email):
    try:
        domain = email.split('@')[1].lower()
        for _, fakes in LOOKALIKE_DOMAINS.items():
            if domain in fakes:
                return 1
    except:
        pass
    return 0


def check_keyboard_pattern(email):
    try:
        local = email.split('@')[0].lower()
        for pattern in COMMON_KEYBOARD_PATTERNS:
            if pattern in local:
                return 1
    except:
        pass
    return 0


def check_suspicious_tld(email):
    try:
        tld = email.split('.')[-1].lower()
        return 1 if tld in SUSPICIOUS_TLDS else 0
    except:
        return 0


# ==========================================================
# 📨 Content-Based Checks
# ==========================================================

def check_spam_keywords(text):
    if not text:
        return 0
    text = text.lower()
    return 1 if any(word in text for word in SPAM_KEYWORDS) else 0


def check_financial_claims(text):
    if not text:
        return 0
    text = text.lower()
    for pattern in FINANCIAL_SCAM_PATTERNS:
        if re.search(pattern, text):
            return 1
    return 0


def check_urgency(text):
    if not text:
        return 0
    text = text.lower()
    return 1 if any(p in text for p in URGENCY_PHRASES) else 0


def check_shortened_urls(text):
    if not text:
        return 0
    text = text.lower()
    return 1 if any(domain in text for domain in SHORTENED_URL_DOMAINS) else 0


# ==========================================================
# 📧 Email Address Keyword Check (NEW)
# ==========================================================

def check_email_keywords(email):
    """Check if spam keywords appear in the email address itself"""
    if not email:
        return 0
    # Check full email (local + domain) for spam keywords
    email_lower = email.lower().replace('.', ' ').replace('-', ' ').replace('_', ' ')
    return 1 if any(word in email_lower for word in SPAM_KEYWORDS) else 0


# ==========================================================
# 🎯 Feature Extraction
# ==========================================================

def extract_features(email, subject="", body=""):

    combined = f"{email} {subject} {body}"

    return [
        check_syntax(email),
        check_length(email),
        check_special_chars(email),
        check_entropy(email),
        check_digit_ratio(email),
        check_consecutive_digits(email),
        check_known_spam(email),
        check_disposable(email),
        check_lookalike(email),
        check_keyboard_pattern(email),
        check_suspicious_tld(email),

        check_email_keywords(email),     # NEW: spam keywords in email address
        check_spam_keywords(subject),
        check_spam_keywords(body),
        check_financial_claims(combined),
        check_urgency(combined),
        check_shortened_urls(body)
    ]


def get_feature_names():
    return [
        "Invalid Syntax",
        "Abnormal Length",
        "Excessive Special Characters",
        "High Entropy",
        "High Digit Ratio",
        "Consecutive Digits",
        "Known Spam Email",
        "Disposable Email",
        "Lookalike Domain",
        "Keyboard Pattern",
        "Suspicious TLD",
        "Email Address Spam Keywords",
        "Subject Spam Keywords",
        "Body Spam Keywords",
        "Financial Scam Claims",
        "Urgent Phrasing",
        "Shortened URLs"
    ]
