document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('addOrgPopup');
    var btn = document.getElementById('addOrgBtn');
    var span = document.getElementsByClassName('close')[0];
    var form = document.getElementById('addOrgForm');

    btn.onclick = function() {
        modal.style.display = 'block';
    }

    span.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    form.onsubmit = function(e) {
        e.preventDefault();
        var formData = new FormData(form);
        fetch('/admin/add_organisation', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Organisation added successfully!');
                modal.style.display = 'none';
                location.reload(); // Reload the page to show the new organisation
            } else {
                alert('Error adding organisation: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the organisation.');
        });
    }
});