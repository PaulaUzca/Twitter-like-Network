import { likePost } from "./likepost.js"

document.querySelector('.like__button').onclick = () =>{
    likePost(document.querySelector('.like__button'))
}
    