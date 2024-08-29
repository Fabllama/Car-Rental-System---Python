# exercise 1

def calc_bmi(height,weight):
    #calculation
    bmi_score = weight / (height**2)

    if bmi_score < 15:
        print (f'Your BMI Score :  {bmi_score:.2f}')
        print("Underweight")
    elif 15 <= bmi_score < 25:
        print (f'Your BMI Score :  {bmi_score:.2f}')
        print("Normal weight")
    elif 25 <= bmi_score < 30:
        print (f'Your BMI Score :  {bmi_score:.2f}')
        print("Overweight")
    elif bmi_score > 30:
        print (f'Your BMI Score :  {bmi_score:.2f}')
        print("Obese")
    else:
        print("Huh?!")
        
    
#input
weight = float(input("Input weight in kg : "))
height = float(input("Input height in meters : "))

calc_bmi(height,weight)
#print (f'Your BMI Score :  {bmi_score:.2f}')