import datetime
from django.utils import timezone
from django.db import models


class project(models.Model):
    project_name = models.CharField(max_length=200)
    create_date = models.DateTimeField('date Created')

    def __str__(self):
        return self.project_name

    def was_created_recently(self):
        return self.create_date >= timezone.now() - datetime.timedelta(days=1)
    was_created_recently.admin_order_field = 'create_date'
    was_created_recently.boolean = True
    was_created_recently.short_description = 'Created recently?'


class sql_script(models.Model):
    project = models.ForeignKey(project)
    script = models.TextField()

    def __str__(self):
        return self.script


class xml(models.Model):
    xml = models.TextField()
    project = models.ForeignKey(project)
    sql_script = models.ForeignKey(sql_script)

    def __str__(self):
        return self.xml


class template(models.Model):
    template = models.TextField()
    project = models.ForeignKey(project)

    def __str__(self):
        return self.template


class code(models.Model):
    code = models.TextField()
    project = models.ForeignKey(project)
    xml = models.ForeignKey(xml)
    template = models.ForeignKey(template)

    def __str__(self):
        return self.code
