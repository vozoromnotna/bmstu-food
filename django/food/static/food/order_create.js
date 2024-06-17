import DishFactory from "./DishFactory.js";

const dishesContainer = document.querySelector("#dish-container");
const ordersContainer = document.querySelector("#order-container");
const totalPriceNode = document.querySelector("#total-price");
const factory = new DishFactory();

document.dishes.sort(compareDishes)

document.orders = [];

render();
updateTotalPrice();

function compareDishes(a, b){
    return a.name.toUpperCase() < b.name.toUpperCase() ? -1 : 1 
}

function render(){
    dishesContainer.innerHTML = "";
    ordersContainer.innerHTML = "";

    document.dishes.sort(compareDishes);

    document.dishes.forEach(dish => {
        addToDishesContainer(dish);
    });

    document.orders.forEach(order => {
        addToOrdersContainer(order.dish, order.count);
    })

    updateTotalPrice();
}

function addToOrder(dish){
   document.dishes = document.dishes.filter(item => item !== dish);
   document.orders.push({dish: dish, count: 1});
   render();
}
 
function removeFromOrder(dish){
    document.orders = document.orders.filter(item => item.dish !== dish);
    document.dishes.push(dish);
    render();
}

function addToDishesContainer(dish){
    let dishCard = factory.createDishCard(dish, false);
    dishesContainer.append(dishCard);
    dishCard.querySelector("#card-button").onclick = _ => addToOrder(dish);
    dishCard.querySelector("#card-button").onclick = _ => addToOrder(dish);
    
}

function removeFromDishesContainer(dish){
    let dishNode = document.querySelector(`#${dish.name}`);
    dishesContainer.removeChild(dishNode);

}

function addToOrdersContainer(dish, count){
    let orderCard = factory.createDishCard(dish, true, count);
    ordersContainer.append(orderCard);
    orderCard.querySelector("#card-button").onclick = _ => removeFromOrder(dish);
    let input = orderCard.querySelector("#card-input");

    input.addEventListener("input", _ => {
        let order = document.orders.find(item => item.dish = dish)
        order.count = input.value;

        let totalPrice = orderCard.querySelector("#card-total-price");
        totalPrice.parentNode.replaceChild(factory.getNewTotalPrice(dish, input.value), totalPrice);

        updateTotalPrice();
    });
}

function removeFromOrdersContainer(dish){
    let orderNode = document.querySelector(`#${dish.name}`);
    ordersContainer.removeChild(orderNode);
}

function updateTotalPrice(){
    let totalPrice = 0;
    if (document.orders){
        totalPrice = document.orders.reduce((sum, order)=> sum += order.dish.price * order.count, 0);
        totalPriceNode.innerHTML = "";
    }
    totalPriceNode.textContent = `Итог: ${totalPrice} р.`;
}

