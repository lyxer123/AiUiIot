package com.esp32.control;

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

import com.esp32.control.network.NetworkManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class ControlActivity extends AppCompatActivity {
    
    private NetworkManager networkManager;
    private Handler handler;
    
    private TextView tvConnectionStatus, tvDeviceStatus, tvLastUpdate;
    private Switch switchIO1;
    private Button btnRefresh, btnTestConnection;
    private CardView statusCard, controlCard;
    
    private boolean isConnected = false;
    private boolean isDeviceOnline = false;
    private boolean currentIO1State = false;
    
    private static final int REFRESH_INTERVAL = 5000; // 5秒刷新一次
    private Runnable refreshRunnable;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_control);
        
        // 初始化网络管理器
        networkManager = new NetworkManager(this);
        
        // 初始化Handler
        handler = new Handler(Looper.getMainLooper());
        
        // 初始化视图
        initViews();
        
        // 设置点击事件
        setupClickListeners();
        
        // 开始自动刷新
        startAutoRefresh();
    }
    
    private void initViews() {
        tvConnectionStatus = findViewById(R.id.tv_connection_status);
        tvDeviceStatus = findViewById(R.id.tv_device_status);
        tvLastUpdate = findViewById(R.id.tv_last_update);
        switchIO1 = findViewById(R.id.switch_io1);
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
        
        switchIO1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // 防止在状态更新时触发
                if (switchIO1.isEnabled()) {
                    controlIO1(switchIO1.isChecked());
                }
            }
        });
    }
    
    private void startAutoRefresh() {
        refreshRunnable = new Runnable() {
            @Override
            public void run() {
                refreshStatus();
                handler.postDelayed(this, REFRESH_INTERVAL);
            }
        };
        handler.post(refreshRunnable);
    }
    
    private void stopAutoRefresh() {
        if (refreshRunnable != null) {
            handler.removeCallbacks(refreshRunnable);
        }
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        stopAutoRefresh();
    }
    
    private void refreshStatus() {
        // 获取系统状态
        networkManager.getSystemStatus(new NetworkManager.NetworkCallback() {
            @Override
            public void onSuccess(String response) {
                try {
                    JSONObject jsonResponse = new JSONObject(response);
                    if (jsonResponse.getBoolean("success")) {
                        JSONObject data = jsonResponse.getJSONObject("data");
                        isConnected = data.getBoolean("mqtt_connected");
                        isDeviceOnline = data.getString("system_status").equals("运行中");
                        
                        updateStatusUI();
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            
            @Override
            public void onError(String error) {
                isConnected = false;
                isDeviceOnline = false;
                updateStatusUI();
            }
        });
        
        // 获取IO1当前状态
        networkManager.getIO1CurrentState(new NetworkManager.NetworkCallback() {
            @Override
            public void onSuccess(String response) {
                try {
                    JSONObject jsonResponse = new JSONObject(response);
                    if (jsonResponse.getBoolean("success")) {
                        JSONObject data = jsonResponse.getJSONObject("data");
                        currentIO1State = data.getBoolean("state");
                        updateIO1UI();
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            
            @Override
            public void onError(String error) {
                // 保持当前状态
            }
        });
    }
    
    private void updateStatusUI() {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                // 更新连接状态
                if (isConnected) {
                    tvConnectionStatus.setText("已连接");
                    tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
                } else {
                    tvConnectionStatus.setText("未连接");
                    tvConnectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                }
                
                // 更新设备状态
                if (isDeviceOnline) {
                    tvDeviceStatus.setText("在线");
                    tvDeviceStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
                } else {
                    tvDeviceStatus.setText("离线");
                    tvDeviceStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                }
                
                // 更新最后更新时间
                tvLastUpdate.setText("最后更新: " + getCurrentTime());
                
                // 根据连接状态启用/禁用控制
                boolean canControl = isConnected && isDeviceOnline;
                switchIO1.setEnabled(canControl);
                controlCard.setAlpha(canControl ? 1.0f : 0.5f);
            }
        });
    }
    
    private void updateIO1UI() {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                // 暂时禁用开关，防止触发点击事件
                switchIO1.setOnClickListener(null);
                switchIO1.setChecked(currentIO1State);
                switchIO1.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (switchIO1.isEnabled()) {
                            controlIO1(switchIO1.isChecked());
                        }
                    }
                });
            }
        });
    }
    
    private void controlIO1(boolean state) {
        // 显示加载状态
        switchIO1.setEnabled(false);
        
        networkManager.controlIO1(state, new NetworkManager.NetworkCallback() {
            @Override
            public void onSuccess(String response) {
                try {
                    JSONObject jsonResponse = new JSONObject(response);
                    if (jsonResponse.getBoolean("success")) {
                        currentIO1State = state;
                        Toast.makeText(ControlActivity.this, 
                            "IO1已" + (state ? "开启" : "关闭"), Toast.LENGTH_SHORT).show();
                    } else {
                        // 控制失败，恢复原状态
                        switchIO1.setChecked(!state);
                        Toast.makeText(ControlActivity.this, 
                            "控制失败: " + jsonResponse.getString("error"), Toast.LENGTH_SHORT).show();
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                    switchIO1.setChecked(!state);
                    Toast.makeText(ControlActivity.this, "响应解析失败", Toast.LENGTH_SHORT).show();
                }
                
                // 重新启用开关
                switchIO1.setEnabled(true);
            }
            
            @Override
            public void onError(String error) {
                // 控制失败，恢复原状态
                switchIO1.setChecked(!state);
                switchIO1.setEnabled(true);
                Toast.makeText(ControlActivity.this, "网络错误: " + error, Toast.LENGTH_SHORT).show();
            }
        });
    }
    
    private void testConnection() {
        btnTestConnection.setEnabled(false);
        btnTestConnection.setText("测试中...");
        
        networkManager.testConnection(new NetworkManager.NetworkCallback() {
            @Override
            public void onSuccess(String response) {
                try {
                    JSONObject jsonResponse = new JSONObject(response);
                    if (jsonResponse.getBoolean("success")) {
                        Toast.makeText(ControlActivity.this, "连接正常", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(ControlActivity.this, "连接异常", Toast.LENGTH_SHORT).show();
                    }
                } catch (JSONException e) {
                    Toast.makeText(ControlActivity.this, "响应解析失败", Toast.LENGTH_SHORT).show();
                }
                
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnTestConnection.setEnabled(true);
                        btnTestConnection.setText("测试连接");
                    }
                });
            }
            
            @Override
            public void onError(String error) {
                Toast.makeText(ControlActivity.this, "连接失败: " + error, Toast.LENGTH_SHORT).show();
                
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnTestConnection.setEnabled(true);
                        btnTestConnection.setText("测试连接");
                    }
                });
            }
        });
    }
    
    private String getCurrentTime() {
        java.text.SimpleDateFormat sdf = new java.text.SimpleDateFormat("HH:mm:ss");
        return sdf.format(new java.util.Date());
    }
}
