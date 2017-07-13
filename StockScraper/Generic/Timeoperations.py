"""Stores functions related to datetime."""

import pytz
from datetime import datetime


class TimeOperate:
    # 1 day is equal to 86400000ms
    _1DAY = 86400000
    _datetime_zero_day_epoch = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

    @staticmethod
    def get_current_time():
        """Return current time according to host timezone.

        :return: datetime object.
        """
        return datetime.now()

    @staticmethod
    def get_current_time_utc():
        """Return current time in utc datetime.

        :return: datetime object.
        """
        return datetime.utcnow()

    @staticmethod
    def to_utc(date):
        """Convert date to utc.

        :param date: datetime object.
        :return: utc datetime object.
        """
        if isinstance(date, datetime):
            try:
                # for timezone aware objects
                return date.astimezone(pytz.utc)
            except ValueError:
                # replace timezone if naive date
                return date.replace(tzinfo=pytz.utc)
        raise TypeError('Provided object is not instance of datetime.')

    @staticmethod
    def datetime_to_epoch(date):
        """Convert date to unix epoch format

        :param date: datetime object.
        :return: string containing date in unix epoch format.
        """
        if isinstance(date, datetime):
            return date.timestamp()
        raise TypeError('Provided object is not instance of datetime.')

    @classmethod
    def days_in_epoch(cls, date):
        """Convert date to days passed in unix epoch format.

        :param date: datetime object.
        :return: days since the zero date in epoch format.
        """
        if isinstance(date, datetime):
            diff_date = cls.to_utc(date) - cls._datetime_zero_day_epoch
            return diff_date.days * cls._1DAY
        raise TypeError('Provided object is not instance of datetime.')
