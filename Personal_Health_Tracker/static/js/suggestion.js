document.addEventListener("DOMContentLoaded", function() {
    // Get the elements
    const mealBtn = document.getElementById('meal-btn');
    const exerciseBtn = document.getElementById('exercise-btn');
    const mealsContent = document.getElementById('meals-content');
    const exercisesContent = document.getElementById('exercises-content');
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const contentSections = document.querySelectorAll('.content-section');

    // Function to update the view
    function updateView(activeButton, activeContent) {
        // Update button active state
        toggleButtons.forEach(btn => btn.classList.remove('active'));
        activeButton.classList.add('active');

        // Update content visibility
        contentSections.forEach(section => section.classList.remove('visible'));
        activeContent.classList.add('visible');
    }

    // Event Listeners
    if (mealBtn) {
        mealBtn.addEventListener('click', () => {
            updateView(mealBtn, mealsContent);
        });
    }

    if (exerciseBtn) {
        exerciseBtn.addEventListener('click', () => {
            updateView(exerciseBtn, exercisesContent);
        });
    }

    // Set the default view on page load
    if (mealBtn && mealsContent) {
        updateView(mealBtn, mealsContent);
    }
});