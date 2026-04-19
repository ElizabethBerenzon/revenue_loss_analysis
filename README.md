# revenue_loss_analysis
Project Overview
--
This project focuses on identifying the root cause of revenue decline and churned users segmenting them  by industry and reason.
The goal was to provide actionable insights to help business reduce churn,optimize payment processes,and improve customer retention.

Key Business Questions:
--
* 1. Where is the money going? - Which industries are experiencing the most significant drop in monthly recurring revenue? (MRR)
* 2. Why they are leaving? - What are primary reasons for churn? ( Tech.problems,price or product fit)
* 3. If there was preceding churn sign before cancelation of recurring payment

Tech Stack:
--
 * SQL:Data extraction,joing transactional tables.
 * Python (Pandas):Data cleaning,creationg new attribute and saving new csv file.
 * Tableu: Developing an interactive dashboard to visualize in which industries was revenue decline

Technical Workflow
--
* 1.Datasets & SQL extraction
ravenstack_accounts: To segment users by Industry (FinTech, EdTech, DevTools, etc.).
ravenstack_subscriptions: To track MRR (Monthly Recurring Revenue) and billing cycles.
ravenstack_churn_events: To identify the specific Reason Codes for customer departures.
<img width="594" height="608" alt="Снимок экрана 2026-04-18 в 17 17 27" src="https://github.com/user-attachments/assets/5e417fe3-44f2-4b4a-9400-2ab8a4cacf5f" />
