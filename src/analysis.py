import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Malgun Gothic"

df = pd.read_csv("data/서울교통공사_역별 일별 시간대별 승하차인원_20251231.csv", encoding="cp949")

line1_boarding = df[(df["호선"] == "1호선") & (df["승하차구분"] == "승차")].copy()

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

plt.figure(figsize=(20,6))
plt.bar(top10.index, top10.values)
plt.title("2025년 서울 지하철 1호선 상위 10개 역 연간 승차 인원")
plt.xlabel("상위 10개 역")
plt.ylabel("연간 승차 인원")
plt.ticklabel_format(style="plain", axis="y")
plt.show()


# print(line1_boarding[["역명", "일일총승차인원"]].head())
