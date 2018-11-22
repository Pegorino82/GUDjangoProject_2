const showBasket = ({image, name, now_price, quantity, id, totalPrice}) => (
    `
    <div class="product-line" id="${id}">
        <img class="product-small-photo" src="${image}" alt="${name}">
        <div class="product-info name">
            ${name}
        </div>
        <div class="product-info price">
            ${now_price}
        </div>
        <button class="add_one" onclick="addOne(${id})">+</button>
        <button class="remove_one" onclick="removeOne(${id})">-</button>
        <span class="quantity">
            ${quantity}
        </span>
        <span class="total_price">
            ${totalPrice}
        </span>
    </div>
    <hr>
    `
);


const listApiUrl = 'http://127.0.0.1:8000/api/basket/list/';
const detailApiUrl = 'http://127.0.0.1:8000/api/basket/detail/?id=';
const updateApiUrl = 'http://127.0.0.1:8000/api/basket/update/';
const productApiUrl = 'http://127.0.0.1:8000/api/products/detail/';

function getJson(apiUrl) {
    let HttpReq = new XMLHttpRequest(); // a new request
    HttpReq.open("GET", apiUrl, false);
    HttpReq.send(null);
    console.log(JSON.parse(HttpReq.responseText));
    return JSON.parse(HttpReq.responseText);
}

function updateRequest(updateApiUrl, params) {
    let HttpReq = new XMLHttpRequest(); // a new request
    HttpReq.open("GET", updateApiUrl + '?' + params, false);
    HttpReq.send(null);
}

function renderBasketItem(detailApiUrl, id) {
    let currentBasketItem = getJson(detailApiUrl + id).results;
    let productId = currentBasketItem.product_id;
    let product = getJson(productApiUrl + productId + '/').results;
    product['quantity'] = currentBasketItem.quantity;
    product['id'] = id;
    product['totalPrice'] = currentBasketItem.quantity * product.now_price;
    let basketItem = showBasket(
        {
            image: product.image,
            name: product.name + 'hmm..',
            now_price: product.now_price,
            quantity: product.quantity,
            id: product.id,
            totalPrice: product.totalPrice
        }
    );
    currentBasketItem.innerHTML = '';
    currentBasketItem.innerHTML = basketItem;
    console.log(currentBasketItem.innerHTML);
}

function renderBasket(apiUrl) {
    let gotJson = getJson(apiUrl);
    let basketData = gotJson.results;
    let getBasket = [];
    basketData.forEach(function (item) {
        let product = getJson(productApiUrl + item.product_id + '/').results;
        product['quantity'] = item.quantity;
        product['id'] = item.id;
        product['totalPrice'] = item.quantity * product.now_price;
        getBasket.push(product);
    });
    let basketItems = getBasket.map(showBasket).join('');
    let basketHtml = document.getElementById('basket_js');
    basketHtml.innerHTML = '';
    basketHtml.innerHTML += basketItems;

}

renderBasket(listApiUrl);


function addOne(id) {
    let currBasketItem = document.getElementById(id);
    let htmlQuantity = currBasketItem.getElementsByClassName('quantity')[0];
    let currQuantity = parseInt(htmlQuantity.textContent);
    currQuantity = currQuantity + 1;
    htmlQuantity.innerHTML = '';
    htmlQuantity.innerHTML = currQuantity;

    let params = 'id=' + id + '&quantity=' + currQuantity;
    updateRequest(updateApiUrl, params);
    // renderBasketItem(detailApiUrl, id);
    renderBasket(listApiUrl);
}

function removeOne(id) {
    let currBasketItem = document.getElementById(id);
    let htmlQuantity = currBasketItem.getElementsByClassName('quantity')[0];
    let currQuantity = parseInt(htmlQuantity.textContent);
    if (currQuantity > 0) {
        currQuantity = currQuantity - 1;
        htmlQuantity.innerHTML = '';
        htmlQuantity.innerHTML = currQuantity;
    }
    let params = 'id=' + id + '&quantity=' + currQuantity;
    updateRequest(updateApiUrl, params);
    // renderBasketItem(detailApiUrl, id);
    renderBasket(listApiUrl);
}