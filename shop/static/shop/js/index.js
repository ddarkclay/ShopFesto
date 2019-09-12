//Find out the cart items in localStorage
if (localStorage.getItem('cart') == null) {
    var cart = {};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
    document.getElementById('cart').innerHTML = Object.keys(cart).length;
    updateCart(cart)
}

// if the add to cart button clicked add/increment the item
// $('.cart').click(function() {
$('.divpr').on('click', 'button.cart', function() {
    var idstr = this.id.toString();
    if (cart[idstr] != undefined) {
        qty = cart[idstr][0] + 1;
    } else {
        qty = 1;
        name = document.getElementById('name' + idstr).innerHTML;
        price = document.getElementById('price' + idstr).innerHTML;
        cart[idstr] = [qty, name, parseInt(price)];
    }
    updateCart(cart);
});


function updateCart(cart) {
    var sum = 0;
    for (var item in cart) {
        sum = sum + cart[item][0];
        document.getElementById('div' + item).innerHTML = "<button id='minus" + item + "' class='flex-c-m sizefull bg1 bo-rad-23 hov1 s-text1 py-2 mx-4 my-1 minus'><i class='fas fa-minus'></i></button><span id='val" + item + "'' style='padding-top: 7px'><h5 style='color:#111111;'>" + cart[item][0] + "</h4></span><button id='plus" + item + "' class='flex-c-m sizefull bg1 bo-rad-23 hov1 s-text1 py-2 mx-4 my-1 plus'> <i class='fas fa-plus'> </button>";
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart').innerHTML = sum;
    localStorage.setItem('cart_mobile', JSON.stringify(cart));
    document.getElementById('cart_mobile').innerHTML = sum;
    updatePopover(cart);
}

updatePopover(cart)

function updatePopover(cart) {
    var popStr = "";
    // popStr = popStr + '<h5>Cart for your Item</h5><br>';
    var i = 1;
    var total_amount = 0;
    for (var item in cart) {
        popStr = popStr + "<span><span'><big><b class='mr-3'>" + i + ".</b></big><span style='color: red;'>";
        item_name = document.getElementById('name' + item).innerHTML.slice(0, 24);
        item_price = document.getElementById('price' + item).innerHTML;
        amount_item = cart[item][0] * item_price;
        popStr = popStr + item_name + " ...</span><br><span class='ml-5'>Qty: " + cart[item][0] + '</span> X ' + item_price + ' = ₹' + amount_item + ' <br><hr style="margin-top:10px;margin-bottom:10px">';
        total_amount = total_amount + amount_item;
        i = i + 1;
    }
    popStr = popStr + "</span>";
    $('#popcart').html(popStr);
    $('#total_amount').html('<h5>Total Amount : ₹' + total_amount + '</h5>');
    $('#popcart_mobile').html(popStr);
    $('#total_amount_mobile').html('<h5>Total Amount : ₹' + total_amount + '</h5>');
}

$('#clear_cart').click(function() {
    clearCart();
    $('#popcart').html('<h6>Your Cart is Empty .<p>Please Add Some Item</p>');
});

$('#clear_cart_mobile').click(function() {
    clearCart();
    $('#popcart_mobile').html('<h6>Your Cart is Empty .<p>Please Add Some Item</p>');
});

function clearCart() {
    cart = JSON.parse(localStorage.getItem('cart'));
    for (var item in cart) {
        document.getElementById('div' + item).innerHTML = '<button id="' + item + '" style="width: 150px;" class="flex-c-m sizefull bg1 bo-rad-23 hov1 s-text1 py-2 mx-4 my-2 cart">Add to Cart</button>'
    }
    localStorage.clear();
    cart = {};
    updateCart(cart);
}

// If minus button is clicked, change the cart as well as the display value
$('.divpr').on("click", "button.minus", function() {
    a = this.id.slice(7, );
    cart['pr' + a][0] = cart['pr' + a][0] - 1;
    cart['pr' + a][0] = Math.max(0, cart['pr' + a][0]);
    if (cart['pr' + a][0] == 0) {
        document.getElementById('divpr' + a).innerHTML = '<button id="pr' + a + '" class="flex-c-m sizefull bg1 bo-rad-23 hov1 s-text1 py-2 mx-4 my-2 cart">Add to Cart</button>';
        delete cart['pr' + a];
    } else {
        document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
    }
    updateCart(cart);
});

// If plus button is clicked, change the cart as well as the display value
$('.divpr').on("click", "button.plus", function() {
    a = this.id.slice(6, );
    cart['pr' + a][0] = cart['pr' + a][0] + 1;
    document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
    updateCart(cart);
});