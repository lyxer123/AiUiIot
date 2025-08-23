package com.esp32.control;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import com.esp32.control.network.NetworkManager;

public class SettingsActivity extends AppCompatActivity {
    
    private NetworkManager networkManager;
    private SharedPreferences sharedPreferences;
    
    private EditText etServerUrl;
    private Button btnSave, btnTest, btnReset;
    private TextView tvCurrentUrl, tvConnectionStatus;
    private CardView settingsCard, statusCard;
    
    private static final String PREF_NAME = "ESP32Control";
    private static final String KEY_SERVER_URL = "server_url";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        
        // 初始化SharedPreferences
        sharedPreferences = getSharedPreferences(PREF_NAME, MODE_PRIVATE);
        
        // 初始化网络管理器
        networkManager = new NetworkManager(this);
        
        // 初始化视图
        initViews();
        
        // 设置点击事件
        setupClickListeners();
        
        // 加载当前设置
        loadCurrentSettings();
    }
    
    private void initViews() {
        etServerUrl = findViewById(R.id.et_server_url);
        btnSave = findViewById(R.id.btn_save);
        btnTest = findViewById(R.id.btn_test);
        btnReset = findViewById(R.id.btn_reset);
        tvCurrentUrl = findViewById(R.id.tv_current_url);
        tvConnectionStatus = findViewById(R.id.tv_connection_status);
        settingsCard = findViewById(R.id.settings_card);
        statusCard = findViewById(R.id.status_card);
    }
    
    private void setupClickListeners() {
        btnSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveSettings();
            }
        });
        
        btnTest.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                testConnection();
            }
        });
        
        btnReset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetToDefault();
            }
        });
    }
    
    private void loadCurrentSettings() {
        String currentUrl = sharedPreferences.getString(KEY_SERVER_URL, "http://10.1.95.252:5000/api");
        tvCurrentUrl.setText("当前服务器: " + currentUrl);
        etServerUrl.setText(currentUrl);
        
        // 测试当前连接
        testCurrentConnection();
    }
    
    private void saveSettings() {
        String newUrl = etServerUrl.getText().toString().trim();
        
        if (newUrl.isEmpty()) {
            Toast.makeText(this, "请输入服务器地址", Toast.LENGTH_SHORT).show();
            return;
        }
        
        if (!newUrl.startsWith("http://") && !newUrl.startsWith("https://")) {
            Toast.makeText(this, "请输入有效的URL地址", Toast.LENGTH_SHORT).show();
            return;
        }
        
        // 保存新设置
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(KEY_SERVER_URL, newUrl);
        editor.apply();
        
        // 更新网络管理器
        networkManager.setServerUrl(newUrl);
        
        // 更新显示
        tvCurrentUrl.setText("当前服务器: " + newUrl);
        
        Toast.makeText(this, "设置已保存", Toast.LENGTH_SHORT).show();
        
        // 测试新连接
        testConnection();
    }
    
    private void testConnection() {
        btnTest.setEnabled(false);
        btnTest.setText("测试中...");
        
        networkManager.testConnection(new NetworkManager.NetworkCallback() {
            @Override
            public void onSuccess(String response) {
                try {
                    org.json.JSONObject jsonResponse = new org.json.JSONObject(response);
                    if (jsonResponse.getBoolean("success")) {
                        updateConnectionStatus("连接正常", true);
                        Toast.makeText(SettingsActivity.this, "连接测试成功", Toast.LENGTH_SHORT).show();
                    } else {
                        updateConnectionStatus("连接异常", false);
                        Toast.makeText(SettingsActivity.this, "连接测试失败", Toast.LENGTH_SHORT).show();
                    }
                } catch (org.json.JSONException e) {
                    updateConnectionStatus("响应解析失败", false);
                    Toast.makeText(SettingsActivity.this, "响应解析失败", Toast.LENGTH_SHORT).show();
                }
                
                btnTest.setEnabled(true);
                btnTest.setText("测试连接");
            }
            
            @Override
            public void onError(String error) {
                updateConnectionStatus("连接失败: " + error, false);
                Toast.makeText(SettingsActivity.this, "连接失败: " + error, Toast.LENGTH_SHORT).show();
                
                btnTest.setEnabled(true);
                btnTest.setText("测试连接");
            }
        });
    }
    
    private void testCurrentConnection() {
        // 静默测试当前连接状态
        networkManager.testConnection(new NetworkManager.NetworkCallback() {
            @Override
            public void onSuccess(String response) {
                try {
                    org.json.JSONObject jsonResponse = new org.json.JSONObject(response);
                    if (jsonResponse.getBoolean("success")) {
                        updateConnectionStatus("连接正常", true);
                    } else {
                        updateConnectionStatus("连接异常", false);
                    }
                } catch (org.json.JSONException e) {
                    updateConnectionStatus("响应解析失败", false);
                }
            }
            
            @Override
            public void onError(String error) {
                updateConnectionStatus("连接失败: " + error, false);
            }
        });
    }
    
    private void updateConnectionStatus(final String status, final boolean isSuccess) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                tvConnectionStatus.setText(status);
                if (isSuccess) {
                    tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
                } else {
                    tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                }
            }
        });
    }
    
    private void resetToDefault() {
        String defaultUrl = "http://10.1.95.252:5000/api";
        
        // 保存默认设置
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(KEY_SERVER_URL, defaultUrl);
        editor.apply();
        
        // 更新网络管理器
        networkManager.setServerUrl(defaultUrl);
        
        // 更新显示
        tvCurrentUrl.setText("当前服务器: " + defaultUrl);
        etServerUrl.setText(defaultUrl);
        
        Toast.makeText(this, "已重置为默认设置", Toast.LENGTH_SHORT).show();
        
        // 测试默认连接
        testConnection();
    }
}
