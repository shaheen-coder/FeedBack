document.addEventListener('DOMContentLoaded', function() {
    const yearInput = document.getElementById('id_semester');
    const course = document.getElementById('id_course_type');
    console.log("course tyoe : " + course.value);
    const subjectSelect = document.getElementById('id_subject');
    
    yearInput.addEventListener('change', function() {
        const year = this.value;
        const course = document.getElementById('id_course_type').value;
        subjectSelect.innerHTML = ''; 
        
        if (year) {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/classstaff/subjects/${year}/${course}/`, {
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
                    option.textContent = item.subject_code + " " + item.name;
                    subjectSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching subjects:', error));
        }
    });
    course.addEventListener('change', function() {
        const course = Number(this.value);
        subjectSelect.innerHTML = ''; 
        console.log("in event listener");     
        if (year) {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/classstaff/subjects/${year}/${course}/`, {
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
                    option.textContent = item.subject_code + " " + item.name;
                    subjectSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching subjects:', error));
        }
    });
});