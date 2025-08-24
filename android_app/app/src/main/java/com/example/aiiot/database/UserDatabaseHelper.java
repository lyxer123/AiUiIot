package com.example.aiiot.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import com.example.aiiot.model.User;

import java.util.ArrayList;
import java.util.List;

public class UserDatabaseHelper extends SQLiteOpenHelper {
    private static final String TAG = "UserDatabaseHelper";
    private static final String DATABASE_NAME = "ESP32UserDB";
    private static final int DATABASE_VERSION = 1;
    
    // 用户表
    private static final String TABLE_USERS = "users";
    private static final String COLUMN_ID = "id";
    private static final String COLUMN_USERNAME = "username";
    private static final String COLUMN_PASSWORD = "password";
    private static final String COLUMN_EMAIL = "email";
    private static final String COLUMN_CREATE_TIME = "create_time";
    private static final String COLUMN_IS_ACTIVE = "is_active";
    
    // 创建用户表SQL
    private static final String CREATE_TABLE_USERS = 
            "CREATE TABLE " + TABLE_USERS + " (" +
                    COLUMN_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                    COLUMN_USERNAME + " TEXT UNIQUE NOT NULL, " +
                    COLUMN_PASSWORD + " TEXT NOT NULL, " +
                    COLUMN_EMAIL + " TEXT, " +
                    COLUMN_CREATE_TIME + " INTEGER NOT NULL, " +
                    COLUMN_IS_ACTIVE + " INTEGER DEFAULT 1" +
                    ")";
    
    public UserDatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }
    
    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(CREATE_TABLE_USERS);
        Log.d(TAG, "用户数据库表创建成功");
    }
    
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_USERS);
        onCreate(db);
    }
    
    // 添加新用户
    public long addUser(User user) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        
        values.put(COLUMN_USERNAME, user.getUsername());
        values.put(COLUMN_PASSWORD, user.getPassword());
        values.put(COLUMN_EMAIL, user.getEmail());
        values.put(COLUMN_CREATE_TIME, user.getCreateTime());
        values.put(COLUMN_IS_ACTIVE, user.isActive() ? 1 : 0);
        
        long id = db.insert(TABLE_USERS, null, values);
        db.close();
        
        if (id != -1) {
            Log.d(TAG, "用户添加成功: " + user.getUsername());
        } else {
            Log.e(TAG, "用户添加失败: " + user.getUsername());
        }
        
        return id;
    }
    
    // 验证用户登录
    public User validateUser(String username, String password) {
        SQLiteDatabase db = this.getReadableDatabase();
        User user = null;
        
        String[] columns = {COLUMN_ID, COLUMN_USERNAME, COLUMN_PASSWORD, COLUMN_EMAIL, COLUMN_CREATE_TIME, COLUMN_IS_ACTIVE};
        String selection = COLUMN_USERNAME + " = ? AND " + COLUMN_PASSWORD + " = ? AND " + COLUMN_IS_ACTIVE + " = 1";
        String[] selectionArgs = {username, password};
        
        Cursor cursor = db.query(TABLE_USERS, columns, selection, selectionArgs, null, null, null);
        
        if (cursor.moveToFirst()) {
            user = new User();
            user.setId(cursor.getInt(cursor.getColumnIndex(COLUMN_ID)));
            user.setUsername(cursor.getString(cursor.getColumnIndex(COLUMN_USERNAME)));
            user.setPassword(cursor.getString(cursor.getColumnIndex(COLUMN_PASSWORD)));
            user.setEmail(cursor.getString(cursor.getColumnIndex(COLUMN_EMAIL)));
            user.setCreateTime(cursor.getLong(cursor.getColumnIndex(COLUMN_CREATE_TIME)));
            user.setActive(cursor.getInt(cursor.getColumnIndex(COLUMN_IS_ACTIVE)) == 1);
        }
        
        cursor.close();
        db.close();
        
        if (user != null) {
            Log.d(TAG, "用户验证成功: " + username);
        } else {
            Log.d(TAG, "用户验证失败: " + username);
        }
        
        return user;
    }
    
    // 检查用户名是否存在
    public boolean isUsernameExists(String username) {
        SQLiteDatabase db = this.getReadableDatabase();
        
        String[] columns = {COLUMN_ID};
        String selection = COLUMN_USERNAME + " = ?";
        String[] selectionArgs = {username};
        
        Cursor cursor = db.query(TABLE_USERS, columns, selection, selectionArgs, null, null, null);
        boolean exists = cursor.getCount() > 0;
        
        cursor.close();
        db.close();
        
        return exists;
    }
    
    // 获取所有用户
    public List<User> getAllUsers() {
        List<User> userList = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        
        String[] columns = {COLUMN_ID, COLUMN_USERNAME, COLUMN_PASSWORD, COLUMN_EMAIL, COLUMN_CREATE_TIME, COLUMN_IS_ACTIVE};
        String orderBy = COLUMN_CREATE_TIME + " DESC";
        
        Cursor cursor = db.query(TABLE_USERS, columns, null, null, null, null, orderBy);
        
        if (cursor.moveToFirst()) {
            do {
                User user = new User();
                user.setId(cursor.getInt(cursor.getColumnIndex(COLUMN_ID)));
                user.setUsername(cursor.getString(cursor.getColumnIndex(COLUMN_USERNAME)));
                user.setPassword(cursor.getString(cursor.getColumnIndex(COLUMN_PASSWORD)));
                user.setEmail(cursor.getString(cursor.getColumnIndex(COLUMN_EMAIL)));
                user.setCreateTime(cursor.getLong(cursor.getColumnIndex(COLUMN_CREATE_TIME)));
                user.setActive(cursor.getInt(cursor.getColumnIndex(COLUMN_IS_ACTIVE)) == 1);
                userList.add(user);
            } while (cursor.moveToNext());
        }
        
        cursor.close();
        db.close();
        
        return userList;
    }
    
    // 更新用户信息
    public int updateUser(User user) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        
        values.put(COLUMN_USERNAME, user.getUsername());
        values.put(COLUMN_PASSWORD, user.getPassword());
        values.put(COLUMN_EMAIL, user.getEmail());
        values.put(COLUMN_IS_ACTIVE, user.isActive() ? 1 : 0);
        
        String whereClause = COLUMN_ID + " = ?";
        String[] whereArgs = {String.valueOf(user.getId())};
        
        int rowsAffected = db.update(TABLE_USERS, values, whereClause, whereArgs);
        db.close();
        
        if (rowsAffected > 0) {
            Log.d(TAG, "用户更新成功: " + user.getUsername());
        } else {
            Log.e(TAG, "用户更新失败: " + user.getUsername());
        }
        
        return rowsAffected;
    }
    
    // 删除用户
    public int deleteUser(int userId) {
        SQLiteDatabase db = this.getWritableDatabase();
        
        String whereClause = COLUMN_ID + " = ?";
        String[] whereArgs = {String.valueOf(userId)};
        
        int rowsAffected = db.delete(TABLE_USERS, whereClause, whereArgs);
        db.close();
        
        if (rowsAffected > 0) {
            Log.d(TAG, "用户删除成功: ID=" + userId);
        } else {
            Log.e(TAG, "用户删除失败: ID=" + userId);
        }
        
        return rowsAffected;
    }
    
    // 获取用户数量
    public int getUserCount() {
        SQLiteDatabase db = this.getReadableDatabase();
        
        String countQuery = "SELECT COUNT(*) FROM " + TABLE_USERS;
        Cursor cursor = db.rawQuery(countQuery, null);
        
        int count = 0;
        if (cursor.moveToFirst()) {
            count = cursor.getInt(0);
        }
        
        cursor.close();
        db.close();
        
        return count;
    }
}
