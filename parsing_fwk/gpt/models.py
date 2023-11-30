# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TablesAcquiring(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=1000, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    site = models.OneToOneField('TablesSites', models.DO_NOTHING, blank=True, null=True)
    secret_key = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_acquiring'



class TablesConstructor(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    json = models.JSONField()
    file = models.CharField(max_length=100, blank=True, null=True)
    venue = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_constructor'


class TablesEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=2000)
    team1_name = models.CharField(max_length=200, blank=True, null=True)
    team2_name = models.CharField(max_length=200, blank=True, null=True)
    place = models.ForeignKey('TablesPlaces', models.DO_NOTHING)
    first_image = models.CharField(max_length=100, blank=True, null=True)
    second_image = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField()
    header_image = models.CharField(max_length=500, blank=True, null=True)
    top_event = models.BooleanField()
    margin = models.ForeignKey('TablesMargin', models.DO_NOTHING, blank=True, null=True)
    scheme = models.ForeignKey('TablesConstructor', models.DO_NOTHING, blank=True, null=True)
    age = models.CharField(max_length=50)
    date = models.DateTimeField()
    genre = models.CharField(max_length=50, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    scene = models.ForeignKey('TablesScenes', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('TablesSites', models.DO_NOTHING, blank=True, null=True)
    slug = models.CharField(max_length=2000, blank=True, null=True)
    parsed_url = models.JSONField(blank=True, null=True)
    fan_id = models.BooleanField(blank=True, null=True)
    hidden = models.BooleanField(blank=True, null=True)
    decrement = models.DurationField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_event'


class TablesEventTags(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey('TablesEvent', models.DO_NOTHING)
    tags = models.ForeignKey('TablesTags', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tables_event_tags'
        unique_together = (('event', 'tags'),)


class TablesGallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    show = models.BooleanField(blank=True, null=True)
    event = models.ForeignKey('TablesEvent', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_gallery'


class TablesGenres(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'tables_genres'


class TablesMargin(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    rules = models.JSONField()

    class Meta:
        managed = False
        db_table = 'tables_margin'


class TablesNews(models.Model):
    id = models.BigAutoField(primary_key=True)
    header_text = models.CharField(max_length=200)
    news_image = models.CharField(max_length=100)
    main_text = models.TextField()
    top_news = models.BooleanField()
    date = models.DateField()
    site = models.ForeignKey('TablesSites', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_news'


class TablesOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    fio = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    second_info = models.TextField()
    order_info = models.TextField()
    status = models.CharField(max_length=200)
    ordered = models.BooleanField()
    info = models.TextField()
    ticket_ids = models.JSONField()
    site = models.ForeignKey('TablesSites', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    ordered_at = models.DateTimeField(blank=True, null=True)
    profit = models.JSONField()
    utm = models.JSONField(blank=True, null=True)
    mail_receipt = models.CharField(max_length=500, blank=True, null=True)
    event = models.ForeignKey('TablesEvent', models.DO_NOTHING, blank=True, null=True)
    date_close = models.DateTimeField(blank=True, null=True)
    operator = models.CharField(max_length=500, blank=True, null=True)
    award = models.CharField(max_length=50, blank=True, null=True)
    viewers = models.BooleanField(blank=True, null=True)
    total_amount = models.IntegerField(blank=True, null=True)
    fan_id = models.CharField(max_length=50, blank=True, null=True)
    punishment = models.IntegerField(blank=True, null=True)
    site_owner = models.CharField(max_length=100, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_order'


class TablesOrdershistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    operator = models.CharField(max_length=500, blank=True, null=True)
    action = models.CharField(max_length=500, blank=True, null=True)
    done_at = models.DateTimeField()
    order = models.ForeignKey('TablesOrder', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_ordershistory'


class TablesOwners(models.Model):
    venue = models.CharField(max_length=200)
    share1 = models.FloatField()
    share2 = models.FloatField()
    share3 = models.FloatField()
    share4 = models.FloatField()
    share5 = models.FloatField()
    from_date = models.CharField(max_length=50, blank=True, null=True)
    to_date = models.CharField(max_length=50, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'tables_owners'


class TablesParsedevents(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    extra = models.JSONField()
    url = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'tables_parsedevents'


class TablesParsingtypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'tables_parsingtypes'


class TablesPlaces(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    slug = models.CharField(unique=True, max_length=50, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_places'


class TablesScenes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'tables_scenes'

class TablesSites(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    actual_address = models.CharField(max_length=200)
    inn = models.CharField(max_length=200)
    legal_address = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    ogrnip = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    phone_common = models.CharField(max_length=200)
    parsers = models.JSONField(blank=True, null=True)
    reseller = models.BooleanField()
    disabled = models.BooleanField(blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    sole_proprietor = models.CharField(max_length=200, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_sites'


class TablesSitesTags(models.Model):
    id = models.BigAutoField(primary_key=True)
    sites = models.ForeignKey('TablesSites', models.DO_NOTHING)
    tags = models.ForeignKey('TablesTags', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tables_sites_tags'
        unique_together = (('sites', 'tags'),)


class TablesStoredUrls(models.Model):
    id = models.BigIntegerField(primary_key=True)
    urls = models.JSONField()

    class Meta:
        managed = False
        db_table = 'tables_stored_urls'


class TablesTags(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'tables_tags'


class TablesTickets(models.Model):
    id = models.BigAutoField(primary_key=True)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    sector = models.CharField(max_length=200)
    sector_id = models.IntegerField()
    row = models.CharField(max_length=200)
    seat = models.CharField(max_length=200)
    status = models.CharField(max_length=100)
    original_price = models.IntegerField()
    sell_price = models.IntegerField()
    type = models.CharField(max_length=200, blank=True, null=True)
    client = models.CharField(max_length=200, blank=True, null=True)
    operator = models.CharField(max_length=200, blank=True, null=True)
    named = models.BooleanField(blank=True, null=True)
    event_id = models.ForeignKey('TablesEvent', models.DO_NOTHING)
    scheme_id = models.ForeignKey('TablesConstructor', models.DO_NOTHING, blank=True, null=True)
    date_id = models.IntegerField(blank=True, null=True)
    no_schema_available = models.IntegerField(blank=True, null=True)
    own_bought = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables_tickets'
