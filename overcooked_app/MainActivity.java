package com.example.overcooked_app;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }



    public void findRecipe (View view)
    {

        startActivity(new Intent(this,FindData.class));
    }

    public void shoppingList (View view)
    {
        startActivity(new Intent(this,ShoppingList.class));
    }

}
