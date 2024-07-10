import DishFactory from "./DishFactory.js";

const dishesContainer = document.querySelector("#dish-container");
const ordersContainer = document.querySelector("#order-container");
const totalPriceNode = document.querySelector("#total-price");
const createOrderBtn = document.querySelector("#create-order");
const usernameInput = document.querySelector("#usernameInput");
const factory = new DishFactory();

createOrderBtn.onclick = postOrder;

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
        let order = document.orders.find(item => item.dish == dish)
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

async function postOrder(){
    clearError(usernameInput);
    clearError(createOrderBtn);

    if (usernameInput.value == ""){
        addError(usernameInput, "Введите логин заказщика");
        return;
    }

    if (document.orders.length == 0){
        addError(createOrderBtn, "В заказе нет позиций");
        return;
    }
    let resp = await fetch('', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify( {
            username: usernameInput.value,
            order: document.orders.map((item)=> {
                return {
                    dish: item.dish.name,
                    count: item.count
                }
            }),
        }),
    });
    if (resp.redirected == true)
        window.location.href = resp.url;

    let text = await resp.text();
    
    if (text == "UserNotExist"){
        addError(usernameInput, "Такого пользователя не существует");
    }

    if (text == "DishCountError"){
        addError(createOrderBtn, "Не верно указано количество блюд");
    }

    console.log(text);
}
function clearError(element){
    let errorId = "error";
    let parent = element.parentNode;
    let oldErrorDiv = parent.querySelector(`#${errorId}`);
    if (oldErrorDiv){
        parent.removeChild(oldErrorDiv);
    } 
}

function addError(element, error){
    let errorDiv = document.createElement("div");
    errorDiv.textContent = error;

    let errorId = "error";

    errorDiv.id = errorId;
    errorDiv.className = "help-inline text-danger";

    clearError(element);

    element.parentNode.append(errorDiv);
}

function usernameError(error){
    let errorDiv = document.createElement("div");
    errorDiv.textContent = error;

    let errorId = "username-error"

    errorDiv.id = errorId;
    errorDiv.className = "help-inline text-danger";

    let parent = usernameInput.parentNode;
    let oldErrorDiv = parent.querySelector(`#${errorId}`);
    if (oldErrorDiv){
        parent.removeChild(oldErrorDiv);
    } 
    parent.append(errorDiv)
}

function createOrderError(error){
    let errorDiv = document.createElement("div");
    errorDiv.textContent = error;

    let errorId = "create-order-error"

    errorDiv.id = errorId;
    errorDiv.className = "help-inline text-danger";

    let parent = createOrderBtn.parentNode;
    let oldErrorDiv = parent.querySelector(`#${errorId}`);
    if (oldErrorDiv){
        parent.removeChild(oldErrorDiv);
    } 
    parent.append(errorDiv)
}