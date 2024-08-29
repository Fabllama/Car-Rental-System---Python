
def temper(temperature):
        
    if temperature.find("F") == 0:
        degree = float(temperature[temperature.find("F")+1:])
        new_temp = (degree-32)* 5/9
        print(new_temp) 
    elif temperature.find("C") == 0:
        degree = float(temperature[temperature.find("C")+1:])
        new_temp = (degree * 9/5) + 32
        print(new_temp) 
    else:
        print("Enter in F or C format")


if __name__ == "__main__":
    temperature = input("Insert temperature with C/F prefix : ")
    
    temper(temperature)

