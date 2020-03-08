import graphene
from apps.books.schema import Query as BooksQuery


class Query(BooksQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
