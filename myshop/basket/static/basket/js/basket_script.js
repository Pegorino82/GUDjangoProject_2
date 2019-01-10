window.onload = function () {
    // добавляем ajax-обработчик для увеличения товара
    $('.basket_list').on('click', 'button[id="add_product"]', function (event) {
        // console.log(event);
        var target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/basket/add_product_ajax/" + target_href.name + "/",
                success: function (data) {
                    $('.basket_list').html(data.result);
                    // console.log('ajax done');
                },
            });
        }
        event.preventDefault();
    });

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
                },
            });
        }
        event.preventDefault();
    });

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
                },
            });
        }
        event.preventDefault();
    });

};