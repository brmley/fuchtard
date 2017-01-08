import fetch from 'isomorphic-fetch';
// import * as Cookies from 'js-cookie';

// const csrftoken = Cookies.get('csrftoken');

function cartItemAdd(foodItemId, foodItem) {
    return {
        type: 'CART_ITEM_ADD',
        payload: {
            foodItemId: foodItemId,
            foodItem: foodItem,
        },
    }
}

function cartItemIncrease(foodItemId) {
    return {
        type: 'CART_ITEM_INCREASE',
        payload: foodItemId,
    }
}

function cartItemDecrease(foodItemId) {
    return {
        type: 'CART_ITEM_DECREASE',
        payload: foodItemId,
    }
}


function cartItemRemove(foodItemId) {
    return {
        type: 'CART_ITEM_REMOVE',
        payload: foodItemId,
    }
}

function cartPriceUpdate(by) {
    return {
        type: 'CART_PRICE_UPDATE',
        payload: by
    }
}

export function plusButton(foodItem, quantity=0) {
    const foodItemId = foodItem.get('id');
    return dispatch => {
        if (quantity <= 10) {
            if (quantity == 0) {
                dispatch(cartItemAdd(foodItemId, foodItem))
            } else {
                dispatch(cartItemIncrease(foodItemId))
            }
            dispatch(cartPriceUpdate(+foodItem.get('price')))
        }
    }
}

export function minusButton(foodItem, quantity=0) {
    const foodItemId = foodItem.get('id');
    return dispatch => {
        if (quantity >= 1) {
            if (quantity == 1) {
                dispatch(cartItemRemove(foodItemId))
            } else {
                dispatch(cartItemDecrease(foodItemId))
            }
            dispatch(cartPriceUpdate(-foodItem.get('price')))
        }
    }
}