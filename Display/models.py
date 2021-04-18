from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField


# Create your models here.

class TreeType(models.Model):
    id = models.AutoField('编号', primary_key=True)
    name = models.CharField('名称', max_length=100)
    growthHabit = models.TextField('生长习性')

    class Meta:
        verbose_name = '树木类型'
        verbose_name_plural = verbose_name
        db_table = 'TreeType'
        ordering = ['-id']

    def __str__(self):
        return self.name


class User(AbstractUser):
    # is_staff = models.BooleanField("工作人员状态", default=True)
    phone = models.CharField('手机号码', max_length=11)
    sex_type = [['male', u'男'], ['female', u'女']]
    sex = models.CharField('性别', max_length=10, choices=sex_type)
    birthdate = models.DateField('出生日期', blank=True, null=True)
    IDCard = models.CharField('身份证号', max_length=18, blank=True, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'User'
        ordering = ['-id']

    def __str__(self):
        return self.username
    # def save(self, *args, **kwargs):


#         self.password = make_password(self.password)
#         super(User, self).save(*args, **kwargs)

class TreeInformation(models.Model):
    id = models.AutoField('编号', primary_key=True)
    img = models.ImageField('树木图片', upload_to='./upload')
    type = models.ForeignKey(TreeType, on_delete=models.CASCADE, verbose_name="类型", )
    age = models.IntegerField('树龄')
    height = models.FloatField('树高')
    width = models.FloatField('地围')
    date = models.DateField('被领养日期', blank=True, null=True)

    def formatDate(self):
        return self.date.strftime("%Y-%m-%d")

    formatDate.short_description = '发布日期'
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='领养人', blank=True, null=True)

    class Meta:
        verbose_name = '树木信息'
        verbose_name_plural = verbose_name
        db_table = 'TreeInformation'
        ordering = ['-id']

    def __str__(self):
        return '信息' + str(self.id)


class Record(models.Model):
    id = models.AutoField('编号', primary_key=True)
    dateTime = models.DateTimeField('养护时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='养护人', blank=True, null=True)
    method_choices = [['plant', u'种植'], ['water', u'浇水'], ['clip', u'修剪'], ['fertilizer', u'施肥']]
    method = MultiSelectField('措施', max_length=100, choices=method_choices, max_choices=4)
    note = models.CharField('备注', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = '记录信息'
        verbose_name_plural = verbose_name
        db_table = 'Record'
        ordering = ['-id']

    def __str__(self):
        return '记录' + str(self.id)
