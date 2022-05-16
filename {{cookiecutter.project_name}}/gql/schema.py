import graphene
from graphene_federation3 import build_schema


class Query(graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = build_schema(
    # query=Query,
    # mutation=Mutation
)
