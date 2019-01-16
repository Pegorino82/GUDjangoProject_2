window.onload = function () {
    $.ajax({
        url: "/api/basket/list",
        success: function (data) {
            console.log(data);
        }
    })
};
