#create txt
with open ('example.txt','w') as file:
    file.write('8 13 10 7.5\n')
    file.write('8 13 11 9.2\n')
    file.write('8 13 12 11.7\n')

infile = open("mean_temperature.txt","r")

mean_temp = []
for line in infile:
    data = line.split(' ')
    mean_temp = float