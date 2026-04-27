document.addEventListener('DOMContentLoaded', function() {

    const csrftoken = getCookie('csrftoken');
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    };

    check_if_archive_data();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function get_headers(){
    let csrftoken = getCookie('csrftoken');
    return headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    };
}

function delete_archive_element(id) {
    fetch('/delete_archive_element/'+ id, {
        method: 'POST',
        headers: get_headers(),
        body: JSON.stringify({
            id: id
        })
    })
    .then(res => res.json())
    .then(res => {
        if (res.success) {
            window.location.reload();
        }
        alert('Error has occured, please contact ksenijasamardzic4@gmail.com')
    });
}

function check_if_archive_data() {
    fetch('/check_if_archive_data', {
        method: 'GET',
        headers: get_headers()
    })
    .then(res => res.json())
    .then(res => {
        if (res.has_data) {
            document.getElementById('archive_data').style.display = 'block';
        } else {
            document.getElementById('archive_data').style.display = 'none';
        }
    });
}

function download_pdf_from_archive(id) {
    fetch('/download_pdf_from_archive/' + id, {
        method: 'POST',
        headers: get_headers(),
        body: JSON.stringify({
            id: id
        })
    })
    .then(res => res.json())
    .then(res => {
        if (res.message == 'Success') {
            alert('Success! File will open in default preview!')
        }
    });
}