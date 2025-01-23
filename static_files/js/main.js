console.log('OK')


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




function submitEditBill() {
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

function calculateColdWaterV(e){
    const el_id = e.id
    const prev_cold_water_indications = parseInt($('#prev_cold_water_indications').val());
    const cold_water_indications = $('#cold_water_indications');
    const cold_water_volume = $('#cold_water_volume');

    if (el_id === "cold_water_indications"){
        cold_water_volume.val(cold_water_indications.val() - prev_cold_water_indications)
    }
    if (el_id === "cold_water_volume"){
        cold_water_indications.val(prev_cold_water_indications+parseInt(cold_water_volume.val()))
    }
}
function calculateHotWaterV(e){
    const el_id = e.id
    const prev_hot_water_indications = parseInt($('#prev_hot_water_indications').val());
    const hot_water_indications = $('#hot_water_indications');
    const hot_water_volume = $('#hot_water_volume');

    if (el_id === "hot_water_indications"){
        hot_water_volume.val(hot_water_indications.val() - prev_hot_water_indications)
    }
    if (el_id === "hot_water_volume"){
        hot_water_indications.val(prev_hot_water_indications+parseInt(hot_water_volume.val()))
    }
}



function setTodayToPayment_date(){
    $('#payment_date').val($('#today_field').val());
}