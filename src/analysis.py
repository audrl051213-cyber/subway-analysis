import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

def calculate_avg(station_data):
    time_total = station_data.loc[:, "06시이전":"24시이후"].sum(axis=0)
    day_count = station_data["수송일자"].nunique()

    avg = time_total / day_count

    return avg


df = pd.read_csv("data/서울교통공사_역별 일별 시간대별 승하차인원_20251231.csv", encoding="cp949")

# df = df.dropna(how="all")
# print(df.shape)

# total = df.duplicated(subset=["수송일자", "호선", "역번호", "승하차구분"]).sum()
# print(total)

df["수송일자"] = pd.to_datetime(df["수송일자"])

# print(df["수송일자"].dtype)
# print(df["수송일자"].head())

# df["요일번호"] = df["수송일자"].dt.day_of_week
# print(df[["수송일자", "요일번호"]].head(10))
# weekday_df = df[df["요일번호"] < 5]
# weekend_df = df[df["요일번호"] >= 5]
# print("평일 데이터:", weekday_df.shape)
# print("주말 데이터:", weekend_df.shape)




line1_boarding = df[(df["호선"] == "1호선") & (df["승하차구분"] == "승차")].copy()

line1_boarding["요일번호"] = line1_boarding["수송일자"].dt.day_of_week
line1_weekday = line1_boarding[line1_boarding["요일번호"] < 5].copy()
line1_weekend = line1_boarding[line1_boarding["요일번호"] >= 5].copy()
# print("1호선 평일 기록:", line1_weekday.shape)
# print("1호선 주말 기록:", line1_weekend.shape)

line1_weekday_total = line1_weekday.loc[:, "06시이전":"24시이후"].sum(axis=1)
line1_weekday["총승차인원"] = line1_weekday_total
# print(line1_weekday["총승차인원"].head())
weekday_daily_avg = line1_weekday["총승차인원"].sum()/261

line1_weekend_total = line1_weekend.loc[:, "06시이전":"24시이후"].sum(axis=1)
line1_weekend["총승차인원"] = line1_weekend_total
weekend_daily_avg = line1_weekend_total.sum()/104

difference_pct = (weekday_daily_avg - weekend_daily_avg)/weekend_daily_avg*100
# print(round(difference_pct, 2))
# print("평일 하루 평균:", weekday_daily_avg)
# print("주말 하루 평균:", weekend_daily_avg)

station_weekday_total = line1_weekday.groupby("역명")["총승차인원"].sum()
# print(station_weekday_total)

# print(station_weekday_total.sort_values(ascending=False).head(3))

weekday_by_time = line1_weekday.loc[:, "06시이전":"24시이후"].sum(axis=0)
weekday_count = line1_weekday["수송일자"].nunique()
weekday_avg_by_time = weekday_by_time/weekday_count

weekend_by_time = line1_weekend.loc[:, "06시이전":"24시이후"].sum(axis=0)
weekend_count = line1_weekend["수송일자"].nunique()
weekend_avg_by_time = weekend_by_time/weekend_count



# plt.figure(figsize=(16,6))
# plt.plot(weekday_avg_by_time.index, weekday_avg_by_time.values, label = "평일")
# plt.title("2025년 1호선 평일,주말 시간대별 평균 승차 인원")
# plt.xticks(rotation = 45)
# plt.plot(weekend_avg_by_time.index, weekend_avg_by_time.values, label = "주말")
# plt.legend()
# plt.xlabel("시간대")
# plt.ylabel("하루 평균 승차 인원 (명)")
# plt.show()

difference_by_time = (weekday_avg_by_time - weekend_avg_by_time)/weekend_avg_by_time*100
# print(difference_by_time.idxmax(), difference_by_time.max())

difference_people = weekday_avg_by_time - weekend_avg_by_time
# print(difference_people.idxmax(), difference_people.max())

# print(weekday_avg_by_time.loc["24시이후"])
# print(weekend_avg_by_time.loc["24시이후"])

seoul_weekday = line1_weekday[line1_weekday["역명"] == "서울역"]
seoul_weekday_time = seoul_weekday.loc[:, "06시이전" : "24시이후"].sum(axis=0)
seoul_weekday_count = seoul_weekday["수송일자"].nunique()
seoul_weekday_avg = seoul_weekday_time/seoul_weekday_count

# print(seoul_weekday_avg.idxmax(), seoul_weekday_avg.max())

jonggak_weekday = line1_weekday[line1_weekday["역명"] == "종각"]
jonggak_weekday_time = jonggak_weekday.loc[:, "06시이전" : "24시이후"].sum(axis=0)
jonggak_weekday_count = jonggak_weekday["수송일자"].nunique()
jonggak_weekday_avg = jonggak_weekday_time/jonggak_weekday_count

# print(jonggak_weekday_avg.idxmax(), jonggak_weekday_avg.max())

# plt.figure(figsize=(16,6))
# plt.plot(seoul_weekday_avg.index, seoul_weekday_avg.values, label = "서울역")
# plt.plot(jonggak_weekday_avg.index, jonggak_weekday_avg.values, label = "종각역")
# plt.legend()
# plt.xticks(rotation = 45)
# plt.xlabel("시간대")
# plt.ylabel("평균 승차 인원")
# plt.title("서울역과 종각역 평일 시간대별 평균 승차 인원")
# plt.show()

jonggak_alighting = df[(df["승하차구분"] == "하차") & (df["호선"] == "1호선") & (df["역명"] == "종각")]
jonggak_alighting_weekday = jonggak_alighting[jonggak_alighting["수송일자"].dt.day_of_week < 5]
jonggak_alighting_weekday_time = jonggak_alighting_weekday.loc[:, "06시이전" : "24시이후"].sum(axis = 0)
jonggak_alighting_weekday_count = jonggak_alighting_weekday["수송일자"].nunique()
jonggak_alighting_avg = jonggak_alighting_weekday_time/jonggak_alighting_weekday_count

# plt.figure(figsize=(16,6))
# plt.plot(jonggak_alighting_avg.index, jonggak_alighting_avg.values, label = "종각역 하차")
# plt.plot(jonggak_weekday_avg.index, jonggak_weekday_avg.values, label = "종각역 승차")
# plt.legend()
# plt.xticks(rotation = 45)
# plt.xlabel("시간대")
# plt.ylabel("평균 인원")
# plt.title("종각역 평일 시간대별 평균 승하차 인원")
# plt.show()

jonggak_net_flow = jonggak_alighting_avg - jonggak_weekday_avg
print(jonggak_net_flow.idxmax(), jonggak_net_flow.max())
print(jonggak_net_flow.idxmin(), jonggak_net_flow.min())


# colors = ["blue" if x > 0 else "red" for x in jonggak_net_flow]
# plt.bar(jonggak_net_flow.index, jonggak_net_flow.values, color = colors)
# plt.xlabel("시간대")
# plt.ylabel("순유입 인원")
# plt.title("종각역 평일 시간대별 순유입 인원")
# plt.xticks(rotation = 45)
# plt.show()

seoul_weekday_avg = calculate_avg(seoul_weekday)
jonggak_weekday_avg = calculate_avg(jonggak_weekday)

print(seoul_weekday_avg, jonggak_weekday_avg)

time_columns = ['06시이전', '06-07시간대',
       '07-08시간대', '08-09시간대', '09-10시간대', '10-11시간대', '11-12시간대', '12-13시간대',
       '13-14시간대', '14-15시간대', '15-16시간대', '16-17시간대', '17-18시간대', '18-19시간대',
       '19-20시간대', '20-21시간대', '21-22시간대', '22-23시간대', '23-24시간대', '24시이후']

daily_total = line1_boarding[time_columns].sum(axis = 1)
# print(daily_total.head())
line1_boarding["일일총승차인원"] = daily_total
station_total = line1_boarding.groupby("역명")["일일총승차인원"].sum()
# print(station_total)

# print("가장 승차 인원이 많은 역:" + station_total.idxmax())
# print("그 역의 연간 총 승차 인원" + str(station_total.max()))

top10 = station_total.sort_values(ascending = False).head(10)
# print(top10)

# plt.figure(figsize=(20,6))
# plt.bar(top10.index, top10.values)
# plt.title("2025년 서울 지하철 1호선 상위 10개 역 연간 승차 인원")
# plt.xlabel("상위 10개 역")
# plt.ylabel("연간 승차 인원")
# plt.ticklabel_format(style="plain", axis="y")
# plt.show()


# seoul_station = line1_boarding[line1_boarding["역명"] == "서울역"]
# print(seoul_station.head(5))
# seoul_by_time = seoul_station[time_columns].sum(axis=0)
# print(seoul_by_time)
# print(f"승차 인원이 가장 많은 시간대: {seoul_by_time.idxmax()}")
# print(f"해당 시간대 승차 인원: {seoul_by_time.max():,.0f}명")
# plt.figure(figsize= (16,6))
# plt.bar(seoul_by_time.index, seoul_by_time.values)
# plt.title("2025년 서울역 시간대별 승차 인원")
# plt.xlabel("시간대")
# plt.ylabel("승차 인원")
# plt.xticks(rotation=45)
# plt.show()
# print(line1_boarding[["역명", "일일총승차인원"]].head())
