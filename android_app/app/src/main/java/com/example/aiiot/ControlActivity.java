package com.example.aiiot;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import com.example.aiiot.network.NetworkManager;

public class ControlActivity extends AppCompatActivity {
    
    private TextView tvConnectionStatus, tvIo1Status, tvMqttStatus, tvSystemStatus;
    private Switch switchIo1;
    private Button btnRefresh, btnTestConnection;
    private CardView statusCard, controlCard;
    
    private NetworkManager networkManager;
    private Handler handler;
    private Runnable statusRunnable;
    private static final int REFRESH_INTERVAL = 5000; // 5秒刷新一次
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_control);
        
        // 初始化网络管理器
        networkManager = new NetworkManager(this);
        
        // 初始化视图
        initViews();
        
        // 初始化Handler
        handler = new Handler(Looper.getMainLooper());
        
        // 设置点击事件
        setupClickListeners();
        
        // 开始状态监控
        startStatusMonitoring();
    }
    
    private void initViews() {
        tvConnectionStatus = findViewById(R.id.tv_connection_status);
        tvIo1Status = findViewById(R.id.tv_io1_status);
        tvMqttStatus = findViewById(R.id.tv_mqtt_status);
        tvSystemStatus = findViewById(R.id.tv_system_status);
        switchIo1 = findViewById(R.id.switch_io1);
        btnRefresh = findViewById(R.id.btn_refresh);
        btnTestConnection = findViewById(R.id.btn_test_connection);
        statusCard = findViewById(R.id.status_card);
        controlCard = findViewById(R.id.control_card);
    }
    
    private void setupClickListeners() {
        btnRefresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                refreshStatus();
            }
        });
        
        btnTestConnection.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                testConnection();
            }
        });
        
        switchIo1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                controlIo1(switchIo1.isChecked());
            }
        });
    }
    
    private void startStatusMonitoring() {
        statusRunnable = new Runnable() {
            @Override
            public void run() {
                refreshStatus();
                handler.postDelayed(this, REFRESH_INTERVAL);
            }
        };
        handler.post(statusRunnable);
    }
    
    private void refreshStatus() {
        networkManager.getSystemStatus(new NetworkManager.StatusCallback() {
            @Override
            public void onSuccess(boolean mqttConnected, boolean io1State, String systemStatus) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        updateStatusDisplay(mqttConnected, io1State, systemStatus);
                    }
                });
            }
            
            @Override
            public void onFailure(String error) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        updateStatusDisplay(false, false, "error");
                        Toast.makeText(ControlActivity.this, "状态获取失败: " + error, Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });
    }
    
    private void updateStatusDisplay(boolean mqttConnected, boolean io1State, String systemStatus) {
        // 更新MQTT状态
        if (mqttConnected) {
            tvMqttStatus.setText("MQTT: 已连接");
            tvMqttStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
        } else {
            tvMqttStatus.setText("MQTT: 未连接");
            tvMqttStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
        }
        
        // 更新IO1状态
        tvIo1Status.setText("IO1: " + (io1State ? "开启" : "关闭"));
        switchIo1.setChecked(io1State);
        
        // 更新系统状态
        if ("running".equals(systemStatus)) {
            tvSystemStatus.setText("系统: 运行中");
            tvSystemStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
            controlCard.setVisibility(View.VISIBLE);
        } else {
            tvSystemStatus.setText("系统: " + systemStatus);
            tvSystemStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
            controlCard.setVisibility(View.GONE);
        }
        
        // 更新连接状态
        if (mqttConnected && "running".equals(systemStatus)) {
            tvConnectionStatus.setText("连接状态: 正常");
            tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
        } else {
            tvConnectionStatus.setText("连接状态: 异常");
            tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
        }
    }
    
    private void testConnection() {
        btnTestConnection.setEnabled(false);
        btnTestConnection.setText("测试中...");
        
        networkManager.testConnection(new NetworkManager.ConnectionCallback() {
            @Override
            public void onSuccess(String message) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnTestConnection.setEnabled(true);
                        btnTestConnection.setText("测试连接");
                        Toast.makeText(ControlActivity.this, message, Toast.LENGTH_SHORT).show();
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
                        Toast.makeText(ControlActivity.this, error, Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });
    }
    
    private void controlIo1(boolean state) {
        // 禁用开关，防止重复操作
        switchIo1.setEnabled(false);
        
        networkManager.controlIO1(state, new NetworkManager.ControlCallback() {
            @Override
            public void onSuccess(String message) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switchIo1.setEnabled(true);
                        Toast.makeText(ControlActivity.this, message, Toast.LENGTH_SHORT).show();
                        // 刷新状态
                        refreshStatus();
                    }
                });
            }
            
            @Override
            public void onFailure(String error) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switchIo1.setEnabled(true);
                        // 恢复开关状态
                        switchIo1.setChecked(!state);
                        Toast.makeText(ControlActivity.this, error, Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (handler != null && statusRunnable != null) {
            handler.removeCallbacks(statusRunnable);
        }
    }
}
