from datetime import datetime as dt


def format_time(time_format_set):
    time_formatted = [str(i).zfill(2) for i in range(time_format_set)]
    return time_formatted


def get_time_difference(end_time, start_time):
    end_time = dt.strptime(end_time, "%H:%M:%S")
    start_time = dt.strptime(start_time, "%H:%M:%S")
    time_difference = end_time - start_time
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


def format_time_with_am_pm(hour, minute, second, use_am_pm):
    if use_am_pm:
        hour = int(hour)
        am_pm = "AM" if hour < 12 else "PM"
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12
        formatted_time = f"{hour}:{minute}:{second} {am_pm}"
    else:
        formatted_time = f"{hour}:{minute}:{second}"
    return formatted_time