document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('pendingOnderzoekenModal');
    const pendingButton = document.getElementById('pendingOnderzoekenBtn');
    var span = modal.querySelector('.close');
    const pendingList = document.getElementById('pendingOnderzoekenList');

    if (pendingButton && pendingList) {
        pendingButton.addEventListener('click', function() {
            console.log('Pending button clicked');
            fetch('/api/pending_onderzoeken')
                .then(response => response.json())
                .then(data => {
                    console.log('Data fetched:', data);
                    pendingList.innerHTML = ''; 
                    if (data.length === 0) {
                        pendingList.innerHTML = '<p>No pending onderzoeken found.</p>';
                    } else {
                        data.forEach(onderzoek => {
                            const listItem = document.createElement('li');
                            listItem.textContent = onderzoek.titel;
                            pendingList.appendChild(listItem);
                        });
                    }
                    modal.style.display = 'block'; // Show the modal
                })
                .catch(error => {
                    console.error('Error fetching pending onderzoeken:', error);
                    pendingList.innerHTML = '<p>Error loading pending onderzoeken.</p>';
                });
        });
    }

    span.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});
