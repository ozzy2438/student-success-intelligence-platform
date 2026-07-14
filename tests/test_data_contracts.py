from pathlib import Path

import pandas as pd

from src.config import SYNTHETIC_DIR


def test_student_keys_are_unique_after_generation():
    students_path = SYNTHETIC_DIR / "students.csv"
    assert Path(students_path).exists(), "Run `python -m src.generate_synthetic_data` first."
    students = pd.read_csv(students_path)
    assert students["student_key"].notna().all()
    assert students["student_key"].is_unique


def test_attendance_is_valid_after_generation():
    attendance = pd.read_csv(SYNTHETIC_DIR / "attendance.csv")
    assert attendance["attendance_rate"].between(0, 1).all()
