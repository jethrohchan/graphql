from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
# how is above different from from graphene_django.types import DjangoObjectType?


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(object):
    user = graphene.Field(UserType, id=graphene.Int(required=True))  # queryfield is id only
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user  # vis a vis request.user...
        if user.is_anonymous:
            raise Exception('Not Logged In!')
        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()

    def mutate(self, info, **kwargs):
        # retrieve the arguments
        username = kwargs.get('username')
        password = kwargs.get('password')
        email = kwargs.get('email')

        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)  # not just a raw return user here.


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
