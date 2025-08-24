package com.example.aiiot.config;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

/**
 * 应用配置管理类
 * 负责管理所有应用配置的保存和加载
 */
public class AppConfig {
    private static final String TAG = "AppConfig";
    private static final String PREF_NAME = "ESP32Control";
    
    // 配置键名
    public static final String KEY_SERVER_URL = "server_url";
    public static final String KEY_USERNAME = "username";
    public static final String KEY_USER_ID = "user_id";
    public static final String KEY_IS_LOGGED_IN = "is_logged_in";
    
    // 默认值
    public static final String DEFAULT_SERVER_URL = "http://192.168.1.100:5000/api";
    
    private static AppConfig instance;
    private SharedPreferences sharedPreferences;
    
    private AppConfig(Context context) {
        sharedPreferences = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }
    
    public static synchronized AppConfig getInstance(Context context) {
        if (instance == null) {
            instance = new AppConfig(context);
        }
        return instance;
    }
    
    /**
     * 保存服务器地址
     */
    public boolean saveServerUrl(String serverUrl) {
        try {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putString(KEY_SERVER_URL, serverUrl);
            boolean success = editor.commit();
            
            if (success) {
                Log.d(TAG, "服务器地址保存成功: " + serverUrl);
            } else {
                Log.e(TAG, "服务器地址保存失败: " + serverUrl);
            }
            
            return success;
        } catch (Exception e) {
            Log.e(TAG, "保存服务器地址时出错", e);
            return false;
        }
    }
    
    /**
     * 获取服务器地址
     */
    public String getServerUrl() {
        return sharedPreferences.getString(KEY_SERVER_URL, DEFAULT_SERVER_URL);
    }
    
    /**
     * 保存用户登录信息
     */
    public boolean saveUserInfo(String username, int userId) {
        try {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putString(KEY_USERNAME, username);
            editor.putInt(KEY_USER_ID, userId);
            editor.putBoolean(KEY_IS_LOGGED_IN, true);
            boolean success = editor.commit();
            
            if (success) {
                Log.d(TAG, "用户信息保存成功: " + username);
            } else {
                Log.e(TAG, "用户信息保存失败: " + username);
            }
            
            return success;
        } catch (Exception e) {
            Log.e(TAG, "保存用户信息时出错", e);
            return false;
        }
    }
    
    /**
     * 获取用户名
     */
    public String getUsername() {
        return sharedPreferences.getString(KEY_USERNAME, "");
    }
    
    /**
     * 获取用户ID
     */
    public int getUserId() {
        return sharedPreferences.getInt(KEY_USER_ID, -1);
    }
    
    /**
     * 检查是否已登录
     */
    public boolean isLoggedIn() {
        return sharedPreferences.getBoolean(KEY_IS_LOGGED_IN, false);
    }
    
    /**
     * 清除用户登录信息（保留服务器配置）
     */
    public boolean clearUserInfo() {
        try {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.remove(KEY_USERNAME);
            editor.remove(KEY_USER_ID);
            editor.remove(KEY_IS_LOGGED_IN);
            boolean success = editor.commit();
            
            if (success) {
                Log.d(TAG, "用户信息清除成功");
            } else {
                Log.e(TAG, "用户信息清除失败");
            }
            
            return success;
        } catch (Exception e) {
            Log.e(TAG, "清除用户信息时出错", e);
            return false;
        }
    }
    
    /**
     * 重置所有配置为默认值
     */
    public boolean resetAllConfig() {
        try {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.clear();
            boolean success = editor.commit();
            
            if (success) {
                Log.d(TAG, "所有配置重置成功");
            } else {
                Log.e(TAG, "所有配置重置失败");
            }
            
            return success;
        } catch (Exception e) {
            Log.e(TAG, "重置所有配置时出错", e);
            return false;
        }
    }
    
    /**
     * 检查配置是否有效
     */
    public boolean isConfigValid() {
        String serverUrl = getServerUrl();
        return serverUrl != null && !serverUrl.isEmpty() && 
               (serverUrl.startsWith("http://") || serverUrl.startsWith("https://"));
    }
    
    /**
     * 获取配置摘要信息
     */
    public String getConfigSummary() {
        StringBuilder summary = new StringBuilder();
        summary.append("服务器地址: ").append(getServerUrl()).append("\n");
        summary.append("登录状态: ").append(isLoggedIn() ? "已登录" : "未登录");
        
        if (isLoggedIn()) {
            summary.append(" (").append(getUsername()).append(")");
        }
        
        return summary.toString();
    }
}
