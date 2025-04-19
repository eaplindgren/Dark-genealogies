import numpy as np

# default family tree
# Peter is considered an ancestor here because his ancestors didn't father anyone else
families = [
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

# If Tronte was Regina's father
# Regina, Bartosz, Noah, and Agnes are now bootstrapped
families_tronte = families.copy()
families_tronte.remove(('Claudia','Bernd','Regina'))
families_tronte.insert(1,('Claudia','Tronte','Regina'))

# If Bernd was Helge's father
# Peter's ancestry now included because now it's interesting
families_bernd = families.copy()
families_bernd.insert(0,('Bernd','Greta','Helge'))
families_bernd.insert(4,('Helge','Ulla','Peter'))

#alt-universe considered separately
families_copy = families.copy()
families_copy.remove(('Hannah','Mikkel','Jonas'))
families_copy.remove(('Agnes','Unknown','Tronte'))
families_alt = families + [tuple(['alt-'+person for person in family]) for family in families_copy]
families_alt.remove(('Jonas','Martha','Unknown'))
families_alt.remove(('alt-Jonas','alt-Martha','alt-Unknown'))
families_alt.append(('Jonas','alt-Martha','Unknown'))
families_alt.append(('alt-Agnes','Unknown','alt-Tronte'))

def compute_genealogy(families):
    '''
    Given a list of triples representing family relationships, calculates the genetic makeup
    of each person in terms of the individuals at the "leaves" of the family tree, whose parents
    are not included, and from whom everyone else is descended.
        Input: list of triples of the form (parent1, parent2, child) as strings.
        Output: dict of dicts, mapping each person to a dict mapping each of the ancestors of the family tree
        to their percentage of that person's genetic makeup
    '''
    genealogy = {}
    unique_people = list(dict.fromkeys([person for family in families for person in family]))
    n = len(unique_people)
    people_ids = dict(zip(unique_people, np.arange(n)))
    inv_people_ids = {k:v for (v,k) in people_ids.items()}

    genetic_matrix = np.zeros((n,n))
    for (parent1, parent2, child) in families:
        p1 = people_ids[parent1]
        p2 = people_ids[parent2]
        c = people_ids[child]

        genetic_matrix[c][p1] = 0.5
        genetic_matrix[c][p2] = 0.5

    # add self-loops to people w/o parents in matrix
    ancestors = []
    for i in range(n):
        if sum(genetic_matrix[i]) == 0:
            genetic_matrix[i][i] = 1
            ancestors.append(inv_people_ids[i])

    # converge to stationary matrix. It probably doesn't take this many iters lol. Also this is dumb slow matrix exponentiation
    for i in range(1000):
        genetic_matrix = genetic_matrix @ genetic_matrix

    for id,person in inv_people_ids.items():
        percentages = {}
        if person in ancestors:
            continue
        for i in range(n):
            percent_heritage = round(genetic_matrix[id][i] * 100,2)
            if percent_heritage > 0:
                percentages[inv_people_ids[i]] = percent_heritage

        genealogy[person] = percentages
    
    # my failed attempt at doing full genealogies by pruning the transition graph, I'll leave it in but commented because it was interesting
    # if full and ancestors:
    #     print(ancestors)
    #     new_families = []
    #     for family in families:
    #         if family[0] not in ancestors or family[1] not in ancestors:
    #             new_families.append(family)
    #         if families == new_families:
    #             print(families)
    #             return genealogy
    #     new_genealogy = compute_genealogy(new_families)
    #     for person in new_genealogy:
    #         genealogy[person].update(new_genealogy[person])
    #     return genealogy
    # else:
    #     return genealogy
    return genealogy

def compute_genealogy_full(families):
    '''
    Same as compute_genealogy, but computes the ancestry % for each person in the tree, including intermediate ancestors,
    instead of just the leaves. Uses a very  different mathematical technique!
    '''
    genealogy = {}
    unique_people = list(dict.fromkeys([person for family in families for person in family]))
    n = len(unique_people)
    people_ids = dict(zip(unique_people, np.arange(n)))
    inv_people_ids = {k:v for (v,k) in people_ids.items()}

    genetic_matrix = np.zeros((n,n))
    for (parent1, parent2, child) in families:
        p1 = people_ids[parent1]
        p2 = people_ids[parent2]
        c = people_ids[child]

        genetic_matrix[c][p1] = 1
        genetic_matrix[c][p2] = 1

    # let's try this method
    converge_matrix = np.zeros((n,n))
    for i in range(1,100):
        converge_matrix = converge_matrix + np.linalg.matrix_power(genetic_matrix,i) * 2**-(i)

    for id,person in inv_people_ids.items():
        percentages = {}
        for i in range(n):
            percent_heritage = round(converge_matrix[id][i] * 100,2)
            if percent_heritage > 0:
                percentages[inv_people_ids[i]] = percent_heritage

        genealogy[person] = percentages
    return genealogy
    

def write_genealogy(families, filename, description='',full=False):
    if full:
        genealogy = compute_genealogy_full(families)
    else:
        genealogy = compute_genealogy(families)
    with open(filename, 'w') as f:
        if description:
            f.write(description)
        for person, percentages in genealogy.items():
            if not percentages:
                continue
            f.write(f'{person}:\n')
            percentages = list(percentages.items())
            percentages.sort(key=lambda i:-i[1])
            for ancestor, percentage in percentages:
                if percentage > 0:
                    f.write(f'  {ancestor}: {percentage}%\n')
    f.close()

write_genealogy(families,'genealogy.txt')
write_genealogy(families,'full.txt',full=True,\
                description='Full genealogy of each person: shows what % of their ancestry comes from each person.\n'+
                'Sum of percentages will of course be >100% in general\n')
write_genealogy(families_alt, 'alt.txt',description='Genealogy accounting separately for alternate universe versions.\n'
                + 'Note that individuals have asymmetric ancestry from both universes.\n'
                + 'For example, Hannah is Unknown\'s grandmother, but alt-Hannah is not, so Unknown is more Hannah than alt-Hannah.\n')
write_genealogy(families_alt,'alt_full.txt', full=True, description='Full genealogies, accounting for alt-universe, listing as many as 32 ancestors for each person.')
write_genealogy(families_tronte, 'tronte.txt',description='If Tronte had been Regina\'s father. This leads to Regina, Bartosz, Noah, and Agnes being bootstrapped')
write_genealogy(families_bernd, 'bernd.txt',description='If Bernd had been Helge\'s biological father. I added Peter\'s ancestors to the tree.\n'
                + 'This leads to some incest as he is now both Peter\'s grandfather and Charlotte\'s great-great-great-grandfather.\n')