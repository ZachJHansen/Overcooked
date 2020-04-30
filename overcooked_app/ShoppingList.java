package com.example.overcooked_app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class ShoppingList extends AppCompatActivity {
    public static TextView ingr;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_shopping_list);

        ingr=(TextView) findViewById(R.id.ingredient);


    }
}
