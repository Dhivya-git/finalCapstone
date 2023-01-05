# Imports math module for pow()
import math

# Asks the user to choose between investment or bond and coverts it to lower for easier validation
selection = input("""Choose either 'investment' or 'bond' from the menu below to proceed: \n
investment - to calculate the amount of interest you'll earn on your investment
bond       - to calculate the amount you'll have to pay on a home loan\n""").lower()

# Checks for investment
if selection == "investment" :

    # Gets the user input for initial amount, interest rate, number of years and the type of interest
    principal_amount = float(input("Amount of money that you would like to deposit: "))
    interest_rate_percentage = float(input("Interest rate in % (e.g. 5.4): "))
    number_years = int(input("The number of years you plan to invest: "))
    interest_type = input("Choose 'simple' or 'compound': ").lower()
    
    # Initialises the total amount to check for invalid entry
    total_amount = 0
    # Divides the interest rate by hundered for the formula
    interest_rate = interest_rate_percentage / 100

    # Checks the user entry for the type of interest and calculates the total amount accordingly
    if interest_type == "simple" :
        total_amount = principal_amount * (1 + interest_rate * number_years)
    elif interest_type == "compound" :
        total_amount = principal_amount * math.pow(1 + interest_rate, number_years)
    else:
        print("Invalid interest type.")
        exit()

    # Checks for zero investment
    if total_amount != 0 :
        print(f"The total amount you would get back after {number_years} years at {interest_rate_percentage}% is £{total_amount:.2f}")
    else:
        print(f"No returns!")

# Checks for bond  
elif selection == "bond" :

    # Gets the user value for the value of the house, interest rate and mumber of months
    house_value = float(input("The current value of the house: "))
    interest_rate = float(input("Interest rate in % (e.g. 5.4): "))
    number_months = int(input("Number of months you plan to take to repay: "))

    # Divides the interest rate by 12 and then by 100 for the formula
    monthly_interest_rate = interest_rate / 12 / 100

    # Calculates the monthtly payment using math.pow()
    monthly_payment = (monthly_interest_rate * house_value) / (1 - math.pow((1 + monthly_interest_rate), (-number_months)))
    print(f"Your monthly repayment is £{monthly_payment:.2f}")
else:
    print("Invalid selection.")