function openModal() {
    document.getElementById('modal').classList.add('show');
  }
  
  function closeModal() {
    alert("lsjfd")
    document.getElementById('registerModal').classList.remove('show');
    window.location.href = '/';
  } 
  
// write method to disable login and register button and enable logout button
function loggedIn(){
    document.getElementById('login').hidden = true;
    document.getElementById('register').hidden = true;
    document.getElementById('logout').disabled = false;
}

function loggedOut(){
  document.getElementById('login').disabled = false;
  document.getElementById('register').disabled = true;
  document.getElementById('logout').hidden = true;
}

//write a fucntion to call api to verify user logged in or not
function verifyUser(){
  fetch('/get_user_details')
  .then(res => res.text())
  .then(data => {
    console.log(data)
    data = JSON.parse(data);
    if(data.status === 'success'){
      loggedIn();
    }else{
      loggedOut();
    }
  })
}

//write function to call verifyuser() when page loads
