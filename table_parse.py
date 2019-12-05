from bs4 import BeautifulSoup

table_page_url = "http://jwgl.csuft.edu.cn/jsxsd/xskb/xskb_list.do"


def parse_table(_session):
    html_content = _session.get(table_page_url).text

    def resolve_segment(html_data, class_count):
        html_data = str(html_data)
        day_of_week = str((class_count + 1) % 7)
        period = str(int((class_count + 1) / 7) + 1)
        if html_data.__contains__("<div") and html_data.index("<div") == 0:  # 被 seg 分割的前部分
            front = html_data.split('">')
            if not front[3].split('(周)')[0].__contains__(','):  # 未被 , 打断
                if not front[3].split('(周)')[0].__contains__('-'):
                    start = end = front[3].split('(周)')[0]
                else:
                    start = front[3].split('(周)')[0].split("-")[0]
                    end = front[3].split('(周)')[0].split("-")[1]
                data = {"subject": front[1].split('<br/>')[0], "teacher": front[2].split('</font>')[0],
                        "start": start, "end": end,
                        "place": front[4].split('</font>')[0], "day_of_week": day_of_week, "period": period}
                info = [data]
                return info
            # TODO: 处理 '1-6,8,10-17' 这种情况（脏话）
            elif (front[3].split('(周)')[0].count(",") == 1):  # 课程周次只被 ',' 打断过一次
                tmp = front
                j = front[3].split('(周)')[0]
                low = j.split(",")[0]
                low_start = low.split("-")[0]
                low_end = low.split("-")[1]
                high = j.split(",")[1]
                high_start = high.split("-")[0]
                high_end = high.split("-")[1]
                subject = tmp[1].split('<br/>')[0]
                teacher = tmp[2].split('</font>')[0]
                place = tmp[4].split('</font>')[0]
                low_info = {"subject": subject, "teacher": teacher, "start": low_start, "end": low_end,
                            "place": place,
                            "day_of_week": day_of_week, "period": period}
                high_info = {"subject": subject, "teacher": teacher, "start": high_start,
                             "end": high_end, "place": place,
                             "day_of_week": day_of_week, "period": period}
                info = [low_info, high_info]
                return info
        else:
            subject = html_data.split('<br/>')[1]
            teacher = html_data.split('">')[1].split('</font>')[0]
            week = html_data.split('">')[2].split('(周)')[0]
            place = (html_data.split("</font>")[2]).split('title="教室">')[1]
            if week.__contains__(',') and week.count(',') == 1:  # TODO: 处理 '1-6,8,10-17' 这种情况（脏话）
                low = week.split(',')[0]
                high = week.split(',')[1]
                low_start = low.split('-')[0]
                low_end = low.split('-')[1]
                high_start = high.split("-")[0]
                high_end = high.split("-")[1]
                low_info = {"subject": subject, "teacher": teacher, "start": low_start, "end": low_end, "place": place,
                            "day_of_week": day_of_week, "period": period}
                high_info = {"subject": subject, "teacher": teacher, "start": high_start, "end": high_end,
                             "place": place, "day_of_week": day_of_week, "period": period}
                info = [low_info, high_info]
                return info
            else:
                start = week.split('-')[0]
                end = week.split('-')[1]
                info = {"subject": subject, "teacher": teacher, "start": start, "end": end, "place": place,
                        "day_of_week": day_of_week, "period": period}
                return [info]

    table_data = []
    seg = '---------------------'
    class_schedule = [[0] * 7 for i in range(6)]
    bs_content = BeautifulSoup(html_content, "lxml")
    bs_content = bs_content.select(".kbcontent")
    count = 0
    for i in range(6):
        for j in range(7):
            class_schedule[i][j] = bs_content[count]
            # print(bs_content[count])
            count += 1
    # class_schedule 是 6 * 7 的列表
    class_count = 0
    for i in class_schedule:
        for j in i:
            if str(j).count(seg) == 0:  # 单元格内不含 '---------------------'
                if str(j).split('style="display: none;">')[1][0] != '\xa0':  # 单元格内有内容才进行处理
                    j = str(j).split('">')
                    # print(j)
                    if not j[3].split('(周)')[0].__contains__(','):  # 如果周次不像 '2-8,10-18(周)' 这样被考试周打断，则进行常规处理
                        if not j[3].split('(周)')[0].__contains__('-'):  # 某课只上一周的情况（脏话），比如: "结构力学 盛翔教授 18(周)"
                            start, end = j[3].split('(周)')[0]
                        else:
                            start = j[3].split('(周)')[0].split("-")[0]
                            end = j[3].split('(周)')[0].split("-")[1]
                        info = {"subject": j[1].split('<br/>')[0], "teacher": j[2].split('</font>')[0], "start": start,
                                "end": end, "place": j[4].split('</font>')[0],
                                "day_of_week": str((class_count + 1) % 7),
                                "period": str(int((class_count + 1) / 7) + 1)}
                        table_data.append(info)
                    else:  # 对课程周次被考试周打断的处理
                        tmp = j
                        j = j[3].split('(周)')[0]
                        low = j.split(",")[0]
                        low_start = low.split("-")[0]
                        low_end = low.split("-")[1]
                        high = j.split(",")[1]
                        high_start = high.split("-")[0]
                        high_end = high.split("-")[1]
                        subject = tmp[1].split('<br/>')[0]
                        teacher = tmp[2].split('</font>')[0]
                        place = tmp[4].split('</font>')[0]
                        day_of_week = str((class_count + 1) % 7)
                        period = str(int((class_count + 1) / 7) + 1)
                        low_info = {"subject": subject, "teacher": teacher, "start": low_start, "end": low_end,
                                    "place": place,
                                    "day_of_week": day_of_week, "period": period}
                        table_data.append(low_info)
                        high_info = {"subject": subject, "teacher": teacher, "start": high_start,
                                     "end": high_end, "place": place,
                                     "day_of_week": day_of_week, "period": period}
                        table_data.append(high_info)
            else:
                front = str(j).split(seg)[0]  # front
                end = str(j).split(seg)[1]
                front_data = resolve_segment(front, class_count)
                for i in front_data:
                    table_data.append(i)
                end_data = resolve_segment(end, class_count)
                for i in end_data:
                    table_data.append(i)
            class_count += 1
    # for i in table_data:
    #     print(i)
    return table_data
