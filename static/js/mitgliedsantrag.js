var memberCost = 0;
var totalCost = 0;
var sportCostPassiv = 0;
var sportMultiplier = 0;

function kindOfSportChange(element) {
  if (element.checked) {
    sportMultiplier++;
  } else {
    sportMultiplier--;
  }
}

window.onload = (event) => {
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

document.addEventListener('change', function (event) {
    if (event.target && event.target.matches('input[type="date"]')) {
        checkAge();
    }
});


  function berechneKosten() {
    totalCost = 0;
    for (let i = 1; i <= 5; i++) {
      memberCost = 0;
      const memberContainerId = `personalDataField${i}`;

      const memberContainer = document.getElementById(memberContainerId);

      if (memberContainer) {

        const birthdate = memberContainer.querySelector(`input[type="date"]`).value;

        const InputData = new Date(birthdate);

        const currentDate = new Date();

        const differenceInMS = currentDate - InputData;

        // Convert difference in years
        var differenceYears = differenceInMS / (1000 * 60 * 60 * 24 * 365.25);
        if (!document.getElementById('family-membership').checked) {

          if (differenceYears >= 4 && differenceYears <= 6) {
            memberCost = 5.17;
          } else if (differenceYears >= 7 && differenceYears <= 13) {
            memberCost = 6.58;
          } else if (differenceYears >= 14 && differenceYears <= 18) {
            memberCost = 7.67;
          } else if (differenceYears >= 18) {
            memberCost = 10.83;
          }
          differenceYears = 0;
        } else {
          memberCost = 19.17;
        }

        // kind of sport
        if (document.getElementById('passivMember' + i).checked == true) {
          memberCost = 7.5;
          sportMultiplier = 1;
        }

      }

      totalCost += ((sportMultiplier * memberCost));

    }

    var totalCostYearly = totalCost*12;
    var totalCost = (totalCost*12) + 15;
    var processingFee = 15;

    document.getElementById('yearlyPrice').innerText = totalCostYearly.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '€';
    document.getElementById('processingFee').innerText = processingFee.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '€';
    document.getElementById('totalPrice').innerText = totalCost.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '€';
  }

  var inputs = document.querySelectorAll('input');
  inputs.forEach(function (input) {
    input.addEventListener('input', function () {
      setTimeout(berechneKosten, 500);
    });
  });

};