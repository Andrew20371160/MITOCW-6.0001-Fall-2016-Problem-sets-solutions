portion_down_payment = 0.25
r = 0.04
semi_annual_raise= 0.07
total_cost= 1000000
portion_saved =0
down_payment = portion_down_payment * total_cost
max_month_count = 36 

annual_salary= float(input("\nEnter annual salary"))
 

left_saving =  0 
right_saving = 1
trial_c = 0 
while left_saving <=right_saving :	
	trial_c +=1
	current_savings = 0 
	portion_saved = (left_saving +right_saving)/2
	temp_annual_salary =annual_salary 
	month_count = 0 

	while month_count <36:
		if month_count%6==0 and month_count>0:
			temp_annual_salary +=temp_annual_salary*semi_annual_raise
		current_savings += portion_saved *(temp_annual_salary/12) + r*(current_savings/12) 
		month_count+=1
	
	if abs(current_savings-down_payment) <=100:
		break
	if current_savings <down_payment :
		left_saving = portion_saved  +0.0001
	else :
		right_saving = portion_saved -0.0001 




print("\n",(portion_saved))

print("\nsteps: ",trial_c)