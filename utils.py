from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
    from pytz import timezone as ZoneInfo  # For older Python versions using pytz

def get_local_time():
    try:
        # Python 3.9+ zoneinfo version
        return datetime.now(ZoneInfo("Asia/Kolkata"))
    except:
        # Fallback for older versions using pytz
        return datetime.now(ZoneInfo("Asia/Kolkata"))