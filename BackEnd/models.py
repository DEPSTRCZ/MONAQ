from tortoise.models import Model
from tortoise import fields
class Sensors(Model):
    sensor_id = fields.IntField(primary_key=True)

    class Meta:
        table = "sensors"

    def __str__(self):
        return self.name


class Record(Model):
    sensor = fields.ForeignKeyField('models.Sensors', related_name='records')
    co2 = fields.IntField(max_digits=5, decimal_places=2)
    tempature = fields.DecimalField(max_digits=2, decimal_places=2)
    humidity = fields.DecimalField(max_digits=2, decimal_places=2)
    updated_at = fields.DatetimeField(auto_now=True)
    lat = fields.DecimalField(max_digits=9, decimal_places=6)
    long = fields.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        table = "records"
        unique_together = ("sensor","updated_at")

    def __str__(self):
        return self.name
    
