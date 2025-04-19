from dark_genealogy import write_genealogy

"""
Do it yourself even if you don't know anything about programming!
Instructions are provided as comments (lines starting with #).
All you need to do other than following these pretty simple instructions
is to be able to run a Python program. This might be difficult for someone with no technical background,
but there are plenty of resources online explaining it. You need to install Python and either run this file
using an IDE like VScode or run it from the terminal by typing in "python3 custom_genealogy.py". If that doesn't
make sense, Google/Bing/Duckduckgo is your friend.
"""

# Here's the list of relationships. Edit freely to experiment
# For example: to see what the ancestry of a hypothetical
# child of Magnus and Franziska named Jimbob would be, add the following three lines to the bottom:
  # ('Ulrich','Katharina','Magnus'),
  # ('Charlotte','Peter','Franziska'),
  # ('Magnus','Franziska','Jimbob)
# Make sure you put them before the ']' character!
FAMILIES = [
    ('Egon', 'Doris', 'Claudia'),
    ('Claudia', 'Bernd', 'Regina'),
    ('Regina', 'Alexander', 'Bartosz'),
    ('Egon', 'Hannah', 'Silja'),
    ('Bartosz', 'Silja', 'Noah'),
    ('Bartosz', 'Silja', 'Agnes'),
    ('Noah', 'Elizabeth', 'Charlotte'),
    ('Charlotte', 'Peter', 'Elizabeth'),
    ('Tronte', 'Jana', 'Ulrich'),
    ('Ulrich', 'Katharina', 'Martha'),
    ('Ulrich', 'Katharina', 'Mikkel'),
    ('Hannah', 'Mikkel', 'Jonas'),
    ('Jonas', 'Martha', 'Unknown'),
    ('Agnes', 'Unknown', 'Tronte'),
]

# replace the word False with True if you want the "full" genealogy, i.e. showing what percentage of every ancestor someone is
FULL = False

# write the name of the file you want to write to here. Make sure to leave the single quotes and the .txt extension
FILENAME = 'genealogy.txt'

# If you want your file to begin with a description, write it between the single quotes. Type \n for a linebreak.
DESCRIPTION = ''

write_genealogy(FAMILIES,FILENAME,full=FULL,description=DESCRIPTION)