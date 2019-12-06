import datetime

start_year = 2019
start_month = 9
start_day = 2
school_term_start = datetime.date(start_year, start_month, start_day)

start_time = ['08:00', '09:55', '14:00', '15:55', '19:00']
end_time = ['09:40', '11:35', '15:40', '17:35', '20:40']
week_name = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']


def info_to_ics(class_info, username):
    VCALENDAR = '''BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:%(username)s 的课程表
X-WR-TIMEZONE:Asia/Shanghai
X-WR-CALDESC:%(username)s 的课程表
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
X-LIC-LOCATION:Asia/Shanghai
BEGIN:STANDARD
TZOFFSETFROM:+0800
TZOFFSETTO:+0800
TZNAME:CST
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE''' % {'username': username}
    file = open('课程表.ics', 'w', encoding="utf-8")
    file.write(VCALENDAR)
    for info in class_info:
        vevent = '\nBEGIN:VEVENT\n'
        # 课程开始日期
        class_start_date = school_term_start + datetime.timedelta(weeks=int(info['start']) - 1) + datetime.timedelta(
            days=int(info['day_of_week']) - 1)
        # 课程开始时间
        class_start_time = datetime.datetime.strptime(start_time[int(info['period']) - 1], '%H:%M').time()
        # 课程开始 datetime
        class_start_datetime = datetime.datetime.combine(class_start_date, class_start_time)
        # 课程结束时间
        class_end_time = datetime.datetime.strptime(end_time[int(info['period']) - 1], '%H:%M').time()
        # 课程结束 datetime
        class_end_datetime = datetime.datetime.combine(class_start_date, class_end_time)
        vevent += 'DTSTART;TZID=Asia/Shanghai:{class_start_datetime}\n'.format(
            class_start_datetime=class_start_datetime.strftime('%Y%m%dT%H%M%S'))
        vevent += 'DTEND;TZID=Asia/Shanghai:{class_end_datetime}\n'.format(
            class_end_datetime=class_end_datetime.strftime('%Y%m%dT%H%M%S'))
        # 循环 TODO: 单双周
        # count 循环次数 interval 间隔 byday 日程所在星期
        count = int(info['end']) - int(info['start']) + 1
        interval = 0
        byday = week_name[int(info['day_of_week']) - 1]
        vevent += 'RRULE:FREQ=WEEKLY;WKST=MO;COUNT={count};INTERVAL={interval};BYDAY={byday}\n'.format(
            count=count, interval=interval, byday=byday)
        # 地点
        vevent += ('LOCATION:' + info['place'] + '\n')
        # 名称
        vevent += ('SUMMARY:' + info['subject'] + '\n')
        vevent += 'END:VEVENT\n'
        file.write(vevent)
    file.write('END:VCALENDAR')
    file.close()
    print("OK: 课程表.ics")
