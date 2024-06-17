export default class DishFactory{
    
    createDishCard(dish, isInOrder, count=0){
        let container = this.#createContainer(dish);

        let body = this.#createBody();
        this.#fillBody(body, dish, isInOrder, count);

        container.append(body);

        return container;
    }

    getNewTotalPrice(dish, count){
        return this.#createTotalPrice(dish, count);    
    }

    #createContainer(dish){
        let cardContainer = document.createElement("div");
        cardContainer.className = "card";
        cardContainer.id = dish.name;
        return cardContainer;
    }

    #createBody(){
        let cardBody = document.createElement("div");
        cardBody.className = "card-body";
        cardBody.id = "card-body";
        return cardBody;
    }

    #fillBody(cardBody, dish, isInOrder, count){
        cardBody.append(this.#createTitle(dish));
        cardBody.append(this.#createText(dish));
        if (isInOrder > 0){
            cardBody.append( this.#createCountInput(count));
            cardBody.append( this.#createTotalPrice(dish, count));
        }
        cardBody.append(this.#createButton(isInOrder));
    }

    #createTitle(dish){
        let cardTitle = document.createElement("h5");
        cardTitle.textContent = dish.name;
        cardTitle.className = "card-title";
        return cardTitle;
    }

    #createText(dish){
        let cardText = document.createElement("div");
        cardText.textContent = `Цена: ${dish.price} р.`;
        cardText.className = "card-text";
        return cardText;
    }

    #createTotalPrice(dish, count){
        let cardText = document.createElement("div");
        cardText.textContent = `Всего: ${dish.price * count} р.`;
        cardText.className = "card-text";
        cardText.id = "card-total-price";
        return cardText;
    }

    #createButton(isInOrder){
        let button = document.createElement("div");
        button.id = "card-button";
        button.className = "btn ";
        if (isInOrder){
            button.className += "btn-danger";
            button.textContent = "Удалить";
        }else{
            button.className += "btn-primary";
            button.textContent = "Добавить";
        }
        return button;
    }

    #createCountInput(count){
        let input = document.createElement("input");
        input.id = "card-input";
        input.type = "number";
        input.className = "form-control";
        input.min = 1;
        input.step = 1;
        input.value = count;
        return input;
    }

}