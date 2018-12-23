const showCategories = ({name}) =>
    (
        `    
        <div class="col-md-4 col-sm-6 col-xs-12 product_cell">
            <a href="/categories/category/${name}/">
                <div class="product_card">
                    <div class="product_name">
                        ${name}
                    </div>
                </div>
            </a>
        </div>        
        `
    )


const iniApiUrl = '/api/categories/list/?quantity_per_page=3';

function getJson(apiUrl) {
    let HttpReq = new XMLHttpRequest(); // a new request
    HttpReq.open("GET", apiUrl, false);
    HttpReq.send(null);
    // console.log(JSON.parse(HttpReq.responseText));
    return JSON.parse(HttpReq.responseText);
}


function tableCategories(apiUrl) {
// получаем json
    let gotJson = getJson(apiUrl);
    // console.log('получил json', gotJson);
    // console.log(document.location.href);
// рендерим категории на странице (по три)
    let categoryItems = gotJson.results.map(showCategories).join('');
    // console.log(categoryItems);
    let getCategory = document.getElementById('cat_js');
    getCategory.innerHTML = '';
    getCategory.innerHTML += categoryItems;
// показываем номер текущей страницы
    let page = gotJson.page;
    let pages = gotJson.pages_all;
    // console.log('текущая страница:', page);
    let pageHtml = document.getElementById('current_page');
    pageHtml.innerHTML = page + '/' + pages;

    prevNextLinks(gotJson, page)
}

tableCategories(iniApiUrl);


function prevNextLinks(gotJson, page) {
    let prevUrl = gotJson.previous_url;
    let nextUrl = gotJson.next_url;
    // console.log(prevUrl, nextUrl);
    let prevPage = document.getElementById('previous_page');
    let nextPage = document.getElementById('next_page');
    prevPage.href = '';
    nextPage.href = '';
    if (prevUrl) {
        let neededApiUrl = `${iniApiUrl}&page=${page - 1}`;
        // console.log('предыдущий api', prevUrl);
        prevPage.setAttribute('onclick', `tableCategories('${neededApiUrl}')`);
    }
    else {
        prevPage.setAttribute('onclick', 'return false');
    }

    if (nextUrl) {
        let neededApiUrl = `${iniApiUrl}&page=${page + 1}`;
        // console.log('следующий api', nextUrl);
        nextPage.setAttribute('onclick', `tableCategories('${neededApiUrl}')`);
    }
    else {
        nextPage.setAttribute('onclick', 'return false');
    }
}


