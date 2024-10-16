function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

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
function get(a,value){
    
    
    fetch(`http://127.0.0.1:8000/api/count_likes/${value}`, {
                    credentials: "same-origin",
                    method: 'GET',
                    headers: {
                        "Accept": "application/json",
                        'Content-Type': 'application/json',
                        "X-CSRFToken": getCookie("csrfToken"),
                        
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
            credentials: 'same-origin',
            method: 'POST',
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrfToken"),
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
            credentials: "include",
            method: 'GET',
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrfToken"),
                
            },
            })
            .then((response)=>{
                get(a,value[1]);
                
            })
            
            
            
        }
    });
})
