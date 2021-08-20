from django.db import models


class CondoType(models.Model):
    E_STATUS_CHOICES = (
        ('a', 'Active'),
        ('i', 'Inactive'),
        ('d', 'Deleted'),
    )
    condo_type = models.CharField(max_length=64, blank=True)

    created_date = models.DateField()
    modified_date = models.DateField()
    create_by = models.IntegerField(default=None)
    modified_by = models.IntegerField(default=None)
    e_status = models.CharField(
        choices=E_STATUS_CHOICES,
        default='Active',
        max_length=10
    )


class Address(models.Model):
    E_STATUS_CHOICES = (
        ('a', 'Active'),
        ('i', 'Inactive'),
        ('d', 'Deleted'),
    )

    city = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=64, blank=True, null=True)
    street_address = models.CharField(max_length=64, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    zip_code = models.CharField(max_length=64, blank=True, null=True)
    condo = models.ForeignKey('Condo', related_name='address', on_delete=models.CASCADE)

    e_status = models.CharField(
        choices=E_STATUS_CHOICES,
        default='Active',
        max_length=10
    )

    def __str__(self):
        return self.street_address

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Amenity(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Email(models.Model):
    email = models.EmailField()
    condo = models.ForeignKey('Condo', related_name='email', on_delete=models.CASCADE)


class Phone(models.Model):
    phone_number = models.CharField(max_length=18)
    phone_number_canonical = models.CharField(max_length=18)
    condo = models.ForeignKey('Condo', related_name='phone', on_delete=models.CASCADE)


class Organization(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)
    condo = models.ForeignKey('Condo', related_name='organization', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.name}"


class Condo(models.Model):
    E_STATUS_CHOICES = (
        ('a', 'Active'),
        ('i', 'Inactive'),
        ('d', 'Deleted'),
    )

    condo_name = models.CharField(max_length=64)
    picture = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True)
    amenities = models.ManyToManyField(Amenity)
    building_type = models.IntegerField(null=True, blank=True)
    condo_corp = models.CharField(max_length=64, blank=True, null=True)
    floors = models.IntegerField(null=True, blank=True)
    units = models.IntegerField(null=True, blank=True)
    builder = models.IntegerField(null=True, blank=True)
    architect = models.IntegerField(null=True, blank=True)
    interior_designer = models.IntegerField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    pm = models.IntegerField(null=True, blank=True)
    developer = models.CharField(max_length=64, blank=True, null=True)
    view_floor_plans = models.CharField(max_length=64, blank=True)

    modified_date = models.DateTimeField(default=None)

    e_status = models.CharField(
        choices=E_STATUS_CHOICES,
        default='Active',
        max_length=10
    )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
