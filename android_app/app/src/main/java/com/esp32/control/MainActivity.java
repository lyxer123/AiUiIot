package com.esp32.control;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

public class MainActivity extends AppCompatActivity {
    
    private EditText etUsername, etPassword;
    private Button btnLogin, btnRegister;
    private TextView tvStatus;
    private CardView loginCard, mainCard;
    
    private SharedPreferences sharedPreferences;
    private static final String PREF_NAME = "ESP32Control";
    private static final String KEY_USERNAME = "username";
    private static final String KEY_IS_LOGGED_IN = "is_logged_in";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // 初始化视图
        initViews();
        
        // 初始化SharedPreferences
        sharedPreferences = getSharedPreferences(PREF_NAME, MODE_PRIVATE);
        
        // 检查登录状态
        checkLoginStatus();
        
        // 设置点击事件
        setupClickListeners();
    }
    
    private void initViews() {
        etUsername = findViewById(R.id.et_username);
        etPassword = findViewById(R.id.et_password);
        btnLogin = findViewById(R.id.btn_login);
        btnRegister = findViewById(R.id.btn_register);
        tvStatus = findViewById(R.id.tv_status);
        loginCard = findViewById(R.id.login_card);
        mainCard = findViewById(R.id.main_card);
    }
    
    private void checkLoginStatus() {
        boolean isLoggedIn = sharedPreferences.getBoolean(KEY_IS_LOGGED_IN, false);
        if (isLoggedIn) {
            showMainInterface();
        } else {
            showLoginInterface();
        }
    }
    
    private void setupClickListeners() {
        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                performLogin();
            }
        });
        
        btnRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                performRegister();
            }
        });
    }
    
    private void performLogin() {
        String username = etUsername.getText().toString().trim();
        String password = etPassword.getText().toString().trim();
        
        if (username.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "请输入用户名和密码", Toast.LENGTH_SHORT).show();
            return;
        }
        
        // 检查用户凭据（这里使用简单的本地验证）
        if (validateUser(username, password)) {
            // 保存登录状态
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putString(KEY_USERNAME, username);
            editor.putBoolean(KEY_IS_LOGGED_IN, true);
            editor.apply();
            
            showMainInterface();
            Toast.makeText(this, "登录成功", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(this, "用户名或密码错误", Toast.LENGTH_SHORT).show();
        }
    }
    
    private void performRegister() {
        String username = etUsername.getText().toString().trim();
        String password = etPassword.getText().toString().trim();
        
        if (username.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "请输入用户名和密码", Toast.LENGTH_SHORT).show();
            return;
        }
        
        if (password.length() < 6) {
            Toast.makeText(this, "密码长度至少6位", Toast.LENGTH_SHORT).show();
            return;
        }
        
        // 注册新用户
        if (registerUser(username, password)) {
            Toast.makeText(this, "注册成功，请登录", Toast.LENGTH_SHORT).show();
            etPassword.setText("");
        } else {
            Toast.makeText(this, "用户名已存在", Toast.LENGTH_SHORT).show();
        }
    }
    
    private boolean validateUser(String username, String password) {
        // 从SharedPreferences获取用户信息
        String storedPassword = sharedPreferences.getString("user_" + username, "");
        return !storedPassword.isEmpty() && storedPassword.equals(password);
    }
    
    private boolean registerUser(String username, String password) {
        // 检查用户是否已存在
        if (sharedPreferences.contains("user_" + username)) {
            return false;
        }
        
        // 保存新用户信息
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("user_" + username, password);
        editor.apply();
        
        return true;
    }
    
    private void showLoginInterface() {
        loginCard.setVisibility(View.VISIBLE);
        mainCard.setVisibility(View.GONE);
    }
    
    private void showMainInterface() {
        loginCard.setVisibility(View.GONE);
        mainCard.setVisibility(View.VISIBLE);
        
        // 显示欢迎信息
        String username = sharedPreferences.getString(KEY_USERNAME, "");
        tvStatus.setText("欢迎回来，" + username);
    }
    
    // 主界面按钮点击事件
    public void onControlClick(View view) {
        Intent intent = new Intent(this, ControlActivity.class);
        startActivity(intent);
    }
    
    public void onDataClick(View view) {
        Intent intent = new Intent(this, DataActivity.class);
        startActivity(intent);
    }
    
    public void onSettingsClick(View view) {
        Intent intent = new Intent(this, SettingsActivity.class);
        startActivity(intent);
    }
    
    public void onLogoutClick(View view) {
        // 清除登录状态
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.clear();
        editor.apply();
        
        showLoginInterface();
        Toast.makeText(this, "已退出登录", Toast.LENGTH_SHORT).show();
    }
}
