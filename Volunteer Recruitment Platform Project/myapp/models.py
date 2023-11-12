# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class Apply(models.Model):
    ap_id = models.CharField(primary_key=True, max_length=10, verbose_name="申请编号")
    v = models.ForeignKey('account.Volunteer', models.DO_NOTHING, verbose_name="申请志愿者")
    av = models.ForeignKey('activity.Activity', models.DO_NOTHING, verbose_name="申请活动")
    a = models.ForeignKey('Administrator', models.DO_NOTHING, verbose_name="审核管理员")
    ap_time = models.DateTimeField(verbose_name="申请时间")
    # ap_state = models.CharField(max_length=10)
    ap_state = models.DecimalField(choices=((1, "申请通过"), (2, "等待审批中"), (3, "申请不通过")), max_digits=4,
                                   decimal_places=0,
                                   blank=True, null=True, verbose_name="申请状态")
    ap_reason = models.CharField(max_length=100, blank=True, null=True, verbose_name="申请理由")
    ap_approvaltime = models.DateTimeField(blank=True, null=True, verbose_name="审核时间")

    class Meta:
        # managed = False
        ordering = ['ap_time']
        db_table = 'apply'
        verbose_name = "申请信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"【{self.v}】申请报名【{str(self.av)}】"


class Administrator(models.Model):
    a_id = models.CharField(primary_key=True, max_length=10, verbose_name="管理员编号")
    i = models.ForeignKey('account.Institute', models.DO_NOTHING, verbose_name="学院")
    a_pwd = models.CharField(max_length=20, verbose_name="管理员密码")
    a_name = models.CharField(max_length=10, verbose_name="管理员名称")

    class Meta:
        ordering = ['a_name']
        db_table = 'administrator'
        verbose_name = "管理员信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.a_name