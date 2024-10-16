function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        console.log(cookies)
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.addEventListener('DOMContentLoaded', () => {
    var elements = document.querySelectorAll("#click");
    if (elements.length > 0) {
        elements.forEach((elem) => {
            var value = elem.getAttribute("value");

            if (value) {
                value = value.split(" ");
                id = value[1]
            
                fetch(`http://127.0.0.1:8000/api/retrieve/${id}`, {
                    credentials: "same-origin",
                    method: 'GET',
                    headers: {
                        "Accept": "application/json",
                        'Content-Type': 'application/json',
                        "X-CSRFToken": getCookie("csrfToken"),

                    },
                })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data) {
                        var classes = elem.classList;
                        classes.remove("fa-regular");
                        classes.add("fa-solid");
                        elem.style.color = "red";
                    }
                })
                .catch(()=>{

                })
            }
        });
    }
});