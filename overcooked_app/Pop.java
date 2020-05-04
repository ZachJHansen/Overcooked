package com.example.overcooked_app;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.widget.TextView;

public class Pop extends Activity {
    public static TextView popTitle;
    public static TextView recipe;
    String popMess;

    @Override
    protected void onCreate (Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.popwindow);
        popTitle = (TextView) findViewById(R.id.title);
        recipe = (TextView) findViewById(R.id.popup);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        SharedPreferences sharedPreferences = getSharedPreferences("overcooked_preferences",MODE_PRIVATE);


        popMess = fetchData.ingredients[FindData.counter]+"\n\n"+fetchData.instructions[FindData.counter];
        popTitle.setText(fetchData.title[FindData.counter]);
        recipe.setText(popMess);
        int width = dm.widthPixels;
        int height = dm.heightPixels;

        getWindow().setLayout((int)(width*0.8),(int)(height*0.8));


    }
}
