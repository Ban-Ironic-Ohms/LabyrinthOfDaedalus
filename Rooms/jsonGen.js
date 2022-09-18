
//document.querySelector("#input_jkl").addEventListener("input", Set, true)

// function Set(value) {
//     console.log(value)
//     //document.querySelector("#Show").innerHTML = document.querySelector('#Input').value;
// }

light_gray = true;

class Room {

}

class Poi {
    constructor(classes) {
        this.data = {
            // So yeah... this happened.
            // So heres the deal. JavaScript sucks and you cant pass a refrence trough a function.
            // Somewhere along the function chain, the refrence gets converted into a variable.
            // This means that if you try to change the value of the variable, it will not change the value of the refrence. (because the refrence was lost)
            // Back to how JS sucks - some thigs are passed by refrence, some are passed by value.
            // The difference is the type of object you pass. A string is passed by value, an object is passed by refrence.
            // A list is passed by value.
            // So, if you want to pass a refrence, you have to pass an object.
            // This is why I have to pass an object with a single value.
            // THIS IS SO STUPID.
            // I hate JS.
            // I hate JS.
            // ... you get the point.

            // SO! This means we can't just pass this class onto firebase, unless we want to fuck everyrthing up.
            // So we need another function to take this class and convert it into a JSON object / normal js dictionary without the objects.
            
            // Another issue may arise if we need to go back and edit the data (i.e. edit a room).
            // But BouncyPantaloons has gladly offered to do that in it's entierty
            // So we can just have him do that.
            // I'm not going to do it.
            // I'm not going to do it. yay!
            // ... you get the point.
            
            // Hours lost to this issue: 4 - incriment as necessary

            //For the record I did no't agree to do all the js -B.P.

            // General Data
            name: {value: null},
            id: {value: null},
            url: {value: null},
            class: {value: classes},
            descriptions: {
                main_description: {value: null},
            },
            rarity: {value: null},
            value: {value: null},
            poi: {},

            // Consumable
            effect: {value: null},

            // Entity Data
            hp: {value: null},
            dmg: {value: null},
            passive_perception: {value: null},
        }
    }
}

room = new Poi(["room", "enemy", "container"]);

function ShowPoi(poi) {
    base = document.createElement('div');
    base.id = "main";
    base.style.height = "97vh";
    base.style.width = String(25) + "%";
    base.style.backgroundColor = "gray";

    if (poi.data.class.value.includes("room")) {
        CreateSection(poi, "Room", base, [["text", "Room Name", poi.data.name], ["text", "Main Description", poi.data.descriptions.main_description], ["selection", "Class(s)", poi.data.class, ["room", "container", "enemy", "item", "consumable"]]]);
    }

    // if (poi.classes.includes("enemy")) {
    //     CreateSection(poi, "Door", base, [["text", "Description", poi.name], ["input", "Child Pois?", poi.name]]);
    // }

    // if (poi.classes.includes("container")) {
    //     CreateSection(poi, "Pois", base, [["text", "Description", poi.name], ["input", "Child Pois?", poi.name]]);
    // }

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
        function save(variable, event) {
            variable.value = event.srcElement.value;
            console.log(poi);
        }
        
        if (items[i][0] == "selection") {
            field = CreateSelectionField(items[i][1], items[i][3], section_base);
        } 
        else {
            field = CreateInputField(items[i][1], items[i][0], section_base);
            field.addEventListener("input", save.bind(this, items[i][2]))
        }
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

function CreateSelectionField(select_field_name_str, options, parent) {
    input_field_holder = document.createElement('div');
    if (light_gray)
        input_field_holder.style.backgroundColor = "darkgray" 
        light_gray = !light_gray;

    input_field_holder.id = "input_field_holder"

    input_field_name = document.createElement('text');
    input_field_name.style.marginLeft = "25px"
    input_field_name.innerHTML = select_field_name_str;

    input_field = document.createElement('select');
    input_field.style.marginLeft = "50px"
    input_field.multiple = true;
    input_field.className += "chosen-select";
    input_field.id = "poi_type";
    input_field.name = "type_of_poi";
    input_field.width = "100px";
    input_field.placeholder = select_field_name_str;

    for (let i = 0; i < options.length; i++) {
        new_option = document.createElement("option");
        new_option.value = options[i];
        new_option.innerHTML = options[i];
        input_field.appendChild(new_option)
    }

    input_field_holder.appendChild(input_field_name);
    input_field_holder.appendChild(input_field);
    parent.appendChild(input_field_holder);
    return input_field;
}

function GetSelectValues(select) {
    var result = [];
    var options = select && select.options;
    var opt;

    for (var i=0, iLen=options.length; i<iLen; i++) {
        opt = options[i];

        if (opt.selected) {
        result.push(opt.value || opt.text);
        }
    }
    console.log(result);
    return result;
}

ShowPoi(room);









// IGNORE THIS - these are not the droids you are looking for
$(".chosen-select").chosen({
    no_results_text: "Oops, nothing found!"
  })