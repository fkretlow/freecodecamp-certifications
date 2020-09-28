#include <cctype>
#include <iostream>
#include <sstream>
#include <string>


class Time {
    public:
        Time(unsigned _minutes) : minutes(_minutes) { }
        Time(const std::string& src);
        Time(const Time& src) : minutes(src.minutes) { }

        Time operator+(const Time &rhs) const;

        std::string as_string() const;
        unsigned get_minutes() const { return minutes; }
        unsigned get_hours() const { return minutes / 60; }

    private:
        unsigned minutes { 0 };
};


Time::Time(const std::string& src) {
    std::string::size_type start, end;
    for (start = 0, end = 0; isdigit(src[end]); ++end) ;
    unsigned hours = std::stoul(src.substr(start, end));
    if (src.size() > 5 && src.substr(6, 8) == "PM") hours += 12;

    for (start = ++end; isdigit(src[end]); ++end) ;
    minutes = std::stoi(src.substr(start, end)) + 60 * hours;
}

Time Time::operator+(const Time &rhs) const {
    return Time(this->minutes + rhs.minutes);
}

std::string Time::as_string() const {
    unsigned hours = get_hours();
    unsigned _minutes = minutes - hours * 60;
    std::ostringstream out;
    if (hours >= 12) {
        if (hours > 12) hours -= 12;
        out << hours << ":" << _minutes << " PM";
    } else {
        if (hours == 0) hours = 12;
        out << hours << ":" << _minutes << " AM";
    }
    return out.str();
}


std::string add_time(const std::string& start,
                     const std::string& duration)
{
    return std::string("Not implemented.");
}


int main(int argc, char *argv[])
{
    std::string start { argv[1] };
    std::string end { argv[2] };

    const Time result(Time(start) + Time(end));
    std::cout << result.as_string() << std::endl;
    return 0;
}
