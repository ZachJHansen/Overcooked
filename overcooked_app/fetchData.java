package com.example.overcooked_app;

import android.os.AsyncTask;
import android.widget.Button;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import static com.example.overcooked_app.ShoppingList.ingr;

public class fetchData extends AsyncTask<Void,Void,Void> {
    String data = "";
    String dataParsed = "";
    String singleParsed = "";
    String both = "";
    @Override
    protected Void doInBackground(Void... voids) {
        try {
            URL url = new URL("http://10.0.2.2:5000/");

            HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
            InputStream inputStream = httpURLConnection.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
            String line = "";
            while (line != null) {
                line = bufferedReader.readLine();
                data = data + line;
            }

            JSONArray JA = new JSONArray(data);

            for (int i = 0;i<JA.length(); i++){
                JSONObject JO = (JSONObject) JA.get(i);
                singleParsed = "Calories: " + JO.get("calories") + "\n" +
                                "Main_ingredient: " + JO.get("main_ingredient") + "\n" +
                                "complexity: " + JO.get("complexity") + "\n" +
                                "recipe_id: " + JO.get("recipe_id") + "\n" +
                                "Time: " + JO.get("time") + "\n" +
                                "Restrictions: " + JO.get("restrictions");
                dataParsed = dataParsed + singleParsed;
                both = (String) JO.get("main_ingredient");
            }


        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }

        return null;
    }

    @Override
    protected void onPostExecute(Void aVoid) {
        super.onPostExecute(aVoid);
        Button button;

        FindData.data.setText(this.both);
        

    }
}
