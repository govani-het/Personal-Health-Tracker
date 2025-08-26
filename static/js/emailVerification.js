async function verifyEmail(){
    const email = document.getElementById('email').value
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const error = document.getElementById('error')

    const response = await fetch('/user/api/verify_email/',{
        method : 'POST',
        headers : {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body : JSON.stringify({
            email : email
        })
    })

    const data = await response.json()
    if (data.Error){

    }
    if (response.ok){
        window.location.href = data.redirect_url

    }else{
        error.style.color = 'red'
        error.innerHTML = data.message
    }
}