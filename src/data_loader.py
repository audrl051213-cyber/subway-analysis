from pathlib import Path
import pandas as pd


def load_data(file_path):
    """CSV 파일을 불러오고 날짜 데이터를 변환한다."""
    file_path = Path(file_path)

    df = pd.read_csv(file_path, encoding="cp949")
    df["수송일자"] = pd.to_datetime(df["수송일자"])

    return df