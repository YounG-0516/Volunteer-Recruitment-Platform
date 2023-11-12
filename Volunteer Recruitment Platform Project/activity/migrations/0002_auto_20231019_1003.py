# Generated by Django 2.2 on 2023-10-19 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0001_initial'),
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.Administrator', verbose_name='发布活动的管理员'),
        ),
        migrations.AddField(
            model_name='activity',
            name='g',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='activity.Ingroup', verbose_name='举办组织'),
        ),
        migrations.AddField(
            model_name='activity',
            name='l',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='activity.Location', verbose_name='活动地点'),
        ),
        migrations.AddField(
            model_name='activity',
            name='t',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='activity.ActivityType', verbose_name='活动类型'),
        ),
    ]
