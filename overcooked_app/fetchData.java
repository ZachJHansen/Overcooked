package com.example.overcooked_app;



import android.os.AsyncTask;
import android.util.Log;
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
import java.util.ArrayList;
import java.util.List;

public class fetchData extends AsyncTask<Void,Void,String> {
    public static AsyncResponse delegate =null;
    String data = "";
    public static int recNo = 0;
    private String dataParsed  = "";
    String singleParsed = "";
    static String[] title = new String[20];
    static String[] ingredients = new String[20];
    static String[] instructions = new String[20];
    public static String ingredient;

    public static ArrayList<String> recipes = new ArrayList<>();

//    @Override
//    protected void onPreExecute() {
//        super.onPreExecute();
//        String
//    }

    public fetchData(AsyncResponse delegate){
        this.delegate = delegate;
    }

    @Override
    protected String doInBackground(Void... recipes) {
        try {
            String edit = FindData.search.getText().toString();
            String main_ingredient = "main_ingredient="+edit;
            URL url = new URL("http://10.0.2.2:5000/?"+main_ingredient);

            HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
            InputStream inputStream = httpURLConnection.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
            String line = "";
            while (line != null) {
                line = bufferedReader.readLine();
                data = data + line;
            }

            JSONArray JA = new JSONArray(data);
            Log.i("JSONArray",data);
            Log.i("JSONArray","" + JA.length());
            for (int i = 0;i<JA.length(); i++){
                JSONObject JO = (JSONObject) JA.get(i);

                title[i] = (String) JO.get("title");
                ingredients[i] = (String) JO.get("ingredients");
                instructions[i] = (String) JO.get("instructions");
                recNo++;

            }

            return dataParsed;


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
    protected void onPostExecute(String result) {
        super.onPostExecute(result);


        delegate.processFinish(result);





    }

    public interface AsyncResponse {
        void processFinish(String output);
    }

}
