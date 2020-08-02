import pymongo
import re
import nltk
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_wenshu.settings')
django.setup()
from wenshu.models import case_info, apply_laws
# 生成的表  [被告人姓名  被告人姓名  性别  类别 出生日期 民族 职业 户籍 文化程度]
# 法定情节
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

def get_person_type(content):
   result = re.search(r'(被告人|罪犯)([^,，]+)[，,]', content)
   if result is not None:
        return result.group(1)
   else :
       return None

def get_person_name(content):
   result = re.search(r'(被告人|罪犯|被执行人：|复议申请人：|上诉人（原审被告人）)([\u4e00-\u9fa5|X| （|）|：]*)[，|,|。]?', content)
   if(result is not None):
        return result.group(2)
   else:
       return None


def get_person_sex(content):

    result = re.search(r'(被告人|罪犯|被执行人：|复议申请人：)[^男|女]*([男|女])+?', content)
    if (result is not None):
        return result.group(2)
    else:
        return "未知"

def get_person_birthday(content):
    result = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)[出|生]',content)
    if(result is not  None):
        return result.group(1)
    else:
        result = re.search(r'生于(\d{4}年\d{1,2}月\d{1,2}日)', content)
        if(result is not None):
            return result.group(1)
        else:
            return  None

def get_person_age(content): #年龄
    age = None
    result = re.search(r'[，,。][\u4e00-\u9fa5]*([0-9]*岁)[，|,|。]',content[:100])
    if result:
        age = result.group(1)
    return age
def get_person_nation(content):
    result = re.search(r'[，,]([\u4e00-\u9fa5]+族)[，,。]', content)
    if result is not None:
        return result.group(1)
    else:
        return None

def get_person_edu(content):
    result = re.search(r'[,，]([\u4e00-\u9fa5]+?)(文化|毕业|肄业|文化程度)[,，。]',content)
    if result is not None:
        return result.group(1)
    else :
        result = re.search(r'[,，]文化程度([\u4e00-\u9fa5]+)[,，。]',content)
        if result is not None:
            return result.group(1)
        else:
            result = re.search(r'[,，](文盲)[,，。]', content)
            if result is not None:
                return  result.group(1)
            else:
                return None
def get_person_job(content):
    result = re.search(r'[，。,](农民|个体|无业|无职业|职工)',content)
    if result is not None:
        return result.group(1)
    else:
        return None

def get_person_address(content):
    result = re.search(r'(户籍地|户籍所在地|生于)[^\u4e00-\u9fa5]*([\u4e00-\u9fa5]*[省|市|区|县]+[\u4e00-\u9fa5]*)',content)
    # print(content)
    if result is not None:
        return result.group(2)
    else:
        result = re.search(r'[，。,]([\u4e00-\u9fa5]*[省|市|区|县][\u4e00-\u9fa5]*)人[，。,]',content)
        if result is not None:
            return result.group(1)
        else:
            return None

def get_arrest_date(content):
    arrest_date = None
    result = re.search(r'([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日.*?逮捕)', content)
    if result:
        text = result.group(1)
        data_year = re.findall(r'[0-9]{4}年',text)
        data_date = re.findall(r'[0-9]{1,2}月[0-9]{1,2}日', text)
        arrest_date = data_year[-1]+data_date[-1]
    return arrest_date

def get_result(case_no, content):
    penalty_name =None #罪名
    penalty_type =None #处罚
    penalty_content = None #
    penalty_addtion_money=None
    if re.search(r'刑初',str(case_no)) :
        result_type = '一审'
        penalty= re.search(r'\s.*被告人[\u4e00-\u9fa5]+犯([\u4e00-\u9fa5]+)[,。，]判处(拘役[\u4e00-\u9fa5]+|有期徒刑[\u4e00-\u9fa5]+|无期徒刑)' ,content)
        if penalty:
            penalty_name = penalty.group(1)
            penalty_content = penalty.group(2)
        penalty_addtion_money = re.search(r'\s被告人[\u4e00-\u9fa5]+犯.*并处罚金(.*元)', content)
        penalty_addtion_politics = re.search(r'\s被告人[\u4e00-\u9fa5]+犯.*(剥夺政治权利[\u4e00-\u9fa5]+)',content)
        if penalty_addtion_money:
            penalty_addtion_money = penalty_addtion_money.group(1)
            if (re.search(r'人民币', penalty_addtion_money)):
                penalty_addtion_money = re.search(r'人民币(.*元)', penalty_addtion_money).group(1)


    elif re.search(r'刑终',str(case_no)):
        result_type ='二审'
        #本院.*认为.*(裁定|判决)如下.*撤销.*发回.*
        penalty_name =re.search(r'\s.*诉.*维持.*原判',content)
        if penalty_name:
            penalty_name = '维持原判'
        elif re.search(r'\s.*撤销.*发回.*',content):
            penalty_name ='发回重审'
        elif re.search(r'准许上诉人[\u4e00-\u9fa5]+撤回上诉',content):
            penalty_name = '维持原判'
        else :
            penalty_name = '改判'
    else :
        result_type = None

    return (result_type,penalty_name ,penalty_content, penalty_addtion_money)
def get_penalty_addtion_politics(content):
    politics = None
    text = re.search(r'(如下.[\s\S]*审)', content)
    if text:
        content_result = text.group(1)
    elif re.search(r'(判决[\s\S]*审)', content):
        content_result = re.search(r'(判决[\s\S]*审)', content)
    else:
        content_result = ""
    if (re.search(r'政治权利\S', str(content_result))):
        politics  = re.search(r'[\u4e00-\u9fa5]*政治权利[\d]*[\u4e00-\u9fa5]*', str(content_result)).group()
    return   politics




def get_apply_laws(content):
    laws = []
    result = re.search(r'《中华人民共和国刑法》(.*)?，', content)
    if result :
        result =result.group(1)
        if re.search(r'(.*?)《',result):
            result =re.search(r'(.*?)《',result).group(1)
        if re.search(r'(.*?)规定',result):
            result = re.search(r'(.*?)规定', result).group(1)


    else:
        result =  None
    if result:
        result = re.split(r',|。|、|及|之一|和,',result)
        first = None
        second = None
        for item in result:
            if re.search(r'(第[\u4e00-\u9fa5]+条)(第[\u4e00-\u9fa5]+款)', item):
                first = re.search(r'(第[\u4e00-\u9fa5]+条)(第[\u4e00-\u9fa5]+款)', item).group(1)
                second = re.search(r'(第[\u4e00-\u9fa5]+条)(第[\u4e00-\u9fa5]+款)', item).group(2)
                laws.append((first, second))
            elif re.search(r'(第[\u4e00-\u9fa5]+条)', item):
                first = re.search(r'(第[\u4e00-\u9fa5]+条)', item).group(1)
                second = None
                laws.append((first, second))
            elif re.search(r'(第{0,1}[\u4e00-\u9fa5]+款)',item):
                first = first
                second = re.search(r'(第{0,1}[\u4e00-\u9fa5]+款)', item).group(1)
                if re.search(r'第',second) is None:
                    second = '第'+second
                laws.append((first, second))

    return laws

def get_compensate(content):
    compensate_money =None
    text = re.search(r'(如下.[\s\S]*审)',content)
    if text:
        content_result = text.group(1)
    elif re.search(r'(判决[\s\S]*审)', content):
        content_result = re.search(r'(判决[\s\S]*审)', content)
    else:
        content_result=""
    if(re.search(r'赔偿',str(content_result))):

        s = re.search(r'赔偿\S*',str(content_result)).group()
        money = re.findall(r'[\d|\.|一|二|三|四|五|六|七|八|九|十|百|千|万]+元',s)
        # print(re.findall())
        if(money):
            compensate_money = money[-1]

    return compensate_money


class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


if __name__ =='__main__':

    client = pymongo.MongoClient(host='localhost', port=27017)
    db_case = client.case
    judge_doc = db_case.judge_doc
    judge_curor = judge_doc.find()
    count = 0
    isRead = False
    for judge_i in judge_curor:
        count = count +1
        print(count)
        case_no = judge_i["case_no"]

        if(isRead):
            print(judge_i)

            print("写入" + str(case_no))
            case_content = judge_i["content"]
            content = ''
            for i in case_content:
                content += i["text"]
            content = dehtml(content)  # 判决书正文
            # case_content = dehtml(case_content)
            # person_info = judge_i["person_info"]#被告人信息
            # print(content)
            person_name = get_person_name(content)
            person_sex = get_person_sex(content)
            person_type = get_person_type(content)
            person_birthday = get_person_birthday(content)
            person_nation = get_person_nation(content)
            person_job = get_person_job(content)
            person_edu = get_person_edu(content)
            person_address = get_person_address(content)
            result_type, penalty_name, penalty_content, penalty_addition_money = get_result(case_no, content)
            arrest_date = get_arrest_date(content)
            age = get_person_age(content)
            compensate_money = get_compensate(content)
            penalty_addtion_politics = get_penalty_addtion_politics(content)

            case_info_item = case_info(case_no=case_no, case_content=content, person_name=person_name,
                                       person_sex=person_sex,
                                       person_type=person_type,
                                       person_birthday=person_birthday, person_nation=person_nation,
                                       person_job=person_job, person_edu=person_edu,
                                       person_address=person_address, result_type=result_type,
                                       penalty_name=penalty_name,
                                       penalty_content=penalty_content, penalty_addition_money=penalty_addition_money,
                                       arrest_date=arrest_date, penalty_addition_politics=penalty_addtion_politics,
                                       person_age=age, penalty_compensate_money=compensate_money
                                       )
            get_arrest_date(content)
            case_info_item.save()
            laws = get_apply_laws(content)
            for law in laws:
                if (law[0] == ""):
                    continue
                law_content = None
                if law[0] == "第六十七条":
                    if law[1] == "第一款":
                        law_content = "自首"
                    elif law[1] == "第二款":
                        law_content = "准自首"
                    elif law[1] == "第三款":
                        law_content = "坦白"
                elif law[0] == "第六十五条":
                    law_content = "罪犯"
                elif law[0] == "第六十六条":
                    law_content = "特殊罪犯"
                elif law[0] == "第六十八条":
                    law_content = "立功"
                elif law[0] == "第二十六条":
                    if law[1] == "第一款":
                        law_content = "主犯"
                    elif law[1] == "第二款":
                        law_content = "犯罪集团"
                    elif law[1] == "第三款":
                        law_content = "犯罪集团首要分子"
                elif law[0] == "第二十七条":
                    law_content = "从犯"
                elif law[0] == "第二十八条":
                    law_content = "胁从犯"
                elif law[0] == "第二十九条":
                    law_content = "教唆犯"
                elif law[0] == "第十六条":
                    law_content = "不可抗力和意外事件"
                elif law[0] == "第十七条":
                    if law[1] == "第一款":
                        law_content = "完全刑事责任（无刑事责任）"
                    elif law[1] == "第二款":
                        law_content = "相对刑事责任（14-16）"
                    elif law[1] == "第三款":
                        law_content = "减轻刑事责任（14-18）"
                elif law[0] == "第十八条":
                    if law[1] == "第一款":
                        law_content = "无刑事责任（精神病人）"
                    elif law[1] == "第二款":
                        law_content = "（间歇性精神病人）负刑事责任"
                    elif law[1] == "第三款":
                        law_content = "减轻刑事责任"
                    elif law[1] == "第四款":
                        law_content = "完全刑事责任（醉酒）"
                elif law[0] == "第二十条":
                    if law[1] == "第一款":
                        law_content = "正当防卫"
                    elif law[1] == "第二款":
                        law_content = "防卫过当"
                    elif law[1] == "第三款":
                        law_content = "无限防卫权"
                    elif law[1] == "第四款":
                        law_content = "紧急避险"
                apply_law = apply_laws(case=case_info_item, law_item=law[0], law_item_second=law[1],
                                       law_item_content=law_content, case_no=case_no)
                apply_law.save()


        if count == 5966171:
            isRead = True


