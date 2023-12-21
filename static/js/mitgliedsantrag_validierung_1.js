
/*
 ______  _______    ______   __    __ 
/      |/       \  /      \ /  \  /  |
$$$$$$/ $$$$$$$  |/$$$$$$  |$$  \ $$ |
  $$ |  $$ |__$$ |$$ |__$$ |$$$  \$$ |
  $$ |  $$    $$< $$    $$ |$$$$  $$ |
  $$ |  $$$$$$$  |$$$$$$$$ |$$ $$ $$ |
 _$$ |_ $$ |__$$ |$$ |  $$ |$$ |$$$$ |
/ $$   |$$    $$/ $$ |  $$ |$$ | $$$ |
$$$$$$/ $$$$$$$/  $$/   $$/ $$/   $$/ 
*/
/*
 * Returns true if the IBAN is valid 
 * Returns FALSE if the IBAN's length is not as should be (for CY the IBAN Should be 28 chars long starting with CY )
 * Returns any other number (checksum) when the IBAN is invalid (check digits do not match)
 */

function isValidIBANNumber(input) {
    var CODE_LENGTHS = {
        AD: 24, AE: 23, AT: 20, AZ: 28, BA: 20, BE: 16, BG: 22, BH: 22, BR: 29,
        CH: 21, CR: 21, CY: 28, CZ: 24, DE: 22, DK: 18, DO: 28, EE: 20, ES: 24,
        FI: 18, FO: 18, FR: 27, GB: 22, GI: 23, GL: 18, GR: 27, GT: 28, HR: 21,
        HU: 28, IE: 22, IL: 23, IS: 26, IT: 27, JO: 30, KW: 30, KZ: 20, LB: 28,
        LI: 21, LT: 20, LU: 20, LV: 21, MC: 27, MD: 24, ME: 22, MK: 19, MR: 27,
        MT: 31, MU: 30, NL: 18, NO: 15, PK: 24, PL: 28, PS: 29, PT: 25, QA: 29,
        RO: 24, RS: 22, SA: 24, SE: 24, SI: 19, SK: 24, SM: 27, TN: 24, TR: 26,   
        AL: 28, BY: 28, CR: 22, EG: 29, GE: 22, IQ: 23, LC: 32, SC: 31, ST: 25,
        SV: 28, TL: 23, UA: 29, VA: 22, VG: 24, XK: 20
    };
    var iban = String(input).toUpperCase().replace(/[^A-Z0-9]/g, ''), // keep only alphanumeric characters
            code = iban.match(/^([A-Z]{2})(\d{2})([A-Z\d]+)$/), // match and capture (1) the country code, (2) the check digits, and (3) the rest
            digits;
    // check syntax and length
    if (!code || iban.length !== CODE_LENGTHS[code[1]]) {
        return false;
    }
    // rearrange country code and check digits, and convert chars to ints
    digits = (code[3] + code[1] + code[2]).replace(/[A-Z]/g, function (letter) {
        return letter.charCodeAt(0) - 55;
    });
    // final check
    return mod97(digits) === 1;
}

function mod97(string) {
    var checksum = string.slice(0, 2), fragment;
    for (var offset = 2; offset < string.length; offset += 7) {
        fragment = String(checksum) + string.substring(offset, offset + 7);
        checksum = parseInt(fragment, 10) % 97;
    }
    return checksum;
}


/*
  ______   __     ________  ________  _______  
 /      \ /  |   /        |/        |/       \ 
/$$$$$$  |$$ |   $$$$$$$$/ $$$$$$$$/ $$$$$$$  |
$$ |__$$ |$$ |      $$ |   $$ |__    $$ |__$$ |
$$    $$ |$$ |      $$ |   $$    |   $$    $$< 
$$$$$$$$ |$$ |      $$ |   $$$$$/    $$$$$$$  |
$$ |  $$ |$$ |_____ $$ |   $$ |_____ $$ |  $$ |
$$ |  $$ |$$       |$$ |   $$       |$$ |  $$ |
$$/   $$/ $$$$$$$$/ $$/    $$$$$$$$/ $$/   $$/ 
*/

function pruefeAlter(geburtsdatum) {
    // Das Mindestalter festlegen (in Jahren)
    var mindestalter = 18;

    // Aktuelles Datum abrufen
    var aktuellesDatum = new Date();
    // Das Alter berechnen
    var alter = aktuellesDatum.getFullYear() - geburtsdatum.getFullYear();
    // Überprüfen, ob das Geburtstag dieses Jahr bereits stattgefunden hat
    if (aktuellesDatum.getMonth() < geburtsdatum.getMonth() || (aktuellesDatum.getMonth() === geburtsdatum.getMonth() && aktuellesDatum.getDate() < geburtsdatum.getDate())) {
        alter--;
    }
    // Das Ergebnis ausgeben
    if (alter >= mindestalter) {
        return true;
    } else {
        return false;
    }
}

/*
 ________         __             ______                          
/        |       /  |           /      \                         
$$$$$$$$/______  $$ |  ______  /$$$$$$  |______   _______        
   $$ | /      \ $$ | /      \ $$ |_ $$//      \ /       \       
   $$ |/$$$$$$  |$$ |/$$$$$$  |$$   |  /$$$$$$  |$$$$$$$  |      
   $$ |$$    $$ |$$ |$$    $$ |$$$$/   $$ |  $$ |$$ |  $$ |      
   $$ |$$$$$$$$/ $$ |$$$$$$$$/ $$ |    $$ \__$$ |$$ |  $$ |      
   $$ |$$       |$$ |$$       |$$ |    $$    $$/ $$ |  $$ |      
   $$/  $$$$$$$/ $$/  $$$$$$$/ $$/      $$$$$$/  $$/   $$/  
*/

function checkPhoneNumber(phoneNumber) {  
    // Regulärer Ausdruck für das erwartete Format: +1234567890
    const phoneRegex = /^\+\d{10,}$/;
  
    if (phoneRegex.test(phoneNumber)) {

      return true;
    } else {
      return false;
    }
}



function defaultProove() {
    console.log("defaultProove() called");
    var button = document.getElementById('validationButton');
	button.click();
    return 1;
}

function proove_alter(){
    var alter = document.getElementById('date1');
    var alter_val = new Date(alter.value);
 
    if (pruefeAlter(alter_val) != true){
        alter.setCustomValidity('Das erste Mitglied muss mindestens 18 sein, sollten Sie Ihr kind anmelden wollen, geben Sie sich als erstes Mitglied an und das Kind als zweites Mitglied.')
        return false;
    }else{
        alter.setCustomValidity(''); 
        return true;
    }

}

//return False if te evaluation failed
function proove_iban() {
    var iban = document.getElementById('iban');
    var iban_val = iban.value;
    console.log(iban_val)
    /* var phoneNumbers = document.querySelectorAll() */
    
    // Check if the IBAN is valid
    if (isValidIBANNumber(iban_val) != true) {
        iban.setCustomValidity('Bitte geben Sie eine gültige IBAN an.'); 
        return false;
    } else {
        iban.setCustomValidity('');
        return true;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Wait for the DOM to be fully loaded
    
    // Find the button by its ID or any other suitable selector
    var myButton = document.getElementById('submit_btn');
    var form = document.getElementById('antragsformular');
    // Add a click event listener to the button
    myButton.addEventListener('click', function (event) {
        defaultProove()
        if (proove_iban() === false | proove_alter() === false) {
            // If evaluation passed, prevent the default behavior of the click event
            event.preventDefault();

            // Check if the button has the data-callback attribute set to "onSubmit"
            if (myButton.getAttribute('data-callback') === 'onSubmit') {
                // Override or modify the onSubmit function to prevent its default behavior
                window.onSubmit = function () {
                };
            }

            // Continue with the default behavior or additional logic
            console.log('Default behavior or custom logic here');
        } else {
            defaultProove();
            // Evaluation failed, continue with the default behavior
            if (form.checkValidity()){
                console.log("test called")
                form.submit();
            }
            
        }
    });
});
