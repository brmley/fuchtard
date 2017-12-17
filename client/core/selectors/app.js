import { createSelector } from 'reselect';
import sumBy from 'lodash/sumBy';
import find from 'lodash/find';
import mapValues from 'lodash/mapValues';
import values from 'lodash/values';

import { restaurantSettings } from 'core/config';

const {minimalOrderRequirement} = restaurantSettings;

export const getQuantityByFoodId = (state, props) => cartSelector(state)[props.foodItemId];



export const getFoodItemsBySlugOrID = (state, props) => {
    const foodItems = getFoodItemsOfCategory(state, props);
    return foodItems.find(food => food.slug === props.match.params.foodSlug || food.id === +props.match.params.foodSlug)
};

const foodItemsSelector = state => Object.values(state.products.resources);
const giftsSelector = state => Object.values(state.gifts.resources);
export const cartSelector = state => state.cart.present.foodItems;
export const cartOrderingSelector = state => state.cart.present.ordering;
export const cartAsOrderedMap = state => new Map(cartOrderingSelector(state).map(v => [v, cartSelector(state)[v]]));
const getFoodItemById = (foodItems, id) => find(foodItems, v => v.id === +id);

export const getFoodItemAnnotatedCart = (cart, foodItems) => mapValues(
    cart,
    (quantity, foodItemId) => ({
        quantity,
        foodItem: getFoodItemById(foodItems, foodItemId),
    })
);

export const foodItemAnnotatedCartSelector = createSelector(cartSelector, foodItemsSelector, getFoodItemAnnotatedCart);

const getAnnotatedCartMap = (ordering, foodItems) => new Map(
    ordering.map(foodItemId => [foodItemId, foodItems[foodItemId]])
);

export const cartAsAnnotatedMapSelector = createSelector(cartOrderingSelector, foodItemAnnotatedCartSelector, getAnnotatedCartMap);


const getSubtotal = (cart) => sumBy(
    values(cart),
    ({quantity, foodItem}) => foodItem && foodItem.price * quantity
);


export const subtotalSelector = createSelector(foodItemAnnotatedCartSelector, getSubtotal);

export const cartIsEmptySelector = createSelector(
    subtotalSelector,
    subtotal => subtotal <= 0
);

export const minimalOrderRequirementSatisfiedSelector = createSelector(
    subtotalSelector,
    subtotal => subtotal >= minimalOrderRequirement,
);

const getFoodItemAnnotatedGifts = (gifts, foodItems) => gifts.map(
    ({food_item, ...rest}) => ({
        foodItem: getFoodItemById(foodItems, food_item),
        ...rest,
    })
);

export const foodItemAnnotatedGifts = createSelector(giftsSelector, foodItemsSelector, getFoodItemAnnotatedGifts);
