import csv,operator

#path = 'c:\\temp\\'


file9=open("TM90_100T_9x9Aya_0310-1342train7clauses.csv", "r")

reader = csv.reader(file9)
#reader9n = csv.reader(file9neg)
#reader9p = csv.reader(file9pos)
table = []
table2 = []
counter =0
with open("TM90_100T_9x9Aya_0310-1342train7clauses.csv", 'r') as file:
    for line in file.readlines():
        if counter != 0 and counter != 13:
            line = [int(x) for x in line.strip().split(',')[2:]]
            table.append(line)
        counter+=1

#0 loss pos_true
#1 win pos true
#3 loss pos false
#4 win pos false
#5 draw pos false
#6 loss neg false
#7 win neg false
#8 draw neg false
#9 loss neg true
#10 win neg true
#11 draw neg true
#12 loss weights
#13 win weights
#14 draw weights
def sort_table(table, col):
    return sorted(table, key=operator.itemgetter(col), reverse=True)
loss_pos_true = []
win_pos_true = []
loss_pos_false = []
win_pos_false = []
draw_pos_false = []
loss_neg_true = []
win_neg_true = []
loss_neg_false = []
win_neg_false = []
draw_neg_true = []
for i in range(len(table[0])):
    if i%2 == 0:
        loss_pos_true.append([i,table[0][i]*table[12][i]])
        win_pos_true.append([i,table[1][i]*table[13][i]])
        loss_pos_false.append([i,table[3][i]*table[12][i]])
        win_pos_false.append([i,table[4][i]*table[13][i]])
        draw_pos_false.append([i,table[5][i]*table[14][i]])
    if i%2 != 0:
        loss_neg_false.append([i,table[6][i]*table[12][i]])
        win_neg_false.append([i,table[7][i]*table[13][i]])
        loss_neg_true.append([i,table[9][i]*table[12][i]])
        win_neg_true.append([i,table[10][i]*table[13][i]])
        draw_neg_true.append([i,table[11][i]*table[14][i]])

loss_pos_true = sort_table(loss_pos_true,1)
win_pos_true = sort_table(win_pos_true,1)
loss_pos_false = sort_table(loss_pos_false,1)
win_pos_false = sort_table(win_pos_false,1)
draw_pos_false = sort_table(draw_pos_false,1)
loss_neg_true = sort_table(loss_neg_true,1)
win_neg_true = sort_table(win_neg_true,1)
loss_neg_false = sort_table(loss_neg_false,1)
win_neg_false = sort_table(win_neg_false,1)
draw_neg_true = sort_table(draw_neg_true,1)
print("Loss_pos_true ,  Loss_pos_false, Win_pos_true ,   Win_pos_false ,  Loss_neg_true,  Loss_neg_false , Win_neg_true ,  Win_neg_false")
for i in range(10):
    print(loss_pos_true[i], loss_pos_false[i], win_pos_true[i], win_pos_false[i], loss_neg_true[i], loss_neg_false[i], win_neg_true[i],win_neg_false[i])
lpt = 0
wpt= 0
lnt= 0
wnt= 0
lnf= 0
wnf= 0
lpf= 0
wpf = 0
for i in range(len(loss_neg_true)):
    lpt += loss_pos_true[i][1]
    wpt += win_pos_true[i][1]
    lpf += loss_pos_false[i][1]
    wpf += win_pos_false[i][1]
    lnt += loss_neg_true[i][1]
    wnt += win_neg_true[i][1]
    lnf += loss_neg_false[i][1]
    wnf += win_neg_false[i][1]
#print(lpt)
#print(wpt)
#print(lpf)
#print(wpf)
#print(lnt)
#print(wnt)
#print(lnf)
#print(wnf)
winPrecision =wpt/(wpt+wpf)
print("Win Precision: %s"%(winPrecision))
lossPrecision = lpt/(lpt+lpf)
print("Loss Precision: %s"%(lossPrecision))
winRecall = wpt/(wnf+wpt)
print("Win Recall: %s"%(winRecall))
lossRecall = lpt/(lnf+lpt)
print("Loss Recall: %s"%(lossRecall))