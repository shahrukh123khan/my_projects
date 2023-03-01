from datetime import date
dob=input("enter your date of Birth : ")
ud,um,uy=int(dob[0:2]),int(dob[3:5]),int(dob[6:10])
today=str(date.today())
sy,sm,sd=int(today[0:4]),int(today[5:7]),int(today[8:10])
#fd=sd-ud
#fm=sm-um
fy=sy-uy
print("your age is : ",fy)
