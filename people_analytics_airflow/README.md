# Employee Retention Insights
looker : https://lookerstudio.google.com/s/hKu1pm1-B9c
This report gives insight in the the employee churn data. The model predicts employee attrition risk using machine learning, orchestrated with Apache Airflow, stored in BigQuery, and visualised in Looker Studio.

---

## Project Overview

Employee attrition is costly. This project builds a pipeline that identifies employees at risk of leaving so HR teams can act before it happens.

---

## Pipeline Architecture

```
IBM HR Dataset (CSV)
        ↓
Python / Google Colab
  - Data cleaning
  - Exploratory data analysis
  - Model training
  - Flight risk scoring
        ↓
Apache Airflow
  - Monthly DAG orchestration
  - Automated pipeline runs
        ↓
Google BigQuery
  - Partitioned storage
  - SQL queries
        ↓
Looker Studio
  - Interactive retention dashboard
```

---

## Dataset

- **Source:** IBM HR Analytics Attrition Dataset (Kaggle)
- **Rows:** 1,470 employees
- **Columns:** 35 features including department, job role, tenure, salary, overtime, satisfaction scores
- **Target:** Attrition (Yes/No) — 16.1% attrition rate

---

## What the Pipeline Does

1. **Loads** the IBM HR CSV
2. **Cleans** the data — drops constant columns, encodes categorical features
3. **Trains** a Logistic Regression model to predict attrition probability
4. **Scores** every employee with a flight risk label — Low, Medium, High
5. **Exports** predictions to BigQuery
6. **Visualises** results in a Looker Studio dashboard

---

## Models Used

| Model | Accuracy | ROC-AUC | Recall |
|---|---|---|---|
| Logistic Regression | 75.2% | 0.80 | 61.7% |
| Random Forest | 83.7% | 0.76 | 6.4% |

Logistic Regression was selected as the production model — higher AUC and recall make it more reliable for identifying employees at risk of leaving despite lower raw accuracy.

---

## Key Findings

- Overall attrition rate: **16.1%**
- Sales department has the highest attrition rate
- Employees who work overtime are **3x more likely** to leave
- Leavers had on average **3 fewer years** of tenure than stayers
- Low satisfaction scores and no recent promotion are strong attrition signals

---

## Flight Risk Breakdown

| Risk Level | Employees | Actual Attrition |
|---|---|---|
| Low | 767 | 3.4% |
| Medium | 361 | 12.7% |
| High | 341 | 48.4% |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data cleaning, EDA, modelling |
| Pandas / Scikit-learn | Data manipulation and ML |
| Apache Airflow | Pipeline orchestration |
| Astronomer | Local Airflow setup via Docker |
| Google BigQuery | Cloud data storage and SQL queries |
| Looker Studio | Interactive dashboard |

---

## Project Structure

```
people_analytics_airflow/
  ├── dags/
  │   └── people_analytics_dag.py   ← Airflow DAG
  ├── include/
  │   ├── WA_Fn-UseC_-HR-Employee-Attrition.csv
  │   └── hr_with_predictions.csv
  ├── requirements.txt
  └── README.md
```

---

## Airflow DAG

The pipeline runs weekly and consists of 4 tasks:

```
load_data → clean_data → train_and_predict → export_data
```

All 4 tasks completed successfully in 19 seconds.

---

## Dashboard

The Looker Studio dashboard shows:
- Overall attrition rate scorecard
- Attrition rate by department
- Flight risk breakdown (Low / Medium / High)
- High risk employee table with attrition probability scores
- Interactive filters by department and flight risk

---

## How to Run Locally

**Requirements:**
- Docker Desktop
- Astronomer CLI

**Steps:**
```bash
git clone https://github.com/your_username/people_analytics_airflow
cd people_analytics_airflow
astro dev start
```

Then open `localhost:8080` and trigger the `people_analytics_pipeline` DAG.

---

## Author

Ashley Vanessa

