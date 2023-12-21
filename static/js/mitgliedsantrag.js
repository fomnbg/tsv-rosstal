document.addEventListener('DOMContentLoaded', function() {
    function validateEmail(email) {
        var regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return regex.test(email);
    }

    function validateAndDisplayFeedback(emailInputId, feedbackId) {
        var emailInput = document.getElementById(emailInputId);
        var emailFeedback = document.getElementById(feedbackId);

        emailInput.addEventListener('blur', function() {
            if (!validateEmail(emailInput.value)) {
                emailFeedback.style.display = 'inline';
                emailFeedback.textContent = 'Bitte geben Sie eine gültige E-Mail-Adresse ein.';
            } else {
                emailFeedback.style.display = 'none';
                emailFeedback.textContent = '';
            }
        });
    }

    validateAndDisplayFeedback('emailInput1', 'emailFeedback1');
    validateAndDisplayFeedback('emailInput2', 'emailFeedback2');
    validateAndDisplayFeedback('emailInput3', 'emailFeedback3');
});
