from django.contrib import admin

# Register your models here.
from wenshu.models import wenshu,case_info


class case_infoAdmin(admin.ModelAdmin):
    list_display = ('case_no', 'person_type','person_type', 'person_birthday')
    search_fields =["case_no"]
    list_filter = ['person_sex', 'person_type' ,'person_nation']
    show_full_result_count = False
    list_per_page = 50

admin.site.register(wenshu)
admin.site.register(case_info,case_infoAdmin)
admin.site.site_header = '案件数据管理'
admin.site.site_title = '案件数据管理后台系统'