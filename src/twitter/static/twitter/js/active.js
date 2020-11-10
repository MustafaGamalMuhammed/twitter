let nav_links = document.getElementsByClassName("nav-link");
let active_link = null;

function changeLinkStyle(link) {
    if(active_link) {
        active_link.style.color = '#333';
    }
    active_link = link;
    active_link.style.color = '#1DA1F2';
}

for(let link of nav_links) {
    if(link.pathname == document.location.pathname) {
        changeLinkStyle(link)
    }

    link.addEventListener('click', (e) => {
        changeLinkStyle(e.target);
    })
}