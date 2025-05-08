import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;

public class DataManager implements DataManagerInterface {
    private static final String DB_URL = "jdbc:sqlite:lib/database.db";

    public DataManager() {
        // Initialize the database (create tables if they don't exist)
        try (Connection connection = DriverManager.getConnection(DB_URL)) {
            String createTableSQL = "CREATE TABLE IF NOT EXISTS weather (" +
                    "date TEXT PRIMARY KEY, " +
                    "temperature REAL, " +
                    "feels_like REAL, " +
                    "pressure INTEGER, " +
                    "humidity INTEGER, " +
                    "clouds INTEGER, " +
                    "visibility INTEGER);";
            try (PreparedStatement statement = connection.prepareStatement(createTableSQL)) {
                statement.execute();
            }
        } catch (SQLException e) {
            LoggerManager.log("Error initializing database: " + e.getMessage());
        }
    }

    public boolean isWeatherSaved(LocalDate date) {
        String query = "SELECT 1 FROM weather WHERE date = ?";
        try (Connection connection = DriverManager.getConnection(DB_URL);
             PreparedStatement statement = connection.prepareStatement(query)) {
            statement.setString(1, date.toString());
            try (ResultSet resultSet = statement.executeQuery()) {
                return resultSet.next();
            }
        } catch (SQLException e) {
            LoggerManager.log("Error checking weather in database: " + e.getMessage());
        }
        return false;
    }

    public void saveWeather(Weather weather) {
        String insertSQL = "INSERT INTO weather (date, temperature, feels_like, pressure, humidity, clouds, visibility) " +
                "VALUES (?, ?, ?, ?, ?, ?, ?)";
        try (Connection connection = DriverManager.getConnection(DB_URL);
             PreparedStatement statement = connection.prepareStatement(insertSQL)) {
            statement.setString(1, weather.getDate().toString());
            statement.setDouble(2, weather.getTemperature());
            statement.setDouble(3, weather.getFeelsLike());
            statement.setInt(4, weather.getPressure());
            statement.setInt(5, weather.getHumidity());
            statement.setInt(6, weather.getClouds());
            statement.setInt(7, weather.getVisibility());
            statement.executeUpdate();
        } catch (SQLException e) {
            LoggerManager.log("Error saving weather to database: " + e.getMessage());
        }
    }

    @Override
    public String fetchData() {
        // Placeholder for fetching data from the database
        LoggerManager.log("Fetching data from database...");
        return "Sample Data from Database";
    }

    @Override
    public void saveData(String data) {
        // Placeholder for saving data to the database
        LoggerManager.log("Saving data to database: " + data);
    }
}

