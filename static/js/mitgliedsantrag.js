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
    let totalCost = 0;
    const isFamilyMembership = document.getElementById('family-membership').checked;
    const processingFee = 15;

    for (let i = 1; i <= 5; i++) {
      let memberCost = calculateMemberCost(i, isFamilyMembership);
      totalCost += memberCost * sportMultiplier;
    }

    const totalCostYearly = totalCost * 12;
    const finalTotalCost = totalCostYearly + processingFee;

    updateCostDisplay(totalCostYearly, processingFee, finalTotalCost);
  }

  function calculateMemberCost(memberIndex, isFamilyMembership) {
    const birthdateElement = document.querySelector(`#personalDataField${memberIndex} input[type="date"]`);

    if (!birthdateElement) {
      return 0;
    }

    const birthdate = birthdateElement.value;
    const age = calculateAge(birthdate);

    if (document.getElementById('passivMember' + memberIndex) &&
        document.getElementById('passivMember' + memberIndex).checked) {
      return 7.5;
    }

    if (isFamilyMembership) {
      return 19.17;
    }

    return calculateActiveMemberCost(age);
  }


  function calculateActiveMemberCost(age) {
    if (age >= 4 && age <= 6) {
      return 5.17;
    } else if (age >= 7 && age <= 13) {
      return 6.58;
    } else if (age >= 14 && age <= 18) {
      return 7.67;
    } else if (age >= 18) {
      return 10.83;
    }
    return 0;
  }

  function calculateAge(birthdate) {
    const birthDate = new Date(birthdate);
    const currentDate = new Date();
    const age = currentDate.getFullYear() - birthDate.getFullYear();
    return age;
  }

  function updateCostDisplay(totalCostYearly, processingFee, totalCost) {
    document.getElementById('yearlyPrice').innerText = `${totalCostYearly.toFixed(2)}€`;
    document.getElementById('processingFee').innerText = `${processingFee.toFixed(2)}€`;
    document.getElementById('totalPrice').innerText = `${totalCost.toFixed(2)}€`;
  }


  var inputs = document.querySelectorAll('input');
  inputs.forEach(function (input) {
    input.addEventListener('input', function () {
      setTimeout(berechneKosten, 500);
    });
  });

};