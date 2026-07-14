"""Generate realistic, fully synthetic higher-education analytics source data.

The generator deliberately creates coherent relationships across SIS, LMS,
assessment, attendance and intervention records. It contains no real student
or institutional data and produces deterministic output for reproducibility.
"""

from __future__ import annotations

import hashlib
from datetime import date, timedelta

import numpy as np
import pandas as pd

from src.config import RANDOM_SEED, SYNTHETIC_DIR

N_STUDENTS = 2_400
WEEKS_PER_TERM = 12
TERMS = [
    {"term_id": "2025S1", "term_name": "Semester 1 2025", "start_date": "2025-02-24"},
    {"term_id": "2025S2", "term_name": "Semester 2 2025", "start_date": "2025-07-21"},
    {"term_id": "2026S1", "term_name": "Semester 1 2026", "start_date": "2026-02-23"},
]

PROGRAMS = [
    ("P001", "Business", "Business and Law", "Bachelor of Business Analytics", "Undergraduate"),
    ("P002", "Business", "Business and Law", "Master of Business Analytics", "Postgraduate"),
    ("P003", "Engineering", "Computing Technologies", "Bachelor of Information Technology", "Undergraduate"),
    ("P004", "Engineering", "Computing Technologies", "Master of Data Science", "Postgraduate"),
    ("P005", "Design", "Design and Creative Practice", "Bachelor of Communication Design", "Undergraduate"),
    ("P006", "Health", "Health and Biomedical Sciences", "Bachelor of Health Science", "Undergraduate"),
    ("P007", "Vocational Education", "Digital Technologies", "Diploma of Information Technology", "Vocational"),
    ("P008", "Social Sciences", "Global, Urban and Social Studies", "Bachelor of Social Science", "Undergraduate"),
]

COURSES = [
    ("C101", "Data Analytics Foundations", "Business", 12, "Blended", "High"),
    ("C102", "Business Statistics", "Business", 12, "Blended", "High"),
    ("C103", "Database Concepts", "Business", 12, "Online", "Medium"),
    ("C201", "Programming Fundamentals", "Engineering", 12, "Blended", "High"),
    ("C202", "Data Structures", "Engineering", 12, "Campus", "High"),
    ("C203", "Cloud Data Platforms", "Engineering", 12, "Online", "Medium"),
    ("C301", "Design Research Methods", "Design", 12, "Campus", "Medium"),
    ("C302", "Digital Prototyping", "Design", 12, "Campus", "Medium"),
    ("C401", "Public Health Foundations", "Health", 12, "Blended", "Medium"),
    ("C402", "Evidence in Health Practice", "Health", 12, "Online", "High"),
    ("C501", "IT Service Management", "Vocational Education", 12, "Campus", "Low"),
    ("C502", "Cyber Security Essentials", "Vocational Education", 12, "Blended", "High"),
    ("C601", "Research Methods", "Social Sciences", 12, "Campus", "Medium"),
    ("C602", "Policy and Society", "Social Sciences", 12, "Online", "Medium"),
]

COURSE_BY_FACULTY = {}
for course in COURSES:
    COURSE_BY_FACULTY.setdefault(course[2], []).append(course)


def sigmoid(value: np.ndarray | float) -> np.ndarray | float:
    return 1 / (1 + np.exp(-value))


def stable_key(prefix: str, value: int) -> str:
    digest = hashlib.sha256(f"{prefix}-{value}-synthetic-only".encode()).hexdigest()[:12]
    return f"{prefix}_{digest}"


def term_week_date(start_date: str, week_number: int) -> str:
    return (date.fromisoformat(start_date) + timedelta(days=(week_number - 1) * 7)).isoformat()


def build_reference_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    programs = pd.DataFrame(
        PROGRAMS,
        columns=["program_id", "faculty", "school", "program_name", "program_level"],
    )
    courses = pd.DataFrame(
        COURSES,
        columns=[
            "course_id",
            "course_name",
            "faculty",
            "credit_points",
            "delivery_mode",
            "assessment_intensity",
        ],
    )
    terms = pd.DataFrame(TERMS)
    return programs, courses, terms


def build_students(rng: np.random.Generator, programs: pd.DataFrame) -> pd.DataFrame:
    programme_weights = np.array([0.18, 0.08, 0.20, 0.08, 0.12, 0.14, 0.08, 0.12])
    programme_ids = rng.choice(programs["program_id"].to_numpy(), size=N_STUDENTS, p=programme_weights)
    lookup = programs.set_index("program_id")

    study_load = rng.choice(["Full-time", "Part-time"], size=N_STUDENTS, p=[0.78, 0.22])
    delivery_preference = rng.choice(["Campus", "Blended", "Online"], size=N_STUDENTS, p=[0.35, 0.42, 0.23])
    equity_group = rng.choice(
        ["Not disclosed", "First in family", "Low SES", "Regional/Remote", "Disability disclosure"],
        size=N_STUDENTS,
        p=[0.62, 0.14, 0.10, 0.08, 0.06],
    )

    academic_preparedness = np.clip(rng.normal(0.0, 0.9, N_STUDENTS), -2.5, 2.5)
    digital_confidence = np.clip(rng.normal(0.1, 0.85, N_STUDENTS), -2.5, 2.5)
    external_pressure = np.clip(rng.normal(0.0, 0.85, N_STUDENTS), -2.5, 2.5)
    prior_failures = np.where(
        rng.random(N_STUDENTS) < sigmoid(-1.65 - 0.8 * academic_preparedness + 0.45 * external_pressure),
        rng.integers(1, 3, N_STUDENTS),
        0,
    )

    student_rows = []
    for index in range(N_STUDENTS):
        programme = lookup.loc[programme_ids[index]]
        student_rows.append(
            {
                "student_key": stable_key("STU", index + 1),
                "program_id": programme_ids[index],
                "faculty": programme["faculty"],
                "study_level": programme["program_level"],
                "study_load": study_load[index],
                "delivery_preference": delivery_preference[index],
                "equity_group": equity_group[index],
                "commencement_term": rng.choice(["2025S1", "2025S2", "2026S1"], p=[0.35, 0.35, 0.30]),
                "prior_course_failures": int(prior_failures[index]),
                "academic_preparedness_latent": round(float(academic_preparedness[index]), 4),
                "digital_confidence_latent": round(float(digital_confidence[index]), 4),
                "external_pressure_latent": round(float(external_pressure[index]), 4),
            }
        )
    return pd.DataFrame(student_rows)


def build_enrolments(
    rng: np.random.Generator,
    students: pd.DataFrame,
    terms: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[tuple[str, str], list[str]]]:
    enrolment_rows: list[dict] = []
    enrolled_courses: dict[tuple[str, str], list[str]] = {}

    for student in students.itertuples(index=False):
        commencement_index = [term["term_id"] for term in TERMS].index(student.commencement_term)
        for term in TERMS[commencement_index:]:
            course_pool = COURSE_BY_FACULTY.get(student.faculty, COURSES)
            course_count = 3 if student.study_load == "Full-time" else 2
            selected = rng.choice(course_pool, size=min(course_count, len(course_pool)), replace=False)
            key = (student.student_key, term["term_id"])
            enrolled_courses[key] = []
            for course in selected:
                enrolment_rows.append(
                    {
                        "enrolment_id": stable_key("ENR", len(enrolment_rows) + 1),
                        "student_key": student.student_key,
                        "course_id": course[0],
                        "term_id": term["term_id"],
                        "enrolment_status": "Enrolled",
                        "credit_points": course[3],
                    }
                )
                enrolled_courses[key].append(course[0])
    return pd.DataFrame(enrolment_rows), enrolled_courses


def build_assessments() -> pd.DataFrame:
    rows = []
    for course_id, _, _, _, _, intensity in COURSES:
        schedule = [("Quiz", 3, 20), ("Assignment", 6, 35), ("Project", 9, 45)]
        if intensity == "Low":
            schedule = [("Quiz", 4, 25), ("Assignment", 8, 35), ("Project", 11, 40)]
        for assessment_type, due_week, weight in schedule:
            rows.append(
                {
                    "assessment_id": f"{course_id}_{assessment_type.upper()}_{due_week}",
                    "course_id": course_id,
                    "assessment_type": assessment_type,
                    "due_week": due_week,
                    "weight": weight,
                }
            )
    return pd.DataFrame(rows)


def build_behavioural_data(
    rng: np.random.Generator,
    students: pd.DataFrame,
    enrolments: pd.DataFrame,
    assessments: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    student_lookup = students.set_index("student_key")
    course_lookup = pd.DataFrame(COURSES, columns=["course_id", "course_name", "faculty", "credit_points", "delivery_mode", "assessment_intensity"]).set_index("course_id")
    assessment_lookup = assessments.groupby("course_id")

    lms_rows: list[dict] = []
    attendance_rows: list[dict] = []
    submission_rows: list[dict] = []
    outcomes: list[dict] = []
    latent_rows: list[dict] = []

    for enrolment in enrolments.itertuples(index=False):
        student = student_lookup.loc[enrolment.student_key]
        course = course_lookup.loc[enrolment.course_id]
        intensity_adjustment = {"Low": -0.15, "Medium": 0.0, "High": 0.18}[course.assessment_intensity]
        starting_engagement = 0.45 * student.academic_preparedness_latent + 0.55 * student.digital_confidence_latent - 0.65 * student.external_pressure_latent - 0.35 * student.prior_course_failures + intensity_adjustment + rng.normal(0, 0.35)
        risk_signal = []

        for week in range(1, WEEKS_PER_TERM + 1):
            assessment_pressure = 0.45 if week in {3, 6, 9} else 0.0
            fatigue = max(0, week - 7) * 0.08
            weekly_latent = starting_engagement - fatigue - assessment_pressure * 0.16 + rng.normal(0, 0.30)
            engagement_propensity = sigmoid(weekly_latent)
            active_minutes = int(np.clip(rng.normal(35 + 260 * engagement_propensity, 22), 0, 480))
            login_count = int(np.clip(rng.poisson(1 + 8 * engagement_propensity), 0, 25))
            content_views = int(np.clip(rng.poisson(3 + 24 * engagement_propensity), 0, 70))
            attendance_rate = float(np.clip(rng.normal(0.30 + 0.67 * engagement_propensity, 0.16), 0, 1))

            lms_rows.append(
                {
                    "student_key": enrolment.student_key,
                    "course_id": enrolment.course_id,
                    "term_id": enrolment.term_id,
                    "week_number": week,
                    "login_count": login_count,
                    "content_views": content_views,
                    "active_minutes": active_minutes,
                }
            )
            attendance_rows.append(
                {
                    "student_key": enrolment.student_key,
                    "course_id": enrolment.course_id,
                    "term_id": enrolment.term_id,
                    "week_number": week,
                    "attendance_rate": round(attendance_rate, 4),
                }
            )
            risk_signal.append(1 - engagement_propensity)

        course_assessments = assessment_lookup.get_group(enrolment.course_id)
        weighted_mark = 0.0
        total_weight = 0
        late_count = 0
        missing_count = 0
        for assessment in course_assessments.itertuples(index=False):
            pre_due_risk = float(np.mean(risk_signal[max(0, assessment.due_week - 3): assessment.due_week]))
            missing_probability = sigmoid(-3.0 + 3.7 * pre_due_risk + 0.42 * student.external_pressure_latent + 0.34 * student.prior_course_failures)
            submitted_flag = int(rng.random() > missing_probability)
            if submitted_flag:
                late_lambda = max(0.05, 0.20 + 1.6 * pre_due_risk + 0.25 * max(student.external_pressure_latent, 0))
                late_days = int(min(rng.poisson(late_lambda), 14)) if rng.random() < sigmoid(-1.4 + 2.8 * pre_due_risk) else 0
                score = float(np.clip(rng.normal(74 - 38 * pre_due_risk + 6 * student.academic_preparedness_latent - 2.5 * late_days, 13), 0, 100))
            else:
                late_days = 0
                score = 0.0
                missing_count += 1
            late_count += int(late_days > 0)
            weighted_mark += score * assessment.weight
            total_weight += assessment.weight
            submission_rows.append(
                {
                    "submission_id": stable_key("SUB", len(submission_rows) + 1),
                    "student_key": enrolment.student_key,
                    "assessment_id": assessment.assessment_id,
                    "course_id": enrolment.course_id,
                    "term_id": enrolment.term_id,
                    "submitted_flag": submitted_flag,
                    "late_days": late_days,
                    "score": round(score, 2),
                }
            )

        final_mark = weighted_mark / total_weight
        mean_engagement_risk = float(np.mean(risk_signal))
        outcome_logit = -3.0 + 3.4 * mean_engagement_risk + 0.85 * missing_count + 0.30 * late_count + 0.43 * student.prior_course_failures + 0.52 * student.external_pressure_latent - 0.7 * student.academic_preparedness_latent
        adverse_probability = float(sigmoid(outcome_logit))
        withdrawn_flag = int(rng.random() < adverse_probability * 0.32)
        failed_flag = int((final_mark < 50 and not withdrawn_flag) or (rng.random() < adverse_probability * 0.18 and not withdrawn_flag))
        outcome_status = "Withdrawn" if withdrawn_flag else "Fail" if failed_flag else "Pass"
        if withdrawn_flag:
            final_mark = np.nan

        outcomes.append(
            {
                "student_key": enrolment.student_key,
                "course_id": enrolment.course_id,
                "term_id": enrolment.term_id,
                "final_mark": None if pd.isna(final_mark) else round(float(final_mark), 2),
                "outcome_status": outcome_status,
                "withdrawn_flag": withdrawn_flag,
                "failed_flag": failed_flag,
            }
        )
        latent_rows.append(
            {
                "student_key": enrolment.student_key,
                "course_id": enrolment.course_id,
                "term_id": enrolment.term_id,
                "mean_engagement_risk_latent": mean_engagement_risk,
                "adverse_outcome_probability_latent": adverse_probability,
            }
        )

    return (
        pd.DataFrame(lms_rows),
        pd.DataFrame(attendance_rows),
        pd.DataFrame(submission_rows),
        pd.DataFrame(outcomes),
        pd.DataFrame(latent_rows),
    )


def build_interventions(
    rng: np.random.Generator,
    enrolments: pd.DataFrame,
    lms: pd.DataFrame,
    attendance: pd.DataFrame,
    submissions: pd.DataFrame,
) -> pd.DataFrame:
    weekly = lms.merge(attendance, on=["student_key", "course_id", "term_id", "week_number"], how="inner")
    weekly = weekly.sort_values(["student_key", "course_id", "term_id", "week_number"])
    weekly["engagement_score"] = (
        weekly["active_minutes"] / 300 * 0.55
        + weekly["login_count"] / 10 * 0.20
        + weekly["content_views"] / 30 * 0.25
    ).clip(0, 1)
    weekly["engagement_change"] = weekly.groupby(["student_key", "course_id", "term_id"])["engagement_score"].diff().fillna(0)

    submission_features = submissions.groupby(["student_key", "course_id", "term_id"], as_index=False).agg(
        missing_submissions=("submitted_flag", lambda x: int((x == 0).sum())),
        late_submissions=("late_days", lambda x: int((x > 0).sum())),
        assessment_average=("score", "mean"),
    )
    weekly = weekly.merge(submission_features, on=["student_key", "course_id", "term_id"], how="left")
    weekly["risk_proxy"] = sigmoid(
        -2.6
        + 2.7 * (1 - weekly["engagement_score"])
        + 1.6 * (1 - weekly["attendance_rate"])
        + 1.3 * weekly["missing_submissions"].fillna(0)
        + 0.55 * weekly["late_submissions"].fillna(0)
        - 0.015 * weekly["assessment_average"].fillna(60)
    )

    candidate_weeks = weekly.query("week_number >= 4").copy()
    selected = candidate_weeks[candidate_weeks["risk_proxy"] >= 0.62].copy()
    selected = selected.groupby(["student_key", "term_id"], as_index=False).first()

    rows = []
    intervention_types = ["Academic outreach", "Study skills referral", "Peer mentoring", "Wellbeing check-in"]
    for row in selected.itertuples(index=False):
        if rng.random() > 0.60:
            continue
        intervention_type = rng.choice(intervention_types, p=[0.45, 0.25, 0.18, 0.12])
        contacted = int(rng.random() < 0.82)
        accepted = int(contacted and rng.random() < 0.68)
        outcome = "Pending"
        if contacted:
            outcome = rng.choice(["Engagement improved", "No response", "Referred", "Monitoring"], p=[0.44, 0.22, 0.18, 0.16])
        rows.append(
            {
                "intervention_id": stable_key("INT", len(rows) + 1),
                "student_key": row.student_key,
                "term_id": row.term_id,
                "risk_week": int(row.week_number),
                "intervention_type": intervention_type,
                "contact_status": "Contacted" if contacted else "Not contacted",
                "accepted_support_flag": accepted,
                "outcome_status": outcome,
                "assigned_team": rng.choice(["Student Success", "Academic Support", "Wellbeing", "Faculty Advising"]),
            }
        )
    return pd.DataFrame(rows)


def write_csv(frame: pd.DataFrame, filename: str) -> None:
    path = SYNTHETIC_DIR / filename
    frame.to_csv(path, index=False)
    print(f"Wrote {len(frame):>7,} rows → {path.relative_to(SYNTHETIC_DIR.parent.parent)}")


def main() -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    programs, courses, terms = build_reference_tables()
    students = build_students(rng, programs)
    enrolments, _ = build_enrolments(rng, students, terms)
    assessments = build_assessments()
    lms, attendance, submissions, outcomes, _ = build_behavioural_data(rng, students, enrolments, assessments)
    interventions = build_interventions(rng, enrolments, lms, attendance, submissions)

    weekly_calendar = pd.DataFrame(
        [
            {
                "term_id": term["term_id"],
                "week_number": week,
                "week_start_date": term_week_date(term["start_date"], week),
            }
            for term in TERMS
            for week in range(1, WEEKS_PER_TERM + 1)
        ]
    )

    for frame, filename in [
        (students.drop(columns=["academic_preparedness_latent", "digital_confidence_latent", "external_pressure_latent"]), "students.csv"),
        (programs, "programs.csv"),
        (courses, "courses.csv"),
        (terms, "terms.csv"),
        (weekly_calendar, "term_weeks.csv"),
        (enrolments, "enrolments.csv"),
        (assessments, "assessments.csv"),
        (lms, "lms_activity.csv"),
        (attendance, "attendance.csv"),
        (submissions, "submissions.csv"),
        (outcomes, "course_outcomes.csv"),
        (interventions, "interventions.csv"),
    ]:
        write_csv(frame, filename)

    print("\nSynthetic data generation completed successfully.")
    print("No real student or institutional data were created or used.")


if __name__ == "__main__":
    main()
