document.addEventListener('DOMContentLoaded', () => {
    // --- 1. DOM Element References ---
    const addForm = document.getElementById('add-reminder-form');
    const remindersList = document.getElementById('reminders-list');
    const emptyState = document.getElementById('empty-state');
    const editModal = document.getElementById('edit-modal');
    const editForm = document.getElementById('edit-form');

    // --- 2. State Management (Replace with your backend data) ---
    // This demo data will be replaced by your actual Django logic.
    let reminders = [
        { id: 1, title: 'Drink 2L of water', description: 'Throughout the day', time: '2024-09-10T12:00' },
        { id: 2, title: 'High-protein lunch', description: 'Chicken salad', time: '2024-09-10T13:00' },
        { id: 3, title: 'Evening yoga session', description: '45 minutes', time: '2024-09-10T19:00' }
    ];
    let nextId = 4;

    // --- 3. Core Functions ---
    const renderReminders = () => {
        remindersList.innerHTML = '';
        if (reminders.length === 0) {
            remindersList.appendChild(emptyState);
            emptyState.style.display = 'block';
            return;
        }

        const sortedReminders = [...reminders].sort((a, b) => new Date(a.time) - new Date(b.time));

        sortedReminders.forEach(reminder => {
            const li = createReminderElement(reminder);
            remindersList.appendChild(li);
        });
    };

    const createReminderElement = (reminder) => {
        const li = document.createElement('li');
        li.className = 'reminder-item';
        li.dataset.id = reminder.id;

        const date = new Date(reminder.time);
        const formattedTime = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

        let iconClass = 'fa-solid fa-bell icon-default';
        const titleLower = reminder.title.toLowerCase();
        if (titleLower.includes('pill') || titleLower.includes('vitamin')) iconClass = 'fa-solid fa-pills icon-pills';
        else if (titleLower.includes('water') || titleLower.includes('drink')) iconClass = 'fa-solid fa-glass-water icon-water';
        else if (titleLower.includes('workout') || titleLower.includes('gym') || titleLower.includes('run') || titleLower.includes('yoga')) iconClass = 'fa-solid fa-dumbbell icon-workout';

        li.innerHTML = `
            <div class="reminder-icon">
                <i class="${iconClass}"></i>
            </div>
            <div class="reminder-content">
                <h3>${reminder.title}</h3>
                <p>${reminder.description || ''}</p>
            </div>
            <div class="reminder-time">${formattedTime}</div>
            <div class="reminder-actions">
                <button class="btn-edit" title="Edit"><i class="fa-solid fa-pencil"></i></button>
                <button class="btn-delete" title="Delete"><i class="fa-solid fa-trash-can"></i></button>
            </div>
        `;
        return li;
    };

    const addReminder = (e) => {
        e.preventDefault();
        const newReminder = {
            id: nextId++,
            title: addForm.title.value.trim(),
            description: addForm.description.value.trim(),
            time: addForm.reminder_time.value
        };
        // TODO: In your real app, send this data to the backend via fetch/AJAX.
        reminders.push(newReminder);
        renderReminders();
        addForm.reset();
    };

    const handleListClick = (e) => {
        const editBtn = e.target.closest('.btn-edit');
        const deleteBtn = e.target.closest('.btn-delete');

        if (editBtn) {
            const id = parseInt(editBtn.closest('.reminder-item').dataset.id);
            openEditModal(id);
        } else if (deleteBtn) {
            const id = parseInt(deleteBtn.closest('.reminder-item').dataset.id);
            if (confirm('Are you sure you want to delete this reminder?')) {
                // TODO: In your real app, send a DELETE request to the backend.
                reminders = reminders.filter(r => r.id !== id);
                renderReminders();
            }
        }
    };

    const openEditModal = (id) => {
        const reminder = reminders.find(r => r.id === id);
        if (!reminder) return;

        editForm.querySelector('#edit-id').value = id;
        editForm.querySelector('#edit-title').value = reminder.title;
        editForm.querySelector('#edit-description').value = reminder.description;
        editForm.querySelector('#edit-time').value = reminder.time;

        editModal.classList.add('visible');
    };

    const closeEditModal = () => editModal.classList.remove('visible');

    const updateReminder = (e) => {
        e.preventDefault();
        const id = parseInt(editForm.querySelector('#edit-id').value);
        // TODO: In your real app, send the updated data to the backend.
        reminders = reminders.map(r => r.id === id ? {
            id,
            title: editForm.querySelector('#edit-title').value.trim(),
            description: editForm.querySelector('#edit-description').value.trim(),
            time: editForm.querySelector('#edit-time').value
        } : r);
        renderReminders();
        closeEditModal();
    };

    // --- 4. Event Listeners ---
    addForm.addEventListener('submit', addReminder);
    remindersList.addEventListener('click', handleListClick);
    editForm.addEventListener('submit', updateReminder);
    editModal.addEventListener('click', (e) => e.target === editModal && closeEditModal());
    document.addEventListener('keydown', (e) => e.key === 'Escape' && closeEditModal());

    // --- 5. Initial Render ---
    // TODO: In your real app, you would fetch the initial 'reminders' array from your backend here.
    renderReminders();
});