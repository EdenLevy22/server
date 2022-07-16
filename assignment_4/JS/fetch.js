function myFunction() {
     let num =  document.getElementById("user_id").value
    console.log(num)
    fetch(`https://reqres.in/api/users/${num}`).then(
        response => response.json()
    ).then(
        response => createUsersList(response.data)
    ).catch(
        err => console.log(err)
    );
}

function createUsersList(users){
       console.log(users)
       const user =users
       const curr_main = document.querySelector("main");

            const section = document.createElement('section');
            section.innerHTML = `
            <br>
             <img src="${user.avatar}" alt="Profile Picture"/>
             <div>
                <span>${user.first_name} ${user.last_name}</span>
                <br>
                <br>
                 <a href="mailto:${user.email}">Send Email</a>
            </div>
            `;
             curr_main.appendChild(section);



}