package com.example.aiiot.adapter;

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
        ESP32Data data = dataList.get(position);
        holder.bind(data);
    }
    
    @Override
    public int getItemCount() {
        return dataList.size();
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
        
        public void bind(ESP32Data data) {
            tvValue.setText("AD值: " + data.getAd1Value());
            tvTimestamp.setText("时间: " + data.getFormattedTimestamp());
            tvIndex.setText("#" + (getAdapterPosition() + 1));
        }
    }
}
