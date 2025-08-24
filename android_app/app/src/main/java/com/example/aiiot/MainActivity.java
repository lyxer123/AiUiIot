package com.example.aiiot;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import com.example.aiiot.config.AppConfig;
import com.example.aiiot.database.UserDatabaseHelper;
import com.example.aiiot.model.User;

public class MainActivity extends AppCompatActivity {
    
    private EditText etUsername, etPassword, etEmail;
    private Button btnLogin, btnRegister, btnLogout;
    private TextView tvStatus, tvCurrentUser;
    private CardView loginCard, mainCard;
    
    private AppConfig appConfig;
    private UserDatabaseHelper userDbHelper;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // 初始化配置管理器
        appConfig = AppConfig.getInstance(this);
        
        // 初始化数据库
        userDbHelper = new UserDatabaseHelper(this);
        
        // 初始化视图
        initViews();
        
        // 检查登录状态
        checkLoginStatus();
        
        // 设置点击事件
        setupClickListeners();
    }
    
    private void initViews() {
        etUsername = findViewById(R.id.et_username);
        etPassword = findViewById(R.id.et_password);
        etEmail = findViewById(R.id.et_email);
        btnLogin = findViewById(R.id.btn_login);
        btnRegister = findViewById(R.id.btn_register);
        btnLogout = findViewById(R.id.btn_logout);
        tvStatus = findViewById(R.id.tv_status);
        tvCurrentUser = findViewById(R.id.tv_current_user);
        loginCard = findViewById(R.id.login_card);
        mainCard = findViewById(R.id.main_card);
    }
    
    private void checkLoginStatus() {
        boolean isLoggedIn = appConfig.isLoggedIn();
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
        
        btnLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                performLogout();
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
        
        // 验证用户
        User user = userDbHelper.validateUser(username, password);
        if (user != null) {
            // 保存登录状态
            boolean success = appConfig.saveUserInfo(username, user.getId());
            
            if (success) {
                showMainInterface();
                Toast.makeText(this, "登录成功", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "登录状态保存失败", Toast.LENGTH_SHORT).show();
            }
        } else {
            Toast.makeText(this, "用户名或密码错误", Toast.LENGTH_SHORT).show();
        }
    }
    
    private void performRegister() {
        String username = etUsername.getText().toString().trim();
        String password = etPassword.getText().toString().trim();
        String email = etEmail.getText().toString().trim();
        
        if (username.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "请输入用户名和密码", Toast.LENGTH_SHORT).show();
            return;
        }
        
        if (password.length() < 6) {
            Toast.makeText(this, "密码长度至少6位", Toast.LENGTH_SHORT).show();
            return;
        }
        
        // 检查用户名是否已存在
        if (userDbHelper.isUsernameExists(username)) {
            Toast.makeText(this, "用户名已存在", Toast.LENGTH_SHORT).show();
            return;
        }
        
        // 创建新用户
        User newUser = new User(username, password, email);
        long userId = userDbHelper.addUser(newUser);
        
        if (userId != -1) {
            Toast.makeText(this, "注册成功，请登录", Toast.LENGTH_SHORT).show();
            // 清空输入框
            etUsername.setText("");
            etPassword.setText("");
            etEmail.setText("");
        } else {
            Toast.makeText(this, "注册失败，请重试", Toast.LENGTH_SHORT).show();
        }
    }
    
    private void performLogout() {
        // 使用配置管理器清除用户登录信息（保留服务器配置）
        boolean success = appConfig.clearUserInfo();
        
        if (success) {
            showLoginInterface();
            Toast.makeText(this, "已退出登录", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(this, "退出登录失败，请重试", Toast.LENGTH_SHORT).show();
        }
    }
    
    private void showLoginInterface() {
        loginCard.setVisibility(View.VISIBLE);
        mainCard.setVisibility(View.GONE);
        tvStatus.setText("请登录或注册");
    }
    
    private void showMainInterface() {
        loginCard.setVisibility(View.GONE);
        mainCard.setVisibility(View.VISIBLE);
        
        String username = appConfig.getUsername();
        tvCurrentUser.setText("当前用户: " + username);
        tvStatus.setText("登录成功，请选择功能");
    }
    
    // 导航到控制页面
    public void goToControl(View view) {
        Intent intent = new Intent(this, ControlActivity.class);
        startActivity(intent);
    }
    
    // 导航到数据监控页面
    public void goToDataMonitor(View view) {
        Intent intent = new Intent(this, DataMonitorActivity.class);
        startActivity(intent);
    }
    
    // 导航到设置页面
    public void goToSettings(View view) {
        Intent intent = new Intent(this, SettingsActivity.class);
        startActivity(intent);
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (userDbHelper != null) {
            userDbHelper.close();
        }
    }
}