package com.example.aiiot.network;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;
import android.widget.Toast;

import com.example.aiiot.model.ESP32Data;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
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
    private SharedPreferences prefs;
    
    public NetworkManager(Context context) {
        this.context = context;
        this.prefs = context.getSharedPreferences("ESP32Control", Context.MODE_PRIVATE);
        
        // 初始化OkHttpClient
        client = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .build();
        
        // 获取服务器地址
        this.baseUrl = prefs.getString("server_url", "http://192.168.1.100:5000/api");
    }
    
    public void setServerUrl(String url) {
        this.baseUrl = url;
        SharedPreferences.Editor editor = prefs.edit();
        editor.putString("server_url", url);
        editor.apply();
    }
    
    public String getServerUrl() {
        return baseUrl;
    }
    
    // 测试连接
    public void testConnection(ConnectionCallback callback) {
        String url = baseUrl + "/status";
        Request request = new Request.Builder().url(url).build();
        
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "连接测试失败", e);
                callback.onFailure("连接失败: " + e.getMessage());
            }
            
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    callback.onSuccess("连接成功");
                } else {
                    callback.onFailure("服务器响应错误: " + response.code());
                }
            }
        });
    }
    
    // 获取系统状态
    public void getSystemStatus(StatusCallback callback) {
        String url = baseUrl + "/status";
        Request request = new Request.Builder().url(url).build();
        
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "获取状态失败", e);
                callback.onFailure("网络错误: " + e.getMessage());
            }
            
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        String responseBody = response.body().string();
                        JSONObject json = new JSONObject(responseBody);
                        
                        if (json.getBoolean("success")) {
                            JSONObject data = json.getJSONObject("data");
                            boolean mqttConnected = data.getBoolean("mqtt_connected");
                            boolean io1State = data.getBoolean("io1_current_state");
                            String systemStatus = data.getString("system_status");
                            
                            callback.onSuccess(mqttConnected, io1State, systemStatus);
                        } else {
                            callback.onFailure("服务器错误: " + json.getString("error"));
                        }
                    } catch (JSONException e) {
                        callback.onFailure("数据解析错误: " + e.getMessage());
                    }
                } else {
                    callback.onFailure("服务器响应错误: " + response.code());
                }
            }
        });
    }
    
    // 获取AD1数据
    public void getAD1Data(int limit, DataCallback<List<ESP32Data>> callback) {
        String url = baseUrl + "/ad1/data?limit=" + limit;
        Request request = new Request.Builder().url(url).build();
        
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "获取AD1数据失败", e);
                callback.onFailure("网络错误: " + e.getMessage());
            }
            
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        String responseBody = response.body().string();
                        JSONObject json = new JSONObject(responseBody);
                        
                        if (json.getBoolean("success")) {
                            JSONArray dataArray = json.getJSONArray("data");
                            List<ESP32Data> dataList = new ArrayList<>();
                            
                            for (int i = 0; i < dataArray.length(); i++) {
                                JSONObject item = dataArray.getJSONObject(i);
                                ESP32Data data = new ESP32Data();
                                data.setAd1Value(item.getInt("value"));
                                data.setTimestamp(item.getLong("timestamp"));
                                dataList.add(data);
                            }
                            
                            callback.onSuccess(dataList);
                        } else {
                            callback.onFailure("服务器错误: " + json.getString("error"));
                        }
                    } catch (JSONException e) {
                        callback.onFailure("数据解析错误: " + e.getMessage());
                    }
                } else {
                    callback.onFailure("服务器响应错误: " + response.code());
                }
            }
        });
    }
    
    // 控制IO1
    public void controlIO1(boolean state, ControlCallback callback) {
        String url = baseUrl + "/io1/control";
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("state", state);
        } catch (JSONException e) {
            callback.onFailure("参数错误: " + e.getMessage());
            return;
        }
        
        RequestBody body = RequestBody.create(jsonBody.toString(), JSON);
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();
        
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG, "控制IO1失败", e);
                callback.onFailure("网络错误: " + e.getMessage());
            }
            
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        String responseBody = response.body().string();
                        JSONObject json = new JSONObject(responseBody);
                        
                        if (json.getBoolean("success")) {
                            callback.onSuccess("控制成功");
                        } else {
                            callback.onFailure("控制失败: " + json.getString("error"));
                        }
                    } catch (JSONException e) {
                        callback.onFailure("响应解析错误: " + e.getMessage());
                    }
                } else {
                    callback.onFailure("服务器响应错误: " + response.code());
                }
            }
        });
    }
    
    // 回调接口
    public interface ConnectionCallback {
        void onSuccess(String message);
        void onFailure(String error);
    }
    
    public interface StatusCallback {
        void onSuccess(boolean mqttConnected, boolean io1State, String systemStatus);
        void onFailure(String error);
    }
    
    public interface DataCallback<T> {
        void onSuccess(T data);
        void onFailure(String error);
    }
    
    public interface ControlCallback {
        void onSuccess(String message);
        void onFailure(String error);
    }
}
