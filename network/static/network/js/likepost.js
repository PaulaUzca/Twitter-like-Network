// import csrftoken i got with cookie function in the other document
import { csrftoken } from "./csrftoken.js"


function sendLike(method, id){
    return(
        fetch('/likemanager',{
            method: method,
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
                'postid': id
            })
        })
        .then(response => {
            switch(response.status){
                case 200:
                    return response.json();
                break;
                case 401:
                    alert("sign in to like post");
                break;
                default:
                    throw new Error("Not 2xx response")
                break;
            }
        })
        .catch(error => console.log(error))
    )
}


// function for listen to like button click on document click. 
// This functions executes in the document.onclick function of the page
function likePost(element){
    // LIKE BUTTON
        let method = element.innerText == '❤️'? 'DELETE' : 'PUT'
        let postId = element.dataset.id

        // sendLike returns a fetch call. After that it should wait until a response comes (thats why I use .then)
        sendLike(method, postId).then(result => {
            if(result != undefined){
                if(element.innerText == '❤️'){
                    element.innerText = '🤍'
                }
                else{
                    element.innerText = '❤️'
                }
                element.nextElementSibling.innerText = result.likes
            }
    })
}
export {likePost}




