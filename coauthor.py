import csv

def read_csv(fp):
    data = []
    with open(fp, 'r') as f:
        csv_data = csv.reader(f)
        for row in csv_data:
            data.append(row)
    return data


def write_csv(data, csv_fp):
    '''Writes a list to a csv file.'''
    with open(csv_fp, 'w') as out:
        csv_out = csv.writer(out, lineterminator='\n')
        for row in data:
            csv_out.writerow(row)


def format_for_csv(data):
    formatted_list = []
    append_list = ['']
    for name in stevens_abb_names:
        append_list.append(name)
    formatted_list.append(append_list)
    for entry in stevens_abb_names:
        if entry not in data:
            append_list = [entry] + [0] * len(stevens_abb_names)
        else:
            append_list = [entry]
            for name in stevens_abb_names:
                if name not in data[entry] or data[entry][name] == None:
                    append_list.append(0)
                else:
                    append_list.append(data[entry][name])
        formatted_list.append(append_list)
    return formatted_list

association_dict = {}
node_data = [['Id', 'Label', 'Male']]
gephi_data = [["Source", "Target", "Weight"]]

scopus_data = read_csv("scopus_master.csv")[1:]
stevens_data = read_csv("stevens_faculty.csv")[1:]

stevens_abb_names = []
name = 2
for member in stevens_data:
    split_name = member[name].split()
    abb_name = split_name[1] + ' ' + split_name[0][0] + '.'
    member.insert(0, abb_name)
    stevens_abb_names.append(abb_name)

name += 1
abb_name = 0
gender = 11

# create dictionary of author connections
for entry in scopus_data:  # loop through entries from scopus
    authors = entry[0].split(', ')  # separate each author for each book
    for author1 in authors:  # loop through authors
        if author1 in stevens_abb_names:  # if the professor works for Stevens
            for author2 in authors:  # loop through authors again
                if author2 in stevens_abb_names:  # if the second author works for Stevens
                    if not author1 == author2:  # if it is not the same author
                        if author1 in association_dict:  # add to dictionary for author1
                            if author2 in association_dict[author1]:
                                association_dict[author1][author2] += .5
                            else:
                                association_dict[author1][author2] = .5
                        else:
                            association_dict[author1] = {author2: .5}
                        if author2 in association_dict:  # add to dictionary for author2
                            if author1 in association_dict[author2]:
                                association_dict[author2][author1] += .5
                            else:
                                association_dict[author2][author1] = .5
                        else:
                            association_dict[author2] = {author1: .5}

#create node data
for person in stevens_data:
	if person[abb_name] in association_dict: # only take the relevant nodes
		node_data.append([person[abb_name], person[name], person[gender]]) #include name because we want to display full names

#create gephi data
for person1 in association_dict: 
    for person2 in association_dict[person1]:
        gephi_data.append(
            [person1, person2, association_dict[person1][person2]])

edge_data = format_for_csv(association_dict)
write_csv(edge_data, 'author_connections_stevens_only.csv')
write_csv(node_data, 'nodes_stevens_only.csv')
write_csv(gephi_data, 'author_connections_for_gephi.csv')
