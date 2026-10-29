# DATA INTERPRETATION AND PREDICTIVE ANALYTICS

Interactive educational mini-project for **Logic and Data Interpretation II (TE / B)**, built with Python and Streamlit. It combines reasoning practice, worked solutions, and session-based performance insights in a single web interface. A Tkinter desktop version is retained as an optional alternative.

## Project summary

The application addresses a simple learning need: students often practise questions without a clear, topic-wise view of their progress. It provides a structured bank of **90 computed questions** across six modules—Clock, Calendar, Pattern, Bar Graph, Pie Chart, and Line Graph. Each module contains 15 questions spanning Easy, Medium, and Hard levels. Learners can study notes and formulas, attempt timed quizzes, receive immediate correctness feedback, read worked explanations, and review mistakes.

The **Performance Insights** page summarises completed quizzes, compares recent accuracy, highlights topic-level performance, and offers a transparent next-attempt estimate. The estimate is a recency-weighted average of up to the last three quiz percentages. It is an interpretable baseline for an academic demonstration—not a trained or validated machine-learning model. Quiz results stay in Streamlit session state; no database or external account is required.

## Presentation details — TE / B

- **Course Name:** Logic and Data Interpretation II
- **Branch:** Artificial Intelligence and Data Science
- **Class / Division:** TE / B
- **Professor:** Siddharth Machhindra Bhore

### Group members

| Roll No. | Name |
|---:|---|
| 05 | Sudiksha Dumbre |
| 18 | Sakshi Mulik |
| 31 | Vaishnavi Pol |
| 32 | Vedant Rajmane |
| 35 | Sneha Rathod |

## Main features

- Refined Home page with a professional hero banner, key project metrics, presentation details placed above the research summary, and the group-member table.
- Dashboard with overall and topic-wise performance.
- Study & Practice Library with notes, formulas, exam tips, videos, and PDF/printable guides.
- Timed 10-question and 15-question topic quizzes, plus a 20-question Mixed Challenge.
- Step-by-step solutions, answer review, and an option to filter mistakes.
- Performance Insights with quiz history, a recent weighted estimate, topic-level progress bands, and a suggested area to revise.
- Professional teal, deep-navy, white, and amber theme with refined cards, spacing, and responsive presentation details.

## Recommended setup on Windows

1. Install **Python 3.11 or newer** and ensure Python is on PATH.
2. Extract the ZIP file to a folder you can easily find.
3. Open that folder in File Explorer.
4. Double-click **`run_windows.bat`**. The script creates a local virtual environment if needed, installs the required packages, and starts the website.
5. Open the local URL displayed in the terminal (usually `http://localhost:8501`). Keep the terminal window open while using the website.

### Manual setup (Command Prompt)

Open Command Prompt inside this project folder, then run:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

If `python` is not recognised, install Python and select **Add Python to PATH**, or use `py` in place of `python` in the first command. Do not run the installation command from the parent folder; it must be run in the folder containing `requirements.txt`.

## Optional desktop version

After installing the requirements, run `python main.py`. This launches the retained Tkinter desktop interface. The website is the primary version and is launched with `streamlit_app.py`.

## Project structure

```text
Data_Interpretation_and_Predictive_Analytics_Project/
├── streamlit_app.py       # Primary web application
├── main.py                # Optional Tkinter desktop app
├── theme.py               # Shared desktop colour theme
├── questions.py           # Generated question bank
├── study.py                # Notes, formulas, tips, and resources
├── quiz_engine.py          # Quiz sampling and scoring logic
├── modules/                # Desktop application screens
├── guides/                 # PDF learning guides
├── tests/                  # Automated core checks
├── requirements.txt
└── run_windows.bat         # One-click Windows setup and launch
```

## Methodology

1. **Question generation:** deterministic templates construct numeric reasoning and chart-reading questions with computed answer keys.
2. **Assessment:** the quiz engine samples a requested number of questions, enforces a time limit, and records answers.
3. **Feedback:** each submitted answer is checked and the worked explanation is displayed.
4. **Descriptive analytics:** results are aggregated by attempt and topic to calculate accuracy.
5. **Predictive baseline:** up to the latest three attempt percentages are averaged with increasing weights, assigning greater weight to the most recent result.
6. **Recommendation:** the lowest-accuracy assessed topic is suggested for revision.

## Scope and limitations

- There is no login system, external database, or permanent cloud storage. Session history can be lost when the Streamlit session ends.
- The score estimate is heuristic and should not be presented as an accurate exam-score predictor. It does not use a student dataset or a trained ML model.
- Question templates are intended for practice and learning; students should still verify concepts with course notes.

## References for background reading

- IBM, [What is Predictive Analytics?](https://www.ibm.com/think/topics/predictive-analytics).
- Batool et al. (2023), [Educational Data Mining to Predict Students' Academic Performance: A Survey Study](https://eric.ed.gov/?id=EJ1363934).
- Streamlit, [Official documentation](https://docs.streamlit.io/).
