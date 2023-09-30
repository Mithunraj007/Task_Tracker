document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const taskInput = document.getElementById('task-input');
    const deadlineInput = document.getElementById('deadline-input');
    const priorityInput = document.getElementById('priority-input');
    const taskList = document.getElementById('tasks');

    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const taskText = taskInput.value.trim();
        const taskDeadline = deadlineInput.value;
        const taskPriority = priorityInput.value;

        if (taskText !== '') {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>Task:</strong> ${taskText}, <strong>Deadline:</strong> ${taskDeadline}, <strong>Priority:</strong> ${taskPriority}`;
            taskList.appendChild(listItem);

            // Clear form inputs
            taskInput.value = '';
            deadlineInput.value = '';
            priorityInput.value = '';

            // send data to flask backend '/add_task' url
            fetch('/add_task', {
                method: 'POST',
                // Converts a javascript object into a 'json' string
                body: JSON.stringify({ text: taskText, deadline: taskDeadline, priority: taskPriority }),
                // header indicates that the content of the request body is in JSON format
                headers: {
                    'Content-Type': 'application/json',
                },
            });
        }
    });
});
