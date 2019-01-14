window.onload = function () {
    let TOTAL_FORMS = parseInt($('input[name="items-TOTAL_FORMS"]').val());
     // console.log(TOTAL_FORMS);
    let totalCost = [];
    let prodNames = [];
    let listQuantity = [];
    let listPrice = [];
    for (let i=0; i < TOTAL_FORMS; i++) {
        product = parseFloat($('select[name="items-' + i + '-product"]').val());
        $.ajax({
            url: "/api/products/detail/" + product + "/",
            success: function (data) {
                listPrice[i] = parseFloat(data.results.now_price).toFixed(2);
                listQuantity[i] = parseInt(data.results.quantity);
                prodNames[i] = data.results.name;
                let _cost = parseFloat($('input[name="items-' + i + '-price"]').val()).toFixed(2);
                totalCost[i] = _cost;
            }
        });
    }

    for (let i=0; i < TOTAL_FORMS; i++) {

        let neededQuantity = "items-" + i + "-quantity";
        $('.table').on('change', 'input[name=' + neededQuantity + ']', function (event) {
            let quantity = parseInt($('input[name="items-' + i + '-quantity"]').val());
            // console.log(quantity, listQuantity[i]);
            if (quantity < listQuantity[i]) {
                let totPrice = parseFloat(listPrice[i] * quantity).toFixed(2);
                $('#id_items-' + i + '-price').val(totPrice);
            }
            else {
                $('#id_items-' + i + '-quantity').val(listQuantity[i]);
                alert('Max items of ' + prodNames[i] + ' to order: ' + listQuantity[i])
            };

            totalCost[i] = listPrice[i] * parseInt($('input[name="items-' + i + '-quantity"]').val());
            console.log(totalCost);
            let total = 0;
            for (let i = 0; i < totalCost.length; i++) {
                total += totalCost[i] << 0;
            };

            $('#total_cost').html(parseFloat(total).toFixed(2));

        });
    };


};
