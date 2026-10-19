package vn.edu.softwaretesting.pages;

import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public final class InventoryPage {

    private static final By CART_BADGE =
            By.cssSelector(".shopping_cart_badge");
    private static final By CART_LINK =
            By.cssSelector(".shopping_cart_link");

    private final WebDriver driver;
    private final WebDriverWait wait;

    public InventoryPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(8));
        wait.until(ExpectedConditions.visibilityOfElementLocated(
                By.id("inventory_container")));
    }

    public InventoryPage addProduct(String productSlug) {
        By addButton = By.cssSelector(
                "[data-test='add-to-cart-" + productSlug + "']");
        driver.findElement(addButton).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(
                By.cssSelector("[data-test='remove-" + productSlug + "']")));
        return this;
    }

    public boolean isCartBadgeDisplayed() {
        return !driver.findElements(CART_BADGE).isEmpty()
                && driver.findElement(CART_BADGE).isDisplayed();
    }

    public String getCartBadgeCount() {
        return wait.until(
                ExpectedConditions.visibilityOfElementLocated(CART_BADGE))
                .getText();
    }

    public CartPage openCart() {
        driver.findElement(CART_LINK).click();
        return new CartPage(driver);
    }
}
