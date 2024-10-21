document.addEventListener('DOMContentLoaded', function() {
    const yearInput = document.getElementById('id_semester');
    const subjectSelect = document.getElementById('id_subject');

    yearInput.addEventListener('change', function() {
        const year = this.value;
        subjectSelect.innerHTML = ''; 
        
        if (year) {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/classstaff/subjects/${year}/`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                data.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item.id;
                    option.textContent = item.name;
                    subjectSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching subjects:', error));
        }
    });
});