package com.example.aiiot.adapter;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.aiiot.R;
import com.example.aiiot.model.ESP32Data;

import java.util.List;

public class DataAdapter extends RecyclerView.Adapter<DataAdapter.DataViewHolder> {
    private static final String TAG = "DataAdapter";
    
    private List<ESP32Data> dataList;
    
    public DataAdapter(List<ESP32Data> dataList) {
        this.dataList = dataList;
    }
    
    @NonNull
    @Override
    public DataViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_data, parent, false);
        return new DataViewHolder(view);
    }
    
    @Override
    public void onBindViewHolder(@NonNull DataViewHolder holder, int position) {
        try {
            ESP32Data data = dataList.get(position);
            if (data != null) {
                holder.bind(data, position);
            } else {
                holder.bindError("数据无效", position);
            }
        } catch (Exception e) {
            Log.e(TAG, "绑定数据失败，位置: " + position, e);
            holder.bindError("数据错误", position);
        }
    }
    
    @Override
    public int getItemCount() {
        return dataList != null ? dataList.size() : 0;
    }
    
    public void updateData(List<ESP32Data> newData) {
        this.dataList = newData;
        notifyDataSetChanged();
    }
    
    static class DataViewHolder extends RecyclerView.ViewHolder {
        private TextView tvValue, tvTimestamp, tvIndex;
        
        public DataViewHolder(@NonNull View itemView) {
            super(itemView);
            tvValue = itemView.findViewById(R.id.tv_value);
            tvTimestamp = itemView.findViewById(R.id.tv_timestamp);
            tvIndex = itemView.findViewById(R.id.tv_index);
        }
        
        public void bind(ESP32Data data, int position) {
            try {
                // 验证数据有效性
                if (data.getAd1Value() >= 0) {
                    tvValue.setText("AD值: " + data.getAd1Value());
                } else {
                    tvValue.setText("AD值: 无效");
                }
                
                // 验证时间戳
                if (data.getTimestamp() > 0) {
                    tvTimestamp.setText("时间: " + data.getFormattedTimestamp());
                } else {
                    tvTimestamp.setText("时间: 无效");
                }
                
                tvIndex.setText("#" + (position + 1));
                
            } catch (Exception e) {
                Log.e(TAG, "绑定数据项失败", e);
                bindError("数据异常", position);
            }
        }
        
        public void bindError(String errorMessage, int position) {
            tvValue.setText("错误: " + errorMessage);
            tvTimestamp.setText("位置: " + (position + 1));
            tvIndex.setText("#" + (position + 1));
        }
    }
}
