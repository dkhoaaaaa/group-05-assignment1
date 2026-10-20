
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

    // ===== SORT & INVENTORY =====
    private static final By SORT_DROPDOWN =
            By.className("product_sort_container");

    private static final By INVENTORY_ITEMS =
            By.className("inventory_item");

    private static final By INVENTORY_ITEM_NAME =
            By.className("inventory_item_name");

    private static final By INVENTORY_ITEM_PRICE =
            By.className("inventory_item_price");

    private static final By INVENTORY_CONTAINER =
            By.id("inventory_container");

    // ===== CART =====
    private static final By CART_BADGE =
            By.cssSelector(".shopping_cart_badge");

    private static final By CART_LINK =
            By.cssSelector(".shopping_cart_link");

    private final WebDriver driver;
    private final WebDriverWait wait;

    // ===== CONSTRUCTOR =====
    public InventoryPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    // ===== OPEN PAGE =====
    public InventoryPage open() {
        driver.get("https://www.saucedemo.com/inventory.html");
        waitForPageLoaded();
        return this;
    }

    public void waitForPageLoaded() {
        wait.until(ExpectedConditions.visibilityOfElementLocated(
                INVENTORY_CONTAINER));
        wait.until(ExpectedConditions.visibilityOfElementLocated(
                SORT_DROPDOWN));
    }

    // ===== SORT PRODUCTS =====

    /**
     * Chọn kiểu sắp xếp
     * @param sortOption az, za, lohi, hilo
     */
    public void selectSort(String sortOption) {
        WebElement dropdown = wait.until(
                ExpectedConditions.elementToBeClickable(SORT_DROPDOWN));

        Select select = new Select(dropdown);
        select.selectByValue(sortOption);

        wait.until(ExpectedConditions.visibilityOfElementLocated(
                INVENTORY_ITEMS));
    }

    /**
     * Lấy danh sách tên sản phẩm theo thứ tự hiển thị
     */
    public List<String> getItemNames() {
        List<WebElement> items = wait.until(
                ExpectedConditions.presenceOfAllElementsLocatedBy(
                        INVENTORY_ITEM_NAME));

        return items.stream()
                .map(WebElement::getText)
                .toList();
    }

    /**
     * Lấy danh sách giá sản phẩm theo thứ tự hiển thị
     */
    public List<Double> getItemPrices() {
        List<WebElement> items = wait.until(
                ExpectedConditions.presenceOfAllElementsLocatedBy(
                        INVENTORY_ITEMS));

        return items.stream()
                .map(item -> {
                    String priceText = item.findElement(
                            INVENTORY_ITEM_PRICE).getText();

                    return Double.parseDouble(
                            priceText.replace("$", ""));
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

    // ===== ADD TO CART =====

    /**
     * Thêm sản phẩm vào giỏ hàng
     * @param productSlug Ví dụ: sauce-labs-backpack
     */
    public InventoryPage addProduct(String productSlug) {
        By addButton = By.cssSelector(
                "[data-test='add-to-cart-" + productSlug + "']");

        WebElement button = wait.until(
                ExpectedConditions.elementToBeClickable(addButton));

        button.click();

        wait.until(ExpectedConditions.visibilityOfElementLocated(
                By.cssSelector(
                        "[data-test='remove-" + productSlug + "']")));

        return this;
    }

    // ===== CART BADGE =====

    /**
     * Kiểm tra badge giỏ hàng có hiển thị không
     */
    public boolean isCartBadgeDisplayed() {
        return !driver.findElements(CART_BADGE).isEmpty()
                && driver.findElement(CART_BADGE).isDisplayed();
    }

    /**
     * Lấy số lượng sản phẩm trên badge giỏ hàng
     */
    public String getCartBadgeCount() {
        return wait.until(
                ExpectedConditions.visibilityOfElementLocated(
                        CART_BADGE))
                .getText();
    }

    // ===== OPEN CART =====

    /**
     * Chuyển đến trang giỏ hàng
     */
    public CartPage openCart() {
        WebElement cartLink = wait.until(
                ExpectedConditions.elementToBeClickable(CART_LINK));

        cartLink.click();

        return new CartPage(driver);
    }
}
