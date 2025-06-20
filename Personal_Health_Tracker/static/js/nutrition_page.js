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