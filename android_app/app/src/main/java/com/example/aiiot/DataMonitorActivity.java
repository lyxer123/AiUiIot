package com.example.aiiot;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.aiiot.adapter.DataAdapter;
import com.example.aiiot.model.ESP32Data;
import com.example.aiiot.network.NetworkManager;

import java.util.ArrayList;
import java.util.List;

public class DataMonitorActivity extends AppCompatActivity {
    
    private TextView tvCurrentValue, tvLastUpdate, tvDataCount;
    private Button btnRefresh, btnLoadMore;
    private RecyclerView recyclerView;
    
    private NetworkManager networkManager;
    private DataAdapter dataAdapter;
    private Handler handler;
    private Runnable refreshRunnable;
    private static final int REFRESH_INTERVAL = 10000; // 10秒刷新一次
    
    private List<ESP32Data> dataList;
    private int currentLimit = 50;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_data_monitor);
        
        // 初始化网络管理器
        networkManager = new NetworkManager(this);
        
        // 初始化数据列表
        dataList = new ArrayList<>();
        
        // 初始化视图
        initViews();
        
        // 初始化RecyclerView
        initRecyclerView();
        
        // 初始化Handler
        handler = new Handler(Looper.getMainLooper());
        
        // 设置点击事件
        setupClickListeners();
        
        // 开始数据监控
        startDataMonitoring();
        
        // 加载初始数据
        loadData();
    }
    
    private void initViews() {
        tvCurrentValue = findViewById(R.id.tv_current_value);
        tvLastUpdate = findViewById(R.id.tv_last_update);
        tvDataCount = findViewById(R.id.tv_data_count);
        btnRefresh = findViewById(R.id.btn_refresh);
        btnLoadMore = findViewById(R.id.btn_load_more);
        recyclerView = findViewById(R.id.recycler_view);
    }
    
    private void initRecyclerView() {
        dataAdapter = new DataAdapter(dataList);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(dataAdapter);
    }
    
    private void setupClickListeners() {
        btnRefresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                refreshData();
            }
        });
        
        btnLoadMore.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loadMoreData();
            }
        });
    }
    
    private void startDataMonitoring() {
        refreshRunnable = new Runnable() {
            @Override
            public void run() {
                refreshData();
                handler.postDelayed(this, REFRESH_INTERVAL);
            }
        };
        handler.post(refreshRunnable);
    }
    
    private void loadData() {
        btnRefresh.setEnabled(false);
        btnRefresh.setText("加载中...");
        
        networkManager.getAD1Data(currentLimit, new NetworkManager.DataCallback<List<ESP32Data>>() {
            @Override
            public void onSuccess(List<ESP32Data> data) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        updateDataDisplay(data);
                        btnRefresh.setEnabled(true);
                        btnRefresh.setText("刷新数据");
                    }
                });
            }
            
            @Override
            public void onFailure(String error) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnRefresh.setEnabled(true);
                        btnRefresh.setText("刷新数据");
                        Toast.makeText(DataMonitorActivity.this, "数据加载失败: " + error, Toast.LENGTH_LONG).show();
                        updateDataDisplay(new ArrayList<>()); // 显示空数据
                    }
                });
            }
        });
    }
    
    private void refreshData() {
        btnRefresh.setEnabled(false);
        btnRefresh.setText("刷新中...");
        
        networkManager.getAD1Data(currentLimit, new NetworkManager.DataCallback<List<ESP32Data>>() {
            @Override
            public void onSuccess(List<ESP32Data> data) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        updateDataDisplay(data);
                        btnRefresh.setEnabled(true);
                        btnRefresh.setText("刷新数据");
                        Toast.makeText(DataMonitorActivity.this, "数据刷新成功", Toast.LENGTH_SHORT).show();
                    }
                });
            }
            
            @Override
            public void onFailure(String error) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnRefresh.setEnabled(true);
                        btnRefresh.setText("刷新数据");
                        Toast.makeText(DataMonitorActivity.this, "数据刷新失败: " + error, Toast.LENGTH_LONG).show();
                    }
                });
            }
        });
    }
    
    private void loadMoreData() {
        btnLoadMore.setEnabled(false);
        btnLoadMore.setText("加载中...");
        
        int newLimit = currentLimit + 50;
        networkManager.getAD1Data(newLimit, new NetworkManager.DataCallback<List<ESP32Data>>() {
            @Override
            public void onSuccess(List<ESP32Data> data) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        currentLimit = newLimit;
                        updateDataDisplay(data);
                        btnLoadMore.setEnabled(true);
                        btnLoadMore.setText("加载更多");
                        Toast.makeText(DataMonitorActivity.this, "成功加载更多数据", Toast.LENGTH_SHORT).show();
                    }
                });
            }
            
            @Override
            public void onFailure(String error) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btnLoadMore.setEnabled(true);
                        btnLoadMore.setText("加载更多");
                        Toast.makeText(DataMonitorActivity.this, "加载更多失败: " + error, Toast.LENGTH_LONG).show();
                    }
                });
            }
        });
    }
    
    private void updateDataDisplay(List<ESP32Data> data) {
        if (data != null && !data.isEmpty()) {
            // 验证数据有效性
            List<ESP32Data> validData = new ArrayList<>();
            for (ESP32Data item : data) {
                if (item.getAd1Value() >= 0 && item.getTimestamp() > 0) {
                    validData.add(item);
                }
            }
            
            if (!validData.isEmpty()) {
                dataList.clear();
                dataList.addAll(validData);
                dataAdapter.notifyDataSetChanged();
                
                // 更新当前值显示
                ESP32Data latestData = validData.get(0);
                tvCurrentValue.setText("当前AD值: " + latestData.getAd1Value());
                tvLastUpdate.setText("最后更新: " + latestData.getFormattedTimestamp());
                tvDataCount.setText("数据条数: " + validData.size());
            } else {
                showNoDataMessage();
            }
        } else {
            showNoDataMessage();
        }
    }
    
    private void showNoDataMessage() {
        dataList.clear();
        dataAdapter.notifyDataSetChanged();
        
        tvCurrentValue.setText("当前AD值: 无数据");
        tvLastUpdate.setText("最后更新: 无");
        tvDataCount.setText("数据条数: 0");
        
        Toast.makeText(this, "暂无有效数据", Toast.LENGTH_SHORT).show();
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (handler != null && refreshRunnable != null) {
            handler.removeCallbacks(refreshRunnable);
        }
    }
}
