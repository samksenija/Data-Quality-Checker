document.addEventListener('DOMContentLoaded', function() {

    const csrftoken = getCookie('csrftoken');
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    };

})