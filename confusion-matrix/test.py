from sklearn.metrics import confusion_matrix

y_true = [2, 0, 2, 2, 0, 1]
y_pred = [0, 0, 2, 2, 0, 2]

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print(f'{tn} {fp} {fn} {tp}')
print(confusion_matrix(y_true, y_pred))

'''
cf=
[0[2 0 0]
 1[0 0 1]
 2[1 0 2]]
   0 1 2 

line 6, in <module>
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
ValueError: too many values to unpack (expected 4)

sens = 

https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html


[1, 0, 1, 1, 0, 0]
[1, 0, 1, 0, 0, 1]

https://www.google.com/url?sa=i&url=https%3A%2F%2Ftowardsdatascience.com%2Funderstanding-confusion-matrix-a9ad42dcfd62&psig=AOvVaw1f0B9403xSckZVCwPvCUme&ust=1614822452025000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLiMiceAk-8CFQAAAAAdAAAAABAD

'''

def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_hat)): 
        if y_actual[i]==y_hat[i]==1:
           TP += 1
        if y_hat[i]==1 and y_actual[i]!=y_hat[i]:
           FP += 1
        if y_actual[i]==y_hat[i]==0:
           TN += 1
        if y_hat[i]==0 and y_actual[i]!=y_hat[i]:
           FN += 1

    return(TP, FP, TN, FN)
