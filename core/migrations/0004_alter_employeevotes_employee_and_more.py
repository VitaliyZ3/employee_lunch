# Generated by Django 4.2.4 on 2023-08-10 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0003_employeevotes_menuvotes_employees"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeevotes",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="employeevotes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="menuvotes",
            name="employees",
            field=models.ManyToManyField(
                blank=True,
                related_name="menu_votes",
                through="core.EmployeeVotes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="employee who votes",
            ),
        ),
        migrations.DeleteModel(
            name="Employee",
        ),
    ]
