import numpy as np
from edit_docx import *
from doc2pdf import *



def contain_date(ch_str):

    if("january" in ch_str or "february" in ch_str or "march" in ch_str or "april" in ch_str or "may" in ch_str or "june" in ch_str or "july" in ch_str or "august" in ch_str or "september" in ch_str or "october" in ch_str or "november" in ch_str or "december" in ch_str):
        return True
    else:
        return False
    
def extract_date(ch_str):
    fst_pos = -1
    lst_pos = -1
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    for i in np.arange(12):
        if(months[i] in ch_str):
            fst_pos = ch_str.find(months[i])
            lst_pos = fst_pos + len(months[i]) - 1
    fst_itl = fst_pos - 1
    lst_itl = lst_pos + 1

    while(fst_itl >= 0):
        if(ch_str[fst_itl] == ' ' or ch_str[fst_itl] == ','):
            fst_itl -= 1
            continue
        if(ch_str[fst_itl].isnumeric()):
            fst_pos = fst_itl
            fst_itl -= 1
        else:
            break

    while(lst_itl < len(ch_str)):
        if(ch_str[lst_itl] == ' ' or ch_str[lst_itl] == ','):
            lst_itl += 1
            continue
        if(ch_str[lst_itl].isnumeric()):
            lst_pos = lst_itl
            lst_itl += 1
        else:
            break

    return ch_str[fst_pos:lst_pos+1]

def is_ID_number(ch_str):
    is_ID = True
    for i in range(len(ch_str)):
        if(ch_str[i].isnumeric() == False and ch_str[i] != ' '):
            is_ID = False
            break
    return is_ID


def categorize_sections(str_arr):

    section_value_arr = []
    section_name_arr = []

    species_appears = 0
    appr_no_birthDate = 0
    appr_no_entryDate = 0
    appr_no_gregorian = 0

    changedDate_arr = []

    count_nationality = 0
    count_religion = 0
    count_maritalStatus = 0
    
    pos_fst_appr_name = 0
    pos_sex_value = 0

    for i in range(len(str_arr)):
        if("name" in str_arr[i].lower()):
            pos_fst_appr_name = i
            break

    for i in range(len(str_arr)):
        if("male" in str_arr[i].lower()):
            pos_sex_value = i
            break
    tmp_value_arr = []
    tmp_name_arr = []
    tmp_list = []

    for i in np.arange(pos_fst_appr_name, pos_sex_value):
        
        if("first" in str_arr[i].lower() and "name" in str_arr[i].lower()):
            if("father" not in str_arr[i+1].lower() and "mother" not in str_arr[i+1].lower()):
                if("name" not in str_arr[i+1].lower()  and "page" not in str_arr[i+1].lower() and "sex" not in str_arr[i+1].lower() and "nationality" not in str_arr[i+1].lower() and "id" not in str_arr[i+1].lower()):  # in the case of i+1 th line is name value
                    tmp_name_arr.append("first_name")
                    tmp_value_arr.append(str_arr[i+1]) 
                    i += 1
                    continue
                else:
                    tmp_list.append("first_name")
                    continue
            else:
                continue

        if("last" in str_arr[i].lower() and "name" in str_arr[i].lower()):
            if("name" not in str_arr[i+1].lower()  and "page" not in str_arr[i+1].lower() and "father" not in str_arr[i+1].lower() and "mother" not in str_arr[i+1].lower() and "sex" not in str_arr[i+1].lower() and "nationality" not in str_arr[i+1].lower() and "id" not in str_arr[i+1].lower()):  # in the case of i+1 th line is name value
                    tmp_name_arr.append("last_name")
                    tmp_value_arr.append(str_arr[i+1])
                    print("last name is ", str_arr[i+1])
                    i += 1
            else:
                tmp_list.append("last_name")
            continue

        if(str_arr[i].lower().count("father") == 1):
            if("name" not in str_arr[i+1].lower() and "father" not in str_arr[i+1].lower() and "mother" not in str_arr[i+1].lower() and "page" not in str_arr[i+1].lower() and "sex" not in str_arr[i+1].lower() and "nationality" not in str_arr[i+1].lower() and "id" not in str_arr[i+1].lower()):
                tmp_name_arr.append("first name of father")
                tmp_value_arr.append(str_arr[i+1])
                i += 1
            else:
                tmp_list.append("first name of father")
            continue

        if(str_arr[i].lower().count("father") == 2):
            if("name" not in str_arr[i+1].lower() and "father" not in str_arr[i+1].lower() and "mother" not in str_arr[i+1].lower() and "page" not in str_arr[i+1].lower() and "sex" not in str_arr[i+1].lower() and "nationality" not in str_arr[i+1].lower() and "id" not in str_arr[i+1].lower()):
                tmp_name_arr.append("first name of father of father")
                tmp_value_arr.append(str_arr[i+1])
                i += 1
            else:
                tmp_list.append("first name of father of father")
            continue

        if("mother" in str_arr[i].lower()):
            if("name" not in str_arr[i+1].lower() and "father" not in str_arr[i+1].lower() and "mother" not in str_arr[i+1].lower() and "page" not in str_arr[i+1].lower() and "sex" not in str_arr[i+1].lower() and "nationality" not in str_arr[i+1].lower() and "id" not in str_arr[i+1].lower()):
                tmp_name_arr.append("first name of mother")
                tmp_value_arr.append(str_arr[i+1])
                i += 1
            else:
                tmp_list.append("first name of mother")
            continue

        if("name" in str_arr[i].lower() or "sex" in str_arr[i].lower() or "id" in str_arr[i].lower() or "page" in str_arr[i].lower() or "nationality" in str_arr[i].lower() ):
            continue


        if(len(tmp_list)):
            tmp_name_arr.append(tmp_list[0])
            tmp_value_arr.append(str_arr[i])
            tmp_list.pop(0)

    print("this is tmp_name_arr", tmp_name_arr)

    print("this is tmp_value_arr", tmp_value_arr)
        

    for i in range(len(str_arr)):
        if("species" in str_arr[i].lower() or "sex" in str_arr[i].lower()):
            species_appears = i
            break

    tmp_section_list = []
    i = species_appears - 1
    
    while i < len(str_arr)-2:
        i += 1

        if("hebrew" in str_arr[i].lower()):
            continue
        if("gregorian" in str_arr[i].lower()):
            appr_no_gregorian = 1
            continue

        if((appr_no_gregorian == 0) and (contain_date(str_arr[i].lower())) and ('date' not in str_arr[i].lower()) ):
            changedDate_arr.append(str_arr[i].lower())
            continue
        
        if("nationality" in str_arr[i].lower()):
            count_nationality += 1
            if(count_nationality == 2):
                continue
        
        if("religion" in str_arr[i].lower()):
            count_religion += 1
            if(count_religion == 2):
                continue

        if("marital" in str_arr[i].lower() or "personal" in str_arr[i].lower() or "family" in str_arr[i].lower()):
            count_maritalStatus += 1
            if(count_maritalStatus == 2):
                continue
        
        if("change" in str_arr[i].lower() and "date" in str_arr[i].lower()):
            continue
        


        if(("address" not in str_arr[i-1].lower()) and is_ID_number(str_arr[i])):
            section_name_arr.append("ID number")
            section_value_arr.append(str_arr[i])
            continue
        
        # if("date" in str_arr[i].lower() and "change" in str_arr[i].lower() and "religion" in str_arr[i+1].lower()):
        #     i += 1
        #     if(contain_date(str_arr[i+1].lower())):
        #         i += 1
        #         section_name_arr.append("Date of change of religion")
        #         section_value_arr.append(str_arr[i])
        #     else:
        #         tmp_section_list.append("Date of change of religion")
        #     continue
        # if("date" in str_arr[i].lower() and "change" in str_arr[i].lower() and "nationality" in str_arr[i+1].lower()):    
        #     i += 1
        #     if(contain_date(str_arr[i+1].lower())):
        #         i += 1
        #         section_name_arr.append("Date of change of nationality")
        #         section_value_arr.append(str_arr[i])
        #     else:
        #         tmp_section_list.append("Date of change of nationality")
        #     continue
        if("date" in str_arr[i].lower() and "birth" in str_arr[i].lower() and appr_no_birthDate == 0):    
            appr_no_birthDate = 1
            # if(contain_date(str_arr[i+1].lower())):
                # i += 1
                # section_name_arr.append("Hebrew date of birth")
                # section_value_arr.append(str_arr[i])
            # else:
                # tmp_section_list.append("Hebrew date of birth")
            tmp_section_list.append("Hebrew date of birth")
            continue
        if("date" in str_arr[i].lower() and "birth" in str_arr[i].lower() and appr_no_birthDate == 1):
            if(contain_date(str_arr[i+1].lower())):
                i += 1
                section_name_arr.append("Gregorian date of birth")
                section_value_arr.append(str_arr[i])
            else:
                tmp_section_list.append("Gregorian date of birth")
            continue

        if("date" in str_arr[i].lower() and "registration" in str_arr[i].lower() and ("permanent" in str_arr[i+1].lower() or "immigrant" in str_arr[i+1].lower())):
            # this is 'registration date', so split date from str_arr[i+1]
            "Registration date as an immigrant / permanent resident"
            i += 1
            if(contain_date(str_arr[i].lower())):
                section_name_arr.append("Registration date as an immigrant / permanent resident")
                section_value_arr.append(extract_date(str_arr[i].lower()))
            elif(contain_date(str_arr[i+1].lower())):
                i += 1
                section_name_arr.append("Registration date as an immigrant / permanent resident")
                section_value_arr.append(str_arr[i])
            else:
                tmp_section_list.append("Registration date as an immigrant / permanent resident")
            continue
        if("species" in str_arr[i].lower() or "sex" in str_arr[i].lower()):
            if(str_arr[i+1].lower() == 'male' or str_arr[i+1].lower() == 'female'):
                i += 1
                section_name_arr.append("Sex")
                section_value_arr.append(str_arr[i][0].upper()+str_arr[i][1:])
            else:
                tmp_section_list.append("Sex")
            continue

        if("nationality" in str_arr[i].lower()):
            tmp_section_list.append("Nationality")
            continue

        if("id" in str_arr[i].lower() and "number" in str_arr[i].lower()):
        #     tmp_section_list.append("ID number")
            continue

        if("religion" in str_arr[i].lower()):     
            tmp_section_list.append("Religion")
            continue

        if(("family" in str_arr[i].lower() and "status" in str_arr[i].lower()) or ("marital" in str_arr[i].lower() and "status" in str_arr[i].lower()) or ("personal" in str_arr[i].lower() and "situation" in str_arr[i].lower())):
            tmp_section_list.append("Marital status")
            continue

        # if("family" in str_arr[i].lower() and "status" in str_arr[i].lower() and "date" in str_arr[i].lower()) or ("marital" in str_arr[i].lower() and "status" in str_arr[i].lower() and "date" in str_arr[i].lower()) or ("personal" in str_arr[i].lower() and "situation" in str_arr[i].lower() and "date" in str_arr[i].lower()):
        #     i += 1
        #     if(contain_date(str_arr[i+1].lower())):
        #         i += 1
        #         section_name_arr.append("Date of change of Marital status")
        #         section_value_arr.append(str_arr[i])
        #     else:
        #         tmp_section_list.append("Date of change of Marital status")
        #     continue

        if(("state" in str_arr[i].lower() or "country" in str_arr[i].lower() or "place" in str_arr[i].lower()) and "birth" in str_arr[i].lower()):
            tmp_section_list.append("State of birth")
            continue

        if(("city" in str_arr[i].lower() and "birth" in str_arr[i].lower()) or ("return" in str_arr[i].lower())):
            tmp_section_list.append("City of birth")
            continue

        if(("entry" in str_arr[i].lower() or "entrance" in str_arr[i].lower()) and "date" in str_arr[i].lower() and appr_no_entryDate == 0):
            appr_no_entryDate = 1
            if(contain_date(str_arr[i].lower())):
                section_name_arr.append("Date of entrance to Israel")
                section_value_arr.append(extract_date(str_arr[i].lower()))
            elif(contain_date(str_arr[i+1].lower())):
                i += 1
                section_name_arr.append("Date of entrance to Israel")
                section_value_arr.append(str_arr[i])
            else:
                tmp_section_list.append("Date of entrance to Israel")
            continue

        if("class" in str_arr[i].lower() or "status" in str_arr[i].lower()):
            tmp_section_list.append("Status")
            continue

        if("address" in str_arr[i].lower() or "whom" in str_arr[i].lower()):
            rlt = str_arr[i][str_arr[i].find(':')+1:]
            while "date" not in str_arr[i+1] and "entry" not in str_arr[i+1]:
                i += 1
                rlt += str_arr[i]
            # tmp_section_list.append("Address")
            section_name_arr.append("Address")
            section_value_arr.append(rlt)
            continue

        if("date" in str_arr[i].lower() and "entry" in str_arr[i].lower()):
            if(contain_date(str_arr[i].lower())):
                section_name_arr.append("Date of entry to the address")
                section_value_arr.append(extract_date(str_arr[i].lower()))
            elif(contain_date(str_arr[i+1].lower())):
                i += 1
                section_name_arr.append("Date of entry to the address")
                section_value_arr.append(str_arr[i])
            else:
                tmp_section_list.append("Date of entry to the address")
            continue
        
        if(("remark" in str_arr[i].lower() or "note" in str_arr[i].lower()) and "certificate" not in str_arr[i+1][:15].lower()):
            # print("###### we visit remarks")
            section_name_arr.append("Notes")
            section_value_arr.append(str_arr[i+1])
            i += 1
            while i < len(str_arr) - 1:
                i += 1
                if(contain_date(str_arr[i].lower())):
                    section_name_arr.append("IssuedOn")
                    section_value_arr.append(extract_date(str_arr[i].lower()))
                    continue
                if("authority" in str_arr[i].lower()):
                    section_name_arr.append("AuthorityIn")
                    section_value_arr.append(str_arr[i][str_arr[i].lower().find("authority")+13:])
            continue
        
        # print(str_arr[i])

        if(len(tmp_section_list)):
            print("current value is ", str_arr[i])
            print("inserted value is ", tmp_section_list[0], " & ",str_arr[i])
            # if("sex" in tmp_section_list[0]):
            #     print("Opops, we find 'sex' in tmp_section_list")
            if(("sex" in tmp_section_list[0].lower() or "species" in tmp_section_list[0].lower()) and ("male" not in str_arr[i].lower() and "female" not in str_arr[i].lower())):
                continue
            section_name_arr.append(tmp_section_list[0])
            section_value_arr.append(str_arr[i])
            tmp_section_list.pop(0)


    ind_date_lit = 0
    tmp_arr = [count_nationality, count_religion, count_maritalStatus]
    tmporary_name_arr = ["Date of change of nationality", "Date of change of religion", "Date of change of Marital status"]

    print(tmp_arr)
    print(changedDate_arr)

    for i in range(3):
        if(tmp_arr[i] < 2):
            continue
        else:
            if(len(changedDate_arr) <= ind_date_lit):
                continue
            section_name_arr.append(tmporary_name_arr[i])
            section_value_arr.append(changedDate_arr[ind_date_lit])
            ind_date_lit += 1

    # read_edit_docx(section_name_arr, section_value_arr)
    # if(convert_docx2pdf()):
    #     return True
    # else:
    #     return False
    return [section_name_arr, section_value_arr, tmp_name_arr, tmp_value_arr]    


# file = open("translatedText.txt", "r")
# file_content = file.read()
# rlt = file_content.split("\n")
# categorize_sections(rlt)
