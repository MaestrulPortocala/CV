const imageEl = document.querySelector(".image-compartiment");
const btnEL = document.querySelector(".btn");

btnEL.addEventListener(
    "click", ()=>{
       
        moreIMG();
    }
);

function moreIMG(){
    for (let index = 0; index < 10; index++) {
        const imgEL = document.createElement("img");
    imgEL.src = `https://picsum.photos/300?random=${Math.floor(Math.random()*20000)}`;
    imageEl.appendChild(imgEL)
    }
    
};