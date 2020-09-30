#include <cctype>
#include <iomanip>
#include <iostream>
#include <regex>
#include <sstream>
#include <string>


class Time {
    friend std::ostream& operator<<(std::ostream&, const Time&);

    public:
        Time() = default;
        Time(unsigned m) : minutes(m) { }
        Time(const std::string&);
        Time(const Time&) = default;
        ~Time() = default;

        Time& operator=(const Time& rhs) = default;

        Time operator+(const Time& rhs) const;
        Time& operator+=(const Time& rhs);

        Time operator-(const Time& rhs) const;
        Time& operator-=(const Time& rhs);

        unsigned get_minutes() const { return minutes; }
        unsigned get_hours() const { return minutes / 60; }

    private:
        unsigned minutes { 0 };
};


Time::Time(const std::string& s) {
    std::regex re("(\\d{2}):(\\d{2})(?: (AM|PM))?");
    std::smatch m;
    std::regex_search(s, m, re);

    unsigned hours = static_cast<unsigned>(std::stoul(m[1].str()));
    if (m[3].matched && m[3].str() == "PM" && hours < 12) hours += 12;

    minutes = static_cast<unsigned>(std::stoul(m[2].str())) + hours * 60;
}

Time Time::operator+(const Time &rhs) const {
    return Time(this->minutes + rhs.minutes);
}

Time& Time::operator+=(const Time& rhs) {
    minutes += rhs.minutes;
    return *this;
}

Time Time::operator-(const Time &rhs) const {
    return Time(this->minutes - rhs.minutes);
}

Time& Time::operator-=(const Time& rhs) {
    minutes -= rhs.minutes;
    return *this;
}

std::ostream& operator<<(std::ostream& os, const Time& t) {
    unsigned hours = t.get_hours();
    unsigned minutes = t.minutes - hours * 60;
    hours %= 24;
    std::string sign = hours < 12 ? "AM" : "PM";
    if (hours > 12) hours -= 12;

    std::ios_base::fmtflags f { os.flags() };

    os << std::setfill('0') << std::right;
    os << std::setw(2) << hours
       << ":"
       << std::setw(2) << minutes
       << " " << sign;

    os.flags(f);

    return os;
}


int main(int argc, char *argv[])
{
    if (argc < 3) {
        std::cerr << "2 parameters required." << std::endl;
        return -1;
    }
    std::string start { argv[1] };
    std::string duration { argv[2] };

    Time t = Time(start) + Time(duration);
    std::cout << t << std::endl;

    return 0;
}
