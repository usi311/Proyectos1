import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType  # Importa el UserType desde users.schema
from .services import obtener_chistes_jokeapi
from jokes.models import Chiste, Vote

class ChisteType(DjangoObjectType):
    class Meta:
        model = Chiste

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    chistes = graphene.List(ChisteType)
    votes = graphene.List(VoteType)

    def resolve_chistes(self, info):
        return Chiste.objects.all()
     
    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

class CreateChiste(graphene.Mutation):
    chiste = graphene.Field(ChisteType)

    class Arguments:
        autor = graphene.String()
        categoria = graphene.String()

    def mutate(self, info, autor, categoria):
        user = info.context.user  # Obtén el usuario desde el contexto de la solicitud
        texto_chiste, _, _ = obtener_chistes_jokeapi()
        chiste = Chiste.objects.create(texto=texto_chiste, autor=autor, categoria=categoria, posted_by=user)
        return CreateChiste(chiste=chiste)

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    chiste = graphene.Field(ChisteType)

    class Arguments:
        chiste_id = graphene.Int()

    def mutate(self, info, chiste_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Debes estar autenticado para votar.')

        chiste = Chiste.objects.filter(id=chiste_id).first()
        if not chiste:
            raise Exception('Chiste inválido.')

        # Verifica si el usuario ya ha votado por este chiste
        if Vote.objects.filter(user=user, chiste=chiste).exists():
            raise Exception('Ya has votado por este chiste.')

        # Crea un nuevo voto
        Vote.objects.create(
            user=user,
            chiste=chiste,
        )

        return CreateVote(user=user, chiste=chiste)

class Mutation(graphene.ObjectType):
    create_chiste = CreateChiste.Field()
    create_vote = CreateVote.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)

