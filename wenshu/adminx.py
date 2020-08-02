import xadmin
from wenshu.models import case_info, apply_laws
from xadmin.layout import Main, Side, Fieldset, Row, AppendedText

@xadmin.sites.register(case_info)
class case_infoAdmin(object):
    # list_display = ['case_no', 'person_type','person_type', 'person_birthday']
    search_fields =["case_no"]
    show_full_result_count = False
    list_per_page = 50


    class apply_lawsInline(object):
        model = apply_laws
        extra = 0

    inlines = [apply_lawsInline]

    # def show_apply_law(self,obj):
    #     if obj.apply_law.all():
    #         return [law.law_item for law in obj.apply_law.all()]
    #     else :
    #         return None
    readonly_fields = ['case_no',]

    form_layout = (
        Main(
            Fieldset('案件编号',
                     'case_no',
                     ),
            Fieldset('正文',
                     'case_content',
                     ),
    ),
        Side(
            Fieldset('角色信息',
                     "person_name", "person_type",
                     "person_birthday", "person_sex",
                     "person_job", "person_edu",
                     "person_nation", "person_address",
                     "person_age","arrest_date"
                     ),
            Fieldset('判决结果',
                     "result_type", "penalty_name",
                     "penalty_content",
                     "penalty_addition_money",
                     "penalty_addition_politics",
                     "penalty_compensate_money"
                     ),
        )
        )

