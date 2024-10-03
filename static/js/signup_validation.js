document.addEventListener('DOMContentLoaded', function () {
    // Validate first name field
    document.getElementById('id_first_name').addEventListener('blur', function () {
        const firstName = this.value.trim();
        const errorField = document.getElementById('firstNameError');
        if (firstName === '') {
            errorField.textContent = 'First name is required.';
        } else {
            errorField.textContent = '';
        }
    });

    // Validate last name field
    document.getElementById('id_last_name').addEventListener('blur', function () {
        const lastName = this.value.trim();
        const errorField = document.getElementById('lastNameError');
        if (lastName === '') {
            errorField.textContent = 'Last name is required.';
        } else {
            errorField.textContent = '';
        }
    });

    // Validate email field
    document.getElementById('id_email').addEventListener('blur', function () {
        const email = this.value.trim();
        const errorField = document.getElementById('emailError');
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            errorField.textContent = 'Please enter a valid email address.';
        } else {
            errorField.textContent = '';
        }
    });

    // Validate phone number field
    document.getElementById('id_phone_number').addEventListener('blur', function () {
        const phoneNumber = this.value.trim();
        const errorField = document.getElementById('phoneNumberError');
        const phonePattern = /^\+?1?\d{9,15}$/;  // Use regex to match the phone number pattern
        if (!phonePattern.test(phoneNumber)) {
            errorField.textContent = 'Please enter a valid phone number.';
        } else {
            errorField.textContent = '';
        }
    });

    // Validate password1 field
    document.getElementById('id_password1').addEventListener('blur', function () {
        const password = this.value;
        const errorField = document.getElementById('password1Error');
        if (password.length < 8) {
            errorField.textContent = 'Password must be at least 8 characters.';
        } else {
            errorField.textContent = '';
        }
    });

    // Validate password2 field
    document.getElementById('id_password2').addEventListener('blur', function () {
        const password1 = document.getElementById('id_password1').value;
        const password2 = this.value;
        const errorField = document.getElementById('password2Error');
        if (password1 !== password2) {
            errorField.textContent = 'Passwords do not match.';
        } else {
            errorField.textContent = '';
        }
    });
});
