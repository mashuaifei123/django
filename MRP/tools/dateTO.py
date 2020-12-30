import datetime
import time

def holiday(d, s="2019-01-01", e="2020-12-31"):
    hol = {"2020-01-01", "2020-01-24", "2020-01-25", "2020-01-26", "2020-01-27", "2020-01-28", "2020-01-29",
           "2020-01-30", "2020-04-04", "2020-04-05", "2020-04-06", "2020-05-01", "2020-06-25", "2020-06-26"
           "2020-06-27", "2020-10-01", "2020-10-02", "2020-10-03", "2020-10-04", "2020-10-05", "2020-10-06",
           "2020-10-07", "2020-10-08", '2019-10-01', '2019-10-02', '2019-10-03', '2019-10-04', '2019-10-05',}
    work = {"2020-01-19", "2020-02-01", "2020-06-28", "2020-09-27", "2020-10-10" }
    s1 = datetime.datetime.strptime(s, '%Y-%m-%d')
    e1 = datetime.datetime.strptime(e, '%Y-%m-%d')
    def get_week_day(d):
        week_day_dict = {
            0: '一',
            1: '二',
            2: '三',
            3: '四',
            4: '五',
            5: '六',
            6: '日',
        }
        day1 = d.weekday()
        return week_day_dict[day1]
    week = get_week_day(datetime.datetime.strptime(d, '%Y-%m-%d'))
    # weekend = {-1: '报错', 0: '工作日', 1: '休息日', 2: '节假日'}
    if not isinstance(d, str):
        print("Please input string date")
        return -1
    else:
        d1 = datetime.datetime.strptime(d, '%Y-%m-%d')
        if d1 > e1 or d1 < s1:
            print("not in 2019-2020 year")
            leb = r'<label class="label label-success">'
            leb2 = r'</label>'
            return '{}{}{}'.format(leb, d, leb2), week
        elif d in hol:
            leb = r'<label class="label label-danger">'
            leb2 = r'</label>'
            return '{}{}{}'.format(leb, d, leb2), week
        elif d in work:
            leb = r'<label class="label label-default">'
            leb2 = r'</label>'
            return '{}{}{}'.format(leb, d, leb2), week
        elif d1.weekday() in (5, 6):
            leb = r'<label class="label label-info">'
            leb2 = r'</label>'
            return '{}{}{}'.format(leb, d, leb2), week
        else:
            leb = r'<label class="label label-default">'
            leb2 = r'</label>'
            return '{}{}{}'.format(leb, d, leb2), week
    # <label class="label label-success"> 内容字符串 </label>  颜色代码label
    # .label-default灰色.label-primary 深绿蓝.label-success 绿色.label-info 蓝色 .label-warning 橙色.label-danger 红色

def Date_Year_Month_1():
    '''得到过去12个月'''
    #Python 实现得到现在时间12个月前的每个月
    # 假设现在的时间是2016年9月25日
    #得到现在的时间  得到now等于2016年9月25日
    now = datetime.datetime.now()
    #得到今年的的时间 （年份） 得到的today_year等于2016年
    today_year = now.year
    #今年的时间减去1，得到去年的时间。last_year等于2015
    last_year =  int(now.year) -1
    #得到今年的每个月的时间。today_year_months等于1 2 3 4 5 6 7 8 9，
    today_year_months = range(1,now.month+1)
    #得到去年的每个月的时间  last_year_months 等于10 11 12 
    last_year_months = range(now.month+1, 13)
    #定义列表去年的数据
    data_list_lasts = []
    #通过for循环，得到去年的时间夹月份的列表
    #先遍历去年每个月的列表
    for last_year_month in last_year_months:
        # 定义date_list 去年加上去年的每个月
        date_list = '%s-%s' % (last_year, last_year_month)
        #通过函数append，得到去年的列表
        data_list_lasts.append(date_list)
    data_list_todays = []
    #通过for循环，得到今年的时间夹月份的列表
    #先遍历今年每个月的列表
    for today_year_month in today_year_months:
        # 定义date_list 去年加上今年的每个月
        data_list = '%s-%s' % (today_year, today_year_month)
        #通过函数append，得到今年的列表
        data_list_todays.append(data_list)
    #去年的时间数据加上今年的时间数据得到年月时间列表
    data_year_month = data_list_lasts + data_list_todays
    # data_year_month.reverse()
    return data_year_month


if __name__ == "__main__":
    day = "2019-10-14"
    print(holiday(day))