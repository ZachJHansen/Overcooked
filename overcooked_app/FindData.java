package com.example.overcooked_app;

import androidx.appcompat.app.AppCompatActivity;


import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.Editable;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class FindData extends AppCompatActivity implements fetchData.AsyncResponse {
    public static TextView data;
    Button click;
    public static EditText search;
    int recipeNo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_find_data);

        click = (Button) findViewById(R.id.search_button);

        search=(EditText) findViewById(R.id.search_bar);

        fetchData.delegate = this;


        click.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                fetchData process = new fetchData(fetchData.delegate);
                process.execute();



            }
        });
    }


    @Override
    public void processFinish(String output) {

        recipeNo = fetchData.recNo;

        LinearLayout layout = (LinearLayout) findViewById(R.id.space_layout);
        for (int i = 0; i < recipeNo; i++) {
            Button myButton = new Button(this);
            myButton.setId(i);
            myButton.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
            myButton.setText(fetchData.both[i]);
            layout.addView(myButton);


        }

        for (int i = 0; i<recipeNo; i++) {

        }

        SharedPreferences sharedPreferences = getSharedPreferences("overcooked_preferences",MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("text",output);
        editor.apply();
    }
}
