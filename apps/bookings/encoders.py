import json
from datetime import date, datetime


class DateJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()  # Convert date/datetime to ISO format
        return super().default(obj)
