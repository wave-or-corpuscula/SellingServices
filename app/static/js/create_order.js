var itemsCount = 0;


async function fillObjectCategoriesDiv(object_id, catsDiv, costDisplayInput, objectCost) {
    catsDiv.innerHTML = "";
    await fetch(`/get_object_categories/${object_id}`)
    .then(response => response.json())
    .then((data) => {
        const objectCategories = data["object_categories"];
        const categoriesSubcats = data["category_subcategories"];

        for (let i = 0; i < objectCategories.length; i++) {
            const categoryDiv = document.createElement("div");
            categoryDiv.classList.add("service-object-category");
            const categorySelect = document.createElement("select");
            const newLabel = document.createElement("label");
            newLabel.classList.add("form-label");
            newLabel.setAttribute("for", objectCategories[i].id);
            newLabel.innerHTML = objectCategories[i].name;
            
            // Category cost input + label

            const categoryCostInput = document.createElement("input")
            categoryCostInput.readOnly = true
            categoryCostInput.id = "category-cost"
            categoryCostInput.type = "text"
            categoryCostInput.value = 0;
            categoryCostInput.classList.add("form-control", "mb-3")

            const categoryCostInputLabel = document.createElement("label")
            categoryCostInputLabel.classList.add("form-label");
            categoryCostInputLabel.setAttribute("for", categoryCostInput.id)
            categoryCostInputLabel.innerHTML = "Стоимость категории"

            categorySelect.id = objectCategories[i].id;
            categorySelect.textContent = objectCategories[i].name;
            categorySelect.classList.add("form-control");
            categoriesSubcats[i].forEach(element => {
                const option = document.createElement("option");
                option.value = element.id;
                option.textContent = element.name;
                option.setAttribute("cost", element.cost);
                categorySelect.appendChild(option);
            });

            categorySelect.addEventListener("change", function() {
                categoryCostInput.value = categorySelect.options[categorySelect.selectedIndex].getAttribute("cost");
                setOrderCost();
            })
            categorySelect.dispatchEvent(new Event('change'));

            categoryDiv.appendChild(newLabel);
            categoryDiv.appendChild(categorySelect);
            categoryDiv.appendChild(categoryCostInputLabel);
            categoryDiv.appendChild(categoryCostInput);
            
            catsDiv.appendChild(categoryDiv);
        }
        
        costDisplayInput.value = objectCost;
        setOrderCost();
    });
}

async function addNewServiceObjectItem() {
    itemsCount++;
    const allItemsDiv = document.getElementById("service_objects");
    const newItemDiv = document.createElement("div")
    const objectAndCategoriesDiv = document.createElement("div");
    const serviceObjectsSelect = document.createElement("select");
    const objectCategoriesDiv = document.createElement("div");
    objectCategoriesDiv.classList.add("mb-3", "service-object-categories");
    newItemDiv.classList.add("service-object-item");
    
    objectAndCategoriesDiv.name = `service-object-item`;

    // Service object list

    await fetch("/employee/load_service_objects")
    .then(response => response.json())
    .then((data) => {
        serviceObjectsSelect.innerHTML = '<option value="">Выберите вид услуги</option>';
        serviceObjectsSelect.classList.add("form-control");
        data.forEach(element => {
            const option = document.createElement("option");
            option.value = element.id;
            option.setAttribute("cost", element.cost);
            option.textContent = element.name;
            serviceObjectsSelect.appendChild(option);
        });
    });
    serviceObjectsSelect.addEventListener("change", function() {
        fillObjectCategoriesDiv(serviceObjectsSelect.options[serviceObjectsSelect.selectedIndex].value, objectCategoriesDiv, objectCostInput, serviceObjectsSelect.options[serviceObjectsSelect.selectedIndex].getAttribute("cost")); 
    });

    // Object cost input

    const objectCostInput = document.createElement("input")
    objectCostInput.readOnly = true
    objectCostInput.id = "object-cost"
    objectCostInput.name = "object-cost"
    objectCostInput.type = "text"
    objectCostInput.value = 0;
    objectCostInput.classList.add("form-control", "mb-3")
    const objectCostInputLabel = document.createElement("label")
    objectCostInputLabel.classList.add("form-label");
    objectCostInputLabel.setAttribute("for", objectCostInput.id)
    objectCostInputLabel.innerHTML = "Стоимость услуги"

    // Remove button
    
    const removeButton = document.createElement("button");
    removeButton.classList.add("btn", "btn-danger", "mb-3");
    removeButton.type = "button";
    removeButton.innerHTML = "Удалить";
    removeButton.addEventListener("click", () => { 
        newItemDiv.remove(); 
        setOrderCost();
        itemsCount--;
    });


    // Objects count input + label

    const countInput = document.createElement("input");
    countInput.type = "text";
    countInput.id = "count-input"
    countInput.classList.add("form-control", "mb-3");
    countInput.addEventListener("input", function() {
        setOrderCost();
    });

    const inputLabel = document.createElement("label");
    inputLabel.classList.add("form-label");
    inputLabel.setAttribute("for", countInput.id);
    inputLabel.innerHTML = "Количество";
    
    objectAndCategoriesDiv.appendChild(serviceObjectsSelect);
    objectAndCategoriesDiv.appendChild(objectCostInputLabel);
    objectAndCategoriesDiv.appendChild(objectCostInput);
    objectAndCategoriesDiv.appendChild(objectCategoriesDiv);
    newItemDiv.appendChild(objectAndCategoriesDiv);
    newItemDiv.appendChild(inputLabel);
    newItemDiv.appendChild(countInput);
    newItemDiv.appendChild(removeButton);
    allItemsDiv.appendChild(newItemDiv);
}

function setOrderCost() {
    let sum = 0;
    let serviceCost = parseFloat(document.getElementById("serviceCost").value);
    const orderPriceDisplay = document.getElementById("totalPrice");
    const serviceObjectsItems = Array.from(document.getElementsByClassName("service-object-item"));

    serviceObjectsItems.forEach(serviceObjectsItem => {
        let objectWithServicesCost = 0;
        let objectsCount = parseFloat(serviceObjectsItem.querySelector("#count-input").value);
        let objectCost = parseFloat(serviceObjectsItem.querySelector("#object-cost").value);
        objectWithServicesCost += objectCost
        const serviceObjectItems = serviceObjectsItem.querySelectorAll(".service-object-category");
        serviceObjectItems.forEach(serviceObjectItem => {
            const categoryCostInput = serviceObjectItem.getElementsByTagName("input")[0];
            let categoryCost = parseFloat(categoryCostInput.value);
            objectWithServicesCost += categoryCost;
        })
        sum += objectWithServicesCost * objectsCount;
    })
    if (!isNaN(sum)) {
        orderPriceDisplay.value = Math.round((sum + serviceCost) * 100) / 100;
    }
    else {
        orderPriceDisplay.value = serviceCost;
    }
}

function collectAllObjectsData() {
    const serviceObjectsItems = Array.from(document.getElementsByClassName("service-object-item"));
    // let objectData = {
    //     "object_id": 1,
    //     "object_categories":
    // }
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("add_service_object_but").addEventListener("click", addNewServiceObjectItem);
    setOrderCost();
})

