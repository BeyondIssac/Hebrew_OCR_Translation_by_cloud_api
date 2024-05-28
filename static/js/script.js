let validata = false
let accessToken = ""
let inputType = ''

function validateFile(fileInput) {
  const allowedExtensions = /(\.jpg|\.jpeg|\.png|\.pdf)$/i;
  const fileError = document.getElementById('fileError');

  if (!allowedExtensions.exec(fileInput.value)) {
    fileInput.value = '';
    fileError.textContent = 'Please select a JPG, JPEG, PNG or PDF file.';
    fileError.style.display = 'block';
    return false;
  } else {
    fileError.style.display = 'none';
    return true;
  }
}

function getFileExtension(filename) {
  const extension = filename.split('.').pop();
  return extension;
}

function downloadFile(url, filename) {
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

$('#imageInput').change(function(){

  validata = validateFile(this)
  const fileExtension = getFileExtension(this.value);

  switch(fileExtension.toLowerCase()) {
    case 'jpg':
    case 'jpeg':
      inputType = 'image/jpeg';
      break;
    case 'png':
      inputType = 'image/png';
      break;
    case 'pdf':
      inputType = 'application/pdf';
      break;
    default:
      inputType = '';
      break;
  }

  fetch('/get_access', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ request_data: 'get_token'})
  })
  .then(response => response.json())
  .then(data=>{
    accessToken = data.token_value

    if(!validata) {
      const fileError = document.getElementById('fileError');
      fileError.textContent = 'Please input a correct file type.';
      fileError.style.display = 'block';
    }
    else {
      fileError.style.display = 'none';
      const imageInput = document.getElementById('imageInput');
      const imageFile = imageInput.files[0];
      // Create a new FileReader object
      const fileReader = new FileReader();    
      fileReader.onload = function() {
          const base64ImageWithPrefix = fileReader.result;
          // Remove the data URI prefix from the base64-encoded string
          const base64ImageWithoutPrefix = base64ImageWithPrefix.split(',')[1];
          fetch('https://eu-documentai.googleapis.com/v1/projects/679844559797/locations/eu/processors/fdac58f1e29315ea:process', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${accessToken}`
              },
              body: JSON.stringify(
                  {
                      "skipHumanReview": false,
                      "rawDocument": {
                      "mimeType": `${inputType}`,
                      "content": `${base64ImageWithoutPrefix}`
                      },
                      "fieldMask": "",
                      "processOptions": {
                      }
                  }
              )
          })
          .then(response => response.json())
          .then(data => {
            console.log("scrapted data from Document AI: ", data.document.text)
            fetch('https://translation.googleapis.com/language/translate/v2', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': `Bearer ${accessToken}`,
                "x-goog-user-project" : "graceful-earth-424212-e2",
            },
            body: JSON.stringify(
                {
                  "q": data.document.text.split('\n'),
                  "target": "en"
                }
            )
          })
          .then(response => response.json())
          .then(response_data => {
            console.log('translated data:', response_data.data.translations);
            
            fetch('/treat_translated_text', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ 
                to:response_data.data.translations
              })
            })
            .then(response => response.json())
            .then(data=>{
              console.log("treated data from backend :", data)

              document.getElementById("fst_name").value = data.FirstName
              document.getElementById("lst_name").value = data.LastName
              
              document.getElementById("fa_fst_name").value = data.FirstNameofFather
              document.getElementById("ma_fst_name").value = data.FirstNameofMother
              document.getElementById("grandfa_fst_name").value = data.FirstNameofFatherofFather




              document.getElementById("sex").value = data.Sex
              document.getElementById("nationality").value = data.Nationality
              document.getElementById("date_nationality").value = data.DateNationality
              document.getElementById("marital").value = data.MaritalStatus
              document.getElementById("date_marital").value = data.DateMarital
              document.getElementById("hebrew_birthday").value = data.HebrewBirth
              document.getElementById("date_entrance").value = data.DateEntrance
              document.getElementById("registration_date").value = data.RegistrationDate
              document.getElementById("id_number").value = data.IDnumber
              document.getElementById("religion").value = data.Religion
              document.getElementById("date_religion").value = data.DateReligion
              document.getElementById("date_marital").value = data.DateMarital
              document.getElementById("city_birth").value = data.CityBirth
              document.getElementById("stateBirth").value = data.StateBirth
              document.getElementById("gregorian_birth").value = data.GregorianBirth
              document.getElementById("status").value = data.Status
              document.getElementById("address").value = data.Address
              document.getElementById("date_entry").value = data.DateEntry
              document.getElementById("notes").value = data.Notes
              document.getElementById("authorityIn").value = data.AuthorityIn
              document.getElementById("issuedOn").value = data.IssuedOn
            })
            
            .catch(error => {
              console.error('Error:', error);
            });
          })
          .catch(error => {
            console.error('Error:', error);
          }); 
          })
          .catch(error => console.error(error));
      };
      fileReader.readAsDataURL(imageFile);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
})

$('#mailsend').click(function(){

  if(!validata) {
    const fileError = document.getElementById('fileError');
    fileError.textContent = 'Please input a correct file type.';
    fileError.style.display = 'block';
  }
  else{
      if( document.getElementById("recipient_address").value == "" ) {
        alert("Please enter recipient address")
        return
      }

      fetch('/send_file', {

        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          recipient: document.getElementById("recipient_address").value
        })
      })
      .then(response => response.text())
      .then(data => {
        if(data == "success"){
          alert("Message sent!")
        }
      })
      .catch(error => {
          alert("An error is occured during message transmission!")
      });
  }
})

$('#pdfDwnLd').click(function(){

  if(!validata) {
    const fileError = document.getElementById('fileError');
    fileError.textContent = 'Please input a correct file type.';
    fileError.style.display = 'block';
  }
  else {
        
      let value = {
        "fst_name" : document.getElementById("fst_name").value,
        "lst_name" : document.getElementById("lst_name").value,
        "fa_fst_name" : document.getElementById("fa_fst_name").value,
        "ma_fst_name" : document.getElementById("ma_fst_name").value,
        "grandfa_fst_name" : document.getElementById("grandfa_fst_name").value,
        
        "sex"  : document.getElementById("sex").value ,
        "nationality"  : document.getElementById("nationality").value,
        "date_nationality"  : document.getElementById("date_nationality").value,
        "marital"  : document.getElementById("marital").value,
        "date_marital"  : document.getElementById("date_marital").value,
        "hebrew_birth"  : document.getElementById("hebrew_birthday").value,
        "stateBirth" : document.getElementById("stateBirth").value,
        "date_entrance"  : document.getElementById("date_entrance").value ,
        "registration_date"  : document.getElementById("registration_date").value ,
        "id_number"  : document.getElementById("id_number").value,
        "religion"  : document.getElementById("religion").value ,
        "date_religion"  : document.getElementById("date_religion").value ,
        "date_marital"  : document.getElementById("date_marital").value,
        "city_birth"  : document.getElementById("city_birth").value ,
        "gregorian_birth"  : document.getElementById("gregorian_birth").value ,
        "status"  : document.getElementById("status").value,
        "address"  : document.getElementById("address").value ,
        "date_entry"  : document.getElementById("date_entry").value,
        "notes"  : document.getElementById("notes").value ,
        "authorityIn"  : document.getElementById("authorityIn").value ,
        "issuedOn"  : document.getElementById("issuedOn").value,
      }
      fetch('/createDocxFile', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          to: value
        })
      })
      .then(response => response.json())
      .then(data => {
        downloadFile('/static/result_document.pdf', 'result_document.pdf')
      })
      .catch(error => {
      console.error('Error:', error);
      });

    }
  

  
})

$('#wrdDwnLd').click(function(){
    console.log("You clicked word download button")
    if(!validata) {
      const fileError = document.getElementById('fileError');
      fileError.textContent = 'Please input a correct file type.';
      fileError.style.display = 'block';
    }
    else {
          let value = {
                  "fst_name" : document.getElementById("fst_name").value,
                  "lst_name" : document.getElementById("lst_name").value,
                  "fa_fst_name" : document.getElementById("fa_fst_name").value,
                  "ma_fst_name" : document.getElementById("ma_fst_name").value,
                  "grandfa_fst_name" : document.getElementById("grandfa_fst_name").value,
                  
                  "sex"  : document.getElementById("sex").value ,
                  "nationality"  : document.getElementById("nationality").value,
                  "date_nationality"  : document.getElementById("date_nationality").value,
                  "marital"  : document.getElementById("marital").value,
                  "date_marital"  : document.getElementById("date_marital").value,
                  "hebrew_birth"  : document.getElementById("hebrew_birthday").value,
                  "stateBirth" : document.getElementById("stateBirth").value,
                  "date_entrance"  : document.getElementById("date_entrance").value ,
                  "registration_date"  : document.getElementById("registration_date").value ,
                  "id_number"  : document.getElementById("id_number").value,
                  "religion"  : document.getElementById("religion").value ,
                  "date_religion"  : document.getElementById("date_religion").value ,
                  "date_marital"  : document.getElementById("date_marital").value,
                  "city_birth"  : document.getElementById("city_birth").value ,
                  "gregorian_birth"  : document.getElementById("gregorian_birth").value ,
                  "status"  : document.getElementById("status").value,
                  "address"  : document.getElementById("address").value ,
                  "date_entry"  : document.getElementById("date_entry").value,
                  "notes"  : document.getElementById("notes").value ,
                  "authorityIn"  : document.getElementById("authorityIn").value ,
                  "issuedOn"  : document.getElementById("issuedOn").value,
          }
          fetch('/createDocxFile', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
              to: value
            })
          })
          .then(response => response.json())
          .then(data => {
            downloadFile('/static/result_document.docx', 'result_document.docx')
          })
          .catch(error => {
            console.error('Error:', error);
          });

    }
       
})

$('#translate_btn').click(function(){
  if(!validata) {
    const fileError = document.getElementById('fileError');
    fileError.textContent = 'Please input a correct file type.';
    fileError.style.display = 'block';
  }
  else {
    fileError.style.display = 'none';
    const imageInput = document.getElementById('imageInput');
    const imageFile = imageInput.files[0];
    // Create a new FileReader object
    const fileReader = new FileReader();    
    fileReader.onload = function() {
        const base64ImageWithPrefix = fileReader.result;
        // Remove the data URI prefix from the base64-encoded string
        const base64ImageWithoutPrefix = base64ImageWithPrefix.split(',')[1];
        fetch('https://eu-documentai.googleapis.com/v1/projects/679844559797/locations/eu/processors/fdac58f1e29315ea:process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(
                {
                    "skipHumanReview": false,
                    "rawDocument": {
                    "mimeType": "image/jpeg",
                    "content": `${base64ImageWithoutPrefix}`
                    },
                    "fieldMask": "",
                    "processOptions": {
                    }
                }
            )
        })
        .then(response => response.json())
        .then(data => {
          console.log(data.document.text)
          fetch('https://translation.googleapis.com/language/translate/v2', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json; charset=utf-8',
              'Authorization': `Bearer ${accessToken}`,
              "x-goog-user-project" : "graceful-earth-424212-e2",
          },
          body: JSON.stringify(
              {
                "q": data.document.text.split('\n'),
                "target": "en"
              }
          )
        })
        .then(response => response.json())
        .then(response_data => {
          console.log('Server response:', response_data.data.translations);
          
          fetch('/treat_translated_text', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
              to:response_data.data.translations,
              lastname: document.getElementById('lst_name').value,
              firstname: document.getElementById('fst_name').value,
              father_firstname: document.getElementById('fa_fst_name').value,
              mother_firstname: document.getElementById('ma_fst_name').value,
              grandfa_firstname: document.getElementById('grandfa_fst_name').value,
            })
          })
          .then(response => response.json())
          
          .catch(error => {
            console.error('Error:', error);
          });
        })
        .catch(error => {
          console.error('Error:', error);
        }); 
        })
        .catch(error => console.error(error));
    };
    fileReader.readAsDataURL(imageFile);
  }
})