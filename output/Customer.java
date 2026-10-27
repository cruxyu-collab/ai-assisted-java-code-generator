/** DTO generated from a validated design definition. */
public class Customer {

    /** 顧客ID */
    private long customerId;

    /** 顧客名 */
    private String customerName;

    /** 有効フラグ */
    private boolean active;

    public long getCustomerId() {
        return customerId;
    }

    public void setCustomerId(long customerId) {
        this.customerId = customerId;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

}
