package com.example.aiiot.model;

import android.util.Log;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class ESP32Data {
    private static final String TAG = "ESP32Data";
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
        try {
            if (timestamp <= 0) {
                return "无效时间";
            }
            
            SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss", Locale.getDefault());
            return sdf.format(new Date(timestamp));
        } catch (Exception e) {
            Log.e(TAG, "时间格式化失败", e);
            return "时间错误";
        }
    }
    
    public String getFullFormattedTimestamp() {
        try {
            if (timestamp <= 0) {
                return "无效时间";
            }
            
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
            return sdf.format(new Date(timestamp));
        } catch (Exception e) {
            Log.e(TAG, "完整时间格式化失败", e);
            return "时间错误";
        }
    }
}
