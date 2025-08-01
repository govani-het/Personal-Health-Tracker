document.addEventListener("DOMContentLoaded", function() {
    // --- Date Picker Logic ---
    const dateInput = document.getElementById('current-date');
    if (dateInput) {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${year}-${month}-${day}`;
    }

    // --- Modal Logic ---
    const modal = document.getElementById('add-meal-modal');
    const openBtn = document.getElementById('add-meal-btn');
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

async function update_data(){
    const date = document.getElementById('current-date').value
    const mealLog = document.querySelector('.meal-log')
    const daily_summery = document.querySelector('.daily-summary')

    mealLog.innerHTML='';


     const summary = {
        calories: {
            progress: document.getElementById('summary-calories-progress'),
            value: document.getElementById('summary-calories-value'),
            goal: 2000
        },
        protein: {
            progress: document.getElementById('summary-protein-progress'),
            value: document.getElementById('summary-protein-value'),
            goal: 150
        },
        carbs: {
            progress: document.getElementById('summary-carbs-progress'),
            value: document.getElementById('summary-carbs-value'),
            goal: 250
        },
        fats: {
            progress: document.getElementById('summary-fats-progress'),
            value: document.getElementById('summary-fats-value'),
            goal: 70
        }
    };

    const response = await fetch(`/nutrition/api/get_data_based_on_date/?date=${date}`)

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data =await response.json()

    console.log("Data received from backend:", data);

    summary.calories.value.textContent = `${data.summary[0].toFixed(2)} /2000`;
    summary.calories.progress.style.setProperty('--p', data.percentages[0]);

    summary.protein.value.textContent = `${data.summary[1].toFixed(2)}/150`;
    summary.protein.progress.style.setProperty('--p', data.percentages[1]);

    summary.carbs.value.textContent = `${data.summary[2].toFixed(2)}/250`;
    summary.carbs.progress.style.setProperty('--p', data.percentages[2]);

    summary.fats.value.textContent = `${data.summary[3].toFixed(2)}/70`;
    summary.fats.progress.style.setProperty('--p', data.percentages[3]);

    data.meals.forEach(meal => {
        const mealLogHTML = `
            <div class="card meal-group">
                <h4>${meal.meal_type}</h4>
        
                <div class="meal-item">
                    <div>
                        <h5>${meal.food_name}</h5>
                        <p>${meal.food_quantity} | ${meal.kcal} kcal</p>
                    </div>
                    <div class="meal-macros">
                        <span title="Protein">P: ${meal.protein || 0}g</span>
                        <span title="Carbs">C: ${meal.carbs || 0}g</span>
                        <span title="Fats">F: ${meal.fats || 0}g</span>
                    </div>
                    <div class="item-actions">
                    
                    </div>
                </div>
            </div>
        `;
        mealLog.innerHTML += mealLogHTML;
    });

}

