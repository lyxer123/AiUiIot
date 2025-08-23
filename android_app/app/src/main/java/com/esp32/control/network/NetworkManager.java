package com.esp32.control.network;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class NetworkManager {
    
    private static final String TAG = "NetworkManager";
    private static final MediaType JSON = MediaType.get("application/json; charset=utf-8");
    
    private OkHttpClient client;
    private String baseUrl;
    private Context context;
    
    public interface NetworkCallback {
        void onSuccess(String response);
        void onError(String error);
    }
    
    public NetworkManager(Context context) {
        this.context = context;
        this.client = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(10, TimeUnit.SECONDS)
                .writeTimeout(10, TimeUnit.SECONDS)
                .build();
        
        // 从SharedPreferences获取服务器配置
        SharedPreferences prefs = context.getSharedPreferences("ESP32Control", Context.MODE_PRIVATE);
        this.baseUrl = prefs.getString("server_url", "http://10.1.95.252:5000/api");
    }
    
    public void setServerUrl(String url) {
        this.baseUrl = url;
        // 保存到SharedPreferences
        SharedPreferences prefs = context.getSharedPreferences("ESP32Control", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();
        editor.putString("server_url", url);
        editor.apply();
    }
    
    public String getServerUrl() {
        return baseUrl;
    }
    
    // GET请求
    public void get(String endpoint, NetworkCallback callback) {
        String url = baseUrl + endpoint;
        Log.d(TAG, "GET请求: " + url);
        
        Request request = new Request.Builder()
                .url(url)
                .get()
                .build();
        
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "GET请求失败: " + e.getMessage());
                callback.onError("网络请求失败: " + e.getMessage());
            }
            
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    String responseBody = response.body().string();
                    Log.d(TAG, "GET响应: " + responseBody);
                    callback.onSuccess(responseBody);
                } else {
                    Log.e(TAG, "GET请求失败，状态码: " + response.code());
                    callback.onError("服务器响应错误: " + response.code());
                }
            }
        });
    }
    
    // POST请求
    public void post(String endpoint, JSONObject data, NetworkCallback callback) {
        String url = baseUrl + endpoint;
        String jsonData = data.toString();
        Log.d(TAG, "POST请求: " + url + ", 数据: " + jsonData);
        
        RequestBody body = RequestBody.create(jsonData, JSON);
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();
        
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "POST请求失败: " + e.getMessage());
                callback.onError("网络请求失败: " + e.getMessage());
            }
            
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    String responseBody = response.body().string();
                    Log.d(TAG, "POST响应: " + responseBody);
                    callback.onSuccess(responseBody);
                } else {
                    Log.e(TAG, "POST请求失败，状态码: " + response.code());
                    callback.onError("服务器响应错误: " + response.code());
                }
            }
        });
    }
    
    // 测试连接
    public void testConnection(NetworkCallback callback) {
        get("/test", callback);
    }
    
    // 获取系统状态
    public void getSystemStatus(NetworkCallback callback) {
        get("/status", callback);
    }
    
    // 获取AD1数据
    public void getAD1Data(int limit, NetworkCallback callback) {
        get("/ad1/data?limit=" + limit, callback);
    }
    
    // 获取IO1当前状态
    public void getIO1CurrentState(NetworkCallback callback) {
        get("/io1/current", callback);
    }
    
    // 控制IO1开关
    public void controlIO1(boolean state, NetworkCallback callback) {
        try {
            JSONObject data = new JSONObject();
            data.put("state", state);
            post("/io1/control", data, callback);
        } catch (JSONException e) {
            Log.e(TAG, "创建JSON数据失败: " + e.getMessage());
            callback.onError("数据格式错误");
        }
    }
    
    // 获取IO1控制历史
    public void getIO1ControlHistory(NetworkCallback callback) {
        get("/io1/control", callback);
    }
    
    // 获取设备状态历史
    public void getDeviceStatusHistory(int limit, NetworkCallback callback) {
        get("/device/status?limit=" + limit, callback);
    }
    
    // 检查网络连接状态
    public boolean isNetworkAvailable() {
        return android.net.ConnectivityManager.isNetworkTypeValid(
                android.net.ConnectivityManager.TYPE_WIFI);
    }
    
    // 显示网络错误提示
    public void showNetworkError(String error) {
        if (context != null) {
            Toast.makeText(context, error, Toast.LENGTH_SHORT).show();
        }
    }
}
