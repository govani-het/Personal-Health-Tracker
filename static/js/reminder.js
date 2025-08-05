document.addEventListener('DOMContentLoaded',function () {


    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const reminderList = document.getElementById('reminders-list');
    const createForm = document.getElementById('add-reminder-form')
    const errorContainer = document.getElementById('error-container')



    function createReminderCard(reminder) {
        const reminderDate = new Date(reminder.datetime);
        return `         
                <li class="reminder-item" id="reminder-item-${reminder.id}" data-id="reminder-1">
                    <input type="hidden" value="${reminder.id}" name="id">
                    <div class="reminder-details">
                        <h3 id="title">${reminder.reminder_title}</h3>
                        <p id="description">${reminder.reminder_description}</p>
                    </div>
                    <span class="reminder-time" id="date">${reminderDate.toLocaleString()}</span>
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

    async function fetchAndDisplayReminder(event){

        errorContainer.innerHTML=" ";

        try {
            const response = await fetch(`api/get_reminder/`)

            if (!response.ok) {
                throw new Error('Could not fetch reminders from the server.');
            }

            const data = await response.json()
            reminderList.innerHTML = ' ';

            if (data.length === 0){
                reminderList.innerHTML = '<p>You have no reminders set. Add one using the form!</p>';
            }else{
                data.forEach(data => {
                    const dataHTML = createReminderCard(data);
                    reminderList.innerHTML += dataHTML
                })
            }
        }
        catch (error){
            errorContainer.textContent = error.message;
        }
    }


    async function handleCreateFormSubmit(event){
        event.preventDefault()
        errorContainer.innerHTML=" ";

        const formData = new FormData(createForm)

        const reminderId = document.getElementById('id').value


        const data = {
            reminder_title: formData.get('reminder_title'),
            reminder_description: formData.get('reminder_description'),
            datetime: formData.get('datetime'),
        };


        try {
            if (reminderId){
                const response = await fetch(`api/update_reminder/${reminderId}`,{
                    method : 'PUT',
                    headers: {
                        'content-type' : 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify(data)
                });

                const newReminder = await response.json();
                    if (!response.ok) {
                        const errorMessage = Object.values(newReminder).flat().join(' ');
                        throw new Error(errorMessage || 'An unknown error occurred.');
                    }

                fetchAndDisplayReminder();
                createForm.reset();

            }else{
                const response = await fetch('api/reminder/',{
                    method : 'POST',
                    headers: {
                        'content-type' : 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify(data)
                });
                const newReminder = await response.json();
                console.log(newReminder)
                    if (!response.ok) {
                        const errorMessage = Object.values(newReminder).flat().join(' ');
                        throw new Error(errorMessage || 'An unknown error occurred.');
                    }

                const newCardHTML = createReminderCard(newReminder)
                reminderList.innerHTML += newCardHTML

                createForm.reset();
            }
        }
        catch (error) {
            errorContainer.textContent = error.message;
        }
    }
    async function editReminder(reminderItem){
        const form = document.getElementById('add-reminder-form')

        const id = reminderItem.querySelector('input[name="id"]').value
        const title = reminderItem.querySelector('h3[id="title"]').textContent.trim();
        const description = reminderItem.querySelector('p[id="description"]').textContent.trim();
        const date = reminderItem.querySelector('span[id="date"]').textContent.trim();

        const formatedDate = new Date(date).toISOString().slice(0,16)

        form.reset()

        form.querySelector('input[name="id"]').value = id;
        form.querySelector('input[name="reminder_title"]').value = title;
        form.querySelector('input[name="reminder_description"]').value = description;
        form.querySelector('input[name="datetime"]').value = formatedDate;
        form.querySelector('button[type="submit"]').textContent = 'Update Data'


    }

    reminderList.addEventListener('click', function (event){
        const editBtn = event.target.closest('.edit-btn');

        if (!editBtn){
            return;
        }

        const reminderItem = editBtn.closest('.reminder-item');


        editReminder(reminderItem)

    })

    createForm.addEventListener('submit', handleCreateFormSubmit);
    fetchAndDisplayReminder();

});

async function deleteReminder(reminderId){
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const errorContainer = document.getElementById('error-container')

        if (!confirm('Are you sure you want to delete this reminder?')) {
            return;
        }

        try {
            const response = await fetch(`api/delete_reminder/${reminderId}`,{
                method : 'DELETE',
                headers :{
                    'X-CSRFToken': csrfToken,
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete the reminder.');
            }

            const ReminderElement = document.getElementById(`reminder-item-${reminderId}`)
            if (ReminderElement){
                ReminderElement.remove();
            }
        }catch (error){
            errorContainer.textContent = error.message;
        }
}