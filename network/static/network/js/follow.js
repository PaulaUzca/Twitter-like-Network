import { csrftoken } from "./csrftoken.js"

    let followButton = document.querySelector('#followButton')
    
    followButton.addEventListener('click', () => {
        fetch('', {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrftoken,
            }
        })
        .then(response => response.json())
        .then(result => {
            if(result.status = 200){
                //now user is following change button to unfollow
                if(result.follow){
                   followButton.innerHTML = 'Unfollow'
                }
                //now user has unfollowed change button to follow
                else{
                    followButton.innerHTML = 'Follow'
                }
        }

        })
        .catch(error => console.log(error))
    })