import pandas as pd
import datetime
from datetime import date
from datetime import timedelta
from calendar import isleap
from faker import Faker
import random
from tkinter import *
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from functools import partial
from tkinter import filedialog
import time
import numpy as np
from sklearn.utils import shuffle

# Takes user input for record generation
# num = int(input('How many records do you want to generate? :'))

fake = Faker()

# List of data for random function
l_state = ['WA','AL','AK','CA','IN','TX','NY']
l_city = {'WA':['South Creek','Roslyn','Sprague','Gig Harbor','Lake Cassidy','Tenino'],'AL':['Moores Mill','Sanford','Thomasville','Smoke Rise','Kellyton','Town Creek'],'AK':['Oscarville','Kasaan','Mountain Village','Tanana'],'CA':['Patterson Tract','Redcrest','Madera','Brooktrails'],'IN':['Liberty','Griffin','Wakarusa','Whitewater'],'TX':['San Saba','Zapata','Hearne','Hudson Oaks'],'NY':['Inwood','Plattsburgh','Sanborn','Almond']}
l_dedct = ['500.00','1000.00','1500.00','2000.00']
l_edu = ['High School','Graduate','Masters']
l_reln = ['Self','Spouse','Mother','Father','Child','Blood Relative','Not Related']
l_inc_type = ['Single Vehicle Collision','Multi Vehicle Collision','Vehicle Theft']
l_inc_sev = ['Minor Damage','Major Damage','Total Loss']
bool_dmg = ['YES','NO']
l_auto_mk = ['HONDA','FORD','MERCEDES','DODGE','BMW','FAIT','GM','KIA','HYUNDAI','NISSAN','VOLVO','TOYOTA','TESLA']


def char_mask(str):
    ssn = list(str)
    #     print("Original SSN as list : ", ssn)
    #     print("Length of SSN list :", len(ssn))
    # create a new dictionary
    charDictionary = dict()
    digitList = list()
    count = 0

    for s in ssn:
        if (s.isdigit()):
            digitList.append(s)

        else:
            charDictionary.update({count: s})
        count += 1

    # Generate the strings with original format.
    result = ""
    count2 = 0
    np.random.shuffle(digitList)

    for i in range(len(ssn)):
        if i in charDictionary:
            result = result + charDictionary[i]

        else:
            result = result + digitList[count2]
            count2 += 1

    return result


# defines function to increase date of birth with 18 years for generating customer effective date
def add_years(d, years):
    new_year = d.year + years
    try:
        return d.replace(year=new_year)
    except ValueError:
        if (d.month == 2 and d.day == 29 and # leap day
            isleap(d.year) and not isleap(new_year)):
            return d.replace(year=new_year, day=28)
        raise


# Defines function to generate customer effective date greater than DOB
def gen_eff_date(dob):
    ad_yr = add_years(dob, 18)
    eff = fake.date_between(start_date="-20y", end_date="-3y")
    x = int(eff.year) > int(ad_yr.year)

    if x:
        cust_eff_date = eff
    else:
        cust_eff_date = ad_yr

    return cust_eff_date


# Defines function to generate bind date greater than customer effective date
def gen_bind_date(cust_eff_date):
    deff = fake.date_between(start_date="-6y", end_date="-2y")
    x = int(deff.year) > int(cust_eff_date.year)

    randtemp = random.randint(0, 310)

    if x:
        bind_date = deff
    else:
        bind_date = deff + datetime.timedelta(days=randtemp)
    return bind_date

# defines phone number in XXX-XXX-XXXX format
def gen_phn():
    first = str(random.randint(100,999))
    second = str(random.randint(1,888)).zfill(3)
    last = (str(random.randint(1,9998)).zfill(4))
    return '{}-{}-{}'.format(first,second,last)


# defines function to generate independent columns
def gen_all_col():
    pol_num = random.randint(1000000,9999999)
    ssn = fake.ssn()
    phn = gen_phn()
    dob = fake.date_of_birth(minimum_age=18,maximum_age=80)
    cust_eff_dt = gen_eff_date(dob)
    bind_dt = gen_bind_date(cust_eff_dt)
    today = datetime.date.today()
    age = today.year-dob.year
    gender = 'M' if random.randint(0,1)==0 else 'F'
    name = fake.name_male() if gender=='M' else fake.name_female()
    ins_state = random.choice(l_state)
    ins_city = random.choice(l_city[ins_state])
    ins_add = fake.address()
    pol_deduct = random.choice(l_dedct)
    ann_prem = round(random.uniform(4000,10000),2)
    umb_lmt = round((ann_prem*12),-4)
    zip = fake.zipcode()
    edu_lvl = random.choice(l_edu)
    job = fake.job()
    relation = random.choice(l_reln)
    inc_dt = fake.date_between(start_date="-500d", end_date="-60d")
    inc_type = random.choice(l_inc_type)
    inc_sev = random.choice(l_inc_sev)
    inc_state = random.choice(l_state)
    inc_city = random.choice(l_city[inc_state])
    inc_loc = fake.address()
    num_veh_col = random.randint(2, 4) if inc_type == 'Multi Vehicle Collision' else 1
    prop_dmg = random.choice(bool_dmg)
    prop_clm = round(random.uniform(500, ann_prem * 3.3), 2) if prop_dmg == 'YES' else 0
    bod_injy = 0 if inc_type=='Vehicle Theft' else random.randint(1,2)
    inj_clm = round(random.uniform(100, ann_prem * 1.8), 2) if bod_injy == 1 else round(random.uniform(500, ann_prem * 3.3),2) if bod_injy == 2 else 0
    veh_clm = round(random.uniform(900, ann_prem * 3.3), 2) if inc_sev=='Total Loss' else round(random.uniform(400, ann_prem * 2.5), 2) if inc_sev=='Major Dammage' else round(random.uniform(10, ann_prem * 0.5), 2)
    tot_clm_amt = prop_clm + inj_clm + veh_clm
    veh_num = fake.license_plate()
    auto_mk = random.choice(l_auto_mk)
    model_yr = random.randint((today.year - 15), today.year) if random.randint((today.year - 15), today.year) < int(inc_dt.year) else int(inc_dt.year)
    yield {'Customer_Effective_Date': cust_eff_dt, 'Policy_number': 'P' + str(pol_num), 'Name': name, 'SSN': ssn,
           'Phone_Number': phn, 'Policy_Bind_Date': bind_dt, 'D.O.B': dob, 'Age': age, 'Insured_sex': gender,
           'Policy_State': ins_state, 'Insured_City': ins_city, 'Insured_Address': ins_add,
           'Policy_Deductable': pol_deduct, 'Policy_Annual_Premium': ann_prem, 'Umbrella_Limit': umb_lmt,
           'Insured_Zip': zip, 'Insured_Education_Level': edu_lvl, 'Insured_Occupation': job,
           'Insured_Relationship': relation, 'Incident_Date': inc_dt, 'Incident_Type': inc_type,
           'Incident_Severity': inc_sev, 'Incident_State': inc_state, 'Incident_City': inc_city,
           'Incident_Location': inc_loc, 'No_of_vehicles_involved': num_veh_col, 'Property_Damage': prop_dmg,
           'Bodily_Injuries': bod_injy, 'Total_Claim_Amount': tot_clm_amt, 'Property_Claim': prop_clm,
           'Injury_Claim': inj_clm, 'Vehicle_Claim': veh_clm, 'License_Plate_Number': veh_num, 'Auto_Make': auto_mk,
           'Auto_Year': model_yr}


def get_data(num,label):
    start_time = time.time()
    str1 = num.get()
    num1 = int(str1)
# for loop to generate multiple values
    value1 = [value for i in range(num1) for value in gen_all_col()]
# converts to dataframe
    df = pd.DataFrame(value1)
# Loads data to a CSV file
    df.to_csv('C:\\Users\\sshankar\\Downloads\\SyntheticData.csv',index=False)
    label.config(text="Data loaded in 'SyntheticData.csv' successfully in 'C:/Users/sraina/PycharmProjects/Tekathon2019/Result Set' \nwith an execution time of %s seconds!" %round((time.time()-start_time),3))

# print(df)
# define browse functionality
def browsefunc():
    path = filedialog.askopenfilename()
    return path

# define function to de-identify data
def data_deidentify(label_d):
    fileName = browsefunc()
# making data frame
    dfMain = pd.read_csv(fileName)
    colNames = list(dfMain.columns)

# Policy Number
    dfPolicyNumber = dfMain['Policy_number']
    policyNumberList = list()
    for value in dfPolicyNumber:
        policyNumberList.append(char_mask(value))

    data = {'Policy_number': policyNumberList}
    dfPolNo = pd.DataFrame.from_dict(data)
    dfMain.drop("Policy_number", axis=1, inplace=True)
    dfMain = pd.concat([dfMain, dfPolNo], axis=1)

# SSN masking
    dfSsn = dfMain['SSN']
    ssnList = list()
    for value in dfSsn:
        ssnList.append(char_mask(value))

    data = {'SSN': ssnList}
    dfSsnNo = pd.DataFrame.from_dict(data)
    dfMain.drop("SSN", axis=1, inplace=True)
    dfMain = pd.concat([dfMain, dfSsnNo], axis=1)

# Phone Number masking
    dfPhoneNumber = dfMain['Phone_Number']
    phoneNumberList = list()
    for value in dfPhoneNumber:
        phoneNumberList.append(char_mask(value))

    data = {'Phone_Number': phoneNumberList}
    dfPhoneNo = pd.DataFrame.from_dict(data)
    dfMain.drop("Phone_Number", axis=1, inplace=True)
    dfMain = pd.concat([dfMain, dfPhoneNo], axis=1)

# dfLicensePlateNumber masking
    dfLicensePlateNumber = dfMain['License_Plate_Number']
    licensePlateNumberList = list()
    for value in dfLicensePlateNumber:
        licensePlateNumberList.append(char_mask(value))

    data = {'License_Plate_Number': licensePlateNumberList}
    dfLicenseNo = pd.DataFrame.from_dict(data)
    dfMain.drop("License_Plate_Number", axis=1, inplace=True)
    dfMain = pd.concat([dfMain, dfLicenseNo], axis=1)

    dfAge = dfMain['Age']
    dfDob = dfMain['D.O.B']
    dfAge.to_frame()
    dfDob.to_frame()
    dfTemp = pd.concat([dfAge, dfDob], axis=1)
    dfTemp = shuffle(dfTemp)
    dfTemp.reset_index(inplace=True, drop=True)
    dfMain.drop(["Age", "D.O.B"], axis=1, inplace=True)
    dfMain = pd.concat([dfMain, dfTemp], axis=1)

    dfNm = dfMain['Name']
    dfGen = dfMain['Insured_sex']
    dfNm.to_frame()
    dfGen.to_frame()
    dfTemp = pd.concat([dfNm, dfGen], axis=1)
    dfTemp = shuffle(dfTemp)
    dfTemp.reset_index(inplace=True, drop=True)
    dfMain.drop(["Name", "Insured_sex"], axis=1, inplace=True)
    dfMain = pd.concat([dfMain, dfTemp], axis=1)

    dfMain['Insured_Zip'] = np.random.permutation(dfMain['Insured_Zip'].values)
    dfMain['Insured_Occupation'] = np.random.permutation(dfMain['Insured_Occupation'].values)
    dfMain = dfMain[colNames]

    # print(dfMain)
    dfMain.to_csv('C:/Users/sraina/PycharmProjects/Tekathon2019/Result Set/output.csv', index=False)
    label_d.config(text="Data loaded in 'output.csv' successfully in C:/Users/sraina/PycharmProjects/Tekathon2019/Result Set.")


# # Prints success message in console
# print('\nData loaded in CSV file successfully!')

# Display setup in tkinter
root = tk.Tk()
root.geometry("800x400")
root.title('Synthetic Data Generator')
root.configure(background='#99ccff')

# declaring tkinter variables
record_count = tk.StringVar()

# declaring result label
label_result1 = tk.Label(root)
label_result1.place(x=30,y=300)
label_result2 = tk.Label(root)
label_result2.place(x=30,y=340)

# declaring labels and entry text field
count = Label(root,text='Enter record count:').place(x=40,y=80)
e1 = tk.Entry(root,textvariable=record_count).place(x=150,y=82)
data_generator = partial(get_data,record_count,label_result1)
data_deident = partial(data_deidentify,label_result2)



#declaring buttons and integrating them with actual functionality
gen_data = tk.Button(root,height=2,width=20,text = 'Generate Data',command=data_generator).place(x=40,y=150)
de_data = tk.Button(root,height=2,width=20,text = 'De-Identify Data',command=data_deident).place(x=400,y=80)
enc_data = tk.Button(root,height=2,width=20,text = 'Encrypt Data').place(x=400,y=150)

root.mainloop()
