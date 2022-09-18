const item_innerHTML = "<label for='type_of_item' class='tab1'>What type of POI is this? </label><select name='type_of_item' id='item_type'><option value='weapon'>Weapon</option><option value='armor'>Armor</option><option value='consumable'>Consumable</option><option value='money'>Money</option></select>"
const container_innerHTML = ""

document.querySelector("#poi_type").addEventListener("change", updatePoiDataFields, false)

function updatePoiDataFields() {
    console.log("updatePoiDataFields");
    value = document.querySelector("#poi_type").value;
    if (value == "item") {
        document.querySelector("#poi_data").innerHTML = item_innerHTML;
    }
    else if (value == "container") {
        document.querySelector("#poi_data").innerHTML = container_innerHTML;
    }
    console.log(value);
}
