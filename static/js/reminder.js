document.addEventListener('DOMContentLoaded', function () {

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const reminderList = document.getElementById('reminders-list');
    const createForm = document.getElementById('add-reminder-form');
    const errorContainer = document.getElementById('error-container');

    function createReminderCard(reminder) {

        const displayDate = dayjs(reminder.datetime).format('MMMM D, YYYY, h:mm A');

        return `
            <li class="reminder-item" id="reminder-item-${reminder.id}" data-datetime="${reminder.datetime}">
                <input type="hidden" value="${reminder.id}" name="id">
                <div class="reminder-details">
                    <h3 id="title">${reminder.reminder_title}</h3>
                    <p id="description">${reminder.reminder_description}</p>
                </div>
                <span class="reminder-time" id="date">${displayDate}</span>
                <div class="reminder-action-buttons">
                    <button class="action-btn edit-btn" title="Edit Reminder">
                        <i class="fas fa-pencil-alt"></i>
                    </button>
                    <button class="action-btn delete-btn" onclick="deleteReminder(${reminder.id})" title="Delete Reminder">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </li>
        `;
    }

    async function fetchAndDisplayReminder() {
        errorContainer.innerHTML = " ";
        try {
            const response = await fetch(`api/get_reminder/`);
            if (!response.ok) {
                throw new Error('Could not fetch reminders from the server.');
            }
            const data = await response.json();
            reminderList.innerHTML = ' ';

            if (data.length === 0) {
                reminderList.innerHTML = '<p>You have no reminders set. Add one using the form!</p>';
            } else {
                data.forEach(reminder => {
                    const reminderHTML = createReminderCard(reminder);
                    reminderList.innerHTML += reminderHTML;
                });
            }
        } catch (error) {
            errorContainer.textContent = error.message;
        }
    }

    async function handleCreateFormSubmit(event) {
        const form = document.getElementById('add-reminder-form')
        event.preventDefault();
        errorContainer.innerHTML = " ";

        const formData = new FormData(createForm);
        const reminderId = formData.get('id');

        const localDateTimeValue = formData.get('datetime');


        const utcDateTimeString = dayjs(localDateTimeValue).toISOString();

        const data = {
            reminder_title: formData.get('reminder_title'),
            reminder_description: formData.get('reminder_description'),
            datetime: utcDateTimeString,
        };

        try {
            let response;
            if (reminderId) {

                response = await fetch(`api/update_reminder/${reminderId}`, {
                    method: 'PUT',
                    headers: {
                        'content-type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify(data)
                });
            } else {

                response = await fetch('api/reminder/', {
                    method: 'POST',
                    headers: {
                        'content-type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify(data)
                });
            }

            const responseData = await response.json();
            if (!response.ok) {
                const errorMessage = Object.values(responseData).flat().join(' ');
                throw new Error(errorMessage || 'An unknown error occurred.');
            }

            form.querySelector('button[type="submit"]').textContent = 'Add Reminder';
            await fetchAndDisplayReminder(); // Refresh the whole list
            createForm.reset();

        } catch (error) {
            errorContainer.textContent = error.message;
        }
    }


    async function editReminder(reminderItem) {
        const form = document.getElementById('add-reminder-form');

        // Get the original UTC string from the data attribute
        const utcDateTimeString = reminderItem.dataset.datetime;

        // Convert the UTC string to the local 'YYYY-MM-DDTHH:mm' format for the input
        const localDateTimeForInput = dayjs(utcDateTimeString).format('YYYY-MM-DDTHH:mm');

        // Get other data
        const id = reminderItem.querySelector('input[name="id"]').value;
        const title = reminderItem.querySelector('h3[id="title"]').textContent.trim();
        const description = reminderItem.querySelector('p[id="description"]').textContent.trim();

        // Populate the form
        form.reset();
        form.querySelector('input[name="id"]').value = id;
        form.querySelector('input[name="reminder_title"]').value = title;
        form.querySelector('input[name="reminder_description"]').value = description;
        form.querySelector('input[name="datetime"]').value = localDateTimeForInput; // Set the correct local time
        form.querySelector('button[type="submit"]').textContent = 'Update Reminder';

        // Scroll to the top so the user sees the form
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    reminderList.addEventListener('click', function (event) {
        const editBtn = event.target.closest('.edit-btn');
        if (!editBtn) {
            return;
        }
        const reminderItem = editBtn.closest('.reminder-item');
        editReminder(reminderItem);
    });

    createForm.addEventListener('submit', handleCreateFormSubmit);
    fetchAndDisplayReminder();
});

// Delete function remains the same, but ensure it works with the rest of the code
async function deleteReminder(reminderId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const errorContainer = document.getElementById('error-container');

    if (!confirm('Are you sure you want to delete this reminder?')) {
        return;
    }

    try {
        const response = await fetch(`api/delete_reminder/${reminderId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
            }
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Failed to delete.');
        }

        // Success: remove the item from the page
        const ReminderElement = document.getElementById(`reminder-item-${reminderId}`);
        if (ReminderElement) {
            ReminderElement.remove();
        }
        document.getElementById('add-reminder-form').reset();
        document.getElementById('add-reminder-form').querySelector('button[type="submit"]').textContent = 'Add Reminder';


    } catch (error) {
        errorContainer.textContent = error.message;
        errorContainer.style.color = 'red';
    }
}