// для работы с localStorage:
//     создаем объект с ключом storageKey,
//     забираем объект по ключу storageKey,
//     изменяем значение элементов в storageKey на +1 или -1


function addToStorage(storageKey, key, quantity) {
    // получаем элементы хранилища под ключом storageKey
    let sorageItem = getFromStorage(storageKey);
    // создаем объект
    let storageValue = {[key]: quantity};
    // проверяем, есть ли в sorageItem storageValue
    let storageItemValue = sorageItem ? {...sorageItem, ...storageValue} : storageValue;
    // сериализуем объект в json
    let serialValue = JSON.stringify(storageItemValue);
    // сохраняем в хранилище
    localStorage.setItem(storageKey, serialValue);
}

function getFromStorage(storageKey) {
    // получаем всю корзину из хранилища
    let returnedItem = localStorage.getItem(storageKey);
    return returnedItem ? JSON.parse(returnedItem) : {};
}

function incProduct(storageKey, key, quantity = 1) {
    // получаем весь объект хранилища с ключом storageKey (корзина)
    let storageItem = getFromStorage(storageKey);
    // проверяем, что есть в хранилище элемент с ключом key (id продукта)
    // проверяем значение (количество товара)
    if (storageItem[key]) {
        storageItem[key] = storageItem[key];
    }
    // если значения нет (или оно равно 0)
    else {
        storageItem[key] = 0;
    }
    // увеличиваем на 1
    storageItem[key] += quantity;
    return addToStorage(storageKey, key, storageItem[key]);
}

function decProduct(storageKey, key, quantity = 1) {
    // получаем весь объект хранилища с ключом storageKey
    let storageItem = getFromStorage(storageKey);
    // проверяем, что есть в хранилище элемент с ключом key (id продукта)
    // в т.ч. не равен 0
    if (storageItem[key]) {
        storageItem[key] -= quantity;
    }
    return addToStorage(storageKey, key, storageItem[key]);
}

