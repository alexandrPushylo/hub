console.log('OK')function submitEditBill() {
$('#div-body').masonry({
// указываем элемент-контейнер в котором расположены блоки для динамической верстки
    itemSelector: '.application_items',
    // columnWidth: 20,
    // gutter: 10,
    // fitWidth: false,
    // horizontalOrder: true,
// указываем класс элемента являющегося блоком в нашей сетке
    singleMode: true,
// true - если у вас все блоки одинаковой ширины
    isResizable: true,
// перестраивает блоки при изменении размеров окна
    isAnimated: true,
// анимируем перестроение блоков
    animationOptions: {
        queue: false,
        duration: 500
    }
// опции анимации - очередь и продолжительность анимации
});

function goToEditBill(typeBill) {
    window.location.href = typeBill
}

function clickBillsCard(element){
    const billsCardBody = $('.'+element);
    const billsCardButtons = $('.'+element+'-buttons-control');
    // billsCardBody.css('filter', 'blur(3px)')
    billsCardBody.blur()
    billsCardButtons.fadeToggle(100)
}
    const operation = 'submit_edit_bill'
    // const app_material_description = $('#app_mat_desc_id_' + application_material_id).val()
    $.ajax({
        type: 'POST',
        mode: 'same-origin',
        url: window.location,
        data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            operation: operation,
            payment_date: $('#payment_date').val(),
            rate: $('#rate').val(),
            indications: $('#indications').val(),
            amount: $('#amount').val(),
            description: $('#description').val(),
        },
        success: (response) => {
            if (response === 'ok') {
                window.location.href = '/dashboard'
            }
            if (response === 'error') {
                alert('Error')
            }
        },
    })
}