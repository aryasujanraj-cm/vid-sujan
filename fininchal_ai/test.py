from categorize import categorize
from analysis import analyze
from budget import budget_analysis
from advice import give_advice
from indian_finance import sip_calculator, check_50_30_20
from export import generate_pdf_report
from goals import load_goals
from storage import load_expenses
from prediction import predict_monthly_spending

expenses = [
  {'amount':500,'category':'Food','date':'2026-06-12','merchant':'Zomato'},
  {'amount':1000,'category':'Shopping','date':'2026-06-12','merchant':'Amazon'},
  {'amount':2000,'category':'Savings','date':'2026-06-12','merchant':'SIP'},
  {'amount':300,'category':'Transport','date':'2026-06-12','merchant':'Uber'}
]

total, cats, months = analyze(expenses)
print('1. analyze OK - total:', total)
print('2. categorize OK:', categorize('zomato food order'))

advice = give_advice(total, cats)
print('3. advice OK - tips:', len(advice))

budget = budget_analysis(total, cats)
print('4. budget OK - insights:', len(budget))

sip = sip_calculator(500, 12, 5)
print('5. SIP OK:', round(sip))

check = check_50_30_20(total, cats)
print('6. 50-30-20 OK:', check)

pdf = generate_pdf_report(total, cats, months, advice, budget)
print('7. PDF OK - bytes:', len(pdf))

goals = load_goals()
print('8. goals OK:', goals)

print('')
print('ALL TESTS PASSED - Ready to run!')