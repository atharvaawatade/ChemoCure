function sendMessage() {
    var mrn = document.getElementById('user-input').value.trim();
    if (mrn !== '') {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/get_records', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var records = JSON.parse(xhr.responseText);
                    var messagesDiv = document.getElementById('messages');
                    messagesDiv.innerHTML = '<p>Patient Records:</p>';
                    for (var parameter in records) {
                        messagesDiv.innerHTML += `<p><strong>${parameter}</strong>: ${records[parameter].join(', ')}</p>`;
                    }
                } else {
                    console.error('Error:', xhr.responseText);
                    alert('Patient not found!');
                }
            }
        };
        xhr.send('mrn=' + mrn);
    } else {
        alert('Please enter a Medical Record Number!');
    }
}
