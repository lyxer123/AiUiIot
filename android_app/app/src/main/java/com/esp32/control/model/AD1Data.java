package com.esp32.control.model;

public class AD1Data {
    private int id;
    private double value;
    private String timestamp;
    
    public AD1Data() {}
    
    public AD1Data(int id, double value, String timestamp) {
        this.id = id;
        this.value = value;
        this.timestamp = timestamp;
    }
    
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public double getValue() {
        return value;
    }
    
    public void setValue(double value) {
        this.value = value;
    }
    
    public String getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }
    
    @Override
    public String toString() {
        return "AD1Data{" +
                "id=" + id +
                ", value=" + value +
                ", timestamp='" + timestamp + '\'' +
                '}';
    }
}
