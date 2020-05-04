package com.example.overcooked_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MealPlan extends AppCompatActivity implements generatePlan.AsyncResponse {
    Button click;
    public static TextView data;
    int genNo;
    public static int counter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_meal_plan);

        click = (Button) findViewById(R.id.generate);
        generatePlan.delegate = this;
        click.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                generatePlan process = new generatePlan(generatePlan.delegate);
                process.execute();



            }
        });


    }



    @Override
    public void processFinish() {
        final Context context = this;
        genNo = fetchData.recNo;
        Button[] myButton = new Button[genNo];
        int size = myButton.length;
        LinearLayout layout = (LinearLayout) findViewById(R.id.space_layout);
        for (int i = size - 1; i >= genNo; i--) {
            myButton[i].setVisibility(View.GONE);
        }
        for (int i = 0; i < genNo; i++) {

            myButton[i] = new Button(this);
            myButton[i].setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
            myButton[i].setText(fetchData.title[i]);
            layout.addView(myButton[i]);
            myButton[i].setId(i);

            myButton[i].setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    counter = view.getId();
                    startActivity(new Intent(MealPlan.this, Pop.class));

                }

            });


        }
    }


}
