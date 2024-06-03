function createInputWithLabel(
    inputId,
    inputClasses = [],
    inputType = "text",
    inputValue = 0,
    inputReadOnly = false,
    labelClasses = [],
    labelText
) {
    const newInput = document.createElement("input")
    newInput.readOnly = inputReadOnly
    newInput.id = inputId
    newInput.type = inputType
    newInput.value = inputValue;
    for (let cls of inputClasses) {
        newInput.classList.add(cls)
    }

    const newLabel = document.createElement("label")
    for (let cls of labelClasses) {
        newLabel.classList.add(cls)
    }
    newLabel.setAttribute("for", newInput.id)
    newLabel.innerHTML = labelText

    return [newInput, newLabel]
}

function createSelectWithLabel(
    selectId,
    selectClasses = [],
    selectInnerHtml = "",
    selectElements,
    selectSelectedId,
    labelClasses = [],
    labelText
) {

    const newSelect = document.createElement("select");
    newSelect.id = selectId;
    for (let cls of selectClasses) {
        newSelect.classList.add(cls);
    }
    newSelect.innerHTML = selectInnerHtml
    selectElements.forEach(element => {
        const option = document.createElement("option");
        if (element.id == selectSelectedId) {
            option.selected = true;
        }
        option.value = element.id;
        option.textContent = element.name;
        option.setAttribute("cost", element.cost);
        newSelect.appendChild(option);
    });

    const newLabel = document.createElement("label")
    for (let cls of labelClasses) {
        newLabel.classList.add(cls)
    }
    newLabel.setAttribute("for", newSelect.id)
    newLabel.innerHTML = labelText

    return [newSelect, newLabel];
}

async function initFillObjectCategoriesDiv(object_info, catsDiv, costDisplayInput, objectCost) {
    catsDiv.innerHTML = "";
    await fetch(`/get_object_categories/${object_info.object}`)
    .then(response => response.json())
    .then((data) => {
        const objectCategories = data["object_categories"];
        const categoriesSubcats = data["category_subcategories"];

        for (let i = 0; i < objectCategories.length; i++) {
            const categoryDiv = document.createElement("div");
            categoryDiv.classList.add("service-object-category");
            
            
            // Category cost input + label
            const [categoryCostInput, categoryCostInputLabel] = createInputWithLabel(
                "category-cost", ["form-control", "mb-3"], "text", 0, true, ["form-label"], "Стоимость категории"
            )
            
            // Category select + label
            const [categorySelect, categorySelectLabel] = createSelectWithLabel(
                objectCategories[i].id, ["form-control"], 
                '<option value="" cost="0">Не выбрано</option>',
                categoriesSubcats[i], object_info.subcats[i], ["form-label"], objectCategories[i].name
            )

            categorySelect.addEventListener("change", function() {
                if (categorySelect.options[categorySelect.selectedIndex]) {
                    categoryCostInput.value = categorySelect.options[categorySelect.selectedIndex].getAttribute("cost");
                    setOrderCost();
                }
            })
            
            categoryDiv.appendChild(categorySelectLabel);
            categoryDiv.appendChild(categorySelect);
            categoryDiv.appendChild(categoryCostInputLabel);
            categoryDiv.appendChild(categoryCostInput);
            
            catsDiv.appendChild(categoryDiv);
            
            categorySelect.dispatchEvent(new Event('change'));
        }
        costDisplayInput.value = objectCost;
        setOrderCost();
    });
}

async function createObjectItem(object_info) {
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
        serviceObjectsSelect.id = "objectsList";
        data.forEach(element => {
            const option = document.createElement("option");
            option.value = element.id;
            if (element.id == object_info.object) {
                option.selected = true;
            }
            option.setAttribute("cost", element.cost);
            option.textContent = element.name;
            serviceObjectsSelect.appendChild(option);
        });
    });

    // Object cost input
    const [objectCostInput, objectCostInputLabel] = createInputWithLabel(
        "object-cost", ["form-control", "mb-3"], "text", 0, true, ["form-label"], "Стоимость услуги"
    )

    serviceObjectsSelect.addEventListener("change", function() {
        if (serviceObjectsSelect.options[serviceObjectsSelect.selectedIndex]) {
            initFillObjectCategoriesDiv(
                object_info, 
                objectCategoriesDiv, 
                objectCostInput, 
                serviceObjectsSelect.options[serviceObjectsSelect.selectedIndex].getAttribute("cost")); 
        }
    });

    // Objects count input + label
    const [countInput, countInputLabel] = createInputWithLabel(
        "objectsCount", ["form-control", "mb-3"], "text", 1, false, ["form-label"], "Количество"
    )
    countInput.addEventListener("input", function() {
        setOrderCost();
    });

    // Remove button
    const removeButton = document.createElement("button");
    removeButton.classList.add("btn", "btn-danger", "mb-3");
    removeButton.type = "button";
    removeButton.innerHTML = "Удалить";
    removeButton.addEventListener("click", () => { 
        newItemDiv.remove(); 
        setOrderCost();
    });

    objectAndCategoriesDiv.appendChild(serviceObjectsSelect);
    objectAndCategoriesDiv.appendChild(objectCostInputLabel);
    objectAndCategoriesDiv.appendChild(objectCostInput);
    objectAndCategoriesDiv.appendChild(objectCategoriesDiv);
    newItemDiv.appendChild(objectAndCategoriesDiv);
    newItemDiv.appendChild(countInputLabel);
    newItemDiv.appendChild(countInput);
    newItemDiv.appendChild(removeButton);
    allItemsDiv.appendChild(newItemDiv);

    serviceObjectsSelect.dispatchEvent(new Event("change"));
}

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
            
            
            // Category cost input + label
            const [categoryCostInput, categoryCostInputLabel] = createInputWithLabel(
                "category-cost", ["form-control", "mb-3"], "text", 0, true, ["form-label"], "Стоимость категории"
            )
            
            // Category select + label
            const [categorySelect, categorySelectLabel] = createSelectWithLabel(
                objectCategories[i].id, ["form-control"], 
                '<option value="" cost="0">Не выбрано</option>',
                categoriesSubcats[i], undefined, ["form-label"], objectCategories[i].name
            )

            categorySelect.addEventListener("change", function() {
                if (categorySelect.options[categorySelect.selectedIndex]) {
                    categoryCostInput.value = categorySelect.options[categorySelect.selectedIndex].getAttribute("cost");
                    setOrderCost();
                }
            })
            categorySelect.dispatchEvent(new Event('change'));

            categoryDiv.appendChild(categorySelectLabel);
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
        serviceObjectsSelect.id = "objectsList";
        data.forEach(element => {
            const option = document.createElement("option");
            option.value = element.id;
            option.setAttribute("cost", element.cost);
            option.textContent = element.name;
            serviceObjectsSelect.appendChild(option);
        });
    });
    
    serviceObjectsSelect.addEventListener("change", function() {
        if (serviceObjectsSelect.options[serviceObjectsSelect.selectedIndex]) {
            fillObjectCategoriesDiv(serviceObjectsSelect.options[serviceObjectsSelect.selectedIndex].value, objectCategoriesDiv, objectCostInput, serviceObjectsSelect.options[serviceObjectsSelect.selectedIndex].getAttribute("cost")); 
        }
    });

    // Object cost input
    const [objectCostInput, objectCostInputLabel] = createInputWithLabel(
        "object-cost", ["form-control", "mb-3"], "text", 0, true, ["form-label"], "Стоимость услуги"
    )

    // Remove button
    const removeButton = document.createElement("button");
    removeButton.classList.add("btn", "btn-danger", "mb-3");
    removeButton.type = "button";
    removeButton.innerHTML = "Удалить";
    removeButton.addEventListener("click", () => { 
        newItemDiv.remove(); 
        setOrderCost();
    });

    // Objects count input + label

    const [countInput, countInputLabel] = createInputWithLabel(
        "objectsCount", ["form-control", "mb-3"], "text", 1, false, ["form-label"], "Количество"
    )
    countInput.addEventListener("input", function() {
        setOrderCost();
    });
    
    objectAndCategoriesDiv.appendChild(serviceObjectsSelect);
    objectAndCategoriesDiv.appendChild(objectCostInputLabel);
    objectAndCategoriesDiv.appendChild(objectCostInput);
    objectAndCategoriesDiv.appendChild(objectCategoriesDiv);
    newItemDiv.appendChild(objectAndCategoriesDiv);
    newItemDiv.appendChild(countInputLabel);
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
        let objectsCount = parseFloat(serviceObjectsItem.querySelector("#objectsCount").value);
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

function displayMessage(message, category) {
    const messageContainer = document.getElementById("messagesDivContainer")
    messageContainer.innerHTML += 
    `<div class="alert alert-${category} alert-dismissible fade show" role="alert">
    ${message}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>`
          
}

function collectAllObjectsData() {
    const serviceObjectsItems = Array.from(document.getElementsByClassName("service-object-item"));
    const statusSelect = document.getElementById("statusIdSelect")

    let orderInfo = {
        clientId: parseInt(document.getElementById("clientId").innerText),
        serviceId: parseInt(document.getElementById("serviceId").innerText),
        statusId: parseInt(statusSelect.options[statusSelect.selectedIndex].value),
        deliveryDate: document.getElementById("deliveryDate").value,
        objects: []
    }

    console.log(orderInfo.deliveryDate);

    // const orderedObjectsList = [];
    serviceObjectsItems.forEach(serviceObjectsItem => {
        orderInfo.objects.push({
            objectId: parseInt(serviceObjectsItem.querySelector("#objectsList").value),
            objectAmount: serviceObjectsItem.querySelector("#objectsCount").value,
            objectCategories: getCatsListFromObjectItem(serviceObjectsItem),
            objectSubCategories: getSubCatsListFromObjectItem(serviceObjectsItem),
        })
    })
    return orderInfo;
}

function getCatsListFromObjectItem(objectItem) {
    const categoryDivs = objectItem.querySelectorAll(".service-object-category");
    const categorysList = [];
    categoryDivs.forEach(catDiv => {
        categorysList.push(parseInt(catDiv.getElementsByTagName("select")[0].id));
    })

    return categorysList;
}

function getSubCatsListFromObjectItem(objectItem) {
    const subCategoryDivs = objectItem.querySelectorAll(".service-object-category");
    const subCategorysList = [];
    subCategoryDivs.forEach(catDiv => {
        const subcatSelect = catDiv.getElementsByTagName("select")[0];
            subcatId = parseInt(subcatSelect.options[subcatSelect.selectedIndex].value);
            if (isNaN(subcatId)) {
                subCategorysList.push(undefined);
            }
            else {
                subCategorysList.push(subcatId);
            }
    })

    return subCategorysList;
}

function updateOrderData(sendingStatus) {
    let requestId = document.getElementById("orderId").innerText;

    fetch(`/update_order/${requestId}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            orderInfo: collectAllObjectsData(), 
            status: sendingStatus
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            displayMessage(data.message, data.status);
        }
        if (data.url) {
            document.location.href = data.url;
        }
    })
}


function loadOrderData() {
    let orderId = document.getElementById("orderId").innerText
    fetch(`/get_order_info/${orderId}`)
    .then(response => response.json())
    .then((data) => {
        data.forEach((object_info) => {
            createObjectItem(object_info);
        })
    })
}


document.addEventListener('DOMContentLoaded', () => {
    loadOrderData();
    document.getElementById("add_service_object_but").addEventListener("click", addNewServiceObjectItem);

    document.getElementById("update_order").addEventListener("click", function() {
        updateOrderData("update_data")
    })
});