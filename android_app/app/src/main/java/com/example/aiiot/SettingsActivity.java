package com.example.aiiot;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import com.example.aiiot.network.NetworkManager;

public class SettingsActivity extends AppCompatActivity {
    
    private EditText etServerUrl;
    private Button btnSave, btnTestConnection, btnReset;
    private TextView tvCurrentUrl, tvConnectionStatus;
    private CardView settingsCard, statusCard;
    
    private NetworkManager networkManager;
    private SharedPreferences sharedPreferences;
    private static final String PREF_NAME = "ESP32Control";
    private static final String KEY_SERVER_URL = "server_url";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        
        // 初始化网络管理器
        networkManager = new NetworkManager(this);
        
        // 初始化SharedPreferences
        sharedPreferences = getSharedPreferences(PREF_NAME, MODE_PRIVATE);
        
        // 初始化视图
        initViews();
        
        // 加载当前设置
        loadCurrentSettings();
        
        // 设置点击事件
        setupClickListeners();
    }
    
    private void initViews() {
        etServerUrl = findViewById(R.id.et_server_url);
        btnSave = findViewById(R.id.btn_save);
        btnTestConnection = findViewById(R.id.btn_test_connection);
        btnReset = findViewById(R.id.btn_reset);
        tvCurrentUrl = findViewById(R.id.tv_current_url);
        tvConnectionStatus = findViewById(R.id.tv_connection_status);
        settingsCard = findViewById(R.id.settings_card);
        statusCard = findViewById(R.id.status_card);
    }
    
    private void loadCurrentSettings() {
        String currentUrl = sharedPreferences.getString(KEY_SERVER_URL, "http://192.168.1.100:5000/api");
        tvCurrentUrl.setText("当前服务器: " + currentUrl);
        etServerUrl.setText(currentUrl);
    }
    
    private void setupClickListeners() {
        btnSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveSettings();
            }
        });
        
        btnTestConnection.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                testConnection();
            }
        });
        
        btnReset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetSettings();
            }
        });
    }
    
    private void saveSettings() {
        String serverUrl = etServerUrl.getText().toString().trim();
        
        if (serverUrl.isEmpty()) {
            Toast.makeText(this, "请输入服务器地址", Toast.LENGTH_SHORT).show();
            return;
        }
        
        // 验证URL格式
        if (!serverUrl.startsWith("http://") && !serverUrl.startsWith("https://")) {
            Toast.makeText(this, "请输入有效的URL地址", Toast.LENGTH_SHORT).show();
            return;
        }
        
        // 保存设置
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(KEY_SERVER_URL, serverUrl);
        editor.apply();
        
        // 更新网络管理器
        networkManager.setServerUrl(serverUrl);
        
        // 更新显示
        tvCurrentUrl.setText("当前服务器: " + serverUrl);
        
        Toast.makeText(this, "设置保存成功", Toast.LENGTH_SHORT).show();
    }
    
    private void testConnection() {
        btnTestConnection.setEnabled(false);
        btnTestConnection.setText("测试中...");
        tvConnectionStatus.setText("连接状态: 测试中...");
        
        networkManager.testConnection(new NetworkManager.ConnectionCallback() {
            @Override
            public void onSuccess(String message) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnTestConnection.setEnabled(true);
                        btnTestConnection.setText("测试连接");
                        tvConnectionStatus.setText("连接状态: 成功");
                        tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
                        Toast.makeText(SettingsActivity.this, message, Toast.LENGTH_SHORT).show();
                    }
                });
            }
            
            @Override
            public void onFailure(String error) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnTestConnection.setEnabled(true);
                        btnTestConnection.setText("测试连接");
                        tvConnectionStatus.setText("连接状态: 失败");
                        tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                        Toast.makeText(SettingsActivity.this, error, Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });
    }
    
    private void resetSettings() {
        // 重置为默认值
        String defaultUrl = "http://192.168.1.100:5000/api";
        
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(KEY_SERVER_URL, defaultUrl);
        editor.apply();
        
        // 更新网络管理器
        networkManager.setServerUrl(defaultUrl);
        
        // 更新显示
        tvCurrentUrl.setText("当前服务器: " + defaultUrl);
        etServerUrl.setText(defaultUrl);
        tvConnectionStatus.setText("连接状态: 已重置");
        tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_blue_dark));
        
        Toast.makeText(this, "设置已重置为默认值", Toast.LENGTH_SHORT).show();
    }
}
