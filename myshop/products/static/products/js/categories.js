const Category = ({name}) =>
    (
        `<li>
            <a href="/categories/category/${name}/">${name}</a>
        </li>`
    );

const renderCategories = res => {
    let menuItems = res.data.results.map(Category).join('');
    // console.log(menuItems);
    // let getMenu = document.getElementsByClassName('submenu');
    let getMenu = document.getElementById('js');
    getMenu.innerHTML = '';
    getMenu.innerHTML += menuItems;
};