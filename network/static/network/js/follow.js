import { csrftoken } from "./csrftoken.js"

    let followButton = document.querySelector('#followButton')
    
    followButton.addEventListener('click', () => {
        fetch('', {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrftoken,
            }
        })
        .then(response => {
            switch(response.status){
                case 200:
                    return response.json()
                break;
                case 401:
                    alert("Sign in to follow users! :D")
                break;
                default:
                    console.log("something went wrong")
                break;
            }
        })
        .then(result => {
            //now user is following change button to unfollow
            if(result.follow){
                followButton.innerHTML = 'Unfollow'
            }
            //now user has unfollowed change button to follow
            else{
                followButton.innerHTML = 'Follow'
            }

        })
        .catch(error => console.log(error))
    })