document.addEventListener('DOMContentLoaded', function() {
    const applicationsBtn = document.getElementById('applicationsBtn');
    const applicationsModal = document.getElementById('applicationsModal');
    const applicationsList = document.getElementById('applicationsList');
    const closeModal = applicationsModal.querySelector('.close');

    applicationsBtn.onclick = function() {
        fetch('/api/applications')
            .then(response => response.json())
            .then(data => {
                applicationsList.innerHTML = '';
                data.forEach(application => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${application.ervaringsdeskundige} applied for ${application.onderzoek}`;

                    // Create Approve button
                    const approveBtn = document.createElement('button');
                    approveBtn.textContent = 'Approve';
                    approveBtn.onclick = function() {
                        fetch(`/approve_application/${application.onderzoek_id}/${application.ervaringsdeskundige_id}`, {
                            method: 'POST'
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert('Application approved successfully.');
                                listItem.remove(); // Remove the item from the list
                                notifyErvaringsdeskundige(application.ervaringsdeskundige_id, 'approved');
                            } else {
                                alert('Error approving application: ' + data.message);
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('An error occurred while approving the application.');
                        });
                    };

                    // Create Disapprove button
                    const disapproveBtn = document.createElement('button');
                    disapproveBtn.textContent = 'Disapprove';
                    disapproveBtn.onclick = function() {
                        fetch(`/disapprove_application/${application.onderzoek_id}/${application.ervaringsdeskundige_id}`, {
                            method: 'POST'
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert('Application disapproved successfully.');
                                notifyErvaringsdeskundige(application.ervaringsdeskundige_id, 'disapproved');
                            } else {
                                alert('Error disapproving application: ' + data.message);
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('An error occurred while disapproving the application.');
                        });
                    };

                    // Append buttons to the list item
                    listItem.appendChild(approveBtn);
                    listItem.appendChild(disapproveBtn);
                    applicationsList.appendChild(listItem);
                });
                applicationsModal.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching applications:', error);
            });
    };

    closeModal.onclick = function() {
        applicationsModal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == applicationsModal) {
            applicationsModal.style.display = 'none';
        }
    };

    function notifyErvaringsdeskundige(ervaringsdeskundigeId, status) {
        // Implement notification logic here, e.g., send an email or update a notification system
        console.log(`Notify ervaringsdeskundige ${ervaringsdeskundigeId} that their application was ${status}.`);
    }
});


