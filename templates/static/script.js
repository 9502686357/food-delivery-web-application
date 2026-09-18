function addToCart(name, price) {

    let cart = JSON.parse(
        localStorage.getItem("cart")
    ) || [];

    cart.push({
        name: name,
        price: price
    });

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

    alert(name + " added to cart.");
}


function displayCart() {

    let cart = JSON.parse(
        localStorage.getItem("cart")
    ) || [];

    let container =
        document.getElementById("cart-items");

    let total = 0;

    cart.forEach(function(item) {

        let element =
            document.createElement("p");

        element.innerText =
            item.name + " - ₹" + item.price;

        container.appendChild(element);

        total += Number(item.price);
    });

    document.getElementById(
        "cart-total"
    ).innerText = total;
}
