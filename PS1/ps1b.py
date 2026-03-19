portion_down_payment = 0.25
current_savings = 0 
r = 0.04

annual_salary= float(input("\nEnter annual salary"))

portion_saved= float(input("\nEnter percent of salary to save"))

total_cost= float(input("\nEnter the cost"))

semi_annual_raise = float(input('\nEnter semi-annual raise'))
down_payment = portion_down_payment * total_cost

month_count = 0 
while current_savings <down_payment:
	if month_count%6==0 and month_count>0:
		annual_salary +=annual_salary*semi_annual_raise
	current_savings += portion_saved *(annual_salary/12) + r*(current_savings/12) 
	month_count+=1


print("\n",month_count)

