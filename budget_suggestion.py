from analysis import get_monthly_summary
from database import get_budget
def suggest_budget_adjustments(month, year):
   summary = get_monthly_summary(month, year)
   budget = get_budget(month, year)
   if summary['expenses'] <= budget:
       return "You're within your budget. Keep it up!"
   overspending = summary['expenses'] - budget
   suggestions = []
   high_spending = summary['breakdown'].sort_values(by='total', ascending=False)
   for _, row in high_spending.iterrows():
       if overspending <= 0:
           break
       reduction_suggestion = min(overspending, row['total'] * 0.1)  # Suggest cutting 10%
       suggestions.append(f"Reduce {row['category']} spending by ${reduction_suggestion:.2f}")
       overspending -= reduction_suggestion
   return suggestions if suggestions else ["Consider reducing discretionary spending."]

