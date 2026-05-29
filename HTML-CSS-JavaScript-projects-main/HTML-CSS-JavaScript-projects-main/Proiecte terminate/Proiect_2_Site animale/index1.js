let buttons=new Array(4);
let audio=new Array(4);
let animals= new Array("bird", "cat", "cow", "dog");
for(i=0; i<4; ++i){
    buttons[i]=document.querySelector(`.btn${i}`);
    audio[i]=document.createElement("audio");
    audio[i].src=`audio/${animals[i]}.wav`;
    buttons[i].appendChild(audio[i]);
}
buttons[0].addEventListener("click", ()=>{
    audio[0].play();
});
buttons[1].addEventListener("click", ()=>{
    audio[1].play();
});
buttons[2].addEventListener("click", ()=>{
    audio[2].play();
});
buttons[3].addEventListener("click", ()=>{
    audio[3].play();
});
