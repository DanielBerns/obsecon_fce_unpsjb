from typing import Dict
from pathlib import Path
import subprocess
import logging

from components.core.text_generator import TextGenerator

# https://www.adminschoice.com/crontab-quick-reference

class UpdateCrontabException(Exception):
    pass

class Crontab:
    def __init__(self):
        self._text = TextGenerator()

    @property
    def text(self) -> TextGenerator:
        return self._text
    
    def check_command(self, command: str) -> str:
        item = Path(command).expanduser()
        if item.exists():
            return str(item)
        raise UpdateCrontabException(f"command doesn't exists: {str(item):s}")
    
    def check_minute(self, minute: str) -> str:
        if minute:
            if minute == '*':
                return minute
            try:
                if 0 <= int(minute) < 60:
                    return minute
                else:
                    UpdateCrontabException(f"invalid minute range: {minute:s}")
            except ValueError:
                raise UpdateCrontabException(f"invalid minute value: {minute:s}")
        else:
            raise UpdateCrontabException(f"invalid minute length")            

    def check_hour(self, hour: str) -> str:
        if hour:
            if hour == '*':
                return hour
            try:
                if 0 <= int(hour) <= 23:
                    return hour
                else:
                    UpdateCrontabException(f"invalid hour range: {hour:s}")
            except ValueError:
                raise UpdateCrontabException(f"invalid hour value: {hour:s}")
        else:
            raise UpdateCrontabException("invalid hour length")            

    def check_day_of_month(self, day_of_month: str) -> str:
        if day_of_month:
            if day_of_month == '*':
                return day_of_month
            try:
                if 1 <= int(day_of_month) <= 31:
                    return day_of_month
                else:
                    UpdateCrontabException(
                        f"invalid day_of_month range: {day_of_month:s}")
            except ValueError:
                raise UpdateCrontabException(
                    f"invalid day_of_month value: {day_of_month:s}")
        else:
            raise UpdateCrontabException("invalid day_of_month length")            

    def check_month(self, month: str) -> str:
        if month:
            if month == '*':
                return month
            try:
                if 1 <= int(month) <= 12:
                    return month
                else:
                    UpdateCrontabException(
                        f"invalid month range: {month:s}")
            except ValueError:
                raise UpdateCrontabException(
                    f"invalid month value: {month:s}")
        else:
            raise UpdateCrontabException("invalid month length")            

    def check_day_of_week(self, day_of_week: str) -> str:
        if day_of_week:
            if day_of_week == '*':
                return day_of_week
            try:
                if 0 <= int(day_of_week) <= 6:
                    return day_of_month
                else:
                    UpdateCrontabException(
                        f"invalid day_of_week range: {day_of_week:s}")
            except ValueError:
                raise UpdateCrontabException(
                    f"invalid day_of_month value: {day_of_week:s}")
        else:
            raise UpdateCrontabException("invalid day_of_week length")            
                
    def add(self, 
            key: str, 
            command: str, 
            minute: str,
            hour: str,
            day_of_month: str,
            month: str,
            day_of_week: str) -> None:
        try:
            _command = self.check_command(command)
            _minute = self.check_minute(minute)
            _hour = self.check_hour(hour)
            _day_of_month = self.check_day_of_month(day_of_month)
            _month = self.check_month(month)
            _day_of_week = self.check_day_of_week(day_of_week)
        except UpdateCrontabException as message:
            logging.info(f"{str(message):s}")
            raise UpdateCrontabException(
                " ".join(("Erroneous parameters:",
                          command, 
                          minute, 
                          hour, 
                          day_of_month, 
                          month, 
                          day_of_week)))
        else:
            line = " ".join(
                (_minute,
                 _hour,
                 _day_of_month,
                 _month,
                 _day_of_week,
                 _command))
            self.text.add(key, line)
          
    def remove(self, key: str) -> None:
        self.text.remove(key)
    
    def content(self):
        return self.text.content()
    
    def update(crontab_txt: Path) -> None:
        with open(crontab_txt, "w") as target:
             target.write(self.content())
        cp = subprocess.run(["crontab", crontab_txt])
        if cp.returncode:
            logging.info(f"update_crontab returncode {cp.returncode:d}")
