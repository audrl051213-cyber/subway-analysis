from pathlib import Path
import matplotlib.pyplot as plt


plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def plot_comparison(data1, data2, label1, label2,
                    title, filename):
    """두 시간대별 데이터를 선 그래프로 비교한다."""

    plt.figure(figsize=(14, 6))

    plt.plot(data1.index, data1.values, label=label1)
    plt.plot(data2.index, data2.values, label=label2)

    plt.title(title)
    plt.xlabel("시간대")
    plt.ylabel("하루 평균 인원 (명)")

    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / filename, dpi=300)
    plt.close()


def plot_bar(data, title, filename, ylabel="인원 (명)"):
    """막대그래프를 생성하고 저장한다."""

    plt.figure(figsize=(14, 6))

    plt.bar(data.index, data.values)

    plt.title(title)
    plt.xlabel("역명")
    plt.ylabel(ylabel)
    plt.ticklabel_format(style="plain", axis="y")

    plt.ticklabel_format(style="plain", axis="y")
    plt.ticklabel_format(style="plain", axis="y")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / filename, dpi=300)
    plt.close()


def plot_net_flow(net_flow, title, filename):
    """순유입·순유출을 색상으로 구분한다."""

    colors = [
        "blue" if value > 0 else "red"
        for value in net_flow.values
    ]

    plt.figure(figsize=(14, 6))

    plt.bar(net_flow.index, net_flow.values, color=colors)
    plt.axhline(0, color="black", linewidth=0.8)

    plt.title(title)
    plt.xlabel("시간대")
    plt.ylabel("순유입 인원 (명)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / filename, dpi=300)
    plt.close()