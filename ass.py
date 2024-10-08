from collections import defaultdict
import math
def solution(fees, records):
    a, b, c, d = fees
    dict = defaultdict(tuple)
    for record in records:
        t, n, inout = record.split(" ")
        if dict[n] == (): # 초기화
            dict[n] = (t, 0) # 시각과 총 이용 시간. 요금은 나중에 계산
            continue
        if dict[n][0] == "": # 입출 끝났는데 또 입 했을 때
            dict[n] = (t, dict[n][1])
            continue
        h, m = map(int, t.split(":"))
        hh, mm = map(int, dict[n][0].split(":"))

        use = (h-hh)*60+m-mm

        dict[n] = ("", use)

    answer = []
    for car, (intime, usetime) in dict.items():
        if intime != "":
            hh, mm = map(int, intime.split(":"))
            usetime += ((23-hh)*60+59-mm)
        tot = b+math.ceil((usetime-a)/c)*d if usetime > a else b
        answer.append((car, tot))

    answer.sort()
    for i in range(len(answer)):
        answer[i] = answer[i][1]

    return answer