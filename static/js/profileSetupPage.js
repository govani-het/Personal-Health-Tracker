
document.getElementById("profileForm").addEventListener("submit", function(event) {
    const username = document.getElementById("username").value.trim();
    const height = parseFloat(document.getElementById("height").value);
    const weight = parseFloat(document.getElementById("current-weight").value);
    const goal = parseFloat(document.getElementById("goal-weight").value);
    const dob = document.getElementById("dob").value;


    if (!username) {
        alert("Username cannot be empty.");
        event.preventDefault();
        return;
    }

    if (isNaN(height) || height < 100 || height > 250) {
        alert("Please enter a valid height between 100 cm and 250 cm.");
        event.preventDefault();
        return;
    }


    if (isNaN(weight) || weight < 30 || weight > 250) {
        alert("Please enter a valid weight between 30 kg and 250 kg.");
        event.preventDefault();
        return;
    }

    if (isNaN(goal) || goal < 30 || goal > 250) {
        alert("Please enter a valid goal weight between 30 kg and 250 kg.");
        event.preventDefault();
        return;
    }


    if (Math.abs(goal - weight) > 50) {
        alert("Goal weight should not differ more than 50 kg from your current weight.");
        event.preventDefault();
        return;
    }


    if (!dob) {
        alert("Please enter your Date of Birth.");
        event.preventDefault();
        return;
    }

    const today = new Date();
    const birthDate = new Date(dob);
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }

    if (age < 15 || age > 70) {
        alert("Age must be between 15 and 70 years.");
        event.preventDefault();
        return;
    }
});

