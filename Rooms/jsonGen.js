
document.querySelector("#input").addEventListener("input", Set, true)

// function Set() {
//     document.querySelector("#Show").innerHTML = document.querySelector('#Input').value;
// }


class Poi {
    constructor() {
        this.child_pois = [];
    }
}

room = new Poi();

function ShowPoi(poi) {
    const template = document.createElement('div');
    template.style.height = "97vh";
    template.style.width = String(25) + "%";
    //template.style.marginTop = "100px";
    template.style.color = "green"; 
    template.style.backgroundColor = "orange";
    template.innerHTML = "Test POI";

    document.body.appendChild(template);
}

ShowPoi(room);