schema = '''Node property are the following
(:Vehicle {name: "Vehicle",indexes: [],constraints: []}),
(:Area {name: "Area",indexes: ["areaCode"],constraints: []}), 
(:Email {name: "Email",indexes: [],constraints: []}), 
(:Phone {name: "Phone",indexes: [],constraints: []}), 
(:Crime {name: "Crime",indexes: ["last_outcome", "type"],constraints: []}),
(:PhoneCall {name: "PhoneCall",indexes: [],constraints: []}), 
(:Object {name: "Object",indexes: ["type"],constraints: []}),
(:PostCode {name: "PostCode",indexes: ["code"],constraints: []}),
(:Person {name: "Person",indexes: ["name", "nhs_no", "surname"],constraints: []}), 
(:Location {name: "Location",indexes: ["postcode", "address"],constraints: []}), 
(:Officer {name: "Officer",indexes: ["rank", "surname"],constraints: []})

Relationship details are the following
(:Crime)-[:INVESTIGATED_BY]->(:Officer), 
(:Crime)<-[:INVOLVED_IN]-(:Vehicle), 
(:Crime)<-[:INVOLVED_IN]-(:Object), 
(:Crime)<-[:PARTY_TO]-(:Person),
(:Crime)-[:OCCURRED_AT]->(:Location), 
(:Location)<-[:CURRENT_ADDRESS]-(:Person),
(:Location)-[:HAS_POSTCODE]->(:PostCode), 
(:Location)-[:LOCATION_IN_AREA]->(:Area), 
(:PostCode)-[:POSTCODE_IN_AREA]->(:Area), 
(:PhoneCall)-[:CALLER]->(:Phone), 
(:PhoneCall)-[:CALLED]->(:Phone), 
(:Person)-[:HAS_PHONE]->(:Phone), 
(:Person)-[:HAS_EMAIL]->(:Email), 
(:Person)-[:KNOWS_SN]->(:Person), 
(:Person)-[:KNOWS]->(:Person), 
(:Person)-[:KNOWS_LW]->(:Person),
(:Person)-[:KNOWS_PHONE]->(:Phone), 
(:Person)-[:FAMILY_REL]->(:Person)
'''

CYPHER_GENERATION_TEMPLATE = """Task: Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema: 
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}

Example: If the question was to find the officer who has investigated the maximum number of crimes, and also provide the count of crimes they investigated, the generated Cypher should be:
MATCH (o:Officer)<-[r:INVESTIGATED_BY]-(c:Crime)
WITH o, count(r) AS numCrimes
ORDER BY numCrimes DESC
RETURN o.name AS Officer, numCrimes AS NumberOfCrimes
LIMIT 1;

Ensure the RETURN statement includes the property values used in the query's filtering condition, alongside the main information requested from the original question.
"""