# import json
# from django.shortcuts import render
# from neo4j import GraphDatabase  # Import Neo4j driver
#
# def get_taxonomy_data():
#     uri = "bolt://localhost:7687"  # Your Neo4j URI
#     user = "neo4j"
#     password = "hardi1902"
#
#     driver = GraphDatabase.driver(uri, auth=(user, password))
#
#     with driver.session() as session:
#         # Cypher query to retrieve data
#         cypher_query = """
#             MATCH (root:Taxonomy)
#             CALL apoc.path.expandConfig(root, {
#               relationshipFilter: 'HAS_CHILD',
#               labelFilter: 'Taxonomy',
#               terminatorNodes: [],
#               minLevel: 0
#             })
#             YIELD path
#             WITH nodes(path) AS nodes
#             WITH [node in nodes | node.Title] AS levels, LAST(nodes).Description as Description
#             RETURN levels AS Hierarchy, Description
#             """
#         result = session.run(cypher_query)
#
#         # Extract data from Neo4j result and convert to a list of dictionaries
#         data = [dict(record) for record in result]
#
#     driver.close()
#     return data
#
#
# def show_taxonomy_data(request):
#     data = get_taxonomy_data()  # Fetch data from Neo4j
#     json_data = json.dumps(data)
#     print(json_data)
#     return render(request, 'taxonomy_data.html', {'json_data': json_data})
import json

from django.http import HttpResponse
from django.shortcuts import render
from neo4j import GraphDatabase


def get_hierarchy(request):
    # Pass the data to the template
    return render(request, 'hierarchy_template.html', {})


def get_data(request):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "hardi1902"))

    # Execute your Cypher query
    with driver.session() as session:
        result = session.run("""
                MATCH (root:Taxonomy)
                CALL apoc.path.expandConfig(root, {
                    relationshipFilter: 'HAS_CHILD',
                    labelFilter: 'Taxonomy',
                    terminatorNodes: [],
                    minLevel: 0
                })
                YIELD path
                WITH nodes(path) AS nodes
                WITH [node in nodes | node.Title] AS levels, LAST(nodes).Description as Description
                RETURN levels AS Hierarchy, Description
            """)

        # Extract the data from the result
        # max_hierarchy_length = max(len(record["levels"]) for record in result)
        data = [{"Hierarchy": record["Hierarchy"], "Description": record["Description"]} for record in result]
    # Close the Neo4j driver
    driver.close()
    return HttpResponse(json.dumps({'data': data}))

# from django.shortcuts import render
# from neo4j import GraphDatabase
#
#
# def get_hierarchy(request):
#     # Connect to your Neo4j database
#     driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "hardi1902"))
#
#     # Execute your Cypher query
#     with driver.session() as session:
#         result = session.run("""
#             MATCH (root:Taxonomy)
#             CALL apoc.path.expandConfig(root, {
#                 relationshipFilter: 'HAS_CHILD',
#                 labelFilter: 'Taxonomy',
#                 terminatorNodes: [],
#                 minLevel: 0
#             })
#             YIELD path
#             WITH nodes(path) AS nodes
#             WITH [node in nodes | node.Title] AS levels, LAST(nodes).Description as Description
#             RETURN levels, Description
#         """)
#
#         # Extract the data from the result
#         max_hierarchy_length = max(len(record["levels"]) for record in result)
#         column_names = [f"Level_{i + 1}" for i in range(max_hierarchy_length)]
#         data = [{f"Level_{i + 1}": record["levels"][i] if i < len(record["levels"]) else "" for i in
#                  range(max_hierarchy_length)} | {"Description": record["Description"]} for record in result]
#
#     # Close the Neo4j driver
#     driver.close()
#
#     # Pass the data to the template
#     return render(request, 'hierarchy_template.html', {'data': data, 'column_names': column_names})
