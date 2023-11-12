# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activity(models.Model):
    av_id = models.CharField(primary_key=True, max_length=10, verbose_name="活动编号")
    l = models.ForeignKey('Location', models.DO_NOTHING, verbose_name="活动地点")
    g = models.ForeignKey('Ingroup', models.DO_NOTHING, verbose_name="举办组织")
    t = models.ForeignKey('ActivityType', models.DO_NOTHING, verbose_name="活动类型")
    a = models.ForeignKey('myapp.Administrator', models.DO_NOTHING, verbose_name="发布活动的管理员")
    av_title = models.CharField(max_length=20, verbose_name="活动名称")
    # av_state = models.CharField(max_length=10)
    av_state = models.DecimalField(
        choices=((0, "尚未开始招募"), (1, "正在招募"), (2, "招募结束")),
        max_digits=4, decimal_places=0,
        verbose_name="活动状态")
    av_request = models.CharField(max_length=100, verbose_name="活动要求")
    av_content = models.CharField(max_length=100, verbose_name="活动简介")
    av_starttime = models.DateTimeField(verbose_name="活动开始时间")
    av_endtime = models.DateTimeField(verbose_name="活动结束时间")
    av_number = models.IntegerField(verbose_name="招募总人数")

    class Meta:
        ordering = ['av_starttime']
        # managed = False
        db_table = 'activity'
        verbose_name = "活动信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.av_title


class ActivityType(models.Model):
    t_id = models.CharField(primary_key=True, max_length=10, verbose_name="活动类型编号")
    t_name = models.CharField(max_length=20, unique=True, verbose_name="活动类型名称")

    class Meta:
        # managed = False
        ordering = ['t_name']
        db_table = 'activity_type'
        verbose_name = "活动类型信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.t_name


class Ingroup(models.Model):
    g_id = models.CharField(primary_key=True, max_length=10, verbose_name="举办组织编号")
    g_name = models.CharField(max_length=20, unique=True, verbose_name="举办组织名称")

    class Meta:
        # managed = False
        ordering = ['g_name']
        db_table = 'ingroup'
        verbose_name = "举办组织信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.g_name


class Location(models.Model):
    l_id = models.CharField(primary_key=True, max_length=10, verbose_name="地点编号")
    l_name = models.CharField(max_length=20, unique=True, verbose_name="地点名称")

    class Meta:
        # managed = False
        ordering = ['l_name']
        db_table = 'location'
        verbose_name = "地点信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.l_name
