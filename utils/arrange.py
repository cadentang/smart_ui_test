#-*- encoding:UTF-8 -*-
import time
from datetime import datetime, date

RULES = 6

def convert_string_to_date(string_time):
  """把字符串类型转换为date类型"""
  if string_time[0:2] == "20":
    year = string_time[0:4]
    month = string_time[4:6]
    day= string_time[6:8]
    begin_time = date(int(year), int(month), int(day))
    return begin_time
  else :
    year = "20" + string_time[0:2]
    month = string_time[2:4]
    day = string_time[4:6]
    begin_time = date(int(year), int(month), int(day))
    return begin_time


def compare_time(now_time, string_time):
  """比较两个时间,并返回两个日期之间相差的天数"""

  if isinstance(now_time, date):
    pass
  else:
    now_time = convert_string_to_date(now_time)

  if isinstance(string_time, date):
    pass
  else:
    string_time = convert_string_to_date(string_time)
  result = now_time - string_time
  return result.days


def get_target_date(orgin_rules, orgin_date, target_date):
  """
  通过传入的原时间在规则里面的第几天和目标日期获取目标日期在规则里面的第几天
  """
  count_days = compare_time(target_date, orgin_date)
  mod = count_days % RULES
  if orgin_rules + mod <= RULES:
      target_rules = orgin_rules + mod
  else:
      target_rules = orgin_rules + mod - RULES
  return target_rules


def get_result(orgin_rules, orgin_date, target_date):
  rule_detail = ["白班1⃣️", "白班2⃣️", "小夜", "大夜", "夜休", "休"]
  index = get_target_date(orgin_rules, orgin_date, target_date)

  return "目标日期是：%s, 这天你的排班是：%s" % (target_date, rule_detail[index])


print(compare_time("20201215", "20201212")%4)
print(get_target_date(3, "20201214", "20201218"))
print(get_result(3, "20201214", "20201224"))


