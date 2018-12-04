const showProducts = ({product_marker, image, name, currency, now_price, old_price}) => (
    `
    <div class="col-md-4 col-sm-6 col-xs-12 product_cell">
        <div class="product_card ${product_marker}">
            <img class="product_img" src="${image}" alt="">
            <div class="name_price">
                <div class="product_name">
                    ${name}
                </div>
                <div class="product_price">
                    <div class="now_price">
                        ${currency} ${now_price}
                    </div>
                    <div class="old_price">
                        ${currency} ${old_price}
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
);

const iniApiUrl = 'http://127.0.0.1:8000/api/products/list';

// const iniApiUrl = 'http://127.0.0.1:8000/framework_api/products/';  //for rest_framework

function getJson(apiUrl) {
    let HttpReq = new XMLHttpRequest(); // a new request
    HttpReq.open("GET", apiUrl, false);
    HttpReq.send(null);
    console.log(JSON.parse(HttpReq.responseText));
    return JSON.parse(HttpReq.responseText);
}


function tableProducts(apiUrl) {
// получаем json
    let gotJson = getJson(apiUrl);
    console.log('получил json', gotJson);
    console.log(document.location.href);
// рендерим категории на странице (по три)
    let productItems = gotJson.results.map(showProducts).join('');
    // console.log(productItems);
    let getProduct = document.getElementById('cat_js');
    getProduct.innerHTML = '';
    getProduct.innerHTML += productItems;
// показываем номер текущей страницы
    let page = gotJson.page;
    let pages = gotJson.pages_all;
    // let pages = Math.floor(gotJson.count / 3);  //for rest_framework
    console.log('текущая страница:', page);
    let pageHtml = document.getElementById('current_page');
    pageHtml.innerHTML = page + '/' + pages;

    prevNextLinks(gotJson, page)
}

tableProducts(iniApiUrl);

function prevNextLinks(gotJson, page) {
    let prevUrl = gotJson.previous_url;
    let nextUrl = gotJson.next_url;
    console.log('>>>>>>>', prevUrl, nextUrl);
    let prevPage = document.getElementById('previous_page');
    // let prevPage = document.getElementById('previous'); //for rest_framework
    let nextPage = document.getElementById('next_page');
    // let nextPage = document.getElementById('next'); //for rest_framework
    prevPage.href = '';
    nextPage.href = '';
    if (prevUrl) {
        let neededApiUrl = `${iniApiUrl}/?page=${page - 1}`;
        console.log('предыдущий api', prevUrl);
        prevPage.setAttribute('onclick', `tableProducts('${neededApiUrl}')`);
    }
    else {
        prevPage.setAttribute('onclick', 'return false');
    }

    if (nextUrl) {
        let neededApiUrl = `${iniApiUrl}/?page=${page + 1}`;
        console.log('следующий api', nextUrl);
        nextPage.setAttribute('onclick', `tableProducts('${neededApiUrl}')`);
    }
    else {
        nextPage.setAttribute('onclick', 'return false');
    }
}