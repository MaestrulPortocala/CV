const reluEL=document.querySelector(".relu");
const bodyEL=document.querySelector("body");

updateBody();
function updateBody(){
    if (reluEL.checked){
bodyEL.style.background = "black";
    }
    else{
        bodyEL.style.background = "white";
    }
}

reluEL.addEventListener("input", ()=>{
    updateBody()
})

