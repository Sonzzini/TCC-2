import java.awt.*;
import java.awt.event.ActionEvent;
import javax.swing.*;

public class App {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                // Initialize the main application window
                JFrame frame = new JFrame("Weather Application");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                frame.setSize(400, 300);

                // Create instances of DataManager, NetworkManager, and ViewModel
                DataManager dataManager = new DataManager();
                NetworkManager networkManager = new NetworkManager();
                ViewModel viewModel = new ViewModel(dataManager, networkManager);

                // Create UI components
                JPanel panel = new JPanel(new GridLayout(4, 1));
                JLabel label = new JLabel("Weather Application", SwingConstants.CENTER);
                JButton fetchDataButton = new JButton("Fetch Data");
                JButton fetchNetworkDataButton = new JButton("Fetch Network Data");
                JButton fetchWeatherButton = new JButton("Fetch Weather");

                // Add action listeners to buttons
                fetchDataButton.addActionListener((ActionEvent e) -> {
                    String data = viewModel.getData();
                    JOptionPane.showMessageDialog(frame, "Data: " + data);
                });

                fetchNetworkDataButton.addActionListener((ActionEvent e) -> {
                    String networkData = viewModel.getNetworkData();
                    JOptionPane.showMessageDialog(frame, "Network Data: " + networkData);
                });

                fetchWeatherButton.addActionListener(e -> {
                    String city = "London"; // Example city
                    String country = "uk"; // Example country

                    Weather weather = networkManager.fetchCurrentWeather(city, country);
                    if (weather != null) {
                        if (!dataManager.isWeatherSaved(weather.getDate())) {
                            dataManager.saveWeather(weather);
                            JOptionPane.showMessageDialog(frame, "Weather data saved for: " + weather.getDate());
                        } else {
                            JOptionPane.showMessageDialog(frame, "Weather data for today is already saved.");
                        }
                    } else {
                        JOptionPane.showMessageDialog(frame, "Failed to fetch weather data.");
                    }
                });

                // Add components to the panel
                panel.add(label);
                panel.add(fetchDataButton);
                panel.add(fetchNetworkDataButton);
                panel.add(fetchWeatherButton);

                // Add panel to the frame
                frame.add(panel);

                // Make the frame visible
                frame.setVisible(true);
            } catch (Exception e) {
                LoggerManager.log("Error initializing the application: " + e.getMessage());
            }
        });
    }
}

