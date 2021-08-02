import { csrftoken } from "./csrftoken.js"
import { getPosts } from "./display-posts.js"

document.querySelector('#newpost').onsubmit =  (evt) => {
    evt.preventDefault()
    sendNewPost(document.querySelector('#postcontent').value)
}


function sendNewPost(content){
    if(content == ""){
        alert("you are supposed to write something!")
    }
    else{

        fetch('newpost', {
            method : 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body : JSON.stringify({
                'content' : content
            })
        })
        .then(response => {
            if(response.status === 200){
                // if the user posts something. It should go back to the first page and see their post
                document.querySelector('#postcontent').value = ''
                let page = 1
                getPosts()

            }
            else{
                alert('something went wrong while posting')
            }
        })
    }
}