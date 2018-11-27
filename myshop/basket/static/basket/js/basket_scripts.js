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

//**************************************

const Basket = ({basket_total, basket_len, basket_currency}) =>
    (
        `
        В корзине<br>
        ${basket_len} товаров<br>
        ${basket_total} ${basket_currency}
       `
    )


function renderBasketWidget(listApiUrl) {
    let basketItems = getJson(listApiUrl).results;
    console.log(basketItems);

    let basket_total = 0;
    let basket_len = 0;
    let basket_currency = null;

    basketItems.forEach(function (item) {
        let product = getJson(productApiUrl + item.product_id + '/').results;
        basket_total += item.quantity * product.now_price;
        basket_len += 1;
        basket_currency = product.currency;
    });

    console.log(basket_total, basket_len, basket_currency);

    basketHtml = document.getElementsByClassName('basket__control')[0];
    basketLinkHtml = document.getElementsByClassName('basket')[0];
    basketLinkHtml.style.display = 'block';
    basketHtml.innerHTML = '';
    basketHtml.innerHTML = Basket(
        {
            basket_total: basket_total,
            basket_len: basket_len,
            basket_currency: basket_currency,
        }
    )
};

renderBasketWidget(listApiUrl)
//**************************************

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
    console.log('basket-->', getBasket)
    let basketItems = getBasket.map(showBasket).join('');
    let basketHtml = document.getElementById('basket_js');
    basketHtml.innerHTML = '';
    basketHtml.innerHTML += basketItems;
    renderBasketWidget(apiUrl)

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
    renderBasketWidget(listApiUrl);
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
    renderBasketWidget(listApiUrl);
};

