document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById('password-modal');
    const openBtn = document.getElementById('open-password-modal-btn');
    const closeBtn = document.getElementById('close-modal-btn');

    function openModal() {
        if (modal) modal.classList.add('visible');
    }

    function closeModal() {
        if (modal) modal.classList.remove('visible');
    }

    if (openBtn) openBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);

    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) closeModal();
        });
    }
});

async function update_profile_data(){
    const messageBox = document.getElementById('message-box');

    messageBox.textContent = '';

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const form = document.getElementById("profileForm");
    const formData = {
        username: document.getElementById("profileName").value,
        height: document.getElementById("height").value,
        weight: document.getElementById("current-weight").value,
        goal: document.getElementById("goal-weight").value,
        dob: document.getElementById("dob").value,
        gender: form.querySelector('input[name="gender"]:checked')?.value,
        activityLevel: document.getElementById("activity-level").value,
    };


    const response = await fetch('user/api/update_profile_data/',{
        method:"POST",
        headers : {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(formData)
    })

    const data = await response.json()
    console.log(data)
    if (data.success){
        messageBox.style.display = 'block'
        messageBox.textContent = data.message
        messageBox.className = 'message-box message-success'
    }else{
        messageBox.style.display = 'block'
        messageBox.textContent = data.message
        messageBox.className = 'message-box message-error'

    }

}


async function update_password(){
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const password = document.getElementById('current-password').value
    const newPassword = document.getElementById('new-password').value
    const confirmPassword = document.getElementById('confirm-password').value
    const formModel = document.getElementById('password-change')

    const message = document.getElementById('message')

    const specialCharRegex = /[!@#$%^&*(),.?":{}|<>]/;

    if (newPassword.length < 8) {
        alert('Password must be at least 8 characters long.');
        return false;
    }

    if (!specialCharRegex.test(newPassword)) {
        alert('Password must contain at least one special character (e.g., !, @, #, $).');
        return false;
    }

    if (newPassword !== confirmPassword) {
        alert('Your passwords do not match.');
        return false;
    }

    const response = await fetch('user/api/change_password/',{
        method : 'POST',
        headers : {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body : JSON.stringify({
            password : password,
            newPassword : newPassword
        })
    })

    const data = await response.json()
    console.log(data)
    if (data.success){

        message.textContent =  data.message
        message.style.color = 'green'
        formModel.reset()
        setTimeout(() =>{
            document.getElementById('password-modal').style.display = 'none';
        },2000)
    }
    else{
        message.textContent =  data.message
        message.style.color = 'red'
        formModel.reset()
    }
}