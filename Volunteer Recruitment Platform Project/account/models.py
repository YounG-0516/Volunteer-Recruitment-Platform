# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Volunteer(models.Model):
    v_id = models.CharField(primary_key=True, max_length=10, verbose_name="志愿者编号")
    i = models.ForeignKey('Institute', models.DO_NOTHING, verbose_name="学院")
    vg = models.ForeignKey('Volunteergroup', models.DO_NOTHING, verbose_name="义工组织")
    v_pwd = models.CharField(max_length=20, verbose_name="密码")
    v_name = models.CharField(max_length=10, unique=True, verbose_name="姓名")

    class Meta:
        ordering = ['v_name']
        db_table = 'volunteer'
        verbose_name = "志愿者信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.v_name


class Volunteergroup(models.Model):
    vg_id = models.CharField(primary_key=True, max_length=10, verbose_name="义工组织编号")
    vg_name = models.CharField(max_length=20, verbose_name="义工组织名称")
    vg_introduction = models.CharField(max_length=100, blank=True, null=True, verbose_name="义工组织介绍")

    class Meta:
        # managed = False
        ordering = ['vg_name']
        db_table = 'volunteergroup'
        verbose_name = "义工组织信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.vg_name


class Institute(models.Model):
    i_id = models.CharField(primary_key=True, max_length=10, verbose_name="学院编号")
    i_name = models.CharField(max_length=20, verbose_name="学院名称")

    class Meta:
        # managed = False
        ordering = ['i_name']
        db_table = 'institute'
        verbose_name = "学院信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.i_name
