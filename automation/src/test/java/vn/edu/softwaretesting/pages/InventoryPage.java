package vn.edu.softwaretesting.pages;

import java.time.Duration;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Page Object cho trang Inventory (Danh sách sản phẩm)
 */
public final class InventoryPage {

    private static final By SORT_DROPDOWN = By.className("product_sort_container");
    private static final By INVENTORY_ITEMS = By.className("inventory_item");
    private static final By INVENTORY_ITEM_NAME = By.className("inventory_item_name");
    private static final By INVENTORY_ITEM_PRICE = By.className("inventory_item_price");
    private static final By CART_BADGE =
            By.cssSelector(".shopping_cart_badge");
    private static final By CART_LINK =
            By.cssSelector(".shopping_cart_link");

    private final WebDriver driver;
    private final WebDriverWait wait;

    public InventoryPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public InventoryPage open() {
        driver.get("https://www.saucedemo.com/inventory.html");
        waitForPageLoaded();
        return this;
    }

    public void waitForPageLoaded() {
        wait.until(ExpectedConditions.visibilityOfElementLocated(SORT_DROPDOWN));
    }

    /**
     * Chọn kiểu sắp xếp
     * @param sortOption Giá trị value của dropdown: az, za, lohi, hilo
     */
    public void selectSort(String sortOption) {
        WebElement dropdown = wait.until(
                ExpectedConditions.elementToBeClickable(SORT_DROPDOWN));
        Select select = new Select(dropdown);
        select.selectByValue(sortOption);
        // Đợi items re-render
        wait.until(ExpectedConditions.visibilityOfElementLocated(INVENTORY_ITEMS));
    }

    /**
     * Lấy danh sách tên sản phẩm theo thứ tự hiển thị
     */
    public List<String> getItemNames() {
        List<WebElement> items = wait.until(
                ExpectedConditions.presenceOfAllElementsLocatedBy(INVENTORY_ITEM_NAME));
        return items.stream()
                .map(WebElement::getText)
                .toList();
    }

    /**
     * Lấy danh sách giá sản phẩm theo thứ tự hiển thị
     */
    public List<Double> getItemPrices() {
        List<WebElement> items = wait.until(
                ExpectedConditions.presenceOfAllElementsLocatedBy(INVENTORY_ITEMS));
        return items.stream()
                .map(item -> {
                    String priceText = item.findElement(INVENTORY_ITEM_PRICE).getText();
                    return Double.parseDouble(priceText.replace("$", ""));
                })
                .toList();
    }

    /**
     * Lấy số lượng sản phẩm trên trang
     */
    public int getItemCount() {
        return driver.findElements(INVENTORY_ITEMS).size();
    }

    /**
     * Kiểm tra trang đã load đầy đủ
     */
    public boolean isLoaded() {
        try {
            return !driver.findElements(INVENTORY_ITEMS).isEmpty();
        } catch (Exception e) {
            return false;
        }
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
