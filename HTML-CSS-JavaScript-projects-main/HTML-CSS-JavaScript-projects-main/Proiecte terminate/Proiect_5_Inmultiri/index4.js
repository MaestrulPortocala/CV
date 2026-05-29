const num1 = Math.ceil(Math.random()*10);
const num2 = Math.ceil(Math.random()*10);
let score= JSON.parse(localStorage.getItem(".score"));
if(!score){
    score = 0;
}
const scoreEl = document.querySelector(".score");
const inputEl = document.querySelector(".masa");
const textEL = document.querySelector(".text");
const formEl = document.querySelector(".square");
textEL.innerText = `What is ${num1}*${num2}?`;
scoreEl.innerText = `score: ${score}`;
const correctAns = num1 * num2;


formEl.addEventListener(
    "submit", ()=>{
        const userAns = +inputEl.value;
        if(userAns === correctAns){
            score++;
            yes();
           }
           else{
               score--;
              yes();
     } })
     function yes(){
        localStorage.setItem(".score", JSON.stringify(score));
    }; 
 