import itertools

string1 = 'Hallo Java'
string2 = 'Hallo python'

#Every 2 alpha put in tuple
every2alpha = list(zip(string1, string2))


def f(x,y):
    return x==y

result = []
result1 = []
for i in range(len(string1)):
    #only True boolen put in lst
    if list(itertools.accumulate(every2alpha[i], f))[1] == True:
        result.append(list(itertools.accumulate(every2alpha[i], f))[1])
        result1.append(list(itertools.accumulate(every2alpha[i], f)))


print(result)
print(len(result),' alpha are in string equal position')
print('wich alpha or position are equal: ',result1)
