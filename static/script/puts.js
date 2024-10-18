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
console.log("ssadasd")

