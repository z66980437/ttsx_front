function updateselectall() {
    var flag=true
    $('.selectOne').each(function () {
        if (!this.checked) {
            flag=false
        }
    })
    $('#selectAll').prop('checked', flag)
    if ($('.cart_list_td').length == 0) {
        $('#selectAll').prop('checked', false)
    }
}


function changestatus(goods_id,evt) {
    var goods_status = evt.checked
    console.log(goods_status)
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/cart/change/2/',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': goods_id,'goods_status':goods_status},
        success: function(data){
            if(data.code == '200'){
                changeNumPrise()
            }
        },
        error: function(data){
            console.log(evt.checked)
            if (evt.checked) {
                evt.checked = false
            } else {
                evt.checked = true
            }
            console.log(evt.checked)
            alert('修改商品状态失败')
        }
    })
    updateselectall()
}


//计算商品数量
function goodsNums() {
    var goodsNum = 0
    var goodsTotalPrise = 0
    var $kinds = $('.num_show')
    for (var i = 0; i < $kinds.length; i++) {
        if ($('.selectOne').eq(i).prop('checked')) {
            goodsNum += parseInt($kinds.eq(i)[0].value)
            goodsTotalPrise += parseInt($kinds.eq(i)[0].value) * parseFloat($kinds.eq(i).parent().parent().prev()[0].textContent)
        }
    }
    return [goodsNum, goodsTotalPrise]
}


//修改总件数和总价格
function changeNumPrise() {
    var all = goodsNums()
    $('#totalCount')[0].textContent = all[0]
    $('#totalPrice')[0].textContent = all[1].toFixed(2)
    changeXiaoJi()
}


//修改小计
function changeXiaoJi() {
    $('.cart_list_td .col07').each(function () {
       $(this).text((parseInt($(this).prev().children().children('.num_show').val()) * parseFloat($(this).prev().prev().text())).toFixed(2) + '元')
    })
}


function changenums(goods_id,evt,type){
    var goods_num = parseInt($(evt).parent().children('.num_show').val()) + type;
    if (goods_num>=1 && goods_num<=200) {

    } else {
        goods_num = 1
    }
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/cart/change/1/',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': goods_id, 'goods_num': goods_num},
        success: function(data){
            if(data.code == '200'){
                $(evt).parent().children('.num_show').val(goods_num)
                $(evt).parent().children('.num_show').attr('value', goods_num)
                changeNumPrise()
            }
        },
        error: function(data){
            alert('改变商品数量失败')
        }
    })
}


function removegoods(goods_id,evt) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/cart/change/3/',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': goods_id},
        success: function(data){
            if(data.code == '200'){
                $(evt).parent().parent().remove()
                $('.total_count em')[0].textContent = data.goods_kind
                $('#show_count')[0].textContent = data.goods_kind
                changeNumPrise()
            }
        },
        error: function(data){
            alert('删除商品失败')
        }
    })
    if ($('.cart_list_td').length == 1) {
        $('#selectAll').prop('checked', false)
    }
}


function changeselectall(evt) {
    var goods_status = evt.checked
    console.log(goods_status)
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/cart/change/2/',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': -1,'goods_status':goods_status},
        success: function(data){
            if(data.code == '200'){
                if ($(evt).prop('checked')) {
                    $('.selectOne').each(function() {
                        this.checked = true;
                    });
                } else {
                    $('.selectOne').each(function() {
                        this.checked = false;
                    });
                }
                changeNumPrise()
            }
        },
        error: function(data){
            if (evt.checked) {
                evt.checked = false
            } else {
                evt.checked = true
            }
            alert('修改商品状态失败')
        }
    })
}


changeNumPrise();
updateselectall();