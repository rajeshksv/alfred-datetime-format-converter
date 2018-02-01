# -*- coding: utf-8 -*-

import alfred
import calendar
from delorean import utcnow, parse, epoch

def process(query_str):
    """ Entry point """
    value = parse_query_value(query_str)
    if value is not None:
        results = alfred_items_for_value(value)
        xml = alfred.xml(results) # compiles the XML answer
        alfred.write(xml) # writes the XML back to Alfred

def parse_query_value(query_str):
    """ Return value for the query string """
    try:
        query_str = str(query_str).strip('"\' ')
        if query_str == 'now':
            d = utcnow()
        else:
            # Parse datetime string or timestamp
            try:
                if (float(query_str) > 9999999999):
                    query_str = float(query_str)/1000
                d = epoch(float(query_str))
            except ValueError:
                d = parse(str(query_str))
    except (TypeError, ValueError):
        d = None
    return d

def alfred_items_for_value(value):
    """
    Given a delorean datetime object, return a list of
    alfred items for each of the results
    """

    index = 0
    results = []

    # First item as timestamp
    item_value = calendar.timegm(value.datetime.utctimetuple())
    results.append(alfred.Item(
        title=str(item_value),
        subtitle=u'UTC Timestamp',
        attributes={
            'uid': alfred.uid(index), 
            'arg': item_value,
        },
        icon='icon.png',
    ))
    index += 1

    item_value = value.datetime.strftime("%Y-%m-%d %H:%M:%S")
    results.append(alfred.Item(
        title=str(item_value),
        subtitle="UTC",
        attributes={
            'uid': alfred.uid(index), 
            'arg': item_value,
        },
    icon='icon.png',
    ))
    index += 1

    item_value = value.shift('Asia/Kolkata').datetime.strftime("%Y-%m-%d %H:%M:%S")
    results.append(alfred.Item(
        title=str(item_value),
        subtitle="IST",
        attributes={
            'uid': alfred.uid(index), 
            'arg': item_value,
        },
    icon='icon.png',
    ))
    index += 1

    return results

if __name__ == "__main__":
    try:
        query_str = alfred.args()[0]
    except IndexError:
        query_str = None
    process(query_str)
