from datetime import datetime, date
from decimal import Decimal
import simplejson as json


def epoch(tm, as_int=True):
    if tm is None:
        return None

    if isinstance(tm, date) and not isinstance(tm, datetime):
        tm = datetime(year=tm.year, month=tm.month, day=tm.day)

    offset = tm.utcoffset()
    out = (tm.replace(tzinfo=None) - datetime.utcfromtimestamp(0))
    if offset:
        out = out - offset
    out = Decimal(out.total_seconds()) if not as_int else int(out.total_seconds())

    return out


def chunk_it(seq, max_size=500):
    current = 0

    while current < len(seq):
        yield seq[current:(current + max_size)]
        current = current + max_size


def jsonify(dictionary, **kwargs):
    # we can't use the normal jsonify method because it doesn't like doubles
    def default(o):
        if hasattr(o, "to_dict"):
            return o.to_dict()
        elif hasattr(o, "serialize"):
            return o.serialize()
        elif isinstance(o, datetime):
            return epoch(o)
        elif isinstance(o, date):
            return epoch(o, as_int=True)
        elif isinstance(o, set):
            return list(o)
        return str(o)

    out = json.dumps(dictionary, default=default, use_decimal=True, ensure_ascii=False, **kwargs)
    return out
