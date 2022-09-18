
//document.querySelector("#input_jkl").addEventListener("input", Set, true)

function Set(value) {
    console.log(value)
    //document.querySelector("#Show").innerHTML = document.querySelector('#Input').value;
}

light_gray = true;

class Poi {
    constructor() {
        this.name;
        this.bool;
        this.number;
        this.description;
        this.child_pois = [];
        this.classes = [];
    }
}

room = new Poi();

function ShowPoi(poi) {
    base = document.createElement('div');
    base.id = "main";
    base.style.height = "97vh";
    base.style.width = String(25) + "%";
    base.style.backgroundColor = "gray";

    CreateSection(poi, "Room", base, [["text", "Name", poi.name], ["text", "Description", poi.description], ["checkbox", "Bool", poi.bool], ["number", "Number", poi.number]]);
    CreateSection(poi, "Door", base, [["text", "Description", poi.name], ["input", "Child Pois?", poi.name]]);

    document.body.appendChild(base);
    document.body.appendChild(base);
}

function CreateSection(poi, section_name, parent, items) {
    section_base = document.createElement('div');

    section_base.id = "section";
    section_base.style.width = "90%"
    section_base.style.marginLeft = "5%"
    section_base.style.outline = '3px dashed black';
    section_base.height = "10px";

    header = document.createElement("h1");
    header.innerHTML=section_name;
    header.style.height = "17px";
    section_base.appendChild(header);


    for (let i = 0; i < items.length; i++) {
        items[i][2] = CreateInputField(items[i][1], items[i][0], section_base);
    }
    parent.appendChild(section_base);
}

function CreateInputField(input_field_name_str, type, parent) {
    input_field_holder = document.createElement('div');
    if (light_gray)
        input_field_holder.style.backgroundColor = "darkgray" 
        light_gray = !light_gray;

    input_field_holder.id = "input_field_holder"

    input_field_name = document.createElement('text');
    input_field_name.style.marginLeft = "25px"
    input_field_name.innerHTML = input_field_name_str;

    input_field = document.createElement('input');
    input_field.style.marginLeft = "25px"
    input_field.placeholder = input_field_name_str;
    input_field.type = type

    input_field_holder.appendChild(input_field_name);
    input_field_holder.appendChild(input_field);
    parent.appendChild(input_field_holder);
    return input_field_holder;
}

ShowPoi(room);