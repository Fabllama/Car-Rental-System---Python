# exercise 2
#input
weight = float(input("Input weight in kg : "))
height = float(input("Input height in meters : "))

#calculation
bmi_score = weight / (height**2)

print (f'Your BMI Score :  {bmi_score:.2f}')