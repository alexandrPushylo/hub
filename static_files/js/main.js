
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

$('#subscriptions_container').masonry({
// указываем элемент-контейнер в котором расположены блоки для динамической верстки
    itemSelector: '.subscriptions_item',
    columnWidth: 20,
    gutter: 10,
    // fitWidth: false,
    // horizontalOrder: true,
// указываем класс элемента являющегося блоком в нашей сетке
    singleMode: true,
// true - если у вас все блоки одинаковой ширины
    isResizable: false,
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

////////////////////////////////////////////////////////////////
function submitWaterSupplyData() {
    const operation = 'submit_water_supply_data'
    // const app_material_description = $('#app_mat_desc_id_' + application_material_id).val()
    $.ajax({
        type: 'POST',
        mode: 'same-origin',
        url: window.location,
        data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            operation: operation,
            id: $('#water_supply_id').val(),
            payment_date: $('#payment_date').val(),
            payment_month: $('#payment_month').val(),

            cold_water_indications: $('#cold_water_indications').val(),
            hot_water_indications: $('#hot_water_indications').val(),

            water_rate: $('#water_rate').val(),
            water_heating_rate: $('#water_heating_rate').val(),
            cold_water_volume: $('#cold_water_volume').val(),
            hot_water_volume: $('#hot_water_volume').val(),
            total_water_volume: $('#total_water_volume').val(),
            total_water_amount: $('#total_water_amount').val(),
            water_heating_volume: $('#water_heating_volume').val(),
            water_heating_amount: $('#water_heating_amount').val(),
            prev_cold_water_indications: $('#prev_cold_water_indications').val(),
            prev_hot_water_indications: $('#prev_hot_water_indications').val(),
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
    calculateTotalWaterVolume()
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
    calculateTotalWaterVolume()
}

function calculateTotalWaterVolume(){
    const total_water_volume = $('#total_water_volume');
    const cold_water_volume = $('#cold_water_volume').val();
    const hot_water_volume = $('#hot_water_volume').val();
    total_water_volume.val(parseInt(cold_water_volume) + parseInt(hot_water_volume))
    calculateWaterAmount()
}
function calculateWaterAmount(){
    const total_water_amount = $('#total_water_amount');
    const total_water_volume = $('#total_water_volume').val();
    const water_rate = $('#water_rate').val();
    total_water_amount.val(parseInt(total_water_volume) + parseFloat(water_rate))
}
function calculateWaterHeatingAmount(){
    const water_heating_amount = $('#water_heating_amount');
    const water_heating_volume = $('#water_heating_volume').val();
    const water_heating_rate = $('#water_heating_rate').val();
    water_heating_amount.val(parseFloat(water_heating_volume) + parseFloat(water_heating_rate))
}



///////////////////////////////////////////////////////
function setTodayToPayment_date(){
    $('#payment_date').val($('#today_field').val());
}

function submitElectricityData() {
    const operation = 'submit_electricity_data'
    $.ajax({
        type: 'POST',
        mode: 'same-origin',
        url: window.location,
        data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            operation: operation,
            id: $('#electricity_id').val(),
            payment_date: $('#payment_date').val(),
            payment_month: $('#payment_month').val(),

            electricity_indications: $('#electricity_indications').val(),

            electricity_volume: $('#electricity_volume').val(),
            electricity_rate: $('#electricity_rate').val(),
            electricity_amount: $('#electricity_amount').val(),
            prev_indications: $('#prev_indications').val(),

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

function calculateElectricityV(e){
    const el_id = e.id
    const prev_indications = parseInt($('#prev_indications').val());
    const electricity_indications = $('#electricity_indications');
    const electricity_volume = $('#electricity_volume');

    if (el_id === "electricity_indications"){
        electricity_volume.val(electricity_indications.val() - prev_indications)
    }
    if (el_id === "electricity_volume"){
        electricity_indications.val(prev_indications+parseInt(electricity_volume.val()))
    }
    calculateElectricityAmount()
}
function calculateElectricityAmount() {
    const electricity_volume = $('#electricity_volume').val();
    const electricity_rate = $('#electricity_rate').val();
    const electricity_amount = $('#electricity_amount');
    electricity_amount.val(parseInt(electricity_volume) * parseFloat(electricity_rate))
}

function submitRentData() {
    const operation = 'submit_rent_data'
    $.ajax({
        type: 'POST',
        mode: 'same-origin',
        url: window.location,
        data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            operation: operation,
            id: $('#electricity_id').val(),
            payment_date: $('#payment_date').val(),
            payment_month: $('#payment_month').val(),
            rent_amount: $('#rent_amount').val(),
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

function gotoLocation(url){
    window.location.href=url;
}