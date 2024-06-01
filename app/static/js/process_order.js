document.addEventListener('DOMContentLoaded', (event) => {
    const container = document.getElementById('ordered-objects-container');
    const addButton = document.getElementById('add-object-button');
    // let objectIndex = {{ ordered_objects|length }} + 1;

    // Function to load categories based on selected service object
    const loadCategories = (objectSelect, index) => {
        const objectId = objectSelect.value;
        const categorySelect = document.getElementById(`cat_id_${index}`);
        const subcategorySelect = document.getElementById(`sub_cat_id_${index}`);

        fetch(`/employee/load_categories/${objectId}`)
            .then(response => response.json())
            .then(data => {
                categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
                data.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category.id;
                    option.textContent = category.name;
                    categorySelect.appendChild(option);
                });
                subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';
            });
    };

    // Function to load subcategories based on selected category
    const loadSubcategories = (categorySelect, index) => {
        const categoryId = categorySelect.value;
        const subcategorySelect = document.getElementById(`sub_cat_id_${index}`);
        
        fetch(`/employee/load_subcategories/${categoryId}`)
            .then(response => response.json())
            .then(data => {
                subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';
                data.forEach(subcat => {
                    const option = document.createElement('option');
                    option.value = subcat.id;
                    option.textContent = subcat.name;
                    subcategorySelect.appendChild(option);
                });
            });
    };

    // Attach event listeners to existing service object selects
    document.querySelectorAll('.service-object-select').forEach((select, index) => {
        loadCategories(select, index + 1);
        select.addEventListener('change', () => loadCategories(select, index + 1));
    });

    // Attach event listeners to existing category selects
    document.querySelectorAll('.category-select').forEach((select, index) => {
        select.addEventListener('change', () => loadSubcategories(select, index + 1));
    });

    addButton.addEventListener('click', () => {
        const objectDiv = document.createElement('div');
        objectDiv.classList.add('ordered-object');
        objectDiv.dataset.index = objectIndex;
        
        objectDiv.innerHTML = `
            <div class="form-group">
                <label for="object_id_${objectIndex}">Объект</label>
                <select class="form-control service-object-select" id="object_id_${objectIndex}" name="object_id">
                    <option value="">Выберите объект</option>
                    {% for so in service_objects %}
                    <option value="{{ so.id }}">{{ so.object_name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="cat_id_${objectIndex}">Категория</label>
                <select class="form-control category-select" id="cat_id_${objectIndex}" name="cat_id">
                    <option value="">Выберите категорию</option>
                </select>
            </div>
            <div class="form-group">
                <label for="sub_cat_id_${objectIndex}">Подкатегория</label>
                <select class="form-control subcategory-select" id="sub_cat_id_${objectIndex}" name="sub_cat_id">
                    <option value="">Выберите подкатегорию</option>
                </select>
            </div>
            <div class="form-group">
                <label for="count_${objectIndex}">Количество</label>
                <input type="number" class="form-control" id="count_${objectIndex}" name="count" value="1">
            </div>
            <div class="form-group">
                <label for="price_${objectIndex}">Цена</label>
                <input type="number" class="form-control" id="price_${objectIndex}" name="price" value="0">
            </div>
            <button type="button" class="btn btn-danger remove-object-button">Удалить объект</button>
        `;

        container.appendChild(objectDiv);

        const objectSelect = objectDiv.querySelector('.service-object-select');
        const categorySelect = objectDiv.querySelector('.category-select');
        
        objectSelect.addEventListener('change', () => loadCategories(objectSelect, objectIndex));
        categorySelect.addEventListener('change', () => loadSubcategories(categorySelect, objectIndex));

        objectDiv.querySelector('.remove-object-button').addEventListener('click', () => {
            objectDiv.remove();
        });

        objectIndex++;
    });

    document.querySelectorAll('.remove-object-button').forEach(button => {
        button.addEventListener('click', (event) => {
            button.parentElement.remove();
        });
    });
});