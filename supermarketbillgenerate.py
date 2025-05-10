from datetime import datetime


name=input("Enter your name:")


#list of items
list='''
Rice     Rs 50/kg
Sugar    Rs 30/kg
Salt     Rs 20/kg
Oil      Rs 110/liter
Paneer   Rs 400/kg
Maggi    Rs 80/each
Boost    Rs 90/each
colgate  Rs 85/each
soap     Rs 20/each
'''
price=0
pricelist=[]
Totalprice=0
Finalprice=0
finalamount=0
ilist=[]
plist=[]
qlist=[]
 
 #rates for items
items={'rice':50,'Sugar':30,'Salt':20,'Oil':110,'Panner':400,
        'maggi':80,'Boost':90,'colgate':85,'soap':20}

option=int(input("for list of items press 1:"))
if option==1:
    print(list)

for i in range(len(items)):
    inp1=int(input("if you want to buy press 1 or 2 for Exit:"))
    if inp1==2:
        break
    if inp1==1:
        item=input("Enter your items:")
        
        quantity=int(input("Enter quantity:"))
       
        if item in items.keys():
            price=quantity*(items[item])
            pricelist.append((item,quantity,items,price))
            Totalprice+=price
            ilist.append(item)
            qlist.append(quantity)
            plist.append(price)
            gst=(Totalprice*5)/100
            finalamount=gst+Totalprice
        else:
            print("sorry you entered item is not available")
        
    else:
        print("you entered wrong number")
    inp=input("can i bill the item yes or no:") 
    if inp=='yes':
        pass
        if finalamount!=0:
            print(25*"=","optimus SuperMarket",25*"=")
            print(28*" ","vijayawada")
            print("Name:",name,30*" ","Date:",datetime.now())
            print(75*"-")
            print("sno",8*" ","items",8*" ","Quantity",3*" ","price")
            for i in range(len(pricelist)):
                print(i,8* ' ',8* ' ',ilist[i], 3*' ',qlist[i],plist[i])
            print(75*"-")
            print(50*" ","TotalAmount:"'Rs',Totalprice)  
            print("gst amount",50*" ",'Rs',gst)
            print(75*"-") 
            print(50*" ","finalAmount:"'Rs',finalamount)  
            print(75*"-") 
            print(50*" ","Thanks for visiting")
            print(75*"-") 
            
            
        
        