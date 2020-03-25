# cookbook/ingredients/schema.py
import graphene

from graphene_django.types import DjangoObjectType

from cookbook.ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(object):
    category = graphene.Field(CategoryType, id=graphene.Int(), name=graphene.String())
    all_categories = graphene.List(CategoryType)
    
    ingredient = graphene.Field(IngredientType, id=graphene.Int(), name=graphene.String())
    all_ingredients = graphene.List(IngredientType)

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None


class CreateIngredient(graphene.Mutation):
    ingredient = graphene.Field(IngredientType)

    class Arguments:
        name = graphene.String()
        notes = graphene.String()
        category_id = graphene.Int()

    def mutate(self, info, **kwargs):
        # retrieve the arguments
        name = kwargs.get('name')
        notes = kwargs.get('notes', '')
        category_id = kwargs.get('category_id')

        ingredient = Ingredient.objects.create(name=name, notes=notes, category_id=category_id)
        return CreateIngredient(ingredient=ingredient)


class Mutation(graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()
