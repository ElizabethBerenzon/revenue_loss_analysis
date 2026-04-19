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

Step 1 
--
Merging accounts ,subscriptions, and churn events to create a unified view
this dataset allows us to correlate customer profiles with subscription info and churn behavior
```
SELECT 
    a.account_id,
    a.industry,             -- Business sector for segmentation
    a.plan_tier,            -- Subscription level (Basic/Pro/Enterprise)
    s.mrr_amount,           -- Monthly Recurring Revenue 
    s.billing_frequency,    -- Monthly vs Annual payments
    c.churn_date,           -- Termination date
    c.reason_code,          -- Categorized reason for leaving
    c.preceding_downgrade_flag -- Indicator of activity decline before churn
FROM ravenstack_accounts  a
JOIN ravenstack_subscriptions s  ON a.account_id = s.account_id
LEFT JOIN ravenstack_churn_events c ON a.account_id = c.account_id
Limit 1000;
```
Using here left join for identifying not only churned accounts because null here will mean that account is active


-- Step 2 Revenue loss analysis by Churn reason
Select 
reason_code,     -- identify the reason
Count(churn_event_id) as total_churns,
ROUND(
AVG(
refund_amount_usd),2) as avg_refund,  -- the avg_refund which was sent back to user in case of cancellation
Sum(mrr_amount) as lost_mrr   -- the lost revenue 
From ravenstack_churn_events r
join ravenstack_subscriptions s2
on r.account_id = s2.account_id 
where reason_code is not null
group by reason_code
Order by lost_mrr;
 
-- Step 3  Calculation Churn Rate of each kind of industry
SELECT 
    industry,   -- segmentation
    COUNT(account_id) AS total_accounts,  
    SUM(
        CASE 
            WHEN churn_flag = 'True' THEN 1
            ELSE 0
        END
    ) AS churned_accounts,    -- if user's purchases were decreased earlier
    ROUND(
        SUM(
            CASE 
                WHEN churn_flag = 'True' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(account_id),
        2                               -- what the percentage of this kind of users
    ) AS churn_rate_percentage
FROM ravenstack_accounts r
GROUP BY industry
ORDER BY churn_rate_percentage DESC;

-- Step 4 Early warning Signals (Downgrade Pattern Analysis)
Select                    
preceding_downgrade_flag, -- if user's purchases were decreased earlier
Count(*) as total_cases,  -- it will be indicator
Sum(
Case when churn_date is not null then 1 
else 0 End) as churned_count             
From ravenstack_churn_events r 
group by preceding_downgrade_flag ;

-- Step 5 Refund and Cash outflow audit
SELECT                                     
reason_code,          -- segmantation by reason
Avg(refund_amount_usd) as refund_amount_valeu,  -- average amount of refund of each reason
Sum(refund_amount_usd) as total_cash_out    -- the lost revenue, segmented one
From ravenstack_churn_events r 
Group by r.reason_code 
Order by  refund_amount_valeu DESC;

