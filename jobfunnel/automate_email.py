import imaplib, email
import csv
import pandas as pd
  
user = 'riya.agrahari@hackerrank.com'
password = 'wvtufdqovypfmtjy'
imap_url = 'imap.gmail.com'
  
# Function to get email content part i.e its body part 
def get_body(msg): 
    if msg.is_multipart(): 
        return get_body(msg.get_payload(0)) 
    else: 
        return msg.get_payload(None, True) 
  
# Function to search for a key value pair  
def search(key, value, con):  
    result, data = con.search(None, key, '"{}"'.format(value)) 
    return data 
  
# Function to get the list of emails under this label 
def get_emails(result_bytes): 
    msgs = [] # all the email data are pushed inside an array 
    for num in result_bytes[0].split(): 
        typ, data = con.fetch(num, '(RFC822)') 
        msgs.append(data) 
  
    return msgs 
  
# this is done to make SSL connnection with GMAIL 
con = imaplib.IMAP4_SSL(imap_url)  
  
# logging the user in 
con.login(user, password)  
  
# calling function to check for email under this label 
con.select('Inbox')  

msgs = get_emails(search('FROM', 'reports@hackerrank.com', con))[-2:] 

# print(msgs)  
  
  
# Finding the required content from our msgs 
# User can make custom changes in this part to 
# fetch the required content he / she needs 
file = open('file.txt','w')
file.close()
 
for msg in msgs[::-1]:  
    for sent in msg: 
        if type(sent) is tuple:  
  
            # encoding set as utf-8 
            content = str(sent[1], 'utf-8')  
            data = str(content) 
  
            # Handling errors related to unicodenecode 
            try:  
                indexstart = data.find("ltr") 
                data2 = data[indexstart + 5: len(data)] 
                indexend = data2.find("</div>") 
  
                # printtng the required content which we need 
                # to extract from our email i.e our body 
                file = open('file.txt','a')
                file.write(data2[0: indexend])
                file.close()
                # print(data2[0: indexend]) 
  
            except UnicodeEncodeError as e: 
                pass
    break
# replace invalid keywords
f = open('file.txt','r')
filedata = f.read()
f.close()

newdata = filedata.replace("=0D","")
newdata = newdata.replace("0D","")
newdata = newdata.replace("=","")
newdata = newdata.replace("\n","")

f = open('file.txt','w')
f.write(newdata)
f.close()
print("********************************************************************************************************")
data = ""
# find index of string
with open('file.txt', 'r') as f:
    content = f.read()
    first_index = content.index('|0A|')
    last_index = content.index('|0A0A')
    data = content[first_index+4:last_index]
    data = data.replace("0D","")
# write data to a csv 
cols = ['Name', 'Email', 'Company', 'Phone', 'Payment plan', 'Country', 'Current status']
rows = []
l = data.split("|0A|")
print(l)
for i in l:
    row = i.split("|")
    row = [x.replace("\n","") for x in row]
    row = [x.strip(' ') for x in row]
    rows.append(row)
df = pd.DataFrame(rows,columns=cols)
df.to_csv('data.csv',index=False)

            

