package com.example.overcooked_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;

import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;

import android.widget.TextView;


public class FindData extends AppCompatActivity implements fetchData.AsyncResponse {
    public static TextView data;
    Button click;
    Button pop;
    public static EditText search;
    int recipeNo;
    public static int counter = 0;


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
        final Context context = this;
        recipeNo = fetchData.recNo;
        Button[] myButton = new Button[recipeNo];
        LinearLayout layout = (LinearLayout) findViewById(R.id.space_layout);

        for (int i = 0; i < recipeNo; i++) {

            myButton[i] = new Button(this);
            myButton[i].setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
            myButton[i].setText(fetchData.title[i]);
            layout.addView(myButton[i]);
            myButton[i].setId(i);

            myButton[i].setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    counter = view.getId();
                    startActivity(new Intent(FindData.this,Pop.class));

                }
            });

            SharedPreferences sharedPreferences = getSharedPreferences("overcooked_preferences",MODE_PRIVATE);
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.putString("text",output);
            editor.apply();

        }






    }
}
