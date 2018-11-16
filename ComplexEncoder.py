import pandas as pd
import numpy as np
import math
import cmath

class ComplexEncoder():
    
    #returns mapings of category to value
    def fit(self,column):
        column = column.astype(str) #not string breaks value_counts indexing
        #count frequencies of each category
        val_counts = column.value_counts() #it creates sorted from largest to smallest pandas series
        #count number of categories
        k = column.nunique()-1

        #create a dictionary of j values for every group
        #smallest values of i goes to the most frequent groups
        j = {}
        for i in range(0,column.nunique()):
            j[column.value_counts().index[i]] = i #i=0 - largest group

        #create dictionary with module R for every group
        module_R = {}
        for level in range(0,len(column.value_counts())):
            z=0
            for i in range(1,column.value_counts()[level]+1):
                z+=i
            module_R[column.value_counts().index[level]]=z/column.value_counts()[level]

        #find all ties
        ties = {}
        for key, value in module_R.items():
            try:
                ties[value].append(key)
            except KeyError:
                ties[value] = [key]
        ties_list = [l for l in ties.values() if len(l)>1]
        not_ties = [l for l in ties.values() if len(l)==1]
        #calculate phase for every ties level
        phase = {}
        for d in range(0,len(val_counts)):
            m=0
            #val_counts has all levels of category, for this reason levels d for ties and not ties are less than val counts
            #for this reason we need to pass these levels of d, which do not have the level d
            try:
                for i in ties_list[d]:
                    if m==0:
                        phase[i]=0
                    else:
                        phase[i]=math.pi*j[i]/k
                    m+=1
            except:
                pass
            try:
                for i in not_ties[d]:
                    phase[i]=0
            except:
                pass
        #calculate exponential form
        self.exp = {}
        for key, value in module_R.items():
            if phase[key]==0:
                self.exp[key] = module_R[key]
            else:
                self.exp[key] = value*np.exp(cmath.sqrt(-1)*phase[key])  
        return self
    
    #map category to corresponding value
    def transform(self, column):
         #map exponential form instead of categorical for column
        column = column.astype(str)
        column=column.map(self.exp) 
        return column
    
    
    def fit_transform(self, column):
        return self.fit(column).transform(column)
