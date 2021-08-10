from django.db import models

class Condos(models.Model):
    E_STATUS_CHOICES = (('a', 'Active'),
                        ('i', 'Inactive'),
                        ('d', 'Deleted')
                    )

    template_id = models.IntegerField()
    condo_name = models.CharField(max_length=64, blank=True)
    picture = models.CharField(max_length=64, blank=True, default=None)
    location_id = models.IntegerField()
    street_name = models.CharField(max_length=64, blank=True)
    street_address = models.CharField(max_length=64, blank=True)
    district = models.CharField(max_length=64, blank=True, default=None)
    province = models.CharField(max_length=64, blank=True)
    zip_code = models.IntegerField()
    note = models.CharField(max_length=64, blank=True, default=None)
    description = models.CharField(max_length=100, blank=True)
    amenities = models.CharField(max_length=64, blank=True, default=None)
    building_type_id = models.IntegerField(default=None)
    condo_type_id = models.IntegerField()
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