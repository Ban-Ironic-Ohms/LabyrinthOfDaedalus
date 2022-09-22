import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getDatabase, ref, set, onValue } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-database.js";
import { getAuth, onAuthStateChanged } from "../node_modules/firebase/firebase-auth.js";


const firebaseConfig = {
  databaseURL: "https://labyrinthofdaedalus-79a5f-default-rtdb.firebaseio.com/",
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const db = getDatabase();

console.log("jsonGen.js loaded");
const auth = getAuth()
onAuthStateChanged(auth, (user) => {
  if (user) {
    console.log("OOGOA BOOOGA")
  }
  else {
    console.log("NO USER")
  }
});

// class Poi {
//     constructor(classes) {
//         this.data = {
//             // So yeah... this happened.
//             // So heres the deal. JavaScript sucks and you cant pass a refrence trough a function.
//             // Somewhere along the function chain, the refrence gets converted into a variable.
//             // This means that if you try to change the value of the variable, it will not change the value of the refrence. (because the refrence was lost)
//             // Back to how JS sucks - some thigs are passed by refrence, some are passed by value.
//             // The difference is the type of object you pass. A string is passed by value, an object is passed by refrence.
//             // A list is passed by value.
//             // So, if you want to pass a refrence, you have to pass an object.
//             // This is why I have to pass an object with a single value.
//             // THIS IS SO STUPID.
//             // I hate JS.
//             // I hate JS.
//             // ... you get the point.

//             // SO! This means we can't just pass this class onto firebase, unless we want to fuck everyrthing up.
//             // So we need another function to take this class and convert it into a JSON object / normal js dictionary without the objects.
            
//             // Another issue may arise if we need to go back and edit the data (i.e. edit a room).
//             // But BouncyPantaloons has gladly offered to do that in it's entierty
//             // So we can just have him do that.
//             // I'm not going to do it.
//             // I'm not going to do it. yay!
//             // ... you get the point.
            
//             // Hours lost to this issue: 4 - incriment as necessary

//             //For the record I did no't agree to do all the js -B.P.

//             // General Data
//             name: {value: null},
//             id: {value: null},
//             url: {value: null},
//             class: {value: classes},
//             descriptions: {
//                 main_description: {value: null},
//                 door_description: {value: null},
//                 attack_description: {value: null},
//             },
//             rarity: {value: null},
//             value: {value: null},
//             poi: {value: []},

//             // Consumable
//             effect: {value: null},

//             // Entity Data
//             hp: {value: null},
//             dmg: {value: null},
//             passive_perception: {value: null},
//         }
//     }
// }

function capitalize(str) {
  // Takes in a string of words separated by spaces or underscores, returns a string of words separated by spaces with each first letter capitalized
  let words = str.includes("_") ? str.split("_") : str.split(" ");
  for(let i = 0; i < words.length; i++) {
    words[i] = words[i][0].toUpperCase() + words[i].substring(1);
  }
  return words.join(" ")
}

// function addClassToPoi(poi, className) {
//   if("class" in poi) {
//     poi["class"].push(className);
//   }
//   for(let key in classes[className]) {
//     poi[key] = classes[className][key].default;
//   }
// }

// function getBaseRoom() {
//   let poi = {}
//   addClassToPoi(poi, "poi");
//   addClassToPoi(poi, "room");
//   addClassToPoi(poi, "container");
//   poi.name = "Room"

//   return poi;
// }

function setToValue(dict, key, newValue) {
  dict[key] = newValue
}

let inputTypes = {
  // TODO: Have to figure out when & when not to autofill the default / previously-entered values
  text: (def="", onChange=setToValue, fillDefault=false) => ({default: def, inputType: "input", options: "text", onChange: onChange, fillDefault: fillDefault}),
  number: (def, onChange=setToValue, fillDefault=false) => ({default: def, inputType: "input", options: "number", onChange: onChange, fillDefault: fillDefault}),
  select: (def, multiple, items, onChange=setToValue, fillDefault=false) => ({default: def, inputType: "select", options: {multiple: multiple, list: items}, onChange: onChange, fillDefault: fillDefault}),
  none: (def=undefined, fillDefault=false) => ({default: def, inputType: "none", fillDefault})
}

let classes = {
  poi: {
      name: inputTypes.text("Poi"),
      class: inputTypes.select(["container"], true, ["room", "container", "enemy"]),
      descriptions: {
          main_description: inputTypes.text()
      }
  },
  room: {
      id: inputTypes.number("temporary!"),
      descriptions: {
        door_description: inputTypes.text()
      },
      url: inputTypes.none(),
      rarity: inputTypes.none()
  },
  container: {
      poi: inputTypes.select("Child Poi 1", false, ["Child poi 1", "Child poi 2"]),
      size: inputTypes.number(0)
  },
  enemy: {
    descriptions: {
      attack_description: inputTypes.text()
    }
  }
}

function showPoi(poi) {
    let poiDiv = document.createElement('div');
    poiDiv.classList.add("poi");

    createSection(poi, "poi", poiDiv)

    for(let i = 0; i < poi["class"].length; i++) {
      createSection(poi, poi["class"][i], poiDiv)
    }

    document.getElementById("main").appendChild(poiDiv);
}

function createSection(poi, className, parent) {
    let section_base = document.createElement('div');
    section_base.classList.add("section");

    let header = document.createElement("h1");
    header.innerHTML = capitalize(className);
    section_base.appendChild(header);

    let counter = 0;
    for(let key in classes[className]) {
      let dict = classes[className][key]
      if(!("inputType" in dict)) {
        for(let secondaryKey in dict) {
          if(!(key in poi)) {
            poi[key] = {}
          }
          counter = addInput(poi[key], secondaryKey, dict[secondaryKey], section_base, counter)
          
        } 
      }

      counter = addInput(poi, key, classes[className][key], section_base, counter)
    }

    parent.appendChild(section_base);
}

function addInput(dict, key, input, parentSection, counter) {
  let inputType = input.inputType;
  let options = input.options;
  let field;

  let defaultValue = null;
  if(!(key in dict)) {
    dict[key] = input.default;
    if(input.fillDefault) {
      defaultValue = input.default;
    }
  } else {
    defaultValue = dict[key];
  }

  if (inputType == "input") {
    [field, counter] = createInputField(capitalize(key), options, parentSection, counter, defaultValue);
    field.addEventListener("input", (event) => {
      input.onChange(dict, key, event.srcElement.value);
    })
  } else if(inputType == "select" && !options.multiple) {
    [field, counter] = createSelectionField(capitalize(key), options.list, parentSection, counter, defaultValue);
    field.addEventListener("change", (event) => {
      input.onChange(dict, key, event.srcElement.value);
    });
  } else if(inputType == "select" && options.multiple) {
    [field, counter] = CreateSelectionFieldMultiple(capitalize(key), options.list, parentSection, counter, (values) => {
      input.onChange(dict, key, values)
    }, defaultValue);
    
  }

  return counter
}

function createInputField(input_field_name_str, type, parent, fieldNum, defaultValue=null) {
    let input_field_holder = document.createElement('div');
    input_field_holder.classList.add(fieldNum++ % 2 ? "odd" : "even")
    input_field_holder.classList.add("input_field_holder");

    let input_field_name = document.createElement('span');
    input_field_name.classList.add("input_field_name")
    input_field_name.innerHTML = input_field_name_str;

    let input_field = document.createElement('input');
    input_field.placeholder = input_field_name_str;
    input_field.type = type
    if(defaultValue != null) {
      input_field.value = defaultValue;
    }

    input_field_holder.appendChild(input_field_name);
    input_field_holder.appendChild(input_field);
    parent.appendChild(input_field_holder);
    return [input_field_holder, fieldNum];
}

function createSelectionField(select_field_name_str, list, parent, fieldNum, defaultValue=null) {
    let input_field_holder = document.createElement('div');
    input_field_holder.classList.add(fieldNum++ % 2 ? "odd" : "even")
    input_field_holder.classList.add("input_field_holder")

    let input_field_name = document.createElement('span');
    input_field_name.classList.add("input_field_name")
    input_field_name.innerHTML = select_field_name_str;

    let input_field = document.createElement('select');
    input_field.multiple = false;
    // input_field.className += "chosen-select";
    input_field.id = "poi_type";
    input_field.name = "type_of_poi";
    input_field.width = "100px";
    input_field.placeholder = select_field_name_str;

    list = list.map((word) => capitalize(word))
    for (let i = 0; i < list.length; i++) {
        let new_option = document.createElement("option");
        new_option.value = list[i];
        new_option.innerHTML = list[i];
        input_field.appendChild(new_option)
    }

    input_field.value = defaultValue;

    input_field_holder.appendChild(input_field_name);
    input_field_holder.appendChild(input_field);
    parent.appendChild(input_field_holder);
    // input_field_holder.addEventListener("change", print, false);
    return [input_field_holder, fieldNum];
}

function CreateSelectionFieldMultiple(select_field_name_str, list, parent, fieldNum, onChange, defaultValue=null) {
    var selection_field_holder = document.createElement('div');
    selection_field_holder.classList.add("selection_field_holder")

    var name_field_holder = document.createElement("div")
    name_field_holder.classList.add(fieldNum++ % 2 ? "odd" : "even")
    name_field_holder.classList.add("name_field_holder")
    selection_field_holder.appendChild(name_field_holder)

    var input_field_name = document.createElement('span');
    input_field_name.classList.add("input_field_name")
    input_field_name.innerHTML = capitalize(select_field_name_str);
    name_field_holder.appendChild(input_field_name);

    var fields = [];

    var selectedItems = []
    for (let i = 0; i < list.length; i++) {
        [fields[i], fieldNum] = (createInputField("&nbsp⦿ " + capitalize(list[i]), "checkbox", selection_field_holder, fieldNum));
        fields[i].addEventListener("change", (event) => {
          if(event.srcElement.checked) {
            selectedItems.push(list[i]);
          } else {
            selectedItems.splice(selectedItems.indexOf(list[i]), 1);
          }
          onChange(selectedItems);
        })
    }

    let total_height = 10;

    for (let i = 0; i < fields.length; i++) {
        total_height += fields[i].style.height;
    }

    selection_field_holder.style.height = total_height;

    parent.appendChild(selection_field_holder);
    return [selection_field_holder, fieldNum];
}

function GetSelectValues(select) {
    var result = [];
    var options = select && select.options;
    console.log(options)
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

function print() {
    console.log("PRINTING" + this);
}

function saveRoom(poi) {
  // No longer need to create new PoiDict, since poi is already in the correct format.

  // When saving room, trim any variables in poi that don't correspond to any classes on poi
  // Also, we should probably calculate stuff like rarity and id here, right?

  console.log(poi);

  const room_ref = ref(database, '/rooms/' + poi.id);
  set(room_ref, poi);
}


let room = {};

for(let i in [1]) {
  showPoi(room);
}

document.getElementById("set_room").addEventListener("click", function () {saveRoom(room)})


// IGNORE THIS - these are not the droids you are looking for
// $(".chosen-select").chosen({
//     no_results_text: "Oops, nothing found!"
//   })

//   $('.chosen-select').on("change", function(e) {console.log(e)});
