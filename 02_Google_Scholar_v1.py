#Using code from: https://pypi.org/project/scholarly/
#
#pip3 install scholarly
#
#Gave warnings:
#  WARNING: The script pygmentize.exe is installed in 'C:\Users\Staff\AppData\Roaming\Python\Python37\Scripts' which is not on PATH.
#  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#  WARNING: The script pybabel.exe is installed in 'C:\Users\Staff\AppData\Roaming\Python\Python37\Scripts' which is not on PATH.
#  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#  WARNING: The scripts sphinx-apidoc.exe, sphinx-autogen.exe, sphinx-build.exe and sphinx-quickstart.exe are installed in 'C:\Users\Staff\AppData\Roaming\Python\Python37\
#Scripts' which is not on PATH.
#  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#  WARNING: The scripts futurize.exe and pasteurize.exe are installed in 'C:\Users\Staff\AppData\Roaming\Python\Python37\Scripts' which is not on PATH.
#  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#  WARNING: The script dotenv.exe is installed in 'C:\Users\Staff\AppData\Roaming\Python\Python37\Scripts' which is not on PATH.
#  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

# Example code from webpage

from scholarly import scholarly
import NeoQuery
from Functions import msg, return_alphanum

'''
match(s:staff) where
    s.name = "Simon Barrans" or
    s.name = "Grigoris Antoniou" or
    s.name = "Adrian Pitts" or
    s.name = "Paul Thomas"
set s.gsname = s.name

match(s:staff)-[:publication]-(p:publication)
detach delete p
'''

case = 4

if case == 4:
    msg("CASE 4")
    msg("Establishing Neo4j query")
    query1 = NeoQuery.NeoQuery("bolt://localhost", "neo4j", "neo4jj")
    msg("Running query to get staff names")
    query1.set("match (s:staff) where s.gsname is not null return s.id, s.gsname")

    msg("Query completed, examining results")
    for each_row in query1.getResultsArray():
        staff_id = each_row[0]
        staff_gsname = each_row[1]

        msg(f"Searching Google Scholar for author name\t\t\t{staff_gsname}")
        search_query = scholarly.search_author(staff_gsname)                    # Search for all authors by this name
        print("\tFound matching author names, searching for affiliation with Huddersfield:", end = "\t")

        found_affiliation_match = False
        for i, author in enumerate(search_query):                               # For each result
            name = author["name"]                                               # |
            affiliation = author["affiliation"]                                 # |
                                                                                # |
            if "huddersfield" in affiliation.lower():                           # |   If the affiliation is a grim northern town
                found_affiliation_match = True                                  #
                print("\tFound author affiliation with Huddersfield. Collecting publication details.")
                details = scholarly.fill(author)                                # |   |   Get the author's details
                publications = details["publications"]                          # |   |   And strip out the publications
                print(f"\t{len(publications)} publications found.")
                print("\tMerging publication nodes and joining to authors")

                for j, each_entry in enumerate(publications):                   # |   |   For each publication
                    publication_title = each_entry['bib']['title']
                    publication_title = return_alphanum(publication_title)
                    #print(f"{i}-{j} ".rjust(10), publication_title )    # |   |   |   Print the title
                    query1.set(f"match(s:staff{{id:{staff_id}}}) ")
                    query1.add(f"merge(p{j}:publication{{title:\"{publication_title}\"}}) merge(s)-[:publication]->(p{j})\n")
                    print(query1.get())
                    query1.runQuery()

        if not found_affiliation_match:
            print("NO AFFILIATION MATCH FOUND")
    msg("Author searches complete. Closing Neo4j query.")
    query1.close()
    msg("Finished")

if case == 3:
    msg("Establishing Neo4j query")
    query1 = NeoQuery.NeoQuery("bolt://localhost", "neo4j", "neo4jj")
    msg("Running query to get staff names")
    query1.set("match (s:staff) where s.gsname is not null return s.id, s.gsname")

    msg("Query completed, examining results")
    for each_row in query1.getResultsArray():
        staff_id = each_row[0]
        staff_gsname = each_row[1]

        msg(f"Searching Google Scholar for author name\t\t\t{staff_gsname}")
        search_query = scholarly.search_author(staff_gsname)                    # Search for all authors by this name
        print("\tFound matching author names, searching for affiliation with Huddersfield:", end = "\t")

        found_affiliation_match = False
        for i, author in enumerate(search_query):                               # For each result
            name = author["name"]                                               # |
            affiliation = author["affiliation"]                                 # |
                                                                                # |
            if "huddersfield" in affiliation.lower():                           # |   If the affiliation is a grim northern town
                found_affiliation_match = True                                  #
                print("\tFound author affiliation with Huddersfield. Collecting publication details.")
                details = scholarly.fill(author)                                # |   |   Get the author's details
                publications = details["publications"]                          # |   |   And strip out the publications
                print(f"\t{len(publications)} publications found.")
                print("\tMerging publication nodes and joining to authors")
                query1.set(f"match(s:staff{{id:{staff_id}}})\n")
                for j, each_entry in enumerate(publications):                   # |   |   For each publication
                    publication_title = each_entry['bib']['title']
                    publication_title = return_alphanum(publication_title)
                    #print(f"{i}-{j} ".rjust(10), publication_title )    # |   |   |   Print the title
                    query1.add(f"merge(p{j}:publication{{title:\"{publication_title}\"}}) merge(s)-[:publication]->(p{j})\n")
                print("\tSubmitting Neo4j query to add publications to author in database.")
                print(query1.get())
                query1.runQuery()
                print("\tQuery completed.")
        if not found_affiliation_match:
            print("NO AFFILIATION MATCH FOUND")
    msg("Author searches complete. Closing Neo4j query.")
    query1.close()
    msg("Finished")

if case == 2:
    search_query = scholarly.search_author('Peter Hughes')                  # Search for all authors by this name
    for i, author in enumerate(search_query):                               # For each result
        name = author["name"]                                               #   |
        affiliation = author["affiliation"]                                 #   |
        print(f"{i}\t{name}\t{affiliation}")                                #   |   Display the name and affiliation
        if "huddersfield" in affiliation.lower():                           #   |   If the affiliation is a grim northern town
            details = scholarly.fill(author)                                #   |   |   Get the author's details
            publications = details["publications"]                          #   |   |   And strip out the publications
            for j, each_entry in enumerate(publications):                   #   |   |   For each publication
                print(f"{i}-{j} ".rjust(10), each_entry['bib']['title'])    #   |   |   |   Print the title

# Achtung! The results from code above has a spurious entry: "This file was downloaded from: http://eprints. qut. edu. au/58378"
# Inspecting the element shows that this is the title that is shown in the data, so the error is not caused by
# a bug in the code, but in the source data. The same error occurs on Google Scholar's webpage.
# It may be necessary to create a cleansing rule to reject entries with titles starting "This file was downloaded from..."

if case == 1:
    # Source code from example webpage
    # Retrieve the author's data, fill-in, and print
    # Get an iterator for the author results

    search_query = scholarly.search_author('Steven A Cholewiak')

    # Retrieve the first result from the iterator
    first_author_result = next(search_query)
    scholarly.pprint(first_author_result)

    # Retrieve all the details for the author
    author = scholarly.fill(first_author_result )
    scholarly.pprint(author)

    # Take a closer look at the first publication
    first_publication = author['publications'][0]
    first_publication_filled = scholarly.fill(first_publication)
    scholarly.pprint(first_publication_filled)

    # Print the titles of the author's publications
    publication_titles = [pub['bib']['title'] for pub in author['publications']]
    print(publication_titles)

    # Which papers cited that publication?
    citations = [citation['bib']['title'] for citation in scholarly.citedby(first_publication_filled)]
    print(citations)