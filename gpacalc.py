from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pandas import *
#email=input("Email: ")
#password=input("Password: ")
def setup_and_data(email,password):
    print("\nLogging you in...")
    browser=webdriver.Chrome("chromedriver.exe")
    browser.implicitly_wait(20)
    browser.get("http://parents.genesisedu.com/mcvts")
    user=browser.find_element_by_id("j_username")
    user.send_keys(email)
    passw=browser.find_element_by_id("j_password")
    passw.send_keys(password)
    login=browser.find_element_by_xpath("//input[@type='submit']")
    login.click()
    print("Obtaining data...")
    tabs=browser.find_elements_by_class_name("headerCategoryTab")
    for each in tabs:
        if each.text=="Grading":
            each.click()
            break
    table=read_html(browser.page_source)[1]
    new_table=DataFrame(columns=["Courses","MP1","MP2","MP3","MP4","Credits"])
    d={"Courses":None,"MP1":None,"MP2":None,"MP3":None,"MP4":None,"Credits":None}
    for a in range(3,table.shape[0]):
        d["Courses"]=table[0][a]
        d["Credits"]=table[16][a]
        new_table=new_table.append(d,ignore_index=True)
    new_table.index=new_table["Courses"]
    courses=list(new_table["Courses"])
    del new_table["Courses"]
    tabs=browser.find_elements_by_class_name("headerCategoryTab")
    for each in tabs:
        if each.text=="Gradebook":
            each.click()
            break
    for b in range(4):
        browser.find_element_by_xpath("//select[@name=\'fldMarkingPeriod\']/option[@value=\'MP"+str(b+1)+"\']").click()
        table=read_html(browser.page_source)[1]
        #print(table)
        a=3
        while a<table.shape[0]:
            if table[0][a+1][-1]=='%':
                new_table.at[table[0][a],"MP"+str(b+1)]=table[0][a+1]
                a+=2
            else:
                a+=1
    new_table=new_table.fillna('0.00%')
    means=[]
    for b in range(4):
        means.append(list(new_table["MP"+str(b+1)]))
    mean=[]
    for a in range(0,len(means[0])):
        mean.append(str((float(means[0][a][:-1])+float(means[1][a][:-1])+float(means[2][a][:-1])+float(means[3][a][:-1]))/4)+'%')
    new_table["Final Year"]=mean
    print(new_table)
    for a in range(6):
        if a!=4:
            grades=list(new_table[new_table.columns[a]])
            courses=list(new_table.index)
            for b in range(0,len(grades)):
                if float(grades[b][:-1])==0:
                    g=input("What is your exact grade percentage for "+courses[b]+" for "+new_table.columns[a]+'? If you only know the letter grade, put the minimum grade in percent for that letter grade. If you don\'t have a grade for this subject at this time, put N/A: ')
                    if g.lower()!="n/a":
                        if g[-1]!='%':
                            g+='%'
                        new_table.at[courses[b],new_table.columns[a]]=g
                    print('\n')
    mp1=calc_gpa('MP1',new_table)
    mp1w=calc_weighted('MP1',new_table)
    mp2=calc_gpa('MP2',new_table)
    mp2w=calc_weighted('MP2',new_table)
    mp3=calc_gpa('MP3',new_table)
    mp3w=calc_weighted('MP3',new_table)
    mp4=calc_gpa('MP4',new_table)
    mp4w=calc_weighted('MP4',new_table)
    final=calc_gpa('Final Year',new_table)
    finalw=calc_weighted('Final Year',new_table)
    print("Unweighted data:")
    print("MP1 UW: "+str(mp1))
    print("MP2 UW: "+str(mp2))
    print("MP3 UW: "+str(mp3))
    print("MP4 UW: "+str(mp4))
    print("Final UW: "+str(final))
    print("Weighted data:")
    print("MP1 W: "+str(mp1w))
    print("MP2 W: "+str(mp2w))
    print("MP3 W: "+str(mp3w))
    print("MP4 W: "+str(mp4w))
    print("Final W: "+str(finalw))
def classify(grade,w):
    if w==0:
        if float(grade[:-1])>=97.5:
            return 4.33
        elif float(grade[:-1])>=91.5:
            return 4.00
        elif float(grade[:-1])>=89.5:
            return 3.67
        elif float(grade[:-1])>=85.5:
            return 3.33
        elif float(grade[:-1])>=81.5:
            return 3.00
        elif float(grade[:-1])>=79.5:
            return 2.67
        elif float(grade[:-1])>=75.5:
            return 2.33
        elif float(grade[:-1])>=71.5:
            return 2.00
        elif float(grade[:-1])>=69.5:
            return 1.67
        elif float(grade[:-1])>=64.5:
            return 1.33
        else:
            return 0.00
    elif w=='A':
        if float(grade[:-1])>=97.5:
            return 5.33
        elif float(grade[:-1])>=91.5:
            return 5.00
        elif float(grade[:-1])>=89.5:
            return 4.67
        elif float(grade[:-1])>=85.5:
            return 4.33
        elif float(grade[:-1])>=81.5:
            return 4.00
        elif float(grade[:-1])>=79.5:
            return 3.67
        elif float(grade[:-1])>=75.5:
            return 3.33
        elif float(grade[:-1])>=71.5:
            return 3.00
        elif float(grade[:-1])>=69.5:
            return 2.67
        elif float(grade[:-1])>=64.5:
            return 2.33
        else:
            return 0.00
    elif w=='H':
        if float(grade[:-1])>=97.5:
            return 4.73
        elif float(grade[:-1])>=91.5:
            return 4.50
        elif float(grade[:-1])>=89.5:
            return 4.17
        elif float(grade[:-1])>=85.5:
            return 3.83
        elif float(grade[:-1])>=81.5:
            return 3.50
        elif float(grade[:-1])>=79.5:
            return 3.17
        elif float(grade[:-1])>=75.5:
            return 2.83
        elif float(grade[:-1])>=71.5:
            return 2.50
        elif float(grade[:-1])>=69.5:
            return 2.17
        elif float(grade[:-1])>=64.5:
            return 1.83
        else:
            return 0.00
def calc_gpa(s,df):
    grades=list(df[s])
    creds=list(map(float,list(df["Credits"])))
    courses=list(df.index)
    uw=0
    cred=set()
    for a in range(len(grades)):
        if float(grades[a][:-1])!=0:
            uw+=classify(grades[a],0)*float(creds[a])
        else:
            cred.add(a)
    for each in cred:
        del creds[each]
    uw/=sum(creds)
    return uw
def calc_weighted(s,df):
    grades=list(df[s])
    creds=list(map(float,list(df["Credits"])))
    courses=list(df.index)
    w=0
    cred=set()
    for a in range(len(grades)):
        if float(grades[a][:-1])!=0:
            if "honors" in courses[a].lower().split():
                w+=classify(grades[a],'H')*float(creds[a])
            elif "ap" in courses[a].lower().split() or "ib" in courses[a].lower().split():
                w+=classify(grades[a],'A')*float(creds[a])
            else:
                w+=classify(grades[a],0)*float(creds[a])
        else:
            cred.add(a)
            print("YES")
    for each in cred:
        del creds[each]
    w/=sum(creds)
    return w
if __name__=='__main__':
    print("Welcome to GPA Calculator, specifically designed for Genesis.")
    email=input("Email: ")
    passw=input("Password: ")
    grades=setup_and_data(email,passw)
