import pandas as pd


TIME_COLUMNS = [
    "06시이전",
    "06-07시간대",
    "07-08시간대",
    "08-09시간대",
    "09-10시간대",
    "10-11시간대",
    "11-12시간대",
    "12-13시간대",
    "13-14시간대",
    "14-15시간대",
    "15-16시간대",
    "16-17시간대",
    "17-18시간대",
    "18-19시간대",
    "19-20시간대",
    "20-21시간대",
    "21-22시간대",
    "22-23시간대",
    "23-24시간대",
    "24시이후",
]


def filter_data(df, line_name=None, station_name=None,
                boarding_type=None, day_type=None):
    """호선, 역, 승하차, 평일·주말 조건으로 데이터를 필터링한다."""

    if day_type not in (None, "weekday", "weekend"):
        raise ValueError("day_type은 weekday 또는 weekend만 가능합니다.")

    result = df.copy()

    if line_name is not None:
        result = result[result["호선"] == line_name]

    if station_name is not None:
        result = result[result["역명"] == station_name]

    if boarding_type is not None:
        result = result[result["승하차구분"] == boarding_type]

    if day_type == "weekday":
        result = result[result["수송일자"].dt.dayofweek < 5]

    elif day_type == "weekend":
        result = result[result["수송일자"].dt.dayofweek >= 5]

    return result


def calculate_avg(station_data):
    """시간대별 하루 평균 이용 인원을 계산한다."""

    if station_data.empty:
        return None

    day_count = station_data["수송일자"].nunique()

    if day_count == 0:
        return None

    time_total = station_data[TIME_COLUMNS].sum(axis=0)

    return time_total / day_count


def calculate_station_avg(df, station_name, boarding_type,
                          line_name, day_type):
    """특정 역의 시간대별 평균 승하차 인원을 반환한다."""

    station_data = filter_data(
        df,
        line_name=line_name,
        station_name=station_name,
        boarding_type=boarding_type,
        day_type=day_type,
    )

    return calculate_avg(station_data)


def calculate_line_avg(df, line_name, boarding_type, day_type):
    """특정 호선의 시간대별 하루 평균 이용 인원을 계산한다."""

    line_data = filter_data(
        df,
        line_name=line_name,
        boarding_type=boarding_type,
        day_type=day_type,
    )

    return calculate_avg(line_data)


def calculate_station_totals(df, line_name, boarding_type="승차"):
    """역별 전체 기간의 누적 이용 인원을 계산한다."""

    data = filter_data(
        df,
        line_name=line_name,
        boarding_type=boarding_type,
    ).copy()

    data["일일총인원"] = data[TIME_COLUMNS].sum(axis=1)

    return (
        data.groupby("역명")["일일총인원"]
        .sum()
        .sort_values(ascending=False)
    )


def calculate_net_flow(boarding_avg, alighting_avg):
    """순유입 인원 = 하차 인원 - 승차 인원."""

    return alighting_avg - boarding_avg


def compare_weekday_weekend(weekday_avg, weekend_avg):
    """평일과 주말의 인원 차이 및 감소율을 계산한다."""

    difference = weekday_avg - weekend_avg

    decrease_rate = (
        difference / weekday_avg.replace(0, float("nan"))
    ) * 100

    return difference, decrease_rate
