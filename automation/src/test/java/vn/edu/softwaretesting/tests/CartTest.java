package vn.edu.softwaretesting.tests;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import vn.edu.softwaretesting.core.WebTestBase;
import vn.edu.softwaretesting.pages.CartPage;
import vn.edu.softwaretesting.pages.InventoryPage;
import vn.edu.softwaretesting.pages.LoginPage;
import vn.edu.softwaretesting.pages.LoginPage.LoginResult;

@Tag("web")
@DisplayName("FR-CART: Shopping cart")
class CartTest extends WebTestBase {

    private InventoryPage inventoryPage;

    @BeforeEach
    void loginAsStandardUser() {
        LoginResult result = new LoginPage(driver, baseUrl)
                .open()
                .login("standard_user", "secret_sauce");
        assertTrue(result.accepted(),
                () -> "Could not log in as standard_user: " + result.message());
        inventoryPage = new InventoryPage(driver);
    }

    @ParameterizedTest(name = "TC-CART-AUTO-{index}: add products and check badge")
    @CsvSource({
            "sauce-labs-backpack, 'Sauce Labs Backpack', sauce-labs-bike-light, 'Sauce Labs Bike Light'",
            "sauce-labs-bolt-t-shirt, 'Sauce Labs Bolt T-Shirt', sauce-labs-fleece-jacket, 'Sauce Labs Fleece Jacket'",
            "sauce-labs-onesie, 'Sauce Labs Onesie', sauce-labs-backpack, 'Sauce Labs Backpack'"
    })
    void addingProductsShouldUpdateBadgeAndCartContents(
            String firstSlug, String firstName, String secondSlug, String secondName) {
        assertFalse(inventoryPage.isCartBadgeDisplayed(),
                "Badge should be hidden when the cart is empty");

        inventoryPage.addProduct(firstSlug);
        assertEquals("1", inventoryPage.getCartBadgeCount());

        inventoryPage.addProduct(secondSlug);
        assertEquals("2", inventoryPage.getCartBadgeCount());

        CartPage cartPage = inventoryPage.openCart();
        assertEquals(2, cartPage.getProductNames().size());
        assertTrue(cartPage.getProductNames().contains(firstName));
        assertTrue(cartPage.getProductNames().contains(secondName));
    }

    @ParameterizedTest(name = "TC-CART-AUTO-{index}: remove one product")
    @CsvSource({
            "sauce-labs-backpack, 'Sauce Labs Backpack', sauce-labs-bike-light, 'Sauce Labs Bike Light'",
            "sauce-labs-bolt-t-shirt, 'Sauce Labs Bolt T-Shirt', sauce-labs-fleece-jacket, 'Sauce Labs Fleece Jacket'"
    })
    void removingProductShouldUpdateBadgeAndKeepOtherProduct(
            String removedSlug, String removedName,
            String remainingSlug, String remainingName) {
        CartPage cartPage = inventoryPage
                .addProduct(removedSlug)
                .addProduct(remainingSlug)
                .openCart()
                .removeProduct(removedSlug)
                .waitForCartBadgeCount("1");

        assertEquals(1, cartPage.getProductNames().size());
        assertTrue(cartPage.getProductNames().contains(remainingName));
        assertFalse(cartPage.getProductNames().contains(removedName));
        assertEquals("1", cartPage.getCartBadgeCount());
    }

    @ParameterizedTest(name = "TC-CART-AUTO-{index}: remove final product")
    @CsvSource({
            "sauce-labs-backpack",
            "sauce-labs-bike-light",
            "sauce-labs-onesie"
    })
    void removingFinalProductShouldEmptyCartAndHideBadge(String productSlug) {
        CartPage cartPage = inventoryPage
                .addProduct(productSlug)
                .openCart()
                .removeProduct(productSlug)
                .waitForCartBadgeToDisappear();

        assertTrue(cartPage.getProductNames().isEmpty(),
                "Cart should be empty after removing its final product");
        assertFalse(cartPage.isCartBadgeDisplayed(),
                "Badge should be hidden when the cart is empty");
    }
}
