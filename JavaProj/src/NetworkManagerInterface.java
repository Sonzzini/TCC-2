public interface NetworkManagerInterface {
    String fetchDataFromNetwork();
    void sendDataToNetwork(String data);
    Weather fetchCurrentWeather(String city, String country);
}
