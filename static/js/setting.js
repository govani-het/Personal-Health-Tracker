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