from pathlib import Path

from data_loader import load_data
from analysis import (
    calculate_station_avg,
    calculate_line_avg,
    calculate_station_totals,
    calculate_net_flow,
    compare_weekday_weekend,
)
from visualization import (
    plot_comparison,
    plot_bar,
    plot_net_flow,
)


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "서울교통공사_역별 일별 시간대별 승하차인원_20251231.csv"
)


def main():
    # 1. 데이터 불러오기
    df = load_data(DATA_PATH)

    print("데이터 로딩 완료")
    print(f"데이터 크기: {df.shape}")

    # 2. 1호선 평일·주말 승차 비교
    line1_weekday = calculate_line_avg(
        df, "1호선", "승차", "weekday"
    )

    line1_weekend = calculate_line_avg(
        df, "1호선", "승차", "weekend"
    )

    plot_comparison(
        line1_weekday,
        line1_weekend,
        "평일",
        "주말",
        "1호선 평일·주말 시간대별 평균 승차 인원",
        "line1_weekday_weekend.png",
    )

    # 3. 서울역과 종각역 평일 승차 비교
    seoul_avg = calculate_station_avg(
        df, "서울역", "승차", "1호선", "weekday"
    )

    jonggak_avg = calculate_station_avg(
        df, "종각", "승차", "1호선", "weekday"
    )

    plot_comparison(
        seoul_avg,
        jonggak_avg,
        "서울역",
        "종각역",
        "서울역·종각역 평일 시간대별 평균 승차 인원",
        "seoul_jonggak_comparison.png",
    )

    # 4. 종각역 평일 승차·하차 비교
    jonggak_alighting = calculate_station_avg(
        df, "종각", "하차", "1호선", "weekday"
    )

    plot_comparison(
        jonggak_avg,
        jonggak_alighting,
        "승차",
        "하차",
        "종각역 평일 시간대별 평균 승하차 인원",
        "jonggak_boarding_alighting.png",
    )

    # 5. 종각역 순유입·순유출
    net_flow = calculate_net_flow(
        jonggak_avg,
        jonggak_alighting,
    )

    plot_net_flow(
        net_flow,
        "종각역 평일 시간대별 순유입·순유출",
        "jonggak_net_flow.png",
    )

    # 6. 종각역 평일·주말 승차 비교
    jonggak_weekend = calculate_station_avg(
        df, "종각", "승차", "1호선", "weekend"
    )

    plot_comparison(
        jonggak_avg,
        jonggak_weekend,
        "평일",
        "주말",
        "종각역 평일·주말 시간대별 평균 승차 인원",
        "jonggak_weekday_weekend.png",
    )

    # 7. 평일·주말 차이 분석
    difference, decrease_rate = compare_weekday_weekend(
        jonggak_avg,
        jonggak_weekend,
    )

    max_diff_time = difference.idxmax()
    max_diff_count = difference.max()
    rate = decrease_rate[max_diff_time]

    print("\n[종각역 분석 결과]")
    print(f"평일 최대 승차 시간: {jonggak_avg.idxmax()}")
    print(f"주말 최대 승차 시간: {jonggak_weekend.idxmax()}")

    print(
        f"평일과 주말의 차이가 가장 큰 시간대는 "
        f"{max_diff_time}입니다."
    )

    print(
        f"평일이 주말보다 하루 평균 "
        f"{max_diff_count:,.0f}명 많으며, "
        f"주말 승차 인원은 평일 대비 "
        f"{rate:.1f}% 적습니다."
    )

    # 8. 1호선 역별 누적 승차 인원 TOP 10
    station_totals = calculate_station_totals(
        df, "1호선"
    )

    top10 = station_totals.head(10)

    plot_bar(
        top10,
        "2025년 1호선 역별 누적 승차 인원 TOP 10",
        "line1_top10_stations.png",
        ylabel="누적 승차 인원 (명)",
    )

    print("\n[1호선 승차 인원 TOP 10]")
    print(top10)

    print("\n분석 완료! results 폴더를 확인하세요.")


if __name__ == "__main__":
    main()