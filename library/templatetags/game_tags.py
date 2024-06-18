import time
from datetime import datetime
from django import template
# from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter()
def format_date(date_obj):
    d = date_obj.strftime('%Y-%m-%d')
    return d

@register.filter()
def display_playtime(hours):
    """Convert play time decimal to human-readable string.

    Args:
        hours (decimal): No. of hours played

    Returns:
        str: Display play time in hours or minutes
    """
    if hours < 1:
        time = round(hours * 60)
        display = str(time) + ' minutes'
    else:
        time = round(hours)
        display = str(time) + ' hours'
    return display


@register.filter()
def display_time_elapsed(timestamp):
    """Convert time elapsed from UNIX timestamp to human-readable string.

    Args:
        timestamp (int): UNIX timestamp

    Returns:
        str: Time elapsed
    """
    now = round(time.time())
    time_elapsed = now - timestamp
    # Check if `time_elapsed` is within the last minute
    if time_elapsed < 60:
        print(now, timestamp, time_elapsed)
        display_str = 'Less than a minute ago'
    # Check if `time_elapsed` is within the last hour
    elif time_elapsed < 60 * 60:
        minutes = round(time_elapsed / 60)
        if minutes == 1:
            display_str = 'A minute ago'
        else:
            display_str = str(minutes) + ' minutes ago'
    # Check if `time_elapsed` is within the last day
    elif time_elapsed < 60 * 60 * 24:
        hours = round(time_elapsed / (60 * 60))
        if hours == 1:
            display_str = 'An hour ago'
        else:
            display_str = str(hours) + ' hours ago'
    # Check if `time_elapsed` is within the last month
    elif time_elapsed < 60 * 60 * 24 * 30:
        days = round(time_elapsed / (60 * 60 * 24))
        if days == 1:
            display_str = 'Yesterday'
        else:
            display_str = str(days) + ' days ago'
    # Check if `time_elapsed` is within the last year
    elif time_elapsed < 60 * 60 * 24 * 30 * 12:
        months = round(time_elapsed / (60 * 60 * 24 * 30))
        if months == 1:
            display_str = 'A month ago'
        else:
            display_str = str(months) + ' months ago'
    # Check if `time_elapsed` is more than a year
    elif time_elapsed > 60 * 60 * 24 * 30 * 12:
        years = round(time_elapsed / (60 * 60 * 24 * 30 * 12))
        if years == 1:
            display_str = 'A year ago'
        else:
            display_str = str(years) + ' years ago'
    return display_str


@register.filter()
def display_timestamp(timestamp):
    """Convert UNIX timestamp to datetime format.

    Args:
        timestamp (int): UNIX timestamp

    Returns:
        datetime: Converted datetime object
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt