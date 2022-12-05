'use strict';



async function createHighscores() {
    let highscores = await makeAFetchForData('/gethighscores');
    let container = document.getElementById('scroe');
    for(let i = 0; i < highscores.length; i++){
        
    }
}

window.onload = async function(){
    createHighscores();
}