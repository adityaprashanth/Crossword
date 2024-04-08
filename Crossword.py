import csv
import random
import copy as cy
import tkinter as tk
from tkinter import messagebox  

path="nytcrosswords2.csv"
file = open(path, "r")
data = csv.reader(file)
l1=[]
x=0
for line in data :
  l1.append(list(line))
  x+=1
l1.pop(0)
file.close() 

defaultnum=11

while(True):
  finalhints={}
  def randomword():
      x = random.choice(l1)
      global finalhints
      finalhints[x[0]]=x[1]
      return x[0]
  def commonletters(i,j):
    x=set(i)&set(j)
    return x

  finalwords=[]
  finallist=[[]]
  word1=randomword()
  for i in word1:
      finallist[0].append(i)
  finalwords.append(word1)
  finallistcopy=cy.deepcopy(finallist)
  currentx, x = 0,0
  currenty, y = 0,0
  coordlist = [(currentx,currenty)]
  coordlistcopy=cy.deepcopy(coordlist)
  xmax=1
  ymax=len(word1)
  finallistcopy=cy.deepcopy(finallist)
  finalwordscopy=cy.deepcopy(finalwords)

  def expand(xmax,ymax):
      for i in range(xmax-len(finallist)):
          finallist.append([])
      for i in range(len(finallist)):
          while len(finallist[i])<ymax:
              finallist[i].append(" ")
      for i in finallist:
          while len(i)<len(finallist[0]):
              i.append(' ')


  root = tk.Tk()
  length1 = tk.DoubleVar()
  tk.Label(root, text="Enter number of words: ").grid(row=0)
  length1.set(defaultnum)
  def valuecheck(value):
    newvalue=int(value)
    if(newvalue%2==0):
      if newvalue<float(value):
        newvalue+=1
      elif newvalue>float(value):
        newvalue-=1
      else:
        newvalue-=1
    slider.set(newvalue)
  slider = tk.Scale(root, variable=length1, from_=5, to=17, command=valuecheck, orient="horizontal")
  slider.grid(row=0, column=1)
  tk.Button(root, text="Submit", command=root.destroy).grid(column=1, row=2)
  tk.Button(root, text="Exit", command=exit).grid(column=0, row=2)
  root.mainloop()
  lennum=int(length1.get())
  defaultnum=lennum

  def addwords():
      while(True):
          word2 = randomword()
          commonset = commonletters(finalwords[-1], word2)
          while(len(commonset)==0):
              word2 = randomword()
              commonset = commonletters(finalwords[-1], word2)
          commonletter=commonset.pop()
          global currentx
          if(word2.index(commonletter)>currentx):
              currentx=x
              continue
          global currenty
          currentx-=word2.index(commonletter)
          currenty+=finalwords[-1].rindex(commonletter)
          r=max(currentx+len(word2),xmax)
          cx = currentx
          cy = currenty

          word3 = randomword()
          commonset = commonletters(word2, word3)
          while(len(commonset)==0):
              word3 = randomword()
              commonset = commonletters(word2, word3)
          commonletter=commonset.pop()
          if(word3.index(commonletter)>currenty):
              currenty=y
              currentx=x
              continue
          t=max(currenty+len(word3),ymax)
          currentx+=word2.rindex(commonletter)
          currenty-=word3.index(commonletter)
          expand(r,t)
          finalwords.append(word2)
          finalwords.append(word3)
          coordlist.append((cx,cy))
          coordlist.append((currentx,currenty))

          for i in range(len(word3)):
              if finallist[currentx][currenty+i]==word3[i]:
                  None
              elif finallist[currentx][currenty+i]!=' ':
                  return False
              finallist[currentx][currenty+i]=word3[i]
          for i in range(len(word2)):
              if finallist[cx+i][cy]==word2[i]:
                  None
              elif finallist[cx+i][cy]!=' ':
                  return False
              finallist[cx+i][cy]=word2[i]
          
          break
      return True

  counter=0
  while True:
      if (addwords()):
          counter+=1
          x=currentx
          y=currenty
          finallistcopy=cy.deepcopy(finallist)
          finalwordscopy=cy.deepcopy(finalwords)
          coordlistcopy=cy.deepcopy(coordlist)
      else:
          currentx=x
          currenty=y
          finallist=cy.deepcopy(finallistcopy)
          finalwords=cy.deepcopy(finalwordscopy)
          coordlist=cy.deepcopy(coordlistcopy)
      Flag=True
      while(Flag):
          for i in finallist:
              if i.pop()!=" ":
                  Flag=False
                  finallist=cy.deepcopy(finallistcopy)
          finallistcopy=cy.deepcopy(finallist)
      if counter==lennum//2:
          break

  for i in finallist:
      print(i)
  print(finalwords)
  for i in finalwords:
      print(i, f"({len(i)}) -", finalhints[i])

  root = tk.Tk()
  for i in range(len(finallist)):
    for j in range(len(finallist[i])):
      if finallist[i][j]!=" ":
        tk.Button(text=" ", height=1, width=2, bg="white").grid(row=i,column=j)
        tk.Label(text=" ", height=1, width=2, bg="white").grid(row=i,column=j)
  a=0
  lst=[]
  for i in finalwords:
    lst.append(tk.StringVar())
  for i in finalwords:
      tk.Entry(textvariable=lst[a], width=int(j)*2).grid(columnspan=int(j), row=a+len(finallist))
      tk.Label(text=str(f"({len(i)}) -"+finalhints[i])).grid(row=a+len(finallist),column=j+1)
      a+=1

  wordselect=set()
  def buttonpress():
    global lst
    for i in range(len(lst)):
      if finalwords[i] == lst[i].get().upper():
        wordselect.add(finalwords[i])
        if(i%2):
          for k in range(len(finalwords[i])):
            tk.Label(text=finalwords[i][k], height=1, width=2, bg="white").grid(row=coordlist[i][0]+k,column=coordlist[i][1])
        else:
          for k in range(len(finalwords[i])):
            tk.Label(text=finalwords[i][k], height=1, width=2, bg="white").grid(row=coordlist[i][0],column=coordlist[i][1]+k)
        tk.Label(root, text=finalwords[i], bg="#F0F0F0", width=int(j)*2).grid(columnspan=int(j), row=i+len(finallist))
    if lennum==len(wordselect):
      if(messagebox.askyesno(title="None", message="The crossword is completed. Do you want to continue?")):
        root.destroy()
      else:
        exit()

  tk.Button(text="Submit",command=buttonpress).grid(row=a+len(finallist)+1,column=j+1)
  tk.Button(text="Exit",command=exit).grid(row=a+len(finallist)+1,column=0,columnspan=j)
  root.mainloop()