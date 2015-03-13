# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 14:56:29 2015

@author: mohammed.ashik
"""
import pandas as pd
import os
import Tkinter, tkFileDialog

def calculator(infile,refile):
    #ilength = infile.shape[1,]
    #rlength = refile.shape[1,]
    output_ = pd.DataFrame(index={"A"}, columns={"keywords","Match","Score"})
    #output_ = output_.fillna(0)   
    icolumn = list(infile.columns.values)
    rcolumn = list(refile.columns.values)
    print "Icolumn : %s rcolumns : %s",icolumn,rcolumn
    i = 0
    for x in infile.index:
        iword = infile['Words'].ix[x]
        score = 999999        
        word = ""
        for j in refile.index:
            rword = refile['Words'].ix[j]
            lscore = levenshtein(iword,rword) 
            if(lscore < score):
                score =lscore
                word = rword
        print iword
        print word
        print score
        print "-----------------------------"
        output_.loc[i] = [iword,word,score]
        i+=1
    return output_
    
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]
    
#Set directory
wd_path = tkFileDialog.askdirectory(title = "Select Working Directory")
os.chdir(wd_path)
root = Tkinter.Tk()
root.withdraw()
in_path = tkFileDialog.askopenfilename(title = "Select Source File")
inputfiles = pd.read_csv(in_path)
out_path = tkFileDialog.askopenfilename(title = "Select Reference File")
referfiles = pd.read_csv(out_path)
columnnames = list(inputfiles.columns.values)
xri = calculator(inputfiles,referfiles)
print "output saved in directory"
xri.to_csv("Matchresult.csv")