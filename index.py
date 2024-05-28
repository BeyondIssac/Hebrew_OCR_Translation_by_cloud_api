from flask import Flask, redirect, url_for, render_template, jsonify, send_from_directory, current_app, request, session
from translatepy.translators.google import GoogleTranslate, Language
from flask_mail import Mail, Message
from pathlib import Path
import os
import config
from categorize_string import *
from edit_docx import *

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kur86597@gmail.com'
app.config['MAIL_PASSWORD'] = 'apjfzfxciucpqwep'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index.html', data={})

@app.route('/get_access', methods=['POST'])
def get_access():
    token = config.get_access_token() 
    response = {
        "token_value": token
    }
    return jsonify(response)

@app.route('/createDocxFile', methods=['POST'])
def createDocxFile():
    src = request.get_json().get('to')
    read_edit_docx(src)
    print(src)
    result = {
        "data" : "data",
    }
    return jsonify(result)


@app.route('/download/<filename>')
def download_file(filename):
    static_folder = os.path.join(current_app.root_path, 'static')
    return send_from_directory(static_folder, filename, as_attachment=True)


@app.route('/send_file', methods=['POST'])
def send_file():

    recipient_email = request.get_json().get('recipient')

    file_path = Path("static/result_document.pdf")  # Replace with the actual file path
    with file_path.open(mode="rb") as file:
        file_data = file.read()

    msg = Message("Email with File Attachment",
                  sender="kur86597@gmail.com",
                  recipients=[recipient_email])
    msg.body = "Please find the attached file."
    msg.attach(file_path.name, "application/pdf", file_data)  # Attach the file

    mail.send(msg)
    return "success"

@app.route('/treat_translated_text', methods=['POST'])
def treat_translated_text():

    Hebrew_words_combination = []
    src = request.get_json().get('to')

    for i in range(len(src)):
        Hebrew_words_combination.append(src[i]['translatedText'])
        # print(src[i]['translatedText'])
    # name_list = []
    # name_list.append(request.get_json().get('lastname'))
    # name_list.append(request.get_json().get('firstname'))
    # name_list.append(request.get_json().get('father_firstname'))
    # name_list.append(request.get_json().get('mother_firstname'))
    # name_list.append(request.get_json().get('grandfa_firstname'))
    
    name_arr = []
    value_arr = []
    name_arr0 = []
    value_arr0 = []
    return_arr = {}
    [name_arr, value_arr, name_arr0, value_arr0] = categorize_sections(Hebrew_words_combination)
    
    if("first_name" not in name_arr0):
        return_arr["First Name"] = ""
    else:
        return_arr["First Name"] = value_arr0[name_arr0.index("first_name")]

    if("first name of father" not in name_arr0):
        return_arr["First Name of Father"] = ""
    else:
        return_arr["First Name of Father"] = value_arr0[name_arr0.index("first name of father")]

    if("first name of mother" not in name_arr0):
        return_arr["First Name of Mother"] = ""
    else:
        return_arr["First Name of Mother"] = value_arr0[name_arr0.index("first name of mother")]

    if("first name of father of father" not in name_arr0):
        return_arr["First Name of Father of Father"] = ""
    else:
        return_arr["First Name of Father of Father"] = value_arr0[name_arr0.index("first name of father of father")]

    if("last_name" not in name_arr0):
        return_arr["Last Name"] = ""
    else:
        return_arr["Last Name"] = value_arr0[name_arr0.index("last_name")]


    if("Sex" not in name_arr):
        return_arr["Sex"] = ""
    else:
        return_arr["Sex"] = value_arr[name_arr.index("Sex")]
    if("ID number" not in name_arr):
        return_arr["ID number"] = ""
    else:
        return_arr["ID number"] = value_arr[name_arr.index("ID number")]
    if("Nationality" not in name_arr):
        return_arr["Nationality"] = ""
    else:
        return_arr["Nationality"] = value_arr[name_arr.index("Nationality")]
    if("Religion" not in name_arr):
        return_arr["Religion"] = ""
    else:
        return_arr["Religion"] = value_arr[name_arr.index("Religion")]
    if("Date of change of nationality" not in name_arr):
        return_arr["Date of change of nationality"] = ""
    else:
        return_arr["Date of change of nationality"] = value_arr[name_arr.index("Date of change of nationality")]
    if("Date of change of religion" not in name_arr):
        return_arr["Date of change of religion"] = ""
    else:
        return_arr["Date of change of religion"] = value_arr[name_arr.index("Date of change of religion")]
    if("Marital status" not in name_arr):
        return_arr["Marital status"] = ""
    else:
        return_arr["Marital status"] = value_arr[name_arr.index("Marital status")]
        if("bachelor" in return_arr["Marital status"] .lower()):
            return_arr["Marital status"]  = "Single"
    if("Date of change of Marital status" not in name_arr):
        return_arr["Date of change of Marital status"] = ""
    else:
        return_arr["Date of change of Marital status"] = value_arr[name_arr.index("Date of change of Marital status")]
    if("State of birth" not in name_arr):
        return_arr["State of birth"] = ""
    else:
        return_arr["State of birth"] = value_arr[name_arr.index("State of birth")]
    if("City of birth" not in name_arr):
        return_arr["City of birth"] = ""
    else:
        return_arr["City of birth"] = value_arr[name_arr.index("City of birth")]

    if("Gregorian date of birth" not in name_arr):
        return_arr["Gregorian date of birth"] = ""
    else:
        return_arr["Gregorian date of birth"] = value_arr[name_arr.index("Gregorian date of birth")]
    if("Date of entrance to Israel" not in name_arr):
        return_arr["Date of entrance to Israel"] = ""
    else:
        return_arr["Date of entrance to Israel"] = value_arr[name_arr.index("Date of entrance to Israel")]
    if("Status" not in name_arr):
        return_arr["Status"] = ""
    else:
        return_arr["Status"] = value_arr[name_arr.index("Status")]
        if("costs" in return_arr["Status"].lower()):
            return_arr["Status"] = "Immigrant"
    if("Registration date as an immigrant / permanent resident" not in name_arr):
        return_arr["Registration date as an immigrant / permanent resident"] = ""
    else:
        return_arr["Registration date as an immigrant / permanent resident"] = value_arr[name_arr.index("Registration date as an immigrant / permanent resident")]
    if("Address" not in name_arr):
        return_arr["Address"] = ""
    else:
        return_arr["Address"] = value_arr[name_arr.index("Address")]
    if("Date of entry to the address" not in name_arr):
        return_arr["Date of entry to the address"] = ""
    else:
        return_arr["Date of entry to the address"] = value_arr[name_arr.index("Date of entry to the address")]
    if("IssuedOn" not in name_arr):
        return_arr["IssuedOn"] = ""
    else:
        return_arr["IssuedOn"] = value_arr[name_arr.index("IssuedOn")]
    if("Notes" not in name_arr):
        return_arr["Notes"] = ""
    else:
        return_arr["Notes"] = value_arr[name_arr.index("Notes")]
    if("AuthorityIn" not in name_arr):
        return_arr["AuthorityIn"] = ""
    else:
        return_arr["AuthorityIn"] = value_arr[name_arr.index("AuthorityIn")]

    response = {
        "FirstName" : return_arr["First Name"],
        "LastName" : return_arr["Last Name"],
        "FirstNameofFather" : return_arr["First Name of Father"],
        "FirstNameofMother": return_arr["First Name of Mother"],
        "FirstNameofFather": return_arr["First Name of Father"],
        "FirstNameofFatherofFather": return_arr["First Name of Father of Father"],

        "Sex" : return_arr["Sex"],
        "IDnumber" : return_arr["ID number"],
        "Nationality" : return_arr["Nationality"],
        "Religion" : return_arr["Religion"],
        "DateNationality" : return_arr["Date of change of nationality"],
        "DateReligion" : return_arr["Date of change of religion"],
        "MaritalStatus" : return_arr["Marital status"],
        "DateMarital" : return_arr["Date of change of Marital status"],
        "StateBirth" : return_arr["State of birth"],
        "CityBirth" : return_arr["City of birth"],
        "HebrewBirth" : "---",
        "GregorianBirth" : return_arr["Gregorian date of birth"],
        "DateEntrance" : return_arr["Date of entrance to Israel"],
        "Status" : return_arr["Status"],
        "RegistrationDate" : return_arr["Registration date as an immigrant / permanent resident"],
        "Address" : return_arr["Address"],
        "DateEntry" : return_arr["Date of entry to the address"],
        "IssuedOn" : return_arr["IssuedOn"],
        "Notes" : "",
        "AuthorityIn" : return_arr["AuthorityIn"],
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0")