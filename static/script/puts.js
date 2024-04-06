function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();;
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function get(a,value){
    fetch(`http://127.0.0.1:8000/api/count_likes/${value}`, {
                    credentials: "same-origin",
                    method: 'GET',
                    headers: {
                        "Accept": "application/json",
                        'Content-Type': 'application/json',
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                })
                .then((response) => {
                    return response.json()
                })
                .then((data)=>{
                    a.nextElementSibling.textContent = data['count']
                })
}
const elements = document.querySelectorAll("#click")
elements.forEach((a)=>{
    a.addEventListener("click", (e) => {
        var classes = e.target.classList;
        var value = e.target.getAttribute("value");        
        var value = value.split(" ");
        if (classes.contains("fa-regular")) {
            classes.remove("fa-regular");
            classes.add("fa-solid");
            a.style.color = "red";
            fetch('http://127.0.0.1:8000/api/create/', {
            credentials: "same-origin",
            method: 'POST',
            headers: {
                /*"Authorization": 'Bearer ' + token,*/
                "Accept": "application/json",
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({"profile":value[0],"post":value[1],"liked":"True"})
            })
            .then((response)=>{
                get(a,value[1])
                
            })
            
            
        
        } else if (classes.contains("fa-solid")) {
            var id = value[1];
            classes.remove("fa-solid");
            classes.add("fa-regular");
            a.style.color = "black";
            fetch(`http://127.0.0.1:8000/api/delete/${id}`, {
            credentials: "same-origin",
            method: 'GET',
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken"),
            },
            })
            .then((response)=>{
                get(a,value[1]);
                
            })
            
            
            
        }
    });
})
