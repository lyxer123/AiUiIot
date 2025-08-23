package com.esp32.control.adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.esp32.control.R;
import com.esp32.control.model.AD1Data;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class DataAdapter extends RecyclerView.Adapter<DataAdapter.DataViewHolder> {
    
    private List<AD1Data> dataList;
    
    public DataAdapter(List<AD1Data> dataList) {
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
        AD1Data data = dataList.get(position);
        holder.bind(data);
    }
    
    @Override
    public int getItemCount() {
        return dataList.size();
    }
    
    public void updateData(List<AD1Data> newDataList) {
        this.dataList = newDataList;
        notifyDataSetChanged();
    }
    
    static class DataViewHolder extends RecyclerView.ViewHolder {
        private TextView tvValue, tvTimestamp, tvId;
        
        public DataViewHolder(@NonNull View itemView) {
            super(itemView);
            tvValue = itemView.findViewById(R.id.tv_value);
            tvTimestamp = itemView.findViewById(R.id.tv_timestamp);
            tvId = itemView.findViewById(R.id.tv_id);
        }
        
        public void bind(AD1Data data) {
            tvId.setText("ID: " + data.getId());
            tvValue.setText(String.format(Locale.getDefault(), "%.2f", data.getValue()));
            tvTimestamp.setText(formatTimestamp(data.getTimestamp()));
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
}
