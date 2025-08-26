document.addEventListener('DOMContentLoaded', () => {
    const otpForm = document.getElementById('otp-form');
    const otpInputs = document.querySelectorAll('.otp-input');

    otpInputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            if (input.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '') {
                if (index > 0) {
                    otpInputs[index - 1].focus();
                }
            } else if (e.key === 'ArrowLeft') {
                if (index > 0) {
                    otpInputs[index - 1].focus();
                }
            } else if (e.key === 'ArrowRight') {
                if (index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
            }
        });

        input.addEventListener('paste', (e) => {
            e.preventDefault();
            const pastedData = e.clipboardData.getData('text');
            if (!/^\d+$/.test(pastedData) || pastedData.length !== otpInputs.length) {
                return;
            }
            for (let i = 0; i < otpInputs.length; i++) {
                if (i < pastedData.length) {
                    otpInputs[i].value = pastedData[i];
                }
            }
            otpInputs[otpInputs.length - 1].focus();
        });
    });

    // --- Modal Logic ---
    const passwordModal = document.getElementById('password-modal');
    const closeModalBtn = passwordModal.querySelector('.close-btn');

    const showModal = () => passwordModal.classList.add('show');
    const hideModal = () => passwordModal.classList.remove('show');

    otpForm.addEventListener('submit', (e) => {
        e.preventDefault();
        checkOtp()
    });
     async function checkOtp(){
         const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const otp = document.getElementById('otp-full').value
        const response = await fetch(`user/api/check_otp/`,{
            method:'POST',
            headers : {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
            },
            body : JSON.stringify({
                otp : otp
            })
        })
        const message = document.getElementById('message')
        if (!response.ok){
            throw new Error('Invalid OTP')
        }
        const data = await response.json()

        if (data.success){
            showModal();
        }
        if (data.Error){
            window.location.href = data.redirect_url
            message.style.color = 'red'
            message.innerHTML = data.message
            otpForm.reset()
        }

    }
    closeModalBtn.addEventListener('click', hideModal);
    passwordModal.addEventListener('click', (e) => {
        if (e.target === passwordModal) hideModal();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && passwordModal.classList.contains('show')) hideModal();
    });

    const newPasswordForm = document.getElementById('new-password-form');
    newPasswordForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Password has been updated successfully!');
        hideModal();
        otpForm.reset();
        newPasswordForm.reset();
        otpInputs[0].focus();
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const otpContainer = document.getElementById('otp-container');
    const otpInputs = [...otpContainer.querySelectorAll('.otp-input')];
    const hiddenInput = document.getElementById('otp-full');

    const combineOtp = () => {
        let otp = '';
        otpInputs.forEach(input => {
            otp += input.value;
        });
        hiddenInput.value = otp;
    };

    otpInputs.forEach((input, index) => {
        // Event for typing/entering a value
        input.addEventListener('input', () => {
            // If a value is entered and it's not the last input, focus the next one
            if (input.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
            combineOtp();
        });

        // Event for handling backspace
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value.length === 0 && index > 0) {
                otpInputs[index - 1].focus();
            }
        });

        // Event for handling pasting the OTP
        input.addEventListener('paste', (e) => {
            e.preventDefault();
            const pastedData = e.clipboardData.getData('text');
            const otpArray = pastedData.split('').slice(0, otpInputs.length);

            otpArray.forEach((char, i) => {
                if (otpInputs[index + i]) {
                    otpInputs[index + i].value = char;
                }
            });

            // Focus the last filled input or the next empty one
            const nextFocusIndex = Math.min(index + otpArray.length, otpInputs.length - 1);
            otpInputs[nextFocusIndex].focus();
            combineOtp();
        });
    });
});


async function updatePassword(){
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const password = document.getElementById('new-password').value
    const confirmPassword = document.getElementById('confirm-password').value
    const message = document.getElementById('error-message')

    const specialCharRegex = /[!@#$%^&*(),.?":{}|<>]/;

    if (password !== confirmPassword){
        message.innerHTML = 'Passwords do not match!'
        message.style.color = 'red'
    }

    if (password.length < 8) {
        alert('Password must be at least 8 characters long.');
        return false;
    }

    if (!specialCharRegex.test(password)) {
        alert('Password must contain at least one special character (e.g., !, @, #, $).');
        return false;
    }

    if (password !== confirm_password) {
        alert('Your passwords do not match.');
        return false;
    }

    const response = await fetch('user/api/update_password/',{
        method:'POST',
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            password : password
        })
    })

    const data = await response.json()
    if (data.success){
        alert(data.message)
        window.location.href = '/'
    }

}