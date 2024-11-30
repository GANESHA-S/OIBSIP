def calculate_bmi():
    print("Welcome to the BMI Calculator!")
    
    try:
        weight = float(input("Enter your weight in kilograms: "))
        height = float(input("Enter your height in meters: "))
        if weight <= 0 or height <= 0:
            print("Weight and height must be positive values.")
            return
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "You belong to the Underweight category"
        elif 18.5 <= bmi < 24.9:
            category = "You belong to the Normal weight category"
        elif 25 <= bmi < 29.9:
            category = "You belong to the Overweight category"
        else:
            category = "You belong to the Obesity category"
        print(f"\nYour BMI is: {bmi:.2f}")
        print(f"Category: {category}")
    except ValueError:
        print(" Please enter correct values.")
if __name__ == "__main__":
    calculate_bmi()
