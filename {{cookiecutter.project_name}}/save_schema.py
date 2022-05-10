from gql.schema import schema

with open("schema.graphql", "w") as f:
    sdl = schema.execute("{_service{sdl}}").data["_service"]["sdl"]
    f.write(str(sdl))
