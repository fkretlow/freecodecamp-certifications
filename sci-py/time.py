def divide_in_units(total, units):
    """
    All arguments are ints. For each unit, divide out as many as possible from total.
    Return a list of factors. Example: divide_in_units(28, (10, 5, 1)) -> [2, 1, 3].
    """
    result = []
    for unit in units:
        factor = int(total / unit)
        total -= factor * unit
        result.append(factor)
    if total: result.append(total)
    return result


class Time(object):
    def __init__(self, minutes=0):
        self._minutes = minutes

    @classmethod
    def from_string(cls, string):
        """Accepts a time string like '11:30 AM'."""
        parts = string.split()
        time = parts[0]
        hours, minutes = (int(x) for x in time.split(':'))
        if len(parts) == 2 and parts[1] == "PM":
            hours += 12
        return cls(60 * hours + minutes)

    def __repr__(self):
        return f"Time({self._minutes})"

    def as_string(self, style="12-hours"):
        days, hours, minutes = divide_in_units(self._minutes, (1440, 60, 1))
        s = ""

        if style == "12-hours":
            if hours > 11: apm = "PM"
            else: apm = "AM"
            hours %= 12
            if hours == 0: hours = 12
            s += f"{hours}:{minutes:0>2} {apm}"
        else:
            if hours == 0: hours = 12
            s += f"{hours}:{minutes:0>2}"

        return s

    def days(self):
        return int(self._minutes / 1440)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return self.__class__(self._minutes + other._minutes)


class Day(object):
    names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    def __init__(self, arg):
        if isinstance(arg, str):
            self._index = Day.names.index(arg.lower().capitalize())
        elif isinstance(arg, int):
            self._index = arg
        else:
            raise TypeError("Error: Can only construct Day from string or integer.")

    def __str__(self):
        return Day.names[self._index % 7]

    def advance(self, n):
        self._index += n



def add_time(start, duration, day=None):
    time = Time.from_string(start) + Time.from_string(duration)
    s = time.as_string()

    if day is not None:
        day = Day(day)
        day.advance(time.days())
        s += f", {day}"

    if time.days() == 1:
        s += " (next day)"
    elif time.days() > 1:
        s += f" ({time.days()} days later)"

    return s
