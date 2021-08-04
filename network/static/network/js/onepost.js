import { likePost } from "./likepost.js"
import { isAllBlank } from "./checkpost.js"
import { csrftoken } from "./csrftoken.js"


document.querySelector('.like__button').onclick = () =>{
    likePost(document.querySelector('.like__button'))
}

//opens the editor view
let editor = document.querySelector('#edit-button')
if(editor)
    editor.onclick = () =>{
    showSections()
    }

// x button on top of editor view
let closeEditor = document.querySelector('#close-editor')
if(closeEditor)
    closeEditor.onclick = () =>{
    showSections()
}

function showSections(){
    document.querySelector('.editpost').classList.toggle('hidesection')  
    document.querySelector('.onepost').classList.toggle('hidesection')  
}

//User has edited the post and now clicks done editing
let doneEditing = document.querySelector('#edit-done')
if(doneEditing)
    doneEditing.onclick = () => editPost()

function isContentInvalid(newcontent){
    if(newcontent == document.querySelector(".content").textContent)
    {
        alert("You didn't edit anything")
        return true
    }
    if(isAllBlank(newcontent)){
        alert("You can't post an empty post")
        return true
    }
    return false
}

function editPost(){
    let newcontent = document.querySelector('#newcontent').value

    if(!isContentInvalid(newcontent) ){
        fetch('', {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body : JSON.stringify({
                'newcontent' : newcontent
            })
        })
        .then(response => {
            if(response.status == 200){
                location.reload()
            }
            else{
                alert("something went wrong :(")
            }
            return response.json()
        })
        .catch(error => console.log(error))

    }
}

let deleteButton = document.querySelector('#delete-post') 
if(deleteButton)
    deleteButton.onclick = () => deletePost()
function deletePost(){
    fetch('', {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": csrftoken,
        }
    })
    .then(response => {
        if(response.ok){
            location.href = '/'
        }
        else{
            alert("something went wrong :(. We couldn't delete your post")
        }
    })
}