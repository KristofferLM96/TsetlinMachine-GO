import csv


file9=open("TM90_100T_9x9Aya_0310-1342short_train7fixed.csv", "r")
pred = open("Prediction"+".csv", 'w')
end = open("End_Result"+".csv", 'w')
komi = open("No_Komi"+".csv", 'w')
reader9 = csv.reader(file9)

table2 = []

for line in reader9:
    newTable = [line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18], line[19], line[20], line[21], line[22], line[23], line[24], line[25], line[26], line[27], line[28], line[29], line[30]]
    table2.append(newTable)

count0=[0,0,0,0,0,0,0,0,0,0]
count1=[0,0,0,0,0,0,0,0,0,0]
print("Current Prediction is correct with end result")
pred.write("Current Prediction is correct with end result\n")
for i in range(len(table2)-1):
    i+=1
    for j in range(10):
        k=j*3+2
        if table2[i][0][0] == '0' and table2[i][0][0] == table2[i][k]:
            count0[j] = count0[j] +1
        if table2[i][0][0] == '1' and table2[i][0][0] == table2[i][k]:
            count1[j] = count1[j] + 1
        #if table2[i][0][0] == '2' and table2[i][0][0] == table2[i][k]:
        #    count2[j] = count2[j] + 1
print(count0)
print(count1)
pred0 = count0
pred1= count1
count0=[0,0,0,0,0,0,0,0,0,0]
count1=[0,0,0,0,0,0,0,0,0,0]
print("Current board is correct with end result")
end.write("Current board is correct with end result\n")
for i in range(len(table2)-1):
    i+=1
    for j in range(10):
        k=j*3+1
        if table2[i][0][0] == '0' and int(table2[i][k]) < 0:
            count0[j] = count0[j] +1
        if table2[i][0][0] == '1' and int(table2[i][k])>0:
            count1[j] = count1[j] + 1

print(count0)
print(count1)
end0 = count0
end1= count1
count0=[0,0,0,0,0,0,0,0,0,0]
count1=[0,0,0,0,0,0,0,0,0,0]
print("Current board is correct with end result - komi")
komi.write("Current board is correct with end result - komi\n")
for i in range(len(table2)-1):
    i+=1
    for j in range(10):
        k=j*3+1
        if table2[i][0][0] == '0' and int(table2[i][k]) < -7:
            count0[j] = count0[j] +1
        if table2[i][0][0] == '1' and int(table2[i][k])> -7:
            count1[j] = count1[j] + 1

print(count0)
print(count1)
komi0 = count0
komi1= count1
count00 =0
count01= 0
for i in range(len(table2)):
    if table2[i][0][0] == '0':
        count00 +=1
    if table2[i][0][0] == '1':
        count01 +=1
print("Total White Win: %s Total Black Win: %s Total Games: %s"%(count00,count01,count00+count01))
pred.write("%s"%(pred0[0]))
end.write("%s"%(end0[0]))
komi.write("%s"%(komi0[0]))
for i in range(len(pred0)-1):
    i=i+1
    pred.write(",%s"%(pred0[i]))
    end.write(",%s"%(end0[i]))
    komi.write(",%s"%(komi0[i]))
pred.write("\n")
end.write("\n")
komi.write("\n")
pred.write("%s"%(pred1[0]))
end.write("%s"%(end1[0]))
komi.write("%s"%(komi1[0]))
for i in range(len(pred1)-1):
    i=i+1
    pred.write(",%s"%(pred1[i]))
    end.write(",%s"%(end1[i]))
    komi.write(",%s"%(komi1[i]))
pred.write("\n")
end.write("\n")
komi.write("\n")
pred.write("White,%s,Black,%s,Total,%s" %(count00,count01,count00+count01))
end.write("White,%s,Black,%s,Total,%s" %(count00,count01,count00+count01))
komi.write("White,%s,Black,%s,Total,%s" %(count00,count01,count00+count01))