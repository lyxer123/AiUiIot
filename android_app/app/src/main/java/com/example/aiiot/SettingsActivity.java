package com.example.aiiot;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import com.example.aiiot.config.AppConfig;
import com.example.aiiot.network.NetworkManager;

public class SettingsActivity extends AppCompatActivity {
    
    private EditText etServerUrl;
    private Button btnSave, btnTestConnection, btnReset;
    private TextView tvCurrentUrl, tvConnectionStatus;
    private CardView settingsCard, statusCard;
    
    private NetworkManager networkManager;
    private AppConfig appConfig;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        
        // 初始化配置管理器
        appConfig = AppConfig.getInstance(this);
        
        // 初始化网络管理器
        networkManager = new NetworkManager(this);
        
        // 初始化视图
        initViews();
        
        // 加载当前设置
        loadCurrentSettings();
        
        // 设置点击事件
        setupClickListeners();
        
        // 显示保存状态
        showSaveStatus();
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
        
        // 添加配置摘要显示
        TextView tvConfigSummary = findViewById(R.id.tv_config_summary);
        if (tvConfigSummary != null) {
            updateConfigSummary(tvConfigSummary);
        }
    }
    
    private void updateConfigSummary(TextView tvConfigSummary) {
        String summary = appConfig.getConfigSummary();
        tvConfigSummary.setText(summary);
    }
    
    private void loadCurrentSettings() {
        // 从配置管理器加载保存的服务器地址
        String savedUrl = appConfig.getServerUrl();
        
        // 确保网络管理器使用保存的地址
        networkManager.setServerUrl(savedUrl);
        
        // 更新UI显示
        tvCurrentUrl.setText("当前服务器: " + savedUrl);
        etServerUrl.setText(savedUrl);
        
        // 显示连接状态
        tvConnectionStatus.setText("连接状态: 未知");
        tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_blue_dark));
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
            Toast.makeText(this, "请输入有效的URL地址（以http://或https://开头）", Toast.LENGTH_LONG).show();
            return;
        }
        
        // 验证URL结构
        if (!serverUrl.contains("://") || serverUrl.split("://").length != 2) {
            Toast.makeText(this, "请输入有效的URL地址", Toast.LENGTH_SHORT).show();
            return;
        }
        
        try {
            // 使用配置管理器保存设置
            boolean success = appConfig.saveServerUrl(serverUrl);
            
            if (success) {
                // 更新网络管理器
                networkManager.setServerUrl(serverUrl);
                
                // 更新显示
                tvCurrentUrl.setText("当前服务器: " + serverUrl);
                
                // 更新配置摘要
                TextView tvConfigSummary = findViewById(R.id.tv_config_summary);
                if (tvConfigSummary != null) {
                    updateConfigSummary(tvConfigSummary);
                }
                
                // 显示成功消息
                Toast.makeText(this, "设置保存成功！重启应用后仍会保持", Toast.LENGTH_LONG).show();
                
                // 更新保存状态显示
                showSaveStatus();
                
                // 自动测试连接
                testConnection();
                
            } else {
                Toast.makeText(this, "设置保存失败，请重试", Toast.LENGTH_SHORT).show();
            }
            
        } catch (Exception e) {
            Toast.makeText(this, "保存设置时出错: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }
    
    private void testConnection() {
        btnTestConnection.setEnabled(false);
        btnTestConnection.setText("测试中...");
        tvConnectionStatus.setText("连接状态: 测试中...");
        tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_blue_dark));
        
        networkManager.testConnection(new NetworkManager.ConnectionCallback() {
            @Override
            public void onSuccess(String message) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnTestConnection.setEnabled(true);
                        btnTestConnection.setText("测试连接");
                        tvConnectionStatus.setText("连接状态: 成功 ✓");
                        tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
                        Toast.makeText(SettingsActivity.this, "连接测试成功: " + message, Toast.LENGTH_SHORT).show();
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
                        tvConnectionStatus.setText("连接状态: 失败 ✗");
                        tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                        Toast.makeText(SettingsActivity.this, "连接测试失败: " + error, Toast.LENGTH_LONG).show();
                    }
                });
            }
        });
    }
    
    private void resetSettings() {
        try {
            // 使用配置管理器重置为默认值
            boolean success = appConfig.saveServerUrl(AppConfig.DEFAULT_SERVER_URL);
            
            if (success) {
                // 更新网络管理器
                networkManager.setServerUrl(AppConfig.DEFAULT_SERVER_URL);
                
                // 更新显示
                tvCurrentUrl.setText("当前服务器: " + AppConfig.DEFAULT_SERVER_URL);
                etServerUrl.setText(AppConfig.DEFAULT_SERVER_URL);
                tvConnectionStatus.setText("连接状态: 已重置");
                tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_blue_dark));
                
                // 更新配置摘要
                TextView tvConfigSummary = findViewById(R.id.tv_config_summary);
                if (tvConfigSummary != null) {
                    updateConfigSummary(tvConfigSummary);
                }
                
                Toast.makeText(this, "设置已重置为默认值", Toast.LENGTH_SHORT).show();
                
                // 更新保存状态显示
                showSaveStatus();
                
            } else {
                Toast.makeText(this, "重置设置失败，请重试", Toast.LENGTH_SHORT).show();
            }
            
        } catch (Exception e) {
            Toast.makeText(this, "重置设置时出错: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }
    
    private void showSaveStatus() {
        // 显示当前保存的配置信息
        String savedUrl = appConfig.getServerUrl();
        String status = "配置已保存到手机本地存储\n重启应用后仍会保持此设置";
        
        // 可以在界面上添加一个状态提示
        // 这里我们通过Toast来显示
        Toast.makeText(this, "当前配置: " + savedUrl, Toast.LENGTH_SHORT).show();
    }
    
    @Override
    protected void onResume() {
        super.onResume();
        // 每次回到设置页面时，重新加载当前设置
        loadCurrentSettings();
    }
}
