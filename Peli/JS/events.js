'use strict';


async function flight_events() {
    const response = await FetchFromDatabase('/events/');
    let dialog = document.getElementById('events');
    let div = document.getElementById('options');
    div.innerHTML = ''
    let p = document.createElement('p');
    p.id = 'question'
    let img = document.createElement('img');
    img.id = 'pic'
    let ul = document.createElement('ul');
    p.innerHTML = response.question;
    img.src = response.url;
    for (let key in response.options) {
        let li = document.createElement('li');
        let link = document.createElement('a');
        link.innerHTML = response.options[key];
        link.addEventListener('click', function () {
            dialog.close();
            console.log('moi')
        })
        li.appendChild(link)
        ul.appendChild(li);
    }
    div.appendChild(img);
    div.appendChild(p);
    div.appendChild(ul);
    dialog.showModal();
}