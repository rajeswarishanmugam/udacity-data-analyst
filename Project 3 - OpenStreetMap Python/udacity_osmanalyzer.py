# Author: Rajeswari Shanmugam
# Udacity Project for OpenstreetMap Analysis
# Dec 27 2017
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict


chennai_data = "C:\\temp\\python\\chennai.osm"

# Function count_tags will take the OSM file as input and will iterate through the tags and return them
def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Key value pair to iterate through all regex combinations to filter out lower, lower_colon and problemchars
def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            k = tag.get('k')
            if lower.search(k):
                keys['lower'] += 1
            elif lower_colon.search(k):
                keys['lower_colon'] += 1
            elif problemchars.search(k):
                keys['problemchars'] += 1
            else:
                keys['other'] += 1
    return keys

# Function process_map will take the OSM file as input and will iterate through the tags to return the regex criteria
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


# Function process_map will take the OSM file as input and will iterate through the tags to return the count of users
def process_map_users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        for e in element:
            if 'uid' in e.attrib:
                users.add(e.attrib['uid'])
    return users


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Avenue", "Boulevard", "Commons", "Court", "Drive", "Lane", "Parkway",
            "Place", "Road", "Square", "Street", "Trail"]

mapping = {'Ave': 'Avenue',
           'Blvd': 'Boulevard',
           'Dr': 'Drive',
           'Ln': 'Lane',
           'Pkwy': 'Parkway',
           'Rd': 'Road',
           'Rd.': 'Road',
           'St': 'Street',
           'st': 'Street',
           'street': "Street",
           'Salai': 'Road',
           'salai': 'Road',
           'Ct': "Court",
           'Cir': "Circle",
           'Cr': "Court",
           'ave': 'Avenue',
           'Hwg': 'Highway',
           'Hwy': 'Highway',
           'Sq': "Square"}

# Audit function to run an audit against the street_types and street name
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# Utility function to check if a given element is a street_name
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Audit function that takes OSM file as input and runs through the street name analysis
def audit(osmfile):
    osm_file = open(osmfile, "r", encoding="utf8")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

# Utility function to update names
def update_name(name, mapping, regex):
    m = regex.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = re.sub(regex, mapping[street_type], name)

    return name

# Magic starts here :)

def main():
    print("Python OSM Analysis - Udacity - Rajeswari Shanmugam")
    print("===== Count of tags in OSM file =====");
    chennai_tags = count_tags(chennai_data)
    pprint.pprint(chennai_tags)
    print("===== Regex analysis for lower,lower_colon,other and problem chars of tags in OSM file =====");
    chennai_keys = process_map(chennai_data)
    pprint.pprint(chennai_keys)
    print("===== Process OSM file and count the users =====");
    users = process_map_users(chennai_data)
    print(len(users))
    print("===== Dictonory of all Chennai street types =====");
    chennai_street_types = audit(chennai_data)
    pprint.pprint(dict(chennai_street_types))
    print("===== Cleaned Data post updates, eg. changing of local names like Salai ==> Road etc. =====");
    for street_type, ways in chennai_street_types.items():
        for name in ways:
            better_name = update_name(name, mapping, street_type_re)
            print(name, "=>", better_name)

if __name__ == "__main__":
    main()