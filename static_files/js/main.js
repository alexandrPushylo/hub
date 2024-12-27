console.log('OK')function submitEditBill() {
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