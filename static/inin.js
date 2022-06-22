window.onload = function(){

  
    const activePage = window.location.pathname;
    console.log(activePage);
    
     document.querySelectorAll('a').forEach(link => {    
      if(link.href.includes(`${activePage}`)){
        link.classList.add('active');
      }
    });
    
    }
    
    function showNames() {
      document.getElementById("change").innerHTML = "LUCKY, SKY, ALPHA ";
    }

    function send() {
      document.getElementById("send").innerHTML = "תודה רבה! ניצור עמך קשר ברגע שנמצא לך חבר מתאים";
    }

