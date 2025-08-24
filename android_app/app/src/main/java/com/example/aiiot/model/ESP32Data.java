package com.example.aiiot.model;

public class ESP32Data {
    private int ad1Value;
    private boolean io1State;
    private long timestamp;
    private String deviceStatus;

    public ESP32Data() {}

    public ESP32Data(int ad1Value, boolean io1State) {
        this.ad1Value = ad1Value;
        this.io1State = io1State;
        this.timestamp = System.currentTimeMillis();
        this.deviceStatus = "online";
    }

    // Getters and Setters
    public int getAd1Value() { return ad1Value; }
    public void setAd1Value(int ad1Value) { this.ad1Value = ad1Value; }

    public boolean isIo1State() { return io1State; }
    public void setIo1State(boolean io1State) { this.io1State = io1State; }

    public long getTimestamp() { return timestamp; }
    public void setTimestamp(long timestamp) { this.timestamp = timestamp; }

    public String getDeviceStatus() { return deviceStatus; }
    public void setDeviceStatus(String deviceStatus) { this.deviceStatus = deviceStatus; }

    public String getFormattedTimestamp() {
        return new java.text.SimpleDateFormat("HH:mm:ss", java.util.Locale.getDefault())
                .format(new java.util.Date(timestamp));
    }
}
