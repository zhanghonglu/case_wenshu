import re
from datetime import  date
CN_NUM = {
    '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
}

CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}


def chinese_to_arabic(cn: str) -> int:
    unit = 0  # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val


def get_date(str):
    date_result = re.search(r'(.*)年(.*)月(.*)日',str)
    year =int(date_result.group(1))
    month = int(date_result.group(2))
    day = int(date_result.group(3))
    if day >31:
        day = 1
    try:
        da = date(year, month, day)
    except :
        da =None
    return da

def get_month_length(str):
    year = 0
    month = 0
    if (re.search(r'([一二三四五六七八九十百千万两亿壹贰叁肆伍陆柒捌玖貮]+)年', str)):
        year = int(chinese_to_arabic(re.search(r'([一二三四五六七八九十百千万两亿壹贰叁肆伍陆柒捌玖貮]+)年', str).group(1)))
    if (re.search(r'([一二三四五六七八九十百千万两亿壹贰叁肆伍陆柒捌玖貮]+)个月', str)):
        month = int(chinese_to_arabic(re.search(r'([一二三四五六七八九十百千万两亿壹贰叁肆伍陆柒捌玖貮]+)个月', str).group(1)))
    return year*12 + month

def get_age_data(data_birth, data_arrest):
   day = (data_arrest - data_birth).days
   age = int(day/365.0)
   return age





if __name__ == '__main__':
    print(chinese_to_arabic('二千'))