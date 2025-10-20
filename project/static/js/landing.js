document.addEventListener('DOMContentLoaded', ()=> {
    const form = document.getElementById('foodForm');
    const nameInput = document.getElementById('fullName');
    const dateInput = document.getElementById('foodChoiceDateTime');
    const fileInput = document.getElementById('inviteUpload');
    const checkboxes = document.querySelectorAll('input[name="food"]');
    const maxAllowed = 1;
    const flashContainer = document.querySelector('#flash-messages .container');

    function CheckboxMax3() {
        const checkedCount = document.querySelectorAll('input[name="food"]:checked').length;
        checkboxes.forEach(function(checkbox) {
            if (!checkbox.checked) {
                checkbox.disabled = checkedCount >= maxAllowed; // if count greater than max
            }
        });
    }
    // add the func to each checkbox
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', CheckboxMax3);
    });
    //CheckboxMax3();

    // called on each form validation element
    function addFlashMessage(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} mt-3`;
        alertDiv.textContent = message;
        flashContainer.appendChild(alertDiv);
    }

    // validate form
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let valid = true;

        // Clear existing msgs
        flashContainer.innerHTML = '';

        // Name
        if (!nameInput.value.trim()) {
            valid = false;
            addFlashMessage('Please enter your name.', 'danger');
        }
        // Date/Time
        if (!dateInput.value.trim()) {
            valid = false;
            addFlashMessage('Please select a date and time.', 'danger');
        }
        // Checkboxes
        const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
        if (!anyChecked) {
            valid = false;
            addFlashMessage('Please select at least one food option.', 'danger');
        }
        // File
        if (fileInput.files.length === 0) {
            valid = false;
            addFlashMessage('Please upload a file.', 'danger');
        }
        // If all data present, submit
        if (valid) {
            form.submit();
        }
    });
});