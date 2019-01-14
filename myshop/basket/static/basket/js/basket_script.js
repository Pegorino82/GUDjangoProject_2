const Basket = (data) => (
    `
        В корзине<br>
        ${data.widget_data.items} товаров<br>
        ${data.widget_data.total_cost}
       `
);

const emptyBasket = (data) => (
    `
        Ваша<br>
        корзина<br>
        пуста
       `
);


window.onload = function () {
    // добавляем ajax-обработчик для увеличения товара
    if($("button").is("#add_product")){
    $('.basket_list').on('click', 'button[id="add_product"]', function (event) {
        // console.log(event);
        var target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/basket/add_product_ajax/" + target_href.name + "/",
                success: function (data) {
                    $('.basket_list').html(data.result);
                    // console.log('ajax done');

                    $.ajax({
                        url: "/api/basket/list",
                        success: function (data) {
                            console.log(data.widget_data);
                            $('.basket__control').html(Basket(data));
                        }
                    })

                },
            });
        }
        event.preventDefault();
    });}


    if($("button").is("#add_product")){
    $('.products_table').on('click', 'button[id="add_product"]', function (event) {
        console.log(event);
        var target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/basket/add_product_ajax/" + target_href.name + "/",
                success: function (data) {
                    $('.basket_list').html(data.result);
                    // console.log('ajax done');

                    $.ajax({
                        url: "/api/basket/list",
                        success: function (data) {
                            console.log(data.widget_data);
                            $('.basket__control').html(Basket(data));
                        }
                    })

                },
            });
        }
        event.preventDefault();
    });}


    if($("button").is("#rem_product")){
    // добавляем ajax-обработчик для уменьшения товара
    $('.basket_list').on('click', 'button[id="rem_product"]', function (event) {
        // console.log(event);
        var target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/basket/remove_product_ajax/" + target_href.name + "/",
                success: function (data) {
                    $('.basket_list').html(data.result);
                    // console.log('ajax done');

                    $.ajax({
                        url: "/api/basket/list",
                        success: function (data) {
                            console.log(data.widget_data);
                            $('.basket__control').html(Basket(data));
                        }
                    })

                },
            });
        }
        event.preventDefault();
    });}

    if($("button").is("#del_product")){
    // добавляем ajax-обработчик для удаления товара
    $('.basket_list').on('click', 'button[id="del_product"]', function (event) {
        // console.log(event);
        var target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/basket/delete_product_ajax/" + target_href.name + "/",
                success: function (data) {
                    $('.basket_list').html(data.result);
                    // console.log('ajax done');

                    $.ajax({
                        url: "/api/basket/list",
                        success: function (data) {
                            console.log(data.widget_data);
                            $('.basket__control').html(Basket(data));
                        }
                    })

                },
            });


        }
        event.preventDefault();
    });}

    $.ajax({
        url: "/api/basket/list",
        success: function (data) {
            // console.log(data.widget_data);
            if(data.widget_data.items > 0) {
                $('.basket__control').html(Basket(data));
            }
            else {
                $('.basket__control').html(emptyBasket(data));
            }

            // console.log($('.basket__control'));
        }
    })

};

