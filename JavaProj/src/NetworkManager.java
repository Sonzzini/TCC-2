import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import org.json.JSONObject;

public class NetworkManager implements NetworkManagerInterface {
    private static final String API_URL = "https://api.openweathermap.org/data/2.5/weather";
    private static final String API_KEY = "b97d9686bcb826e156916739bd49136c";

    @Override
    public String fetchDataFromNetwork() {
        // Placeholder for network operations (e.g., API calls)
        LoggerManager.log("Fetching data from network...");
        return "Network Data";
    }

    @Override
    public void sendDataToNetwork(String data) {
        // Placeholder for sending data over the network
        LoggerManager.log("Sending data to network: " + data);
    }

    @Override
    public Weather fetchCurrentWeather(String city, String country) {
        try {
            String urlString = String.format("%s?q=%s,%s&APPID=%s", API_URL, city, country, API_KEY);
            URL url = new URL(urlString);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            int responseCode = connection.getResponseCode();
            if (responseCode == 200) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = in.readLine()) != null) {
                    response.append(line);
                }
                in.close();

                JSONObject jsonResponse = new JSONObject(response.toString());
                JSONObject main = jsonResponse.getJSONObject("main");
                JSONObject weatherDetails = jsonResponse.getJSONArray("weather").getJSONObject(0);

                double temp = main.getDouble("temp");
                double feelsLike = main.getDouble("feels_like");
                int pressure = main.getInt("pressure");
                int humidity = main.getInt("humidity");
                int clouds = jsonResponse.getJSONObject("clouds").getInt("all");
                int visibility = jsonResponse.getInt("visibility");
                LocalDate date = LocalDate.now();

                return new Weather(temp, feelsLike, pressure, humidity, clouds, visibility, date);
            } else {
                LoggerManager.log("Failed to fetch weather data. Response code: " + responseCode);
            }
        } catch (Exception e) {
            LoggerManager.log("Error fetching weather data: " + e.getMessage());
        }
        return null;
    }
}
