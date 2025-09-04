from tortoise import fields, models


class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    items: fields.ReverseRelation["Item"]

class Item(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    price = fields.FloatField()
    tax = fields.FloatField(null=True)
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "models.Category", related_name="items"
    )
