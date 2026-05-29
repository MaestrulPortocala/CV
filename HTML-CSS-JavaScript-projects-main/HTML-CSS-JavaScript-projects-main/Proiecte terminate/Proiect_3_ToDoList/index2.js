const formEL= document.querySelector(".form");
const inputEL= document.querySelector(".input");
const olEL= document.querySelector(".list");



formEL.addEventListener(
    "submit", (ded)=>{
ded.preventDefault()
toDoList()
    }
)
function toDoList() {
let newTask=inputEL.value;
const leEL = document.createElement("li");
leEL.innerText=newTask;
olEL.appendChild(leEL);
inputEL.value="";
const bitnEL = document.createElement("div");
bitnEL.innerHTML=`<i class="fas fa-check-square">`;
leEL.appendChild(bitnEL);
const trashEL = document.createElement("div");
trashEL.innerHTML=`<i class="fas fa-trash">`;
leEL.appendChild(trashEL);


bitnEL.addEventListener(
    "click", () => {
        leEL.classList.toggle("checked")
    }
)

trashEL.addEventListener(
    "click", () => {
        leEL.remove()
    }
)
}