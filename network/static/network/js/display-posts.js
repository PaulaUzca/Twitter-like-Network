
var page = 1

var post_container = document.querySelector('#allposts')
function getPosts(){
    return(
            fetch(`?page=${page}`)
            .then(response => response.json())
            .then(data => {
                post_container.innerHTML = data.posts
                document.querySelector('#next_button').style.display = data.next>0? 'block':'none'
                document.querySelector('#previous_button').style.display = data.prev>0? 'block':'none'
                document.querySelector('#page_number').textContent = data.page
            })
            .catch(error => console.log(error))
        )
}


/* since new post will be loading every time they wont have any event listeners.
And its kind of annoying to assign new event listeners every time
So it's better to listen to the whole document and check when the user clicks on the like buttons
*/ 

import { likePost } from "./likepost.js"

/*There should be only one document on click event listener per page
Since more would end up in overwriting and not all events would execute
*/
document.onclick = event =>{
    // POST 
    let element = event.target

    if(element.className == 'post'){
        location.href = `/post/${element.dataset.id}`
    }
    if(element.className == 'like__button'){
        likePost(element) // I imported this function which contains what should happen if user clicks on like button
    }
}

window.onload = () =>{
    page = 1
    getPosts()
}

document.querySelector('#previous_button').onclick = () =>{ 
    page --;
    getPosts()
}
document.querySelector('#next_button').onclick = () =>{
    page ++
    getPosts()
}



export {getPosts}


