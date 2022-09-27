import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getDatabase, ref, set, onValue } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-database.js";
import { getAuth, onAuthStateChanged } from "../node_modules/firebase/firebase-auth.js";
// import { generateID, pureRandom } from "./id_generator.js";

const firebaseConfig = {
  databaseURL: "https://labyrinthofdaedalus-79a5f-default-rtdb.firebaseio.com/",
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const db = getDatabase();

console.log("jsonGen.js loaded");


function capitalize(str) {
  // Takes in a string of words separated by spaces or underscores, returns a string of words separated by spaces with each first letter capitalized
  let words = str.includes("_") ? str.split("_") : str.split(" ");
  if(words.length == 0 || (words.length == 1 && words[0] == "")) {
    return "";
  }
  for(let i = 0; i < words.length; i++) {
    words[i] = words[i][0].toUpperCase() + words[i].substring(1);
  }
  return words.join(" ");
}

let inputTypes = {
  getSetToValueFunc: (key) => {
    return (dict, newValue, sectionDiv) => {
      dict[key] = newValue
    }
  },
  Text: class Input {
    constructor(title, def, onChange, fillDefault=false, onCreate=undefined) {
      this.title = title;
      this.default = def;
      this.inputType = "input";
      this.options = {type: "text"};
      this.onChange = typeof onChange == "string" ? inputTypes.getSetToValueFunc(onChange) : onChange;

      this.fillDefault = fillDefault;
      this.onCreate = onCreate;
    }
  },
  Number: class Input {
    constructor(title, def, onChange=this.setToValue, fillDefault=false, onCreate=undefined) {
      this.title = title;
      this.default = def;
      this.inputType = "input";
      this.options = {type: "number"};
      this.onChange = onChange;
      this.fillDefault = fillDefault;
      this.onChange = typeof onChange == "string" ? inputTypes.getSetToValueFunc(onChange) : onChange;
      this.onCreate = onCreate;
    }
  },
  Select: class Input {
    constructor(title, def, multiple, items, onChange, fillDefault=false, onCreate=undefined) {
      this.title = title;
      this.default = def;
      this.inputType = "select";
      this.options = {multiple: multiple, list: items};
      this.onChange = onChange;
      this.fillDefault = fillDefault;
      this.onChange = typeof onChange == "string" ? inputTypes.getSetToValueFunc(onChange) : onChange;
      this.onCreate = onCreate;
    }
  },
  Button: class Input {
    constructor(title, text, onClick, onCreate=undefined) {
      this.title = title;
      this.inputType = "button";
      this.options = {type: "button", text: text};
      this.onClick = onClick;
      this.onCreate = onCreate;
    }
  },
  None: class Input {
    constructor(def, fillDefault=false) {
      this.default = def;
      this.inputType = "none";
      this.fillDefault = fillDefault;
    }
  },
}

function findElementInElement(classToFind, parentElement) {
  if(parentElement.classList.contains(classToFind)) {
    return parentElement;
  }
  let children = parentElement.children;

  for(let i = 0; i < children.length; i++) {
    let childResult = findElementInElement(classToFind, children[i]);
    if(childResult != undefined) {
      return childResult;
    }
  }

  return undefined;
}
let poiIdCounter = 0;
let poisById = {};

let classes = {
  poi: {
      name: new inputTypes.Text("Name", "Poi", (dict, newValue, sectionDiv) => {
        dict["name"] = newValue;
        sectionDiv.children[0].innerHTML = newValue;
        
        let previousLayer = sectionDiv.parentElement.getAttribute("data-poi-layer") - 1;
        if(previousLayer >= 0) {
          let poiDivs = sectionDiv.parentElement.parentElement.children;
          for(let i = 0; i < poiDivs.length; i++) {
            if(poiDivs[i].getAttribute("data-poi-layer") == previousLayer) {
              let selector = findElementInElement("poi_selector", poiDivs[i]);
              selector.options[selector.selectedIndex].innerHTML = newValue;
              console.log(selector.selectedIndex)
            }
          }
        }
      }),
      class: new inputTypes.Select("Classes", [], true, ["room", "container", "enemy"], (dict, newValue, sectionDiv) => {        
        dict["class"] = newValue;
        setSections(dict, sectionDiv.parentElement);
      }),
      descriptions: {
          main_description: new inputTypes.Text("Main Description", "", "main_desciption")
      }
  },
  room: {
      id: new inputTypes.Number("ID (temporary)", 0, "id"),
      descriptions: {
        door_description: new inputTypes.Text("Door Description", "", "door_description")
      },
      url: new inputTypes.None(""),
      rarity: new inputTypes.None(0)
  },
  container: {
      poi: [
        new inputTypes.Select("Child Pois", [], false, [], (dict, newValue, sectionDiv) => {
          removePoi(1 + sectionDiv.parentElement.getAttribute("data-poi-layer"));
          if(newValue != undefined) {
            addPoi(poisById[newValue])
          }
          console.log("CHANGED!")
        }, false, (field) => {field.classList.add("poi_selector")}),
        new inputTypes.Button("", "+", (dict, sectionDiv) => {
          let selector = findElementInElement("poi_selector", sectionDiv);
          let newOption = document.createElement("option");

          newOption.value = poiIdCounter++;
          poisById[newOption.value] = {}
          dict["poi"].push(poisById[newOption.value])

          selector.appendChild(newOption);
          selector.value = newOption.value;
          
          classes.container.poi[0].onChange(dict, newOption.value, sectionDiv)
        }),
        new inputTypes.Button("", "-", (dict, sectionDiv) => {
          let selector = findElementInElement("poi_selector", sectionDiv);
          dict["poi"].splice(dict["poi"].indexOf(selector.value))
          poisById[selector.value] = undefined;
          selector.remove(selector.value);
        })
      ],
      size: new inputTypes.Number("Size", 0, "size")
  },
  enemy: {
    descriptions: {
      attack_description: new inputTypes.Text("Attack Description", "", "attack_description")
    }
  }
}

var poisOnScreen = 0;

/** Adds a new column to the screen representing a POI.
 * Creates and adds div with class "poi" that is background of column, 
 * calls addSection to add base "poi" section, and again to add sections for each class poi has. 
 * @param {Object} poi The POI to add to screen
 */
function addPoi(poi) {
    let poiDiv = document.createElement('div');
    poiDiv.classList.add("poi");
    poiDiv.setAttribute("data-poi-layer", poisOnScreen++)

    addSection(poi, "poi", poiDiv);

    for(let i = 0; i < poi["class"].length; i++) {
      addSection(poi, poi["class"][i], poiDiv)
    }

    document.getElementById("main").appendChild(poiDiv);
}

function removePoi(layer) {
  let poiDivs = document.getElementById("main").children;
  for(let i = 0; i < poiDivs.length; i++) {
    if(poiDivs[i].getAttribute("data-poi-layer") == layer) {
      removePoi(layer + 1);
      document.getElementById("main").removeChild(poiDivs[i]);
      break;
    }
  }
}

function setSections(poi, parentDiv) {
  let sections = Array.from(parentDiv.children).filter(
    (child) => child.classList.contains("section") && child.getAttribute("data-corresponding-class") != "poi");
  let classes = poi["class"];

  for(let i = 0; i < classes.length; i++) {
    let classAlreadyHasSection = false;
    for(let j = 0; j < sections.length; j++) {
      if(sections[j].getAttribute("data-corresponding-class") == classes[i]) {
        classAlreadyHasSection = true;
        break;
      }
    }
    if(!classAlreadyHasSection) {
      // For every class being added (because it doesn't have a section but it's in the list of classes):
      addSection(poi, classes[i], parentDiv);
    }
  }

  for(let i = 0; i < sections.length; i++) {
    let sectionClass = sections[i].getAttribute("data-corresponding-class")
    // console.log(sectionClass, "in [", String(classes), "] =", sectionClass in classes)
    let sectionClassInClasses = false;
    for(let j = 0; j < classes.length; j++) {
      if(sectionClass == classes[j]) {
        sectionClassInClasses = true;
        break;
      }
    }

    if(!sectionClassInClasses) {
      // For every class being removed (because it has a section but isn't in the list of classes):
      removeSection(parentDiv, sectionClass);
    }
  }
}

/** Adds a section corresponding to a class name to a POI Div.
 * Creates a section div and adds it to the POI Div. Creates a header for the section.
 * Loops through all possible parameters that the class adds, and calls addInput for each one.
 * @param {Object} poi Poi that the POI Div is representing.
 * @param {String} className Name of the class corresponding to the section to be added.
 * @param {HTMLElement} parentDiv Div to add the section to.
 */
function addSection(poi, className, parentDiv) {
  let sectionBase = document.createElement('div');
  sectionBase.classList.add("section");
  sectionBase.setAttribute("data-corresponding-class", className);

  let header = document.createElement("h1");
  header.innerHTML = capitalize(className);
  sectionBase.appendChild(header);

  parentDiv.appendChild(sectionBase);

  /** Calls addInput to create an input field for the given input and dictionary. Can take one or a list of inputs.
   * This function exists to handle lists of inputs.
   * @param {*} dict Dictionary to be modified by input.
   * @param {Input or Array of Input} input Input or array of inputs to be added to section.
   * @param {*} sectionBase Class section to add inputs to.
   * @param {*} counter Counter that counts how many inputs have been added.
   * @returns Value of counter after adding inputs.
   */
  function addInputOrInputList(dict, key, input, sectionBase, counter) {
    if(input instanceof Array) {
      for(let i = 0; i < input.length; i++) {
        if(!(key in dict)) {
          dict[key] = input[i].default;
          // TODO: Uncommenting this crashes everything
          // input[i].onChange(dict, dict[key], sectionBase)
        }
        let defaultValue = input[i].fillDefault ? input[i].default : undefined;
        counter = addInput(dict, input[i], sectionBase, counter, defaultValue)
      }
    } else {
      if(!(key in dict)) {
        dict[key] = input.default;
        input.onChange(dict, dict[key], sectionBase);
      }
      let defaultValue = input.fillDefault ? input.default : undefined;
      counter = addInput(dict, input, sectionBase, counter, defaultValue)
    }
    return counter
  }

  let counter = 0;
  for(let key in classes[className]) {
    // dict is either an Input Object, list of Input Objects or a dictionary of Input Objects
    let inputOrInputs = classes[className][key]

    if("inputType" in inputOrInputs || inputOrInputs instanceof Array) {
      // If the selected input is an input or list of inputs, add it/them to sectionBase by calling addInputOrInputList
      counter = addInputOrInputList(poi, key, inputOrInputs, sectionBase, counter)
    } else {
      // If the selected element is actually a dict with inputs inside, loop through the dict instead.
      if(!(key in poi)) {
        poi[key] = {}
      }
      for(let secondaryKey in poi[key]) {
        counter = addInputOrInputList(poi[key], secondaryKey, inputOrInputs[secondaryKey], sectionBase, counter)
      }
    }

    if(className == "poi") {
      header.innerHTML = poi["name"]
    }

  }
}

/** Removes a section from a POI Div, given a class name.
 * Loops through all elements that are a child of the POI Div. If they have the attribute corresponding to the class name inputted, removes them.
 * @param {HTMLElement} parentDiv POI Div that the section is in.
 * @param {String} className Name of class corresponding to section to be removed.
 */
function removeSection(poiDiv, className) {
  let childElements = poiDiv.children;
  for(let i = 0; i < childElements.length; i++) {
    
    if(childElements[i].getAttribute("data-corresponding-class") == className) {
      poiDiv.removeChild(childElements[i]);
      break;
    }
  }
}

/** Ad
 * 
 * @param {Object} dict The dictionary containing the value to be modified. 
 * @param {Object} input The object representing the input to be added. 
 * @param {HTMLElement} parentSection The class section to add the input to.
 * @param {Int} counter A counter that goes up by 1 every time an input is added. Used for coloring.
 * @param {*} defaultValue The value that the input should display when first created. Leave null for nothing.
 * @returns The new value of counter after input has been added.
 */
function addInput(dict, input, parentSection, counter, defaultValue=undefined) {
  let inputType = input.inputType;
  let options = input.options;
  let title = input.title;
  let field;

  if (inputType == "input") {
    [field, counter] = createInputField(title, options, parentSection, counter, defaultValue);
    field.addEventListener("input", (event) => {
      input.onChange(dict, event.srcElement.value, parentSection);
    })
  } else if(inputType == "select" && !options.multiple) {
    [field, counter] = createSelectionField(title, options.list, parentSection, counter, defaultValue);
    field.addEventListener("change", (event) => {
      input.onChange(dict, event.srcElement.value, parentSection);
    });
  } else if(inputType == "select" && options.multiple) {
    [field, counter] = createSelectionFieldMultiple(title, options.list, parentSection, counter, (values) => {
      input.onChange(dict, values, parentSection)
    }, defaultValue);
  } else if(inputType == "button") {
    [field, counter] = createButtonField(title, options.type, parentSection, counter, options.text);
    field.addEventListener("click", () => {
      input.onClick(dict, parentSection);
    })
  }

  if(input.onCreate != undefined) {
    input.onCreate(field)
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
    return [input_field, fieldNum];
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
    // input_field.id = "poi_type";
    // input_field.name = "type_of_poi";
    // input_field.width = "100px";
    input_field.placeholder = select_field_name_str;

    list = list.map((word) => capitalize(word))
    for (let i = 0; i < list.length; i++) {
        let new_option = document.createElement("option");
        // TODO: change this vvv
        new_option.value = list[i];
        new_option.innerHTML = list[i];
        input_field.appendChild(new_option)
    }

    input_field.value = defaultValue;

    input_field_holder.appendChild(input_field_name);
    input_field_holder.appendChild(input_field);
    parent.appendChild(input_field_holder);
    // input_field_holder.addEventListener("change", print, false);
    return [input_field, fieldNum];
}

function createSelectionFieldMultiple(select_field_name_str, list, parent, fieldNum, onChange, defaultValue=null) {
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
    // TODO: What do I return here? vvv
    return [selection_field_holder, fieldNum];
}

function createButtonField(input_field_name_str, type, parent, fieldNum, buttonText="") {
  let input_field_holder = document.createElement('div');
  input_field_holder.classList.add(fieldNum++ % 2 ? "odd" : "even")
  input_field_holder.classList.add("input_field_holder");

  let input_field_name = document.createElement('span');
  input_field_name.classList.add("input_field_name")
  input_field_name.innerHTML = input_field_name_str;

  let input_field = document.createElement('button');
  input_field.innerHTML = buttonText;
  input_field.type = type

  input_field_holder.appendChild(input_field_name);
  input_field_holder.appendChild(input_field);
  parent.appendChild(input_field_holder);
  return [input_field, fieldNum];
}

function saveRoom(poi) {
  // No longer need to create new PoiDict, since poi is already in the correct format.

  // When saving room, trim any variables in poi that don't correspond to any classes on poi
  // Also, we should probably calculate stuff like rarity and id here, right?

  console.log(poi);

  poi.id = generateID();
  console.log(poi.id);
  const room_ref = ref(database, '/rooms/' + poi.id);
  onValue(room_ref, (snapshot) => {
    if ( snapshot.val() != null ) {
      console.log("Room with that ID already exists - you just expirenced a one-in-2.27-thousand-quintillion-quintillion-quintillion chance. And yes, I wrote a case for it");
      saveRoom(poi);
    } else {
      set(room_ref, poi);
    }
  }, {
    onlyOnce: true
  });
}

function generateID() {
  // generates a random 32 character string - letters and numbers, no special characters
  var result = '';
  var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for (var i = 0; i < 32; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}


let room = { };

for(let i in [1]) {
  addPoi(room);
}

document.getElementById("set_room").addEventListener("click", function () {saveRoom(room)})
