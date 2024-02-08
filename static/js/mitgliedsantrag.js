window.onload = (event) => {
  document.addEventListener('change', function (event) {
      if (event.target && event.target.matches('input[type="date"]')) {
          checkAge();
      }
  });

  document.addEventListener('input', function() {
    setTimeout(berechneKosten, 500);
  });

  document.querySelectorAll('#addFieldButton, #removeFieldButton').forEach(button => {
    button.addEventListener('click', function() {
      berechneKosten();
    });
  })
}; 

function checkAge() {
  var parentSignature = document.getElementById('parentSignature');
  var shouldShowParentSignature = false;
  var birthdateFields = document.querySelectorAll('input[type="date"]');

  for (var i = 0; i < birthdateFields.length; i++) {
      var birthdate = new Date(birthdateFields[i].value);
      var currentDate = new Date();
      var age = currentDate.getFullYear() - birthdate.getFullYear();
      if (age < 18) {
          shouldShowParentSignature = true;
          break;
      }
  }

  if (shouldShowParentSignature) {
      parentSignature.classList.remove('hidden-opacity');
  } else {
      parentSignature.classList.add('hidden-opacity');
  }
}

function berechneKosten() {
  var totalCost = 0;
  var totalCostYearly = 0;
  var processingFee = 0;
  
  if (document.querySelector('input[name="membership-type"]:checked').value === 'new-membership')
  {
    for (let i = 1; i <= 5; i++) {
      const memberContainerId = `personalDataField${i}`;
      const memberContainer = document.getElementById(memberContainerId);

      if (memberContainer) {
      
        var selectedSports = document.querySelectorAll(`#Member${i} input[type="checkbox"]:checked`).length;
        var isPassiveMember = document.getElementById('passivMember' + i).checked;

        
        if (selectedSports > 1 || (selectedSports > 0 && !isPassiveMember)) {
          const birthdate = memberContainer.querySelector(`input[type="date"]`).value;
          const InputData = new Date(birthdate);
          const currentDate = new Date();
          const differenceInMS = currentDate - InputData;

        
          var differenceYears = differenceInMS / (1000 * 60 * 60 * 24 * 365.25);
          if (differenceYears >= 4 && differenceYears <= 6) {
            totalCostYearly += 62;
          } else if (differenceYears >= 7 && differenceYears <= 13) {
            totalCostYearly += 79;
          } else if (differenceYears >= 14 && differenceYears <= 18) {
            totalCostYearly += 92;
          } else if (differenceYears >= 18) {
            totalCostYearly += 130;
          }
        }

        if (document.getElementById('passivMember' + i).checked == true) {
          totalCostYearly += 90;
        }

        processingFee += 15;
      }
    }      
  } else if (document.querySelector('input[name="membership-type"]:checked').value === 'family-membership') {
    
    totalCostYearly = 230;
    
    processingFee = document.querySelectorAll('.PD-Container .flexPersonalDataField').length * 15;
  }

  totalCost = totalCostYearly + processingFee;

  document.getElementById('yearlyPrice').innerText = totalCostYearly.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '€';
  document.getElementById('processingFee').innerText = processingFee.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '€';
  document.getElementById('totalPrice').innerText = totalCost.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '€';
}