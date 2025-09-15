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
    const modal = document.getElementById('add-exercise-modal');
    const openBtn = document.getElementById('add-exercise-btn');
    const closeBtn = document.getElementById('close-modal-btn');

    function openModal() { if (modal) modal.classList.add('visible'); }
    function closeModal() { if (modal) modal.classList.remove('visible'); }

    if (openBtn) openBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (modal) modal.addEventListener('click', (event) => { if (event.target === modal) closeModal(); });

    // --- DYNAMIC FORM LOGIC ---
    const exerciseTypeSelect = document.getElementById('exercise-type');
    const cardioFields = document.getElementById('cardio-fields');
    const weightLiftingFields = document.getElementById('weight-lifting-fields');

    if (exerciseTypeSelect) {
        exerciseTypeSelect.addEventListener('change', function() {
            const selectedType = this.value;

            // Hide all dynamic sections first
            cardioFields.style.display = 'none';
            weightLiftingFields.style.display = 'none';

            // Show the relevant section
            if (selectedType === 'Cardio') {
                cardioFields.style.display = 'block';
            } else if (selectedType === 'Weight Lifting') {
                weightLiftingFields.style.display = 'block';
            }
        });
    }
});


async function update_data() {

    const date = document.getElementById('current-date').value
    const exercise_log = document.querySelector('.exercise-log')

    const duration = document.getElementById('duration')
    const kcal_burn = document.getElementById('kcal_burn')

    const today = new Date().toISOString().split("T")[0];

    if (date !== today){
        document.getElementById('add-exercise').style.display = 'none';
    }else {
        document.getElementById('add-exercise').style.display = 'block';
    }

    exercise_log.innerHTML='';

    const response = await fetch(`/exercise/api/get_data_based_on_date/?date=${date}`)

    if (!response.ok){
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data =await response.json()
    console.log(data)

    duration.textContent = (data.header.cardio_details__duration_minutes__sum ?? 0) + " Min"
    kcal_burn.textContent = (data.header.kcal__sum ?? 0)


    data.workout.forEach(workout => {
        if (workout.exercise_type === 'Cardio'){
            const cardioHTML = `    
            <div class="card exercise-entry">
                <div><h3>${workout.exercise_name}</h3>
                    <p>${workout.exercise_type} |  ${workout.intensity}</p>
                </div>
                <div class="entry-stats">
                    <span>${workout.cardio_details__duration_minutes} Min</span>
                    <span>${workout.cardio_details__distance_km} KM</span>
                    <span>${workout.kcal} kcal</span>
                </div>
                
                <div class="item-actions">                                 
                    <a class="icon-btn" title="Delete"
                       href="${deleteWorkoutUrl}?exercise_id=${workout.id}">
                        <svg viewBox="0 0 24 24" width="20" height="20">
                            <path fill="currentColor"
                                  d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"></path>
                        </svg>
                    </a>
                </div>                                
            </div>
        `;
            exercise_log.innerHTML += cardioHTML;
        }

        if (workout.exercise_type === 'Weight Lifting'){

            const weight_liftingHTML = `
            <div class="card exercise-entry">
                <div><h3>${workout.exercise_name}</h3>
                    <p>${workout.exercise_type} | ${workout.intensity}</p>
                </div>
                <div class="entry-stats">
                    <span>${workout.weight_lifting_details__weight_kg} kg</span>
                    <span>${workout.weight_lifting_details__sets} sets</span>
                    <span>${workout.weight_lifting_details__reps} reps</span>
                </div>
                <div class="item-actions">                                 
                    <a class="icon-btn" title="Delete"
                       href="${deleteWorkoutUrl}?exercise_id=${workout.id}">
                        <svg viewBox="0 0 24 24" width="20" height="20">
                            <path fill="currentColor"
                                  d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"></path>
                        </svg>
                    </a>
                </div>   
            </div>
        `;
            exercise_log.innerHTML += weight_liftingHTML;

        }
    })
}
