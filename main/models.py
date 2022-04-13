from django.db import models


# Create your models here.
class Country(models.Model):
    title = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class City(models.Model):
    title = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(max_length=200)
    date_of_creation = models.DateField(blank=True)
    date_of_change = models.DateField(blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SiteUser(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    login = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Overhead(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city', blank=True)
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_city', blank=True)
    day = models.IntegerField(default=0, blank=True)
    sum = models.FloatField(default=0, blank=True)
    date = models.DateField(blank=True)
    rate_dollar = models.FloatField(default=0, blank=True)
    status = models.BooleanField(default=True)
    state = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.from_city.title


class Expenses(models.Model):
    title = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class OverheadCharges(models.Model):
    overhead = models.ForeignKey(Overhead, on_delete=models.CASCADE, blank=True)
    expenses = models.ForeignKey(Expenses, on_delete=models.CASCADE, blank=True)
    cost = models.FloatField(default=0, blank=True)
    emount = models.IntegerField(default=0, blank=True)
    sum = models.FloatField(default=0, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.expenses.title






