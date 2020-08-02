from django.db import models
from djongo import models
# Create your models here.

class wenshu(models.Model):
    case_no = models.CharField(verbose_name="案件编号",max_length=100)
    type = models.IntegerField(verbose_name="案件类型")
    date = models.DateField(verbose_name="审理日期")
    number = models.CharField(max_length=100)
    court = models.CharField(max_length=50)
    judge_produce = models.CharField(max_length=20)

    def __str__(self):
        return self.case_no

    class Meta:
        verbose_name = "判决文书"
        verbose_name_plural = verbose_name
        app_label = 'wenshu'
        db_table="wenshu"
# /* person_info_item ={
#             'case_no':case_no,
#             'case_content':content,
#             'person_name':person_name,
#             'person_sex':person_sex,
#             'person_type':person_type,
#             'person_birthday':person_birthday,
#             'person_nation':person_nation,
#             'person_job':person_job,
#             'person_address':person_address
#         }*/

class case_info(models.Model):
    case_no = models.CharField(verbose_name="文件编号",max_length=50)
    case_content = models.TextField(verbose_name="文件内容",max_length=2000)
    person_name = models.CharField(verbose_name="姓名",max_length=20, blank=True)
    person_type = models.CharField(verbose_name="角色类型",choices=(('被告人', '被告人'),("罪犯","罪犯"),("其他","其他")),max_length=10,blank=True)
    person_nation = models.CharField(verbose_name="民族",max_length=20, blank=True)
    person_birthday = models.CharField(verbose_name="出生日期",max_length=20, blank=True)
    person_age = models.CharField(verbose_name="年龄",max_length=10,blank=True)
    person_sex = models.CharField(verbose_name="性别",max_length=10,choices=(('男','男'), ('女','女'),("未知",'未知')),blank=True)
    person_job = models.CharField(verbose_name="职业",max_length=10,blank=True)
    person_address = models.CharField(verbose_name="户籍",max_length=20,blank=True)
    person_edu = models.CharField(verbose_name="文化程度",max_length=20,blank=True)
    result_type = models.CharField(verbose_name="判决类型",max_length=10,blank=True)
    #result_type,penalty_name ,penalty_type ,penalty_content, penalty_addtion_money, penalty_addtion_politics
    penalty_name = models.CharField(verbose_name='罪名', max_length=20,blank=True)
    penalty_content = models.CharField(verbose_name='刑期', max_length=20,blank=True)
    penalty_addition_money = models.CharField(verbose_name='罚金',max_length=20,blank=True)
    penalty_compensate_money = models.CharField(verbose_name="民事赔偿",max_length=20,blank=True)
    penalty_addition_politics = models.CharField(verbose_name='政治权利',max_length=20,blank=True)
    arrest_date = models.CharField(verbose_name="逮捕日期",max_length=20,blank=True)

    def __str__(self):
        return self.case_no

    class Meta:
        verbose_name = "文书信息"
        verbose_name_plural = verbose_name
        app_label = "wenshu"
        db_table = "wenshu_info"


class apply_laws(models.Model):
    case = models.ForeignKey(case_info, on_delete=models.CASCADE, related_name='law_case_no')
    case_no = models.CharField(verbose_name="文件编号",max_length=50)
    law_item = models.CharField(verbose_name='条', max_length=20,blank=True)
    law_item_second = models.CharField(verbose_name='款',max_length=20,blank=True)
    law_item_content = models.CharField(verbose_name='适用情节', max_length=100,blank=True)
    def __str__(self):
        if self.law_item_second:
            return str(self.law_item)+str(self.law_item_second)
        else:
            return str(self.law_item)

    class Meta:
        verbose_name = "法定情节"
        verbose_name_plural = verbose_name
        app_label = "wenshu"
        db_table = "wenshu_apply_laws"


