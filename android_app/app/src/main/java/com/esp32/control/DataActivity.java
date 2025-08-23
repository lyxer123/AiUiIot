package com.esp32.control;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.esp32.control.adapter.DataAdapter;
import com.esp32.control.model.AD1Data;
import com.esp32.control.network.NetworkManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class DataActivity extends AppCompatActivity {
    
    private NetworkManager networkManager;
    private Handler handler;
    
    private TextView tvCurrentValue, tvLastUpdate, tvDataCount;
    private Button btnRefresh, btnLoadMore;
    private ProgressBar progressBar;
    private RecyclerView recyclerView;
    
    private DataAdapter dataAdapter;
    private List<AD1Data> dataList;
    
    private boolean isLoading = false;
    private int currentLimit = 50;
    private static final int REFRESH_INTERVAL = 10000; // 10秒刷新一次
    private Runnable refreshRunnable;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_data);
        
        // 初始化网络管理器
        networkManager = new NetworkManager(this);
        
        // 初始化Handler
        handler = new Handler(Looper.getMainLooper());
        
        // 初始化数据列表
        dataList = new ArrayList<>();
        
        // 初始化视图
        initViews();
        
        // 设置RecyclerView
        setupRecyclerView();
        
        // 设置点击事件
        setupClickListeners();
        
        // 开始自动刷新
        startAutoRefresh();
        
        // 加载初始数据
        loadData();
    }
    
    private void initViews() {
        tvCurrentValue = findViewById(R.id.tv_current_value);
        tvLastUpdate = findViewById(R.id.tv_last_update);
        tvDataCount = findViewById(R.id.tv_data_count);
        btnRefresh = findViewById(R.id.btn_refresh);
        btnLoadMore = findViewById(R.id.btn_load_more);
        progressBar = findViewById(R.id.progress_bar);
        recyclerView = findViewById(R.id.recycler_view);
    }
    
    private void setupRecyclerView() {
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
    
    private void startAutoRefresh() {
        refreshRunnable = new Runnable() {
            @Override
            public void run() {
                refreshCurrentValue();
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
    
    private void loadData() {
        if (isLoading) return;
        
        isLoading = true;
        showLoading(true);
        
        networkManager.getAD1Data(currentLimit, new NetworkManager.NetworkCallback() {
            @Override
            public void onSuccess(String response) {
                try {
                    JSONObject jsonResponse = new JSONObject(response);
                    if (jsonResponse.getBoolean("success")) {
                        JSONArray dataArray = jsonResponse.getJSONArray("data");
                        parseDataArray(dataArray);
                        updateUI();
                    } else {
                        Toast.makeText(DataActivity.this, 
                            "获取数据失败: " + jsonResponse.getString("error"), Toast.LENGTH_SHORT).show();
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                    Toast.makeText(DataActivity.this, "数据解析失败", Toast.LENGTH_SHORT).show();
                }
                
                isLoading = false;
                showLoading(false);
            }
            
            @Override
            public void onError(String error) {
                Toast.makeText(DataActivity.this, "网络错误: " + error, Toast.LENGTH_SHORT).show();
                isLoading = false;
                showLoading(false);
            }
        });
    }
    
    private void refreshData() {
        currentLimit = 50;
        loadData();
    }
    
    private void loadMoreData() {
        if (isLoading) return;
        
        currentLimit += 50;
        loadData();
    }
    
    private void refreshCurrentValue() {
        // 只获取最新的一条数据来更新当前值
        networkManager.getAD1Data(1, new NetworkManager.NetworkCallback() {
            @Override
            public void onSuccess(String response) {
                try {
                    JSONObject jsonResponse = new JSONObject(response);
                    if (jsonResponse.getBoolean("success")) {
                        JSONArray dataArray = jsonResponse.getJSONArray("data");
                        if (dataArray.length() > 0) {
                            JSONObject latestData = dataArray.getJSONObject(0);
                            updateCurrentValue(latestData);
                        }
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            
            @Override
            public void onError(String error) {
                // 静默处理，不显示错误提示
            }
        });
    }
    
    private void parseDataArray(JSONArray dataArray) throws JSONException {
        dataList.clear();
        
        for (int i = 0; i < dataArray.length(); i++) {
            JSONObject dataObj = dataArray.getJSONObject(i);
            AD1Data data = new AD1Data();
            
            data.setId(dataObj.getInt("id"));
            data.setValue(dataObj.getDouble("value"));
            data.setTimestamp(dataObj.getString("timestamp"));
            
            dataList.add(data);
        }
    }
    
    private void updateCurrentValue(JSONObject latestData) throws JSONException {
        final double value = latestData.getDouble("value");
        final String timestamp = latestData.getString("timestamp");
        
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                tvCurrentValue.setText(String.format(Locale.getDefault(), "%.2f", value));
                tvLastUpdate.setText("最后更新: " + formatTimestamp(timestamp));
            }
        });
    }
    
    private void updateUI() {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                tvDataCount.setText("数据条数: " + dataList.size());
                dataAdapter.notifyDataSetChanged();
                
                // 更新当前值显示
                if (!dataList.isEmpty()) {
                    AD1Data latestData = dataList.get(0);
                    tvCurrentValue.setText(String.format(Locale.getDefault(), "%.2f", latestData.getValue()));
                    tvLastUpdate.setText("最后更新: " + formatTimestamp(latestData.getTimestamp()));
                }
            }
        });
    }
    
    private void showLoading(boolean show) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                progressBar.setVisibility(show ? View.VISIBLE : View.GONE);
                btnRefresh.setEnabled(!show);
                btnLoadMore.setEnabled(!show);
            }
        });
    }
    
    private String formatTimestamp(String timestamp) {
        try {
            // 假设时间戳是ISO格式，转换为本地时间
            SimpleDateFormat inputFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault());
            SimpleDateFormat outputFormat = new SimpleDateFormat("MM-dd HH:mm:ss", Locale.getDefault());
            
            Date date = inputFormat.parse(timestamp);
            return outputFormat.format(date);
        } catch (Exception e) {
            return timestamp;
        }
    }
}
