package com.example.aiiot.model;

public class User {
    private int id;
    private String username;
    private String password;
    private String email;
    private long createTime;
    private boolean isActive;

    public User() {}

    public User(String username, String password) {
        this.username = username;
        this.password = password;
        this.createTime = System.currentTimeMillis();
        this.isActive = true;
    }

    public User(String username, String password, String email) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.createTime = System.currentTimeMillis();
        this.isActive = true;
    }

    // Getters and Setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public long getCreateTime() { return createTime; }
    public void setCreateTime(long createTime) { this.createTime = createTime; }

    public boolean isActive() { return isActive; }
    public void setActive(boolean active) { isActive = active; }
}
