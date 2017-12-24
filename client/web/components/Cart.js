import React from 'react';
import { connect } from 'react-redux';

import { cartAsAnnotatedMapSelector } from 'core/selectors/app';

import TransitionGroup from 'react-transition-group';
import { Card, CardTitle } from 'react-toolbox/lib/card';

import CartItem from './CartItem';
import CartTotal from './CartTotal';

import styles from 'styles/Cart.css';
import { MinimalOrderInfo, AddToCardButtonHowto } from './CheckoutHowto';

const EmptyCart = () => <Card>
        <CardTitle subtitle={
            <span>
                <AddToCardButtonHowto/>
                <br/>
                <MinimalOrderInfo/>
            </span>
        }/>
</Card>;

export class Cart extends React.Component {
    static defaultProps = {
        cart: new Map(),
    };

    render() {
        const {cart} = this.props;
        const cartEntries = [...cart.entries()];
        return <div>
            <p className={styles.subheader}>Корзина</p>
            {/*<TransitionGroup*/}
                {/*transitionName={{*/}
                    {/*enter: styles.animationEnter,*/}
                    {/*enterActive: styles.animationEnterActive,*/}
                    {/*leave: styles.animationLeave,*/}
                    {/*leaveActive: styles.animationLeaveActive,*/}
                {/*}}*/}
                {/*transitionEnterTimeout={400}*/}
                {/*transitionLeaveTimeout={400}>*/}
                {cartEntries.map(([foodItemId, rest]) =>
                    <div
                        className={styles.cartItemAnimationWrapper}
                        key={foodItemId}
                    >

                        <CartItem
                            foodItemId={+foodItemId}
                            {...rest}
                        />
                    </div>
                )}
                { cartEntries.length > 0
                    ? <CartTotal/>
                    : <div className={styles.cartItemAnimationWrapper}>
                        <EmptyCart/>
                    </div>
                }
            {/*</TransitionGroup>*/}
        </div>

    }
}

export default connect(
    state => ({
        cart: cartAsAnnotatedMapSelector(state),
    }),
)(Cart)
