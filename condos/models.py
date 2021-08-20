from django.db import models


class CondoType(models.Model):
    E_STATUS_CHOICES = (('a', 'Active'),
                        ('i', 'Inactive'),
                        ('d', 'Deleted'))
    condo_type = models.CharField(max_length=64, blank=True)
    created_date = models.DateField()
    modified_date = models.DateField()
    create_by_id = models.IntegerField(default=None)
    modified_by_id = models.IntegerField(default=None)
    e_status = models.CharField(
        choices=E_STATUS_CHOICES,
        default='Active',
        max_length=10
    )


class Location(models.Model):
    E_STATUS_CHOICES = (('a', 'Active'),
                        ('i', 'Inactive'),
                        ('d', 'Deleted'))
    city = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=10, default='ON')
    created_date = models.DateField()
    modified_date = models.DateField()
    create_by_id = models.IntegerField(default=None)
    modified_by_id = models.IntegerField(default=None)
    e_status = models.CharField(
        choices=E_STATUS_CHOICES,
        default='Active',
        max_length=10
    )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Condos(models.Model):
    E_STATUS_CHOICES = (('a', 'Active'),
                        ('i', 'Inactive'),
                        ('d', 'Deleted'))
    condo_name = models.CharField(max_length=64, blank=True)
    picture = models.CharField(max_length=500, blank=True, default=None)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    street_name = models.CharField(max_length=64, blank=True)
    street_address = models.CharField(max_length=64, blank=True)
    district = models.CharField(max_length=64, blank=True, default=None)
    province = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=64)
    note = models.CharField(max_length=2000, blank=True, default=None)
    description = models.CharField(max_length=2000, blank=True)
    amenities = models.CharField(max_length=500, blank=True, default=None)
    building_type_id = models.IntegerField(default=None)
    condo_type_id = models.ForeignKey(CondoType, on_delete=models.CASCADE)
    condo_corp = models.CharField(max_length=64, blank=True)
    floors = models.IntegerField()
    units = models.IntegerField()
    builder_id = models.IntegerField(default=None)
    architect_id = models.IntegerField(default=None)
    interior_designer_id = models.IntegerField(default=None)
    date_completed = models.DateTimeField(default=None)
    pm_id = models.IntegerField(default=None)
    developer = models.CharField(max_length=64, blank=True, default=None)
    send_email = models.CharField(max_length=64, blank=True, default=None)
    view_floor_plans = models.CharField(max_length=64, blank=True)
    created_date = models.DateTimeField(default=None)
    modified_date = models.DateTimeField(default=None)
    created_by_id = models.IntegerField(default=None)
    modified_by_id = models.IntegerField(default=None)
    e_status = models.CharField(
        choices=E_STATUS_CHOICES,
        default='Active',
        max_length=10
    )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
